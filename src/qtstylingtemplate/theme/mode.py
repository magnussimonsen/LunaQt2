"""Shared enum that defines the supported theme modes."""

from __future__ import annotations

from enum import Enum


class ThemeMode(str, Enum):
    """Available theme modes."""

    LIGHT = "light"
    DARK = "dark"


__all__ = ["ThemeMode"]
