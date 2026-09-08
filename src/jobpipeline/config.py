"""Application settings, loaded from environment / .env via pydantic-settings."""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Database
    database_url: str = "postgresql+psycopg://jobpipeline:jobpipeline@localhost:5432/jobpipeline"

    # Anthropic
    anthropic_api_key: str = ""
    claude_model: str = "claude-haiku-4-5-20251001"
    claude_temperature: float = 0.3

    # Local tier
    ollama_base_url: str = "http://localhost:11434"
    local_model: str = "qwen2.5:7b"
    enable_local_tier: bool = True

    # Scrapers
    jobspy_search_term: str = "platform engineer"
    jobspy_location: str = "Toronto, ON"
    jobspy_results: int = 50

    # App
    log_level: str = "INFO"


# Import this singleton everywhere instead of re-reading the environment.
settings = Settings()
