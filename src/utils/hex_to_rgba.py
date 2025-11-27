"""Convert hex color codes to rgba() CSS strings."""

from __future__ import annotations


def hex_to_rgba(hex_color: str, alpha: float) -> str:
    """Return an rgba() string for the given hex color and alpha.
    
    Args:
        hex_color: Hex color string (e.g., "#FF5733" or "FF5733")
        alpha: Alpha value between 0.0 and 1.0
        
    Returns:
        rgba() CSS string (e.g., "rgba(255, 87, 51, 0.600)")
        
    Examples:
        >>> hex_to_rgba("#FF5733", 0.5)
        'rgba(255, 87, 51, 0.500)'
        >>> hex_to_rgba("FF5733", 1.0)
        'rgba(255, 87, 51, 1.000)'
    """
    value = hex_color.lstrip("#")
    if len(value) != 6:
        return hex_color
    r = int(value[0:2], 16)
    g = int(value[2:4], 16)
    b = int(value[4:6], 16)
    return f"rgba({r}, {g}, {b}, {alpha:.3f})"


__all__ = ["hex_to_rgba"]
