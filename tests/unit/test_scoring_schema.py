import pytest
from pydantic import ValidationError

from jobpipeline.scoring.schema import ScoreResult


def test_valid_score():
    r = ScoreResult(
        score=80, archetype=28, must_haves=26, experience=18, domain=8, rationale="ok"
    )
    assert r.tier_outcome() == "keep"


def test_score_out_of_range():
    with pytest.raises(ValidationError):
        ScoreResult(score=200, archetype=0, must_haves=0, experience=0, domain=0, rationale="x")


def test_low_score_drops():
    r = ScoreResult(score=40, archetype=10, must_haves=10, experience=10, domain=5, rationale="meh")
    assert r.tier_outcome() == "drop"
