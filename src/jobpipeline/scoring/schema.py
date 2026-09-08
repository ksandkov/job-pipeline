"""Pydantic model for a scoring result."""
from __future__ import annotations

from pydantic import BaseModel, Field


class ScoreResult(BaseModel):
    score: int = Field(ge=0, le=100, description="Overall 0-100 fit score.")
    archetype: int = Field(ge=0, le=30)
    must_haves: int = Field(ge=0, le=30)
    experience: int = Field(ge=0, le=25)
    domain: int = Field(ge=0, le=15)
    rationale: str = Field(description="One or two sentences.")

    def tier_outcome(self, threshold: int = 60) -> str:
        return "keep" if self.score >= threshold else "drop"
