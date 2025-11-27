"""QSS snippet for docked sidebars (settings, notebooks, etc.)."""

from __future__ import annotations

from textwrap import dedent

from theme import Theme, ThemeMode, get_theme, sidebar_tokens

SIDEBAR_DOCK_SELECTOR = "QDockWidget#NotebooksDock, QDockWidget#SettingsDock"
SIDEBAR_ACTION_ROW_SELECTOR = 'QWidget[sidebarRole="action-row"]'


def get_qss(
    mode: ThemeMode = ThemeMode.DARK,
    theme: Theme | None = None,
) -> str:
    """Return QSS that styles all dock-based sidebars consistently."""

    theme = theme or get_theme(mode)
    metrics = theme.metrics
    spacing = sidebar_tokens(metrics)
    bg = theme.bg
    border = theme.border
    text = theme.text

    dock_block = dedent(
        f"""
        {SIDEBAR_DOCK_SELECTOR} {{
            background-color: {bg.sidebar_content};
            color: {text.primary};
            border-left: {spacing.dock_border_width}px solid {border.strong};
        }}

        QDockWidget#NotebooksDock::title,
        QDockWidget#SettingsDock::title {{
            background-color: {bg.sidebar_header};
            color: {text.primary};
            text-align: left;
            padding: {spacing.header_padding}px;
        }}

        {SIDEBAR_DOCK_SELECTOR} > QWidget {{
            background-color: {bg.sidebar_content};
        }}

        QDockWidget#NotebooksDock QWidget#NotebookSidebarPanel,
        QDockWidget#SettingsDock QWidget#SettingsSidebarPanel {{
            background-color: {bg.sidebar_content};
        }}
        """
    ).strip()

    toolbar_block = dedent(
        f"""
        QWidget[sidebarRole="toolbar"] {{
            background-color: {bg.sidebar_toolbar};
            color: {text.primary};
            padding: {spacing.toolbar_padding}px;
            border-bottom: {spacing.toolbar_border_width}px solid {border.strong};
        }}

        QWidget[sidebarRole="toolbar"] QLabel {{
            color: {text.primary};
        }}

        QWidget[sidebarRole="content"] {{
            background-color: {bg.sidebar_content};
            color: {text.primary};
        }}

        {SIDEBAR_ACTION_ROW_SELECTOR} {{
            background-color: {bg.sidebar_toolbar};
            border-radius: {spacing.action_row_radius}px;
            padding: {spacing.action_row_padding_y}px {spacing.action_row_padding_x}px;
        }}
        """
    ).strip()

    # Style child widgets inside sidebars to match the sidebar background
    child_widgets_block = dedent(
        f"""
        QDockWidget#NotebooksDock QListWidget,
        QDockWidget#SettingsDock QListWidget {{
            background-color: transparent;
            border: none;
            color: {text.primary};
        }}

        QDockWidget#NotebooksDock QListWidget::item,
        QDockWidget#SettingsDock QListWidget::item {{
            background-color: transparent;
            color: {text.primary};
        }}

        QDockWidget#NotebooksDock QListWidget::item:selected,
        QDockWidget#SettingsDock QListWidget::item:selected {{
            background-color: {bg.sidebar_toolbar};
            color: {text.primary};
        }}

        QDockWidget#NotebooksDock QComboBox,
        QDockWidget#SettingsDock QComboBox,
        QDockWidget#NotebooksDock QSpinBox,
        QDockWidget#SettingsDock QSpinBox {{
            background-color: {bg.sidebar_content};
            border: {spacing.input_border_width}px solid {border.subtle};
            padding: {spacing.input_padding}px;
        }}

        QDockWidget#NotebooksDock QComboBox:hover,
        QDockWidget#SettingsDock QComboBox:hover,
        QDockWidget#NotebooksDock QSpinBox:hover,
        QDockWidget#SettingsDock QSpinBox:hover {{
            border-color: {border.strong};
        }}

        QDockWidget#NotebooksDock QLabel,
        QDockWidget#SettingsDock QLabel {{
            background-color: transparent;
            color: {text.primary};
        }}
        """
    ).strip()

    return f"{dock_block}\n\n{toolbar_block}\n\n{child_widgets_block}"


__all__ = ["get_qss"]
