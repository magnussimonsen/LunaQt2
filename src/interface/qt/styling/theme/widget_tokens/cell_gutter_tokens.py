"""Cell gutter spacing and border tokens derived from Metrics."""

from __future__ import annotations

from dataclasses import dataclass

from ..metrics import Metrics


@dataclass(frozen=True)
class CellGutterTokens:
    border_width: int
    border_radius: int
    border_width_top: int
    border_width_bottom: int
    border_width_left: int
    border_width_right: int
    padding_top: int
    padding_bottom: int
    padding_left: int
    padding_right: int
    margin_top: int
    margin_bottom: int
    margin_left: int
    margin_right: int
    label_min_width: int


def cell_gutter_tokens(metrics: Metrics) -> CellGutterTokens:
    return CellGutterTokens(
        border_width=metrics.border_width_small, 

        border_radius=metrics.radius_small,

        border_width_top=metrics.border_width_small,
        border_width_bottom=metrics.border_width_small,
        border_width_left=metrics.border_width_small,
        border_width_right=metrics.border_width_small,

        padding_top=metrics.padding_small,
        padding_bottom=metrics.padding_small,
        padding_left=metrics.padding_medium,
        padding_right=metrics.padding_medium,

        margin_top=metrics.padding_small,
        margin_bottom=metrics.padding_small,
        margin_left=metrics.padding_zero,
        margin_right=metrics.padding_zero,

        label_min_width=32,
    )


__all__ = ["CellGutterTokens", "cell_gutter_tokens"]
