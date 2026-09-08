"""Liveness and readiness endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Response, status
from sqlalchemy import text

from ..db.session import engine

router = APIRouter(tags=["health"])


@router.get("/healthz")
def healthz() -> dict:
    """Liveness: the process is up."""
    return {"status": "ok"}


@router.get("/readyz")
def readyz(response: Response) -> dict:
    """Readiness: the database is reachable."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ready"}
    except Exception:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "not-ready"}
