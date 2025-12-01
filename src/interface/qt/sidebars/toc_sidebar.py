"""Placeholder sidebar that will later show a notebook table of contents."""

from __future__ import annotations

try:  # pragma: no cover - only imported when Qt is available
    from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget
except ModuleNotFoundError as exc:  # pragma: no cover - runtime guard
    raise SystemExit("PySide6 must be installed to use the sidebar widgets.") from exc

from interface.qt.styling.theme.widget_tokens import SidebarTokens

class TocSidebarWidget(QWidget):
    """Simple panel that will eventually list notebook headings."""

    def __init__(self, parent: QWidget | None = None, *, tokens: SidebarTokens) -> None:
        super().__init__(parent)
        self.setObjectName("TocSidebarPanel")
        self.setAutoFillBackground(True)
        self._tokens = tokens
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            self._tokens.layout_root_margin_left,
            self._tokens.layout_root_margin_top,
            self._tokens.layout_root_margin_right,
            self._tokens.layout_root_margin_bottom,
        )
        layout.setSpacing(0)

        toolbar = self._build_toolbar()
        layout.addWidget(toolbar)

        content = self._build_content()
        layout.addWidget(content)

    def _build_toolbar(self) -> QWidget:
        toolbar = QWidget(self)
        toolbar.setProperty("sidebarRole", "toolbar")
        toolbar.setAutoFillBackground(True)

        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(
            self._tokens.layout_toolbar_margin_left,
            self._tokens.layout_toolbar_margin_top,
            self._tokens.layout_toolbar_margin_right,
            self._tokens.layout_toolbar_margin_bottom,
        )
        toolbar_layout.setSpacing(8)
        toolbar_layout.addWidget(QLabel("Table of Contents", toolbar))
        toolbar_layout.addStretch()
        return toolbar

    def _build_content(self) -> QWidget:
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

        placeholder = QLabel("This sidepanel will contain the table of content.", content)
        placeholder.setWordWrap(True)
        content_layout.addWidget(placeholder)
        content_layout.addStretch()
        return content


__all__ = ["TocSidebarWidget"]
