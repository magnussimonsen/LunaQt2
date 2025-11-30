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
    QStatusBar,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from interface.qt.sidebars import NotebookSidebarWidget, SettingsSidebarWidget
from interface.qt.styling import apply_global_style
from interface.qt.styling.theme import Metrics, StylePreferences, ThemeMode
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
        index: int,
        header_text: str,
        body_text: str,
        select_callback,
        gutter_callback,
    ) -> None:
        super().__init__()
        self.setProperty("cellType", "row")
        self.setFrameStyle(QFrame.NoFrame)
        self._select_callback = select_callback
        self._gutter_callback = gutter_callback
        self._selected = False

        row_layout = QHBoxLayout(self)
        row_layout.setContentsMargins(2, 2, 2, 2)
        row_layout.setSpacing(5)

        self._gutter = QWidget()
        self._gutter.setProperty("cellType", "gutter")
        gutter_layout = QVBoxLayout(self._gutter)
        gutter_layout.setContentsMargins(5, 0, 5, 0)
        gutter_layout.setSpacing(0)

        gutter_label = QLabel(f"{index:02d}")
        gutter_label.setProperty("cellRole", "line-number")
        gutter_label.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        gutter_layout.addStretch()
        gutter_layout.addWidget(gutter_label)
        gutter_layout.addStretch()

        self._cell_frame = QFrame()
        self._cell_frame.setProperty("cellType", "container")
        cell_layout = QVBoxLayout(self._cell_frame)
        cell_layout.setContentsMargins(0, 0, 0, 0)
        cell_layout.setSpacing(5)

        header = QLabel(header_text)
        header.setProperty("cellPart", "header")
        header.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        cell_layout.addWidget(header)

        body = QLabel(body_text)
        body.setProperty("cellPart", "body")
        body.setWordWrap(True)
        body.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        cell_layout.addWidget(body)

        row_layout.addWidget(self._gutter)
        row_layout.addWidget(self._cell_frame, 1)

        self._gutter.installEventFilter(self)
        self._cell_frame.installEventFilter(self)

    def eventFilter(self, watched, event):
        if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
            if watched is self._cell_frame:
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
        self._apply_state(self._cell_frame, state_value)
        self._apply_state(self._gutter, state_value)

    def is_selected(self) -> bool:
        return self._selected

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
        self._notebooks_panel: NotebookSidebarWidget | None = None
        self._settings_panel: SettingsSidebarWidget | None = None
        self._notebooks_dock: QDockWidget | None = None
        self._settings_dock: QDockWidget | None = None
        self._notebooks_button: QPushButton | None = None
        self._settings_button: QPushButton | None = None
        self._move_up_button: QPushButton | None = None
        self._move_down_button: QPushButton | None = None

        self.setWindowTitle("LunaQt2")
        self.resize(900, 600)

        self._build_menubar()
        self._build_toolbar()
        self._build_central()
        self._build_statusbar()
        self._build_sidebars()
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
        edit_menu.addAction("Move Cell Up")
        edit_menu.addAction("Move Cell Down")
        edit_menu.addSeparator()
        edit_menu.addAction("Delete Cell")
        edit_menu.addAction("Delete Notebook")

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

    def _install_sidebar_corner_buttons(self, menu_bar) -> None:
        corner = QWidget(menu_bar)
        corner.setProperty("widgetRole", "menubar-corner")
        layout = QHBoxLayout(corner)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        if self._move_up_button and self._move_down_button:
            layout.addWidget(self._move_up_button)
            layout.addWidget(self._move_down_button)

        notebooks_button = QPushButton("Notebooks", corner)
        notebooks_button.setCheckable(True)
        notebooks_button.setProperty("btnType", "menubar")
        notebooks_button.toggled.connect(
            lambda checked: (
                self._toggle_notebooks_sidebar(checked),
                self._refresh_button_style(notebooks_button),
            )
        )
        layout.addWidget(notebooks_button)

        settings_button = QPushButton("Settings", corner)
        settings_button.setCheckable(True)
        settings_button.setProperty("btnType", "menubar")
        settings_button.toggled.connect(
            lambda checked: (
                self._toggle_settings_sidebar(checked),
                self._refresh_button_style(settings_button),
            )
        )
        layout.addWidget(settings_button)

        layout.addStretch(1)
        menu_bar.setCornerWidget(corner, Qt.Corner.TopRightCorner)

        self._notebooks_button = notebooks_button
        self._settings_button = settings_button

    def _build_toolbar(self) -> None:
        toolbar = QToolBar("Main Toolbar")
        toolbar.setObjectName("PrimaryToolBar")
        toolbar.setMovable(False)
        primary_btn = QPushButton("Primary")
        primary_btn.setProperty("btnType", "primary")

        toolbar_btn = QPushButton("Toolbar")
        toolbar_btn.setProperty("btnType", "toolbar")

        warn_btn = QPushButton("Warn")
        warn_btn.setProperty("btnType", "warning")

        toolbar.addWidget(primary_btn)
        toolbar.addWidget(toolbar_btn)
        toolbar.addWidget(warn_btn)

        self.addToolBar(toolbar)

    def _build_central(self) -> None:
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        cell_list = QWidget()
        cell_list.setProperty("cellType", "list")
        list_layout = QVBoxLayout(cell_list)
        list_layout.setContentsMargins(5, 5, 5, 5)
        list_layout.setSpacing(0)

        sample_cells = [
            (
                "Notebook Cell",
                "Cells use the container styling, letting you compose editors, tables, or any widget inside.",
            ),
            (
                "Selection Support",
                "Click the body to focus a cell. Click the gutter again to clear selection and reset the border.",
            ),
            (
                "Custom Content",
                "Swap these labels for your own widgets; LunaQt2 just showcases layout and styling hooks.",
            ),
        ]

        for index, (header_text, body_text) in enumerate(sample_cells, start=1):
            row = CellRow(
                index=index,
                header_text=header_text,
                body_text=body_text,
                select_callback=self._handle_cell_selected,
                gutter_callback=self._handle_gutter_clicked,
            )
            self._cell_rows.append(row)
            list_layout.addWidget(row)

        list_layout.addStretch()
        layout.addWidget(cell_list)
        layout.addStretch()

        self.setCentralWidget(central)

    def _build_statusbar(self) -> None:
        status = QStatusBar()
        status.setObjectName("MainStatusBar")
        status.showMessage("Ready")

        warning_label = QLabel("Unsaved changes")
        warning_label.setProperty("statusRole", "warning")
        status.addPermanentWidget(warning_label)

        self.setStatusBar(status)

    def _build_sidebars(self) -> None:
        notebooks_dock = self._create_sidebar_dock("NotebooksDock", "Notebooks")
        notebooks_panel = NotebookSidebarWidget(self)
        notebooks_dock.setWidget(notebooks_panel)
        notebooks_dock.hide()

        settings_dock = self._create_sidebar_dock("SettingsDock", "Settings")
        settings_panel = SettingsSidebarWidget(
            self,
            ui_font_size=self._style_preferences.ui_font_size,
            ui_font_family=self._style_preferences.ui_font_family,
            ui_font_choices=list(self._available_ui_fonts),
            min_font_size=MIN_UI_FONT_POINT_SIZE,
            max_font_size=MAX_UI_FONT_POINT_SIZE,
            step=FONT_SIZE_STEP,
        )
        settings_panel.ui_font_size_changed.connect(self._handle_ui_font_size_changed)
        settings_panel.ui_font_family_changed.connect(self._handle_ui_font_family_changed)
        settings_dock.setWidget(settings_panel)
        settings_dock.hide()

        self._notebooks_dock = notebooks_dock
        self._settings_dock = settings_dock
        self._notebooks_panel = notebooks_panel
        self._settings_panel = settings_panel

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

    def _refresh_button_style(self, button: QPushButton) -> None:
        button.style().unpolish(button)
        button.style().polish(button)
        button.update()

    def _toggle_notebooks_sidebar(self, checked: bool) -> None:
        if not self._notebooks_dock:
            return
        if checked:
            if self._settings_button:
                self._settings_button.setChecked(False)
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
            self._settings_dock.show()
            self._apply_sidebar_width(self._settings_dock)
        else:
            self._settings_dock.hide()

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

    def _handle_gutter_clicked(self, row: CellRow) -> None:
        if row.is_selected():
            row.set_selected(False)
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

    def _on_move_cell_up_clicked(self) -> None:
        pass

    def _on_move_cell_down_clicked(self) -> None:
        pass


__all__ = ["LunaQtWindow"]
