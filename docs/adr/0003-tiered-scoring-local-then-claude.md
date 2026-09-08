# ADR 0003: Tiered scoring (local model, then Claude)

## Status
Accepted

## Context
Scoring every scraped job with Claude is precise but costs tokens on a lot of
obvious non-matches.

## Decision
Run a cheap local Qwen (via Ollama) YES/NO relevance filter first; only jobs
that pass go to Claude. The local tier fails open — if Ollama is down, jobs pass
through rather than being silently dropped.

## Consequences
- Significant token savings on irrelevant jobs.
- Two models to reason about; the local tier can have false negatives, mitigated
  by fail-open and by keeping its prompt permissive.
