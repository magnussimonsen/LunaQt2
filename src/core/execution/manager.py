"""Notebook execution manager orchestrating worker threads."""

from __future__ import annotations

from PySide6.QtCore import QObject, Signal

from .messages import ExecutionRequest, ExecutionResult
from .worker import ExecutionWorker


class ExecutionManager(QObject):
    """High-level API for running code cells per notebook."""

    cell_started = Signal(object)   # ExecutionRequest
    cell_finished = Signal(object)  # ExecutionResult
    cell_failed = Signal(object)    # ExecutionResult

    def __init__(self, parent=None) -> None:
        """Initialize execution manager.
        
        Args:
            parent: Parent QObject
        """
        super().__init__(parent)
        self._workers: dict[str, ExecutionWorker] = {}
        self._plot_style: dict[str, str] | None = None

    def set_plot_style(self, style: dict[str, str] | None) -> None:
        """Set matplotlib style for all future executions.
        
        Args:
            style: Dictionary of matplotlib rcParams to apply
        """
        self._plot_style = dict(style) if style else None

    def run_cell(
        self,
        notebook_id: str,
        cell_id: str,
        code: str,
        execution_count: int | None = None,
    ) -> None:
        """Execute a code cell in the appropriate notebook worker.
        
        Args:
            notebook_id: ID of the notebook containing the cell
            cell_id: ID of the cell to execute
            code: Python code to execute
            execution_count: Execution counter for display
        """
        worker = self._get_or_create_worker(notebook_id)
        request = ExecutionRequest(
            notebook_id=notebook_id,
            cell_id=cell_id,
            code=code,
            execution_count=execution_count,
            plot_style=dict(self._plot_style) if self._plot_style else None,
        )
        worker.enqueue(request)

    def shutdown(self) -> None:
        """Shutdown all worker threads."""
        for worker in self._workers.values():
            worker.shutdown()
        self._workers.clear()

    def shutdown_notebook(self, notebook_id: str) -> None:
        """Shutdown worker for a specific notebook.
        
        Args:
            notebook_id: ID of the notebook to shutdown
        """
        worker = self._workers.get(notebook_id)
        if worker:
            worker.shutdown()
            del self._workers[notebook_id]
    
    def interrupt_notebook(self, notebook_id: str) -> bool:
        """Interrupt execution for a notebook by restarting its worker.
        
        This effectively stops any running cell by shutting down and recreating
        the worker thread. The global namespace is reset.
        
        Args:
            notebook_id: ID of the notebook to interrupt
            
        Returns:
            True if worker was interrupted, False if no worker existed
        """
        worker = self._workers.get(notebook_id)
        if not worker:
            return False
        
        # Shutdown existing worker
        worker.shutdown()
        
        # Create new worker with fresh namespace
        new_worker = ExecutionWorker(notebook_id)
        self._wire_worker_signals(new_worker)
        new_worker.start()
        self._workers[notebook_id] = new_worker
        
        return True

    # Internal helpers --------------------------------------------------
    def _get_or_create_worker(self, notebook_id: str) -> ExecutionWorker:
        """Get existing worker or create a new one for the notebook.
        
        Args:
            notebook_id: ID of the notebook
            
        Returns:
            ExecutionWorker instance for the notebook
        """
        worker = self._workers.get(notebook_id)
        if worker is None:
            worker = ExecutionWorker(notebook_id)
            self._wire_worker_signals(worker)
            worker.start()
            self._workers[notebook_id] = worker
        return worker

    def _wire_worker_signals(self, worker: ExecutionWorker) -> None:
        """Connect worker signals to manager signals.
        
        Args:
            worker: Worker to connect signals from
        """
        worker.request_started.connect(self.cell_started.emit)
        worker.request_finished.connect(self.cell_finished.emit)
        worker.request_failed.connect(self.cell_failed.emit)


__all__ = ["ExecutionManager"]
