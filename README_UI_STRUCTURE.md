# LunaQt2 UI Structure

This document summarizes the main UI layout, styling pipeline, and interaction flow of the LunaQt2 app.

## Styling Data Flow

```
User action (theme toggle, font change)
    ↓
StylePreferences (ui_font_family, ui_font_size)
    ↓
Metrics (padding, spacing, radii, font_size_*)
    ↓
Theme (resolved colors + metrics)
    ↓
QSS string (via style_loader + widget modules)
    ↓
QApplication.setStyleSheet()
```

## High-level Layout

- **Main Window (`LunaQtWindow`)**
  - Central notebook cell list
  - Right-side docked sidebars (Notebooks, Settings)
  - Top menubar + corner buttons
  - Top toolbar
  - Bottom status bar

## Menubar

- **File**
  - New
  - Save
  - Save As…
- **Edit** (placeholders, not wired yet)
  - Move Cell Up
  - Move Cell Down
  - — separator —
  - Delete Cell
  - Delete Notebook
- **View**
  - Light Mode (toggle)
  - Dark Mode (toggle)
- **Corner buttons (right side of menubar)**
  - Move cell up / Move cell down (placeholders, no logic yet)
  - Notebooks (toggle sidebar)
  - Settings (toggle sidebar)

## Toolbar
The toolbar buttons must change depending on witch cell typs user has selected.
If user has  python cell selected, the buttons should be: 
- "Run" If pressed, the code in python cell is run. When python code is running, this button is disabled
- "Stop" If pressed, the python running is stoped. Button is disabled iff Run button is disabled
If user has markdown cell selected, the buttons should be:
- "Preview" Toogle on/off button. If on, shows preview of rendered markdown and latex. If off, shows markdown and $latex$ code

Current implementation only has theese buttons for all cell types. I do not think logic for automatic swiching of toolbar type to match user selected cell type is implemented. It is implemented in OLD_LUNA_QT, so we may look there for tips on how to implement it
- **Primary** button (`btnType="primary"`)
- **Toolbar** button (`btnType="toolbar"`)
- **Warn** button (`btnType="warning"`)

Toolbar buttons are mainly styling examples and are not connected to notebook logic.

## Central Content

- **Cell List** (`cellType="list"`)
  - Vertical list of `CellRow` widgets.
  - Each row has:
    - Left gutter (`cellType="gutter"`) with line number.
    - Right container frame (`cellType="container"`) with:
      - Header label (`cellPart="header"`).
      - Body label (`cellPart="body"`).
- **Selection behavior**
  - Clicking a cell body selects that row.
  - Clicking the gutter toggles selection.

## Sidebars

- **Notebooks Sidebar** (`QDockWidget#NotebooksDock`)
  - Initially hidden, toggled by Notebooks button.
  - Placeholder for future notebook list UI.

- **Settings Sidebar** (`QDockWidget#SettingsDock`)
  - Initially hidden, toggled by Settings button.
  - Contains `SettingsSidebarWidget` with typography controls:
    - UI font family selector (bundled fonts only).
    - UI font size spinbox (with styled up/down buttons).
  - Emits signals that update global UI metrics and reapply the QSS.

## Status Bar

- **Main Status Bar** (`MainStatusBar`)
  - Left: "Ready" message.
  - Right: "Unsaved changes" warning label (`statusRole="warning"`).

## Styling Pipeline & Code Wiring

- **Entry point (`main.py`)**
  - Ensures `src/` is added to `sys.path` so local packages resolve.
  - Imports `apply_global_style` from `style_loader`, `ThemeMode`/`Theme` from `theme`, and `StylePreferences`/`Metrics` from `theme.preferences` / `theme.metrics`.
  - Builds `StylePreferences` from constants (`DEFAULT_UI_FONT_POINT_SIZE`, `BUNDLED_FONTS`) and converts them to a `Metrics` instance.
  - Calls `load_bundled_fonts()` so only packaged fonts are used in the UI.
  - Calls `apply_global_style(app, mode=..., metrics=...)` at startup, and `_apply_current_style()` whenever theme or typography changes.

