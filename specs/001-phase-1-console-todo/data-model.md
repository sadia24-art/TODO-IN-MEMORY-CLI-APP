# Data Model: In-Memory Python Console Todo Application (Phase I)

**Date**: 2026-01-01
**Feature**: [spec.md](./spec.md)
**Plan**: [plan.md](./plan.md)

## Purpose

Define entities, attributes, relationships, and state transitions for Phase I in-memory todo application. All definitions traceable to specification requirements (FR-001 to FR-012) and constitutional principles.

---

## Entities

### Todo

Represents a single task item in the todo list.

**Attributes**:

| Attribute | Type | Constraints | Default | Description |
|-----------|------|-------------|---------|-------------|
| `id` | `int` | Unique, positive, sequential, immutable | Assigned by repository | Unique identifier for the todo item |
| `text` | `str` | Non-empty after `strip()`, no max length | Required | Description of the task |
| `completed` | `bool` | True or False | `False` | Completion status (incomplete/complete) |

**Attribute Details**:

**`id` (int)**:
- **Uniqueness**: Guaranteed unique within a single application session
- **Assignment**: Auto-increment counter starting at 1
- **Immutability**: Once assigned, never changes (even if other todos deleted)
- **Sequence**: Sequential (1, 2, 3, ...) per spec Assumption #10
- **Persistence**: Resets to 1 when application restarts (in-memory only)

