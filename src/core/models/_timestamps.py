"""Utility helpers for timestamp serialization in models."""

from __future__ import annotations

from datetime import datetime, timezone


def parse_timestamp(value: str | None) -> datetime:
    """Parse an ISO 8601 timestamp, accepting trailing ``Z`` notation."""

    if not value:
        raise ValueError("Timestamp value is required")

    if value.endswith("Z"):
        value = f"{value[:-1]}+00:00"
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def ensure_utc(dt: datetime | None) -> datetime:
    """Return a timezone-aware datetime, defaulting to ``UTC`` when missing."""

    if dt is None:
        dt = datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def format_timestamp(dt: datetime | None) -> str:
    """Serialize a datetime as an ISO 8601 string in UTC."""

    return ensure_utc(dt).isoformat()


__all__ = ["parse_timestamp", "ensure_utc", "format_timestamp"]
