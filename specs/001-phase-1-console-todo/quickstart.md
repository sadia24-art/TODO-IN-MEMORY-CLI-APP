# Quickstart Guide: In-Memory Python Console Todo Application (Phase I)

**Date**: 2026-01-01
**Feature**: [spec.md](./spec.md)
**Plan**: [plan.md](./plan.md)

## Purpose

Get users, developers, and evaluators up and running with the Phase I todo application quickly. Covers installation, usage, development setup, and spec-driven workflow validation.

---

## For End Users

### Prerequisites

- **Python 3.13+** installed
- **UV** package manager installed ([installation instructions](https://github.com/astral-sh/uv))
- Terminal/console access (Windows Command Prompt, macOS Terminal, Linux shell)

### Quick Start (3 steps)

1. **Navigate to project directory**:
   ```bash
   cd /path/to/TODO-IN-MEMORY-CLI-APP
   ```

2. **Run the application**:
   ```bash
   uv run src/main.py
   ```

3. **Follow the menu prompts**:
   ```
   ==========================================
           TODO APP - Phase I
   ==========================================

   Main Menu:
   1. Add todo
   2. View all todos
   3. Mark todo as complete
   4. Update todo
   5. Delete todo
   6. Exit

   ⚠️  Note: All data will be lost when you exit

   ==========================================
   Enter your choice (1-6):
   ```

### Basic Usage Example

```
# Add your first todo
> Enter your choice (1-6): 1
> Enter todo description: Buy groceries
✅ Added todo #1: "Buy groceries"

# Add another todo
> Enter your choice (1-6): 1
> Enter todo description: Call mom
✅ Added todo #2: "Call mom"

# View all todos
> Enter your choice (1-6): 2

==========================================
            Your Todos
==========================================

ID   Status   Description
--   ------   -----------
1    [ ]      Buy groceries
2    [ ]      Call mom

------------------------------------------
Total: 2 todos (0 completed, 2 pending)
==========================================

# Mark todo as complete
> Enter your choice (1-6): 3
> Enter todo ID to mark complete: 1
✅ Marked todo #1 as complete

# View updated list
> Enter your choice (1-6): 2

ID   Status   Description
--   ------   -----------
1    [✓]      Buy groceries
2    [ ]      Call mom

------------------------------------------
Total: 2 todos (1 completed, 1 pending)
==========================================

# Exit
> Enter your choice (1-6): 6

==========================================
        Goodbye! Thanks for using TODO App

        ⚠️  All todos have been lost
        (Data is not saved between sessions)
==========================================
```

### Important Notes

⚠️ **No Persistence**: All data is lost when you exit the application. This is intentional for Phase I (in-memory only per constitutional constraints).

💡 **UTF-8 Support**: You can use international characters in todo descriptions (e.g., "タスク", "Tâche").

🔢 **ID Stability**: Todo IDs never change. If you delete todo #2, todos #1 and #3 keep their IDs.

---

## For Developers

### Development Setup

1. **Clone repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd TODO-IN-MEMORY-CLI-APP
   ```

2. **Verify Python version**:
   ```bash
   python --version  # Should be 3.13 or higher
   ```

3. **Install UV** (if not already installed):
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

4. **Initialize UV environment**:
   ```bash
   uv sync
   ```

5. **Run application**:
   ```bash
   uv run src/main.py
   ```

### Project Structure

```
TODO-IN-MEMORY-CLI-APP/
├── src/
│   ├── main.py              # Application entry point
│   ├── cli/                 # CLI Layer
│   │   ├── menu.py          # Menu display
│   │   └── commands.py      # Command routing
│   ├── logic/               # Logic Layer
│   │   ├── todo_service.py  # CRUD operations
│   │   └── validators.py    # Validation rules
│   └── data/                # Data Layer
│       ├── models.py        # Todo dataclass
│       └── todo_repository.py  # In-memory storage
├── specs/001-phase-1-console-todo/
│   ├── spec.md              # Requirements
│   ├── plan.md              # Architecture
│   ├── data-model.md        # Entity definitions
│   ├── research.md          # Technology choices
│   ├── quickstart.md        # This file
│   └── contracts/           # CLI contracts
└── pyproject.toml           # UV configuration
```

### Architecture Overview

**Three-Layer Architecture** (per constitutional Principle III):

1. **CLI Layer** (`src/cli/`):
   - Handles user input/output
   - Displays menu and formats output
   - Validates input format (numeric IDs, non-empty strings)
   - **Depends on**: Logic layer
   - **No knowledge of**: Data layer internals

2. **Logic Layer** (`src/logic/`):
   - Enforces business rules (empty text check, ID existence)
   - Orchestrates CRUD operations
   - Raises exceptions for validation failures
   - **Depends on**: Data layer
   - **No knowledge of**: CLI (no print statements)

3. **Data Layer** (`src/data/`):
   - Manages in-memory todo storage
   - Assigns unique sequential IDs
   - Provides CRUD operations on storage
   - **Depends on**: Nothing (leaf layer)

**Dependency Flow**: CLI → Logic → Data (one direction, no cycles)

### Development Guidelines

**Adding a New Feature**:
1. Update `specs/001-phase-1-console-todo/spec.md` with requirements
2. Update `specs/001-phase-1-console-todo/plan.md` with design
3. Generate tasks with `/sp.tasks` command
4. Implement following tasks order
5. Validate against spec acceptance criteria

**Code Style**:
- Type hints for all function signatures
- Docstrings for public methods
- One class per file (Single Responsibility Principle)
- Clear naming: `todo_service.py`, `TodoRepository`, `add_todo()`

**Testing** (optional for Phase I):
- Unit tests in `tests/unit/`
- Integration tests in `tests/integration/`
- Run tests: `uv run pytest` (if pytest added)

**Debugging**:
- Add `print()` statements in CLI layer (acceptable for debugging)
- Never add `print()` in Logic or Data layers (violates layer separation)
- Use Python debugger: `python -m pdb src/main.py`

---

## For Evaluators

### Validating Spec-Driven Development Workflow

**Constitutional Workflow** (per Principle I):
```
Constitution → Spec → Plan → Tasks → Implementation
```

**Artifacts to Review**:

1. **Constitution** (`.specify/memory/constitution.md`):
   - ✅ Defines Phase I constraints (in-memory, console-only, Python, no persistence)
   - ✅ Establishes Spec-Driven Development workflow
   - ✅ Mandates Separation of Concerns

2. **Specification** (`specs/001-phase-1-console-todo/spec.md`):
   - ✅ 4 prioritized user stories (P1-P3)
   - ✅ 12 functional requirements (FR-001 to FR-012)
   - ✅ 8 measurable success criteria (SC-001 to SC-008)
   - ✅ Technology-agnostic (no implementation details)

3. **Plan** (`specs/001-phase-1-console-todo/plan.md`):
   - ✅ Technical context (Python 3.13+, stdlib only, in-memory)
   - ✅ Constitution check (all 6 principles validated)
   - ✅ Three-layer architecture (CLI, Logic, Data)
   - ✅ Design decisions with rationale

4. **Research** (`specs/001-phase-1-console-todo/research.md`):
   - ✅ Technology choices documented (menu-driven CLI, dataclass, auto-increment IDs)
   - ✅ Alternatives considered and rejected with rationale
   - ✅ Best practices identified

5. **Data Model** (`specs/001-phase-1-console-todo/data-model.md`):
   - ✅ Entity definitions (Todo, TodoRepository)
   - ✅ State transitions (Created → Active → Completed/Deleted)
   - ✅ Validation rules (text non-empty, ID exists)

6. **Contracts** (`specs/001-phase-1-console-todo/contracts/cli-commands.md`):
   - ✅ CLI command specifications (6 commands)
   - ✅ Input/output formats
   - ✅ Error handling standards

7. **Tasks** (`specs/001-phase-1-console-todo/tasks.md`):
   - ⏳ To be generated by `/sp.tasks` command
   - ✅ Will reference spec requirements and plan architecture

8. **Implementation** (`src/` directory):
   - ⏳ To be generated by `/sp.implement` command
   - ✅ Will follow task order and architecture from plan

### Validation Checklist

**✅ Constitutional Compliance**:
- [ ] Phase I constraints enforced (in-memory, console-only, Python, no persistence)
- [ ] Spec-Driven Development workflow followed (no code before spec/plan/tasks)
- [ ] Separation of Concerns implemented (CLI/Logic/Data layers)
- [ ] Deterministic behavior (sequential IDs, no randomness)
- [ ] Documentation complete (spec, plan, research, data-model, contracts)

**✅ Specification Traceability**:
- [ ] All functional requirements (FR-001 to FR-012) addressed in plan
- [ ] All user stories (P1-P3) covered by architecture
- [ ] All success criteria (SC-001 to SC-008) testable from implementation

**✅ Architecture Quality**:
- [ ] Three layers clearly separated (CLI, Logic, Data)
- [ ] One-directional dependencies (CLI → Logic → Data)
- [ ] Each layer independently testable
- [ ] Design decisions documented with rationale

**✅ Implementation Readiness**:
- [ ] All unknowns resolved in research.md
- [ ] Data model fully specified (entities, attributes, relationships)
- [ ] CLI contracts defined (6 commands with input/output/errors)
- [ ] Project structure planned (src/ layout with modules)

### Testing the Application

**Manual Validation** (matches spec acceptance criteria):

1. **User Story 1 - Add and View Todos** (Priority P1):
   ```
   Test: Add todo "Buy groceries"
   Expected: System confirms with ID 1
   ✅ Pass if: Success message shows "Added todo #1"

   Test: View all todos
   Expected: Displays ID, text, status
   ✅ Pass if: Shows "1 [ ] Buy groceries"

   Test: Add empty text
   Expected: Error message, no todo created
   ✅ Pass if: Error shown, count remains same
   ```

2. **User Story 2 - Mark Todos as Complete** (Priority P2):
   ```
   Test: Mark todo 1 as complete
   Expected: Status updated, confirmation shown
   ✅ Pass if: View shows "1 [✓] Buy groceries"

   Test: Mark already-complete todo
   Expected: Handled gracefully (idempotent)
   ✅ Pass if: Success message, no error

   Test: Mark non-existent ID
   Expected: Error with suggestion
   ✅ Pass if: "Todo ID X not found" + suggestion
   ```

3. **User Story 3 - Update Todo Text** (Priority P3):
   ```
   Test: Update todo 1 text to "Buy organic groceries"
   Expected: Text changed, confirmation shown
   ✅ Pass if: View shows updated text

   Test: Update with empty text
   Expected: Error, todo unchanged
   ✅ Pass if: Error shown, text remains same
   ```

4. **User Story 4 - Delete Todos** (Priority P3):
   ```
   Test: Delete todo 1
   Expected: Todo removed, confirmation shown
   ✅ Pass if: View no longer shows todo 1

   Test: Delete from list [1, 2, 3], delete 2
   Expected: Only 2 removed, 1 and 3 remain
   ✅ Pass if: IDs 1 and 3 still present, stable IDs
   ```

**Performance Validation** (per spec NFR-001, NFR-002):
```
Test: Add 100 todos
Expected: Each operation <1 second
✅ Pass if: No noticeable lag

Test: Application startup
Expected: <2 seconds to menu
✅ Pass if: Timed startup under threshold
```

### Reporting Issues

If validation fails:

1. **Check Constitutional Compliance**: Does implementation violate Phase I constraints?
2. **Check Spec Traceability**: Does architecture address all functional requirements?
3. **Check Layer Separation**: Does CLI/Logic/Data have clear boundaries?
4. **Document Finding**: Specify which requirement/principle violated
5. **Suggest Correction**: Reference spec or constitution for expected behavior

---

## Troubleshooting

### Common Issues

**Issue**: `Command not found: uv`
- **Solution**: Install UV following [official instructions](https://github.com/astral-sh/uv)

**Issue**: `Python version 3.12 detected, need 3.13+`
- **Solution**: Upgrade Python to 3.13+ or use `uv python install 3.13`

**Issue**: Application exits immediately
- **Solution**: Check `src/main.py` exists and contains entry point

**Issue**: Menu not displaying correctly
- **Solution**: Ensure terminal supports UTF-8 encoding

**Issue**: Todos not persisting between runs
- **Solution**: This is expected behavior for Phase I (in-memory only)

---

## Next Steps

### After Phase I Completion

1. **Phase II - Web Application**:
   - Replace CLI layer with Next.js frontend
   - Replace in-memory storage with Neon DB (PostgreSQL)
   - Reuse Logic layer in FastAPI backend
   - Reference: Constitutional Phase II constraints

2. **Phase III - AI-Powered Chatbot**:
   - Add natural language interface
   - Integrate OpenAI ChatKit + Anthropic Agents SDK
   - Use MCP for model context
   - Reference: Constitutional Phase III constraints

3. **Phase IV - Kubernetes Deployment**:
   - Containerize with Docker
   - Deploy to local Minikube cluster
   - Use Helm for configuration
   - Reference: Constitutional Phase IV constraints

4. **Phase V - Cloud Production**:
   - Event streaming with Kafka
   - Service orchestration with Dapr
   - Deploy to DigitalOcean DOKS
   - Reference: Constitutional Phase V constraints

---

## References

- **Spec**: [spec.md](./spec.md) - Requirements and user stories
- **Plan**: [plan.md](./plan.md) - Architecture and design
- **Constitution**: [.specify/memory/constitution.md](../../.specify/memory/constitution.md) - Project principles
- **UV Documentation**: https://github.com/astral-sh/uv
- **Python Documentation**: https://docs.python.org/3.13/

---

## Support

For questions or issues:
1. Review spec and plan documentation
2. Check troubleshooting section above
3. Verify constitutional constraints for Phase I
4. Consult evaluators/stakeholders for clarification

---

## Revision History

| Date | Change | Rationale |
|------|--------|-----------|
| 2026-01-01 | Initial quickstart | Phase 1 of `/sp.plan` workflow |
