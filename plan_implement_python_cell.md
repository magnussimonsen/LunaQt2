# Python Cell Execution Implementation Plan for LunaQt2

## Analysis of OLD_LUNA_QT Architecture

The old app uses a well-designed execution system:

### Core Components:
1. **ExecutionWorker** (`QThread`) - Dedicated worker thread per notebook
2. **NotebookExecutionManager** - High-level API orchestrating workers
3. **ExecutionRequest/ExecutionResult** - Data classes for communication
4. **Matplotlib Style Integration** - Theme-aware plot rendering

### Key Features:
- ✅ Background execution (non-blocking UI)
- ✅ Per-notebook globals namespace (variables persist across cells)
- ✅ Matplotlib figure capture with theme-aware styling
- ✅ Stdout/stderr capture
- ✅ Error handling with traceback
- ✅ Plot scaling controls
- ✅ Execution count tracking

---

## Implementation Plan for LunaQt2

### Phase 1: Core Execution Engine
1. Create `src/core/execution/` directory
2. Port execution messages (`ExecutionRequest`, `ExecutionResult`)
3. Implement `ExecutionWorker` with:
   - QThread-based execution
   - Per-notebook global namespace
   - Matplotlib figure capture (Agg backend)
   - Output redirection (stdout/stderr)
   - Exception handling
4. Implement `ExecutionManager` to orchestrate workers

### Phase 2: Matplotlib Theme Integration
1. Create `src/shared/constants/matplotlib_styles.py`
2. Define light/dark matplotlib rcParams
3. Wire theme switching to execution manager
4. Apply styles via context manager during execution

### Phase 3: UI Integration
1. Update `CellRow` to support:
   - Execution count display (`In [n]:` or `In [*]:`)
   - Output area (text + plots)
   - Plot scaling controls
2. Connect Run/Stop buttons to execution engine
3. Add output rendering widgets
4. Implement plot display with QPixmap

### Phase 4: State Management
1. Add execution state to `Cell` model
2. Add execution count to persistence layer
3. Wire execution results to cell updates
4. Handle notebook switching (pause/resume workers)

### Phase 5: Polish
1. Keyboard shortcuts (Shift+Enter to run)
2. Stop button functionality (interrupt execution)
3. Plot export options
4. Clear output functionality

---

## File Structure to Create

```
src/core/execution/
├── __init__.py
├── messages.py          # ExecutionRequest, ExecutionResult
├── worker.py            # ExecutionWorker (QThread)
└── manager.py           # ExecutionManager

src/shared/constants/
└── matplotlib_styles.py # Theme-aware matplotlib styles
```

---

## Benefits of This Approach

1. **Non-blocking UI** - Code runs in background threads
2. **Persistent namespace** - Variables survive across cell executions
3. **Beautiful plots** - Automatic dark/light theme matching
4. **Clean separation** - Execution logic separated from UI
5. **Proven design** - Already working in OLD_LUNA_QT