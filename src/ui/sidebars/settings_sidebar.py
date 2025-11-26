"""Placeholder settings sidebar used by the demo UI."""

from __future__ import annotations

try:  # pragma: no cover - only imported when Qt is available
    from PySide6.QtWidgets import (
        QComboBox,
        QFormLayout,
        QLabel,
        QSpinBox,
        QWidget,
    )
except ModuleNotFoundError as exc:  # pragma: no cover - runtime guard
    raise SystemExit("PySide6 must be installed to use the sidebar widgets.") from exc


class SettingsSidebarWidget(QWidget):
    """Lightweight form with font/precision controls."""

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
    def _build_hint() -> QLabel:
        label = QLabel("Settings wiring will land in a future pass.")
        label.setWordWrap(True)
        label.setProperty("statusRole", "info")
        return label


__all__ = ["SettingsSidebarWidget"]
