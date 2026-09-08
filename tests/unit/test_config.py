from jobpipeline.config import Settings


def test_defaults_load():
    s = Settings()
    assert s.claude_model.startswith("claude")
    assert 0.0 <= s.claude_temperature <= 1.0
