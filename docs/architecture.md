# Architecture

```
 ┌────────────┐   ┌────────────┐
 │ JobSpy      │   │ hiring.cafe │      scrapers/  (Scraper protocol)
 │ (LinkedIn,  │   │ (_next/data)│
 │  Indeed)    │   │  curl_cffi  │
 └─────┬───────┘   └─────┬───────┘
       └──────┬──────────┘
              ▼
          dedupe                         pipeline.py
              ▼
     ┌─────────────────┐  keep?
     │ LocalScorer     │────────► drop
     │ (Qwen/Ollama)   │  (fail-open if Ollama down)
     └────────┬────────┘
              ▼ keep
     ┌─────────────────┐
     │ ClaudeScorer    │  Haiku + prompt caching (rubric cached)
     │ → ScoreResult   │
     └────────┬────────┘
              ▼
          Postgres (jobs, runs)          db/
              ▼
      FastAPI  /jobs  /healthz /readyz /metrics   api/
              ▼
          HTML UI (/)
```

## Why tiered scoring
The local model is free and fast but coarse; Claude is precise but costs
tokens. Filtering obvious non-matches locally means Claude only scores the
plausible ones. See ADR 0003.
