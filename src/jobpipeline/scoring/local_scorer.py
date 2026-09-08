"""First-tier local scorer (Qwen via Ollama).

Cheap pass to discard obviously-irrelevant jobs before spending Claude tokens.
Falls open (keeps the job) if the local tier is disabled or unreachable, so a
broken Ollama never silently drops everything.
"""

from __future__ import annotations

import httpx

from ..config import settings
from ..logging import get_logger
from ..metrics import jobs_scored_total

log = get_logger(__name__)

_PROMPT = (
    "You are a fast relevance filter. Answer only YES or NO: is this job "
    "plausibly a Platform/SRE/DevOps/Infra role for a mid-senior engineer?\n\n"
    "Title: {title}\nCompany: {company}\n\n{description}"
)


class LocalScorer:
    def __init__(self) -> None:
        self.enabled = settings.enable_local_tier

    def keep(self, job: dict) -> bool:
        """Return True if the job should proceed to Claude scoring."""
        if not self.enabled:
            return True
        try:
            resp = httpx.post(
                f"{settings.ollama_base_url}/api/generate",
                json={
                    "model": settings.local_model,
                    "prompt": _PROMPT.format(
                        title=job.get("title", ""),
                        company=job.get("company", ""),
                        description=(job.get("description") or "")[:2000],
                    ),
                    "stream": False,
                },
                timeout=30,
            )
            resp.raise_for_status()
            answer = resp.json().get("response", "").strip().upper()
            outcome = "keep" if answer.startswith("Y") else "drop"
            jobs_scored_total.labels(tier="local", outcome=outcome).inc()
            return outcome == "keep"
        except Exception:
            # Fail open: don't lose jobs because the local tier is down.
            log.warning("local_scorer_unavailable_fail_open", exc_info=True)
            return True
