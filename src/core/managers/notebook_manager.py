"""Notebook lifecycle coordination and cell ordering."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, List

from core.models import Cell, Notebook, NotebookState
from core.persistence import DataStore
from shared.utils.id_generator import generate_notebook_id

from .events import NotebookEvents


class NotebookManager:
    """Manage notebooks and their ordered list of cell identifiers."""

    def __init__(
        self,
        store: DataStore,
        cell_manager,
        *,
        events: NotebookEvents | None = None,
    ) -> None:
        from .cell_manager import CellManager  # avoid circular import at module load

        if not isinstance(cell_manager, CellManager):
            raise TypeError("cell_manager must be an instance of CellManager")

        self._store = store
        self._cell_manager = cell_manager
        self._states: Dict[str, NotebookState] = {}
        self._active_notebook_id: str | None = None
        self.events = events or NotebookEvents()

        self._cell_manager.events.updated.connect(self._handle_cell_updated)
        self._cell_manager.events.deleted.connect(self._handle_cell_deleted)
        self._cell_manager.events.converted.connect(self._handle_cell_updated)

    # ---------------------------------------------------------------------
    # Notebook lifecycle operations
    # ---------------------------------------------------------------------
    def create_notebook(self, title: str) -> Notebook:
        notebook_id = generate_notebook_id()
        now = datetime.now(timezone.utc)

        notebook = Notebook.new(
            notebook_id=notebook_id,
            title=title,
            metadata={
                "kernel": "python3",
                "language": "python",
                "author": "",
                "tags": [],
            },
            created_at=now,
            modified_at=now,
        )

        self._store.save_notebook(notebook.to_payload())
        state = NotebookState(notebook=notebook, cells={})
        self._states[notebook_id] = state
        self._active_notebook_id = notebook_id
        self.events.notebook_created.emit(notebook)
        self.events.state_updated.emit(state)
        return notebook

    def open_notebook(self, notebook_id: str) -> NotebookState | None:
        state = self._states.get(notebook_id)
        if not state:
            state = self._load_state(notebook_id)
        if not state:
            return None

        self._active_notebook_id = notebook_id
        self.events.notebook_opened.emit(state)
        return state

    def close_notebook(self, notebook_id: str, *, save: bool = True) -> bool:
        if save:
            self.save_notebook(notebook_id)

        if self._active_notebook_id == notebook_id:
            self._active_notebook_id = None
        self.events.notebook_closed.emit(notebook_id)
        return True

    def save_notebook(self, notebook_id: str) -> bool:
        state = self._states.get(notebook_id)
        if not state:
            state = self._load_state(notebook_id)
        if not state:
            return False

        notebook = state.notebook.copy_with(modified_at=datetime.now(timezone.utc))
        state.with_notebook(notebook)
        persisted = self._store.save_notebook(notebook.to_payload())
        if persisted:
            self.events.state_updated.emit(state)
        return persisted

    # ------------------------------------------------------------------
    # Cell ordering operations
    # ------------------------------------------------------------------
    def add_cell(
        self,
        notebook_id: str,
        cell: Cell,
        *,
        position: int | None = None,
    ) -> NotebookState | None:
        state = self._ensure_state(notebook_id)
        if not state:
            return None

        insert_position = position if position is not None else len(state.notebook.cell_ids)
        insert_position = max(0, min(insert_position, len(state.notebook.cell_ids)))

        cell_ids = list(state.notebook.cell_ids)
        cell_ids.insert(insert_position, cell.cell_id)

        notebook = state.notebook.copy_with(
            cell_ids=cell_ids,
            modified_at=datetime.now(timezone.utc),
        )

        state.with_notebook(notebook)
        state.set_cell(cell)
        self._store.save_notebook(notebook.to_payload())

        self.events.cell_added.emit(notebook_id, cell.cell_id, insert_position)
        self.events.state_updated.emit(state)
        return state

    def remove_cell(self, notebook_id: str, cell_id: str) -> bool:
        state = self._ensure_state(notebook_id)
        if not state:
            return False

        if cell_id not in state.notebook.cell_ids:
            return False

        cell_ids = [cid for cid in state.notebook.cell_ids if cid != cell_id]
        notebook = state.notebook.copy_with(
            cell_ids=cell_ids,
            modified_at=datetime.now(timezone.utc),
        )

        state.with_notebook(notebook)
        state.remove_cell(cell_id)
        self._store.save_notebook(notebook.to_payload())

        self.events.cell_removed.emit(notebook_id, cell_id)
        self.events.state_updated.emit(state)
        return True

    def move_cell(self, notebook_id: str, cell_id: str, new_position: int) -> bool:
        state = self._ensure_state(notebook_id)
        if not state:
            return False

        if cell_id not in state.notebook.cell_ids:
            return False

        cell_ids = [cid for cid in state.notebook.cell_ids if cid != cell_id]
        new_position = max(0, min(new_position, len(cell_ids)))
        cell_ids.insert(new_position, cell_id)

        notebook = state.notebook.copy_with(
            cell_ids=cell_ids,
            modified_at=datetime.now(timezone.utc),
        )

        state.with_notebook(notebook)
        self._store.save_notebook(notebook.to_payload())

        self.events.cell_moved.emit(notebook_id, cell_id, new_position)
        self.events.state_updated.emit(state)
        return True

    # ------------------------------------------------------------------
    # Lookup helpers
    # ------------------------------------------------------------------
    def get_cell_order(self, notebook_id: str) -> List[str]:
        state = self._ensure_state(notebook_id)
        if not state:
            return []
        return list(state.notebook.cell_ids)

    def get_active_notebook_id(self) -> str | None:
        return self._active_notebook_id

    def get_state(self, notebook_id: str) -> NotebookState | None:
        return self._ensure_state(notebook_id)

    def list_notebooks(self) -> List[Notebook]:
        payloads = self._store.list_notebooks()
        return [Notebook.from_payload(payload) for payload in payloads]

    def rename_notebook(self, notebook_id: str, new_title: str) -> Notebook | None:
        new_title = new_title.strip()
        if not new_title:
            return None

        state = self._ensure_state(notebook_id)
        if not state:
            return None

        notebook = state.notebook.copy_with(
            title=new_title,
            modified_at=datetime.now(timezone.utc),
        )

        state.with_notebook(notebook)
        self._store.save_notebook(notebook.to_payload())

        self.events.notebook_renamed.emit(notebook)
        self.events.state_updated.emit(state)
        return notebook

    def delete_notebook(self, notebook_id: str) -> bool:
        if not notebook_id:
            return False

        deleted = self._store.delete_notebook(notebook_id)
        if deleted:
            self._states.pop(notebook_id, None)
            if self._active_notebook_id == notebook_id:
                self._active_notebook_id = None
            self.events.notebook_deleted.emit(notebook_id)
        return deleted

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _ensure_state(self, notebook_id: str) -> NotebookState | None:
        state = self._states.get(notebook_id)
        if not state:
            state = self._load_state(notebook_id)
        return state

    def _load_state(self, notebook_id: str) -> NotebookState | None:
        payload = self._store.load_notebook(notebook_id)
        if not payload:
            return None

        notebook = Notebook.from_payload(payload)
        valid_cell_ids: list[str] = []
        cells = {}
        for cell_id in notebook.cell_ids:
            cell = self._cell_manager.get_cell(cell_id)
            if cell and cell.deleted_at is None:
                cells[cell_id] = cell
                valid_cell_ids.append(cell_id)

        if valid_cell_ids != list(notebook.cell_ids):
            notebook = notebook.copy_with(
                cell_ids=valid_cell_ids,
                modified_at=datetime.now(timezone.utc),
            )
            self._store.save_notebook(notebook.to_payload())

        state = NotebookState(notebook=notebook, cells=cells)
        self._states[notebook_id] = state
        return state

    def _handle_cell_updated(self, cell: Cell) -> None:
        for state in self._states.values():
            if cell.cell_id in state.cells:
                state.set_cell(cell)
                self.events.state_updated.emit(state)

    def _handle_cell_deleted(self, cell_id: str) -> None:
        for notebook_id, state in list(self._states.items()):
            if cell_id in state.cells:
                state.remove_cell(cell_id)
                if cell_id in state.notebook.cell_ids:
                    cell_ids = [cid for cid in state.notebook.cell_ids if cid != cell_id]
                    notebook = state.notebook.copy_with(
                        cell_ids=cell_ids,
                        modified_at=datetime.now(timezone.utc),
                    )
                    state.with_notebook(notebook)
                    self._store.save_notebook(notebook.to_payload())
                self.events.cell_removed.emit(notebook_id, cell_id)
                self.events.state_updated.emit(state)



__all__ = ["NotebookManager"]
