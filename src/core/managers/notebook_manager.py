"""Notebook lifecycle coordination and cell ordering."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from core.persistence import DataStore
from shared.utils.id_generator import generate_notebook_id


class NotebookManager:
    """Manage notebooks and their ordered list of cell identifiers."""

    def __init__(self, store: DataStore) -> None:
        self._store = store
        self._active_notebook_id: str | None = None

    def create_notebook(self, title: str) -> str:
        notebook_id = generate_notebook_id()
        now = datetime.now(timezone.utc).isoformat()

        notebook_data = {
            "notebook_id": notebook_id,
            "title": title,
            "cell_ids": [],
            "metadata": {
                "kernel": "python3",
                "language": "python",
                "author": "",
                "tags": [],
            },
            "created_at": now,
            "modified_at": now,
            "schema_version": 1,
        }

        self._store.save_notebook(notebook_data)
        return notebook_id

    def open_notebook(self, notebook_id: str) -> dict[str, Any] | None:
        data = self._store.load_notebook(notebook_id)
        if data:
            self._active_notebook_id = notebook_id
        return data

    def close_notebook(self, notebook_id: str, *, save: bool = True) -> bool:
        if save:
            data = self._store.load_notebook(notebook_id)
            if data:
                self.save_notebook(notebook_id)

        if self._active_notebook_id == notebook_id:
            self._active_notebook_id = None
        return True

    def save_notebook(self, notebook_id: str) -> bool:
        data = self._store.load_notebook(notebook_id)
        if not data:
            return False

        data["modified_at"] = datetime.now(timezone.utc).isoformat()
        return self._store.save_notebook(data)

    def add_cell(self, notebook_id: str, cell_id: str, position: int = -1) -> bool:
        data = self._store.load_notebook(notebook_id)
        if not data:
            return False

        cell_ids = list(data.get("cell_ids", []))
        if position == -1 or position >= len(cell_ids):
            cell_ids.append(cell_id)
        else:
            cell_ids.insert(position, cell_id)

        data["cell_ids"] = cell_ids
        return self._store.save_notebook(data)

    def remove_cell(self, notebook_id: str, cell_id: str) -> bool:
        data = self._store.load_notebook(notebook_id)
        if not data:
            return False

        cell_ids = list(data.get("cell_ids", []))
        if cell_id not in cell_ids:
            return False

        cell_ids.remove(cell_id)
        data["cell_ids"] = cell_ids
        return self._store.save_notebook(data)

    def move_cell(self, notebook_id: str, cell_id: str, new_position: int) -> bool:
        data = self._store.load_notebook(notebook_id)
        if not data:
            return False

        cell_ids = list(data.get("cell_ids", []))
        if cell_id not in cell_ids:
            return False

        cell_ids.remove(cell_id)
        cell_ids.insert(new_position, cell_id)

        data["cell_ids"] = cell_ids
        return self._store.save_notebook(data)

    def get_cell_order(self, notebook_id: str) -> list[str]:
        data = self._store.load_notebook(notebook_id)
        if not data:
            return []
        return list(data.get("cell_ids", []))

    def get_active_notebook_id(self) -> str | None:
        return self._active_notebook_id

    def list_notebooks(self) -> list[dict[str, Any]]:
        return self._store.list_notebooks()

    def rename_notebook(self, notebook_id: str, new_title: str) -> bool:
        new_title = new_title.strip()
        if not new_title:
            return False

        data = self._store.load_notebook(notebook_id)
        if not data:
            return False

        data["title"] = new_title
        data["modified_at"] = datetime.now(timezone.utc).isoformat()
        return self._store.save_notebook(data)

    def delete_notebook(self, notebook_id: str) -> bool:
        if not notebook_id:
            return False

        deleted = self._store.delete_notebook(notebook_id)
        if deleted and self._active_notebook_id == notebook_id:
            self._active_notebook_id = None
        return deleted


__all__ = ["NotebookManager"]
