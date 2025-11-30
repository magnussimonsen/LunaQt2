"""Styles for custom cell container widgets (editors, table cells)."""

from __future__ import annotations

from textwrap import dedent

from interface.qt.styling.theme import Theme, ThemeMode, cell_container_tokens, get_theme

CELL_LIST_SELECTOR = 'QWidget[cellType="list"]'
CELL_ROW_SELECTOR = 'QFrame[cellType="row"]'
CELL_SELECTOR = 'QFrame[cellType="container"]'
CELL_HEADER_SELECTOR = 'QWidget[cellPart="header"]'
CELL_BODY_SELECTOR = 'QWidget[cellPart="body"]'


def get_qss(
    mode: ThemeMode = ThemeMode.DARK,
    theme: Theme | None = None,
) -> str:
    """Return QSS for container widgets that hold a cell view/editor."""

    theme = theme or get_theme(mode)
    metrics = theme.metrics
    tokens = cell_container_tokens(metrics)
    bg = theme.bg
    border = theme.border
    text = theme.text
    viewport = theme.viewport

    list_styling = dedent(
        f"""
        {CELL_LIST_SELECTOR} {{
            background: transparent;
        }}
        """
    ).strip()

    row_styling = dedent(
        f"""
        {CELL_ROW_SELECTOR} {{
            background: transparent;
            border: 2px solid {border.subtle};
            border-radius: {tokens.border_radius}px;
            margin-top: {tokens.margin_top}px;
            margin-bottom: {tokens.margin_bottom}px;
            margin-left: {tokens.margin_left}px;
            margin-right: {tokens.margin_right}px;
        }}

        {CELL_ROW_SELECTOR}:hover {{
            border: 2px solid {border.cell_hover};
        }}

        {CELL_ROW_SELECTOR}[state="selected"] {{
            border: 2px solid {border.cell_in_focus};
        }}
        """
    ).strip()

    container = dedent(
        f"""
        {CELL_SELECTOR} {{
            background-color: {bg.cell};
            border-top: {tokens.border_width_top}px solid {border.cell};
            border-bottom: {tokens.border_width_bottom}px solid {border.cell};
            border-left: {tokens.border_width_left}px solid {border.cell};
            border-right: {tokens.border_width_right}px solid {border.cell};
            border-radius: {tokens.border_radius}px;

            padding-top: {tokens.padding_top}px;
            padding-bottom: {tokens.padding_bottom}px;
            padding-left: {tokens.padding_left}px;
            padding-right: {tokens.padding_right}px;

            margin-top: {tokens.margin_top}px;
            margin-bottom: {tokens.margin_bottom}px;
            margin-left: {tokens.margin_left}px;
            margin-right: {tokens.margin_right}px;
        }}

        {CELL_SELECTOR}:hover {{
            border-color: {border.cell_hover};
        }}

        {CELL_SELECTOR}[state="focused"],
        {CELL_SELECTOR}[state="selected"] {{
            border-color: {border.cell_in_focus};
        }}
        """
    ).strip()

    header = dedent(
        f"""
        {CELL_SELECTOR} > {CELL_HEADER_SELECTOR} {{
            background-color: {bg.cell};
            margin-bottom: {tokens.header_margin_bottom}px;
            color: {text.secondary};
            font-size: {metrics.font_size_small}pt;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }}

        /* Header inherits border from parent cell container */
        """
    ).strip()

    body = dedent(
        f"""
        {CELL_SELECTOR} > {CELL_BODY_SELECTOR} {{
            background-color: {bg.cell};
            color: {text.primary};
            font-size: {metrics.cell_body_font_size}pt;
        }}

        /* Body inherits border from parent cell container */
        """
    ).strip()

    viewport_block = dedent(
        f"""
        {CELL_SELECTOR} QTextEdit,
        {CELL_SELECTOR} QTableView {{
            background-color: {viewport.base};
            alternate-background-color: {viewport.alternate};
            color: {text.primary};
            selection-background-color: {viewport.selection};
            selection-color: {viewport.selection_text};
            border: none;
        }}
        """
    ).strip()

    return "\n\n".join([list_styling, row_styling, container, header, body, viewport_block])


__all__ = ["get_qss"]
