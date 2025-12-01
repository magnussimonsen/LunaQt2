"""Round-trip tests for the initial core data layer port."""

from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from core import CellManager, DataStore, NotebookManager
from core.models import NotebookState


class _BaseCoreTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self._tmp = TemporaryDirectory()
        root = Path(self._tmp.name)
        self.store = DataStore(root)
        self.cell_manager = CellManager(self.store)
        self.notebook_manager = NotebookManager(self.store, self.cell_manager)

        self.cell_events: list[tuple[str, tuple]] = []
        self.notebook_events: list[tuple[str, tuple]] = []

        self._connect_event_recorders()

    def tearDown(self) -> None:
        self._tmp.cleanup()
        super().tearDown()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _connect_event_recorders(self) -> None:
        def record_cell(event_name: str):
            def _handler(*args) -> None:
                self.cell_events.append((event_name, args))

            return _handler

        def record_notebook(event_name: str):
            def _handler(*args) -> None:
                self.notebook_events.append((event_name, args))

            return _handler

        events = self.cell_manager.events
        events.created.connect(record_cell("created"))
        events.updated.connect(record_cell("updated"))
        events.deleted.connect(record_cell("deleted"))
        events.converted.connect(record_cell("converted"))

        n_events = self.notebook_manager.events
        n_events.notebook_created.connect(record_notebook("notebook_created"))
        n_events.notebook_opened.connect(record_notebook("notebook_opened"))
        n_events.notebook_closed.connect(record_notebook("notebook_closed"))
        n_events.notebook_renamed.connect(record_notebook("notebook_renamed"))
        n_events.notebook_deleted.connect(record_notebook("notebook_deleted"))
        n_events.cell_added.connect(record_notebook("cell_added"))
        n_events.cell_removed.connect(record_notebook("cell_removed"))
        n_events.cell_moved.connect(record_notebook("cell_moved"))
        n_events.state_updated.connect(record_notebook("state_updated"))


class TestDataStore(_BaseCoreTestCase):
    def test_notebook_round_trip(self) -> None:
        notebook = {"notebook_id": "nb-1", "title": "Demo", "cell_ids": []}
        self.assertTrue(self.store.save_notebook(notebook))

        loaded = self.store.load_notebook("nb-1")
        self.assertIsNotNone(loaded)
        assert loaded is not None
        self.assertEqual(loaded["title"], "Demo")

    def test_cell_round_trip(self) -> None:
        cell = {"cell_id": "cell-1", "content": "print('hi')"}
        self.assertTrue(self.store.save_cell(cell))

        loaded = self.store.load_cell("cell-1")
        self.assertIsNotNone(loaded)
        assert loaded is not None
        self.assertEqual(loaded["content"], "print('hi')")

    def test_list_notebooks(self) -> None:
        notebooks = [
            {"notebook_id": "nb-1", "title": "Alpha"},
            {"notebook_id": "nb-2", "title": "Beta"},
        ]
        for nb in notebooks:
            self.store.save_notebook(nb)

        listed = sorted(self.store.list_notebooks(), key=lambda item: item["notebook_id"])
        self.assertEqual([item["title"] for item in listed], ["Alpha", "Beta"])


class TestCellManager(_BaseCoreTestCase):
    def test_create_update_and_delete_cell(self) -> None:
        cell = self.cell_manager.create_cell("code", content="print('x')")
        self.assertEqual(cell.content, "print('x')")
        self.assertEqual(self.cell_events[0][0], "created")

        updated = self.cell_manager.update_cell(cell.cell_id, content="print('y')")
        assert updated is not None
        self.assertEqual(updated.content, "print('y')")
        self.assertEqual(self.cell_events[-1][0], "updated")

        deleted = self.cell_manager.delete_cell(cell.cell_id)
        self.assertTrue(deleted)
        self.assertEqual(self.cell_events[-1][0], "deleted")

    def test_convert_and_duplicate_cell(self) -> None:
        cell = self.cell_manager.create_cell("code")
        converted = self.cell_manager.convert_cell_type(cell.cell_id, "markdown")
        assert converted is not None
        self.assertEqual(converted.cell_type, "markdown")
        self.assertNotIn("execution_count", converted.metadata)
        self.assertEqual(self.cell_events[-1][0], "converted")

        duplicate = self.cell_manager.duplicate_cell(cell.cell_id)
        assert duplicate is not None
        self.assertNotEqual(duplicate.cell_id, cell.cell_id)
        self.assertEqual(self.cell_events[-1][0], "created")


