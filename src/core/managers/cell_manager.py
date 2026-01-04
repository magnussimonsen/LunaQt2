"""Cell lifecycle management built on top of the persistence layer."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from core.models import Cell, CellType
from core.persistence import DataStore
from shared.utils.id_generator import generate_cell_id

from .events import CellEvents


class CellManager:
    """Create, read, update, and delete notebook cells."""

    def __init__(self, store: DataStore, *, events: CellEvents | None = None) -> None:
        self._store = store
        self.events = events or CellEvents()

    def create_cell(
        self,
        cell_type: CellType,
        *,
        content: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> Cell:
        cell_id = generate_cell_id()
        now = datetime.now(timezone.utc)

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

        cell = Cell.new(
            cell_id=cell_id,
            cell_type=cell_type,
            content=content,
            metadata=resolved_metadata,
            created_at=now,
            modified_at=now,
            outputs=[],
            deleted_at=None,
        )

        self._store.save_cell(cell.to_payload())
        self.events.created.emit(cell)
        return cell

    def get_cell(self, cell_id: str) -> Cell | None:
        payload = self._store.load_cell(cell_id)
        if not payload:
            return None
        return Cell.from_payload(payload)

    def update_cell(
        self,
        cell_id: str,
        *,
        content: str | None = None,
        metadata: dict[str, Any] | None = None,
        outputs: list[dict[str, Any]] | None = None,
        execution_count: int | None | object = None,
    ) -> Cell | None:
        cell = self.get_cell(cell_id)
        if not cell:
            return None

        merged_metadata = cell.metadata.copy()
        if metadata is not None:
            merged_metadata.update(metadata)

        new_outputs = outputs if outputs is not None else cell.outputs
        
        # Handle execution_count separately from metadata
        # Use a sentinel to distinguish between "not provided" and "set to None"
        _UNSET = object()
        new_execution_count = cell.execution_count if execution_count is None else execution_count

        updated_cell = cell.copy_with(
            content=content if content is not None else cell.content,
            metadata=merged_metadata,
            outputs=new_outputs,
            execution_count=new_execution_count,
            modified_at=datetime.now(timezone.utc),
        )

        self._store.save_cell(updated_cell.to_payload())
        self.events.updated.emit(updated_cell)
        return updated_cell

    def delete_cell(self, cell_id: str) -> bool:
        cell = self.get_cell(cell_id)
        if not cell:
            return False

        if cell.deleted_at is not None:
            # Already marked as deleted; still emit so downstream listeners stay in sync.
            self.events.deleted.emit(cell_id)
            return True

        timestamp = datetime.now(timezone.utc)
        tombstone = cell.copy_with(
            deleted_at=timestamp,
            modified_at=timestamp,
        )
        persisted = self._store.save_cell(tombstone.to_payload())
        if persisted:
            self.events.deleted.emit(cell_id)
        return persisted

    def convert_cell_type(self, cell_id: str, new_type: CellType) -> Cell | None:
        cell = self.get_cell(cell_id)
        if not cell:
            return None

        if cell.cell_type == new_type:
            return cell

        metadata = cell.metadata.copy()

        if new_type == "code":
            metadata["language"] = "python"
            metadata.setdefault("execution_count", None)
        elif new_type == "markdown":
            metadata["language"] = "markdown"
            metadata.pop("execution_count", None)
        else:
            metadata["language"] = new_type
            metadata.pop("execution_count", None)

        outputs = [] if cell.cell_type == "code" and new_type != "code" else cell.outputs

        updated_cell = cell.copy_with(
            cell_type=new_type,
            metadata=metadata,
            outputs=outputs,
            modified_at=datetime.now(timezone.utc),
        )

        self._store.save_cell(updated_cell.to_payload())
        self.events.converted.emit(updated_cell)
        return updated_cell

    def duplicate_cell(self, cell_id: str) -> Cell | None:
        source = self.get_cell(cell_id)
        if not source:
            return None

        duplicate = self.create_cell(
            source.cell_type,
            content=source.content,
            metadata=source.metadata,
        )
        return duplicate


__all__ = ["CellManager"]
