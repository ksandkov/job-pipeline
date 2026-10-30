# Metrics

Recorded by `jobpipeline run`. It is a short-lived process, so these metrics do not appear on the
API's `/metrics` endpoint; collecting them would need a Prometheus Pushgateway (not set up yet).

| Metric | Type | Meaning |
| ------ | ---- | ------- |
| `jobs_fetched_total{source}` | counter | Volume per source; a sudden drop = a scraper broke. |
| `jobs_scored_total{tier,outcome}` | counter | Local vs Claude, keep vs drop. Tier funnel. |
| `claude_request_duration_seconds` | histogram | Scoring latency. |
| `claude_cache_hit_ratio` | histogram | Prompt-cache effectiveness (cost signal). |
| `pipeline_run_duration_seconds` | histogram | End-to-end run time. |
| `pipeline_errors_total{stage}` | counter | Errors by stage. |

Keep these names stable: dashboards and alert rules that use them break when a name changes.
