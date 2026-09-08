"""Shared fixtures: in-memory DB and a mocked Anthropic client."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest


@pytest.fixture
def fake_job() -> dict:
    return {
        "title": "Senior Platform Engineer",
        "company": "Acme",
        "location": "Remote",
        "url": "https://example.com/job/1",
        "description": "Kubernetes, Terraform, CI/CD, observability.",
    }


@pytest.fixture
def mock_anthropic(monkeypatch):
    """Patch the Anthropic client so scoring tests never hit the network."""
    fake_msg = MagicMock()
    text_block = MagicMock()
    text_block.type = "text"
    text_block.text = (
        '{"score":82,"archetype":28,"must_haves":26,'
        '"experience":20,"domain":8,"rationale":"Strong platform fit."}'
    )
    fake_msg.content = [text_block]
    fake_msg.usage = MagicMock(
        cache_read_input_tokens=100, cache_creation_input_tokens=0, input_tokens=50
    )
    client = MagicMock()
    client.messages.create.return_value = fake_msg
    monkeypatch.setattr("jobpipeline.scoring.claude_scorer.Anthropic", lambda **_: client)
    return client
