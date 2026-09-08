"""Prometheus metrics. Names are stable; dashboards/alerts depend on them."""
from __future__ import annotations

from prometheus_client import Counter, Histogram

jobs_fetched_total = Counter(
    "jobs_fetched_total", "Jobs fetched from a source", ["source"]
)
jobs_scored_total = Counter(
    "jobs_scored_total", "Jobs scored", ["tier", "outcome"]
)
claude_request_duration_seconds = Histogram(
    "claude_request_duration_seconds", "Latency of a Claude scoring request"
)
claude_cache_hit_ratio = Histogram(
    "claude_cache_hit_ratio", "Prompt cache hit ratio per request", buckets=[0, 0.25, 0.5, 0.75, 1.0]
)
pipeline_run_duration_seconds = Histogram(
    "pipeline_run_duration_seconds", "Duration of a full pipeline run"
)
pipeline_errors_total = Counter(
    "pipeline_errors_total", "Errors during a pipeline run", ["stage"]
)
