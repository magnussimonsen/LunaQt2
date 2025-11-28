"""Encapsulated status bar styling."""

from __future__ import annotations

from textwrap import dedent

from interface.qt.styling.theme import Theme, ThemeMode, get_theme, statusbar_tokens

STATUSBAR_SELECTOR = 'QStatusBar#MainStatusBar'


def get_qss(
    mode: ThemeMode = ThemeMode.DARK,
    theme: Theme | None = None,
) -> str:
    """Return QSS for the status bar including message labels."""

    theme = theme or get_theme(mode)
    metrics = theme.metrics
    spacing = statusbar_tokens(metrics)
    palette = theme.statusbar

    base = dedent(
        f"""
        {STATUSBAR_SELECTOR} {{
            background-color: {palette.background};
            color: {palette.text};
            border-top: {spacing.border_width}px solid {palette.border_top};
            padding: 0 {spacing.padding_horizontal}px;
            min-height: {spacing.min_height}px;
            font-family: {metrics.font_family};
            font-size: {metrics.font_size_small}pt;
        }}

        {STATUSBAR_SELECTOR} QLabel {{
            background-color: {palette.background};
            color: {palette.text};
        }}

        {STATUSBAR_SELECTOR} QLabel[statusRole="warning"] {{
            color: {palette.warning};
            font-weight: 600;
        }}
        """
    ).strip()

    return base


__all__ = ["get_qss"]
