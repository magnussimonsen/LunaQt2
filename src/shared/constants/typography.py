"""Typography-related configuration values shared across the UI."""

from __future__ import annotations

DEFAULT_UI_FONT_POINT_SIZE = 12
MIN_UI_FONT_POINT_SIZE = 10
MAX_UI_FONT_POINT_SIZE = 18
FONT_SIZE_STEP = 1


def clamp_ui_font_point_size(value: int) -> int:
    """Clamp the provided UI font size to the supported bounds."""

    return max(MIN_UI_FONT_POINT_SIZE, min(MAX_UI_FONT_POINT_SIZE, value))


__all__ = [
    "DEFAULT_UI_FONT_POINT_SIZE",
    "MIN_UI_FONT_POINT_SIZE",
    "MAX_UI_FONT_POINT_SIZE",
    "FONT_SIZE_STEP",
    "clamp_ui_font_point_size",
]