class TestNotebookManager(_BaseCoreTestCase):
    def test_notebook_lifecycle_and_ordering(self) -> None:
        notebook = self.notebook_manager.create_notebook("My Notebook")
        self.assertEqual(notebook.title, "My Notebook")
        self.assertEqual(self.notebook_events[0][0], "notebook_created")

        state = self.notebook_manager.get_state(notebook.notebook_id)
        assert isinstance(state, NotebookState)
        self.assertEqual(state.notebook.notebook_id, notebook.notebook_id)

        cell_one = self.cell_manager.create_cell("code", content="print(1)")
        cell_two = self.cell_manager.create_cell("markdown", content="# Title")

        self.notebook_manager.add_cell(notebook.notebook_id, cell_one)
        self.notebook_manager.add_cell(notebook.notebook_id, cell_two, position=0)
        order = self.notebook_manager.get_cell_order(notebook.notebook_id)
        self.assertEqual(order, [cell_two.cell_id, cell_one.cell_id])
        self.assertEqual(self.notebook_events[-1][0], "state_updated")

        moved = self.notebook_manager.move_cell(notebook.notebook_id, cell_one.cell_id, 0)
        self.assertTrue(moved)
        self.assertEqual(
            self.notebook_manager.get_cell_order(notebook.notebook_id),
            [cell_one.cell_id, cell_two.cell_id],
        )
        self.assertEqual(self.notebook_events[-2][0], "cell_moved")

        renamed = self.notebook_manager.rename_notebook(notebook.notebook_id, "Renamed")
        assert renamed is not None
        self.assertEqual(renamed.title, "Renamed")
        self.assertEqual(self.notebook_events[-2][0], "notebook_renamed")

        removed = self.notebook_manager.remove_cell(notebook.notebook_id, cell_two.cell_id)
        self.assertTrue(removed)
        self.assertEqual(self.notebook_manager.get_cell_order(notebook.notebook_id), [cell_one.cell_id])
        self.assertEqual(self.notebook_events[-2][0], "cell_removed")

        # Cell deletion propagates to the cached state
        self.cell_manager.delete_cell(cell_one.cell_id)
        self.assertEqual(self.notebook_manager.get_cell_order(notebook.notebook_id), [])
        self.assertEqual(self.notebook_events[-2][0], "cell_removed")

        self.assertTrue(self.notebook_manager.delete_notebook(notebook.notebook_id))
        self.assertEqual(self.notebook_events[-1][0], "notebook_deleted")

    def test_open_close_and_list(self) -> None:
        notebook = self.notebook_manager.create_notebook("One")
        other = self.notebook_manager.create_notebook("Two")

        self.notebook_manager.close_notebook(notebook.notebook_id)
        self.assertEqual(self.notebook_events[-1][0], "notebook_closed")

        reopened = self.notebook_manager.open_notebook(notebook.notebook_id)
        assert reopened is not None
        self.assertEqual(self.notebook_events[-1][0], "notebook_opened")

        notebooks = self.notebook_manager.list_notebooks()
        self.assertEqual({nb.notebook_id for nb in notebooks}, {notebook.notebook_id, other.notebook_id})

    def test_state_updates_when_cells_change(self) -> None:
        notebook = self.notebook_manager.create_notebook("Notebook")
        cell = self.cell_manager.create_cell("code", content="print('a')")
        self.notebook_manager.add_cell(notebook.notebook_id, cell)

        updated = self.cell_manager.update_cell(cell.cell_id, content="print('b')")
        assert updated is not None

        state = self.notebook_manager.get_state(notebook.notebook_id)
        assert state is not None
        cached_cell = state.get_cell(cell.cell_id)
        assert cached_cell is not None
        self.assertEqual(cached_cell.content, "print('b')")




if __name__ == "__main__":  # pragma: no cover - convenience for local runs
    unittest.main()
