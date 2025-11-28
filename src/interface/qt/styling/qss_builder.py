"""Utility to assemble and apply the full application style sheet."""

from __future__ import annotations

from typing import Iterable, Protocol

from interface.qt.styling.theme import Metrics, Theme, ThemeMode, get_theme
from interface.qt.styling.widget_styles import (
    buttons,
    cell_container,
    cell_gutter,
    main_menubar,
    sidebars,
    statusbar,
)

STYLE_MODULES = (
    buttons,
    cell_container,
    cell_gutter,
    main_menubar,
    sidebars,
    statusbar,
)


def _base_style(theme: Theme) -> str:
    metrics = theme.metrics
    bg = theme.bg
    text = theme.text
    return f"""
    QWidget {{
        background-color: {bg.app};
        color: {text.primary};
        font-family: {metrics.font_family};
        font-size: {metrics.font_size_medium}pt;
    }}

    QDockWidget#NotebooksDock,
    QDockWidget#SettingsDock,
    QDockWidget#NotebooksDock > QWidget,
    QDockWidget#SettingsDock > QWidget,
    QDockWidget#NotebooksDock QWidget#NotebookSidebarPanel,
    QDockWidget#SettingsDock QWidget#SettingsSidebarPanel {{
        background-color: {bg.sidebar_content};
        color: {text.primary};
    }}

    QDockWidget#NotebooksDock QWidget[sidebarRole="toolbar"],
    QDockWidget#SettingsDock QWidget[sidebarRole="toolbar"] {{
        background-color: {bg.sidebar_toolbar};
        color: {text.primary};
    }}

    QDockWidget#NotebooksDock QListWidget,
    QDockWidget#SettingsDock QListWidget {{
        color: {text.primary};
    }}

    QToolBar {{
        background-color: {bg.toolbar};
        spacing: {metrics.padding_small}px;
        padding: 0 {metrics.padding_small}px;
    }}
    """.strip()


def _collect_qss(modules: Iterable, theme: Theme) -> str:
    blocks = [_base_style(theme)]
    for module in modules:
        blocks.append(module.get_qss(mode=theme.mode, theme=theme))
    return "\n\n".join(blocks)


def build_application_qss(
    mode: ThemeMode = ThemeMode.DARK,
    theme: Theme | None = None,
    *,
    metrics: Metrics | None = None,
) -> str:
    """Expose concatenated QSS string for use in tests or debugging."""

    theme = theme or get_theme(mode, metrics=metrics)
    return _collect_qss(STYLE_MODULES, theme)


class _HasStyleSheet(Protocol):
    def setStyleSheet(self, style: str, /) -> None:  # pragma: no cover - provided by Qt
        ...


def apply_global_style(
    app: _HasStyleSheet,
    mode: ThemeMode = ThemeMode.DARK,
    *,
    metrics: Metrics | None = None,
) -> None:
    """Apply the assembled QSS onto the provided QApplication instance."""

    app.setStyleSheet(build_application_qss(mode=mode, metrics=metrics))


__all__ = ["build_application_qss", "apply_global_style"]
