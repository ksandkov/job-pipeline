"""Minimal HTML view of the top jobs (ported from the old Flask app)."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from ..db.models import Job
from ..db.session import get_db

router = APIRouter(tags=["ui"])


@router.get("/", response_class=HTMLResponse)
def index(db: Session = Depends(get_db)) -> str:
    top = db.query(Job).order_by(Job.score.desc()).limit(25).all()
    rows = "".join(
        f"<tr><td>{j.score}</td><td>{j.title}</td>"
        f"<td>{j.company}</td><td>{j.location}</td>"
        f'<td><a href="{j.url}">link</a></td></tr>'
        for j in top
    )
    return f"""<!doctype html>
<html><head><title>job-pipeline</title>
<style>body{{font-family:sans-serif;margin:2rem}}table{{border-collapse:collapse}}
td,th{{border:1px solid #ddd;padding:.4rem .6rem}}</style></head>
<body><h1>Top scored jobs</h1>
<table><tr><th>Score</th><th>Title</th><th>Company</th><th>Location</th><th></th></tr>
{rows}</table></body></html>"""
