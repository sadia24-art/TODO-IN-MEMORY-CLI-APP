# Research: In-Memory Python Console Todo Application (Phase I)

**Date**: 2026-01-01
**Feature**: [spec.md](./spec.md)
**Plan**: [plan.md](./plan.md)

## Purpose

Document technology choices, design patterns, and best practices for Phase I implementation. All decisions traceable to constitutional principles and specification requirements.

## Research Questions

### 1. CLI Framework Selection

**Question**: Which approach for command-line interface?

**Options Evaluated**:
1. **argparse** (Python standard library)
   - Pros: Built-in, powerful argument parsing, supports subcommands
   - Cons: Better for `command arg1 arg2` style than interactive menus
   - Use case: CLI tools like `git`, `docker`

2. **click** (External package)
   - Pros: Modern API, decorator-based, good documentation
   - Cons: **External dependency violates Phase I constraint** (stdlib only)
   - Use case: Complex CLI tools requiring rich features

3. **cmd module** (Python standard library)
   - Pros: Built-in command loop, command history
   - Cons: Overkill for 6 menu options, learning curve for evaluators
   - Use case: Interactive shells (Python REPL-like interfaces)

4. **raw input() loop** (Python standard library)
   - Pros: Simple, no learning curve, full control over UX
   - Cons: More manual work (no built-in command parsing)
   - Use case: Simple interactive menus

**Decision**: **Menu-driven interface with raw input() loop**

**Rationale**:
- ✅ Constitutional compliance: Python standard library only
- ✅ Spec alignment: User story acceptance scenarios describe interactive sessions
- ✅ Simplicity: 6 menu options don't require complex framework
- ✅ Evaluator-friendly: Clear, obvious interaction flow

**Implementation Pattern**:
```python
while True:
    display_menu()
    choice = input("Enter choice (1-6): ").strip()
    if choice == "1":
        handle_add_todo()
    elif choice == "2":
        handle_view_todos()
    # ... etc
    elif choice == "6":
        break
```

---

### 2. Data Structure for Todos

**Question**: How to represent todo items in memory?

**Options Evaluated**:
1. **Dictionary list** `[{id: 1, text: "...", completed: False}, ...]`
   - Pros: Simple, JSON-serializable (useful for Phase II)
   - Cons: No type safety, easy to make mistakes with keys

2. **namedtuple** `Todo = namedtuple('Todo', ['id', 'text', 'completed'])`
   - Pros: Lightweight, type-hinted attribute access
   - Cons: Immutable (update requires creating new instance)

3. **dataclass** `@dataclass class Todo: ...`
   - Pros: Mutable, type hints, auto-generated methods, clean syntax
   - Cons: Slightly more overhead than namedtuple (negligible for < 100 items)

4. **Custom class** without dataclass
   - Pros: Full control
   - Cons: Boilerplate (`__init__`, `__repr__`, `__eq__` manual implementation)

**Decision**: **dataclass with type hints**

**Rationale**:
- ✅ Mutable: Update operations natural (`todo.text = new_text`, `todo.completed = True`)
- ✅ Type hints: Clarity and future IDE support
- ✅ Auto-generated methods: `__init__`, `__repr__`, `__eq__` free
- ✅ Standard library: `from dataclasses import dataclass` (Python 3.7+)
- ✅ Performance: Negligible overhead for 100 items per spec

**Implementation**:
```python
from dataclasses import dataclass

@dataclass
class Todo:
    id: int
    text: str
    completed: bool = False
```

---

### 3. ID Assignment Strategy

**Question**: How to assign and manage todo IDs?

**Options Evaluated**:
1. **List index + 1** (e.g., `todos[0]` has ID 1)
   - Pros: Simple, no separate counter
   - Cons: **IDs change when items deleted** (user deletes ID 2, ID 3 becomes ID 2)
   - Problem: Violates spec Assumption #10 (sequential IDs) and user expectations

