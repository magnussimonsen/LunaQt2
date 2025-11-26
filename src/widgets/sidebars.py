"""QSS snippet for docked sidebars (settings, notebooks, etc.)."""

from __future__ import annotations

from textwrap import dedent

from theme import Theme, ThemeMode, get_theme

SIDEBAR_DOCK_SELECTOR = "QDockWidget#NotebooksDock, QDockWidget#SettingsDock"
SIDEBAR_ACTION_ROW_SELECTOR = 'QWidget[sidebarRole="action-row"]'


def get_qss(
    mode: ThemeMode = ThemeMode.DARK,
    theme: Theme | None = None,
) -> str:
    """Return QSS that styles all dock-based sidebars consistently."""

    theme = theme or get_theme(mode)
    metrics = theme.metrics
    bg = theme.bg
    border = theme.border
    text = theme.text

    dock_block = dedent(
        f"""
        {SIDEBAR_DOCK_SELECTOR} {{
            background-color: {bg.sidebar};
            color: {text.primary};
            border-left: {metrics.border_width}px solid {border.strong};
        }}

        {SIDEBAR_DOCK_SELECTOR} QWidget {{
            background-color: {bg.sidebar};
        }}
        """
    ).strip()

    action_row_block = dedent(
        f"""
        {SIDEBAR_ACTION_ROW_SELECTOR} {{
            background-color: {bg.sidebar_toolbar};
            border-radius: {metrics.radius_small}px;
            padding: {metrics.padding_extra_small}px {metrics.padding_small}px;
        }}
        """
    ).strip()

    return f"{dock_block}\n\n{action_row_block}"


__all__ = ["get_qss"]
