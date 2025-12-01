"""Coordinators that orchestrate domain operations."""

from .cell_manager import CellManager
from .notebook_manager import NotebookManager

__all__ = ["CellManager", "NotebookManager"]
