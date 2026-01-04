"""Typed representation of a notebook cell."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal

from ._timestamps import format_timestamp, parse_timestamp

CellType = Literal["code", "markdown", "raw"]

_UNSET = object()


@dataclass(slots=True, frozen=True)
class Cell:
    """Immutable view of a persisted notebook cell with helper utilities."""

    cell_id: str
    cell_type: CellType
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    outputs: list[dict[str, Any]] = field(default_factory=list)
    execution_count: int | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    modified_at: datetime = field(default_factory=datetime.utcnow)
    schema_version: int = 1
    deleted_at: datetime | None = None

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> "Cell":
        deleted_at_value = payload.get("deleted_at")
        return cls(
            cell_id=payload["cell_id"],
            cell_type=payload.get("cell_type", "code"),
            content=payload.get("content", ""),
            metadata=deepcopy(payload.get("metadata", {})),
            outputs=deepcopy(payload.get("outputs", [])),
            execution_count=payload.get("execution_count"),
            created_at=parse_timestamp(payload.get("created_at")),
            modified_at=parse_timestamp(payload.get("modified_at")),
            schema_version=int(payload.get("schema_version", 1)),
            deleted_at=parse_timestamp(deleted_at_value) if deleted_at_value else None,
        )

    @classmethod
    def new(
        cls,
        *,
        cell_id: str,
        cell_type: CellType,
        content: str,
        metadata: dict[str, Any],
        created_at: datetime,
        modified_at: datetime,
        outputs: list[dict[str, Any]] | None = None,
        execution_count: int | None = None,
        schema_version: int = 1,
        deleted_at: datetime | None = None,
    ) -> "Cell":
        return cls(
            cell_id=cell_id,
            cell_type=cell_type,
            content=content,
            metadata=deepcopy(metadata),
            outputs=deepcopy(outputs) if outputs else [],
            execution_count=execution_count,
            created_at=created_at,
            modified_at=modified_at,
            schema_version=schema_version,
            deleted_at=deleted_at,
        )

    def to_payload(self) -> dict[str, Any]:
        return {
            "cell_id": self.cell_id,
            "cell_type": self.cell_type,
            "content": self.content,
            "metadata": deepcopy(self.metadata),
            "outputs": deepcopy(self.outputs),
            "execution_count": self.execution_count,
            "created_at": format_timestamp(self.created_at),
            "modified_at": format_timestamp(self.modified_at),
            "schema_version": self.schema_version,
            "deleted_at": format_timestamp(self.deleted_at) if self.deleted_at else None,
        }

    def copy_with(
        self,
        *,
        cell_type: CellType | None = None,
        content: str | None = None,
        metadata: dict[str, Any] | None = None,
        outputs: list[dict[str, Any]] | None = None,
        execution_count: int | None | object = _UNSET,
        modified_at: datetime | None = None,
        deleted_at: datetime | None | object = _UNSET,
    ) -> "Cell":
        return Cell(
            cell_id=self.cell_id,
            cell_type=cell_type or self.cell_type,
            content=content if content is not None else self.content,
            metadata=deepcopy(metadata) if metadata is not None else deepcopy(self.metadata),
            outputs=deepcopy(outputs) if outputs is not None else deepcopy(self.outputs),
            execution_count=self.execution_count if execution_count is _UNSET else execution_count,
            created_at=self.created_at,
            modified_at=modified_at or self.modified_at,
            schema_version=self.schema_version,
            deleted_at=self.deleted_at if deleted_at is _UNSET else deleted_at,
        )


__all__ = ["Cell", "CellType"]
