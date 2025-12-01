"""Cell gutter spacing and border tokens derived from Metrics."""

from __future__ import annotations

from dataclasses import dataclass

from ..metrics import Metrics


@dataclass(frozen=True)
class CellGutterTokens:
    """Theme-derived values for both paint-time and layout-time gutter styling."""

    # Visual chrome (consumed by QSS)
    border_width: int
    border_radius: int
    border_width_top: int
    border_width_bottom: int
    border_width_left: int
    border_width_right: int
    paint_padding_top: int
    paint_padding_bottom: int
    paint_padding_left: int
    paint_padding_right: int
    margin_top: int
    margin_bottom: int
    margin_left: int
    margin_right: int

    # Layout geometry (consumed by widgets/layouts)
    layout_inset_top: int
    layout_inset_bottom: int
    layout_inset_left: int
    layout_inset_right: int

    # Misc widget-specific values
    label_min_width: int


def cell_gutter_tokens(metrics: Metrics) -> CellGutterTokens:
    return CellGutterTokens(
        border_width=metrics.border_width_small, 

        border_radius=metrics.radius_small,

        border_width_top=metrics.border_width_zero,
        border_width_bottom=metrics.border_width_zero,
        border_width_left=metrics.border_width_zero,
        border_width_right=metrics.border_width_small,

        paint_padding_top=metrics.padding_zero,
        paint_padding_bottom=metrics.padding_zero,
        paint_padding_left=metrics.padding_zero,
        paint_padding_right=metrics.padding_zero,

        margin_top=metrics.padding_zero,
        margin_bottom=metrics.padding_zero,
        margin_left=metrics.padding_zero,
        margin_right=metrics.padding_zero,

        layout_inset_top=metrics.padding_small,
        layout_inset_bottom=metrics.padding_small,
        layout_inset_left=metrics.padding_medium,
        layout_inset_right=metrics.padding_medium,

        label_min_width=32,
    )


__all__ = ["CellGutterTokens", "cell_gutter_tokens"]
