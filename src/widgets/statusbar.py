"""Encapsulated status bar styling."""

from __future__ import annotations

from textwrap import dedent

from theme import Theme, ThemeMode, get_theme

STATUSBAR_SELECTOR = 'QStatusBar#MainStatusBar'


def get_qss(
    mode: ThemeMode = ThemeMode.DARK,
    theme: Theme | None = None,
) -> str:
    """Return QSS for the status bar including message labels."""

    theme = theme or get_theme(mode)
    metrics = theme.metrics
    palette = theme.statusbar

    base = dedent(
        f"""
        {STATUSBAR_SELECTOR} {{
            background-color: {palette.background};
            color: {palette.text};
            border-top: {metrics.border_width}px solid {palette.border_top};
            padding: 0 {metrics.padding_medium}px;
            min-height: {metrics.statusbar_height}px;
            font-family: {metrics.font_family};
            font-size: {metrics.font_size_small}pt;
        }}

        {STATUSBAR_SELECTOR} QLabel {{
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
