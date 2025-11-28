"""Utilities for loading fonts bundled with the application."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence

FONT_EXTENSIONS: Sequence[str] = (".ttf", ".otf")
IGNORE_DIRECTORIES = {"temp-font-downloads", "__pycache__"}


def _iter_font_files(root: Path) -> Iterable[Path]:
    for entry in root.iterdir():
        if not entry.is_dir() or entry.name in IGNORE_DIRECTORIES or entry.name.startswith('.'):
            continue
        for font_file in entry.rglob("*"):
            if font_file.is_file() and font_file.suffix.lower() in FONT_EXTENSIONS:
                yield font_file


def load_bundled_fonts(font_root: Path | None = None) -> list[str]:
    """Register bundled fonts with Qt's font database."""

    try:
        from PySide6.QtGui import QFontDatabase
    except ModuleNotFoundError:
        return []

    src_dir = Path(__file__).resolve().parents[2]
    default_root = src_dir / "assets" / "fonts"
    root = font_root or default_root
    if not root.exists():
        return []

    loaded_families: list[str] = []
    for font_path in _iter_font_files(root):
        font_id = QFontDatabase.addApplicationFont(str(font_path))
        if font_id == -1:
            continue
        loaded_families.extend(QFontDatabase.applicationFontFamilies(font_id))
    return loaded_families


__all__ = ["load_bundled_fonts"]
