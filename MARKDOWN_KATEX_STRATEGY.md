# Markdown and KaTeX Implementation Strategy for LunaQt2

## Executive Summary

Based on analysis of OLD_LUNA_QT, this document outlines a phased strategy to implement markdown rendering with KaTeX math support in LunaQt2. The old implementation had a basic placeholder; this strategy provides a complete, production-ready approach.

## 🎯 Key Recommendations (TL;DR)

### **Start Here: Lightweight Approach (Recommended)**

1. **Use `python-markdown` + `pykatex` with `QTextBrowser`**
   - ✅ No heavy dependencies (no WebEngine = saves ~100MB)
   - ✅ Fast startup and rendering
   - ✅ Sufficient for 95% of educational math needs
   - ✅ Easier to maintain and debug
   - ✅ Better theme integration with QPalette

2. **Implementation Priority**
   - **Week 1**: Port markdown cell structure + add `python-markdown`
   - **Week 2**: Add `pykatex` for math rendering (inline `$x^2$` and block `$$...$$`)
   - **Week 3**: Polish with syntax highlighting and toolbar buttons
   - **Week 4**: Documentation and testing

3. **Defer These (Not MVP)**
   - Qt WebEngine implementation (only if users demand interactive math)
   - Live preview while typing (nice-to-have, adds complexity)
   - Export to PDF (can add later)

4. **Critical Dependencies to Add**

   ```
   markdown>=3.5          # Core markdown parsing
   pykatex>=0.1.3         # Math rendering (lightweight)
   Pygments>=2.15         # Syntax highlighting for code blocks
   ```

5. **Architecture Pattern**
   - Keep rendering logic in `MarkdownCell` for now (simple)
   - Extract to `MarkdownRenderer` service later if needed for reuse
   - Bundle KaTeX CSS/fonts in `src/assets/katex/` for offline use

---

## Current State Analysis

### OLD_LUNA_QT Implementation

The old LunaQt had a **basic placeholder** markdown cell:

- **Edit Mode**: Plain `QTextEdit` for markdown input
- **Preview Mode**: `QTextBrowser` with minimal HTML rendering
- **Rendering**: Simple newline-to-`<br>` conversion (no real markdown parsing)
- **Math Support**: None implemented (only planned in docs)
- **Toggle**: Button to switch between edit/preview modes

**Key Finding**: The old implementation was intentionally minimal (MVP), with comments noting "Future: use markdown library for proper rendering."

### Planned Features (from plan-doc.md)

- Markdown cells should support standard markdown syntax
- Inline math between `$...$`
- Block math between `$$...$$`
- KaTeX rendering for LaTeX math
- Options: Qt WebEngine for rich rendering OR QTextBrowser for lightweight rendering

---

## Recommended Implementation Strategy

### Phase 1: Basic Markdown Rendering (Foundation)

**Goal**: Port and enhance the existing markdown cell with proper markdown parsing.

#### 1.1 Port Markdown Cell Structure

Copy the working cell architecture from OLD_LUNA_QT:

```
src/interface/qt/widgets/cells/
├── base_cell.py          # Already exists or port from old
├── markdown_cell.py      # NEW - port and enhance
└── python_cell.py        # Already exists
```

**Key Components**:

- `_MarkdownEditor(QTextEdit)` - Edit mode with monospace font
- `_MarkdownPreview(QTextBrowser)` - Preview mode with rendered HTML
- Toggle button to switch between modes
- Focus management and content synchronization

#### 1.2 Add Markdown Library

**Recommended Library**: `markdown` (Python-Markdown)

**Why**:

- Pure Python (no C dependencies, easier deployment)
- Extensible with plugins
- Well-maintained and widely used
- Supports custom extensions for math syntax

**Add to requirements.txt**:

```python
PySide6>=6.7
matplotlib>=3.0
markdown>=3.5         # For markdown rendering
pymdown-extensions>=10.0  # Additional markdown features (optional)
```

**Alternative**: `mistune` - Faster, but less extensible

#### 1.3 Enhanced Render Function

Replace the simple `_render_markdown()` with proper parsing:

