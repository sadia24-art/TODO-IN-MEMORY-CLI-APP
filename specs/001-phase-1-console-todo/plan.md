# Implementation Plan: In-Memory Python Console Todo Application (Phase I)

**Branch**: `001-phase-1-console-todo` | **Date**: 2026-01-01 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-phase-1-console-todo/spec.md`

**Note**: This plan follows the Spec-Driven Development workflow mandated by the project constitution.

## Summary

Build a minimal, in-memory Python console application for managing todo items. The application provides CRUD operations (Create, Read, Update, Delete) plus completion tracking through a command-line interface. No persistence layer—all data exists only during runtime. Architecture emphasizes strict separation of concerns (CLI, Logic, Data) to enable future evolution to web/AI interfaces in subsequent phases.

**Key Characteristics:**
- Single-user, single-session usage
- Menu-driven console interface
- Deterministic, testable behavior
- Foundation for multi-phase evolution (Phase I → Phase V)

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Python standard library only (no external packages)
**Storage**: In-memory only (Python lists/dictionaries, no persistence)
**Testing**: pytest (optional - tests not required for Phase I per spec)
**Target Platform**: Cross-platform (Windows, macOS, Linux with Python 3.13+)
**Project Type**: Single console application
**Performance Goals**: <1 second response time per operation, <2 second startup, handle 100+ todos
**Constraints**: <50MB memory usage, console I/O only, no persistence, no external services
**Scale/Scope**: 1-100 todo items per session (typical use case), tested up to 100 items

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Spec-Driven Development ✅ PASS
- ✅ Specification approved (spec.md complete with 4 user stories, 12 FRs, 8 success criteria)
- ✅ Following mandated workflow: Constitution → Spec → Plan → Tasks → Implementation
- ✅ All architectural decisions documented in this plan
- ✅ No code written before plan approval

### Principle II: Incremental Phase Evolution ✅ PASS
- ✅ Phase I constraints enforced: in-memory, console-only, Python, no persistence
- ✅ Architecture designed for future evolution (layered structure supports Phase II web interface)
- ✅ Separation of Logic layer from CLI enables Phase II+ interface swapping
- ✅ Documentation in `specs/001-phase-1-console-todo/` per convention

### Principle III: Separation of Concerns ✅ PASS
- ✅ Three distinct layers: CLI (interface), Logic (business rules), Data (storage)
- ✅ Clear boundaries: CLI ← → Logic ← → Data
- ✅ Logic layer stateless and portable (no CLI dependencies)
- ✅ Data layer encapsulated (internal structure hidden from Logic)

### Principle IV: Deterministic and Reproducible Behavior ✅ PASS
- ✅ No randomness in ID assignment (sequential from 1)
- ✅ All operations deterministic (same input → same output)
- ✅ State transitions traceable (todo lifecycle: created → [updated] → [completed] → [deleted])
- ✅ No external dependencies (standard library only, versions pinned via UV)

### Principle V: Documentation Completeness ✅ PASS
- ✅ plan.md (this file) documents architecture and decisions
- ✅ research.md will document technology choices and rationale
- ✅ data-model.md will define entities and relationships
- ✅ quickstart.md will provide user/developer onboarding
- ✅ All decisions include rationale and alternatives considered

### Principle VI: Test-Driven Development (Where Applicable) ✅ PASS
- ✅ Specification states "Tests are OPTIONAL unless explicitly requested" (spec.md line 11, Principle VI)
- ✅ No tests required for Phase I per user requirements
- ✅ User stories include testable acceptance criteria if tests added later
- ✅ Architecture supports future test integration (logic layer testable in isolation)

### Phase I Constraints ✅ PASS
- ✅ Python-based implementation only
- ✅ No database, no persistence across sessions
- ✅ Console I/O only (stdin/stdout/stderr)
- ✅ All data stored in-memory (Python data structures)
- ✅ Spec-driven development workflow followed

**GATE RESULT: ✅ ALL CHECKS PASSED - Proceed to Phase 0**

## Project Structure

### Documentation (this feature)

```text
specs/001-phase-1-console-todo/
├── spec.md              # Feature requirements & user stories ✅ Complete
├── plan.md              # This file (architecture & design) ✅ In progress
├── research.md          # Phase 0: Technology choices & rationale (to be created)
├── data-model.md        # Phase 1: Entity definitions (to be created)
├── quickstart.md        # Phase 1: User & developer guide (to be created)
├── contracts/           # Phase 1: API contracts (to be created)
│   └── cli-commands.md  # CLI command specifications
├── checklists/          # Quality validation
│   └── requirements.md  # Spec quality checklist ✅ Complete
└── tasks.md             # Phase 2: Implementation tasks (NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── __init__.py          # Package marker
├── main.py              # Application entry point (CLI initialization)
├── cli/                 # CLI Layer: User interface & command routing
│   ├── __init__.py
│   ├── menu.py          # Menu display & user input handling
│   └── commands.py      # Command parsing & validation
├── logic/               # Logic Layer: Business rules & operations
│   ├── __init__.py
│   ├── todo_service.py  # Todo CRUD operations & validation
│   └── validators.py    # Input validation logic
└── data/                # Data Layer: In-memory storage
    ├── __init__.py
    ├── todo_repository.py  # Todo storage & retrieval
    └── models.py        # Todo data structure definitions

