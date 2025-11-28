"""UUID generation utilities for cells and notebooks."""

from __future__ import annotations

import uuid


def generate_cell_id() -> str:
    """Generate a unique cell identifier."""

    return str(uuid.uuid4())


def generate_notebook_id() -> str:
    """Generate a unique notebook identifier."""

    return str(uuid.uuid4())


__all__ = ["generate_cell_id", "generate_notebook_id"]
