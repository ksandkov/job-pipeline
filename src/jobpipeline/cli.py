"""Command-line entrypoint: `jobpipeline run`, `jobpipeline stats`."""
from __future__ import annotations

import typer

from .config import settings
from .db.session import session_scope
from .db.models import Job
from .pipeline import run as run_pipeline
from .scrapers.hiringcafe_source import HiringCafeSource
from .scrapers.jobspy_source import JobSpySource

app = typer.Typer(help="job-pipeline CLI")


@app.command()
def run() -> None:
    """Run one full pipeline pass."""
    scrapers = [
        JobSpySource(
            search_term=settings.jobspy_search_term,
            location=settings.jobspy_location,
            results=settings.jobspy_results,
        ),
        HiringCafeSource(search_term=settings.jobspy_search_term),
    ]
    stored = run_pipeline(scrapers)
    typer.echo(f"stored {stored} jobs")


@app.command()
def stats() -> None:
    """Print quick counts from the database."""
    with session_scope() as db:
        total = db.query(Job).count()
    typer.echo(f"jobs in db: {total}")


if __name__ == "__main__":
    app()
