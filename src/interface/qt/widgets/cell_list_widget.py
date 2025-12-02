"""Scrollable container for the notebook cell rows."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QScrollArea, QWidget, QVBoxLayout


class CellListWidget(QScrollArea):
    """Scroll area that exposes the inner layout for cell rows."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("CellListScrollArea")
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFrameShape(QScrollArea.NoFrame)
        container = QWidget()
        container.setObjectName("CellListViewport")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setWidget(container)
        self._container = container
        self._layout = layout

    def container_widget(self) -> QWidget:
        return self._container

    def content_layout(self) -> QVBoxLayout:
        return self._layout


__all__ = ["CellListWidget"]
