"""Placeholder for transient UI/application state tracking."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AppState:
    """Track high-level UI state until real state management is implemented."""

    active_notebook_id: str | None = None
    selected_cell_id: str | None = None
    theme_mode: str | None = None


__all__ = ["AppState"]
