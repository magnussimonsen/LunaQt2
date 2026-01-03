from __future__ import annotations

from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QWidget,
)


class BaseToolbar(QWidget):
    """Base class for cell toolbars."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        self._layout = layout

    def add_button(self, text: str, btn_type: str = "toolbar", callback=None) -> QPushButton:
        button = QPushButton(text)
        button.setProperty("btnType", btn_type)
        if callback:
            button.clicked.connect(callback)
        self._layout.addWidget(button)
        return button

    def add_stretch(self) -> None:
        self._layout.addStretch(1)


class EmptyToolbar(BaseToolbar):
    """Toolbar shown when no cell is selected."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        # Empty toolbar has no buttons
        self.add_stretch()


class CodeToolbar(BaseToolbar):
    """Toolbar for Python code cells."""

    run_requested = Signal()
    stop_requested = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        
        self._run_button = self.add_button("▶ Run", "run", self._on_run_clicked)
        self._stop_button = self.add_button("⬛ Stop", "stop", self._on_stop_clicked)
        self._stop_button.setEnabled(False)  # Initially disabled
        
        self.add_stretch()

    def _on_run_clicked(self) -> None:
        self.run_requested.emit()

    def _on_stop_clicked(self) -> None:
        self.stop_requested.emit()

    def set_running_state(self, is_running: bool) -> None:
        self._run_button.setEnabled(not is_running)
        self._stop_button.setEnabled(is_running)


class MarkdownToolbar(BaseToolbar):
    """Toolbar for Markdown cells."""

    preview_toggled = Signal(bool)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        
        self._preview_button = self.add_button("Preview", "toolbar", self._on_preview_clicked)
        self._preview_button.setCheckable(True)
        
        self.add_stretch()

    def _on_preview_clicked(self) -> None:
        is_checked = self._preview_button.isChecked()
        self.preview_toggled.emit(is_checked)
    
    def set_preview_state(self, is_preview: bool) -> None:
        if self._preview_button.isChecked() != is_preview:
            self._preview_button.setChecked(is_preview)
            # Force Qt to re-evaluate :checked pseudo-class
            self._preview_button.style().unpolish(self._preview_button)
            self._preview_button.style().polish(self._preview_button)
            self._preview_button.update()


class DynamicToolbar(QWidget):
    """Container that switches toolbars based on context."""

    run_requested = Signal()
    stop_requested = Signal()
    preview_toggled = Signal(bool)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._stack = QStackedWidget()
        layout.addWidget(self._stack)

        self._empty_toolbar = EmptyToolbar()
        self._code_toolbar = CodeToolbar()
        self._markdown_toolbar = MarkdownToolbar()

        self._stack.addWidget(self._empty_toolbar)
        self._stack.addWidget(self._code_toolbar)
        self._stack.addWidget(self._markdown_toolbar)

        # Connect signals
        self._code_toolbar.run_requested.connect(self.run_requested)
        self._code_toolbar.stop_requested.connect(self.stop_requested)
        self._markdown_toolbar.preview_toggled.connect(self.preview_toggled)

        self._current_cell_type = None

    def set_cell_type(self, cell_type: str | None) -> None:
        self._current_cell_type = cell_type
        if cell_type == "code":
            self._stack.setCurrentWidget(self._code_toolbar)
        elif cell_type == "markdown":
            self._stack.setCurrentWidget(self._markdown_toolbar)
        else:
            self._stack.setCurrentWidget(self._empty_toolbar)

    def set_code_running(self, is_running: bool) -> None:
        self._code_toolbar.set_running_state(is_running)

    def set_markdown_preview(self, is_preview: bool) -> None:
        self._markdown_toolbar.set_preview_state(is_preview)
