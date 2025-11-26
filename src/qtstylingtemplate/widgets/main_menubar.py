"""QSS generator for the main window menu bar."""

from __future__ import annotations

from textwrap import dedent

from qtstylingtemplate.theme import Theme, ThemeMode, get_theme

MENUBAR_SELECTOR = 'QMenuBar#MainMenuBar'
MENU_SELECTOR = 'QMenu[menuRole="primary"]'


def get_qss(
    mode: ThemeMode = ThemeMode.DARK,
    theme: Theme | None = None,
) -> str:
    """Return scoped QSS for the application menu bar and its menus."""

    theme = theme or get_theme(mode)
    metrics = theme.metrics
    menu_palette = theme.menu

    menubar_qss = dedent(
        f"""
        {MENUBAR_SELECTOR} {{
            background-color: {menu_palette.background};
            color: {menu_palette.text};
            spacing: {metrics.padding_sm}px;
            padding: 0 {metrics.padding_md}px;
            border-bottom: {metrics.border_width}px solid {theme.bg.app};
            border-top: {metrics.border_width}px solid {theme.bg.app};
            min-height: {metrics.menubar_height}px;
            font-family: {metrics.font_family};
            font-size: {metrics.font_size_md}pt;
        }}

        {MENUBAR_SELECTOR}::item {{
            background: transparent;
            padding: {metrics.padding_xs}px {metrics.padding_md}px;
        }}

        {MENUBAR_SELECTOR}::item:selected {{
            background: {menu_palette.item_hover};
        }}

        {MENUBAR_SELECTOR}:focus {{
            outline: none;
        }}
        """
    ).strip()

    menu_panel_qss = dedent(
        f"""
        {MENU_SELECTOR} {{
            background-color: {theme.bg.dropdown};
            border: {metrics.border_width}px solid {menu_palette.separator};
            padding: {metrics.padding_xs}px 0;
        }}

        {MENU_SELECTOR}::item {{
            padding: {metrics.padding_xs}px {metrics.padding_lg}px;
            background: transparent;
        }}

        {MENU_SELECTOR}::item:selected {{
            background: {menu_palette.item_hover};
            color: {theme.text.primary};
        }}

        {MENU_SELECTOR}::separator {{
            height: 1px;
            margin: {metrics.padding_xs}px {metrics.padding_lg}px;
            background: {menu_palette.separator};
        }}
        """
    ).strip()

    return f"{menubar_qss}\n\n{menu_panel_qss}"


__all__ = ["get_qss"]
