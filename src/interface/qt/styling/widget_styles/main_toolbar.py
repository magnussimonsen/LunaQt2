"""QSS generator for the main window toolbar."""

from __future__ import annotations

from textwrap import dedent

from interface.qt.styling.theme import (
    Theme,
    ThemeMode,
    get_theme,
    toolbar_tokens as get_toolbar_tokens,
)

TOOLBAR_SELECTOR = 'QToolBar#PrimaryToolBar'


def get_qss(
    mode: ThemeMode = ThemeMode.DARK,
    theme: Theme | None = None,
) -> str:
    """Return scoped QSS for the main application toolbar."""

    theme = theme or get_theme(mode)
    metrics = theme.metrics
    tokens = get_toolbar_tokens(metrics)
    bg = theme.bg
    border = theme.border

    toolbar_qss = dedent(
        f"""
        {TOOLBAR_SELECTOR} {{
            background-color: {bg.toolbar};
            color: {theme.text.primary};
            spacing: {tokens.spacing}px;
            padding: 0px {tokens.padding_horizontal}px;
            margin: 0px;
            border-top: {tokens.border_width}px solid {border.transparent};
            border-bottom: {tokens.border_width}px solid {border.transparent};
            border-radius: {tokens.border_radius}px;
            min-height: {tokens.min_height}px;
            font-family: {metrics.font_family};
            font-size: {metrics.font_size_medium}pt;
        }}
        """
    ).strip()

    return toolbar_qss


__all__ = ["get_qss"]
