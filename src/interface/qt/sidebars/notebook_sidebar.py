"""Notebook sidebar widget used by the LunaQt2 window."""

from __future__ import annotations

try:  # pragma: no cover - only imported when Qt is available
    from PySide6.QtCore import Qt, Signal
    from PySide6.QtGui import QColor, QPalette
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

from interface.qt.styling.theme.widget_tokens import SidebarTokens


class NotebookSidebarWidget(QWidget):
    """Sidebar panel placeholder that will later list notebooks."""

    add_notebook_clicked = Signal()
    notebook_selected = Signal(str)
    rename_notebook_requested = Signal(str, str)

    def __init__(self, parent: QWidget | None = None, *, tokens: SidebarTokens) -> None:
        super().__init__(parent)
        self.setObjectName("NotebookSidebarPanel")
        self.setAutoFillBackground(True)
        self._tokens = tokens
        self._build_ui()

    def _build_ui(self) -> None:
        """Build the 3-row sidebar layout: Header (via dock title) | Toolbar | Content."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            self._tokens.layout_root_margin_left,
            self._tokens.layout_root_margin_top,
            self._tokens.layout_root_margin_right,
            self._tokens.layout_root_margin_bottom,
        )
        layout.setSpacing(0)

        # Row 2: Toolbar with action buttons
        toolbar = self._build_toolbar()
        layout.addWidget(toolbar)

        # Row 3: Content area with notebook list
        content = self._build_content()
        layout.addWidget(content)

    def _build_toolbar(self) -> QWidget:
        """Build toolbar with Add Notebook button."""
        toolbar = QWidget(self)
        toolbar.setProperty("sidebarRole", "toolbar")
        toolbar.setAutoFillBackground(True)
        
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(
            self._tokens.layout_toolbar_margin_left,
            self._tokens.layout_toolbar_margin_top,
            self._tokens.layout_toolbar_margin_right,
            self._tokens.layout_toolbar_margin_bottom,
        )
        toolbar_layout.setSpacing(8)
        
        self._add_button = QPushButton("Add Notebook", toolbar)
        self._add_button.clicked.connect(self.add_notebook_clicked)
        toolbar_layout.addWidget(self._add_button)
        toolbar_layout.addStretch()
        
        return toolbar

    def _build_content(self) -> QWidget:
        """Build content area with notebook list."""
        content = QWidget(self)
        content.setProperty("sidebarRole", "content")
        content.setAutoFillBackground(True)
        
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(
            self._tokens.layout_content_margin_left,
            self._tokens.layout_content_margin_top,
            self._tokens.layout_content_margin_right,
            self._tokens.layout_content_margin_bottom,
        )
        content_layout.setSpacing(8)
        
        # Notebook list
        self._list = QListWidget(content)
        self._list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self._list.itemSelectionChanged.connect(self._on_selection_changed)
        content_layout.addWidget(self._list)
        
        # Placeholder items for testing
        self._list.addItem("Notebook 1")
        self._list.addItem("Notebook 2")
        self._list.addItem("Notebook 3")
        
        return content

    def _on_selection_changed(self) -> None:
        """Handle notebook selection changes."""
        selected = self._list.currentItem()
        if selected:
            self.notebook_selected.emit(selected.text())


__all__ = ["NotebookSidebarWidget"]