- **Theme and metrics (`src/theme`)**
  - `colors.py` defines mode-aware tokens for backgrounds, borders, text, buttons, menus, and status bar.
  - `metrics.py` defines padding, spacing, radii, and font sizes; combined with color tokens into a resolved `Theme` via `get_theme(mode, metrics)`.
  - `preferences.py` exposes `StylePreferences`, which wraps user-facing typography controls and can build a `Metrics` object.

- **Global QSS assembly (`src/style_loader.py`)**
  - Imports `Theme`, `ThemeMode`, `Metrics`, and widget style modules: `widgets.buttons`, `widgets.cell_container`, `widgets.cell_gutter`, `widgets.main_menubar`, `widgets.sidebars`, `widgets.statusbar`.
  - `_base_style(theme)` generates the *global* `QWidget` rule (app background, default font from metrics) and foundational dock/toolbar selectors—widget modules handle *specific* selectors like `QPushButton[btnType="..."]` or `QMenuBar#MainMenuBar`.
  - Each widget module exposes `get_qss(mode, theme)`, returning a QSS block scoped to its widget type.
  - `build_application_qss(mode, metrics)` concatenates `_base_style` + all widget QSS blocks into a single stylesheet string.
  - `apply_global_style(app, ...)` applies that stylesheet to the `QApplication`.
  - **Debugging tip**: `main.py` writes the full QSS to `qss_runtime_dump.txt` at startup—inspect this file to verify selector specificity or diagnose styling issues.

- **Widget-specific styling (`src/widgets`)**
  - `buttons.py` styles `QPushButton` variants, keyed by `btnType` dynamic property (`primary`, `menubar`, `toolbar`, `warning`) and uses `theme.buttons.*` palettes + metrics.
  - `main_menubar.py` styles `QMenuBar#MainMenuBar` and `QMenu[menuRole="primary"]`, using `theme.menu`, `theme.bg`, and menubar spacing tokens.
  - `sidebars.py` styles `QDockWidget#NotebooksDock` / `#SettingsDock`, their title bars, content backgrounds, list widgets, combo boxes, and spin boxes, using `theme.bg.sidebar_*`, `theme.border`, `theme.text`, and `sidebar_tokens(metrics)`.
  - `cell_container.py`, `cell_gutter.py`, and `statusbar.py` style the notebook cell chrome and status bar based on `objectName` and `cellType` / `cellPart` / `statusRole` properties set in `main.py`.

- **UI widgets (`src/ui`)**
  - `ui/sidebars/settings_sidebar.py` builds the Settings sidebar form and emits `ui_font_size_changed` / `ui_font_family_changed` signals.
  - `main.py` listens for these signals, updates `StylePreferences`, rebuilds `Metrics`, and calls `_apply_current_style()` so the QSS reflects the current font choices.

## Design Principles

- **Bundled fonts only**: All fonts are packaged under `src/assets/fonts/` and loaded via `load_bundled_fonts()` at startup to ensure consistent rendering across systems. The Settings sidebar restricts choices to `BUNDLED_FONTS`.

- **Dynamic property contract**: Widget styling relies on properties set in `main.py`:
  - `btnType`: `"primary"`, `"menubar"`, `"toolbar"`, `"warning"` (buttons)
  - `cellType`: `"list"`, `"gutter"`, `"container"` (notebook cells)
  - `cellPart`: `"header"`, `"body"` (cell labels)
  - `cellRole`: `"line-number"` (gutter label)
  - `sidebarRole`: `"toolbar"`, `"content"`, `"action-row"` (sidebar sections)
  - `statusRole`: `"warning"` (status bar labels)
  - `menuRole`: `"primary"` (dropdown menus)
  - `widgetRole`: `"menubar-corner"` (menubar corner widget)

- **State refresh for checkable widgets**: Qt caches style evaluation based on widget state. For checkable buttons (like Notebooks/Settings toggles), `_refresh_button_style(button)` calls `unpolish()` → `polish()` → `update()` to force Qt to re-evaluate the `:checked` pseudo-class and apply the correct background color.

This structure keeps layout, theming, and per-widget styling separated but tightly wired, so changes to palettes or metrics propagate consistently across the UI.