tests/                   # Test structure (optional for Phase I)
├── __init__.py
├── unit/                # Unit tests (if added)
│   ├── test_validators.py
│   └── test_todo_service.py
└── integration/         # Integration tests (if added)
    └── test_cli_workflow.py

pyproject.toml           # UV project configuration
README.md                # Project overview & setup instructions
.python-version          # Python version specification (3.13+)
```

**Structure Decision**: **Single project** (Option 1 from template) selected because:
- Phase I is a standalone console application (no web frontend/backend split needed)
- Simple three-layer architecture (CLI, Logic, Data) fits single project structure
- Modular organization within `src/` enables future extraction for Phase II web backend
- Clear separation via directories (`cli/`, `logic/`, `data/`) supports independent testing and evolution

## Complexity Tracking

> **No constitutional violations detected. This section intentionally left empty.**

All constitutional principles satisfied without exceptions or complexity justifications needed.

---

## Phase 0: Research & Technology Choices

### Overview

Phase 0 resolves technology choices and establishes best practices for Phase I implementation. Since Phase I uses Python standard library only, research focuses on design patterns, CLI architecture, and development tooling.

### Research Topics

1. **CLI Framework Decision**
   - **Options Evaluated**: argparse (stdlib), click (external), raw input()
   - **Decision**: **Menu-driven with raw input()** (stdlib)
   - **Rationale**:
     - Meets constitutional constraint: Python standard library only (no external packages)
     - Menu-driven interface aligns with user story acceptance criteria (numbered options)
     - Simple input/validation loop sufficient for 5 operations (add, view, update, delete, complete)
     - Lower learning curve for evaluators reviewing agentic workflow
   - **Alternatives Rejected**:
     - `argparse`: Better for command-line args (e.g., `todo add "text"`), but spec implies interactive session
     - `click`: External dependency violates Phase I constraints
     - `cmd` module: Overkill for simple menu (5 operations), adds unnecessary complexity

2. **Data Structure Design**
   - **Options Evaluated**: List of dicts, custom Todo class, namedtuples
   - **Decision**: **Custom Todo dataclass** + **List storage**
   - **Rationale**:
     - `@dataclass` (Python 3.7+, stdlib) provides clean attribute access and auto-generated `__init__`, `__repr__`
     - Type hints improve code clarity and enable future validation
     - List provides sequential ID management (index + 1 = ID)
     - Simple enough for in-memory, complex enough to model state (id, text, completed)
   - **Alternatives Rejected**:
     - Plain dicts: Less type-safe, harder to maintain consistency
     - namedtuples: Immutable (update operations require reconstruction)
     - Custom class without @dataclass: More boilerplate for no benefit

3. **ID Management Strategy**
   - **Options Evaluated**: Auto-increment counter, list index +1, UUIDs
   - **Decision**: **Auto-increment counter** (separate from list index)
   - **Rationale**:
     - Spec Assumption #10: "Todo IDs are assigned sequentially starting from 1 and increment with each new todo"
     - Survives deletion without ID gaps confusion (user deletes ID 2, IDs 1 and 3 remain stable)
     - Counter persists in memory, increments on each add, never reused
     - Deterministic per constitutional Principle IV
   - **Alternatives Rejected**:
     - List index + 1: Fragile (IDs change when items deleted, violates user expectations)
     - UUIDs: Overkill for Phase I, non-sequential violates spec assumption

4. **Error Handling Approach**
   - **Options Evaluated**: Exceptions, return codes, result objects
   - **Decision**: **Exceptions for validation errors** + **try/except in CLI layer**
   - **Rationale**:
     - Pythonic approach (EAFP: Easier to Ask Forgiveness than Permission)
     - Logic layer raises `ValueError` for invalid input (empty text, bad ID)
     - CLI layer catches and displays user-friendly messages (per NFR-005)
     - Clean separation: Logic enforces rules, CLI handles presentation
   - **Alternatives Rejected**:
     - Return codes: Less clear (need to check every return value), not idiomatic Python
     - Result objects: Overkill for simple validation errors

5. **Development Tooling (UV)**
   - **Options Evaluated**: pip + venv, poetry, UV
   - **Decision**: **UV** (per spec Technical Requirements)
   - **Rationale**:
     - Spec explicitly requires "Environment & tooling: UV"
     - Faster than pip, built-in virtual environment management
     - `pyproject.toml` for reproducible builds (constitutional Principle IV)
     - Pins Python version and dependencies
   - **Alternatives Rejected**: None (spec requirement)

### Best Practices Identified

1. **Separation of Concerns**
   - CLI layer: No business logic (only input/output and routing)
   - Logic layer: No I/O (only pure functions and validation)
   - Data layer: No logic (only storage and retrieval)
   - **Benefit**: Each layer independently testable and replaceable (Phase II web UI swaps CLI layer)

2. **Input Validation**
   - Validate at boundaries: CLI validates format (numeric ID), Logic validates business rules (ID exists, text non-empty)
   - Fail fast: Check inputs before modifying state
   - Clear error messages: Specify what's wrong and suggest corrective action (per NFR-005)

3. **State Management**
   - Single source of truth: `TodoRepository` owns the list
   - No shared mutable state between layers
   - Logic layer stateless (all state in Data layer)

4. **Code Organization**
   - One module per concern (menu, commands, service, repository, models, validators)
   - Clear naming: `TodoService`, `TodoRepository`, `MenuDisplay`
   - Avoid god objects: Each module has single responsibility

### Documentation Artifact

Full research findings documented in [research.md](./research.md) (Phase 0 output).

---

## Phase 1: Design & Contracts

### Data Model

Detailed entity definitions in [data-model.md](./data-model.md).

**Summary:**

**Todo Entity**
- `id`: int (unique, sequential, starts at 1, immutable)
- `text`: str (non-empty after strip, max length TBD in planning)
- `completed`: bool (default False, toggled by mark complete operation)

**TodoRepository**
- `_todos`: List[Todo] (in-memory storage)
- `_next_id`: int (auto-increment counter, starts at 1)
- Methods: `add(text)`, `get_all()`, `get_by_id(id)`, `update(id, text)`, `delete(id)`, `mark_complete(id)`

**Relationships:**
- TodoRepository contains 0..N Todos
- Todo IDs managed by TodoRepository (not exposed to Logic layer)

**State Transitions:**
```
[Created: completed=False]
  → [Updated: text changes, completed unchanged]
  → [Completed: completed=True]
  → [Deleted: removed from repository]
