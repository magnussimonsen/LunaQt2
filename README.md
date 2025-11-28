# LunaQt2

LunaQt2 is a PySide6 playground for experimenting with notebook-inspired layouts, sidebars, and a modern QSS-driven theme system. The current focus is cleaning up the architecture so that UI concerns live under `interface/qt` while future data/model logic grows inside `app/` and `core/`.

## Requirements

- Python 3.11 (matching the `.venv` that ships with the project)
- PySide6 + dependencies from `requirements.txt`
- Windows 10/11 is the primary target today, but nothing prevents Linux/macOS once PySide6 is available

## Getting Started

1. Create and activate a virtual environment (skip if you already use `.venv`):
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Run the sample UI:
   ```powershell
   python main.py --mode dark   # or omit flag for light mode
   ```
4. Fonts bundled in `assets/fonts` load automatically at startup. If you add new families make sure they are referenced inside `assets/fonts/font_lists.py` so `shared.constants.BUNDLED_FONTS` stays in sync.

## Project Layout

```
LunaQt2/
├─ main.py                    # Thin CLI/bootstrap, hands off to interface.qt
├─ src/
│  ├─ app/                    # Future bootstrap, controllers, state adapters
│  ├─ core/                   # Qt-free business logic, managers, persistence
│  ├─ interface/qt/           # Windows, widgets, menus, styling, sidebars
│  ├─ shared/                 # Constants, utilities, shared types
│  └─ assets/                 # Fonts and UI assets consumed at runtime
└─ README.md
```

### Layering Highlights

- `app/` will eventually host bootstrap helpers (argument parsing, runtime wiring) so `main.py` can shrink to a trivial shim.
- `core/` is the staging area for notebook, cell, and execution managers that must not depend on Qt.
- `interface/qt/` contains everything PySide6-specific: `windows/`, `widgets/`, `menus/`, `sidebars/`, plus the styling pipeline under `styling/`.
- `shared/` holds configuration constants (typography, sidebar sizing, theme defaults) and utilities (font loader, id helpers, color converters) that any layer can reuse.

### Styling Pipeline

1. `interface.qt.styling.theme` defines `ThemeMode`, palettes, metrics, and token objects.
2. `interface.qt.styling.widget_styles` generates modular QSS snippets for buttons, sidebars, status bars, etc.
3. `interface.qt.styling.qss_builder` assembles the modules into a single stylesheet and exposes `build_application_qss` plus `apply_global_style`.
4. `main.py` (and eventually `app/bootstrap.py`) calls `apply_global_style` whenever the theme or typography metrics change.

During development you can dump the exact QSS string that Qt receives by checking `qss_runtime_dump.txt`, which is written every time the app boots.

## Contributing / Next Steps

- Continue migrating legacy modules from `TRASH_BIN`/old folders into `app/`, `core/`, or `interface/qt` depending on their responsibility.
- Replace the placeholder `AppState` with a real state manager once the notebook/core logic is ready.
- Wire up controllers inside `app/` so `main.py` only parses CLI arguments before handing off to the bootstrap layer.

Issues and experiments can be tracked in `ClaudeSonnet45_help.txt` / `ChatGPT5.txt` while the architecture firms up.
