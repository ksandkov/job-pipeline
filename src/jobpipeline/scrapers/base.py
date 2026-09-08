"""Scraper interface. Each source returns a list of normalized job dicts."""
from __future__ import annotations

from typing import Protocol


class Scraper(Protocol):
    name: str

    def fetch(self) -> list[dict]:
        """Return normalized jobs: {title, company, location, url, description}."""
        ...
