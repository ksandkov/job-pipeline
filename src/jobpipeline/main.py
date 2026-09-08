"""FastAPI application factory."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_client import make_asgi_app

from .api import health, jobs, ui
from .logging import configure_logging, get_logger

log = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    log.info("startup")
    yield
    log.info("shutdown")


def create_app() -> FastAPI:
    app = FastAPI(title="job-pipeline", version="0.1.0", lifespan=lifespan)
    app.include_router(health.router)
    app.include_router(jobs.router)
    app.include_router(ui.router)
    # /metrics for Prometheus
    app.mount("/metrics", make_asgi_app())
    return app


app = create_app()
