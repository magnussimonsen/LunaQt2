# LunaQt2

LunaQt2 with a better, cleaner UI codebase. Modular styling, scoped tokens, and a maintained QSS pipeline power Python, Markdown (with LaTeX), and CAS workflows.

## Core Features
- Python editor cells: run code inline with outputs rendered in context.
- Markdown cells: rich Markdown with KaTeX/LaTeX support.
- CAS cells: computer algebra system integrations for symbolic math.
- Improved UI codebase: cleaner styling pipeline, component-scoped tokens, and modular QSS generation.

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
source .venv/bin/activate
pip install -r requirements.txt
python main.py --mode dark
```

## Status
Active development: implementing cell runtimes, Markdown + LaTeX rendering, and CAS adapters, while refining the UI styling system.
