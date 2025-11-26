# QtLayoutAndStylingTemplate

Opinionated template showing how to structure PySide6 styling so that colors, metrics, and widget rules live in predictable modules. The high-level goals:

- Keep the palette and spacing tokens in a single place (`theme/colors.py`).
- Give every widget type its own QSS generator so styles never bleed across widget variants.
- Scope rules via `objectName` and dynamic properties (`btnType`, `cellType`, etc.).
- Provide a global loader that stitches together all QSS and applies it to the `QApplication`.

## Project layout

```
src/
└── qtstylingtemplate/
	├── theme/
	│   └── colors.py         # Palette + metrics definitions
	├── widgets/
	│   ├── buttons.py       # QPushButton variants, dynamic property scoped
	│   ├── main_menubar.py  # QMenuBar and QMenu rules
	│   ├── statusbar.py     # QStatusBar styles
	│   ├── cell_container.py # Container/editor chrome
	│   └── cell_gutter.py   # Line-number gutter styling
	└── style_loader.py      # Aggregates widget QSS and applies globally
```

Each widget module exposes a single `get_qss()` function. The loader imports them, concatenates their strings, and exposes two helpers:

- `qtstylingtemplate.build_application_qss()` – returns the full stylesheet string (handy for testing or debugging).
- `qtstylingtemplate.apply_global_style(app)` – immediately sets the stylesheet on the provided `QApplication`.

## Using the loader

```python
from PySide6.QtWidgets import QApplication

from qtstylingtemplate import apply_global_style


def main() -> None:
	app = QApplication([])
	apply_global_style(app)
	...  # create windows
	app.exec()


if __name__ == "__main__":
	main()
```

To control which style a widget receives, set its `objectName` or dynamic properties:

```python
button.setProperty("btnType", "primary")
menu_bar.setObjectName("MainMenuBar")
status_bar.setObjectName("MainStatusBar")
```

That keeps the QSS selectors precise and prevents unintended overrides of other Qt widgets.
