"""Styles for custom cell container widgets (editors, table cells)."""

from __future__ import annotations

from textwrap import dedent

from interface.qt.styling.theme import Theme, ThemeMode, cell_container_tokens, get_theme

CELL_LIST_SELECTOR = 'QWidget[cellType="list"]'
CELL_ROW_SELECTOR = 'QFrame[cellType="row"]'
CELL_SELECTOR = 'QFrame[cellType="container"]'
CELL_HEADER_SELECTOR = 'QWidget[cellPart="header"]'
CELL_BODY_SELECTOR = 'QWidget[cellPart="body"]'
CELL_EDITOR_SELECTOR = 'QPlainTextEdit[cellPart="editor"]'
CELL_OUTPUT_SELECTOR = 'QPlainTextEdit[cellPart="output"]'


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
            border: 2px solid transparent;
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
    # Container INSIDE the cell row  cell_row(gutter - cell-container)
    container = dedent(
        f"""
        {CELL_SELECTOR} {{
            background-color: {bg.cell_bg};
            border-top: {tokens.border_width_top}px solid transparent;
            border-bottom: {tokens.border_width_bottom}px solid transparent;
            border-left: {tokens.border_width_left}px solid transparent;
            border-right: {tokens.border_width_right}px solid transparent;
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
            background-color: {bg.cell_bg};
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
            background-color: {bg.cell_bg};
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

    # Python code editor styling
    editor_block = dedent(
        f"""
        {CELL_EDITOR_SELECTOR} {{
            background-color: {bg.cell_bg};
            color: {text.primary};
            selection-background-color: {viewport.selection};
            selection-color: {viewport.selection_text};
            border: none;
            border-radius: {tokens.border_radius}px;
            padding: 4px;
        }}
        """
    ).strip()

    # Output area styling
    output_block = dedent(
        f"""
        {CELL_OUTPUT_SELECTOR} {{
            background-color: {bg.app_bg};
            color: {text.primary};
            selection-background-color: {viewport.selection};
            selection-color: {viewport.selection_text};
            border: 1px solid {border.subtle};
            border-radius: {tokens.border_radius}px;
            padding: 8px;
            font-family: "Fira Code", monospace;
            font-size: {metrics.font_size_small}pt;
        }}
        """
    ).strip()

    return "\n\n".join([list_styling, row_styling, container, header, body, viewport_block, editor_block, output_block])


__all__ = ["get_qss"]
