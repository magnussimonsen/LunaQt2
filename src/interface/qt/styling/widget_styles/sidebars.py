"""QSS snippet for docked sidebars (settings, notebooks, etc.)."""

from __future__ import annotations

from textwrap import dedent

from interface.qt.styling.theme import Theme, ThemeMode, get_theme, sidebar_tokens


def get_qss(
    mode: ThemeMode = ThemeMode.DARK,
    theme: Theme | None = None,
) -> str:
    """Return QSS that styles all dock-based sidebars consistently."""

    theme = theme or get_theme(mode)
    metrics = theme.metrics
    spacing = sidebar_tokens(metrics)  # sidebar_tokens = get_sidebar_tokens(metrics)We
    bg = theme.bg
    border = theme.border
    buttons = theme.buttons.sidebar_toolbar
    text = theme.text

    # =========================================================================
    # DOCK (SIDEBAR CONTAINER) WIDGET TITLE BAR
    # QDockWidget QSS can only style the title bar, NOT the content widget
    # =========================================================================
    title_block = dedent(
        f"""
        /* Dock widget title bar styling (header area) */
        QDockWidget#NotebooksDock::title,
        QDockWidget#SettingsDock::title,
        QDockWidget#TocDock::title {{
            background-color: {bg.sidebar_header_bg};
            color: {text.primary};
            text-align: left;
            padding-top: {spacing.sidebar_header_padding_top}px;
            padding-bottom: {spacing.sidebar_header_padding_bottom}px;
            padding-left: {spacing.sidebar_header_padding_left}px;
            padding-right: {spacing.sidebar_header_padding_right}px;
            border-top: {spacing.sidebar_header_border_top_width}px solid {border.subtle};
            border-bottom: {spacing.sidebar_header_border_bottom_width}px solid {border.subtle};
            border-left: {spacing.sidebar_header_border_left_width}px solid {border.subtle};
            border-right: {spacing.sidebar_header_border_right_width}px solid {border.subtle};
        }}
        """
    ).strip()

    # =========================================================================
    # MAIN SIDEBAR PANEL CONTAINER
    # Style the top-level widget that QDockWidget.setWidget() receives
    # =========================================================================
    panel_block = dedent(
        f"""
        /* Main sidebar panel containers */
        QWidget#NotebookSidebarPanel,
        QWidget#SettingsSidebarPanel,
        QWidget#TocSidebarPanel {{
            background-color: {bg.sidebar_bg};
            border-radius: {spacing.sidebar_container_border_radius}px;
            border-top: {spacing.sidebar_container_border_width_top}px solid {border.subtle};
            border-bottom: {spacing.sidebar_container_border_width_bottom}px solid {border.subtle};
            border-left: {spacing.sidebar_container_border_width_left}px solid {border.subtle};
            border-right: {spacing.sidebar_container_border_width_right}px solid {border.subtle};
        }}
        """
    ).strip()

    # =========================================================================
    # SIDEBAR SECTIONS (Toolbar and Content areas)
    # Target widgets by their sidebarRole property
    # =========================================================================
    sections_block = dedent(
        f"""
        /* Toolbar section at top of sidebar */
        QWidget[sidebarRole="toolbar"] {{
            background-color: {bg.sidebar_toolbar_bg};
            border-radius: {spacing.sidebar_toolbar_border_radius}px;
            border-top: {spacing.sidebar_toolbar_border_top_width}px solid {border.subtle};
            border-bottom: {spacing.sidebar_toolbar_border_bottom_width}px solid {border.subtle};
            border-left: {spacing.sidebar_toolbar_border_left_width}px solid {border.subtle};
            border-right: {spacing.sidebar_toolbar_border_right_width}px solid {border.subtle};
            padding-top: {spacing.sidebar_toolbar_padding_top}px;
            padding-bottom: {spacing.sidebar_toolbar_padding_bottom}px;
            padding-left: {spacing.sidebar_toolbar_padding_left}px;
            padding-right: {spacing.sidebar_toolbar_padding_right}px;
            margin-top: {spacing.sidebar_toolbar_margin_top}px;
            margin-bottom: {spacing.sidebar_toolbar_margin_bottom}px;
            margin-left: {spacing.sidebar_toolbar_margin_left}px;
            margin-right: {spacing.sidebar_toolbar_margin_right}px;
            min-height: {metrics.min_sidebar_toolbar_height}px;
        }}

        /* Content section below toolbar */
        QWidget[sidebarRole="content"] {{
              background-color: {bg.sidebar_content_bg};
            border-radius: {spacing.sidebar_content_border_radius}px;
            border-top: {spacing.sidebar_content_border_top_width}px solid {border.subtle};
            border-bottom: {spacing.sidebar_content_border_bottom_width}px solid {border.subtle};
            border-left: {spacing.sidebar_content_border_left_width}px solid {border.subtle};
            border-right: {spacing.sidebar_content_border_right_width}px solid {border.subtle};
            margin-top: {spacing.sidebar_content_margin_top}px;
            margin-bottom: {spacing.sidebar_content_margin_bottom}px;
            margin-left: {spacing.sidebar_content_margin_left}px;
            margin-right: {spacing.sidebar_content_margin_right}px;
        }}
        """
    ).strip()

    # =========================================================================
    # CHILD WIDGETS (Lists, Inputs, Labels)
    # Style specific widget types within sidebars
    # =========================================================================
    child_widgets_block = dedent(
        f"""
        /* List widgets */
        QDockWidget#NotebooksDock QListWidget,
        QDockWidget#SettingsDock QListWidget,
        QDockWidget#TocDock QListWidget {{
            background-color: transparent;
            border: none;
            color: {text.primary};
        }}

        QDockWidget#NotebooksDock QListWidget::item,
        QDockWidget#SettingsDock QListWidget::item,
        QDockWidget#TocDock QListWidget::item {{
            background-color: transparent;
            color: {text.primary};
            padding: 6px 8px;
            border-radius: 4px;
        }}

        QDockWidget#NotebooksDock QListWidget::item:selected,
        QDockWidget#SettingsDock QListWidget::item:selected,
        QDockWidget#TocDock QListWidget::item:selected {{
            background-color: {buttons.pressed};
            color: {buttons.text};
        }}
        
        QDockWidget#NotebooksDock QListWidget::item:hover,
        QDockWidget#SettingsDock QListWidget::item:hover,
        QDockWidget#TocDock QListWidget::item:hover {{
            background-color: {buttons.hover};
            color: {buttons.text};
        }}

        /* Input widgets (ComboBox, SpinBox) */
        QDockWidget#NotebooksDock QComboBox,
        QDockWidget#SettingsDock QComboBox,
        QDockWidget#TocDock QComboBox,
        QDockWidget#NotebooksDock QSpinBox,
        QDockWidget#SettingsDock QSpinBox,
        QDockWidget#TocDock QSpinBox {{
            background-color: {bg.sidebar_content_bg};
            border: {spacing.input_border_width}px solid {buttons.border};
            padding: {spacing.input_padding}px;
            border-radius: 2px;
        }}

        QDockWidget#NotebooksDock QComboBox:hover,
        QDockWidget#SettingsDock QComboBox:hover,
        QDockWidget#TocDock QComboBox:hover,
        QDockWidget#NotebooksDock QSpinBox:hover,
        QDockWidget#SettingsDock QSpinBox:hover,
        QDockWidget#TocDock QSpinBox:hover {{
            border-color: {buttons.focus};
        }}

        /* SpinBox buttons */
        QDockWidget#NotebooksDock QSpinBox::up-button,
        QDockWidget#SettingsDock QSpinBox::up-button,
        QDockWidget#TocDock QSpinBox::up-button,
        QDockWidget#NotebooksDock QSpinBox::down-button,
        QDockWidget#SettingsDock QSpinBox::down-button,
        QDockWidget#TocDock QSpinBox::down-button {{
            background-color: {buttons.normal};
            border: 1px solid {buttons.border};
            width: 16px;
            border-radius: 2px;
        }}

        QDockWidget#NotebooksDock QSpinBox::up-button:hover,
        QDockWidget#SettingsDock QSpinBox::up-button:hover,
        QDockWidget#TocDock QSpinBox::up-button:hover,
        QDockWidget#NotebooksDock QSpinBox::down-button:hover,
        QDockWidget#SettingsDock QSpinBox::down-button:hover,
        QDockWidget#TocDock QSpinBox::down-button:hover {{
            background-color: {buttons.hover};
            border-color: {buttons.focus};
        }}

        QDockWidget#NotebooksDock QSpinBox::up-button:pressed,
        QDockWidget#SettingsDock QSpinBox::up-button:pressed,
        QDockWidget#TocDock QSpinBox::up-button:pressed,
        QDockWidget#NotebooksDock QSpinBox::down-button:pressed,
        QDockWidget#SettingsDock QSpinBox::down-button:pressed,
        QDockWidget#TocDock QSpinBox::down-button:pressed {{
            background-color: {buttons.pressed};
            border-color: {buttons.focus};
        }}

        /* SpinBox arrows */
        QDockWidget#NotebooksDock QSpinBox::up-arrow,
        QDockWidget#SettingsDock QSpinBox::up-arrow,
        QDockWidget#TocDock QSpinBox::up-arrow {{
            width: 0;
            height: 0;
            border-left: 3px solid transparent;
            border-right: 3px solid transparent;
            border-bottom: 4px solid {buttons.text};
            margin: 0px;
        }}

        QDockWidget#NotebooksDock QSpinBox::down-arrow,
        QDockWidget#SettingsDock QSpinBox::down-arrow,
        QDockWidget#TocDock QSpinBox::down-arrow {{
            width: 0;
            height: 0;
            border-left: 3px solid transparent;
            border-right: 3px solid transparent;
            border-top: 4px solid {buttons.text};
            margin: 0px;
        }}

        /* Labels */
        QDockWidget#NotebooksDock QLabel,
        QDockWidget#SettingsDock QLabel,
        QDockWidget#TocDock QLabel {{
            background-color: transparent;
            color: {text.primary};
        }}
        """
    ).strip()

    return f"{title_block}\n\n{panel_block}\n\n{sections_block}\n\n{child_widgets_block}"


__all__ = ["get_qss"]
