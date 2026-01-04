# Python Editor Implementation Plan for LunaQt2

## Analysis of OLD_LUNA_QT Implementation

### Components Found:

#### 1. **PythonCodeEditor** (`python_editor.py`)
A QPlainTextEdit-based editor with:
- **Syntax Highlighting**: Custom `_PythonSyntaxHighlighter` using QSyntaxHighlighter
  - Keywords (def, class, if, for, etc.) - Blue, Bold
  - Built-ins (print, len, range, etc.) - Purple
  - Comments - Gray, Italic
  - Strings (single, double, triple-quoted) - Orange
  - Function/class names after def/class - Green, Bold
  - Multi-line string support across blocks
  
- **Line Numbers**: Custom `_LineNumberArea` widget
  - Displays line numbers in left margin
  - Current line highlighted
  - Auto-adjusts width based on line count
  - Background slightly darker than editor
  
- **Smart Indentation**:
  - Tab key inserts 4 spaces (configurable)
  - Shift+Tab removes 4-space indent
  - Auto-indent after Enter (preserves current indent)
  - Extra indent after lines ending with `:` (def, if, for, etc.)
  - Backspace removes 4 spaces if cursor is on indent
  
- **Keyboard Shortcuts**:
  - Shift+Enter: Emit `execute_requested` signal
  
- **Visual Features**:
  - Current line highlighting (subtle background)
  - Focus change signals
  - No wrap mode
  - No frame
  - Custom tab stop distance based on font metrics

#### 2. **CodeCell Integration** (`code_cell.py`)
- Embeds PythonCodeEditor in a cell widget
- Execution count label (In [n]:)
- Output area (QPlainTextEdit, read-only)
- Plot display with scaling controls
- Auto-height adjustment based on content
- Font service integration for code font

#### 3. **BaseCell** (`base_cell.py`)
- Base class for all cell types
- Handles selection, focus, gutter display
- Content change notifications
- Size hint management

---

## Implementation Plan for LunaQt2

### Current State:
- CellRow displays cells as read-only QLabels
- Execution system functional but no editing capability
- Need interactive editor to write/modify code

### Proposed Architecture:

#### Phase 1: Create PythonEditor Widget (Port & Adapt)
**Goal**: Port PythonCodeEditor as a standalone reusable widget

**Files to Create**:
- `src/interface/qt/widgets/python_editor.py` - Main editor widget

**Components**:
1. **Syntax Highlighter** (`PythonSyntaxHighlighter`)
   - Keep regex-based approach from OLD_LUNA_QT
   - Adapt colors to use theme tokens (light/dark mode)
   - Keywords, builtins, comments, strings, def/class names

2. **Line Number Area** (`LineNumberArea`)
   - Paint line numbers in left margin
   - Highlight current line number
   - Auto-size based on line count

3. **Editor** (`PythonEditor`)
   - Inherit from QPlainTextEdit
   - Smart tab/indent handling
   - Auto-indent on Enter
   - Shift+Enter for execution
   - Current line highlighting
   - Focus change signals
   - Text change signals

**Theme Integration**:
- Use `_TextTokens.primary` for normal text
- Use theme-aware colors for syntax highlighting
- Support light/dark mode switching

---

#### Phase 2: Integrate Editor into CellRow
**Goal**: Replace read-only body label with interactive editor for Python cells

**Modifications**:
- `src/interface/qt/windows/main_window.py` - CellRow class
  - Replace `self._body_label` with `self._editor` for Python cells
  - Keep label for Markdown cells
  - Wire editor text changes to cell content updates
  - Wire editor execute signal to Run handler
  - Handle editor focus for cell selection

**Cell Type Detection**:
- Check cell.cell_type == "python"
- Create PythonEditor for Python cells
- Create QLabel (or MarkdownEditor later) for other types

**Content Synchronization**:
- Editor text changes → update Cell model via CellManager
- Cell model updates → update editor text (avoid loops)

---

#### Phase 3: Auto-Height Adjustment
**Goal**: Editor expands vertically to fit content (no scrollbar)

**Implementation**:
- Calculate document height based on line count
- Set fixed height on editor widget
- Update on text changes
- Trigger parent layout updates

**Sizing**:
- Minimum height: ~2-3 lines (50-60px)
- Maximum height: None (grows with content)
- Horizontal: Expand to fill available width
- Vertical scrollbar: Hidden (widget grows instead)

---

#### Phase 4: Font Management
**Goal**: Use monospace font for code editor

**Options**:
1. Use existing font system from assets/fonts
2. Fixed font (FiraCode, SourceCodePro, etc.)
3. System monospace font

**Implementation**:
- Set monospace font on editor
- Calculate tab width based on font metrics
- Update line number area on font changes

---

#### Phase 5: Styling Integration
**Goal**: Editor colors match theme system

**QSS Generation**:
- Add editor-specific styles to widget_styles/
- Background, text color, selection color
- Line number area colors
- Border/frame handling

**Theme Tokens**:
- Reuse existing text/background tokens where possible
- Add code-specific tokens if needed

---

#### Phase 6: Content Persistence
**Goal**: Editor changes save to cell model

**Flow**:
1. User types in editor
2. `textChanged` signal emitted
3. Debounced save to avoid excessive writes
4. Call `cell_manager.update_cell(cell_id, content=new_text)`
5. Cell model updated
6. DataStore persists to disk

**Debouncing**:
- QTimer with 500ms delay
- Reset timer on each keystroke
- Only save after user stops typing

---

### Summary of Changes:

**New Files**:
- `src/interface/qt/widgets/python_editor.py` - Editor widget with syntax highlighting

**Modified Files**:
- `src/interface/qt/windows/main_window.py` - CellRow to use editor for Python cells
- `src/interface/qt/widgets/__init__.py` - Export PythonEditor
- `src/interface/qt/styling/widget_styles/` - Add editor styling (optional)

**Features**:
✅ Syntax highlighting (keywords, strings, comments, etc.)
✅ Line numbers with current line highlight
✅ Smart indentation (auto-indent, tab=4 spaces)
✅ Shift+Enter to execute
✅ Auto-height sizing (no vertical scroll)
✅ Theme-aware colors (light/dark mode)
✅ Content persistence to cell model
✅ Focus management for cell selection

---

## Implementation Priority:

1. **Phase 1** - Create standalone PythonEditor widget (high priority)
2. **Phase 2** - Integrate into CellRow (high priority)
3. **Phase 3** - Auto-height adjustment (medium priority)
4. **Phase 4** - Font management (medium priority)
5. **Phase 5** - Styling integration (low priority - can use basic colors first)
6. **Phase 6** - Content persistence (high priority)

Suggest starting with Phases 1, 2, and 6 to get basic editing + persistence working, then add polish with Phases 3-5.
