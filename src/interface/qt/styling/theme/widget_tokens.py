"""Per-widget spacing and border tokens derived from Metrics."""

from __future__ import annotations

from dataclasses import dataclass

from .metrics import Metrics


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
        border_radius=metrics.radius_medium,
        border_width=metrics.border_width,
        
        border_width_top=metrics.border_width_small, # Specific per-side border widths for overrides
        border_width_bottom=metrics.border_width_small,
        border_width_left=metrics.border_width_small,
        border_width_right=metrics.border_width_small,

        padding_top=metrics.padding_small,
        padding_bottom=metrics.padding_small,
        padding_left=metrics.padding_medium,
        padding_right=metrics.padding_medium,

        margin_top=metrics.margin_small,
        margin_bottom=metrics.margin_small,
        margin_left=metrics.margin_small,
        margin_right=metrics.margin_small,

        header_margin_bottom=metrics.padding_small, # Heder is only for development
    )


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

        border_width_top=metrics.border_width_small, # Specific per-side border widths for overrides
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

        min_height=metrics.min_menubar_height,

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


__all__ = [
    "ButtonTokens",
    "CellContainerTokens",
    "CellGutterTokens",
    "MenuBarTokens",
    "SidebarTokens",
    "StatusBarTokens",
    "MainToolbarTokens",
    "SidebarToolbarTokens",
    "button_tokens",
    "cell_container_tokens",
    "cell_gutter_tokens",
    "menubar_tokens",
    "sidebar_tokens",
    "statusbar_tokens",
    "main_toolbar_tokens",
    "sidebar_toolbar_tokens",
]