```python
import markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

class MarkdownCell(BaseCell):
    def __init__(self, ...):
        super().__init__(...)
        # Initialize markdown processor once
        self._md_processor = markdown.Markdown(
            extensions=[
                'extra',      # Tables, fenced code, etc.
                'nl2br',      # Newline to <br>
                'sane_lists', # Better list handling
                'codehilite', # Syntax highlighting
            ]
        )

    def _render_markdown(self, text: str) -> str:
        """Render markdown to HTML with theme-aware styling."""
        # Convert markdown to HTML
        html_body = self._md_processor.convert(text)

        # Get theme colors from palette
        bg_color = self.palette().base().color().name()
        text_color = self.palette().text().color().name()
        code_bg = self.palette().alternateBase().color().name()

        # Wrap in styled HTML with theme colors
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    background-color: {bg_color};
                    color: {text_color};
                    font-family: {self._get_text_font_family()};
                    font-size: {self._get_text_font_size()}pt;
                    padding: 8px;
                    margin: 0;
                }}
                code {{
                    background-color: {code_bg};
                    padding: 2px 4px;
                    border-radius: 3px;
                    font-family: 'Fira Code', 'Consolas', monospace;
                }}
                pre {{
                    background-color: {code_bg};
                    padding: 10px;
                    border-radius: 5px;
                    overflow-x: auto;
                }}
                blockquote {{
                    border-left: 4px solid {text_color};
                    padding-left: 10px;
                    margin-left: 0;
                    opacity: 0.8;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                }}
                table, th, td {{
                    border: 1px solid {text_color};
                    padding: 6px;
                }}
                a {{
                    color: #3498db;
                }}
            </style>
        </head>
        <body>
            {html_body}
        </body>
        </html>
        """
        return html
```

**Benefits**:

- Real markdown syntax support (headers, lists, tables, links, images)
- Theme-aware colors (respects light/dark mode)
- Font integration with app font settings
- Inline code and code blocks with syntax highlighting

---

### Phase 2: KaTeX Math Rendering (Advanced)

**Goal**: Add LaTeX math rendering using KaTeX for inline `$...$` and block `$$...$$` math.

#### 2.1 Two Implementation Options

##### **Option A: QTextBrowser with Preprocessed HTML (Recommended)**

**Approach**: Pre-render KaTeX to HTML on the Python side, display in QTextBrowser.

**Pros**:

- No Qt WebEngine dependency (lighter, faster startup)
- Works with existing `QTextBrowser`
- Better for simple notebooks
- Easier theme integration

**Cons**:

- Requires Node.js/npm for KaTeX CLI or Python wrapper
- Math is rendered as static HTML (no interactive features)

**Implementation**:

1. **Add KaTeX CLI Wrapper**:

   ```bash
   pip install pykatex  # Python wrapper for KaTeX
   ```

2. **Math Preprocessor Extension**:

   ```python
   import re
   import pykatex

   class KaTeXPreprocessor(Preprocessor):
       """Markdown preprocessor to convert LaTeX math to KaTeX HTML."""

       # Regex patterns
       INLINE_PATTERN = r'\$(.+?)\$'
       BLOCK_PATTERN = r'\$\$(.+?)\$\$'

       def run(self, lines: list[str]) -> list[str]:
           text = '\n'.join(lines)

           # Process block math first (to avoid conflicts)
           def render_block(match):
               latex = match.group(1)
               try:
                   html = pykatex.render(latex, display_mode=True)
                   return f'<div class="katex-block">{html}</div>'
               except Exception as e:
                   return f'<div class="katex-error">Math Error: {e}</div>'

           text = re.sub(self.BLOCK_PATTERN, render_block, text, flags=re.DOTALL)

           # Process inline math
           def render_inline(match):
               latex = match.group(1)
               try:
                   html = pykatex.render(latex, display_mode=False)
                   return f'<span class="katex-inline">{html}</span>'
               except Exception as e:
                   return f'<span class="katex-error">({e})</span>'

           text = re.sub(self.INLINE_PATTERN, render_inline, text)

           return text.split('\n')

   class KaTeXExtension(Extension):
       def extendMarkdown(self, md):
           md.preprocessors.register(
               KaTeXPreprocessor(md), 'katex', 27
           )

   # Usage in MarkdownCell
   self._md_processor = markdown.Markdown(
       extensions=[
           'extra',
           KaTeXExtension(),  # Add KaTeX support
       ]
   )
   ```

