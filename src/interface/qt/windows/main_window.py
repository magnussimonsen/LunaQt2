"""Main LunaQt2 window and helper widgets."""

from __future__ import annotations

from dataclasses import replace
from typing import Any, Sequence

from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QAction, QActionGroup
from PySide6.QtWidgets import (
    QDockWidget,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    QStatusBar,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from app.state import AppState
from core import CellManager, DataStore, NotebookManager
from core.models import Cell, CellType, Notebook, NotebookState
from interface.qt.sidebars import NotebookSidebarWidget, SettingsSidebarWidget, TocSidebarWidget
from interface.qt.styling import apply_global_style
from interface.qt.styling.theme import Metrics, StylePreferences, ThemeMode
from interface.qt.styling.theme.widget_tokens import (
    ButtonTokens,
    button_tokens,
    CellGutterTokens,
    CellRowTokens,
    cell_gutter_tokens,
    cell_row_tokens,
    CellListTokens,
    cell_list_tokens,
    SidebarTokens,
    sidebar_tokens,
)
from interface.qt.widgets import (
    CellContainerWidget,
    CellGutterWidget,
    SidebarToggleButton,
    CellListWidget,
    DynamicToolbar,
)
from shared.constants import (
    DEFAULT_SIDEBAR_WIDTH,
    MAX_SIDEBAR_WIDTH,
    MIN_SIDEBAR_WIDTH,
    MIN_UI_FONT_POINT_SIZE,
    MAX_UI_FONT_POINT_SIZE,
    FONT_SIZE_STEP,
    clamp_ui_font_point_size,
)


class CellRow(QFrame):
    """Row that combines the gutter and the styled cell content."""

    def __init__(
        self,
        cell_id: str,
        index: int,
        header_text: str,
        body_text: str,
        select_callback,
        gutter_callback,
        row_tokens: CellRowTokens,
        gutter_tokens: CellGutterTokens,
    ) -> None:
        super().__init__()
        self.setProperty("cellType", "row")
        self.setFrameStyle(QFrame.NoFrame)
        self._select_callback = select_callback
        self._gutter_callback = gutter_callback
        self._cell_id = cell_id
        self._index = index
        self._selected = False
        self._row_tokens = row_tokens
        self._gutter_tokens = gutter_tokens
        self.setMinimumHeight(row_tokens.cell_row_min_height)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)

        row_layout = QHBoxLayout(self)
        row_layout.setContentsMargins(
            row_tokens.cell_row_margin_left,
            row_tokens.cell_row_margin_top,
            row_tokens.cell_row_margin_right,
            row_tokens.cell_row_margin_bottom,
        )
        row_layout.setSpacing(row_tokens.gutter_gap)

        self._gutter = CellGutterWidget(index=index, tokens=gutter_tokens)
        gutter_width = (
            gutter_tokens.label_min_width
            + gutter_tokens.layout_inset_left
            + gutter_tokens.layout_inset_right
        )
        self._gutter.setFixedWidth(gutter_width)
        self._gutter.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        self._cell_container = CellContainerWidget(tokens=row_tokens)
        self._cell_container.setMinimumHeight(row_tokens.cell_row_min_height)
        self._cell_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)

        header = QLabel(header_text, self._cell_container)
        header.setProperty("cellPart", "header")
        header.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self._cell_container.add_content_widget(header)
        self._header_label = header

        body = QLabel(body_text, self._cell_container)
        body.setProperty("cellPart", "body")
        body.setWordWrap(True)
        body.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self._cell_container.add_content_widget(body)
        self._body_label = body

        row_layout.addWidget(self._gutter)
        row_layout.addWidget(self._cell_container)

        self._gutter.installEventFilter(self)
        self._cell_container.installEventFilter(self)

    def eventFilter(self, watched, event):
        if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
            if watched is self._cell_container:
                self._select_callback(self)
                return True
            if watched is self._gutter:
                self._gutter_callback(self)
                return True
        return super().eventFilter(watched, event)

    def set_selected(self, selected: bool) -> None:
        if self._selected == selected:
            return
        self._selected = selected
        state_value = "selected" if selected else ""
        self._apply_state(self, state_value)
        self._apply_state(self._cell_container, state_value)
        self._apply_state(self._gutter, state_value)

    def is_selected(self) -> bool:
        return self._selected

    @property
    def cell_id(self) -> str:
        return self._cell_id

    def set_index(self, index: int) -> None:
        if index == self._index:
            return
        self._index = index
        self._gutter.set_index(index)

    def update_text(self, header_text: str, body_text: str) -> None:
        self._header_label.setText(header_text)
        self._body_label.setText(body_text)

    @staticmethod
    def _apply_state(widget, state):
        widget.setProperty("state", state)
        widget.style().unpolish(widget)
        widget.style().polish(widget)


