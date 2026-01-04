"""Python code editor with syntax highlighting and line numbers."""

from __future__ import annotations

import re
from typing import Any

from PySide6.QtCore import QRect, QSize, Qt, Signal
from PySide6.QtGui import (
    QColor,
    QFont,
    QPainter,
    QPalette,
    QSyntaxHighlighter,
    QTextCharFormat,
    QTextCursor,
    QTextDocument,
)
from PySide6.QtWidgets import QPlainTextEdit, QTextEdit, QWidget


class PythonSyntaxHighlighter(QSyntaxHighlighter):
    """Python syntax highlighter using regular expressions."""

    _KEYWORDS = {
        "False", "class", "finally", "is", "return",
        "None", "continue", "for", "lambda", "try",
        "True", "def", "from", "nonlocal", "while",
        "and", "del", "global", "not", "with",
        "as", "elif", "if", "or", "yield",
        "assert", "else", "import", "pass",
        "break", "except", "in", "raise",
    }

    _BUILTINS = {
        "abs", "all", "any", "bool", "dict", "float", "int",
        "len", "list", "map", "max", "min", "print", "range",
        "set", "str", "sum", "zip", "enumerate", "isinstance",
        "tuple", "type", "super", "sorted", "reversed", "open",
    }

    def __init__(self, document: QTextDocument, is_dark_mode: bool = False) -> None:
        """Initialize syntax highlighter.
        
        Args:
            document: Text document to highlight
            is_dark_mode: Whether to use dark mode colors
        """
        super().__init__(document)
        self._is_dark_mode = is_dark_mode
        self._setup_formats()

    def set_dark_mode(self, is_dark: bool) -> None:
        """Update color scheme for theme changes.
        
        Args:
            is_dark: Whether dark mode is active
        """
        if self._is_dark_mode != is_dark:
            self._is_dark_mode = is_dark
            self._setup_formats()
            self.rehighlight()

    def _setup_formats(self) -> None:
        """Configure text formats based on current theme."""
        # Keywords: Blue, Bold
        self._keyword_format = QTextCharFormat()
        keyword_color = QColor(86, 156, 214) if self._is_dark_mode else QColor(0, 0, 255)
        self._keyword_format.setForeground(keyword_color)
        self._keyword_format.setFontWeight(QFont.Weight.Bold)

        # Built-ins: Purple
        self._builtin_format = QTextCharFormat()
        builtin_color = QColor(197, 134, 192) if self._is_dark_mode else QColor(128, 0, 128)
        self._builtin_format.setForeground(builtin_color)

        # Comments: Gray, Italic
        self._comment_format = QTextCharFormat()
        comment_color = QColor(106, 153, 85) if self._is_dark_mode else QColor(0, 128, 0)
        self._comment_format.setForeground(comment_color)
        self._comment_format.setFontItalic(True)

        # Strings: Orange/Brown
        self._string_format = QTextCharFormat()
        string_color = QColor(206, 145, 120) if self._is_dark_mode else QColor(163, 21, 21)
        self._string_format.setForeground(string_color)

        # Function/class names: Teal/Green
        self._defclass_format = QTextCharFormat()
        defclass_color = QColor(78, 201, 176) if self._is_dark_mode else QColor(0, 128, 128)
        self._defclass_format.setForeground(defclass_color)
        self._defclass_format.setFontWeight(QFont.Weight.Bold)

    def highlightBlock(self, text: str) -> None:  # type: ignore[override]
        """Highlight a single block of text.
        
        Args:
            text: Text block to highlight
        """
        self.setCurrentBlockState(0)

        # Highlight keywords and builtins
        for match in re.finditer(r"\b[A-Za-z_][A-Za-z0-9_]*\b", text):
            word = match.group(0)
            if word in self._KEYWORDS:
                self.setFormat(match.start(), len(word), self._keyword_format)
            elif word in self._BUILTINS:
                self.setFormat(match.start(), len(word), self._builtin_format)

        # Highlight def/class names
        for match in re.finditer(r"\b(def|class)\s+(\w+)", text):
            self.setFormat(match.start(1), len(match.group(1)), self._keyword_format)
            self.setFormat(match.start(2), len(match.group(2)), self._defclass_format)

        # Highlight comments
        for match in re.finditer(r"#[^\n]*", text):
            self.setFormat(match.start(), match.end() - match.start(), self._comment_format)

        # Highlight single/double quoted strings
        for match in re.finditer(r"(['\"])(?:(?=(\\?))\2.)*?\1", text):
            self.setFormat(match.start(), match.end() - match.start(), self._string_format)

        # Handle multi-line strings
        self._apply_multiline_strings(text)

    def _apply_multiline_strings(self, text: str) -> None:
        """Apply highlighting for triple-quoted strings across blocks.
        
        Args:
            text: Current text block
        """
        for delimiter in ("'''", '"""'):
            delimiter_state = hash(delimiter)
            
            # Continue from previous block if in multi-line string
            if self.previousBlockState() == delimiter_state:
                end_idx = text.find(delimiter)
                if end_idx == -1:
                    # String continues to next block
                    self.setFormat(0, len(text), self._string_format)
                    self.setCurrentBlockState(delimiter_state)
                    return
                # String ends in this block
                self.setFormat(0, end_idx + 3, self._string_format)
                start_idx = end_idx + 3
            else:
                start_idx = 0

            # Find new multi-line strings in this block
            while True:
                start_idx = text.find(delimiter, start_idx)
                if start_idx < 0:
                    break
                end_idx = text.find(delimiter, start_idx + 3)
                if end_idx < 0:
                    # String starts but doesn't end
                    self.setFormat(start_idx, len(text) - start_idx, self._string_format)
                    self.setCurrentBlockState(delimiter_state)
                    return
                # String starts and ends in this block
                self.setFormat(start_idx, end_idx - start_idx + 3, self._string_format)
                start_idx = end_idx + 3


