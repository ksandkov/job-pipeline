# ADR 0002: Prompt caching for the scoring rubric

## Status
Accepted

## Context
The scoring rubric (system prompt) is large and identical on every call. Sending
it fresh each time wastes tokens and latency.

## Decision
Mark the rubric with `cache_control: ephemeral` so Claude caches it. Track the
cache hit ratio as a metric.

## Consequences
- Cheaper and faster after the first call in a window.
- Must keep the cached block stable; changing it invalidates the cache.
