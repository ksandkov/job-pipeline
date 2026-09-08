"""Fetch jobs from hiring.cafe via its _next/data endpoint.

hiring.cafe is a Next.js app; the JSON behind each page lives at a
`/_next/data/<build-id>/...json` URL. We use curl_cffi to mimic a browser TLS
fingerprint, since a plain requests call gets blocked.
"""
from __future__ import annotations

from ..logging import get_logger

log = get_logger(__name__)

_BASE = "https://hiring.cafe"


class HiringCafeSource:
    name = "hiringcafe"

    def __init__(self, search_term: str) -> None:
        self.search_term = search_term

    def fetch(self) -> list[dict]:
        from curl_cffi import requests as cffi  # type: ignore

        # NOTE: the _next build id changes on each deploy; resolve it from the
        # homepage rather than hardcoding. Left as TODO to keep the example lean.
        try:
            resp = cffi.get(
                f"{_BASE}/api/search",  # TODO: confirm current endpoint
                params={"q": self.search_term},
                impersonate="chrome",
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json()
        except Exception:
            log.warning("hiringcafe_fetch_failed", exc_info=True)
            return []

        jobs = [
            {
                "title": item.get("title"),
                "company": item.get("company"),
                "location": item.get("location"),
                "url": item.get("url"),
                "description": item.get("description") or "",
            }
            for item in data.get("results", [])
        ]
        log.info("hiringcafe_fetched", count=len(jobs))
        return jobs
