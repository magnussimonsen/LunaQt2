"""Sidebar toolbar spacing and border tokens derived from Metrics."""

from __future__ import annotations

from dataclasses import dataclass

from ..interface.qt.styling.theme.metrics import Metrics


@dataclass(frozen=True)
class SidebarToolbarTokens:
    border_width: int
    border_radius: int
    spacing: int
    padding_horizontal: int
    min_height: int


def sidebar_toolbar_tokens(metrics: Metrics) -> SidebarToolbarTokens:
    return SidebarToolbarTokens(
        border_width=metrics.border_width,
        border_radius=metrics.radius_zero,
        spacing=metrics.padding_small,
        padding_horizontal=metrics.padding_medium,
        min_height=metrics.min_sidebar_toolbar_height,
    )


__all__ = ["SidebarToolbarTokens", "sidebar_toolbar_tokens"]