```

**Validation Rules:**
- Text: Must be non-empty after `strip()`, no max length enforced (console wraps naturally)
- ID: Must exist in repository (validated by `get_by_id`)
- Completion: Idempotent (marking completed todo as complete succeeds gracefully)

### CLI Command Contracts

Detailed command specifications in [contracts/cli-commands.md](./contracts/cli-commands.md).

**Command Interface:**
```
Main Menu:
1. Add todo
2. View all todos
3. Mark todo as complete
4. Update todo
5. Delete todo
6. Exit

User selects number (1-6) → CLI routes to appropriate Logic operation
```

**Command Flows:**

1. **Add Todo**
   - Input: Text description (string, prompted after selection)
   - Output: Confirmation message with assigned ID
   - Errors: Empty text → display error, return to menu

2. **View All Todos**
   - Input: None
   - Output: Formatted table (ID | Text | Status) or "No todos yet" if empty
   - Errors: None (empty list is valid state)

3. **Mark Complete**
   - Input: Todo ID (int, prompted after selection)
   - Output: Confirmation message
   - Errors: Non-numeric input → display error; ID not found → display error

4. **Update Todo**
   - Input: Todo ID (int, prompted), new text (string, prompted)
   - Output: Confirmation message
   - Errors: ID not found → display error; empty text → display error

5. **Delete Todo**
   - Input: Todo ID (int, prompted)
   - Output: Confirmation message
   - Errors: ID not found → display error

6. **Exit**
   - Input: None
   - Output: Goodbye message with data loss warning
   - Errors: None

**Error Message Format:**
```
❌ Error: [What went wrong]
💡 Suggestion: [How to fix it]
```

Example:
```
❌ Error: Todo ID 5 not found
💡 Suggestion: Use 'View all todos' to see valid IDs
```

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         User                                 │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      CLI Layer                               │
│  ┌──────────────┐    ┌──────────────┐                       │
│  │  menu.py     │◄───┤ commands.py  │                       │
│  │ (display)    │    │ (parse/route)│                       │
│  └──────────────┘    └──────┬───────┘                       │
│                              │                               │
└──────────────────────────────┼───────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                     Logic Layer                              │
│  ┌─────────────────────┐    ┌─────────────┐                │
│  │  todo_service.py    │◄───┤validators.py│                │
│  │  (CRUD operations)  │    │ (rules)     │                │
│  └──────────┬──────────┘    └─────────────┘                │
│             │                                                │
└─────────────┼────────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Data Layer                               │
│  ┌───────────────────┐    ┌──────────────┐                 │
│  │ todo_repository.py│◄───┤  models.py   │                 │
│  │  (storage)        │    │ (Todo class) │                 │
│  └───────────────────┘    └──────────────┘                 │
└─────────────────────────────────────────────────────────────┘
```

