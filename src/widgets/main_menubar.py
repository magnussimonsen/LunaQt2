"""QSS generator for the main window menu bar."""

from __future__ import annotations

from textwrap import dedent

from theme import Theme, ThemeMode, get_theme, menubar_tokens as get_menubar_tokens

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
   # MENUBAR
    menubar_qss = dedent(
        f"""
        {MENUBAR_SELECTOR} {{
            background-color: {menu_palette.background};
            color: {menu_palette.text};
            spacing: {menubar_tokens.spacing}px;
            padding: 0px {menubar_tokens.padding_horizontal}px;
            margin: 0px;
            border-bottom: {menubar_tokens.border_width}px solid {theme.bg.app};
            border-bottom: none;
            border-top: {menubar_tokens.border_width}px solid {theme.bg.app};
            border-top: none; 
            min-height: {menubar_tokens.min_height}px;
            font-family: {metrics.font_family}; /* THIS SHALL NOT COME FROM METRICS */
            font-size: {metrics.font_size_medium}pt; /* THIS SHALL NOT COME FROM METRICS */
        }}

        {MENUBAR_SELECTOR}::item {{
            background: transparent;
            padding: {menubar_tokens.item_padding_y}px {menubar_tokens.item_padding_x}px;
        }}

        {MENUBAR_SELECTOR}::item:selected {{
            background: {menu_palette.item_hover};
            padding: {menubar_tokens.item_padding_y}px {menubar_tokens.item_padding_x}px;
        }}

        {MENUBAR_SELECTOR}:focus {{
            outline: none;
        }}
        """
    ).strip()
    
    # DROPDOWN MENU PANEL
    menu_panel_qss = dedent(
        f"""
        {MENU_SELECTOR} {{   
            background-color: {theme.bg.dropdown};
            border: {menubar_tokens.border_width}px solid {menu_palette.separator};
            padding: {menubar_tokens.menu_padding_y}px 0px;
        }}

        {MENU_SELECTOR}::item {{
            padding: {menubar_tokens.menu_item_padding_y}px {menubar_tokens.menu_item_padding_x}px;
            background: transparent;
        }}

        {MENU_SELECTOR}::item:selected {{
            background: {menu_palette.item_hover};
            color: {theme.text.primary};
        }}

        {MENU_SELECTOR}::separator {{
            height: 1px;
            margin: {menubar_tokens.separator_margin_y}px {menubar_tokens.separator_margin_x}px;
            background: {menu_palette.separator};
        }}
        """
    ).strip()

    return f"{menubar_qss}\n\n{menu_panel_qss}"


__all__ = ["get_qss"]
