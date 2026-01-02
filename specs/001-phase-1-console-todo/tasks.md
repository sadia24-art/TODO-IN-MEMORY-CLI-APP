---

description: "Task list for Phase I in-memory Python console todo application"
---

# Tasks: In-Memory Python Console Todo Application (Phase I)

**Input**: Design documents from `/specs/001-phase-1-console-todo/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are OPTIONAL for Phase I per specification. No test tasks included in this implementation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root (this project uses single project structure)
- Paths shown below use repository root structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project directory structure (src/, src/cli/, src/logic/, src/data/)
- [X] T002 Initialize Python project with UV (pyproject.toml, .python-version with 3.13)
- [X] T003 [P] Create package markers (src/__init__.py, src/cli/__init__.py, src/logic/__init__.py, src/data/__init__.py)
- [X] T004 [P] Create README.md with project overview and setup instructions

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Create Todo dataclass in src/data/models.py (id: int, text: str, completed: bool = False)
- [X] T006 Create TodoRepository class in src/data/todo_repository.py (initialization with _todos list and _next_id counter)
- [X] T007 Implement TodoRepository.add(text) method in src/data/todo_repository.py (validates text, creates Todo, increments ID)
- [X] T008 Implement TodoRepository.get_all() method in src/data/todo_repository.py (returns copy of todos list)
- [X] T009 Implement TodoRepository.get_by_id(todo_id) method in src/data/todo_repository.py (finds todo or raises KeyError)
- [X] T010 Implement TodoRepository.update(todo_id, text) method in src/data/todo_repository.py (updates text, validates non-empty)
- [X] T011 Implement TodoRepository.delete(todo_id) method in src/data/todo_repository.py (removes todo from list)
- [X] T012 Implement TodoRepository.mark_complete(todo_id) method in src/data/todo_repository.py (sets completed=True, idempotent)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add and View Todos (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new todos and view all existing todos (core MVP functionality)

**Independent Test**: Start application, add multiple todos, view list showing all todos with ID/text/status

### Implementation for User Story 1

- [X] T013 [P] [US1] Create text validation function in src/logic/validators.py (validate_todo_text, strips and checks non-empty)
- [X] T014 [US1] Create TodoService class in src/logic/todo_service.py (initialize with TodoRepository instance)
- [X] T015 [US1] Implement TodoService.add_todo(text) in src/logic/todo_service.py (validates via validators.py, calls repository.add)
- [X] T016 [US1] Implement TodoService.view_all() in src/logic/todo_service.py (calls repository.get_all)
- [X] T017 [P] [US1] Create menu display function in src/cli/menu.py (display_main_menu with 6 numbered options and data loss warning)
- [X] T018 [P] [US1] Create input helper in src/cli/menu.py (get_menu_choice function with validation for 1-6 range)
- [X] T019 [US1] Create command handler for Add in src/cli/commands.py (handle_add_todo, prompts for text, calls service.add_todo, displays success/error)
- [X] T020 [US1] Create command handler for View in src/cli/commands.py (handle_view_todos, calls service.view_all, formats table output or empty state message)
- [X] T021 [US1] Create main application loop in src/main.py (initialize repository and service, display menu, route commands 1 and 2, handle exit)
- [X] T022 [US1] Add error message formatting in src/cli/commands.py (display_error and display_suggestion functions following "❌ Error" + "💡 Suggestion" format)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Users can add todos and view the complete list.

---

## Phase 4: User Story 2 - Mark Todos as Complete (Priority: P2)

**Goal**: Enable users to mark specific todos as complete to track progress

**Independent Test**: Add todos using US1 functionality, mark specific items complete, verify status changes in view

### Implementation for User Story 2

- [X] T023 [P] [US2] Create ID validation function in src/logic/validators.py (validate_todo_id, checks numeric format)
- [X] T024 [US2] Implement TodoService.mark_complete(todo_id) in src/logic/todo_service.py (calls repository.mark_complete, handles KeyError)
- [X] T025 [US2] Create command handler for Mark Complete in src/cli/commands.py (handle_mark_complete, prompts for ID, validates numeric, calls service.mark_complete, displays success/error)
- [X] T026 [US2] Add Mark Complete command routing in src/main.py (route menu option 3 to handle_mark_complete)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. Users can add, view, and mark todos complete.

---

## Phase 5: User Story 3 - Update Todo Text (Priority: P3)

**Goal**: Enable users to edit the text of existing todos

**Independent Test**: Add a todo, update its text with new description, verify change persists in view

### Implementation for User Story 3

- [X] T027 [US3] Implement TodoService.update_todo(todo_id, text) in src/logic/todo_service.py (validates text via validators.py, calls repository.update, handles KeyError)
- [X] T028 [US3] Create command handler for Update in src/cli/commands.py (handle_update_todo, prompts for ID and new text, validates both, calls service.update_todo, displays success/error)
- [X] T029 [US3] Add Update command routing in src/main.py (route menu option 4 to handle_update_todo)

**Checkpoint**: User Stories 1, 2, AND 3 should all work independently. Users can add, view, mark complete, and update todos.

---

## Phase 6: User Story 4 - Delete Todos (Priority: P3)

**Goal**: Enable users to remove todos from the list

**Independent Test**: Add multiple todos, delete specific items by ID, verify only selected todos removed and others remain with stable IDs

### Implementation for User Story 4

- [X] T030 [US4] Implement TodoService.delete_todo(todo_id) in src/logic/todo_service.py (calls repository.delete, handles KeyError)
- [X] T031 [US4] Create command handler for Delete in src/cli/commands.py (handle_delete_todo, prompts for ID, validates numeric, calls service.delete_todo, displays success/error)
- [X] T032 [US4] Add Delete command routing in src/main.py (route menu option 5 to handle_delete_todo)

**Checkpoint**: All user stories (1, 2, 3, 4) should now be independently functional. Users have complete CRUD + completion tracking.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final touches

- [X] T033 [P] Add application header/branding to src/cli/menu.py (display_header with "TODO APP - Phase I" title)
- [X] T034 [P] Add goodbye message to src/cli/menu.py (display_goodbye with data loss warning)
- [X] T035 Update exit handler in src/main.py (display goodbye message, clean exit with return code 0)
- [X] T036 [P] Add comprehensive error handling in src/main.py (catch KeyboardInterrupt for Ctrl+C, display graceful exit message)
- [X] T037 [P] Verify empty list handling in src/cli/commands.py (handle_view_todos shows helpful message when no todos exist)
- [X] T038 [P] Add input sanitization in src/cli/commands.py (strip whitespace from all text inputs before validation)
- [X] T039 Validate all error messages follow standard format in src/cli/commands.py (all errors show "❌ Error" + "💡 Suggestion")
- [X] T040 [P] Test menu option validation in src/cli/menu.py (get_menu_choice handles non-numeric and out-of-range inputs gracefully)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P3)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Depends on Foundational (Phase 2) - Uses US1 functionality for testing but is independently implementable
- **User Story 3 (P3)**: Depends on Foundational (Phase 2) - Operates on existing todos (can use US1 to create test data)
- **User Story 4 (P3)**: Depends on Foundational (Phase 2) - Operates on existing todos (can use US1 to create test data)

### Within Each User Story

- Models/Repository before Service (Data layer → Logic layer)
- Service before CLI handlers (Logic layer → CLI layer)
- CLI handlers before main routing (Commands → Main loop)
- Core implementation before integration

### Parallel Opportunities

- **Setup Phase**: All tasks marked [P] can run in parallel (T003, T004)
- **Foundational Phase**: Tasks T005-T012 are sequential (build repository capabilities in order)
- **User Story 1**: Tasks T013, T017, T018 can run in parallel (different files, no dependencies)
- **User Story 2**: Task T023 can run in parallel with T024 if working on different files
- **User Story 3**: Single developer path (sequential implementation)
- **User Story 4**: Single developer path (sequential implementation)
- **Polish Phase**: Most tasks marked [P] can run in parallel (T033, T034, T036, T037, T038, T040)

**Cross-Story Parallelization**:
- After Foundational phase completes, all 4 user stories (US1, US2, US3, US4) can be worked on in parallel by different team members
- Each story is independently implementable and testable

---

## Parallel Example: Foundational Phase

```bash
# These tasks MUST run sequentially (building TodoRepository):
Task T005: Create Todo dataclass
Task T006: Create TodoRepository class
Task T007: Implement add() method
Task T008: Implement get_all() method
Task T009: Implement get_by_id() method
Task T010: Implement update() method
Task T011: Implement delete() method
Task T012: Implement mark_complete() method
```

## Parallel Example: User Story 1

```bash
# Launch these tasks together (different files, no dependencies):
Task T013: Create validators.py (validation functions)
Task T017: Create menu.py (display functions)
Task T018: Add get_menu_choice to menu.py (input helper)

