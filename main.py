"""Entry-point."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

# Ensure the local "src" directory is importable when running from the repo root.
PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
if SRC_DIR.exists() and str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

try:
    from PySide6.QtCore import qInstallMessageHandler
    from PySide6.QtWidgets import QApplication
except ModuleNotFoundError as exc:  # pragma: no cover - import guard
    raise SystemExit("PySide6 must be installed to run LunaQt2.") from exc

from interface.qt.styling import apply_global_style, build_application_qss
from interface.qt.styling.theme import StylePreferences, ThemeMode
from interface.qt.windows import LunaQtWindow
from shared.constants import (
    BUNDLED_FONTS,
    DEFAULT_THEME_MODE,
    DEFAULT_UI_FONT_POINT_SIZE,
    clamp_ui_font_point_size,
)
from shared.utils.font_loader import load_bundled_fonts


def qt_handler(mode, context, message):  # pragma: no cover - debug helper
    print("QT:", message)


AVAILABLE_UI_FONT_FAMILIES: Sequence[str] = tuple(BUNDLED_FONTS)
if not AVAILABLE_UI_FONT_FAMILIES:
    raise SystemExit("No bundled UI fonts configured. Add entries to assets.fonts.font_lists.BUNDLED_FONTS.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the LunaQt2 window")
    parser.add_argument(
        "--mode",
        choices=[mode.value for mode in ThemeMode],
        default=DEFAULT_THEME_MODE.value,
        help="Theme mode to use when applying the stylesheet",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    mode = ThemeMode(args.mode)
    ui_font_point_size = clamp_ui_font_point_size(DEFAULT_UI_FONT_POINT_SIZE)
    default_ui_family = AVAILABLE_UI_FONT_FAMILIES[0]
    style_preferences = StylePreferences(
        ui_font_size=ui_font_point_size,
        ui_font_family=default_ui_family,
    )
    initial_metrics = style_preferences.build_metrics()

    app = QApplication(sys.argv)
    load_bundled_fonts()
    qInstallMessageHandler(qt_handler)
    # Debug: dump the exact stylesheet string Qt will parse
    try:
        qss_dump = build_application_qss(mode=mode, metrics=initial_metrics)
        with open("qss_runtime_dump.txt", "w", encoding="utf-8") as f:
            f.write(qss_dump)
    except Exception as e:  # pragma: no cover - debug only
        print("Error while dumping runtime QSS:", e)

    apply_global_style(app, mode=mode, metrics=initial_metrics)

    window = LunaQtWindow(
        app,
        mode,
        ui_font_choices=AVAILABLE_UI_FONT_FAMILIES,
        style_preferences=style_preferences,
    )
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
