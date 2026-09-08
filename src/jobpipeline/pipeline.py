"""Orchestrate one pipeline run: fetch -> dedupe -> score -> store."""
from __future__ import annotations

import time

from .db.models import Job
from .db.session import session_scope
from .logging import get_logger
from .metrics import (
    jobs_fetched_total,
    pipeline_errors_total,
    pipeline_run_duration_seconds,
)
from .scoring.claude_scorer import ClaudeScorer
from .scoring.local_scorer import LocalScorer
from .scrapers.base import Scraper

log = get_logger(__name__)


def dedupe(jobs: list[dict]) -> list[dict]:
    """Drop duplicates by (title, company, location)."""
    seen: set[tuple] = set()
    out: list[dict] = []
    for j in jobs:
        key = (j.get("title"), j.get("company"), j.get("location"))
        if key not in seen:
            seen.add(key)
            out.append(j)
    return out


def run(scrapers: list[Scraper]) -> int:
    """Run the pipeline once. Returns the number of jobs stored."""
    started = time.monotonic()
    stored = 0
    try:
        raw: list[dict] = []
        for scraper in scrapers:
            fetched = scraper.fetch()
            jobs_fetched_total.labels(source=scraper.name).inc(len(fetched))
            raw.extend(fetched)

        jobs = dedupe(raw)

        local = LocalScorer()
        claude = ClaudeScorer()
        with session_scope() as db:
            for job in jobs:
                # Tiered scoring: cheap local pass first, Claude only if it survives.
                if not local.keep(job):
                    continue
                score = claude.score(job)
                db.merge(Job.from_scored(job, score))
                stored += 1
        return stored
    except Exception:
        pipeline_errors_total.labels(stage="run").inc()
        log.exception("pipeline_run_failed")
        raise
    finally:
        pipeline_run_duration_seconds.observe(time.monotonic() - started)
        log.info("pipeline_run_complete", stored=stored)
