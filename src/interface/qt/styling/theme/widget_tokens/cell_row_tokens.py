"""Cell row spacing/border tokens derived from Metrics."""
# The cell row is not its own widget. 
# The class is located in main_window.py.


from __future__ import annotations

from dataclasses import dataclass

from ..metrics import Metrics


@dataclass(frozen=True)
class CellRowTokens:
    gutter_gap: int

    cell_row_spacing: int
    
    cell_row_padding_top: int
    cell_row_padding_bottom: int
    cell_row_padding_left: int
    cell_row_padding_right: int
    
    cell_row_margin_top: int
    cell_row_margin_bottom: int
    cell_row_margin_left: int
    cell_row_margin_right: int

def cell_row_tokens(metrics: Metrics) -> CellRowTokens:
    return CellRowTokens(
        gutter_gap=metrics.padding_small,
        cell_row_spacing=metrics.padding_small,
        cell_row_padding_top=metrics.padding_extra_small,
        cell_row_padding_bottom=metrics.padding_extra_small,
        cell_row_padding_left=metrics.padding_extra_small,
        cell_row_padding_right=metrics.padding_extra_small,
        cell_row_margin_top=metrics.margin_extra_small,
        cell_row_margin_bottom=metrics.margin_extra_small,
        cell_row_margin_left=metrics.margin_small,
        cell_row_margin_right=metrics.margin_small,
    )


__all__ = ["CellRowTokens", "cell_row_tokens"]
