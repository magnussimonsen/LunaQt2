"""Per-widget spacing and border tokens.

Each helper exposes a typed dataclass so individual widget spacing can
be adjusted without affecting other widgets. All defaults are derived
from :class:`theme.metrics.Metrics` to keep global sizing coherent while
still allowing targeted overrides.
"""

from __future__ import annotations

from dataclasses import dataclass

from .metrics import Metrics


@dataclass(frozen=True)
class ButtonTokens:
    border_width: int
    radius: int
    padding_y: int
    padding_x: int
    toolbar_padding_y: int
    toolbar_padding_x: int
    toolbar_min_height: int
    toolbar_radius: int
    toolbar_border_width: int
    menubar_padding_y: int
    menubar_padding_x: int
    menubar_min_height: int
    menubar_radius: int
    menubar_border_width: int


def button_tokens(metrics: Metrics) -> ButtonTokens:
    return ButtonTokens(
        border_width=metrics.border_width_small,
        radius=metrics.radius_medium,
        padding_x=metrics.padding_medium,
        padding_y=metrics.padding_small,
        toolbar_padding_x=metrics.padding_small,
        toolbar_padding_y=metrics.padding_extra_small,
        toolbar_min_height=metrics.min_toolbar_height,
        toolbar_radius=metrics.radius_small,
        toolbar_border_width=metrics.border_width_zero,
        menubar_padding_x=metrics.padding_medium,
        menubar_padding_y=metrics.padding_small,
        menubar_min_height=metrics.min_menubar_height,
        menubar_radius=metrics.radius_zero,
        menubar_border_width=metrics.border_width_small,
    )


@dataclass(frozen=True)
class CellContainerTokens:
    border_width: int
    border_radius: int
    padding: int
    header_margin_bottom: int


def cell_container_tokens(metrics: Metrics) -> CellContainerTokens:
    return CellContainerTokens(
        border_width=metrics.border_width,
        border_radius=metrics.radius_medium,
        padding=metrics.padding_small,
        header_margin_bottom=metrics.padding_small,
    )


@dataclass(frozen=True)
class CellGutterTokens:
    border_width: int
    border_radius: int
    padding_horizontal: int
    label_min_width: int


def cell_gutter_tokens(metrics: Metrics) -> CellGutterTokens:
    return CellGutterTokens(
        border_width=metrics.border_width,
        border_radius=metrics.radius_small,
        padding_horizontal=metrics.padding_small,
        label_min_width=32,
    )


@dataclass(frozen=True)
class MenuBarTokens:
    border_width: int
    spacing: int
    padding_horizontal: int
    min_height: int
    item_padding_y: int
    item_padding_x: int
    menu_padding_y: int
    menu_item_padding_y: int
    menu_item_padding_x: int
    separator_margin_y: int
    separator_margin_x: int


def menubar_tokens(metrics: Metrics) -> MenuBarTokens:
    return MenuBarTokens(
        border_width=metrics.border_width_zero,
        spacing=metrics.padding_small,
        padding_horizontal=metrics.padding_zero,
        min_height=metrics.min_menubar_height,
        # Menubar items like file, edit, view etc.
        item_padding_x=metrics.padding_small,
        item_padding_y=metrics.padding_small,
        # DROP DOWN MENU PADDING Y
        menu_padding_y=metrics.padding_medium,
        # DROP DOWN MENU ITEM PADDING
        menu_item_padding_x=metrics.padding_large,
        menu_item_padding_y=metrics.padding_extra_small,
        # DROP DOWN MENU SEPARATOR MARGIN
        separator_margin_x=metrics.padding_large,
        separator_margin_y=metrics.padding_extra_small,
       
    )


@dataclass(frozen=True)
class SidebarTokens:
    dock_border_width: int
    header_padding: int
    toolbar_padding: int
    toolbar_border_width: int
    action_row_radius: int
    action_row_padding_y: int
    action_row_padding_x: int
    input_border_width: int
    input_padding: int


def sidebar_tokens(metrics: Metrics) -> SidebarTokens:
    return SidebarTokens(
        dock_border_width=metrics.border_width,
        header_padding=metrics.padding_medium,
        toolbar_padding=metrics.padding_medium,
        toolbar_border_width=metrics.border_width,
        action_row_radius=metrics.radius_small,
        action_row_padding_y=metrics.padding_extra_small,
        action_row_padding_x=metrics.padding_small,
        input_border_width=metrics.border_width,
        input_padding=metrics.padding_small,
    )


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


__all__ = [
    "ButtonTokens",
    "CellContainerTokens",
    "CellGutterTokens",
    "MenuBarTokens",
    "SidebarTokens",
    "StatusBarTokens",
    "button_tokens",
    "cell_container_tokens",
    "cell_gutter_tokens",
    "menubar_tokens",
    "sidebar_tokens",
    "statusbar_tokens",
]
