"""Reusable widget that renders the main cell body/container."""

from __future__ import annotations

from typing import Iterable

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget

from interface.qt.styling.theme.widget_tokens import CellRowTokens


class CellContainerWidget(QFrame):
    """Container that applies consistent padding and layout for cell content."""

    def __init__(
        self,
        tokens: CellRowTokens,
        *,
        parent: QWidget | None = None,
        initial_children: Iterable[QWidget] | None = None,
    ) -> None:
        super().__init__(parent)
        self._tokens = tokens

        self.setProperty("cellType", "container")
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(
            tokens.cell_row_padding_left,
            tokens.cell_row_padding_top,
            tokens.cell_row_padding_right,
            tokens.cell_row_padding_bottom,
        )
        self._layout.setSpacing(tokens.cell_row_spacing)

        if initial_children:
            for child in initial_children:
                self.add_content_widget(child)

    def add_content_widget(self, widget: QWidget, stretch: int = 0) -> None:
        """Append a widget to the container layout."""

        self._layout.addWidget(widget, stretch)

    def insert_content_widget(self, index: int, widget: QWidget, stretch: int = 0) -> None:
        """Insert a widget at a specific index inside the container."""

        self._layout.insertWidget(index, widget, stretch)

    def layout(self) -> QVBoxLayout:  # type: ignore[override]
        """Expose the internal layout for callers that need finer control."""

        return self._layout


__all__ = ["CellContainerWidget"]
