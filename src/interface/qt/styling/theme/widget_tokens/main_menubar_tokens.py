"""Main menubar spacing and border tokens derived from Metrics."""

from __future__ import annotations

from dataclasses import dataclass

from ..metrics import Metrics


@dataclass(frozen=True)
class MenuBarTokens:
    border_width: int
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
    item_padding_top: int
    item_padding_bottom: int
    item_padding_left: int
    item_padding_right: int
    dropdown_menu_padding_top: int
    dropdown_menu_padding_bottom: int
    dropdown_menu_padding_left: int
    dropdown_menu_padding_right: int
    dropdown_separator_margin_x: int
    dropdown_separator_margin_y: int


def menubar_tokens(metrics: Metrics) -> MenuBarTokens:
    return MenuBarTokens(
        border_width=metrics.border_width_zero,
        
        spacing=metrics.padding_small,

        padding_top=metrics.padding_small,
        padding_bottom=metrics.padding_small,
        padding_left=metrics.padding_small,
        padding_right=metrics.padding_small,

        margin_top=metrics.padding_zero,
        margin_bottom=metrics.padding_zero,
        margin_left=metrics.padding_zero,
        margin_right=metrics.padding_zero,

        min_height=metrics.min_main_menubar_height,

        # Menubar item paddings (File, Edit, View, etc.)
        item_padding_top=metrics.padding_small,
        item_padding_bottom=metrics.padding_small,
        item_padding_right=metrics.padding_medium,
        item_padding_left=metrics.padding_medium,

        # Dropdown menu and dropdown items paddings
        dropdown_menu_padding_top=metrics.padding_medium,
        dropdown_menu_padding_bottom=metrics.padding_medium,
        dropdown_menu_padding_left=metrics.padding_medium,
        dropdown_menu_padding_right=metrics.padding_medium,

        dropdown_separator_margin_x=metrics.padding_large,
        dropdown_separator_margin_y=metrics.padding_extra_small,
    )


__all__ = ["MenuBarTokens", "menubar_tokens"]
