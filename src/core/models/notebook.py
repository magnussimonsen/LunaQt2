"""Typed representation of a notebook and its metadata."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, List

from ._timestamps import format_timestamp, parse_timestamp


@dataclass(slots=True, frozen=True)
class Notebook:
    """Immutable description of a notebook document."""

    notebook_id: str
    title: str
    cell_ids: List[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    modified_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    schema_version: int = 1

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> "Notebook":
        return cls(
            notebook_id=payload["notebook_id"],
            title=payload.get("title", "Untitled"),
            cell_ids=list(payload.get("cell_ids", [])),
            metadata=deepcopy(payload.get("metadata", {})),
            created_at=parse_timestamp(payload.get("created_at")),
            modified_at=parse_timestamp(payload.get("modified_at")),
            schema_version=int(payload.get("schema_version", 1)),
        )

    @classmethod
    def new(
        cls,
        *,
        notebook_id: str,
        title: str,
        created_at: datetime,
        modified_at: datetime,
        metadata: dict[str, Any] | None = None,
        cell_ids: list[str] | None = None,
        schema_version: int = 1,
    ) -> "Notebook":
        return cls(
            notebook_id=notebook_id,
            title=title,
            cell_ids=list(cell_ids or []),
            metadata=deepcopy(metadata) if metadata is not None else {},
            created_at=created_at,
            modified_at=modified_at,
            schema_version=schema_version,
        )

    def to_payload(self) -> dict[str, Any]:
        return {
            "notebook_id": self.notebook_id,
            "title": self.title,
            "cell_ids": list(self.cell_ids),
            "metadata": deepcopy(self.metadata),
            "created_at": format_timestamp(self.created_at),
            "modified_at": format_timestamp(self.modified_at),
            "schema_version": self.schema_version,
        }

    def copy_with(
        self,
        *,
        title: str | None = None,
        cell_ids: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        modified_at: datetime | None = None,
    ) -> "Notebook":
        return Notebook(
            notebook_id=self.notebook_id,
            title=title if title is not None else self.title,
            cell_ids=list(cell_ids if cell_ids is not None else self.cell_ids),
            metadata=deepcopy(metadata) if metadata is not None else deepcopy(self.metadata),
            created_at=self.created_at,
            modified_at=modified_at or datetime.now(timezone.utc),
            schema_version=self.schema_version,
        )


__all__ = ["Notebook"]
