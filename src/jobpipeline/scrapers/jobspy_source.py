"""Fetch jobs from LinkedIn/Indeed/etc via the JobSpy library."""
from __future__ import annotations

from ..logging import get_logger

log = get_logger(__name__)


class JobSpySource:
    name = "jobspy"

    def __init__(self, search_term: str, location: str, results: int = 50) -> None:
        self.search_term = search_term
        self.location = location
        self.results = results

    def fetch(self) -> list[dict]:
        # Imported lazily so tests can run without the heavy dependency installed.
        from jobspy import scrape_jobs  # type: ignore

        df = scrape_jobs(
            site_name=["linkedin", "indeed"],
            search_term=self.search_term,
            location=self.location,
            results_wanted=self.results,
        )
        jobs = [
            {
                "title": r.get("title"),
                "company": r.get("company"),
                "location": r.get("location"),
                "url": r.get("job_url"),
                "description": r.get("description") or "",
            }
            for r in df.to_dict("records")
        ]
        log.info("jobspy_fetched", count=len(jobs))
        return jobs
