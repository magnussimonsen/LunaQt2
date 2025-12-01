"""Placeholder sidebar that will later show a notebook table of contents."""

from __future__ import annotations

try:  # pragma: no cover - only imported when Qt is available
    from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget
except ModuleNotFoundError as exc:  # pragma: no cover - runtime guard
    raise SystemExit("PySide6 must be installed to use the sidebar widgets.") from exc


class TocSidebarWidget(QWidget):
    """Simple panel that will eventually list notebook headings."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("TocSidebarPanel")
        self.setAutoFillBackground(True)
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        placeholder = QLabel("This sidepanel will contain the table of content.", self)
        placeholder.setWordWrap(True)
        layout.addWidget(placeholder)
        layout.addStretch()


__all__ = ["TocSidebarWidget"]
