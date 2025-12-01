"""Cell lifecycle management built on top of the persistence layer."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from core.persistence import DataStore
from shared.utils.id_generator import generate_cell_id


class CellManager:
    """Create, read, update, and delete notebook cells."""

    def __init__(self, store: DataStore) -> None:
        self._store = store

    def create_cell(
        self,
        cell_type: str,
        *,
        content: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> str:
        cell_id = generate_cell_id()
        now = datetime.now(timezone.utc).isoformat()

        resolved_metadata: dict[str, Any] = metadata.copy() if metadata else {}

        if cell_type == "code":
            resolved_metadata.setdefault("execution_count", None)
            resolved_metadata.setdefault("language", "python")
        elif cell_type == "markdown":
            resolved_metadata.setdefault("language", "markdown")
        else:
            resolved_metadata.setdefault("language", cell_type)

        resolved_metadata.setdefault("collapsed", False)
        resolved_metadata.setdefault("tags", [])

        cell_data = {
            "cell_id": cell_id,
            "cell_type": cell_type,
            "content": content,
            "metadata": resolved_metadata,
            "outputs": [],
            "created_at": now,
            "modified_at": now,
            "schema_version": 1,
        }

        self._store.save_cell(cell_data)
        return cell_id

    def get_cell(self, cell_id: str) -> dict[str, Any] | None:
        return self._store.load_cell(cell_id)

    def update_cell(
        self,
        cell_id: str,
        *,
        content: str | None = None,
        metadata: dict[str, Any] | None = None,
        outputs: list[dict[str, Any]] | None = None,
    ) -> bool:
        cell_data = self._store.load_cell(cell_id)
        if not cell_data:
            return False

        if content is not None:
            cell_data["content"] = content

        if metadata is not None:
            cell_data["metadata"].update(metadata)

        if outputs is not None:
            cell_data["outputs"] = outputs

        cell_data["modified_at"] = datetime.now(timezone.utc).isoformat()
        return self._store.save_cell(cell_data)

    def delete_cell(self, cell_id: str) -> bool:
        return self._store.delete_cell(cell_id)

    def convert_cell_type(self, cell_id: str, new_type: str) -> bool:
        cell_data = self._store.load_cell(cell_id)
        if not cell_data:
            return False

        old_type = cell_data["cell_type"]
        if old_type == new_type:
            return True

        cell_data["cell_type"] = new_type
        metadata = cell_data["metadata"]

        if new_type == "code":
            metadata["language"] = "python"
            metadata.setdefault("execution_count", None)
        elif new_type == "markdown":
            metadata["language"] = "markdown"
            metadata.pop("execution_count", None)
        else:
            metadata["language"] = new_type
            metadata.pop("execution_count", None)

        if old_type == "code" and new_type != "code":
            cell_data["outputs"] = []

        cell_data["modified_at"] = datetime.now(timezone.utc).isoformat()
        return self._store.save_cell(cell_data)

    def duplicate_cell(self, cell_id: str) -> str | None:
        cell_data = self._store.load_cell(cell_id)
        if not cell_data:
            return None

        return self.create_cell(
            cell_type=cell_data["cell_type"],
            content=cell_data["content"],
            metadata=cell_data["metadata"].copy(),
        )


__all__ = ["CellManager"]
