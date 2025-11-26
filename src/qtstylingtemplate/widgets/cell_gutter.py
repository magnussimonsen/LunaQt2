"""Styles that control gutter decorations for editor-like widgets."""

from __future__ import annotations

from textwrap import dedent

from qtstylingtemplate.theme import Theme, ThemeMode, get_theme

GUTTER_SELECTOR = 'QWidget[cellType="gutter"]'
GUTTER_LABEL_SELECTOR = 'QLabel[cellRole="line-number"]'


def get_qss(
    mode: ThemeMode = ThemeMode.DARK,
    theme: Theme | None = None,
) -> str:
    """Return QSS for cell gutter areas (line numbers, icons, etc.)."""

    theme = theme or get_theme(mode)
    metrics = theme.metrics
    bg = theme.bg
    border = theme.border
    text = theme.text

    gutter = dedent(
        f"""
        {GUTTER_SELECTOR} {{
            background-color: {bg.cell_gutter};
            border-right: {metrics.border_width}px solid {border.cell_gutter};
            padding: 0 {metrics.padding_sm}px;
            color: {text.muted};
        }}

        {GUTTER_SELECTOR}[state="focused"] {{
            border-color: {border.cell_in_focus};
        }}
        """
    ).strip()

    labels = dedent(
        f"""
        {GUTTER_SELECTOR} > {GUTTER_LABEL_SELECTOR} {{
            color: {text.secondary};
            min-width: 32px;
            qproperty-alignment: AlignRight | AlignVCenter;
            font-family: {metrics.font_family};
            font-size: {metrics.font_size_sm}pt;
        }}
        """
    ).strip()

    return f"{gutter}\n\n{labels}"


__all__ = ["get_qss"]
