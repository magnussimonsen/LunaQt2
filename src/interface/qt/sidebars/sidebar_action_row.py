"""Shared toolbar layout used across sidebar panels."""

from __future__ import annotations

try:  # pragma: no cover - only imported when Qt is available
    from PySide6.QtWidgets import QHBoxLayout, QWidget
except ModuleNotFoundError as exc:  # pragma: no cover - runtime guard
    raise SystemExit("PySide6 must be installed to use the sidebar widgets.") from exc


class SidebarToolbar(QWidget):
    """Horizontal toolbar container for sidebar action buttons and controls."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("sidebarRole", "toolbar")
        self.setAutoFillBackground(True)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        self._layout = layout

    def add_widget(self, widget: QWidget) -> None:
        self._layout.addWidget(widget)

    def add_spacer(self) -> None:
        self._layout.addStretch(1)


__all__ = ["SidebarToolbar"]