3. **Include KaTeX CSS** in HTML template:
   ```python
   KATEX_CSS = """
   <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
   """
   # Or bundle KaTeX CSS locally for offline use
   ```

**Offline Support**: Bundle KaTeX CSS/fonts in app assets:

```
src/assets/katex/
├── katex.min.css
└── fonts/
    ├── KaTeX_Main-Regular.woff2
    ├── KaTeX_Math-Italic.woff2
    └── ...
```

Then reference locally:

```python
katex_css_path = get_asset_path('katex/katex.min.css')
KATEX_CSS = f'<link rel="stylesheet" href="file://{katex_css_path}">'
```

##### **Option B: Qt WebEngine View (Full Featured)**

**Approach**: Use `QWebEngineView` for full HTML/CSS/JS rendering with live KaTeX.

**Pros**:

- Full KaTeX features (interactive, copy-able math)
- Easier to implement (just load HTML with KaTeX JS)
- Better for complex notebooks with rich media

**Cons**:

- Large dependency (Qt WebEngine is ~50-100 MB)
- Slower startup time
- More memory usage
- Complicates deployment

**Implementation**:

1. **Add Qt WebEngine**:

   ```python
   # requirements.txt
   PySide6-WebEngine>=6.7
   ```

2. **Replace QTextBrowser with QWebEngineView**:

   ```python
   from PySide6.QtWebEngineWidgets import QWebEngineView

   class _MarkdownPreview(QWebEngineView):
       def __init__(self):
           super().__init__()
           # Enable offline mode
           self.settings().setAttribute(
               QWebEngineSettings.LocalContentCanAccessRemoteUrls, False
           )
   ```

3. **HTML Template with KaTeX Auto-Render**:

   ```python
   def _render_markdown(self, text: str) -> str:
       # Process markdown first
       html_body = self._md_processor.convert(text)

       # Wrap with KaTeX auto-render
       html = f"""
       <!DOCTYPE html>
       <html>
       <head>
           <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
           <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
           <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
           <style>
               body {{ /* ... theme colors ... */ }}
           </style>
       </head>
       <body>
           {html_body}
           <script>
               document.addEventListener("DOMContentLoaded", function() {{
                   renderMathInElement(document.body, {{
                       delimiters: [
                           {{left: "$$", right: "$$", display: true}},
                           {{left: "$", right: "$", display: false}}
                       ]
                   }});
               }});
           </script>
       </body>
       </html>
       """
       return html
   ```

**Offline Bundle**: Package KaTeX library in `src/assets/` and use `qrc` resources.

#### 2.2 Recommendation

**For LunaQt2**: Start with **Option A (QTextBrowser + pykatex)** for these reasons:

1. Lighter weight (no WebEngine)
2. Faster for most use cases
3. Easier theme integration
4. Sufficient for educational math notation

**Upgrade Path**: If users need interactive features later, add Option B as an alternative rendering mode (user preference).

---

### Phase 3: Advanced Features (Future)

#### 3.1 Syntax Highlighting in Code Blocks

Use `Pygments` for syntax highlighting:

```python
# requirements.txt
Pygments>=2.15

# In markdown processor
from markdown.extensions.codehilite import CodeHiliteExtension
self._md_processor = markdown.Markdown(
    extensions=[
        CodeHiliteExtension(
            css_class='highlight',
            pygments_style='monokai'  # Or theme-based
        )
    ]
)
```

#### 3.2 Live Preview While Typing

Add debounced rendering during edit:

