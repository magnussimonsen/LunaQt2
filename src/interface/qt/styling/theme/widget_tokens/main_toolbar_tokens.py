"""Main toolbar spacing and border tokens derived from Metrics."""

from __future__ import annotations

from dataclasses import dataclass

from ..metrics import Metrics


@dataclass(frozen=True)
class MainToolbarTokens:
    border_width: int
    border_radius: int
    spacing: int
    padding_top: int
    padding_bottom: int
    padding_left: int
    padding_right: int
    margin_top: int
    margin_bottom: int
    margin_left: int
    margin_right: int
    min_height: int


def main_toolbar_tokens(metrics: Metrics) -> MainToolbarTokens:
    return MainToolbarTokens(
        border_width=metrics.border_width_zero,
        border_radius=metrics.radius_zero,
        
        spacing=metrics.padding_small,

        padding_top=metrics.padding_zero,
        padding_bottom=metrics.padding_small,
        padding_left=metrics.padding_small,
        padding_right=metrics.padding_small,
        
        margin_top=metrics.padding_zero,
        margin_bottom=metrics.padding_zero,
        margin_left=metrics.padding_zero,
        margin_right=metrics.padding_zero,

        min_height=metrics.min_main_toolbar_height,
    )


__all__ = ["MainToolbarTokens", "main_toolbar_tokens"]
