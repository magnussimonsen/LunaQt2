"""Typed representation of a notebook cell."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal

from ._timestamps import format_timestamp, parse_timestamp

CellType = Literal["code", "markdown", "raw"]


@dataclass(slots=True, frozen=True)
class Cell:
    """Immutable view of a persisted notebook cell with helper utilities."""

    cell_id: str
    cell_type: CellType
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    outputs: list[dict[str, Any]] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    modified_at: datetime = field(default_factory=datetime.utcnow)
    schema_version: int = 1

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> "Cell":
        return cls(
            cell_id=payload["cell_id"],
            cell_type=payload.get("cell_type", "code"),
            content=payload.get("content", ""),
            metadata=deepcopy(payload.get("metadata", {})),
            outputs=deepcopy(payload.get("outputs", [])),
            created_at=parse_timestamp(payload.get("created_at")),
            modified_at=parse_timestamp(payload.get("modified_at")),
            schema_version=int(payload.get("schema_version", 1)),
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
        schema_version: int = 1,
    ) -> "Cell":
        return cls(
            cell_id=cell_id,
            cell_type=cell_type,
            content=content,
            metadata=deepcopy(metadata),
            outputs=deepcopy(outputs) if outputs else [],
            created_at=created_at,
            modified_at=modified_at,
            schema_version=schema_version,
        )

    def to_payload(self) -> dict[str, Any]:
        return {
            "cell_id": self.cell_id,
            "cell_type": self.cell_type,
            "content": self.content,
            "metadata": deepcopy(self.metadata),
            "outputs": deepcopy(self.outputs),
            "created_at": format_timestamp(self.created_at),
            "modified_at": format_timestamp(self.modified_at),
            "schema_version": self.schema_version,
        }

    def copy_with(
        self,
        *,
        cell_type: CellType | None = None,
        content: str | None = None,
        metadata: dict[str, Any] | None = None,
        outputs: list[dict[str, Any]] | None = None,
        modified_at: datetime | None = None,
    ) -> "Cell":
        return Cell(
            cell_id=self.cell_id,
            cell_type=cell_type or self.cell_type,
            content=content if content is not None else self.content,
            metadata=deepcopy(metadata) if metadata is not None else deepcopy(self.metadata),
            outputs=deepcopy(outputs) if outputs is not None else deepcopy(self.outputs),
            created_at=self.created_at,
            modified_at=modified_at or self.modified_at,
            schema_version=self.schema_version,
        )


__all__ = ["Cell", "CellType"]
