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


class _BaseCoreTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self._tmp = TemporaryDirectory()
        root = Path(self._tmp.name)
        self.store = DataStore(root)
        self.cell_manager = CellManager(self.store)
        self.notebook_manager = NotebookManager(self.store)

    def tearDown(self) -> None:
        self._tmp.cleanup()
        super().tearDown()


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


class TestManagerIntegration(_BaseCoreTestCase):
    def test_create_and_update_cell(self) -> None:
        cell_id = self.cell_manager.create_cell("code", content="print('x')")
        stored = self.store.load_cell(cell_id)
        self.assertIsNotNone(stored)
        assert stored is not None
        self.assertEqual(stored["cell_type"], "code")

        self.assertTrue(self.cell_manager.update_cell(cell_id, content="print('y')"))
        updated = self.store.load_cell(cell_id)
        assert updated is not None
        self.assertEqual(updated["content"], "print('y')")

    def test_convert_and_duplicate_cell(self) -> None:
        cell_id = self.cell_manager.create_cell("code")
        self.assertTrue(self.cell_manager.convert_cell_type(cell_id, "markdown"))
        converted = self.store.load_cell(cell_id)
        assert converted is not None
        self.assertEqual(converted["cell_type"], "markdown")
        self.assertNotIn("execution_count", converted["metadata"])

        duplicate_id = self.cell_manager.duplicate_cell(cell_id)
        self.assertIsNotNone(duplicate_id)
        assert duplicate_id is not None
        self.assertNotEqual(duplicate_id, cell_id)

    def test_notebook_lifecycle_and_ordering(self) -> None:
        notebook_id = self.notebook_manager.create_notebook("My Notebook")
        notebook_path = self.store.data_root / "notebooks" / f"{notebook_id}.json"
        self.assertTrue(notebook_path.exists())

        cell_one = self.cell_manager.create_cell("code", content="print(1)")
        cell_two = self.cell_manager.create_cell("markdown", content="# Title")

        self.assertTrue(self.notebook_manager.add_cell(notebook_id, cell_one))
        self.assertTrue(self.notebook_manager.add_cell(notebook_id, cell_two))
        self.assertTrue(self.notebook_manager.move_cell(notebook_id, cell_two, 0))

        order = self.notebook_manager.get_cell_order(notebook_id)
        self.assertEqual(order, [cell_two, cell_one])

        self.assertTrue(self.notebook_manager.rename_notebook(notebook_id, "Renamed"))
        reloaded = self.store.load_notebook(notebook_id)
        assert reloaded is not None
        self.assertEqual(reloaded["title"], "Renamed")

        self.assertTrue(self.notebook_manager.remove_cell(notebook_id, cell_one))
        self.assertEqual(self.notebook_manager.get_cell_order(notebook_id), [cell_two])

        self.assertTrue(self.cell_manager.delete_cell(cell_one))
        self.assertIsNone(self.store.load_cell(cell_one))

        self.assertTrue(self.notebook_manager.delete_notebook(notebook_id))
        self.assertIsNone(self.store.load_notebook(notebook_id))

    def test_list_notebooks_reflects_new_entries(self) -> None:
        first = self.notebook_manager.create_notebook("One")
        second = self.notebook_manager.create_notebook("Two")

        listed = sorted(
            self.notebook_manager.list_notebooks(),
            key=lambda item: item["notebook_id"],
        )
        self.assertEqual(len(listed), 2)
        self.assertEqual({item["notebook_id"] for item in listed}, {first, second})


if __name__ == "__main__":  # pragma: no cover - convenience for local runs
    unittest.main()
