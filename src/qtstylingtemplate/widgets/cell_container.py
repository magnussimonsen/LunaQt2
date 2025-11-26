"""Styles for custom cell container widgets (editors, table cells)."""

from __future__ import annotations

from textwrap import dedent

from qtstylingtemplate.theme import Theme, ThemeMode, get_theme

CELL_SELECTOR = 'QFrame[cellType="container"]'
CELL_HEADER_SELECTOR = 'QWidget[cellPart="header"]'


def get_qss(
    mode: ThemeMode = ThemeMode.DARK,
    theme: Theme | None = None,
) -> str:
    """Return QSS for container widgets that hold a cell view/editor."""

    theme = theme or get_theme(mode)
    metrics = theme.metrics
    bg = theme.bg
    border = theme.border
    text = theme.text
    viewport = theme.viewport

    container = dedent(
        f"""
        {CELL_SELECTOR} {{
            background-color: {bg.cell};
            border: {metrics.border_width}px solid {border.cell};
            border-radius: {metrics.radius_md}px;
            padding: {metrics.padding_md}px;
        }}

        {CELL_SELECTOR}[state="focused"] {{
            border-color: {border.cell_in_focus};
            box-shadow: 0 0 0 1px {border.cell_in_focus};
        }}
        """
    ).strip()

    header = dedent(
        f"""
        {CELL_SELECTOR} > {CELL_HEADER_SELECTOR} {{
            margin-bottom: {metrics.padding_sm}px;
            color: {text.secondary};
            font-size: {metrics.font_size_sm}pt;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }}
        """
    ).strip()

    viewport = dedent(
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

    return "\n\n".join([container, header, viewport])


__all__ = ["get_qss"]
