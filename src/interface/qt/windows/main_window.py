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
from core import CellManager, DataStore, ExecutionManager, NotebookManager
from core.models import Cell, CellType, Notebook, NotebookState
from interface.qt.sidebars import NotebookSidebarWidget, SettingsSidebarWidget, TocSidebarWidget
from interface.qt.styling import apply_global_style
from interface.qt.styling.theme import Metrics, StylePreferences, ThemeMode
from shared.constants import get_matplotlib_style
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
    CellListWidget,
    DynamicToolbar,
    PythonEditor,
    SidebarToggleButton,
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
        cell_type: str,
        index: int,
        header_text: str,
        body_text: str,
        select_callback,
        gutter_callback,
        run_callback,
        content_changed_callback,
        row_tokens: CellRowTokens,
        gutter_tokens: CellGutterTokens,
        is_dark_mode: bool = False,
    ) -> None:
        super().__init__()
        self.setProperty("cellType", "row")
        self.setFrameStyle(QFrame.NoFrame)
        self._select_callback = select_callback
        self._gutter_callback = gutter_callback
        self._run_callback = run_callback
        self._content_changed_callback = content_changed_callback
        self._cell_id = cell_id
        self._cell_type = cell_type
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

        # Execution count label (for code cells)
        self._exec_count_label = QLabel("", self._cell_container)
        self._exec_count_label.setProperty("cellPart", "execCount")
        self._exec_count_label.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self._exec_count_label.setVisible(False)
        self._cell_container.add_content_widget(self._exec_count_label)

        header = QLabel(header_text, self._cell_container)
        header.setProperty("cellPart", "header")
        header.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        header.setVisible(False)  # Hide the header text
        self._cell_container.add_content_widget(header)
        self._header_label = header

        # Use PythonEditor for code cells, QLabel for others
        self._editor = None
        self._body_label = None
        
        if cell_type == "code":
            self._editor = PythonEditor(self._cell_container, is_dark_mode=is_dark_mode)
            self._editor.setPlainText(body_text)
            self._editor.setProperty("cellPart", "editor")
            # Wire up signals
            self._editor.textChanged.connect(self._on_editor_text_changed)
            self._editor.execute_requested.connect(self._on_editor_execute_requested)
            self._editor.focus_changed.connect(self._on_editor_focus_changed)
            self._cell_container.add_content_widget(self._editor)
        else:
            body = QLabel(body_text, self._cell_container)
            body.setProperty("cellPart", "body")
            body.setWordWrap(True)
            body.setAttribute(Qt.WA_TransparentForMouseEvents, True)
            self._cell_container.add_content_widget(body)
            self._body_label = body
        
        # Output area (stdout/stderr)
        from PySide6.QtWidgets import QPlainTextEdit
        self._output_area = QPlainTextEdit(self._cell_container)
        self._output_area.setProperty("cellPart", "output")
        self._output_area.setReadOnly(True)
        self._output_area.setVisible(False)
        self._output_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._output_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self._output_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        self._cell_container.add_content_widget(self._output_area)
        
        # Plot display area
        self._plot_label = QLabel(self._cell_container)
        self._plot_label.setProperty("cellPart", "plot")
        self._plot_label.setVisible(False)
        self._plot_label.setScaledContents(False)
        self._plot_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        self._cell_container.add_content_widget(self._plot_label)

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
        if self._editor:
            self._editor.setPlainText(body_text)
        elif self._body_label:
            self._body_label.setText(body_text)
    
    def _on_editor_text_changed(self) -> None:
        """Handle text changes in the editor."""
        if self._editor:
            new_content = self._editor.toPlainText()
            self._content_changed_callback(self._cell_id, new_content)
    
    def _on_editor_execute_requested(self) -> None:
        """Handle Shift+Enter in editor."""
        self._run_callback(self)
    
    def _on_editor_focus_changed(self, has_focus: bool) -> None:
        """Handle editor focus changes."""
        if has_focus:
            self._select_callback(self)
    
    def set_execution_count(self, count: int | None) -> None:
        """Update the execution count display."""
        if count is None:
            self._exec_count_label.setText("")
            self._exec_count_label.setVisible(False)
        else:
            self._exec_count_label.setText(f"[{count}]")
            self._exec_count_label.setVisible(True)
    
    def set_output(self, stdout: str, stderr: str, error: str | None) -> None:
        """Display execution output."""
        output_text = ""
        if stdout:
            output_text += stdout
        if stderr:
            if output_text:
                output_text += "\n"
            output_text += stderr
        if error:
            if output_text:
                output_text += "\n"
            output_text += f"Error:\n{error}"
        
        if output_text:
            self._output_area.setPlainText(output_text)
            self._output_area.setVisible(True)
            
            # Auto-adjust height based on line count (like OLD_LUNA_QT and PythonEditor)
            doc = self._output_area.document()
            block_count = max(1, doc.blockCount())
            line_height = self._output_area.fontMetrics().lineSpacing()
            doc_height = line_height * block_count
            
            # Add margins, frame, and document margin
            margins = self._output_area.contentsMargins()
            frame_width = self._output_area.frameWidth() * 2
            doc_margin = int(doc.documentMargin() * 2)
            padding = margins.top() + margins.bottom() + frame_width + doc_margin + 8
            
            total_height = int(doc_height + padding)
            
            # Set minimum height
            min_height = line_height * 2 + padding
            total_height = max(total_height, min_height, 40)
            
            self._output_area.setFixedHeight(total_height)
            self._output_area.updateGeometry()
            
            # Force parent container to update layout
            if self._cell_container:
                self._cell_container.updateGeometry()
        else:
            self._output_area.setPlainText("")
            self._output_area.setVisible(False)
    
    def set_plot(self, image_bytes: bytes | None) -> None:
        """Display a plot from PNG bytes."""
        if not image_bytes:
            self._plot_label.setVisible(False)
            self._plot_label.clear()
            return
        
        from PySide6.QtGui import QPixmap
        pixmap = QPixmap()
        if pixmap.loadFromData(image_bytes):
            # Scale to reasonable size while maintaining aspect ratio
            max_width = 600
            if pixmap.width() > max_width:
                pixmap = pixmap.scaledToWidth(max_width, Qt.TransformationMode.SmoothTransformation)
            self._plot_label.setPixmap(pixmap)
            self._plot_label.setVisible(True)
        else:
            self._plot_label.setVisible(False)
    
    def clear_output(self) -> None:
        """Clear all execution output and plots."""
        self._output_area.setPlainText("")
        self._output_area.setVisible(False)
        self._plot_label.clear()
        self._plot_label.setVisible(False)
    
    def get_plot_pixmap(self) -> Any | None:
        """Get the current plot pixmap for export."""
        if self._plot_label.pixmap() and not self._plot_label.pixmap().isNull():
            return self._plot_label.pixmap()
        return None

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
        self._execution_manager: ExecutionManager | None = None

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
    
    def keyPressEvent(self, event) -> None:
        """Handle keyboard shortcuts."""
        from PySide6.QtCore import Qt
        from PySide6.QtGui import QKeySequence
        
        # Shift+Enter: Execute current cell
        if event.key() == Qt.Key.Key_Return and event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
            state = self._current_state()
            if state and state.active_cell_id:
                cell = state.get_cell(state.active_cell_id)
                if cell and cell.cell_type == "python":
                    self._on_run_code()
                    event.accept()
                    return
        
        super().keyPressEvent(event)
    
    def __del__(self) -> None:
        """Cleanup execution workers on destruction."""
        if hasattr(self, '_execution_manager') and self._execution_manager:
            self._execution_manager.shutdown()

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
        
        edit_menu.addSeparator()
        
        clear_output_action = QAction("Clear Cell Output", self)
        clear_output_action.triggered.connect(self._on_clear_output_triggered)
        edit_menu.addAction(clear_output_action)
        self._clear_output_action = clear_output_action
        
        export_plot_action = QAction("Export Plot...", self)
        export_plot_action.triggered.connect(self._on_export_plot_triggered)
        edit_menu.addAction(export_plot_action)
        self._export_plot_action = export_plot_action

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
        
        # Preserve outputs and editor content before clearing
        preserved_data = {}
        for row in self._cell_rows:
            preserved_data[row.cell_id] = {
                'has_output': row._output_area.isVisible() if hasattr(row, '_output_area') else False,
                'output_text': row._output_area.toPlainText() if hasattr(row, '_output_area') else "",
                'has_plot': row._plot_label.isVisible() if hasattr(row, '_plot_label') else False,
                'plot_pixmap': row._plot_label.pixmap() if hasattr(row, '_plot_label') else None,
                'editor_content': row._editor.toPlainText() if row._editor else None,
            }
        
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
                cell_type=cell.cell_type,
                run_callback=self._on_run_code,
                content_changed_callback=self._on_cell_content_changed,
                is_dark_mode=(self._mode == ThemeMode.DARK),
            )
            
            # Set execution count for code cells
            if cell.cell_type == "code" and cell.execution_count is not None:
                row.set_execution_count(cell.execution_count)
            
            # Restore outputs for code cells
            if cell.cell_type == "code" and cell.outputs:
                stdout_parts = []
                stderr_parts = []
                figures = []
                
                for output in cell.outputs:
                    output_type = output.get("output_type", "")
                    if output_type == "stream":
                        stream_name = output.get("name", "stdout")
                        text = output.get("text", "")
                        if stream_name == "stdout":
                            stdout_parts.append(text)
                        elif stream_name == "stderr":
                            stderr_parts.append(text)
                    elif output_type == "display_data":
                        data = output.get("data", {})
                        if "image/png" in data:
                            import base64
                            png_base64 = data["image/png"]
                            figures.append(base64.b64decode(png_base64))
                
                # Set output text
                stdout = "".join(stdout_parts)
                stderr = "".join(stderr_parts)
                if stdout or stderr:
                    row.set_output(stdout, stderr, None)
                
                # Set first plot
                if figures:
                    row.set_plot(figures[0])
            
            # Restore preserved in-memory outputs (overrides database)
            if cell.cell_id in preserved_data:
                data = preserved_data[cell.cell_id]
                # Restore editor content if it was edited
                if data['editor_content'] is not None and row._editor:
                    row._editor.setPlainText(data['editor_content'])
                # Restore output if it was visible
                if data['has_output']:
                    row._output_area.setPlainText(data['output_text'])
                    row._output_area.setVisible(True)
                # Restore plot if it was visible
                if data['has_plot'] and data['plot_pixmap']:
                    row._plot_label.setPixmap(data['plot_pixmap'])
                    row._plot_label.setVisible(True)
            
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
        
        # For code cells, return full content (editors need all lines)
        if cell.cell_type == "code":
            return cell.content
        
        # For other cell types, show abbreviated first line
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
        
        # Enable clear/export actions only if cell has output/plot
        has_output_or_plot = False
        has_plot = False
        if has_selection and state:
            cell_row = self._find_cell_row(cell_id)
            if cell_row:
                has_output_or_plot = bool(
                    (cell_row._output_area.isVisible() and cell_row._output_area.toPlainText()) or
                    cell_row.get_plot_pixmap() is not None
                )
                has_plot = cell_row.get_plot_pixmap() is not None
        
        if hasattr(self, '_clear_output_action') and self._clear_output_action:
            self._clear_output_action.setEnabled(has_output_or_plot)
        if hasattr(self, '_export_plot_action') and self._export_plot_action:
            self._export_plot_action.setEnabled(has_plot)

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
        
        # Initialize execution manager
        self._execution_manager = ExecutionManager(parent=self)
        self._execution_manager.cell_started.connect(self._on_cell_execution_started)
        self._execution_manager.cell_finished.connect(self._on_cell_execution_finished)
        self._execution_manager.cell_failed.connect(self._on_cell_execution_failed)
        
        # Set initial matplotlib style based on theme
        is_dark = self._mode == ThemeMode.DARK
        self._execution_manager.set_plot_style(get_matplotlib_style(is_dark))
        
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
        """Move the selected notebook up in the sidebar list."""
        if not self._notebooks_toolbar:
            return
        
        # Get current selection
        current_row = self._notebooks_toolbar._list.currentRow()
        if current_row <= 0:
            return  # Already at top or no selection
        
        # Get the item data
        item = self._notebooks_toolbar._list.takeItem(current_row)
        
        # Reinsert at previous position
        self._notebooks_toolbar._list.insertItem(current_row - 1, item)
        self._notebooks_toolbar._list.setCurrentRow(current_row - 1)
        
        # Update button states
        self._notebooks_toolbar._update_move_buttons()

    def _handle_move_notebook_down_clicked(self) -> None:
        """Move the selected notebook down in the sidebar list."""
        if not self._notebooks_toolbar:
            return
        
        # Get current selection
        current_row = self._notebooks_toolbar._list.currentRow()
        if current_row < 0 or current_row >= self._notebooks_toolbar._list.count() - 1:
            return  # Already at bottom or no selection
        
        # Get the item data
        item = self._notebooks_toolbar._list.takeItem(current_row)
        
        # Reinsert at next position
        self._notebooks_toolbar._list.insertItem(current_row + 1, item)
        self._notebooks_toolbar._list.setCurrentRow(current_row + 1)
        
        # Update button states
        self._notebooks_toolbar._update_move_buttons()

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
        
        # Shutdown worker for previous notebook when switching
        if self._app_state.active_notebook_id and self._app_state.active_notebook_id != notebook_id:
            if self._execution_manager:
                self._execution_manager.shutdown_notebook(self._app_state.active_notebook_id)
        
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
        # Shutdown execution worker for this notebook
        if self._execution_manager:
            self._execution_manager.shutdown_notebook(notebook_id)
        
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
        
        # Update matplotlib style for execution manager
        if self._execution_manager:
            is_dark = self._mode == ThemeMode.DARK
            self._execution_manager.set_plot_style(get_matplotlib_style(is_dark))
        
        # Update matplotlib style for execution manager
        if self._execution_manager:
            is_dark = self._mode == ThemeMode.DARK
            self._execution_manager.set_plot_style(get_matplotlib_style(is_dark))

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
    
    def _on_clear_output_triggered(self) -> None:
        """Clear output for the selected cell."""
        state = self._current_state()
        if not state or not state.active_cell_id:
            return
        
        # Find and clear the cell row
        cell_row = self._find_cell_row(state.active_cell_id)
        if cell_row:
            cell_row.clear_output()
            print(f"[DEBUG] Cleared output for cell {state.active_cell_id}")
    
    def _on_export_plot_triggered(self) -> None:
        """Export the current cell's plot to a file."""
        from PySide6.QtWidgets import QFileDialog
        
        state = self._current_state()
        if not state or not state.active_cell_id:
            return
        
        # Find the cell row and get its plot
        cell_row = self._find_cell_row(state.active_cell_id)
        if not cell_row:
            return
        
        pixmap = cell_row.get_plot_pixmap()
        if not pixmap:
            print("[DEBUG] No plot to export")
            return
        
        # Open save dialog
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Plot",
            "",
            "PNG Image (*.png);;JPEG Image (*.jpg *.jpeg);;All Files (*)"
        )
        
        if file_path:
            # Save the pixmap
            if pixmap.save(file_path):
                print(f"[DEBUG] Plot exported to {file_path}")
            else:
                print(f"[DEBUG] Failed to export plot to {file_path}")

    def _on_run_code(self, cell_row: CellRow | None = None) -> None:
        """Handle Run button click or Shift+Enter in editor.
        
        Args:
            cell_row: The CellRow that triggered the run (for Shift+Enter)
        """
        self._dynamic_toolbar.set_code_running(True)
        
        if not self._execution_manager or not self._cell_manager:
            print("[DEBUG] No execution manager or cell manager")
            return
            
        state = self._current_state()
        if not state or not state.active_cell_id:
            print("[DEBUG] No active cell")
            return
            
        cell = state.get_cell(state.active_cell_id)
        if not cell or cell.cell_type != "code":
            print("[DEBUG] Not a code cell")
            return
        
        # Get current content from the editor (if available)
        # DON'T save to database - just get the text to run
        code_to_run = cell.content
        if cell_row and cell_row._editor:
            code_to_run = cell_row._editor.toPlainText()
        elif cell_row is None:
            # Find the active cell row to get editor content
            for row in self._cell_rows:
                if row.cell_id == state.active_cell_id and row._editor:
                    code_to_run = row._editor.toPlainText()
                    break
            
        # Get or increment execution count
        execution_count = (cell.execution_count or 0) + 1
        
        # Run the cell
        self._execution_manager.run_cell(
            notebook_id=state.notebook.notebook_id,
            cell_id=cell.cell_id,
            code=code_to_run,
            execution_count=execution_count,
        )
        
        print(f"[DEBUG] Executing cell {cell.cell_id} (count: {execution_count})")

    def _on_cell_content_changed(self, cell_id: str, new_content: str) -> None:
        """Handle cell content changes from the editor.
        
        Saves content on every keystroke, like OLD_LUNA_QT.
        We disconnect state_updated to prevent rebuilds during save.
        """
        if not self._cell_manager or not self._notebook_manager:
            return
        
        # Disconnect state_updated to prevent rebuilds
        try:
            self._notebook_manager.events.state_updated.disconnect(self._on_notebook_state_updated)
        except:
            pass
        
        # Save the content
        try:
            self._cell_manager.update_cell(cell_id, content=new_content)
        except Exception as e:
            print(f"[DEBUG] Failed to save cell content: {e}")
        
        # Reconnect state_updated
        if self._notebook_manager:
            try:
                self._notebook_manager.events.state_updated.connect(self._on_notebook_state_updated)
            except:
                pass

    def _on_stop_code(self) -> None:
        """Handle Stop button click."""
        self._dynamic_toolbar.set_code_running(False)
        
        if not self._execution_manager:
            return
        
        state = self._current_state()
        if not state:
            return
        
        # Interrupt execution by restarting the worker
        interrupted = self._execution_manager.interrupt_notebook(state.notebook.notebook_id)
        if interrupted:
            print(f"[DEBUG] Interrupted execution for notebook {state.notebook.notebook_id}")
        else:
            print("[DEBUG] No active execution to stop")

    def _on_preview_toggled(self, checked: bool) -> None:
        """Handle Preview toggle."""
        # TODO: Implement actual preview logic
        print(f"Preview toggled: {checked}")
    
    def _on_cell_execution_started(self, request) -> None:
        """Handle cell execution started signal."""
        print(f"[DEBUG] Cell execution started: {request.cell_id}")
        # TODO: Update UI to show running state
        
    def _on_cell_execution_finished(self, result) -> None:
        """Handle cell execution finished signal.
        
        Save outputs to database so they persist across notebook switches.
        """
        self._dynamic_toolbar.set_code_running(False)
        print(f"[DEBUG] Cell execution finished: {result.cell_id}")
        print(f"[DEBUG] Stdout: {result.stdout}")
        print(f"[DEBUG] Stderr: {result.stderr}")
        print(f"[DEBUG] Figures: {len(result.figures)}")
        
        # Build outputs in Jupyter notebook format
        outputs = []
        if result.stdout:
            outputs.append({
                "output_type": "stream",
                "name": "stdout",
                "text": result.stdout
            })
        if result.stderr:
            outputs.append({
                "output_type": "stream",
                "name": "stderr",
                "text": result.stderr
            })
        if result.figures:
            import base64
            for fig_bytes in result.figures:
                outputs.append({
                    "output_type": "display_data",
                    "data": {
                        "image/png": base64.b64encode(fig_bytes).decode('utf-8')
                    },
                    "metadata": {}
                })
        
        # Save outputs to database (disconnect state_updated to prevent rebuild)
        if self._cell_manager and self._notebook_manager:
            try:
                self._notebook_manager.events.state_updated.disconnect(self._on_notebook_state_updated)
            except:
                pass
            
            try:
                self._cell_manager.update_cell(
                    result.cell_id,
                    outputs=outputs,
                    execution_count=result.execution_count
                )
                print(f"[DEBUG] Saved {len(outputs)} outputs to database for cell {result.cell_id}")
            except Exception as e:
                print(f"[DEBUG] Failed to save outputs: {e}")
            
            # Reconnect state_updated
            if self._notebook_manager:
                try:
                    self._notebook_manager.events.state_updated.connect(self._on_notebook_state_updated)
                except:
                    pass
        
        # Update UI
        cell_row = self._find_cell_row(result.cell_id)
        if cell_row:
            print(f"[DEBUG] Found cell row for {result.cell_id}")
            # Update execution count
            cell_row.set_execution_count(result.execution_count)
            
            # Display output
            print(f"[DEBUG] Setting output, visible={bool(result.stdout or result.stderr)}")
            cell_row.set_output(result.stdout, result.stderr, None)
            
            # Display first plot if available
            if result.figures:
                cell_row.set_plot(result.figures[0])
            else:
                cell_row.set_plot(None)
        else:
            print(f"[DEBUG] Could not find cell row for {result.cell_id}")
        
    def _on_cell_execution_failed(self, result) -> None:
        """Handle cell execution failed signal."""
        self._dynamic_toolbar.set_code_running(False)
        print(f"[DEBUG] Cell execution failed: {result.cell_id}")
        print(f"[DEBUG] Error: {result.error}")
        
        # Find the cell row and display error
        cell_row = self._find_cell_row(result.cell_id)
        if cell_row:
            cell_row.set_execution_count(result.execution_count)
            cell_row.set_output(result.stdout, result.stderr, result.error)
            
            # Display plots even if there was an error
            if result.figures:
                cell_row.set_plot(result.figures[0])
            else:
                cell_row.set_plot(None)
    
    def _find_cell_row(self, cell_id: str) -> CellRow | None:
        """Find a CellRow widget by cell ID."""
        for row in self._cell_rows:
            if row.cell_id == cell_id:
                return row
        return None


__all__ = ["LunaQtWindow"]
