"""Cell container spacing and border tokens derived from Metrics."""

from __future__ import annotations

from dataclasses import dataclass

from ..metrics import Metrics


@dataclass(frozen=True)
class CellContainerTokens:
    border_radius: int
    border_width: int
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
    header_margin_bottom: int


def cell_container_tokens(metrics: Metrics) -> CellContainerTokens:
    return CellContainerTokens(
        border_radius=metrics.radius_small,
        border_width=metrics.border_width,
        
        border_width_top=metrics.border_width_small,  
        border_width_bottom=metrics.border_width_small,
        border_width_left=metrics.border_width_small,
        border_width_right=metrics.border_width_small,

        padding_top=metrics.padding_zero,
        padding_bottom=metrics.padding_zero,
        padding_left=metrics.padding_small,
        padding_right=metrics.padding_small,

        margin_top=metrics.margin_small,
        margin_bottom=metrics.margin_small,
        margin_left=metrics.margin_small,
        margin_right=metrics.margin_small,

        header_margin_bottom=metrics.padding_small,
    )


__all__ = ["CellContainerTokens", "cell_container_tokens"]
