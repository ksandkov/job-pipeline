"""SQLAlchemy models: jobs, scores, runs."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(512))
    company: Mapped[str] = mapped_column(String(256))
    location: Mapped[str] = mapped_column(String(256), default="")
    url: Mapped[str] = mapped_column(String(1024), unique=True)
    description: Mapped[str] = mapped_column(Text, default="")
    score: Mapped[int] = mapped_column(Integer, default=0, index=True)
    rationale: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    @classmethod
    def from_scored(cls, job: dict, score) -> Job:
        """Build a Job row from a scraped dict + a ScoreResult."""
        return cls(
            title=job.get("title") or "",
            company=job.get("company") or "",
            location=job.get("location") or "",
            url=job.get("url") or "",
            description=job.get("description") or "",
            score=getattr(score, "score", 0),
            rationale=getattr(score, "rationale", ""),
        )

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "url": self.url,
            "score": self.score,
            "rationale": self.rationale,
        }


class Run(Base):
    __tablename__ = "runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    stored: Mapped[int] = mapped_column(Integer, default=0)
    ok: Mapped[int] = mapped_column(Integer, default=1)  # 1 ok, 0 failed