**`text` (str)**:
- **Validation**: Must be non-empty after `text.strip()` (removes leading/trailing whitespace)
- **Max Length**: None (console wraps naturally per research.md)
- **Encoding**: UTF-8 for international character support (spec Assumption #5)
- **Examples**:
  - Valid: `"Buy groceries"`, `"  Call mom  "` (strips to `"Call mom"`)
  - Invalid: `""`, `"   "` (empty after strip)

**`completed` (bool)**:
- **Initial State**: `False` when todo created
- **Transition**: `False` → `True` via "Mark complete" operation
- **Idempotent**: Marking completed todo as complete again succeeds gracefully (no error)
- **No Reversion**: No "unmark complete" operation in Phase I (out of scope)
- **Display**: `True` = `"[✓]"`, `False` = `"[ ]"` in CLI

**Python Implementation**:
```python
from dataclasses import dataclass

@dataclass
class Todo:
    """Represents a single todo item."""
    id: int
    text: str
    completed: bool = False

    def __str__(self) -> str:
        """Human-readable representation for CLI display."""
        status = "✓" if self.completed else " "
        return f"{self.id}. [{status}] {self.text}"
```

---

### TodoRepository

Manages in-memory storage and retrieval of todo items. Encapsulates storage implementation (List) so Phase II can swap for database-backed version.

**Attributes**:

| Attribute | Type | Visibility | Description |
|-----------|------|------------|-------------|
| `_todos` | `List[Todo]` | Private | In-memory list of all todos |
| `_next_id` | `int` | Private | Auto-increment counter for ID assignment |

**Attribute Details**:

**`_todos` (List[Todo])**:
- **Visibility**: Private (not exposed to Logic layer)
- **Initialization**: Empty list `[]`
- **Lifetime**: Exists only during application runtime (in-memory per constitutional Phase I constraint)
- **Access**: Only via repository methods (`add`, `get_all`, `get_by_id`, `update`, `delete`, `mark_complete`)

**`_next_id` (int)**:
- **Initialization**: Starts at `1`
- **Increment**: Increases by 1 on each `add()` operation
- **Never Decreases**: Deletion doesn't decrement counter (IDs never reused)
- **Deterministic**: Same sequence of operations → same IDs (constitutional Principle IV)

**Methods**:

| Method | Parameters | Returns | Raises | Description |
|--------|------------|---------|--------|-------------|
| `add(text: str)` | `text`: Todo description | `Todo` | `ValueError` if text empty | Create and add new todo |
| `get_all()` | None | `List[Todo]` | Never | Retrieve all todos (may be empty list) |
| `get_by_id(todo_id: int)` | `todo_id`: ID to find | `Todo` | `KeyError` if not found | Retrieve specific todo by ID |
| `update(todo_id: int, text: str)` | `todo_id`: ID to update, `text`: New description | `Todo` | `KeyError` if not found, `ValueError` if text empty | Update todo text |
| `delete(todo_id: int)` | `todo_id`: ID to delete | `None` | `KeyError` if not found | Remove todo from list |
| `mark_complete(todo_id: int)` | `todo_id`: ID to mark | `Todo` | `KeyError` if not found | Set todo's `completed = True` |

**Method Specifications**:

**`add(text: str) -> Todo`**:
```python
def add(self, text: str) -> Todo:
    """
    Create and add a new todo item.

    Args:
        text: Description of the todo (will be stripped)

    Returns:
        The newly created Todo

    Raises:
        ValueError: If text is empty after stripping
    """
    text = text.strip()
    if not text:
        raise ValueError("Todo text cannot be empty")

    todo = Todo(id=self._next_id, text=text, completed=False)
    self._next_id += 1
    self._todos.append(todo)
    return todo
```

**`get_all() -> List[Todo]`**:
```python
def get_all(self) -> List[Todo]:
    """
    Retrieve all todos.

    Returns:
        List of all Todo items (may be empty)
    """
    return self._todos.copy()  # Return copy to prevent external modification
```

**`get_by_id(todo_id: int) -> Todo`**:
```python
def get_by_id(self, todo_id: int) -> Todo:
    """
    Retrieve a specific todo by ID.

    Args:
        todo_id: The ID to search for

    Returns:
        The Todo with matching ID

    Raises:
        KeyError: If no todo with that ID exists
    """
    for todo in self._todos:
        if todo.id == todo_id:
            return todo
    raise KeyError(f"Todo with ID {todo_id} not found")
```

**`update(todo_id: int, text: str) -> Todo`**:
```python
def update(self, todo_id: int, text: str) -> Todo:
    """
    Update a todo's text.

    Args:
        todo_id: The ID of the todo to update
        text: New description (will be stripped)

    Returns:
        The updated Todo

    Raises:
        KeyError: If no todo with that ID exists
        ValueError: If text is empty after stripping
    """
    text = text.strip()
    if not text:
        raise ValueError("Todo text cannot be empty")

    todo = self.get_by_id(todo_id)  # Raises KeyError if not found
    todo.text = text
    return todo
```

**`delete(todo_id: int) -> None`**:
```python
def delete(self, todo_id: int) -> None:
    """
    Delete a todo by ID.

    Args:
        todo_id: The ID of the todo to delete

    Raises:
        KeyError: If no todo with that ID exists
    """
    todo = self.get_by_id(todo_id)  # Raises KeyError if not found
    self._todos.remove(todo)
```

**`mark_complete(todo_id: int) -> Todo`**:
```python
def mark_complete(self, todo_id: int) -> Todo:
    """
    Mark a todo as complete.

    Args:
        todo_id: The ID of the todo to mark complete

    Returns:
        The updated Todo

    Raises:
        KeyError: If no todo with that ID exists

    Note:
        Idempotent - calling on already-completed todo succeeds without error
    """
    todo = self.get_by_id(todo_id)  # Raises KeyError if not found
    todo.completed = True
    return todo
```

---

## Relationships

### TodoRepository → Todo (Composition)

```
TodoRepository (1) ──contains──> (0..N) Todo
```

**Description**: A `TodoRepository` contains zero or more `Todo` items. The repository owns the todos (lifetime management, ID assignment).

**Cardinality**:
- **1 TodoRepository**: Singleton instance per application run
- **0..N Todos**: Can have empty list (0) or many todos (tested up to 100 per spec SC-005)

**Ownership**: TodoRepository owns todos (creates, stores, deletes)

**Lifecycle**: When TodoRepository is garbage collected (application exit), all Todos are lost (in-memory only per constitutional Phase I constraint)

---

## State Transitions

### Todo Lifecycle

```
┌─────────────┐
│  [Created]  │  Initial state: completed = False
└──────┬──────┘
       │
       │ add(text) operation
       ▼
┌─────────────┐
│  [Active]   │  Exists in repository, incomplete
└──────┬──────┘
       │
       ├─────► update(id, text) ────► [Active] (text changed, status unchanged)
       │
       ├─────► mark_complete(id) ───► [Completed]
       │
       └─────► delete(id) ───────────► [Deleted] (removed from repository)


┌─────────────┐
│ [Completed] │  completed = True
└──────┬──────┘
       │
       ├─────► update(id, text) ────► [Completed] (text changed, status unchanged)
       │
       ├─────► mark_complete(id) ───► [Completed] (idempotent, no change)
       │
       └─────► delete(id) ───────────► [Deleted] (removed from repository)


┌─────────────┐
│  [Deleted]  │  Terminal state (no longer in repository)
└─────────────┘
```

**State Descriptions**:

1. **[Created]**: Conceptual state during instantiation (not observable)
   - Transition: Immediately to `[Active]` when added to repository

2. **[Active]**: Todo exists in repository, `completed = False`
   - Can be viewed, updated, marked complete, or deleted
   - Most todos spend majority of time in this state

3. **[Completed]**: Todo exists in repository, `completed = True`
   - Can be viewed, updated (text only), or deleted
   - Cannot be "uncompleted" (no reversion operation in Phase I)

4. **[Deleted]**: Terminal state (todo removed from repository)
   - No operations possible (ID no longer valid)
   - ID never reused (auto-increment counter never decrements)

**Transition Triggers**:

| From State | Trigger | To State | Notes |
|------------|---------|----------|-------|
| [Created] | `repository.add(text)` | [Active] | Immediate transition on creation |
| [Active] | `repository.update(id, text)` | [Active] | Text changes, status unchanged |
| [Active] | `repository.mark_complete(id)` | [Completed] | Status changes to `True` |
| [Active] | `repository.delete(id)` | [Deleted] | Removed from repository |
| [Completed] | `repository.update(id, text)` | [Completed] | Text changes, status unchanged |
| [Completed] | `repository.mark_complete(id)` | [Completed] | Idempotent (no change) |
| [Completed] | `repository.delete(id)` | [Deleted] | Removed from repository |

---

## Validation Rules

### Text Validation

**Rule**: Todo text MUST be non-empty after stripping whitespace

**Enforcement Point**: `TodoRepository.add()` and `TodoRepository.update()`

**Examples**:
```python
# Valid
repository.add("Buy groceries")           # ✅ Non-empty
repository.add("  Call mom  ")            # ✅ Strips to "Call mom"
repository.add("123")                     # ✅ Numbers allowed
repository.add("タスク")                   # ✅ Unicode allowed

# Invalid
repository.add("")                        # ❌ Raises ValueError
repository.add("   ")                     # ❌ Raises ValueError (empty after strip)
repository.add("\t\n")                    # ❌ Raises ValueError (whitespace only)
```

**Rationale**: Empty todos provide no value (spec FR-012: "prevent creation of todos with empty or whitespace-only text")

---

### ID Validation

**Rule**: Todo ID MUST exist in repository

**Enforcement Point**: `TodoRepository.get_by_id()` (called by all ID-based operations)

**Examples**:
```python
# Valid
repository.get_by_id(1)                   # ✅ If ID 1 exists
repository.mark_complete(2)               # ✅ If ID 2 exists

# Invalid
repository.get_by_id(999)                 # ❌ Raises KeyError (ID not found)
repository.update(5, "New text")          # ❌ Raises KeyError if ID 5 doesn't exist
repository.delete(100)                    # ❌ Raises KeyError if ID 100 doesn't exist
```

**Rationale**: Operations on non-existent todos must fail fast with clear error (spec FR-008, NFR-007)

---

### ID Uniqueness

**Rule**: No two todos can have the same ID within a single session

**Enforcement Point**: `TodoRepository.add()` (auto-increment guarantees uniqueness)

**Guarantee**: Auto-increment counter ensures IDs are unique and sequential (1, 2, 3, ...)

**Example**:
```python
repo = TodoRepository()
todo1 = repo.add("First")   # ID = 1
todo2 = repo.add("Second")  # ID = 2
repo.delete(1)              # Delete first todo
todo3 = repo.add("Third")   # ID = 3 (not reusing ID 1)

# IDs: [2, 3] (1 was deleted)
# _next_id: 4 (ready for next add)
```

**Rationale**: Deterministic behavior per constitutional Principle IV; user expectations of stable IDs

---

## Constraints

### Performance Constraints

Per spec NFR-001, NFR-002, NFR-003:

- **Operation Time**: All operations (add, view, update, delete, mark complete) MUST complete in <1 second
  - **Implementation**: In-memory operations on Python list (O(n) for searches, acceptable for n ≤ 100)
  - **Validation**: Manual testing with 100 todos

- **Startup Time**: Application startup MUST complete in <2 seconds
  - **Implementation**: Empty repository initialization (trivial, ~1ms)
  - **Validation**: Timed application launch

- **Memory Usage**: MUST remain under 50MB for typical use (up to 100 todos)
  - **Calculation**: 100 todos × ~200 bytes per todo = ~20 KB (well under limit)
  - **Validation**: Manual memory profiling with 100 todos

### Data Volume Constraints

Per spec Assumption #3, SC-005:

- **Typical Use Case**: 1-100 todo items per session
- **Tested Range**: Application must handle at least 100 todos without degradation
- **Upper Bound**: No hard limit enforced (Python list can hold millions), but not tested beyond 100

### Storage Constraints

Per constitutional Phase I constraints:

- **No Persistence**: All data lost when application exits
- **In-Memory Only**: No file writes, no database, no network storage
- **Session-Scoped**: TodoRepository lifecycle tied to application process

---

## Persistence Strategy

**Phase I**: None (in-memory only)

**Rationale**: Constitutional Phase I constraint explicitly prohibits persistence

**User Warning**: Display on application start and exit:
```
⚠️  Warning: All todos will be lost when you exit this session.
   (No data is saved between runs)
```

**Phase II Evolution**: Replace `TodoRepository` with database-backed version
- **Interface Compatibility**: Same methods (`add`, `get_all`, `get_by_id`, etc.)
- **Technology**: SQLModel + Neon DB per constitutional Phase II constraints
- **Migration**: Logic layer unchanged (depends only on repository interface)

---

## Schema Evolution (Future Phases)

**Phase I Schema** (This Phase):
```python
@dataclass
class Todo:
    id: int
    text: str
    completed: bool
```

**Phase II Additions** (Planned):
- `created_at: datetime` - Timestamp when todo was created
- `updated_at: datetime` - Timestamp of last modification
- `user_id: int` - Foreign key to user (multi-user support)

**Phase III Additions** (Planned):
- `priority: int` - Priority level (1-5)
- `due_date: Optional[datetime]` - Deadline for completion
- `tags: List[str]` - Categories/labels

**Migration Strategy**: Additive only (no breaking changes to existing fields)

---

## References

- **Spec**: [spec.md](./spec.md) - Functional requirements (FR-001 to FR-012)
- **Plan**: [plan.md](./plan.md) - Architecture and design decisions
- **Research**: [research.md](./research.md) - Data structure choice rationale
- **Constitution**: [.specify/memory/constitution.md](../../.specify/memory/constitution.md) - Phase I constraints

---

## Revision History

| Date | Change | Rationale |
|------|--------|-----------|
| 2026-01-01 | Initial data model | Phase 1 of `/sp.plan` workflow |
