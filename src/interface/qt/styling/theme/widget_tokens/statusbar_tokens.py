"""Status bar spacing and border tokens derived from Metrics."""

from __future__ import annotations

from dataclasses import dataclass

from ..metrics import Metrics


@dataclass(frozen=True)
class StatusBarTokens:
    border_width: int
    padding_horizontal: int
    min_height: int


def statusbar_tokens(metrics: Metrics) -> StatusBarTokens:
    return StatusBarTokens(
        border_width=metrics.border_width,
        padding_horizontal=metrics.padding_medium,
        min_height=metrics.min_statusbar_height,
    )


__all__ = ["StatusBarTokens", "statusbar_tokens"]
