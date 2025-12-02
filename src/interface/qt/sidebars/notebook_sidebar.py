"""Notebook sidebar widget used by the LunaQt2 window."""

from __future__ import annotations

try:  # pragma: no cover - only imported when Qt is available
    from PySide6.QtCore import Qt, Signal
    from PySide6.QtGui import QKeySequence, QShortcut
    from PySide6.QtWidgets import (
        QAbstractItemView,
        QHBoxLayout,
        QListWidget,
        QListWidgetItem,
        QPushButton,
        QSizePolicy,
        QVBoxLayout,
        QWidget,
    )
except ModuleNotFoundError as exc:  # pragma: no cover - runtime guard
    raise SystemExit("PySide6 must be installed to use the sidebar widgets.") from exc

from interface.qt.styling.theme.widget_tokens import ButtonTokens, SidebarTokens


class NotebookSidebarWidget(QWidget):
    """Sidebar panel placeholder that will later list notebooks."""

    add_notebook_clicked = Signal()
    move_notebook_up_clicked = Signal()
    move_notebook_down_clicked = Signal()
    notebook_selected = Signal(str)
    rename_notebook_requested = Signal(str, str)
    delete_notebook_requested = Signal(str)

    def __init__(
        self,
        parent: QWidget | None = None,
        *,
        tokens: SidebarTokens,
        button_tokens: ButtonTokens,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("NotebookSidebarPanel")
        self.setAutoFillBackground(True)
        self._tokens = tokens
        self._button_tokens = button_tokens
        self._suppress_item_changed = False
        self._build_ui()
        self._setup_shortcuts()

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
        """Build toolbar containing notebook management buttons."""
        toolbar = QWidget(self)
        toolbar.setProperty("sidebarRole", "toolbar")
        toolbar.setAutoFillBackground(True)
        toolbar.setMinimumHeight(self._tokens.sidebar_toolbar_min_height)
        toolbar.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(
            self._tokens.layout_toolbar_margin_left,
            self._tokens.layout_toolbar_margin_top,
            self._tokens.layout_toolbar_margin_right,
            self._tokens.layout_toolbar_margin_bottom,
        )
        toolbar_layout.setSpacing(self._tokens.sidebar_toolbar_item_x_spacing)
        
        self._add_button = QPushButton("Add Notebook", toolbar)
        self._add_button.clicked.connect(self.add_notebook_clicked)
        self._configure_toolbar_button(self._add_button)
        toolbar_layout.addWidget(self._add_button)

        self._move_up_button = QPushButton("Move Up", toolbar)
        self._move_up_button.clicked.connect(self.move_notebook_up_clicked)
        self._configure_toolbar_button(self._move_up_button)
        toolbar_layout.addWidget(self._move_up_button)

        self._move_down_button = QPushButton("Move Down", toolbar)
        self._move_down_button.clicked.connect(self.move_notebook_down_clicked)
        self._configure_toolbar_button(self._move_down_button)
        toolbar_layout.addWidget(self._move_down_button)
        toolbar_layout.addStretch()
        
        return toolbar

    def _configure_toolbar_button(self, button: QPushButton) -> None:
        """Apply shared sidebar toolbar styling hints to a button."""
        button.setProperty("btnType", "sidebar-toolbar")
        button.setMinimumHeight(self._button_tokens.sidebar_toolbar_min_height)

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
        
        self._list = QListWidget(content)
        self._list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self._list.setEditTriggers(
            QAbstractItemView.EditTrigger.DoubleClicked
            | QAbstractItemView.EditTrigger.EditKeyPressed
            | QAbstractItemView.EditTrigger.SelectedClicked
        )
        self._list.itemSelectionChanged.connect(self._on_selection_changed)
        self._list.itemChanged.connect(self._on_item_changed)

        content_layout.addWidget(self._list)

        return content

    def _setup_shortcuts(self) -> None:
        delete_shortcut = QShortcut(QKeySequence(Qt.Key_Delete), self._list)
        delete_shortcut.activated.connect(self._emit_delete_for_current)
        self._delete_shortcut = delete_shortcut

    # ------------------------------------------------------------------
    # Public API used by the main window
    # ------------------------------------------------------------------
    def set_notebooks(self, notebooks: list[tuple[str, str]]) -> None:
        self._with_suppressed_item_changed(self._list.clear)
        for notebook_id, title in notebooks:
            self._append_item(notebook_id, title)
        self._update_move_buttons()

    def add_notebook(self, notebook_id: str, title: str, *, select: bool = False) -> None:
        item = self._append_item(notebook_id, title)
        if select:
            self.select_notebook(notebook_id)
        self._update_move_buttons()
        return item

    def update_notebook_title(self, notebook_id: str, title: str) -> None:
        item = self._find_item(notebook_id)
        if not item:
            return
        self._set_item_title(item, title)

    def remove_notebook(self, notebook_id: str) -> str | None:
        row = self._row_for(notebook_id)
        if row is None:
            return self.current_notebook_id()

        self._with_suppressed_item_changed(lambda: self._list.takeItem(row))
        next_row = min(row, self._list.count() - 1)
        next_id: str | None = None
        if 0 <= next_row < self._list.count():
            next_item = self._list.item(next_row)
            next_id = next_item.data(self._NOTEBOOK_ID_ROLE)
        self._update_move_buttons()
        return next_id

    def restore_notebook_title(self, notebook_id: str) -> None:
        item = self._find_item(notebook_id)
        if not item:
            return
        previous_title = item.data(self._NOTEBOOK_TITLE_ROLE)
        if previous_title:
            self._set_item_title(item, previous_title)

    def select_notebook(self, notebook_id: str) -> None:
        row = self._row_for(notebook_id)
        if row is None:
            return
        self._list.setCurrentRow(row)

    def current_notebook_id(self) -> str | None:
        item = self._list.currentItem()
        if not item:
            return None
        return item.data(self._NOTEBOOK_ID_ROLE)

    def first_notebook_id(self) -> str | None:
        if self._list.count() == 0:
            return None
        return self._list.item(0).data(self._NOTEBOOK_ID_ROLE)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    _NOTEBOOK_ID_ROLE = Qt.ItemDataRole.UserRole
    _NOTEBOOK_TITLE_ROLE = Qt.ItemDataRole.UserRole + 1

    def _append_item(self, notebook_id: str, title: str) -> QListWidgetItem:
        item = QListWidgetItem()
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
        item.setData(self._NOTEBOOK_ID_ROLE, notebook_id)
        self._set_item_title(item, title)
        self._with_suppressed_item_changed(lambda: self._list.addItem(item))
        return item

    def _set_item_title(self, item: QListWidgetItem, title: str) -> None:
        def _apply() -> None:
            item.setText(title)
            item.setData(self._NOTEBOOK_TITLE_ROLE, title)

        self._with_suppressed_item_changed(_apply)

    def _row_for(self, notebook_id: str) -> int | None:
        for row in range(self._list.count()):
            item = self._list.item(row)
            if item.data(self._NOTEBOOK_ID_ROLE) == notebook_id:
                return row
        return None

    def _find_item(self, notebook_id: str) -> QListWidgetItem | None:
        row = self._row_for(notebook_id)
        return self._list.item(row) if row is not None else None

    def _with_suppressed_item_changed(self, callback) -> None:
        previous = self._suppress_item_changed
        self._suppress_item_changed = True
        try:
            callback()
        finally:
            self._suppress_item_changed = previous

    def _emit_delete_for_current(self) -> None:
        notebook_id = self.current_notebook_id()
        if notebook_id:
            self.delete_notebook_requested.emit(notebook_id)

    def _on_selection_changed(self) -> None:
        """Handle notebook selection changes."""
        selected = self._list.currentItem()
        if selected:
            notebook_id = selected.data(self._NOTEBOOK_ID_ROLE)
            if notebook_id:
                self.notebook_selected.emit(notebook_id)
        self._update_move_buttons()

    def _on_item_changed(self, item: QListWidgetItem) -> None:
        if self._suppress_item_changed:
            return

        notebook_id = item.data(self._NOTEBOOK_ID_ROLE)
        if not notebook_id:
            return

        new_title = item.text().strip()
        if not new_title:
            self.restore_notebook_title(notebook_id)
            return

        previous_title = item.data(self._NOTEBOOK_TITLE_ROLE)
        if previous_title == new_title:
            return

        self.rename_notebook_requested.emit(notebook_id, new_title)

    def _update_move_buttons(self) -> None:
        if not hasattr(self, "_move_up_button"):
            return

        count = self._list.count()
        current_row = self._list.currentRow()
        has_selection = current_row >= 0

        self._move_up_button.setEnabled(has_selection and current_row > 0)
        self._move_down_button.setEnabled(has_selection and current_row < count - 1)


__all__ = ["NotebookSidebarWidget"]
