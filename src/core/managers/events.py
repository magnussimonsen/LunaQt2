"""Simple callback-based event hooks for core managers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Callable, List

if TYPE_CHECKING:  # pragma: no cover - imported for type hints only
    from core.models import Cell, Notebook, NotebookState


class EventHook:
    """Lightweight callback registry mimicking Qt signals."""

    def __init__(self) -> None:
        self._listeners: List[Callable[..., None]] = []

    def connect(self, callback: Callable[..., None]) -> None:
        if callback not in self._listeners:
            self._listeners.append(callback)

    def disconnect(self, callback: Callable[..., None]) -> None:
        if callback in self._listeners:
            self._listeners.remove(callback)

    def emit(self, *args, **kwargs) -> None:
        for listener in tuple(self._listeners):
            listener(*args, **kwargs)

    __call__ = emit


@dataclass(slots=True)
class CellEvents:
    """Events raised by :class:`CellManager`."""

    created: EventHook = field(default_factory=EventHook)
    updated: EventHook = field(default_factory=EventHook)
    deleted: EventHook = field(default_factory=EventHook)
    converted: EventHook = field(default_factory=EventHook)


@dataclass(slots=True)
class NotebookEvents:
    """Events raised by :class:`NotebookManager`."""

    notebook_created: EventHook = field(default_factory=EventHook)
    notebook_opened: EventHook = field(default_factory=EventHook)
    notebook_closed: EventHook = field(default_factory=EventHook)
    notebook_renamed: EventHook = field(default_factory=EventHook)
    notebook_deleted: EventHook = field(default_factory=EventHook)

    cell_added: EventHook = field(default_factory=EventHook)
    cell_removed: EventHook = field(default_factory=EventHook)
    cell_moved: EventHook = field(default_factory=EventHook)

    state_updated: EventHook = field(default_factory=EventHook)


__all__ = ["EventHook", "CellEvents", "NotebookEvents"]
