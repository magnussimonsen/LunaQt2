"""Styles that control gutter decorations for editor-like widgets."""

from __future__ import annotations

from textwrap import dedent

from interface.qt.styling.theme import Theme, ThemeMode, cell_gutter_tokens, get_theme

GUTTER_SELECTOR = 'QWidget[cellType="gutter"]'
GUTTER_LABEL_SELECTOR = 'QLabel[cellRole="line-number"]'


def get_qss(
    mode: ThemeMode = ThemeMode.DARK,
    theme: Theme | None = None,
) -> str:
    """Return QSS for cell gutter areas (line numbers, icons, etc.)."""

    theme = theme or get_theme(mode)
    metrics = theme.metrics
    spacing = cell_gutter_tokens(metrics)
    bg = theme.bg
    border = theme.border
    text = theme.text

    gutter = dedent(
        f"""
        {GUTTER_SELECTOR} {{
            background-color: {bg.cell_gutter};
            border-right: {spacing.border_width}px solid {bg.cell_gutter};
            border-radius: {spacing.border_radius}px;
            padding: {spacing.padding_top}px {spacing.padding_right}px {spacing.padding_bottom}px {spacing.padding_left}px;
            margin: {spacing.margin_top}px {spacing.margin_right}px {spacing.margin_bottom}px {spacing.margin_left}px;
            color: {text.muted};
        }}

        {GUTTER_SELECTOR}:hover {{
            border-color: {border.gutter_hover};
        }}

        {GUTTER_SELECTOR}[state="focused"],
        {GUTTER_SELECTOR}[state="selected"] {{
            background-color: {bg.selected_gutter};
            border-color: {border.gutter_in_focus};
        }}
        """
    ).strip()

    labels = dedent(
        f"""
        {GUTTER_SELECTOR} > {GUTTER_LABEL_SELECTOR} {{
            background-color: transparent;
            color: {text.secondary};
            min-width: {spacing.label_min_width}px;
            qproperty-alignment: 'AlignRight | AlignVCenter';
            font-family: {metrics.font_family};
            font-size: {metrics.font_size_small}pt;
        }}

        /* Labels inherit background from parent gutter */
        """
    ).strip()

    return f"{gutter}\n\n{labels}"


__all__ = ["get_qss"]