2. **Auto-increment counter** (separate from list index)
   - Pros: Stable IDs (deletion doesn't affect other IDs), deterministic
   - Cons: Slight overhead (extra variable)
   - Pattern: `_next_id` starts at 1, increments on each add, never decreases

3. **UUIDs** (e.g., `uuid.uuid4()`)
   - Pros: Globally unique, no collision risk
   - Cons: Non-sequential (violates spec), overkill for single-user session
   - Use case: Distributed systems, Phase II+ with database

**Decision**: **Auto-increment counter** (separate from list)

**Rationale**:
- ✅ Spec compliance: Assumption #10 states "Todo IDs are assigned sequentially starting from 1"
- ✅ Deterministic: Same operations → same IDs (constitutional Principle IV)
- ✅ User-friendly: ID 1 remains ID 1 even if other todos deleted
- ✅ Simple implementation: `self._next_id += 1` on each add

**Implementation**:
```python
class TodoRepository:
    def __init__(self):
        self._todos: List[Todo] = []
        self._next_id: int = 1

    def add(self, text: str) -> Todo:
        todo = Todo(id=self._next_id, text=text, completed=False)
        self._next_id += 1
        self._todos.append(todo)
        return todo
```

---

### 4. Error Handling Strategy

**Question**: How to handle validation errors and invalid operations?

**Options Evaluated**:
1. **Return codes** (e.g., `add_todo()` returns `(success: bool, error_msg: str)`)
   - Pros: Explicit, no exceptions
   - Cons: Caller must check every return value, easy to forget, not Pythonic

2. **Exceptions** (raise `ValueError`, `KeyError`, etc.)
   - Pros: Pythonic (EAFP), clear separation (Logic raises, CLI catches)
   - Cons: Slight performance overhead (negligible for interactive app)

3. **Result objects** (e.g., `Result[T, Error]` like Rust)
   - Pros: Type-safe, explicit
   - Cons: Overkill for simple app, requires custom Result class or library

**Decision**: **Exceptions for validation errors**

**Rationale**:
- ✅ Pythonic: "Easier to Ask Forgiveness than Permission" (EAFP) idiom
- ✅ Clean separation: Logic layer raises errors, CLI layer catches and displays
- ✅ Clear contracts: `add_todo(text)` raises `ValueError` if text empty
- ✅ NFR-005 compliance: CLI formats exceptions as user-friendly messages

**Error Taxonomy**:
- `ValueError`: Invalid input (empty text, non-numeric ID input)
- `KeyError`: Todo ID not found
- `RuntimeError`: Unexpected states (shouldn't occur if logic correct)

**Implementation Pattern**:
```python
# Logic layer
def add_todo(text: str) -> Todo:
    if not text.strip():
        raise ValueError("Todo text cannot be empty")
    return repository.add(text.strip())

# CLI layer
try:
    todo = service.add_todo(user_input)
    print(f"✅ Added todo #{todo.id}")
except ValueError as e:
    print(f"❌ Error: {e}")
    print("💡 Suggestion: Enter a description for your todo")
```

---

### 5. Layer Boundaries and Responsibilities

**Question**: How to organize code into layers?

**Options Evaluated**:
1. **Monolithic** (all code in `main.py`)
   - Pros: Simple, no imports
   - Cons: **Violates constitutional Principle III** (Separation of Concerns)
   - Problem: Cannot evolve to Phase II web UI

2. **Two layers** (CLI + Logic combined, Data separate)
   - Pros: Fewer files
   - Cons: CLI and business logic mixed, harder to test Logic in isolation

3. **Three layers** (CLI, Logic, Data separate)
   - Pros: Clear boundaries, each layer testable, swappable (Phase II)
   - Cons: More files (acceptable tradeoff)

**Decision**: **Three-layer architecture** (CLI → Logic → Data)

**Rationale**:
- ✅ Constitutional Principle III: Separation of Concerns enforced
- ✅ Phase II evolution: CLI layer swappable for web UI, Logic layer reusable in FastAPI backend
- ✅ Testability: Logic layer testable without CLI (pure functions)
- ✅ Maintainability: Single Responsibility Principle per module

**Layer Contracts**:

**CLI Layer** (`src/cli/`)
- **Responsibility**: User interaction (input/output)
- **Dependencies**: Logic layer (imports `TodoService`)
- **No dependencies on**: Data layer (no direct access to `TodoRepository`)
- **Modules**: `menu.py` (display), `commands.py` (parsing/routing)

**Logic Layer** (`src/logic/`)
- **Responsibility**: Business rules and operations
- **Dependencies**: Data layer (imports `TodoRepository`)
- **No dependencies on**: CLI layer (no `print()`, no `input()`)
- **Modules**: `todo_service.py` (CRUD operations), `validators.py` (rules)

**Data Layer** (`src/data/`)
- **Responsibility**: Storage and retrieval
- **Dependencies**: None (leaf layer)
- **Modules**: `models.py` (Todo dataclass), `todo_repository.py` (storage)

**Dependency Flow**: CLI → Logic → Data (one direction, no cycles)

---

### 6. Development Tooling: UV

**Question**: How to manage Python environment and dependencies?

**Options Evaluated**:
1. **pip + venv** (Python standard tooling)
   - Pros: Built-in, widely used
   - Cons: Slower dependency resolution, manual venv management

2. **poetry** (Modern Python packaging)
   - Pros: Good dependency management, lock files
   - Cons: Not specified in requirements

3. **UV** (Fast Python package manager)
   - Pros: **Spec requirement**, faster than pip, built-in venv, lock files
   - Cons: Newer tool (less mature)

**Decision**: **UV** (per spec Technical Requirements)

**Rationale**:
- ✅ Spec compliance: "Environment & tooling: UV" explicitly required
- ✅ Performance: Faster installs and resolves than pip
- ✅ Reproducibility: `uv.lock` ensures deterministic builds (constitutional Principle IV)
- ✅ Simplicity: `uv run` handles venv automatically

**Setup**:
```bash
# Initialize project
uv init

# Specify Python version
echo "3.13" > .python-version

# Run application
uv run src/main.py

# Add dependency (future phases)
uv add <package>
```

**`pyproject.toml` structure**:
```toml
[project]
name = "todo-app-phase-1"
version = "0.1.0"
description = "In-memory Python console todo application"
requires-python = ">=3.13"
dependencies = []  # Empty for Phase I (stdlib only)

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

---

## Best Practices Identified

### Input Validation

**Practice**: Validate at layer boundaries
- **CLI layer**: Format validation (numeric input for IDs, non-empty strings)
- **Logic layer**: Business rule validation (text not empty after strip, ID exists)
- **Data layer**: Structural integrity (ID uniqueness, counter consistency)

**Pattern**:
```python
# CLI validates format
choice = input("Enter choice: ")
if not choice.isdigit():
    print("❌ Error: Please enter a number (1-6)")
    continue

# Logic validates business rules
def add_todo(text: str) -> Todo:
    text = text.strip()
    if not text:
        raise ValueError("Todo text cannot be empty")
    return repository.add(text)
```

### Error Messages

**Practice**: Follow NFR-005 (specify what went wrong + suggest corrective action)

**Format**:
```
❌ Error: [Problem description]
💡 Suggestion: [How to fix]
```

**Examples**:
- `❌ Error: Todo ID 5 not found` + `💡 Suggestion: Use 'View all todos' to see valid IDs`
- `❌ Error: Todo text cannot be empty` + `💡 Suggestion: Enter a description for your todo`
- `❌ Error: Invalid choice` + `💡 Suggestion: Please enter a number between 1 and 6`

### State Management

**Practice**: Single source of truth per constitutional Principle IV

- `TodoRepository` owns the list (only class that modifies `_todos`)
- `TodoService` orchestrates operations (stateless, no stored state)
- CLI displays current state (reads via `service.view_all()`, doesn't cache)

**Anti-pattern to avoid**:
```python
# BAD: CLI caching state
class CLI:
    def __init__(self):
        self.cached_todos = []  # ❌ Duplicate state
```

**Correct pattern**:
```python
# GOOD: CLI always reads from single source of truth
def display_todos():
    todos = service.view_all()  # ✅ Fresh read every time
    for todo in todos:
        print(f"{todo.id}. {todo.text} [{'✓' if todo.completed else ' '}]")
```

### Code Organization

**Practice**: One module per concern (Single Responsibility Principle)

**File naming conventions**:
- `models.py`: Data structures (Todo dataclass)
- `todo_repository.py`: Storage operations (add, get, update, delete)
- `todo_service.py`: Business logic (CRUD orchestration)
- `validators.py`: Validation rules (text non-empty, ID exists)
- `menu.py`: Menu display and formatting
- `commands.py`: Command parsing and routing
- `main.py`: Application entry point (initialization)

**Import guidelines**:
- CLI imports Logic, not Data
- Logic imports Data, not CLI
- Data imports nothing (leaf layer)
- No circular imports

---

## Technology Stack Summary

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Language | Python 3.13+ | Spec requirement, Phase I constitutional constraint |
| CLI Framework | raw `input()` loop | Stdlib only, simple menu (6 options) |
| Data Structure | `@dataclass` | Mutable, type hints, stdlib, clean syntax |
| ID Strategy | Auto-increment counter | Deterministic, spec compliant (sequential IDs) |
| Error Handling | Exceptions | Pythonic, clean separation (Logic raises, CLI catches) |
| Architecture | 3-layer (CLI/Logic/Data) | Constitutional Principle III, Phase II evolution |
| Environment | UV | Spec requirement, fast, reproducible |
| Testing | pytest (optional) | Standard, spec states tests optional for Phase I |

---

## Risks and Mitigations

### Risk 1: ID Management Complexity
- **Risk**: Auto-increment counter could get out of sync with list
- **Mitigation**: Encapsulate in `TodoRepository`, single responsibility for ID generation
- **Validation**: Unit test ID uniqueness and sequential assignment

### Risk 2: User Confusion with Menu
- **Risk**: Users might not understand menu options
- **Mitigation**: Clear option descriptions, help text, error suggestions (NFR-006)
- **Example**: "1. Add todo (create a new task)" instead of just "1. Add"

### Risk 3: Empty State UX
- **Risk**: Viewing empty list might confuse users
- **Mitigation**: Display "No todos yet. Select 'Add todo' to create one." instead of blank output

### Risk 4: Phase II Evolution Breaking Changes
- **Risk**: Phase I architecture might not support Phase II database integration
- **Mitigation**: Data layer abstraction (`TodoRepository` interface can be swapped for DB-backed version)
- **Validation**: Logic layer has zero knowledge of storage implementation

---

## References

- **Spec**: [spec.md](./spec.md)
- **Constitution**: [.specify/memory/constitution.md](../../.specify/memory/constitution.md)
- **Python Dataclasses**: https://docs.python.org/3/library/dataclasses.html
- **Python Input/Output**: https://docs.python.org/3/library/functions.html#input
- **UV Documentation**: https://github.com/astral-sh/uv

---

## Revision History

| Date | Change | Rationale |
|------|--------|-----------|
| 2026-01-01 | Initial research | Phase 0 of `/sp.plan` workflow |
