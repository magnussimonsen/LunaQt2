"""Convert hex color codes to rgba() CSS strings."""

from __future__ import annotations


def hex_to_rgba(hex_color: str, alpha: float) -> str:
    """Return an rgba() string for the given hex color and alpha."""

    value = hex_color.lstrip("#")
    if len(value) != 6:
        return hex_color
    red = int(value[0:2], 16)
    green = int(value[2:4], 16)
    blue = int(value[4:6], 16)
    return f"rgba({red}, {green}, {blue}, {alpha:.3f})"


__all__ = ["hex_to_rgba"]
