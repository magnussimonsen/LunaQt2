"""QSS generator for the main window menu bar."""

from __future__ import annotations

from textwrap import dedent

from interface.qt.styling.theme import (
    Theme,
    ThemeMode,
    get_theme,
    menubar_tokens as get_menubar_tokens,
)

MENUBAR_SELECTOR = 'QMenuBar#MainMenuBar'
MENU_SELECTOR = 'QMenu[menuRole="primary"]'


def get_qss(
    mode: ThemeMode = ThemeMode.DARK,
    theme: Theme | None = None,
) -> str:
    """Return scoped QSS for the application menu bar and its menus."""

    theme = theme or get_theme(mode)
    metrics = theme.metrics
    menubar_tokens = get_menubar_tokens(metrics)
    menu_palette = theme.menu

    menubar_qss = dedent(
        f"""
        {MENUBAR_SELECTOR} {{
            background-color: {menu_palette.background};
            color: {menu_palette.text};
            spacing: {menubar_tokens.spacing}px;
            padding: {menubar_tokens.padding_top}px {menubar_tokens.padding_right}px {menubar_tokens.padding_bottom}px {menubar_tokens.padding_left}px;
            margin: {menubar_tokens.margin_top}px {menubar_tokens.margin_right}px {menubar_tokens.margin_bottom}px {menubar_tokens.margin_left}px;
            border-bottom: {menubar_tokens.border_width}px solid {theme.bg.app};
            border-top: {menubar_tokens.border_width}px solid {theme.bg.app};
            min-height: {menubar_tokens.min_height}px;
            font-family: {metrics.font_family};
            font-size: {metrics.font_size_medium}pt;
        }}

        {MENUBAR_SELECTOR}::item {{
            background: transparent;
            padding-top: {menubar_tokens.item_padding_top}px;
            padding-bottom: {menubar_tokens.item_padding_bottom}px;
            padding-left: {menubar_tokens.item_padding_left}px;
            padding-right: {menubar_tokens.item_padding_right}px;
        }}

        {MENUBAR_SELECTOR}::item:selected {{
            background: {menu_palette.item_hover};
            padding-top: {menubar_tokens.item_padding_top}px;
            padding-bottom: {menubar_tokens.item_padding_bottom}px;
            padding-left: {menubar_tokens.item_padding_left}px;
            padding-right: {menubar_tokens.item_padding_right}px;
        }}

        {MENUBAR_SELECTOR}:focus {{
            outline: none;
        }}

        QWidget[widgetRole="menubar-corner"] {{
            background-color: {menu_palette.background};
        }}
        """
    ).strip()

    menu_panel_qss = dedent(
        f"""
        {MENU_SELECTOR} {{
            background-color: {theme.bg.dropdown};
            border: {menubar_tokens.border_width}px solid {menu_palette.separator};
            padding-top: {menubar_tokens.dropdown_menu_padding_top}px;
            padding-bottom: {menubar_tokens.dropdown_menu_padding_bottom}px;
            padding-left: {menubar_tokens.dropdown_menu_padding_left}px;
            padding-right: {menubar_tokens.dropdown_menu_padding_right}px;
        }}

        {MENU_SELECTOR}::item {{
            padding-top: {menubar_tokens.item_padding_top}px;
            padding-bottom: {menubar_tokens.item_padding_bottom}px;
            padding-left: {menubar_tokens.item_padding_left}px;
            padding-right: {menubar_tokens.item_padding_right}px;
            background: transparent;
        }}

        {MENU_SELECTOR}::item:selected {{
            background: {menu_palette.item_hover};
            color: {theme.text.primary};
        }}

        {MENU_SELECTOR}::separator {{
            height: 1px;
            margin-top: {menubar_tokens.dropdown_separator_margin_y}px;
            margin-bottom: {menubar_tokens.dropdown_separator_margin_y}px;
            margin-left: {menubar_tokens.dropdown_separator_margin_x}px;
            margin-right: {menubar_tokens.dropdown_separator_margin_x}px;
            background: {menu_palette.separator};
        }}
        """
    ).strip()

    return f"{menubar_qss}\n\n{menu_panel_qss}"


__all__ = ["get_qss"]