# Then run sequentially:
Task T014: Create TodoService class
Task T015: Implement add_todo in TodoService
Task T016: Implement view_all in TodoService
Task T019: Create handle_add_todo command
Task T020: Create handle_view_todos command
Task T021: Create main application loop
Task T022: Add error formatting functions
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T012) - CRITICAL GATE
3. Complete Phase 3: User Story 1 (T013-T022)
4. **STOP and VALIDATE**: Test User Story 1 independently
   - Can add todos? ✓
   - Can view todos with ID/text/status? ✓
   - Empty text rejected? ✓
   - Empty list handled gracefully? ✓
5. If validated, proceed to Phase 4 or deploy MVP

### Incremental Delivery

1. **Foundation + US1 (MVP)**: Core value delivery (add + view todos)
   - Demonstrates Spec-Driven Development workflow
   - Validates architecture (3-layer separation)
   - Provides immediate utility

2. **+ US2 (Mark Complete)**: Enhanced tracking capability
   - Adds progress management
   - Introduces idempotent operations
   - Validates error handling for missing IDs

3. **+ US3 (Update)**: Edit capability
   - Improves user flexibility
   - Validates text validation reuse
   - Completes basic CRUD operations

4. **+ US4 (Delete)**: List management
   - Completes full CRUD + completion
   - Validates ID stability (IDs don't change after deletion)
   - Final feature for Phase I

5. **+ Phase 7 (Polish)**: Professional UX
   - Branding and messaging
   - Comprehensive error handling
   - Production-ready experience

### Parallel Team Strategy

With multiple developers after Foundational phase (T005-T012) complete:

- **Developer A**: User Story 1 (T013-T022) - MVP critical path
- **Developer B**: User Story 2 (T023-T026) - Independent parallel work
- **Developer C**: User Story 3 (T027-T029) - Independent parallel work
- **Developer D**: User Story 4 (T030-T032) - Independent parallel work

Then all converge on Phase 7 (Polish) tasks.

---

## Task File Reference

**Data Layer** (Foundational - Phase 2):
- `src/data/models.py`: T005 (Todo dataclass)
- `src/data/todo_repository.py`: T006-T012 (TodoRepository class and all CRUD methods)

**Logic Layer**:
- `src/logic/validators.py`: T013 (US1 - text validation), T023 (US2 - ID validation)
- `src/logic/todo_service.py`: T014-T016 (US1 - service initialization, add, view), T024 (US2 - mark complete), T027 (US3 - update), T030 (US4 - delete)

**CLI Layer**:
- `src/cli/menu.py`: T017-T018 (US1 - menu display, input handling), T033-T034 (Polish - header, goodbye)
- `src/cli/commands.py`: T019-T020, T022 (US1 - add/view handlers, error formatting), T025 (US2 - mark complete handler), T028 (US3 - update handler), T031 (US4 - delete handler), T037-T039 (Polish - empty list, input sanitization, error validation)

**Main Application**:
- `src/main.py`: T021 (US1 - main loop with add/view routing), T026 (US2 - mark complete routing), T029 (US3 - update routing), T032 (US4 - delete routing), T035-T036 (Polish - exit handler, error handling)

**Project Setup**:
- Root directory: T001 (directory structure), T002 (UV project init), T004 (README)
- Package markers: T003 (__init__.py files)

---

## Notes

- **[P] tasks**: Different files, no dependencies - safe to parallelize
- **[Story] label**: Maps task to specific user story for traceability
- **Each user story is independently completable and testable**
- **No test tasks included** (tests are optional per specification, not requested)
- Commit after each task or logical group for incremental progress
- Stop at any checkpoint to validate story independently
- **Foundational phase (T005-T012) is blocking** - all user stories depend on it
- After Foundational phase, user stories can proceed in any order or in parallel
- **Avoid**: Vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Validation Checklist

After completing all tasks, verify:

- [ ] **Spec Traceability**: All 4 user stories (P1, P2, P3, P3) implemented
- [ ] **Functional Requirements**: FR-001 to FR-012 satisfied
- [ ] **Success Criteria**: SC-001 to SC-008 testable and achievable
- [ ] **Architecture**: Three layers (CLI, Logic, Data) with clear separation
- [ ] **Constitutional Compliance**: Phase I constraints met (in-memory, console-only, Python, no persistence)
- [ ] **User Story Independence**: Each story testable on its own
- [ ] **Error Handling**: All errors follow "❌ Error + 💡 Suggestion" format
- [ ] **ID Stability**: Todo IDs remain stable after deletions (per spec Assumption #10)
- [ ] **Empty State**: Application handles empty todo list gracefully
- [ ] **Exit Behavior**: Application exits cleanly with data loss warning (per SC-008)

---

## Quick Reference: Task Count by Phase

| Phase | Task Count | Description |
|-------|------------|-------------|
| Phase 1: Setup | 4 tasks (T001-T004) | Project initialization |
| Phase 2: Foundational | 8 tasks (T005-T012) | Data layer + TodoRepository (BLOCKING) |
| Phase 3: User Story 1 (P1) | 10 tasks (T013-T022) | Add + View todos (MVP) |
| Phase 4: User Story 2 (P2) | 4 tasks (T023-T026) | Mark complete |
| Phase 5: User Story 3 (P3) | 3 tasks (T027-T029) | Update todo text |
| Phase 6: User Story 4 (P3) | 3 tasks (T030-T032) | Delete todos |
| Phase 7: Polish | 8 tasks (T033-T040) | Cross-cutting improvements |
| **TOTAL** | **40 tasks** | Complete Phase I implementation |

**MVP Scope** (recommended first milestone): Phases 1 + 2 + 3 = 22 tasks (T001-T022)

**Full Feature Set**: All 40 tasks (T001-T040)

**Parallel Opportunities**: 7 tasks marked [P] across all phases (can run simultaneously with others)