```python
from PySide6.QtCore import QTimer

class MarkdownCell(BaseCell):
    def __init__(self, ...):
        super().__init__(...)
        self._preview_timer = QTimer()
        self._preview_timer.setSingleShot(True)
        self._preview_timer.timeout.connect(self._update_preview)
        self._editor.textChanged.connect(self._schedule_preview_update)

    def _schedule_preview_update(self):
        """Debounce preview updates."""
        self._preview_timer.start(500)  # Update after 500ms pause

    def _update_preview(self):
        if self._is_preview_mode:
            content = self._editor.toPlainText()
            self._preview.setHtml(self._render_markdown(content))
```

#### 3.3 Export Features

- Export markdown cell as PDF (using QTextDocument)
- Copy rendered HTML to clipboard
- Export as standalone HTML file

#### 3.4 Markdown Toolbar Enhancements

Add formatting buttons to toolbar:

````python
class MarkdownToolbar(BaseToolbar):
    def __init__(self):
        super().__init__()
        self.add_button("**B**", self._insert_bold, tooltip="Bold")
        self.add_button("*I*", self._insert_italic, tooltip="Italic")
        self.add_button("# H", self._insert_heading, tooltip="Heading")
        self.add_button("[ ]", self._insert_link, tooltip="Link")
        self.add_button("```", self._insert_code_block, tooltip="Code Block")
        self.add_button("$", self._insert_math, tooltip="Inline Math")
        self.add_button("$$", self._insert_display_math, tooltip="Display Math")
        self.add_stretch()
        self.add_button("👁 Preview", self._toggle_preview)
````

---

## Implementation Plan

### Step 1: Basic Markdown (Week 1)

- [ ] Add `markdown` to requirements.txt
- [ ] Port `markdown_cell.py` from OLD_LUNA_QT to `src/interface/qt/widgets/cells/`
- [ ] Replace `_render_markdown()` with proper markdown processor
- [ ] Add theme-aware HTML styling
- [ ] Test with sample markdown (headings, lists, code blocks, links)

### Step 2: Math Support (Week 2)

- [ ] Research and choose: pykatex (Option A) vs WebEngine (Option B)
- [ ] Add KaTeX dependency to requirements
- [ ] Implement KaTeX preprocessor for markdown
- [ ] Bundle KaTeX CSS/fonts for offline use
- [ ] Test inline `$x^2$` and block `$$\int_0^\infty$$` math

### Step 3: Polish (Week 3)

- [ ] Add syntax highlighting with Pygments
- [ ] Implement debounced live preview
- [ ] Add markdown formatting toolbar buttons
- [ ] Add keyboard shortcuts (Ctrl+B for bold, etc.)
- [ ] Test theme switching with rendered markdown
- [ ] Ensure proper font scaling

### Step 4: Documentation (Week 4)

- [ ] Add "Markdown Help" dialog with syntax reference
- [ ] Add "Math Help" dialog with KaTeX examples
- [ ] Update user documentation
- [ ] Create sample notebooks demonstrating features

---

## Testing Strategy

### Unit Tests

```python
# tests/interface/test_markdown_cell.py
def test_markdown_rendering():
    cell = MarkdownCell("test-id", "# Heading\n\nParagraph")
    html = cell._render_markdown(cell.get_content())
    assert "<h1>Heading</h1>" in html
    assert "<p>Paragraph</p>" in html

def test_inline_math():
    cell = MarkdownCell("test-id", "Inline $x^2$ math")
    html = cell._render_markdown(cell.get_content())
    assert "katex" in html.lower()

def test_block_math():
    cell = MarkdownCell("test-id", "Block:\n$$\\int_0^1 x dx$$")
    html = cell._render_markdown(cell.get_content())
    assert "katex-block" in html or "display" in html
```

### Manual Testing Checklist

- [ ] Markdown renders correctly (headers, lists, code, links, images)
- [ ] Inline math renders: `$\alpha + \beta$`
- [ ] Block math renders: `$$\sum_{i=1}^n i = \frac{n(n+1)}{2}$$`
- [ ] Theme switching updates markdown colors
- [ ] Font changes apply to rendered text
- [ ] Edit/Preview toggle works smoothly
- [ ] Long markdown documents scroll properly
- [ ] Math errors display helpful messages
- [ ] Works offline (no network required)

---

## Dependencies Summary

