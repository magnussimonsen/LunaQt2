# LunaQt2

LunaQt2 with a better, cleaner UI codebase. Modular styling, scoped tokens, and a maintained QSS pipeline power Python, Markdown (with LaTeX), and CAS workflows.

## Core Features

- **Python editor cells**: run code inline with outputs rendered in context.
- **Markdown cells**: rich Markdown with KaTeX/LaTeX support for beautiful math equations.
  - Standard markdown: headings, bold, italic, lists, tables, links, code blocks
  - Inline math: `$x^2 + y^2 = z^2$`
  - Block math: `$$\int_0^1 x dx = \frac{1}{2}$$`
  - Syntax highlighting: Python, JavaScript, Java, C++, and 100+ languages
  - Theme-aware: automatically adapts to light/dark mode
- **CAS cells**: computer algebra system integrations for symbolic math.
- **Improved UI codebase**: cleaner styling pipeline, component-scoped tokens, and modular QSS generation.

## UI Architecture

- Theme system: centralized palettes (`bg`, `border`, `text`, `menu`, `statusbar`) with light/dark modes.
- Widget tokens: per-widget spacing and border tokens (menubar, main toolbar, sidebar toolbar, sidebars, statusbar, buttons).
- Scoped styles: QSS modules in `src/interface/qt/styling/widget_styles/` (e.g., `main_menubar.py`, `main_toolbar.py`).
- Toolbar separation: distinct tokens and styles for the main toolbar vs. sidebar toolbars.

## Project Layout

```
LunaQt2/
├─ main.py
├─ src/
│  ├─ app/
│  ├─ core/
│  ├─ interface/qt/
│  │  ├─ windows/
│  │  ├─ styling/
│  │  │  ├─ theme/
│  │  │  └─ widget_styles/
│  ├─ shared/
│  └─ assets/
└─ README.md
```

## Getting Started

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py --mode dark
```

### Dependencies

- **PySide6** >= 6.7 - Qt for Python framework
- **markdown** >= 3.5 - Markdown parsing with extensions
- **pykatex** >= 0.1.1 - KaTeX math rendering
- **Pygments** >= 2.15 - Syntax highlighting for code blocks

### Quick Start with Markdown

See [MARKDOWN_QUICKSTART.md](MARKDOWN_QUICKSTART.md) for a comprehensive guide to using markdown cells with math notation.

Example markdown cell content:

```markdown
# My Notebook

The quadratic formula is $x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$.

$$
E = mc^2
$$
```

## Status

Active development: implementing cell runtimes, Markdown + LaTeX rendering, and CAS adapters, while refining the UI styling system.

### Recent Updates

- ✅ **Markdown & KaTeX Implementation** - Full markdown rendering with math support
  - Server-side rendering using pykatex (no Qt WebEngine needed)
  - Theme-aware styling with automatic color injection
  - Syntax highlighting for code blocks
  - See [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) for details

### Documentation

- [MARKDOWN_QUICKSTART.md](MARKDOWN_QUICKSTART.md) - Quick start guide for markdown cells
- [MARKDOWN_EXAMPLE.md](MARKDOWN_EXAMPLE.md) - Comprehensive examples with math and formatting
- [MARKDOWN_KATEX_STRATEGY.md](MARKDOWN_KATEX_STRATEGY.md) - Original implementation strategy
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Implementation details and architecture
