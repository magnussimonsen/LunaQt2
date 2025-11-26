"""Startup theme configuration shared by the demo entry point."""

from __future__ import annotations

from theme import ThemeMode

# Default theme applied when the demo window launches before any user choice.
DEFAULT_THEME_MODE: ThemeMode = ThemeMode.LIGHT

__all__ = ["DEFAULT_THEME_MODE"]