### Minimal Setup (Option A - Recommended)

```
PySide6>=6.7
matplotlib>=3.0
markdown>=3.5
pykatex>=0.1.3          # For KaTeX math rendering
Pygments>=2.15          # For syntax highlighting (optional)
```

### Full Setup (Option B - WebEngine)

```
PySide6>=6.7
PySide6-WebEngine>=6.7  # ~100MB additional
matplotlib>=3.0
markdown>=3.5
Pygments>=2.15
```

**Recommendation**: Start with Option A, defer Option B unless users specifically need interactive math features.

---

## Architecture Considerations

### Cell Type Hierarchy

```
BaseCell
├── PythonCell (code execution)
├── MarkdownCell (markdown + math)
└── RawCell (plain text) [future]
```

### Rendering Service Pattern (Optional)

For better separation of concerns, consider a rendering service:

```python
# src/core/rendering/markdown_renderer.py
class MarkdownRenderer:
    """Service for rendering markdown with math support."""

    def __init__(self):
        self._md = markdown.Markdown(extensions=[...])

    def render(self, text: str, theme: dict) -> str:
        """Render markdown to themed HTML."""
        ...

    def render_to_pdf(self, text: str, filepath: str):
        """Export markdown as PDF."""
        ...

# Usage in cell
class MarkdownCell(BaseCell):
    def __init__(self, ...):
        from src.core.rendering import get_markdown_renderer
        self._renderer = get_markdown_renderer()

    def _render_markdown(self, text: str) -> str:
        theme = self._get_theme_dict()
        return self._renderer.render(text, theme)
```

**Benefits**:

- Testable in isolation
- Shared across multiple components
- Easier to swap implementations
- Can be extended with caching

---

## Known Challenges & Solutions

### Challenge 1: Math Rendering Performance

**Problem**: KaTeX rendering can be slow for large documents with many equations.

**Solutions**:

- Cache rendered HTML for unchanged cells
- Lazy render (only render visible cells)
- Use pykatex (C binding) instead of pure Python

### Challenge 2: Theme Integration

**Problem**: KaTeX CSS might not respect app themes.

**Solutions**:

- Override KaTeX CSS with theme colors
- Generate dynamic CSS based on current palette
- Use SVG rendering (theme-aware colors)

### Challenge 3: Offline Operation

**Problem**: CDN links won't work without internet.

**Solutions**:

- Bundle KaTeX assets in app package
- Use Qt Resource System (qrc) for assets
- Check internet, fallback to bundled assets

### Challenge 4: Font Rendering

**Problem**: Math fonts might look inconsistent with app fonts.

**Solutions**:

- Use KaTeX's bundled math fonts
- Ensure proper font fallback in CSS
- Match code font to app's code font setting

---

## References

### Libraries

- **Python-Markdown**: https://python-markdown.github.io/
- **PyKaTeX**: https://github.com/mbarkhau/pykatex
- **KaTeX**: https://katex.org/
- **Pygments**: https://pygments.org/

### Qt Documentation

- **QTextBrowser**: https://doc.qt.io/qt-6/qtextbrowser.html
- **QWebEngineView**: https://doc.qt.io/qt-6/qwebengineview.html

### Inspiration

- **Jupyter Notebook**: Markdown + LaTeX rendering patterns
- **Typora**: Live markdown editor
- **Obsidian**: Markdown with math support

---

## Summary & Action Items

### **Recommended Path (Phased Approach)**

#### 🚀 **MVP Phase (Do First - 2 weeks)**

1. **✅ Add dependencies to `requirements.txt`**

   ```python
   markdown>=3.5
   pykatex>=0.1.3
   ```

2. **✅ Port markdown cell structure**
   - Copy `markdown_cell.py` from OLD_LUNA_QT to `src/interface/qt/widgets/cells/`
   - Keep `_MarkdownEditor` and `_MarkdownPreview` classes
   - Maintain edit/preview toggle pattern

3. **✅ Replace basic rendering with proper markdown**
   - Initialize `markdown.Markdown()` processor in `__init__`
   - Use extensions: `extra`, `nl2br`, `sane_lists`
   - Generate theme-aware HTML with palette colors

