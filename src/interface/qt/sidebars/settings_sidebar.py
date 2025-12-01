"""Settings sidebar focused on typography controls."""

from __future__ import annotations

from typing import Sequence

try:  # pragma: no cover - only imported when Qt is available
    from PySide6.QtCore import Signal
    from PySide6.QtWidgets import (
        QComboBox,
        QFormLayout,
        QHBoxLayout,
        QLabel,
        QSpinBox,
        QVBoxLayout,
        QWidget,
    )
except ModuleNotFoundError as exc:  # pragma: no cover - runtime guard
    raise SystemExit("PySide6 must be installed to use the sidebar widgets.") from exc

from interface.qt.styling.theme.widget_tokens import SidebarTokens

class SettingsSidebarWidget(QWidget):
    """Lightweight form with reactive typography controls."""

    ui_font_size_changed = Signal(int)
    ui_font_family_changed = Signal(str)

    def __init__(
        self,
        parent: QWidget | None = None,
        *,
        ui_font_size: int,
        ui_font_family: str,
        ui_font_choices: Sequence[str],
        min_font_size: int,
        max_font_size: int,
        step: int = 1,
        tokens: SidebarTokens,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("SettingsSidebarPanel")
        self.setAutoFillBackground(True)
        self._tokens = tokens

        self._font_choices = list(ui_font_choices)
        self._ui_font_combo = QComboBox(self)
        self._ui_font_spin = QSpinBox(self)
        self._configure_font_combo(ui_font_family)
        self._configure_font_spin(ui_font_size, min_font_size, max_font_size, step)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(
            tokens.layout_root_margin_left,
            tokens.layout_root_margin_top,
            tokens.layout_root_margin_right,
            tokens.layout_root_margin_bottom,
        )
        main_layout.setSpacing(0)
        
        # Row 2: Toolbar (not used in settings)
        #toolbar = self._build_toolbar()
        #main_layout.addWidget(toolbar)
        
        # Row 3: Content area with settings form
        content = self._build_content_container()
        main_layout.addWidget(content)

    def _configure_font_spin(
        self,
        value: int,
        min_value: int,
        max_value: int,
        step: int,
    ) -> None:
        self._ui_font_spin.setRange(min_value, max_value)
        self._ui_font_spin.setSingleStep(max(1, step))
        self._ui_font_spin.setValue(value)
        self._ui_font_spin.valueChanged.connect(self.ui_font_size_changed)

    def _configure_font_combo(self, family: str) -> None:
        self._ui_font_combo.clear()
        for entry in self._font_choices:
            self._ui_font_combo.addItem(entry)

        try:
            index = self._font_choices.index(family)
        except ValueError:
            index = 0
        self._ui_font_combo.setCurrentIndex(index)
        self._ui_font_combo.setEnabled(bool(self._font_choices))
        self._ui_font_combo.currentTextChanged.connect(self.ui_font_family_changed)

    #def _build_toolbar(self) -> QWidget:
        # In the settings we do not need a toolbar. WE keep the code if it is used in future.
        """Build toolbar section (placeholder for future settings actions)."""
        #toolbar = QWidget(self)
        #toolbar.setProperty("sidebarRole", "toolbar")
        #toolbar.setAutoFillBackground(True)
        
        #toolbar_layout = QHBoxLayout(toolbar)
        #toolbar_layout.setContentsMargins(8, 6, 8, 6)
        #toolbar_layout.setSpacing(8)
        
        # Future: Add reset button, export/import settings, etc.
        #toolbar_layout.addStretch()
        
        #return toolbar

    def _build_content_container(self) -> QWidget:
        container = QWidget(self)
        container.setProperty("sidebarRole", "content")
        container.setAutoFillBackground(True)
        content_layout = QVBoxLayout(container)
        content_layout.setContentsMargins(
            self._tokens.layout_content_margin_left,
            self._tokens.layout_content_margin_top,
            self._tokens.layout_content_margin_right,
            self._tokens.layout_content_margin_bottom,
        )
        content_layout.setSpacing(12)

        #typography_label = QLabel("Typography", container)
        #typography_label.setProperty("sidebarSection", "typography")
        #content_layout.addWidget(typography_label)

        form_layout = QFormLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(6)
        form_layout.addRow("UI font family", self._ui_font_combo)
        form_layout.addRow("UI font size", self._ui_font_spin)
        content_layout.addLayout(form_layout)
        content_layout.addStretch()
        return container


__all__ = ["SettingsSidebarWidget"]
