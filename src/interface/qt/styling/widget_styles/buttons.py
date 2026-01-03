"""Encapsulated button styling logic with dynamic property scoping."""

from __future__ import annotations

from textwrap import dedent

from interface.qt.styling.theme import (
    ButtonTokens,
    Theme,
    ThemeMode,
    button_tokens as get_button_tokens,
    get_theme,
)
from shared.utils.hex_to_rgba import hex_to_rgba


def _button_block(selector: str, palette, metrics) -> str:
    """Return a QSS block for a single button selector."""

    return dedent(
        f"""
        {selector} {{
            background-color: {palette.normal};
            color: {palette.text};
            border: 1px solid {palette.border};
            border-radius: 4px;
            padding: 4px 6px;
            font-family: {metrics.font_family};
            font-size: {metrics.font_size_medium}pt;
        }}

        {selector}:hover {{
            background-color: {palette.hover};
        }}

        {selector}:pressed {{
            background-color: {palette.pressed};
        }}

        {selector}:checked {{
            background-color: {palette.pressed};
            border-color: {palette.focus};
        }}

        {selector}:disabled {{
            background-color: {palette.disabled};
            color: {hex_to_rgba(palette.text, 0.6)};
            border-color: {palette.disabled};
        }}

        {selector}:focus-visible {{
            outline: none;
            border-color: {palette.focus};
        }}
        """
    ).strip()


def get_qss(
    mode: ThemeMode = ThemeMode.DARK,
    theme: Theme | None = None,
) -> str:
    """Concatenate QSS for all supported button variants."""

    theme = theme or get_theme(mode)
    metrics = theme.metrics
    button_tokens = get_button_tokens(metrics)
    palettes = theme.buttons

    sections = [
        _button_block('QPushButton[btnType="primary"]', palettes.primary, metrics),
        _button_block('QPushButton[btnType="warning"]', palettes.warning, metrics),
        _button_block('QPushButton[btnType="run"]', palettes.run, metrics),
        _button_block('QPushButton[btnType="stop"]', palettes.stop, metrics),
    ]

    menubar_overrides = dedent(
        f"""
        QPushButton[btnType="menubar"] {{
            background-color: {palettes.menubar.normal};
            color: {palettes.menubar.text};
            border: {button_tokens.main_menubar_border_width}px solid {palettes.menubar.border};
            border-radius: {button_tokens.main_menubar_radius}px;
            padding-top: {button_tokens.main_menubar_padding_top}px;
            padding-bottom: {button_tokens.main_menubar_padding_bottom}px;
            padding-left: {button_tokens.main_menubar_padding_left}px;
            padding-right: {button_tokens.main_menubar_padding_right}px;
            margin-top: 0px;
            margin-bottom: 0px;
            font-family: {metrics.font_family};
            font-size: {metrics.font_size_medium}pt;
        }}

        QPushButton[btnType="menubar"]:hover {{
            background-color: {palettes.menubar.hover};
        }}

        QPushButton[btnType="menubar"]:pressed {{
            background-color: {palettes.menubar.pressed};
        }}

        QPushButton[btnType="menubar"]:checked {{
            background-color: {palettes.menubar.pressed};
            color: {palettes.menubar.text};
        }}

        QPushButton[btnType="menubar"]:disabled {{
            background-color: {palettes.menubar.disabled};
            color: {hex_to_rgba(palettes.menubar.text, 0.6)};
        }}

        QPushButton[btnType="menubar"]:focus-visible {{
            outline: none;
            border-color: {palettes.menubar.focus};
        }}
        """
    ).strip()

    main_toolbar_overrides = dedent(
        f"""
        QPushButton[btnType="toolbar"] {{
            background-color: {palettes.main_toolbar.normal};
            color: {palettes.main_toolbar.text};
            border: {button_tokens.main_toolbar_border_width}px solid {palettes.main_toolbar.border};
            border-radius: {button_tokens.main_toolbar_radius}px;
            padding-top: {button_tokens.main_toolbar_padding_top}px;
            padding-bottom: {button_tokens.main_toolbar_padding_bottom}px;
            padding-left: {button_tokens.main_toolbar_padding_left}px;
            padding-right: {button_tokens.main_toolbar_padding_right}px;
            min-height: {button_tokens.main_toolbar_min_height}px;
            font-family: {metrics.font_family};
            font-size: {metrics.font_size_medium}pt;
        }}

        QPushButton[btnType="toolbar"]:hover {{
            background-color: {palettes.main_toolbar.hover};
        }}

        QPushButton[btnType="toolbar"]:pressed {{
            background-color: {palettes.main_toolbar.pressed};
        }}

        QPushButton[btnType="toolbar"]:checked {{
            background-color: {palettes.main_toolbar.pressed};
            border-color: {palettes.main_toolbar.focus};
        }}

        QPushButton[btnType="toolbar"]:disabled {{
            background-color: {palettes.main_toolbar.disabled};
            color: {hex_to_rgba(palettes.main_toolbar.text, 0.6)};
        }}

        QPushButton[btnType="toolbar"]:focus-visible {{
            outline: none;
            border-color: {palettes.main_toolbar.focus};
        }}
        """
    ).strip()

    sidebar_toolbar_overrides = dedent(
        f"""
        QPushButton[btnType="sidebar-toolbar"] {{
            background-color: {palettes.sidebar_toolbar.normal};
            color: {palettes.sidebar_toolbar.text};
            border: {button_tokens.sidebar_toolbar_border_width}px solid {palettes.sidebar_toolbar.border};
            border-radius: {button_tokens.sidebar_toolbar_radius}px;
            padding-top: {button_tokens.sidebar_toolbar_padding_top}px;
            padding-bottom: {button_tokens.sidebar_toolbar_padding_bottom}px;
            padding-left: {button_tokens.sidebar_toolbar_padding_left}px;
            padding-right: {button_tokens.sidebar_toolbar_padding_right}px;
            min-height: {button_tokens.sidebar_toolbar_min_height}px;
            font-family: {metrics.font_family};
            font-size: {metrics.font_size_medium}pt;
        }}

        QPushButton[btnType="sidebar-toolbar"]:hover {{
            background-color: {palettes.sidebar_toolbar.hover};
        }}

        QPushButton[btnType="sidebar-toolbar"]:pressed {{
            background-color: {palettes.sidebar_toolbar.pressed};
        }}

        QPushButton[btnType="sidebar-toolbar"]:checked {{
            background-color: {palettes.sidebar_toolbar.pressed};
            border-color: {palettes.sidebar_toolbar.focus};
        }}

        QPushButton[btnType="sidebar-toolbar"]:disabled {{
            background-color: {palettes.sidebar_toolbar.disabled};
            color: {hex_to_rgba(palettes.sidebar_toolbar.text, 0.6)};
        }}

        QPushButton[btnType="sidebar-toolbar"]:focus-visible {{
            outline: none;
            border-color: {palettes.sidebar_toolbar.focus};
        }}
        """
    ).strip()

    focus_reset = dedent(
        """
        QPushButton {
            outline: none;
        }
        """
    ).strip()

    return "\n\n".join(sections + [menubar_overrides, main_toolbar_overrides, sidebar_toolbar_overrides, focus_reset])


__all__ = ["get_qss"]