**Layer Responsibilities:**

**CLI Layer:**
- Display menu and prompts
- Read user input (numbers, text)
- Parse and validate input format (e.g., numeric IDs)
- Route commands to Logic layer
- Format and display results
- Handle CLI-specific errors (e.g., non-numeric input for menu selection)

**Logic Layer:**
- Enforce business rules (non-empty text, ID exists)
- Coordinate operations (add, view, update, delete, mark complete)
- Validate business constraints (e.g., text not empty after strip)
- Raise exceptions for validation failures
- Stateless: no storage, only operations

**Data Layer:**
- Store todos in memory (List[Todo])
- Manage ID assignment (auto-increment counter)
- Provide CRUD operations on storage
- Return todos or raise exceptions if not found
- Encapsulate internal structure (Logic doesn't know List vs Dict)

**Key Design Decisions:**

1. **Why three layers instead of two (CLI + Logic only)?**
   - **Reason**: Phase II will replace in-memory storage with database (Neon DB + SQLModel)
   - **Benefit**: Data layer isolates storage implementation; Phase II swaps `TodoRepository` for DB-backed version
   - **Tradeoff**: Slight overhead for Phase I, but critical for evolution strategy

2. **Why menu-driven instead of command-line args (e.g., `todo add "text"`)?**
   - **Reason**: Spec acceptance scenarios describe interactive session ("user requests to view", "user marks todo 1")
   - **Benefit**: Simpler input validation, clear workflow for evaluators
   - **Tradeoff**: Less scriptable, but Phase I is human-interactive by design

3. **Why exceptions instead of return codes for errors?**
   - **Reason**: Pythonic (EAFP), cleaner separation (Logic raises, CLI catches/displays)
   - **Benefit**: Logic layer doesn't need to know CLI message format
   - **Tradeoff**: Slight performance cost (negligible for human-interactive app)

4. **Why separate validators.py from todo_service.py?**
   - **Reason**: Single Responsibility Principle (validation vs orchestration)
   - **Benefit**: Validators reusable across services, easier to test
   - **Tradeoff**: More files, but clearer boundaries

### Quickstart Guide

User and developer onboarding documented in [quickstart.md](./quickstart.md).

**Summary:**
- **Users**: Run `uv run src/main.py`, follow menu prompts
- **Developers**: Install UV, `uv sync`, structure explained, contribution guidelines
- **Evaluators**: Step-by-step verification of spec-driven workflow (spec → plan → tasks → implementation)

---

## Phase 2: Task Generation

**Phase 2 is handled by the `/sp.tasks` command** (NOT by `/sp.plan`).

After this plan is approved:
1. Run `/sp.tasks` to generate `tasks.md` with concrete implementation steps
2. Tasks will reference specific files and line numbers from this architecture
3. Task dependencies derived from layer boundaries (Data → Logic → CLI)
4. Tasks organized by user story priority (P1 → P2 → P3 → P4) per spec

---

## Constitutional Re-Check (Post-Design)

*GATE: Validate architecture against constitution after Phase 1 design.*

### Principle I: Spec-Driven Development ✅ PASS
- ✅ Plan documents all architectural decisions with rationale
- ✅ No implementation performed (only design artifacts created)
- ✅ Design traceable to spec requirements (FR-001 to FR-012, NFR-001 to NFR-014)

### Principle II: Incremental Phase Evolution ✅ PASS
- ✅ Architecture designed for Phase II evolution:
  - Data layer isolates storage (swap for DB in Phase II)
  - Logic layer portable (reusable in FastAPI backend Phase II)
  - CLI layer replaceable (Next.js frontend in Phase II)

### Principle III: Separation of Concerns ✅ PASS
- ✅ Three layers with clear boundaries and responsibilities
- ✅ No circular dependencies (CLI → Logic → Data, one direction only)
- ✅ Each layer independently testable and replaceable

### Principle IV: Deterministic and Reproducible Behavior ✅ PASS
- ✅ ID assignment deterministic (auto-increment counter)
- ✅ All operations deterministic (no randomness)
- ✅ State transitions explicit (created → updated → completed → deleted)

### Principle V: Documentation Completeness ✅ PASS
- ✅ plan.md documents architecture and decisions
- ✅ research.md documents technology choices and rationale
- ✅ data-model.md defines entities and relationships
- ✅ contracts/cli-commands.md specifies CLI interface
- ✅ quickstart.md provides onboarding guidance

### Principle VI: Test-Driven Development (Where Applicable) ✅ PASS
- ✅ Tests optional for Phase I per spec
- ✅ Architecture supports future testing (Logic layer testable in isolation)
- ✅ Test structure documented in project structure (tests/unit/, tests/integration/)

**GATE RESULT: ✅ ALL CHECKS PASSED - Architecture approved for task generation**

---

## Next Steps

1. **Review this plan** with stakeholders/evaluators
2. **Run `/sp.tasks`** to generate implementation tasks from this architecture
3. **Run `/sp.implement`** to execute tasks and build Phase I application
4. **Validate against spec** using success criteria (SC-001 to SC-008)

---

## Appendix: Design Alternatives Considered

### Alternative: Single-layer "quick and dirty" implementation
- **Description**: All code in `main.py`, no layer separation
- **Rejected because**: Violates constitutional Principle III (Separation of Concerns), makes Phase II evolution difficult
- **Tradeoff**: Faster initial implementation vs technical debt for future phases

### Alternative: Use `click` for CLI
- **Description**: External library for command-line interfaces
- **Rejected because**: Violates Phase I constraint (Python standard library only), adds unnecessary dependency
- **Tradeoff**: Nicer CLI features vs constitutional compliance and simplicity

### Alternative: JSON file persistence
- **Description**: Save todos to `todos.json` on exit, load on startup
- **Rejected because**: Violates Phase I constraint (no persistence), contradicts spec SC-008 ("All data is lost when application terminates")
- **Tradeoff**: User convenience vs constitutional compliance and spec requirements

### Alternative: List index as ID
- **Description**: Use list position (index + 1) as todo ID
- **Rejected because**: IDs change when items deleted, violates user expectations and spec Assumption #10 (sequential IDs)
- **Tradeoff**: Simpler implementation vs user confusion and non-deterministic IDs
