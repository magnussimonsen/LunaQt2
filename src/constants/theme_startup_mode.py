"""Startup theme configuration shared by the LunaQt2 entry point."""

from __future__ import annotations

from theme import ThemeMode

# Default theme applied when the LunaQt2 window launches before any user choice.
DEFAULT_THEME_MODE: ThemeMode = ThemeMode.LIGHT

__all__ = ["DEFAULT_THEME_MODE"]
