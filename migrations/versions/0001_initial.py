"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-01-01
"""

import sqlalchemy as sa
from alembic import op

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "jobs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String(512), nullable=False),
        sa.Column("company", sa.String(256), nullable=False),
        sa.Column("location", sa.String(256), server_default=""),
        sa.Column("url", sa.String(1024), nullable=False, unique=True),
        sa.Column("description", sa.Text, server_default=""),
        sa.Column("score", sa.Integer, server_default="0"),
        sa.Column("rationale", sa.Text, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_jobs_score", "jobs", ["score"])
    op.create_table(
        "runs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("stored", sa.Integer, server_default="0"),
        sa.Column("ok", sa.Integer, server_default="1"),
    )


def downgrade() -> None:
    op.drop_table("runs")
    op.drop_index("ix_jobs_score", table_name="jobs")
    op.drop_table("jobs")
