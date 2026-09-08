"""Structured JSON logging with a per-request id."""

from __future__ import annotations

import logging

import structlog

from .config import settings


def configure_logging() -> None:
    """Configure structlog to emit JSON lines at the configured level."""
    logging.basicConfig(format="%(message)s", level=settings.log_level)
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.getLevelName(settings.log_level)
        ),
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    return structlog.get_logger(name)
