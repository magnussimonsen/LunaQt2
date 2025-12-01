"""Cached, in-memory view of a notebook and its cells."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, Iterator

from .cell import Cell
from .notebook import Notebook


@dataclass(slots=True)
class NotebookState:
    """Holds a notebook record and the cells currently loaded in memory."""

    notebook: Notebook
    cells: Dict[str, Cell] = field(default_factory=dict)
    active_cell_id: str | None = None

    def cell_order(self) -> list[str]:
        return list(self.notebook.cell_ids)

    def get_cell(self, cell_id: str) -> Cell | None:
        return self.cells.get(cell_id)

    def iter_cells(self) -> Iterator[Cell]:
        for cell_id in self.notebook.cell_ids:
            cell = self.cells.get(cell_id)
            if cell:
                yield cell

    def with_notebook(self, notebook: Notebook) -> "NotebookState":
        self.notebook = notebook
        return self

    def set_cell(self, cell: Cell) -> None:
        self.cells[cell.cell_id] = cell

    def remove_cell(self, cell_id: str) -> None:
        if cell_id in self.cells:
            del self.cells[cell_id]
        if self.active_cell_id == cell_id:
            self.active_cell_id = None

    def update_cells(self, cells: Iterable[Cell]) -> None:
        for cell in cells:
            self.set_cell(cell)


__all__ = ["NotebookState"]
