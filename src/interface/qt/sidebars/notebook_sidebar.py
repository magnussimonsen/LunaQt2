"""Notebook sidebar widget used by the LunaQt2 window."""

from __future__ import annotations

try:  # pragma: no cover - only imported when Qt is available
    from PySide6.QtCore import Qt, Signal
    from PySide6.QtWidgets import (
        QHBoxLayout,
        QLabel,
        QListWidget,
        QPushButton,
        QVBoxLayout,
        QWidget,
    )
except ModuleNotFoundError as exc:  # pragma: no cover - runtime guard
    raise SystemExit("PySide6 must be installed to use the sidebar widgets.") from exc


class NotebookSidebarWidget(QWidget):
    """Sidebar panel placeholder that will later list notebooks."""

    add_notebook_clicked = Signal()
    notebook_selected = Signal(str)
    rename_notebook_requested = Signal(str, str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("NotebookSidebarPanel")
        self.setAutoFillBackground(True)
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        toolbar = QWidget(self)
        toolbar.setProperty("sidebarRole", "toolbar")
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(8, 8, 8, 8)
        toolbar_layout.setSpacing(8)
        toolbar_layout.addWidget(QLabel("Toolbar", toolbar))
        toolbar_layout.addStretch()
        layout.addWidget(toolbar)

        content = QWidget(self)
        content.setProperty("sidebarRole", "content")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(8, 8, 8, 8)
        content_layout.setSpacing(8)

        placeholder = QLabel("Content Area", content)
        placeholder.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        content_layout.addWidget(placeholder)
        content_layout.addStretch()

        layout.addWidget(content)

        self._list = QListWidget(content)
        self._list.setSelectionMode(QListWidget.SingleSelection)
        self._list.setProperty("sidebarRole", "content")
        content_layout.insertWidget(1, self._list)

        self._add_button = QPushButton("Add Notebook", toolbar)
        toolbar_layout.insertWidget(1, self._add_button)


__all__ = ["NotebookSidebarWidget"]
