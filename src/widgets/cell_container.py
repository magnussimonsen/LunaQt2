"""Styles for custom cell container widgets (editors, table cells)."""

from __future__ import annotations

from textwrap import dedent

from theme import Theme, ThemeMode, cell_container_tokens, get_theme

CELL_LIST_SELECTOR = 'QWidget[cellType="list"]'
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
    spacing = cell_container_tokens(metrics)
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

    container = dedent(
        f"""
        {CELL_SELECTOR} {{
            background-color: {bg.cell};
            border: {spacing.border_width}px solid {border.cell};
            border-radius: {spacing.border_radius}px;
            padding: {spacing.padding}px;
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
            margin-bottom: {spacing.header_margin_bottom}px;
            color: {text.secondary};
            font-size: {metrics.font_size_small}pt;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }}
        """
    ).strip()

    body = dedent(
        f"""
        {CELL_SELECTOR} > {CELL_BODY_SELECTOR} {{
            background-color: {bg.cell};
            color: {text.primary};
            font-size: {metrics.font_size_medium}pt;
        }}
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

    return "\n\n".join([list_styling, container, header, body, viewport_block])


__all__ = ["get_qss"]
