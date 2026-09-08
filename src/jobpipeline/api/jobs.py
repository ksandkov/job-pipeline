"""Read API for scored jobs."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..db.models import Job
from ..db.session import get_db

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("")
def list_jobs(
    min_score: int = Query(0, ge=0, le=100),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
) -> list[dict]:
    """List jobs above a score threshold, most relevant first."""
    rows = (
        db.query(Job)
        .filter(Job.score >= min_score)
        .order_by(Job.score.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return [r.as_dict() for r in rows]