class LineNumberArea(QWidget):
    """Line number display area for code editor."""

    def __init__(self, editor: PythonEditor) -> None:
        """Initialize line number area.
        
        Args:
            editor: Parent editor widget
        """
        super().__init__(editor)
        self._editor = editor

    def sizeHint(self) -> QSize:  # type: ignore[override]
        """Calculate size hint based on editor."""
        return QSize(self._editor.line_number_area_width(), 0)

    def paintEvent(self, event: Any) -> None:  # type: ignore[override]
        """Paint line numbers.
        
        Args:
            event: Paint event
        """
        self._editor.paint_line_numbers(event)


class PythonEditor(QPlainTextEdit):
    """Code editor for Python with syntax highlighting and line numbers."""

    focus_changed = Signal(bool)
    execute_requested = Signal()

    def __init__(self, parent: QWidget | None = None, is_dark_mode: bool = False, font_size: int = 11) -> None:
        """Initialize Python editor.
        
        Args:
            parent: Parent widget
            is_dark_mode: Whether to use dark mode colors
            font_size: Font size in points (default: 11)
        """
        super().__init__(parent)
        self._tab_spaces = 4
        self._is_dark_mode = is_dark_mode
        self._font_size = font_size
        
        # Configure editor behavior
        self.setTabChangesFocus(False)
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.setFrameShape(QPlainTextEdit.Shape.NoFrame)
        self.setFrameShadow(QPlainTextEdit.Shadow.Plain)
        
        # Set monospace font - use Fira Code (bundled with app)
        font = QFont("Fira Code", self._font_size)
        font.setStyleHint(QFont.StyleHint.Monospace)
        font.setFixedPitch(True)
        self.setFont(font)
        
        # Setup syntax highlighting
        self._highlighter = PythonSyntaxHighlighter(self.document(), is_dark_mode)
        
        # Setup line numbers
        self._line_number_area = LineNumberArea(self)
        self.blockCountChanged.connect(self._update_line_number_area_width)
        self.updateRequest.connect(self._update_line_number_area)
        self._update_line_number_area_width(0)
        
        # Current line highlighting
        self.cursorPositionChanged.connect(self._highlight_current_line)
        self._highlight_current_line()
        
        # Set tab width
        self.set_tab_width_spaces(self._tab_spaces)
        
        # Auto-height adjustment
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.document().documentLayout().documentSizeChanged.connect(self._update_height)
        self.textChanged.connect(self._update_height)  # Also update on text change
        self._update_height()

    def set_dark_mode(self, is_dark: bool) -> None:
        """Update editor for theme change.
        
        Args:
            is_dark: Whether dark mode is active
        """
        if self._is_dark_mode != is_dark:
            self._is_dark_mode = is_dark
            self._highlighter.set_dark_mode(is_dark)
            self._highlight_current_line()
            self._line_number_area.update()

    def set_tab_width_spaces(self, spaces: int) -> None:
        """Set tab width in spaces.
        
        Args:
            spaces: Number of spaces per tab
        """
        self._tab_spaces = max(1, spaces)
        metrics = self.fontMetrics()
        self.setTabStopDistance(metrics.horizontalAdvance(' ') * self._tab_spaces)

    def set_font_size(self, size: int) -> None:
        """Update editor font size.
        
        Args:
            size: Font size in points
        """
        self._font_size = max(6, min(size, 72))  # Clamp between 6-72
        font = self.font()
        font.setPointSize(self._font_size)
        self.setFont(font)
        
        # Update tab width for new font metrics
        self.set_tab_width_spaces(self._tab_spaces)
        
        # Update line number area
        self._update_line_number_area_width(0)
        self._line_number_area.update()
        
        # Update height for new font size
        self._update_height()

    # Focus events ---------------------------------------------------------
    def focusInEvent(self, event: Any) -> None:  # type: ignore[override]
        """Handle focus in event.
        
        Args:
            event: Focus event
        """
        super().focusInEvent(event)
        self.focus_changed.emit(True)

    def focusOutEvent(self, event: Any) -> None:  # type: ignore[override]
        """Handle focus out event.
        
        Args:
            event: Focus event
        """
        super().focusOutEvent(event)
        self.focus_changed.emit(False)

    # Keyboard handling ----------------------------------------------------
    def keyPressEvent(self, event: Any) -> None:  # type: ignore[override]
        """Handle key press events for smart editing.
        
        Args:
            event: Key event
        """
        key = event.key()
        modifiers = event.modifiers()

        # Shift+Enter: Execute code
        if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter) and modifiers == Qt.KeyboardModifier.ShiftModifier:
            event.accept()
            self.execute_requested.emit()
            return

        # Enter: Smart auto-indent
        if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            indent = self._current_line_indent()
            extra = ''
            # Add extra indent after lines ending with ':'
            if self.textCursor().block().text().rstrip().endswith(":"):
                extra = ' ' * self._tab_spaces
            super().keyPressEvent(event)
            self.insertPlainText(indent + extra)
            return

        # Backspace: Remove full indent if on spaces
        if key == Qt.Key.Key_Backspace and modifiers == Qt.KeyboardModifier.NoModifier:
            cursor = self.textCursor()
            if not cursor.hasSelection():
                pos_in_block = cursor.positionInBlock()
                if pos_in_block >= self._tab_spaces:
                    block_text = cursor.block().text()
                    segment = block_text[pos_in_block - self._tab_spaces : pos_in_block]
                    if segment == ' ' * self._tab_spaces:
                        cursor.beginEditBlock()
                        for _ in range(self._tab_spaces):
                            cursor.deletePreviousChar()
                        cursor.endEditBlock()
                        return
            super().keyPressEvent(event)
            return

        # Tab/Shift+Tab: Indent/dedent
        if key == Qt.Key.Key_Tab and modifiers in (Qt.KeyboardModifier.NoModifier, Qt.KeyboardModifier.ShiftModifier):
            spaces = ' ' * self._tab_spaces
            cursor = self.textCursor()
            if modifiers == Qt.KeyboardModifier.ShiftModifier:
                # Dedent
                cursor.movePosition(QTextCursor.MoveOperation.StartOfLine, QTextCursor.MoveMode.MoveAnchor)
                line = cursor.block().text()
                remove = min(self._tab_spaces, len(line) - len(line.lstrip(' ')))
                if remove > 0:
                    cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor, remove)
                    cursor.removeSelectedText()
                else:
                    self.textCursor().deletePreviousChar()
            else:
                # Indent
                cursor.insertText(spaces)
            return

        super().keyPressEvent(event)

    # Line numbers ---------------------------------------------------------
    def line_number_area_width(self) -> int:
        """Calculate required width for line number area.
        
        Returns:
            Width in pixels
        """
        digits = len(str(max(1, self.blockCount())))
        space = self.fontMetrics().horizontalAdvance('9') * digits + 12
        return space

    def _update_line_number_area_width(self, _new_block_count: int) -> None:
        """Update editor margins for line number area.
        
        Args:
            _new_block_count: New block count (unused)
        """
        margins = self.viewportMargins()
        left_margin = self.line_number_area_width()
        if margins.left() != left_margin:
            self.setViewportMargins(left_margin, margins.top(), margins.right(), margins.bottom())

    def _update_line_number_area(self, rect: QRect, dy: int) -> None:
        """Update line number area on scroll or content change.
        
        Args:
            rect: Update rectangle
            dy: Vertical scroll delta
        """
        if dy:
            self._line_number_area.scroll(0, dy)
        else:
            self._line_number_area.update(0, rect.y(), self._line_number_area.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self._update_line_number_area_width(self.blockCount())

    def resizeEvent(self, event: Any) -> None:  # type: ignore[override]
        """Handle resize event to update line number area.
        
        Args:
            event: Resize event
        """
        super().resizeEvent(event)
        cr = self.contentsRect()
        width = self.line_number_area_width()
        self._line_number_area.setGeometry(QRect(cr.left(), cr.top(), width, cr.height()))

    def paint_line_numbers(self, event: Any) -> None:
        """Paint line numbers in the line number area.
        
        Args:
            event: Paint event
        """
        painter = QPainter(self._line_number_area)
        
        # Background color (slightly darker than editor)
        bg = self.palette().color(QPalette.ColorRole.Base).darker(105)
        painter.fillRect(event.rect(), bg)
        
        # Text colors
        fg = self.palette().color(QPalette.ColorRole.Text).lighter(150)
        highlight = self.palette().color(QPalette.ColorRole.Text)
        
        # Paint line numbers
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())
        current = self.textCursor().blockNumber()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(highlight if block_number == current else fg)
                painter.drawText(
                    0,
                    top,
                    self._line_number_area.width() - 6,
                    self.fontMetrics().height(),
                    Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                    number,
                )

            block = block.next()
            block_number += 1
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())

    # Helper methods -------------------------------------------------------
    def _current_line_indent(self) -> str:
        """Get indentation of current line.
        
        Returns:
            Whitespace prefix of current line
        """
        cursor = self.textCursor()
        line_text = cursor.block().text()
        match = re.match(r"\s*", line_text)
        return match.group(0) if match else ""

    def _highlight_current_line(self) -> None:
        """Highlight the current line with a subtle background."""
        extra = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            # Subtle highlight color
            if self._is_dark_mode:
                line_color = QColor(80, 80, 80, 30)
            else:
                line_color = QColor(200, 200, 200, 50)
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextCharFormat.Property.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra.append(selection)
        self.setExtraSelections(extra)

    # Auto-height adjustment --------------------------------------------------
    def _update_height(self, size: QSize | None = None) -> None:
        """Update editor height to fit content (like OLD_LUNA_QT).
        
        Args:
            size: Document size (unused, for signal compatibility)
        """
        # Calculate height based on line count (more reliable than document size)
        doc = self.document()
        block_count = max(1, doc.blockCount())
        line_height = self.fontMetrics().lineSpacing()
        doc_height = line_height * block_count
        
        # Add margins, frame, and document margin
        margins = self.contentsMargins()
        frame_width = self.frameWidth() * 2
        doc_margin = int(doc.documentMargin() * 2)
        padding = margins.top() + margins.bottom() + frame_width + doc_margin + 4
        
        total_height = int(doc_height + padding)
        
        # Set minimum height (at least 3 lines)
        min_height = line_height * 3 + padding
        total_height = max(total_height, min_height, 50)
        
        # Update fixed height
        self.setFixedHeight(total_height)
        self.updateGeometry()
        
        # Force parent to update layout
        if self.parent():
            self.parent().updateGeometry()

    def sizeHint(self) -> QSize:
        """Return size hint based on content.
        
        Returns:
            Preferred size for the editor
        """
        # Width: use parent's width or a default
        width = 400
        if self.parent():
            parent_width = self.parent().width()
            if parent_width > 0:
                width = parent_width
        
        # Height: based on content
        doc_height = self.document().size().height()
        margins = self.contentsMargins()
        frame_width = self.frameWidth()
        height = int(doc_height) + margins.top() + margins.bottom() + (frame_width * 2)
        
        # Minimum height
        min_height = self.fontMetrics().height() * 3
        height = max(height, min_height)
        
        return QSize(width, height)


__all__ = ["PythonEditor", "PythonSyntaxHighlighter", "LineNumberArea"]
