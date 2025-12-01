"""Reusable widget that renders a notebook cell gutter."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from interface.qt.styling.theme.widget_tokens import CellGutterTokens


class CellGutterWidget(QWidget):
    """Line-number gutter that mirrors the styling token contract."""

    def __init__(
        self,
        index: int,
        tokens: CellGutterTokens,
        *,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._tokens = tokens
        self._index = index

        self.setProperty("cellType", "gutter")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        layout = QVBoxLayout(self)
        # Layout geometry insets stay in QWidget code because Qt stylesheets
        # cannot adjust QLayout margins—tokens keep them theme-aware.
        layout.setContentsMargins(
            tokens.layout_inset_left,
            tokens.layout_inset_top,
            tokens.layout_inset_right,
            tokens.layout_inset_bottom,
        )
        layout.setSpacing(0) # Has no effect. 

        self._label = QLabel(self._format_index(index), self)
        self._label.setProperty("cellRole", "line-number")
        self._label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self._label.setMinimumWidth(tokens.label_min_width)
        self._label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        layout.addStretch()
        layout.addWidget(self._label)
        layout.addStretch()

    def set_index(self, index: int) -> None:
        """Update the displayed line number."""

        if index == self._index:
            return
        self._index = index
        self._label.setText(self._format_index(index))

    @staticmethod
    def _format_index(index: int) -> str:
        return f"{index:02d}"


__all__ = ["CellGutterWidget"]
