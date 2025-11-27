"""Notebook sidebar widget used by the LunaQt2 window."""

from __future__ import annotations

try:  # pragma: no cover - only imported when Qt is available
    from PySide6.QtCore import Qt, Signal
    from PySide6.QtGui import QPalette, QColor
    from PySide6.QtWidgets import (
        QAbstractItemView,
        QListWidget,
        QListWidgetItem,
        QPushButton,
        QVBoxLayout,
        QWidget,
    )
except ModuleNotFoundError as exc:  # pragma: no cover - runtime guard
    raise SystemExit("PySide6 must be installed to use the sidebar widgets.") from exc

class NotebookSidebarWidget(QWidget):
    """Sidebar panel that lists notebooks and exposes add/rename hooks."""

    add_notebook_clicked = Signal()
    notebook_selected = Signal(str)
    rename_notebook_requested = Signal(str, str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("NotebookSidebarPanel")
        self.setAutoFillBackground(True)
        self._is_updating = False
        self._build_ui()

    def _build_ui(self) -> None:
        from PySide6.QtWidgets import QHBoxLayout, QLabel
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Add sidebar toolbar
        sidebar_toolbar = QWidget(self)
        sidebar_toolbar.setProperty("sidebarRole", "toolbar")
        sidebar_toolbar.setAutoFillBackground(True)
        toolbar_layout = QHBoxLayout(sidebar_toolbar)
        toolbar_layout.setContentsMargins(8, 8, 8, 8)
        toolbar_layout.setSpacing(8)
        toolbar_label = QLabel("Toolbar", sidebar_toolbar)
        toolbar_layout.addWidget(toolbar_label)
        toolbar_layout.addStretch()
        layout.addWidget(sidebar_toolbar)

        # Content area container
        content_container = QWidget(self)
        content_container.setProperty("sidebarRole", "content")
        content_container.setAutoFillBackground(True)
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(8, 8, 8, 8)
        
        content_label = QLabel("Content Area", content_container)
        content_layout.addWidget(content_label)
        content_layout.addStretch()
        
        layout.addWidget(content_container)
        
        self._list = None
        self._add_button = None


__all__ = ["NotebookSidebarWidget"]
