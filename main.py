"""Quick demo entry-point to preview the styling system."""

from __future__ import annotations

import argparse
import sys
from importlib import import_module
from pathlib import Path
from typing import Any

# Ensure the local "src" directory is importable when running from the repo root.
PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
if SRC_DIR.exists() and str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

def _load_qt_widgets():  # pragma: no cover - import helper
    try:
        widgets = import_module("PySide6.QtWidgets")
        gui = import_module("PySide6.QtGui")
        core = import_module("PySide6.QtCore")
    except ModuleNotFoundError as exc:
        raise SystemExit("PySide6 must be installed to run the demo window.") from exc

    return (
        gui.QAction,
        gui.QActionGroup,
        widgets.QApplication,
        widgets.QFrame,
        widgets.QHBoxLayout,
        widgets.QLabel,
        widgets.QMainWindow,
        widgets.QPushButton,
        widgets.QStatusBar,
        widgets.QToolBar,
        widgets.QVBoxLayout,
        widgets.QWidget,
        core.QEvent,
        core.Qt,
    )


def _load_style_package():  # pragma: no cover - import helper
    try:
        styling = import_module("style_loader")
        theme_mod = import_module("theme")
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "Unable to import 'style_loader' or 'theme'. Ensure the repo's 'src' directory is on PYTHONPATH."
        ) from exc

    return styling.apply_global_style, theme_mod.ThemeMode


def _load_constants():  # pragma: no cover - import helper
    try:
        constants = import_module("constants")
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "Unable to import 'constants'. Ensure the repo's 'src' directory is on PYTHONPATH."
        ) from exc

    return constants.DEFAULT_THEME_MODE


(QAction, QActionGroup, QApplication, QFrame, QHBoxLayout, QLabel, QMainWindow, QPushButton, QStatusBar, QToolBar, QVBoxLayout, QWidget, QEvent, Qt) = _load_qt_widgets()
apply_global_style, ThemeMode = _load_style_package()
DEFAULT_THEME_MODE = _load_constants()


class CellRow(QWidget):
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
        self._select_callback = select_callback
        self._gutter_callback = gutter_callback
        self._selected = False

        row_layout = QHBoxLayout(self)
        row_layout.setContentsMargins(0, 0, 0, 12)
        row_layout.setSpacing(8)

        self._gutter = QWidget()
        self._gutter.setProperty("cellType", "gutter")
        gutter_layout = QVBoxLayout(self._gutter)
        gutter_layout.setContentsMargins(12, 12, 12, 12)
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
        cell_layout.setContentsMargins(12, 12, 12, 12)
        cell_layout.setSpacing(8)

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

    def eventFilter(self, watched, event):  # pragma: no cover - UI behavior
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
        self._apply_state(self._cell_frame, state_value)
        self._apply_state(self._gutter, state_value)

    def is_selected(self) -> bool:
        return self._selected

    @staticmethod
    def _apply_state(widget, state):
        widget.setProperty("state", state)
        widget.style().unpolish(widget)
        widget.style().polish(widget)


class DemoWindow(QMainWindow):
    """Minimal window that lights up the different style modules."""

    def __init__(self, app: Any, mode) -> None:
        super().__init__()
        self._app = app
        self._mode = mode
        self._theme_group = QActionGroup(self)
        self._theme_group.setExclusive(True)
        self._theme_actions: dict[str, Any] = {}
        self._cell_rows: list[CellRow] = []

        self.setWindowTitle("Qt Styling Template Demo")
        self.resize(900, 600)

        self._build_menubar()
        self._build_toolbar()
        self._build_central()
        self._build_statusbar()

    def _build_menubar(self) -> None:
        menu_bar = self.menuBar()
        menu_bar.setObjectName("MainMenuBar")

        file_menu = menu_bar.addMenu("File")
        file_menu.setProperty("menuRole", "primary")
        file_menu.addAction("New")
        file_menu.addAction("Save")
        file_menu.addAction("Save As…")

        view_menu = menu_bar.addMenu("View")
        view_menu.setProperty("menuRole", "primary")

        for label, mode_value in (("Light Mode", ThemeMode.LIGHT), ("Dark Mode", ThemeMode.DARK)):
            action = QAction(label, self)
            action.setCheckable(True)
            action.triggered.connect(lambda checked, m=mode_value: self._switch_theme(m) if checked else None)
            view_menu.addAction(action)
            self._theme_group.addAction(action)
            self._theme_actions[mode_value.value] = action

        # Ensure the action that matches the current theme is checked.
        self._theme_actions[self._mode.value].setChecked(True)

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
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        cell_list = QWidget()
        cell_list.setProperty("cellType", "list")
        list_layout = QVBoxLayout(cell_list)
        list_layout.setContentsMargins(0, 0, 0, 0)
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
                "Swap these labels for your own widgets; the demo just showcases layout and styling hooks.",
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

    def _switch_theme(self, mode) -> None:
        if mode == self._mode:
            return
        self._mode = mode
        apply_global_style(self._app, mode=mode)
        for row in self._cell_rows:
            row.set_selected(row.is_selected())

    def _handle_cell_selected(self, row: CellRow) -> None:
        for candidate in self._cell_rows:
            candidate.set_selected(candidate is row)

    def _handle_gutter_clicked(self, row: CellRow) -> None:
        if row.is_selected():
            row.set_selected(False)
        else:
            self._handle_cell_selected(row)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Qt styling demo window")
    parser.add_argument(
        "--mode",
        choices=[mode.value for mode in ThemeMode],
        default=DEFAULT_THEME_MODE.value,
        help="Theme mode to use when applying the stylesheet",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    mode = ThemeMode(args.mode)

    app = QApplication(sys.argv)
    apply_global_style(app, mode=mode)

    window = DemoWindow(app, mode)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