4. **✅ Add KaTeX math support**
   - Implement `KaTeXPreprocessor` to convert `$...$` and `$$...$$` to HTML
   - Use `pykatex.render()` for LaTeX-to-HTML conversion
   - Include KaTeX CSS in HTML template

5. **✅ Bundle KaTeX assets for offline**
   - Download KaTeX CSS and fonts to `src/assets/katex/`
   - Reference locally: `file:///.../katex.min.css`
   - No internet required for rendering

#### 🎨 **Polish Phase (Do Second - 1-2 weeks)**

6. **⏭️ Add syntax highlighting**
   - Install Pygments: `pip install Pygments>=2.15`
   - Add `codehilite` extension to markdown processor
   - Use theme-based color scheme (monokai for dark, vs for light)

7. **⏭️ Enhance markdown toolbar**
   - Add formatting buttons: Bold, Italic, Heading, Link, Code
   - Add math buttons: Inline Math (`$...$`), Display Math (`$$...$$`)
   - Implement keyboard shortcuts (Ctrl+B, Ctrl+I, etc.)

8. **⏭️ Add debounced live preview (optional)**
   - Use `QTimer` with 500ms delay
   - Update preview automatically while typing
   - Only if performance is acceptable

#### 🔮 **Future Enhancements (Defer)**

9. **⏭️ Consider Qt WebEngine (only if needed)**
   - Add as user preference option
   - Only implement if users need interactive/copyable math
   - Trade-off: +100MB dependency for minimal benefit

10. **⏭️ Export features**
    - Export cell to PDF using `QTextDocument.print()`
    - Copy rendered HTML to clipboard
    - Export as standalone HTML file

11. **⏭️ Advanced markdown features**
    - Task lists: `- [ ] Todo item`
    - Footnotes: `[^1]`
    - Definition lists
    - Table of contents generation

### **Why This Order?**

1. **MVP First**: Get working markdown + math quickly (core value)
2. **Polish Next**: Improve UX once basics work (usability)
3. **Defer Heavy Features**: WebEngine adds complexity without proportional value

### **Success Metrics**

✅ **MVP is complete when:**

- Users can write markdown with headers, lists, links, code blocks
- Inline math `$\alpha + \beta$` renders correctly
- Block math `$$\sum_{i=1}^n i$$` renders correctly
- Theme switching updates markdown colors
- Works completely offline (no CDN dependencies)

✅ **Polish is complete when:**

- Code blocks have syntax highlighting
- Toolbar buttons insert markdown/math syntax
- Performance is smooth (no lag on typing)
- Help documentation is available

### **Decision Tree: When to Add WebEngine?**

```
Does user need...
├─ Copy math as LaTeX? → No, pykatex sufficient
├─ Interactive equations? → No, pykatex sufficient
├─ 3D plots in cells? → Maybe, consider WebEngine
├─ JSXGraph geometry? → Yes, need WebEngine
└─ JavaScript cells? → Yes, need WebEngine
```

**Current Recommendation**: Stick with `QTextBrowser` + `pykatex` unless geometry/JS cells are planned.

### **Risk Assessment**

| Risk                       | Likelihood | Impact | Mitigation                        |
| -------------------------- | ---------- | ------ | --------------------------------- |
| pykatex installation fails | Low        | Medium | Document manual install steps     |
| Math rendering too slow    | Low        | Medium | Add caching, lazy rendering       |
| Theme colors not applied   | Low        | Low    | Override KaTeX CSS with palette   |
| Offline bundle too large   | Low        | Low    | Only include needed KaTeX fonts   |
| Users want WebEngine       | Medium     | Low    | Add as alternative renderer later |

### **Final Recommendation**

**🎯 Start with lightweight approach (QTextBrowser + pykatex):**

- Implement markdown + math in 2-3 weeks
- Get user feedback before adding WebEngine
- Defer advanced features until core is solid
- Maintain clean separation for easy upgrades

This strategy balances functionality, performance, and maintainability while providing a clear upgrade path for advanced features if needed.
