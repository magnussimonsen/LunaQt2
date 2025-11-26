"""Reusable sidebar widgets for the demo UI."""

from __future__ import annotations

try:  # pragma: no cover - imported during runtime
    from PySide6.QtCore import Qt, Signal
    from PySide6.QtWidgets import (
        QAbstractItemView,
        QComboBox,
        QFormLayout,
        QHBoxLayout,
        QLabel,
        QListWidget,
        QListWidgetItem,
        QPushButton,
        QSpinBox,
        QVBoxLayout,
        QWidget,
    )
except ModuleNotFoundError as exc:  # pragma: no cover - runtime guard
    raise SystemExit("PySide6 must be installed to use the sidebar widgets.") from exc


class SidebarActionRow(QWidget):
    """Simple horizontal container for action buttons inside a sidebar."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        self._layout = layout

    def add_widget(self, widget: QWidget) -> None:
        self._layout.addWidget(widget)

    def add_spacer(self) -> None:
        self._layout.addStretch(1)


class NotebookSidebarWidget(QWidget):
    """Notebook sidebar with add button, list, and rename support."""

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
            # Prevent empty labels from sticking around.
            self._is_updating = True
            item.setText(text)
            self._is_updating = False

        self.rename_notebook_requested.emit(notebook_id, text)


class SettingsSidebarWidget(QWidget):
    """Lightweight placeholder settings form for the demo window."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QFormLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        self.ui_font_combo = self._build_combo(["Inter", "Figtree", "JetBrains Mono"])
        layout.addRow("UI Font", self.ui_font_combo)

        self.ui_font_size = self._build_spinbox(8, 24, 14)
        layout.addRow("UI Size", self.ui_font_size)

        self.code_font_combo = self._build_combo(["Fira Code", "JetBrains Mono"])
        layout.addRow("Code Font", self.code_font_combo)

        self.code_font_size = self._build_spinbox(8, 24, 13)
        layout.addRow("Code Size", self.code_font_size)

        self.precision_spin = self._build_spinbox(0, 10, 4)
        layout.addRow("Precision", self.precision_spin)

        layout.addRow("", self._build_hint())

    @staticmethod
    def _build_combo(values: list[str]) -> QComboBox:
        combo = QComboBox()
        combo.addItems(values)
        combo.setEditable(False)
        return combo

    @staticmethod
    def _build_spinbox(min_value: int, max_value: int, current: int) -> QSpinBox:
        spin = QSpinBox()
        spin.setRange(min_value, max_value)
        spin.setValue(current)
        return spin

    @staticmethod
    def _build_hint() -> QWidget:
        label = QLabel("Settings wiring will land in a future pass.")
        label.setWordWrap(True)
        label.setProperty("statusRole", "info")
        return label


__all__ = [
    "NotebookSidebarWidget",
    "SettingsSidebarWidget",
    "SidebarActionRow",
]
