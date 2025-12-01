"""Layout tokens for the vertical list that contains cell rows."""

from __future__ import annotations

from dataclasses import dataclass

from ..metrics import Metrics


@dataclass(frozen=True)
class CellListTokens:
    content_margin_top: int
    content_margin_bottom: int
    content_margin_left: int
    content_margin_right: int
    content_spacing: int


def cell_list_tokens(metrics: Metrics) -> CellListTokens:
    return CellListTokens(
        content_margin_top=metrics.padding_small,
        content_margin_bottom=metrics.padding_small,
        content_margin_left=metrics.padding_small,
        content_margin_right=metrics.padding_small,
        content_spacing=metrics.padding_zero,
    )


__all__ = ["CellListTokens", "cell_list_tokens"]
