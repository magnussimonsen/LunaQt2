"""Shared row layout used across sidebar panels."""

from __future__ import annotations

try:  # pragma: no cover - only imported when Qt is available
    from PySide6.QtWidgets import QHBoxLayout, QWidget
except ModuleNotFoundError as exc:  # pragma: no cover - runtime guard
    raise SystemExit("PySide6 must be installed to use the sidebar widgets.") from exc


class SidebarActionRow(QWidget):
    """Simple horizontal container for action buttons inside a sidebar."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("sidebarRole", "action-row")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        self._layout = layout

    def add_widget(self, widget: QWidget) -> None:
        self._layout.addWidget(widget)

    def add_spacer(self) -> None:
        self._layout.addStretch(1)


__all__ = ["SidebarActionRow"]
