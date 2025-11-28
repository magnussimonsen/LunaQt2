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
        _button_block('QPushButton[btnType="menubar"]', palettes.menubar, metrics),
        _button_block('QPushButton[btnType="toolbar"]', palettes.main_toolbar, metrics),
        _button_block('QPushButton[btnType="warning"]', palettes.warning, metrics),
    ]

    toolbar_overrides = dedent(
        f"""
        QPushButton[btnType="toolbar"] {{
            border: none;
            border-radius: {button_tokens.main_toolbar_radius}px;
            padding: {button_tokens.main_toolbar_padding_top}px {button_tokens.main_toolbar_padding_right}px {button_tokens.main_toolbar_padding_bottom}px {button_tokens.main_toolbar_padding_left}px;
            min-height: {button_tokens.main_toolbar_min_height}px;
        }}
        """
    ).strip()

    menubar_overrides = dedent(
        f"""
        QPushButton[btnType="menubar"] {{
            border: none;
            border-radius: {button_tokens.main_menubar_radius}px;
            padding: {button_tokens.main_menubar_padding_top}px {button_tokens.main_menubar_padding_right}px {button_tokens.main_menubar_padding_bottom}px {button_tokens.main_menubar_padding_left}px;
            margin-top: 0px;
            margin-bottom: 0px;
        }}

        QPushButton[btnType="menubar"]:checked {{
            background-color: {palettes.menubar.pressed};
            color: {palettes.menubar.text};
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

    return "\n\n".join(sections + [toolbar_overrides, menubar_overrides, focus_reset])


__all__ = ["get_qss"]
