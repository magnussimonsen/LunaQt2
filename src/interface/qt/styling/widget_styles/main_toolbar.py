"""QSS generator for the main window toolbar."""

from __future__ import annotations

from textwrap import dedent

from interface.qt.styling.theme import (
    Theme,
    ThemeMode,
    get_theme,
    main_toolbar_tokens as get_main_toolbar_tokens,
)

TOOLBAR_SELECTOR = 'QToolBar#PrimaryToolBar'


def get_qss(
    mode: ThemeMode = ThemeMode.DARK,
    theme: Theme | None = None,
) -> str:
    """Return scoped QSS for the main application toolbar."""

    theme = theme or get_theme(mode)
    metrics = theme.metrics
    tokens = get_main_toolbar_tokens(metrics)
    bg = theme.bg
    border = theme.border

    toolbar_qss = dedent(
        f"""
        {TOOLBAR_SELECTOR} {{
            background-color: {bg.toolbar_bg};
            color: {theme.text.primary};
            spacing: {tokens.spacing}px;

            padding-top: {tokens.padding_top}px;
            padding-bottom: {tokens.padding_bottom}px;
            padding-left: {tokens.padding_left}px;
            padding-right: {tokens.padding_right}px;
            
            margin-top: {tokens.margin_top}px;
            margin-bottom: {tokens.margin_bottom}px;
            margin-left: {tokens.margin_left}px;
            margin-right: {tokens.margin_right}px;

            border-top: {tokens.border_width}px solid {border.transparent};
            border-bottom: {tokens.border_width}px solid {border.transparent};
            border-left: {tokens.border_width}px solid {border.transparent};
            border-right: {tokens.border_width}px solid {border.transparent};
            
            border-radius: {tokens.border_radius}px;
            min-height: {tokens.min_height}px;
            font-family: {metrics.font_family};
            font-size: {metrics.font_size_medium}pt;
        }}
        
        {TOOLBAR_SELECTOR} > QWidget {{
            background-color: transparent;
        }}
        
        {TOOLBAR_SELECTOR} QStackedWidget {{
            background-color: transparent;
        }}
        """
    ).strip()

    return toolbar_qss


__all__ = ["get_qss"]
