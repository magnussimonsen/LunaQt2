"""JSON persistence layer for notebooks and cells."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:  # pragma: no cover - Qt may be unavailable during tests
    from PySide6.QtCore import QStandardPaths
except ModuleNotFoundError:  # pragma: no cover - fallback path will be used
    QStandardPaths = None  # type: ignore[assignment]


class DataStore:
    """Handle notebook and cell persistence using JSON files."""

    def __init__(self, root_dir: Path | str | None = None) -> None:
        self._data_dir = self._resolve_root(root_dir)
        self._notebooks_dir = self._data_dir / "notebooks"
        self._cells_dir = self._data_dir / "cells"

        self._notebooks_dir.mkdir(parents=True, exist_ok=True)
        self._cells_dir.mkdir(parents=True, exist_ok=True)

    def load_notebook(self, notebook_id: str) -> dict[str, Any] | None:
        file_path = self._notebooks_dir / f"{notebook_id}.json"
        if not file_path.exists():
            return None

        try:
            with file_path.open("r", encoding="utf-8") as handle:
                return json.load(handle)
        except (json.JSONDecodeError, OSError):
            return None

    def save_notebook(self, notebook_data: dict[str, Any]) -> bool:
        notebook_id = notebook_data.get("notebook_id")
        if not notebook_id:
            return False

        file_path = self._notebooks_dir / f"{notebook_id}.json"
        return self._atomic_write(file_path, notebook_data)

    def load_cell(self, cell_id: str) -> dict[str, Any] | None:
        file_path = self._cells_dir / f"{cell_id}.json"
        if not file_path.exists():
            return None

        try:
            with file_path.open("r", encoding="utf-8") as handle:
                return json.load(handle)
        except (json.JSONDecodeError, OSError):
            return None

    def save_cell(self, cell_data: dict[str, Any]) -> bool:
        cell_id = cell_data.get("cell_id")
        if not cell_id:
            return False

        file_path = self._cells_dir / f"{cell_id}.json"
        return self._atomic_write(file_path, cell_data)

    def delete_notebook(self, notebook_id: str) -> bool:
        file_path = self._notebooks_dir / f"{notebook_id}.json"
        try:
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except OSError:
            return False

    def delete_cell(self, cell_id: str) -> bool:
        file_path = self._cells_dir / f"{cell_id}.json"
        try:
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except OSError:
            return False

    def list_notebooks(self) -> list[dict[str, Any]]:
        notebooks: list[dict[str, Any]] = []
        for file_path in self._notebooks_dir.glob("*.json"):
            data = self.load_notebook(file_path.stem)
            if data:
                notebooks.append(data)
        return notebooks

    @property
    def data_root(self) -> Path:
        """Return the root directory used for persistence (mainly for tests)."""

        return self._data_dir

    def _resolve_root(self, root_dir: Path | str | None) -> Path:
        if root_dir is not None:
            return Path(root_dir).expanduser()

        if QStandardPaths is not None:  # pragma: no branch - trivial check
            location = QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.AppDataLocation
            )
            if location:
                return Path(location).expanduser() / "LunaQt"

        # Fallback to a hidden directory inside the user's home folder
            return Path.home() / ".lunaqt"

    def _atomic_write(self, file_path: Path, data: dict[str, Any]) -> bool:
        temp_path = file_path.with_suffix(".tmp")
        try:
            with temp_path.open("w", encoding="utf-8") as handle:
                json.dump(data, handle, indent=2, ensure_ascii=False)

            temp_path.replace(file_path)
            return True
        except (OSError, TypeError):
            if temp_path.exists():
                try:
                    temp_path.unlink()
                except OSError:
                    pass
            return False


__all__ = ["DataStore"]
