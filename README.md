# job-pipeline

Scrapes job postings from multiple sources, scores each one for fit with an LLM
(local model first, then Claude), stores the results in Postgres, and serves the
good ones over an API and a small web UI. This is the app I actually use to find
roles — it doubles as my reference "production Python service".

[![ci](https://github.com/ksandkov/job-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/ksandkov/job-pipeline/actions/workflows/ci.yml)

## Problem
Job boards are noisy. Reading every posting is slow, and keyword filters are
dumb. I want a pipeline that pulls postings, throws away the obvious noise
cheaply, then spends real model budget only on the plausible ones — and shows me
a ranked shortlist with a one-line rationale.

## Architecture
```
scrapers (JobSpy, hiring.cafe) → dedupe → LocalScorer (Qwen/Ollama, fail-open)
    → ClaudeScorer (Haiku + prompt caching) → Postgres → FastAPI /jobs + UI
                                                              └► /metrics (Prometheus)
```
See `docs/architecture.md` for the full diagram and `docs/metrics.md` for the
metrics contract that the `observability` repo depends on.

## Key decisions (and why)
- **Tiered scoring** — cheap local filter before Claude saves tokens. ADR 0003.
- **Prompt caching** — the big rubric is cached across calls. ADR 0002.
- **Postgres** — real concurrency + a meaningful `/readyz`. ADR 0001.
- **`/healthz` vs `/readyz`** — liveness never touches the DB; readiness does, so
  k8s only sends traffic when the DB is actually reachable.

## Run it
```bash
cp .env.example .env                            # set ANTHROPIC_API_KEY; use @postgres:5432 as the DB host for compose
docker compose up -d --build                    # app + postgres
docker compose exec app alembic upgrade head    # create tables
docker compose exec app jobpipeline run         # one pipeline pass
open http://localhost:8000/                     # ranked shortlist
```
Local dev without Docker:
```bash
make dev && make migrate && make run
make test && make lint
```

## What broke and how I fixed it
- **hiring.cafe blocked plain requests.** It's a Next.js app behind bot
  detection; a normal `requests` call got 403s. Fixed by using `curl_cffi` to
  impersonate a real browser TLS fingerprint and reading the `_next/data` JSON.
- **A down Ollama silently dropped every job.** The local filter now *fails
  open* — if it can't reach the model, jobs pass through to Claude instead of
  being discarded.

## What I'd do differently
- Persist a `Run` row per execution (model exists) and alert off it directly.
- Add a proper job-detail page instead of just the ranked table.
- Cache scraped descriptions to re-score without re-fetching.

## Layout
- `src/jobpipeline/scrapers` — sources (Scraper protocol).
- `src/jobpipeline/scoring` — local + Claude scorers, rubric, schema.
- `src/jobpipeline/api` — health, jobs, UI routers.
- `src/jobpipeline/db` — models + session.
- `migrations/` — Alembic.
- `docs/` — architecture, metrics, ADRs.
