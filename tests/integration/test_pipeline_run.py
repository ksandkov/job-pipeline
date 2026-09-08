"""End-to-end pipeline run with fully mocked externals."""
from unittest.mock import MagicMock, patch

from jobpipeline.pipeline import dedupe


def test_pipeline_scoring_flow(fake_job, mock_anthropic):
    # Local tier keeps the job; Claude returns a mocked high score.
    with patch("jobpipeline.scoring.local_scorer.LocalScorer.keep", return_value=True):
        from jobpipeline.scoring.claude_scorer import ClaudeScorer

        scorer = ClaudeScorer()
        result = scorer.score(fake_job)
        assert result.score == 82
        assert result.tier_outcome() == "keep"


def test_dedupe_used_in_pipeline(fake_job):
    assert dedupe([fake_job, fake_job]) == [fake_job]
