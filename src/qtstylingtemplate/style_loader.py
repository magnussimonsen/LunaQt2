"""Utility to assemble and apply the full application style sheet."""

from __future__ import annotations

from typing import Iterable, Protocol

from qtstylingtemplate.theme import Theme, ThemeMode, get_theme
from qtstylingtemplate.widgets import buttons, cell_container, cell_gutter, main_menubar, statusbar

STYLE_MODULES = (
    buttons,
    main_menubar,
    statusbar,
    cell_container,
    cell_gutter,
)


def _base_style(theme: Theme) -> str:
    metrics = theme.metrics
    return f"""
    QWidget {{
        background-color: {theme.bg.app};
        color: {theme.text.primary};
        font-family: {metrics.font_family};
        font-size: {metrics.font_size_md}pt;
    }}

    QToolBar {{
        background-color: {theme.bg.toolbar};
        spacing: {metrics.padding_sm}px;
        padding: 0 {metrics.padding_sm}px;
    }}
    """.strip()


def _collect_qss(modules: Iterable, theme: Theme) -> str:
    """Return concatenated QSS from all provided modules."""

    blocks = [_base_style(theme)]
    for module in modules:
        blocks.append(module.get_qss(mode=theme.mode, theme=theme))
    return "\n\n".join(blocks)


def build_application_qss(
    mode: ThemeMode = ThemeMode.DARK,
    theme: Theme | None = None,
) -> str:
    """Expose concatenated QSS string for use in tests or debugging."""

    theme = theme or get_theme(mode)
    return _collect_qss(STYLE_MODULES, theme)


class _HasStyleSheet(Protocol):
    def setStyleSheet(self, style: str, /) -> None:  # pragma: no cover - runtime provided by Qt
        ...


def apply_global_style(app: _HasStyleSheet, mode: ThemeMode = ThemeMode.DARK) -> None:
    """Apply the assembled QSS onto the provided QApplication instance."""

    app.setStyleSheet(build_application_qss(mode=mode))


__all__ = ["build_application_qss", "apply_global_style"]
