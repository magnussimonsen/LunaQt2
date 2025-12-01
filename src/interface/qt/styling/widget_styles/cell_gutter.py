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
    """Return QSS for cell gutter areas (line numbers, icons, etc.).

    Widget code handles layout-only concerns (layout insets, label configuration)
    while this module focuses on paint-time styling such as background, borders,
    and typography.
    """

    theme = theme or get_theme(mode)
    metrics = theme.metrics
    tokens = cell_gutter_tokens(metrics)
    bg = theme.bg
    border = theme.border
    text = theme.text

    gutter = dedent(
        f"""
        {GUTTER_SELECTOR} {{
            background-color: {bg.cell_gutter_bg};
            border-top: {tokens.border_width_top}px solid {border.subtle};
            border-bottom: {tokens.border_width_bottom}px solid {border.subtle};
            border-left: {tokens.border_width_left}px solid {border.subtle};
            border-right: {tokens.border_width_right}px solid {border.subtle};
            border-radius: {metrics.radius_zero}px;
            padding-top: {tokens.paint_padding_top}px;
            padding-right: {tokens.paint_padding_right}px;
            padding-bottom: {tokens.paint_padding_bottom}px;
            padding-left: {tokens.paint_padding_left}px;
            margin: 0px;
        }}
        /* For focused/selected states */
        /* Add more qss if needed */

        {GUTTER_SELECTOR}[state="focused"],
        {GUTTER_SELECTOR}[state="selected"] {{
            background-color: {bg.selected_gutter_bg};
        }}

        {GUTTER_SELECTOR}:hover,
        {GUTTER_SELECTOR}[state="focused"]:hover,
        {GUTTER_SELECTOR}[state="selected"]:hover {{
            background-color: {bg.hover_bg};
        }}
        """
    ).strip()
     
    # The index number 
    labels = dedent(
        f"""
        {GUTTER_SELECTOR} > {GUTTER_LABEL_SELECTOR} {{
            background-color: transparent;
            color: {text.secondary};
            min-width: {tokens.label_min_width}px;
            qproperty-alignment: 'AlignRight | AlignVCenter';
            font-family: {metrics.font_family};
            font-size: {metrics.font_size_small}pt;
        }}

        /* Labels inherit background from parent gutter */
        """
    ).strip()

    return f"{gutter}\n\n{labels}"


__all__ = ["get_qss"]
