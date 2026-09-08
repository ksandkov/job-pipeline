"""Second-tier scorer using Anthropic Claude with prompt caching.

The system rubric is large and identical across calls, so it is marked with
cache_control to cut cost/latency on every request after the first.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

from anthropic import Anthropic

from ..config import settings
from ..logging import get_logger
from ..metrics import (
    claude_cache_hit_ratio,
    claude_request_duration_seconds,
    jobs_scored_total,
)
from .schema import ScoreResult

log = get_logger(__name__)

_SYSTEM = (Path(__file__).parent / "prompts" / "system.md").read_text(encoding="utf-8")

_SCHEMA_HINT = (
    'Return ONLY JSON: {"score":int,"archetype":int,"must_haves":int,'
    '"experience":int,"domain":int,"rationale":str}'
)


class ClaudeScorer:
    def __init__(self) -> None:
        self._client = Anthropic(api_key=settings.anthropic_api_key)

    def score(self, job: dict) -> ScoreResult:
        started = time.monotonic()
        try:
            msg = self._client.messages.create(
                model=settings.claude_model,
                max_tokens=400,
                temperature=settings.claude_temperature,
                system=[
                    {
                        "type": "text",
                        "text": _SYSTEM,
                        # Cache the big, static rubric across requests.
                        "cache_control": {"type": "ephemeral"},
                    },
                    {"type": "text", "text": _SCHEMA_HINT},
                ],
                messages=[
                    {
                        "role": "user",
                        "content": (
                            f"Title: {job.get('title')}\n"
                            f"Company: {job.get('company')}\n"
                            f"Location: {job.get('location')}\n\n"
                            f"{(job.get('description') or '')[:6000]}"
                        ),
                    }
                ],
            )
            self._record_cache(msg)
            text = "".join(b.text for b in msg.content if b.type == "text")
            result = ScoreResult(**json.loads(_strip_fences(text)))
            jobs_scored_total.labels(tier="claude", outcome=result.tier_outcome()).inc()
            return result
        finally:
            claude_request_duration_seconds.observe(time.monotonic() - started)

    @staticmethod
    def _record_cache(msg) -> None:
        u = getattr(msg, "usage", None)
        if not u:
            return
        read = getattr(u, "cache_read_input_tokens", 0) or 0
        created = getattr(u, "cache_creation_input_tokens", 0) or 0
        total = read + created + (getattr(u, "input_tokens", 0) or 0)
        if total:
            claude_cache_hit_ratio.observe(read / total)


def _strip_fences(text: str) -> str:
    return text.replace("```json", "").replace("```", "").strip()
