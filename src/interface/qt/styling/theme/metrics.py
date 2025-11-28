"""Shared spacing and typography metrics used by all theme modules."""

from __future__ import annotations

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Metrics:
    """Spacing, sizing, and typography metrics shared by all styles."""

    test_value: int = 80  # Temporary debug token

    radius_zero: int = 0
    radius_small: int = 2
    radius_medium: int = 4
    radius_large: int = 6

    padding_zero: int = 0
    padding_extra_small: int = 2
    padding_small: int = 4
    padding_medium: int = 6
    padding_large: int = 8
    padding_extra_large: int = 12

    margin_zero: int = 0
    margin_extra_small: int = 2
    margin_small: int = 4
    margin_medium: int = 6
    margin_large: int = 80
    margin_extra_large: int = 12

    gutter_width: int = 12
    min_toolbar_height: int = 5
    min_menubar_height: int = 5

    min_main_toolbar_height: int = 5 
    min_sidebar_toolbar_height: int = 5

    min_statusbar_height: int = 32

    sidebar_default_width: int = 320
    sidebar_min_width: int = 220
    sidebar_max_width: int = 560

    font_family: str = "Segoe UI, 'Noto Sans', sans-serif"
    font_size_small: int = 11
    font_size_medium: int = 12
    font_size_large: int = 14
    cell_body_font_size: int = 12

    border_width: int = 1
    border_width_zero: int = 0
    border_width_small: int = 1
    border_width_medium: int = 2
    border_width_large: int = 4

def build_metrics_for_ui_font(
    ui_point_size: int,
    *,
    template: "Metrics" | None = None,
    small_offset: int = 2,
    large_offset: int = 2,
) -> "Metrics":
    """Return a Metrics instance adjusted to the requested UI font size."""

    base = template or Metrics()
    adjusted_small = max(ui_point_size - small_offset, 6)
    adjusted_large = ui_point_size + large_offset
    return replace(
        base,
        font_size_small=adjusted_small,
        font_size_medium=ui_point_size,
        font_size_large=adjusted_large,
    )


__all__ = ["Metrics", "build_metrics_for_ui_font"]
