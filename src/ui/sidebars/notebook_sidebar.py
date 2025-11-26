"""Notebook sidebar widget used by the demo window."""

from __future__ import annotations

try:  # pragma: no cover - only imported when Qt is available
    from PySide6.QtCore import Qt, Signal
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

from .sidebar_action_row import SidebarActionRow


class NotebookSidebarWidget(QWidget):
    """Sidebar panel that lists notebooks and exposes add/rename hooks."""

    add_notebook_clicked = Signal()
    notebook_selected = Signal(str)
    rename_notebook_requested = Signal(str, str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._is_updating = False
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        action_row = SidebarActionRow(self)
        add_button = QPushButton("Add Notebook", self)
        add_button.clicked.connect(self.add_notebook_clicked)
        action_row.add_widget(add_button)
        action_row.add_spacer()
        layout.addWidget(action_row)

        list_widget = QListWidget(self)
        list_widget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        list_widget.setEditTriggers(
            QAbstractItemView.EditTrigger.DoubleClicked
            | QAbstractItemView.EditTrigger.EditKeyPressed
        )
        list_widget.itemSelectionChanged.connect(self._on_selection_changed)
        list_widget.itemChanged.connect(self._on_item_changed)
        layout.addWidget(list_widget)

        self._list = list_widget
        self._add_button = add_button

    def set_notebooks(self, notebooks: list[dict[str, str]], active_notebook_id: str | None) -> None:
        """Populate the list with the provided notebook metadata."""

        self._is_updating = True
        self._list.clear()

        for notebook in notebooks:
            title = notebook.get("title") or "Untitled Notebook"
            item = QListWidgetItem(title)
            item.setData(Qt.ItemDataRole.UserRole, notebook.get("notebook_id"))
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
            self._list.addItem(item)

            if active_notebook_id and notebook.get("notebook_id") == active_notebook_id:
                self._list.setCurrentItem(item)

        self._is_updating = False

    def set_active_notebook(self, notebook_id: str) -> None:
        if not notebook_id:
            return

        self._is_updating = True
        for index in range(self._list.count()):
            item = self._list.item(index)
            if item.data(Qt.ItemDataRole.UserRole) == notebook_id:
                self._list.setCurrentItem(item)
                break
        self._is_updating = False

    def focus_add_button(self) -> None:
        self._add_button.setFocus()

    def _on_selection_changed(self) -> None:
        if self._is_updating:
            return

        item = self._list.currentItem()
        if not item:
            return

        notebook_id = item.data(Qt.ItemDataRole.UserRole)
        if isinstance(notebook_id, str):
            self.notebook_selected.emit(notebook_id)

    def _on_item_changed(self, item: QListWidgetItem) -> None:
        if self._is_updating:
            return

        notebook_id = item.data(Qt.ItemDataRole.UserRole)
        if not isinstance(notebook_id, str):
            return

        text = item.text().strip() or "Untitled Notebook"
        if text != item.text():
            self._is_updating = True
            item.setText(text)
            self._is_updating = False

        self.rename_notebook_requested.emit(notebook_id, text)


__all__ = ["NotebookSidebarWidget"]