class LunaQtWindow(QMainWindow):
    """Main LunaQt2 window that lights up the different style modules."""

    def __init__(
        self,
        app: Any,
        mode: ThemeMode,
        *,
        ui_font_choices: Sequence[str],
        style_preferences: StylePreferences | None = None,
    ) -> None:
        super().__init__()
        self._app = app
        self._mode = mode
        self._available_ui_fonts = list(ui_font_choices)
        if not self._available_ui_fonts:
            raise ValueError("At least one UI font choice must be provided.")
        base_preferences = style_preferences or StylePreferences()
        normalized_size = clamp_ui_font_point_size(base_preferences.ui_font_size)
        if base_preferences.ui_font_size != normalized_size:
            base_preferences = replace(base_preferences, ui_font_size=normalized_size)
        if base_preferences.ui_font_family not in self._available_ui_fonts:
            base_preferences = replace(base_preferences, ui_font_family=self._available_ui_fonts[0])
        self._style_preferences = base_preferences
        self._theme_group = QActionGroup(self)
        self._theme_group.setExclusive(True)
        self._theme_actions: dict[str, Any] = {}
        self._cell_rows: list[CellRow] = []
        self._cell_list_widget: CellListWidget | None = None
        self._cell_list_layout: QVBoxLayout | None = None
        self._cell_list_spacer: QSpacerItem | None = None
        self._empty_state_label: QLabel | None = None
        self._current_notebook_state: NotebookState | None = None
        self._move_cell_up_action: QAction | None = None
        self._move_cell_down_action: QAction | None = None
        self._delete_cell_action: QAction | None = None
        self._delete_notebook_action: QAction | None = None
        self._app_state = AppState()
        self._data_store: DataStore | None = None
        self._cell_manager: CellManager | None = None
        self._notebook_manager: NotebookManager | None = None
        #self._notebooks_panel: NotebookSidebarWidget | None = None
        self._notebooks_toolbar: NotebookSidebarWidget | None = None
        self._settings_toolbar: SettingsSidebarWidget | None = None 
        #self._settings_panel: SettingsSidebarWidget | None = None # DEPRECATED
        #self._toc_panel: TocSidebarWidget | None = None # DEPRECATED
        self._toc_toolbar: TocSidebarWidget | None = None 

        self._notebooks_dock: QDockWidget | None = None
        self._settings_dock: QDockWidget | None = None
        self._toc_dock: QDockWidget | None = None
        self._notebooks_button: SidebarToggleButton | None = None
        self._settings_button: SidebarToggleButton | None = None
        self._toc_button: SidebarToggleButton | None = None
        self._move_up_button: QPushButton | None = None
        self._move_down_button: QPushButton | None = None
        self._dynamic_toolbar: DynamicToolbar | None = None

        self.setWindowTitle("LunaQt2")
        self.resize(900, 600)

        self._setup_core()
        self._build_menubar()
        self._build_toolbar()
        self._build_central()
        self._build_statusbar()
        self._build_sidebars()
        self._initialize_notebook_sidebar()
        self._apply_current_style()

    def _build_menubar(self) -> None:
        menu_bar = self.menuBar()
        menu_bar.setObjectName("MainMenuBar")

        file_menu = menu_bar.addMenu("File")
        file_menu.setProperty("menuRole", "primary")
        file_menu.addAction("New")
        file_menu.addAction("Save")
        file_menu.addAction("Save As…")

        edit_menu = menu_bar.addMenu("Edit")
        edit_menu.setProperty("menuRole", "primary")
        move_cell_up_action = QAction("Move Cell Up", self)
        move_cell_up_action.triggered.connect(self._on_move_cell_up_clicked)
        edit_menu.addAction(move_cell_up_action)
        self._move_cell_up_action = move_cell_up_action

        move_cell_down_action = QAction("Move Cell Down", self)
        move_cell_down_action.triggered.connect(self._on_move_cell_down_clicked)
        edit_menu.addAction(move_cell_down_action)
        self._move_cell_down_action = move_cell_down_action

        edit_menu.addSeparator()

        delete_cell_action = QAction("Delete Cell", self)
        delete_cell_action.triggered.connect(self._on_delete_cell_triggered)
        edit_menu.addAction(delete_cell_action)
        self._delete_cell_action = delete_cell_action

        delete_notebook_action = QAction("Delete Notebook", self)
        delete_notebook_action.triggered.connect(self._on_delete_notebook_triggered)
        edit_menu.addAction(delete_notebook_action)
        self._delete_notebook_action = delete_notebook_action

        insert_menu = menu_bar.addMenu("Insert")
        insert_menu.setProperty("menuRole", "primary")

        insert_markdown_action = QAction("Insert Markdown Cell", self)
        insert_markdown_action.triggered.connect(self._on_insert_markdown_cell)
        insert_menu.addAction(insert_markdown_action)

        insert_python_action = QAction("Insert Python Cell", self)
        insert_python_action.triggered.connect(self._on_insert_python_cell)
        insert_menu.addAction(insert_python_action)

        insert_cas_action = QAction("Insert CAS Cell", self)
        insert_cas_action.setEnabled(False)
        insert_cas_action.setToolTip("CAS support is not available yet.")
        insert_menu.addAction(insert_cas_action)

        view_menu = menu_bar.addMenu("View")
        view_menu.setProperty("menuRole", "primary")

        for label, mode_value in (("Light Mode", ThemeMode.LIGHT), ("Dark Mode", ThemeMode.DARK)):
            action = QAction(label, self)
            action.setCheckable(True)
            action.triggered.connect(lambda checked, m=mode_value: self._switch_theme(m) if checked else None)
            view_menu.addAction(action)
            self._theme_group.addAction(action)
            self._theme_actions[mode_value.value] = action

        self._theme_actions[self._mode.value].setChecked(True)

        self._install_cell_action_buttons(menu_bar)
        self._install_sidebar_corner_buttons(menu_bar)
        self._update_cell_action_states()

    def _install_cell_action_buttons(self, menu_bar) -> None:
        move_up_btn = QPushButton("Move cell up ↑")
        move_up_btn.setProperty("btnType", "menubar")
        move_up_btn.setToolTip("Move Cell Up")
        move_up_btn.clicked.connect(self._on_move_cell_up_clicked)

        move_down_btn = QPushButton("Move cell down ↓")
        move_down_btn.setProperty("btnType", "menubar")
        move_down_btn.setToolTip("Move Cell Down")
        move_down_btn.clicked.connect(self._on_move_cell_down_clicked)

        self._move_up_button = move_up_btn
        self._move_down_button = move_down_btn
        self._update_cell_action_states()

    def _install_sidebar_corner_buttons(self, menu_bar) -> None:
        corner = QWidget(menu_bar)
        corner.setProperty("widgetRole", "menubar-corner")
        layout = QHBoxLayout(corner)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        if self._move_up_button and self._move_down_button:
            layout.addWidget(self._move_up_button)
            layout.addWidget(self._move_down_button)
        
        
        toc_button = SidebarToggleButton(
            "Table of Contents",
            on_toggle=self._toggle_toc_sidebar,
            parent=corner,
            tooltip="Show or hide the Table of Contents sidebar",
        )
        layout.addWidget(toc_button)

        notebooks_button = SidebarToggleButton(
            "Notebooks",
            on_toggle=self._toggle_notebooks_sidebar,
            parent=corner,
            tooltip="Show or hide the Notebooks sidebar",
        )
        layout.addWidget(notebooks_button)

        settings_button = SidebarToggleButton(
            "Settings",
            on_toggle=self._toggle_settings_sidebar,
            parent=corner,
            tooltip="Show or hide the Settings sidebar",
        )
        layout.addWidget(settings_button)


        layout.addStretch(1)
        menu_bar.setCornerWidget(corner, Qt.Corner.TopRightCorner)

        self._toc_button = toc_button
        self._notebooks_button = notebooks_button
        self._settings_button = settings_button

    def _build_toolbar(self) -> None:
        toolbar = QToolBar("Main Toolbar")
        toolbar.setObjectName("PrimaryToolBar")
        toolbar.setMovable(False)

        self._dynamic_toolbar = DynamicToolbar()
        self._dynamic_toolbar.run_requested.connect(self._on_run_code)
        self._dynamic_toolbar.stop_requested.connect(self._on_stop_code)
        self._dynamic_toolbar.preview_toggled.connect(self._on_preview_toggled)

        toolbar.addWidget(self._dynamic_toolbar)
        self.addToolBar(toolbar)

    def _build_central(self) -> None:
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        cell_list = CellListWidget()
        viewport = cell_list.container_widget()
        viewport.setProperty("cellType", "list")
        list_layout = cell_list.content_layout()

        metrics = self._current_metrics()
        list_tokens = cell_list_tokens(metrics)

        list_layout.setContentsMargins(
            list_tokens.content_margin_left,
            list_tokens.content_margin_top,
            list_tokens.content_margin_right,
            list_tokens.content_margin_bottom,
        )
        list_layout.setSpacing(list_tokens.content_spacing)

        self._cell_list_widget = cell_list
        self._cell_list_layout = list_layout

        empty_label = QLabel("This notebook has no cells yet. Use the Insert menu to add one.", viewport)
        empty_label.setProperty("cellPart", "empty-state")
        empty_label.setWordWrap(True)
        empty_label.hide()
        self._empty_state_label = empty_label
        list_layout.addWidget(empty_label)

        spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self._cell_list_spacer = spacer
        list_layout.addItem(spacer)

        layout.addWidget(cell_list)

        self.setCentralWidget(central)
        self._show_empty_state()

    def _clear_cell_rows(self) -> None:
        if not self._cell_rows:
            return
        if not self._cell_list_layout:
            self._cell_rows.clear()
            return
        for row in self._cell_rows:
            self._cell_list_layout.removeWidget(row)
            row.deleteLater()
        self._cell_rows.clear()

    def _show_empty_state(self) -> None:
        if self._empty_state_label:
            self._empty_state_label.show()
        self._dynamic_toolbar.set_cell_type(None)
        self._update_cell_action_states()

    def _hide_empty_state(self) -> None:
        if self._empty_state_label:
            self._empty_state_label.hide()

    def _render_cells_for_state(self, state: NotebookState) -> None:
        if not self._cell_list_layout:
            return

        self._current_notebook_state = state
        self._clear_cell_rows()

        cells = list(state.iter_cells())
        if not cells:
            self._app_state.selected_cell_id = None
            state.active_cell_id = None
            self._show_empty_state()
            return

        available_ids = {cell.cell_id for cell in cells}
        if self._app_state.selected_cell_id not in available_ids:
            self._app_state.selected_cell_id = None

        self._hide_empty_state()

        metrics = self._current_metrics()
        row_tokens = cell_row_tokens(metrics)
        gutter_tokens = cell_gutter_tokens(metrics)

        insert_at = self._cell_list_layout.count()
        if self._cell_list_spacer:
            insert_at = max(0, insert_at - 1)

        for index, cell in enumerate(cells, start=1):
            header_text = self._format_cell_header(cell, index)
            body_text = self._format_cell_body(cell)
            row = CellRow(
                cell_id=cell.cell_id,
                index=index,
                header_text=header_text,
                body_text=body_text,
                select_callback=self._handle_cell_selected,
                gutter_callback=self._handle_gutter_clicked,
                row_tokens=row_tokens,
                gutter_tokens=gutter_tokens,
            )
            self._cell_rows.append(row)
            self._cell_list_layout.insertWidget(insert_at, row)
            insert_at += 1
            if cell.cell_id == self._app_state.selected_cell_id:
                row.set_selected(True)
            else:
                row.set_selected(False)

        state.active_cell_id = self._app_state.selected_cell_id
        self._update_cell_action_states()

    def _format_cell_header(self, cell: Cell, index: int) -> str:
        if cell.cell_type == "code":
            label = "Python"
        elif cell.cell_type == "markdown":
            label = "Markdown"
        else:
            label = cell.cell_type.title()
        return f"{index:02d} · {label} Cell"

    def _format_cell_body(self, cell: Cell) -> str:
        content = cell.content.strip()
        if not content:
            return "(empty cell)"

        first_line = content.splitlines()[0]
        if len(first_line) <= 120:
            return first_line
        return f"{first_line[:117]}..."

    def _current_state(self) -> NotebookState | None:
        if not self._notebook_manager:
            return None

        notebook_id = self._app_state.active_notebook_id
        if not notebook_id:
            return None

        if (
            self._current_notebook_state
            and self._current_notebook_state.notebook.notebook_id == notebook_id
        ):
            return self._current_notebook_state

        state = self._notebook_manager.get_state(notebook_id)
        if state:
            self._current_notebook_state = state
        return state

    def _update_cell_action_states(self) -> None:
        state = self._current_state()
        cell_id = self._app_state.selected_cell_id

        can_move_up = False
        can_move_down = False

        if state and cell_id and cell_id in state.notebook.cell_ids:
            order = list(state.notebook.cell_ids)
            index = order.index(cell_id)
            can_move_up = index > 0
            can_move_down = index < len(order) - 1

        has_selection = cell_id is not None

        if self._move_up_button:
            self._move_up_button.setEnabled(can_move_up)
        if self._move_down_button:
            self._move_down_button.setEnabled(can_move_down)
        if self._move_cell_up_action:
            self._move_cell_up_action.setEnabled(can_move_up)
        if self._move_cell_down_action:
            self._move_cell_down_action.setEnabled(can_move_down)
        if self._delete_cell_action:
            self._delete_cell_action.setEnabled(has_selection)
        if self._delete_notebook_action:
            self._delete_notebook_action.setEnabled(self._app_state.active_notebook_id is not None)

    def _move_selected_cell(self, step: int) -> None:
        state = self._current_state()
        if not state or not self._notebook_manager:
            return

        cell_id = self._app_state.selected_cell_id
        if not cell_id or cell_id not in state.notebook.cell_ids:
            return

        order = list(state.notebook.cell_ids)
        index = order.index(cell_id)
        new_index = index + step

        if new_index < 0 or new_index >= len(order):
            return

        moved = self._notebook_manager.move_cell(state.notebook.notebook_id, cell_id, new_index)
        if moved:
            self._app_state.selected_cell_id = cell_id
            state.active_cell_id = cell_id
        self._update_cell_action_states()

    def _delete_selected_cell(self) -> None:
        if not (self._cell_manager and self._notebook_manager):
            return

        notebook_id = self._app_state.active_notebook_id
        cell_id = self._app_state.selected_cell_id
        if not notebook_id or not cell_id:
            return

        state = self._current_state()
        if not state or cell_id not in state.notebook.cell_ids:
            return

        order = list(state.notebook.cell_ids)
        index = order.index(cell_id)

        next_selection: str | None = None
        if len(order) > 1:
            if index + 1 < len(order):
                next_selection = order[index + 1]
            elif index - 1 >= 0:
                next_selection = order[index - 1]

        previous_selection = self._app_state.selected_cell_id
        self._app_state.selected_cell_id = next_selection
        state.active_cell_id = next_selection

        removed = self._notebook_manager.remove_cell(notebook_id, cell_id)
        if removed:
            self._cell_manager.delete_cell(cell_id)
            # Update toolbar to reflect new selection (or lack thereof)
            if next_selection and state:
                cell = state.get_cell(next_selection)
                if cell:
                    self._dynamic_toolbar.set_cell_type(cell.cell_type)
                else:
                    self._dynamic_toolbar.set_cell_type(None)
            else:
                self._dynamic_toolbar.set_cell_type(None)
        else:
            self._app_state.selected_cell_id = previous_selection
            state.active_cell_id = previous_selection
        self._update_cell_action_states()

    def _build_statusbar(self) -> None:
        status = QStatusBar()
        status.setObjectName("MainStatusBar")
        status.showMessage("Ready")

        warning_label = QLabel("Unsaved changes")
        warning_label.setProperty("statusRole", "warning")
        status.addPermanentWidget(warning_label)

        self.setStatusBar(status)

    def _build_sidebars(self) -> None:
        # Sidebar panel should be renamed to sidebar toolbar
        metrics = self._current_metrics()
        sidebar_layout_tokens = sidebar_tokens(metrics)
        sidebar_button_tokens = button_tokens(metrics)

        notebooks_dock = self._create_sidebar_dock("NotebooksDock", "Notebooks")
        notebooks_toolbar = NotebookSidebarWidget(
            self,
            tokens=sidebar_layout_tokens,
            button_tokens=sidebar_button_tokens,
        )
        notebooks_dock.setWidget(notebooks_toolbar)
        notebooks_dock.hide()

        settings_dock = self._create_sidebar_dock("SettingsDock", "Settings")
        settings_toolbar = SettingsSidebarWidget(
            self,
            ui_font_size=self._style_preferences.ui_font_size,
            ui_font_family=self._style_preferences.ui_font_family,
            ui_font_choices=list(self._available_ui_fonts),
            min_font_size=MIN_UI_FONT_POINT_SIZE,
            max_font_size=MAX_UI_FONT_POINT_SIZE,
            step=FONT_SIZE_STEP,
            tokens=sidebar_layout_tokens,
        )
        settings_toolbar.ui_font_size_changed.connect(self._handle_ui_font_size_changed)
        settings_toolbar.ui_font_family_changed.connect(self._handle_ui_font_family_changed)
        settings_dock.setWidget(settings_toolbar)
        settings_dock.hide()

        toc_dock = self._create_sidebar_dock("TocDock", "Table of Contents")
        toc_toolbar = TocSidebarWidget(self, tokens=sidebar_layout_tokens)
        toc_dock.setWidget(toc_toolbar)
        toc_dock.hide()

        self._notebooks_dock = notebooks_dock
        self._settings_dock = settings_dock
        self._toc_dock = toc_dock
        self._notebooks_toolbar = notebooks_toolbar
        self._settings_toolbar = settings_toolbar
        self._toc_toolbar = toc_toolbar

    def _setup_core(self) -> None:
        self._data_store = DataStore()
        self._cell_manager = CellManager(self._data_store)
        self._notebook_manager = NotebookManager(self._data_store, self._cell_manager)
        self._connect_notebook_events()

    def _connect_notebook_events(self) -> None:
        if not self._notebook_manager:
            return

        events = self._notebook_manager.events
        events.notebook_created.connect(self._on_notebook_created)
        events.notebook_opened.connect(self._on_notebook_opened)
        events.notebook_renamed.connect(self._on_notebook_renamed)
        events.notebook_deleted.connect(self._on_notebook_deleted)
        events.state_updated.connect(self._on_notebook_state_updated)

    def _initialize_notebook_sidebar(self) -> None:
        if not (self._notebooks_toolbar and self._notebook_manager):
            return
        toolbar = self._notebooks_toolbar
        toolbar.add_notebook_clicked.connect(self._handle_add_notebook_clicked)
        toolbar.move_notebook_up_clicked.connect(self._handle_move_notebook_up_clicked)
        toolbar.move_notebook_down_clicked.connect(self._handle_move_notebook_down_clicked)
        toolbar.notebook_selected.connect(self._handle_notebook_selected)
        toolbar.rename_notebook_requested.connect(self._handle_notebook_rename_requested)
        toolbar.delete_notebook_requested.connect(self._handle_notebook_delete_requested)

        existing = self._notebook_manager.list_notebooks()
        toolbar.set_notebooks([(nb.notebook_id, nb.title) for nb in existing])
        if existing:
            first_id = existing[0].notebook_id
            toolbar.select_notebook(first_id)
            self._handle_notebook_selected(first_id)
        else:
            self._create_notebook()

    def _create_sidebar_dock(self, object_name: str, title: str) -> QDockWidget:
        dock = QDockWidget(title, self)
        dock.setObjectName(object_name)
        dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        # Hide the title bar by setting it to an empty widget
        dock.setTitleBarWidget(QWidget())
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)
        return dock

    def _normalize_sidebar_width(self, desired: int | None) -> int:
        width = desired or DEFAULT_SIDEBAR_WIDTH
        width = max(width, MIN_SIDEBAR_WIDTH)
        if MAX_SIDEBAR_WIDTH:
            width = min(width, MAX_SIDEBAR_WIDTH)
        return width

    def _apply_sidebar_width(self, dock: QDockWidget) -> None:
        width = self._normalize_sidebar_width(DEFAULT_SIDEBAR_WIDTH)
        try:
            self.resizeDocks([dock], [width], Qt.Orientation.Horizontal)
        except Exception:
            pass

    # ------------------------------------------------------------------
    # Notebook sidebar event handlers
    # ------------------------------------------------------------------
    def _handle_add_notebook_clicked(self) -> None:
        self._create_notebook()

    def _handle_move_notebook_up_clicked(self) -> None:
        # TODO: Persist notebook ordering once supported in the core layer.
        pass

    def _handle_move_notebook_down_clicked(self) -> None:
        # TODO: Persist notebook ordering once supported in the core layer.
        pass

    def _handle_notebook_selected(self, notebook_id: str) -> None:
        if not self._notebook_manager:
            return
        state = self._notebook_manager.open_notebook(notebook_id)
        if state:
            self._app_state.active_notebook_id = notebook_id

    def _handle_notebook_rename_requested(self, notebook_id: str, new_title: str) -> None:
        if not self._notebook_manager or not self._notebooks_toolbar:
            return

        notebook = self._notebook_manager.rename_notebook(notebook_id, new_title)
        if not notebook:
            self._notebooks_toolbar.restore_notebook_title(notebook_id)

    def _handle_notebook_delete_requested(self, notebook_id: str) -> None:
        if self._notebook_manager:
            self._notebook_manager.delete_notebook(notebook_id)

    # ------------------------------------------------------------------
    # Core notebook event callbacks
    # ------------------------------------------------------------------
    def _on_notebook_created(self, notebook: Notebook) -> None:
        if self._notebooks_toolbar:
            self._notebooks_toolbar.add_notebook(notebook.notebook_id, notebook.title, select=True)
        self._app_state.active_notebook_id = notebook.notebook_id

    def _on_notebook_opened(self, state: NotebookState) -> None:
        notebook_id = state.notebook.notebook_id
        self._app_state.active_notebook_id = notebook_id
        self._app_state.selected_cell_id = state.active_cell_id
        if self._notebooks_toolbar:
            self._notebooks_toolbar.select_notebook(notebook_id)
        self._render_cells_for_state(state)

        if state.active_cell_id:
            cell = state.get_cell(state.active_cell_id)
            if cell:
                self._dynamic_toolbar.set_cell_type(cell.cell_type)
            else:
                self._dynamic_toolbar.set_cell_type(None)
        else:
            self._dynamic_toolbar.set_cell_type(None)

    def _on_notebook_renamed(self, notebook: Notebook) -> None:
        if self._notebooks_toolbar:
            self._notebooks_toolbar.update_notebook_title(notebook.notebook_id, notebook.title)

    def _on_notebook_deleted(self, notebook_id: str) -> None:
        if not self._notebooks_toolbar:
            return

        next_id = self._notebooks_toolbar.remove_notebook(notebook_id)
        if next_id:
            self._notebooks_toolbar.select_notebook(next_id)
        else:
            self._app_state.active_notebook_id = None
            self._app_state.selected_cell_id = None
            self._current_notebook_state = None
            self._clear_cell_rows()
            self._show_empty_state()
            self._update_cell_action_states()

    def _on_notebook_state_updated(self, state: NotebookState) -> None:
        if state.notebook.notebook_id != self._app_state.active_notebook_id:
            return
        self._render_cells_for_state(state)

    # ------------------------------------------------------------------
    # Notebook helpers
    # ------------------------------------------------------------------
    def _create_notebook(self) -> Notebook | None:
        if not self._notebook_manager:
            return None
        title = self._generate_notebook_title()
        return self._notebook_manager.create_notebook(title)

    def _generate_notebook_title(self) -> str:
        if not self._notebook_manager:
            return "Untitled Notebook"

        existing_titles = {nb.title for nb in self._notebook_manager.list_notebooks()}
        base = "Untitled Notebook"
        if base not in existing_titles:
            return base

        suffix = 2
        while True:
            candidate = f"{base} {suffix}"
            if candidate not in existing_titles:
                return candidate
            suffix += 1

    def _toggle_notebooks_sidebar(self, checked: bool) -> None:
        if not self._notebooks_dock:
            return
        if checked:
            if self._settings_button:
                self._settings_button.setChecked(False)
            if self._toc_button:
                self._toc_button.setChecked(False)
            self._notebooks_dock.show()
            self._apply_sidebar_width(self._notebooks_dock)
        else:
            self._notebooks_dock.hide()

    def _toggle_settings_sidebar(self, checked: bool) -> None:
        if not self._settings_dock:
            return
        if checked:
            if self._notebooks_button:
                self._notebooks_button.setChecked(False)
            if self._toc_button:
                self._toc_button.setChecked(False)
            self._settings_dock.show()
            self._apply_sidebar_width(self._settings_dock)
        else:
            self._settings_dock.hide()

    def _toggle_toc_sidebar(self, checked: bool) -> None:
        if not self._toc_dock:
            return
        if checked:
            if self._notebooks_button:
                self._notebooks_button.setChecked(False)
            if self._settings_button:
                self._settings_button.setChecked(False)
            self._toc_dock.show()
            self._apply_sidebar_width(self._toc_dock)
        else:
            self._toc_dock.hide()

    def _current_metrics(self) -> Metrics:
        return self._style_preferences.build_metrics()

    def _apply_current_style(self) -> None:
        apply_global_style(self._app, mode=self._mode, metrics=self._current_metrics())
        for row in self._cell_rows:
            row.set_selected(row.is_selected())

    def _switch_theme(self, mode: ThemeMode) -> None:
        if mode == self._mode:
            return
        self._mode = mode
        self._apply_current_style()

    def _handle_cell_selected(self, row: CellRow) -> None:
        for candidate in self._cell_rows:
            candidate.set_selected(candidate is row)
        self._app_state.selected_cell_id = row.cell_id
        state = self._current_state()
        if state:
            state.active_cell_id = row.cell_id
            cell = state.get_cell(row.cell_id)
            if cell:
                self._dynamic_toolbar.set_cell_type(cell.cell_type)
            else:
                self._dynamic_toolbar.set_cell_type(None)
        else:
            self._dynamic_toolbar.set_cell_type(None)
        self._update_cell_action_states()

    def _handle_gutter_clicked(self, row: CellRow) -> None:
        if row.is_selected():
            row.set_selected(False)
            self._app_state.selected_cell_id = None
            state = self._current_state()
            if state:
                state.active_cell_id = None
            self._dynamic_toolbar.set_cell_type(None)
            self._update_cell_action_states()
        else:
            self._handle_cell_selected(row)

    def _handle_ui_font_size_changed(self, point_size: int) -> None:
        clamped_size = clamp_ui_font_point_size(point_size)
        if clamped_size == self._style_preferences.ui_font_size:
            return
        self._style_preferences = replace(self._style_preferences, ui_font_size=clamped_size)
        self._apply_current_style()

    def _handle_ui_font_family_changed(self, font_family: str) -> None:
        normalized_family = font_family.strip()
        if not normalized_family:
            return
        if normalized_family not in self._available_ui_fonts:
            return
        if normalized_family == self._style_preferences.ui_font_family:
            return
        self._style_preferences = replace(
            self._style_preferences,
            ui_font_family=normalized_family,
        )
        self._apply_current_style()

    def _create_and_insert_cell(self, cell_type: CellType) -> None:
        if not (self._cell_manager and self._notebook_manager):
            return

        notebook_id = self._app_state.active_notebook_id
        if not notebook_id:
            notebook = self._create_notebook()
            if not notebook:
                return
            notebook_id = notebook.notebook_id
            self._app_state.active_notebook_id = notebook_id

        default_content = ""
        cell = self._cell_manager.create_cell(cell_type, content=default_content)
        self._app_state.selected_cell_id = cell.cell_id
        state = self._notebook_manager.add_cell(notebook_id, cell)
        if state:
            self._app_state.active_notebook_id = notebook_id
            state.active_cell_id = cell.cell_id

    def _on_insert_markdown_cell(self, checked: bool | None = None) -> None:
        self._create_and_insert_cell("markdown")

    def _on_insert_python_cell(self, checked: bool | None = None) -> None:
        self._create_and_insert_cell("code")

    def _on_move_cell_up_clicked(self, checked: bool | None = None) -> None:
        self._move_selected_cell(-1)

    def _on_move_cell_down_clicked(self, checked: bool | None = None) -> None:
        self._move_selected_cell(1)

    def _on_delete_cell_triggered(self, checked: bool | None = None) -> None:
        self._delete_selected_cell()

    def _on_delete_notebook_triggered(self, checked: bool | None = None) -> None:
        notebook_id = self._app_state.active_notebook_id
        if notebook_id:
            self._handle_notebook_delete_requested(notebook_id)

    def _on_run_code(self) -> None:
        self._dynamic_toolbar.set_code_running(True)
        # TODO: Implement actual execution logic
        print("Run code requested")

    def _on_stop_code(self) -> None:
        self._dynamic_toolbar.set_code_running(False)
        # TODO: Implement actual stop logic
        print("Stop code requested")

    def _on_preview_toggled(self, checked: bool) -> None:
        # TODO: Implement actual preview logic
        print(f"Preview toggled: {checked}")


__all__ = ["LunaQtWindow"]
