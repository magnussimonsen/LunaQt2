"""Button spacing and border tokens derived from Metrics."""

from __future__ import annotations

from dataclasses import dataclass

from ..metrics import Metrics


@dataclass(frozen=True)
class ButtonTokens:
    main_menubar_border_width: int
    main_menubar_padding_top: int
    main_menubar_padding_bottom: int
    main_menubar_padding_left: int
    main_menubar_padding_right: int
    main_menubar_min_height: int
    main_menubar_radius: int

    main_toolbar_border_width: int
    main_toolbar_padding_top: int
    main_toolbar_padding_bottom: int
    main_toolbar_padding_left: int
    main_toolbar_padding_right: int
    main_toolbar_min_height: int
    main_toolbar_radius: int

    sidebar_toolbar_border_width: int
    sidebar_toolbar_padding_top: int
    sidebar_toolbar_padding_bottom: int
    sidebar_toolbar_padding_left: int
    sidebar_toolbar_padding_right: int
    sidebar_toolbar_min_height: int
    sidebar_toolbar_radius: int


def button_tokens(metrics: Metrics) -> ButtonTokens:
    return ButtonTokens(
        main_menubar_border_width=metrics.border_width_small,
        main_menubar_padding_top=metrics.padding_small,
        main_menubar_padding_bottom=metrics.padding_small,
        main_menubar_padding_left=metrics.padding_small,
        main_menubar_padding_right=metrics.padding_small,
        main_menubar_min_height=metrics.min_main_menubar_height,
        main_menubar_radius=metrics.radius_small,

        main_toolbar_border_width=metrics.border_width_small,
        main_toolbar_padding_top=metrics.padding_small,
        main_toolbar_padding_bottom=metrics.padding_small,
        main_toolbar_padding_left=metrics.padding_small,
        main_toolbar_padding_right=metrics.padding_small,
        main_toolbar_min_height=metrics.min_main_toolbar_height,
        main_toolbar_radius=metrics.radius_small,

        sidebar_toolbar_border_width=metrics.border_width_small,
        sidebar_toolbar_padding_top=metrics.padding_small,
        sidebar_toolbar_padding_bottom=metrics.padding_small,
        sidebar_toolbar_padding_left=metrics.padding_small,
        sidebar_toolbar_padding_right=metrics.padding_small,
        sidebar_toolbar_min_height=metrics.min_sidebar_toolbar_height,
        sidebar_toolbar_radius=metrics.radius_small,
    )


__all__ = ["ButtonTokens", "button_tokens"]
