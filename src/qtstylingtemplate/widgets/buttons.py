"""Encapsulated button styling logic with dynamic property scoping."""

from __future__ import annotations

from textwrap import dedent

from qtstylingtemplate.theme import Metrics, Theme, ThemeMode, get_theme


def _button_block(selector: str, palette, metrics: "Metrics") -> str:
    """Return a QSS block for a single button selector."""

    return dedent(
        f"""
        {selector} {{
            background-color: {palette.normal};
            color: {palette.text};
            border: {metrics.border_width}px solid {palette.border};
            border-radius: {metrics.radius_md}px;
            padding: {metrics.padding_sm}px {metrics.padding_md}px;
            font-family: {metrics.font_family};
            font-size: {metrics.font_size_md}pt;
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
            color: {palette.text}99;
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
    palettes = theme.buttons

    sections = [
        _button_block('QPushButton[btnType="primary"]', palettes.primary, metrics),
        _button_block('QPushButton[btnType="toolbar"]', palettes.toolbar, metrics),
        _button_block('QPushButton[btnType="warning"]', palettes.warning, metrics),
    ]

    # Toolbar buttons tend to be smaller and flatter, so override specifics.
    toolbar_overrides = dedent(
        f"""
        QPushButton[btnType="toolbar"] {{
            border-radius: {metrics.radius_sm}px;
            padding: {metrics.padding_xs}px {metrics.padding_sm}px;
            min-height: {metrics.toolbar_height - 10}px;
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

    return "\n\n".join(sections + [toolbar_overrides, focus_reset])


__all__ = ["get_qss"]
