"""Startup theme configuration shared by the LunaQt2 entry point."""

from __future__ import annotations

from interface.qt.styling.theme import ThemeMode

DEFAULT_THEME_MODE: ThemeMode = ThemeMode.LIGHT

__all__ = ["DEFAULT_THEME_MODE"]
