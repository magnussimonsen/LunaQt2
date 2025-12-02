"""Helper utilities for translating typography choices into concrete sizes."""

from __future__ import annotations

from math import ceil


def toolbar_min_height_for_font(ui_point_size: int, *, min_height: int = 28, scale: float = 2.0) -> int:
    """Return a reasonable minimum toolbar height for the given UI font size.

    The value is proportional to the selected point size so menubars, toolbars,
    and sidebar toolbars do not collapse when the overall window height is small.
    The default scale/min height values are tuned for Segoe UI/Noto Sans, but can
    be tweaked if the typography system changes later.
    """

    if ui_point_size <= 0:
        return min_height
    scaled = ceil(ui_point_size * scale)
    return max(min_height, scaled)


def cell_row_min_height_for_font(
    body_point_size: int,
    *,
    min_lines: int = 2,
    line_height_scale: float = 1.35,
    padding: int = 12,
    min_height: int = 40,
) -> int:
    """Return a minimum row height that keeps at least ``min_lines`` visible.

    Rows can grow with content automatically; this value only guards against the
    layout collapsing them below a readable threshold when the window shrinks.
    """

    if body_point_size <= 0:
        return min_height
    line_height = body_point_size * line_height_scale
    content_height = line_height * max(1, min_lines)
    scaled = ceil(content_height + padding)
    return max(min_height, scaled)


__all__ = ["toolbar_min_height_for_font", "cell_row_min_height_for_font"]
