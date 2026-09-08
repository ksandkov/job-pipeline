# Metrics

Exposed at `/metrics` (Prometheus format).

| Metric | Type | Meaning / SLO use |
| ------ | ---- | ----------------- |
| `jobs_fetched_total{source}` | counter | Volume per source; a sudden drop = a scraper broke. |
| `jobs_scored_total{tier,outcome}` | counter | Local vs Claude, keep vs drop. Tier funnel. |
| `claude_request_duration_seconds` | histogram | Scoring latency; feeds latency SLO. |
| `claude_cache_hit_ratio` | histogram | Prompt-cache effectiveness (cost signal). |
| `pipeline_run_duration_seconds` | histogram | End-to-end run time. |
| `pipeline_errors_total{stage}` | counter | Errors by stage; drives the "no run in 24h" alert. |

These names are stable contracts — the `observability` repo's alert rules and
dashboards reference them directly.
