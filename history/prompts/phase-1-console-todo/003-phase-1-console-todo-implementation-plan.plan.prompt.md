---
id: 003
title: Phase 1 Console Todo Implementation Plan
stage: plan
date: 2026-01-01
surface: agent
model: claude-sonnet-4-5
feature: phase-1-console-todo
branch: 001-phase-1-console-todo
user: HP FOLIO 1040
command: /sp.plan
labels: ["plan", "phase-1", "architecture", "three-layer", "python", "in-memory"]
links:
  spec: specs/001-phase-1-console-todo/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-phase-1-console-todo/plan.md
  - specs/001-phase-1-console-todo/research.md
  - specs/001-phase-1-console-todo/data-model.md
  - specs/001-phase-1-console-todo/contracts/cli-commands.md
  - specs/001-phase-1-console-todo/quickstart.md
tests:
  - N/A (planning stage, no code yet)
---

## Prompt

```text
/sp.plan

Project: In-Memory Python Console Todo App (Phase I)

Architecture:
Layered console application with strict separation of concerns.

Components:
- CLI: input/output, menu, command routing
- Logic: add, delete, update, view, mark complete
- Data: in-memory todo storage (runtime only)

Flow:
User → CLI → Logic → In-Memory Data → CLI

Structure:
- Single entry point
- Separate modules for CLI, logic, and data

Rules:
- Spec → Plan → Tasks → Implement
- No persistence, no external services

Outcome:
Simple, deterministic console todo app for agentic, spec-driven evaluation.
```

## Response snapshot

Created comprehensive implementation plan with complete architecture design for Phase I in-memory Python console todo application.

**Plan Structure:**

**Technical Context:**
- Language: Python 3.13+, stdlib only
- Storage: In-memory (lists/dicts, no persistence)
- Testing: pytest optional (tests not required per spec)
- Platform: Cross-platform (Windows/macOS/Linux)
- Performance: <1s response, <2s startup, <50MB memory
- Scale: 1-100 todos per session

**Constitution Check (All Principles PASS):**
1. ✅ Spec-Driven Development: Spec → Plan → Tasks workflow followed
2. ✅ Incremental Phase Evolution: Architecture supports Phase II+ evolution
3. ✅ Separation of Concerns: Three layers (CLI → Logic → Data)
4. ✅ Deterministic Behavior: Sequential IDs, no randomness
5. ✅ Documentation Completeness: 5 artifacts created (plan, research, data-model, contracts, quickstart)
6. ✅ Test-Driven Development: Optional tests, architecture supports future testing

**Project Structure:**
- Single project layout (src/ with cli/, logic/, data/ subdirectories)
- Clear layer boundaries with one-directional dependencies
- 7 Python modules planned (main.py, menu.py, commands.py, todo_service.py, validators.py, models.py, todo_repository.py)

**Phase 0: Research & Technology Choices (research.md):**
1. CLI Framework: Menu-driven with raw input() (stdlib, simple)
2. Data Structure: @dataclass with type hints (mutable, clean syntax)
3. ID Management: Auto-increment counter (deterministic, stable IDs)
4. Error Handling: Exceptions (Pythonic, clean separation)
5. Development Tooling: UV (spec requirement, fast, reproducible)

**Key Decisions:**
- Menu-driven interface (vs command-line args) for interactive sessions
- Three layers (vs monolithic) for Phase II evolution support
- Auto-increment counter (vs list index) for stable todo IDs
- Exceptions (vs return codes) for Pythonic error handling

**Phase 1: Design & Contracts (data-model.md, contracts/cli-commands.md):**

**Data Model:**
- Todo Entity: id (int), text (str), completed (bool)
- TodoRepository: _todos (List[Todo]), _next_id (int), 6 CRUD methods
- State Transitions: Created → Active → Completed/Deleted
- Validation Rules: text non-empty after strip, ID must exist, idempotent completion

**CLI Contracts:**
- 6 commands specified: Add, View, Mark Complete, Update, Delete, Exit
- Each with input/output/error formats
- Error message standard: "❌ Error: [problem] 💡 Suggestion: [solution]"
- Acceptance criteria mapped to spec user stories

**Architecture Diagram:**
```
User → CLI Layer (menu.py, commands.py)
         ↓
     Logic Layer (todo_service.py, validators.py)
         ↓
     Data Layer (models.py, todo_repository.py)
```

**Quickstart Guide (quickstart.md):**
- User guide: 3-step setup (navigate, run, follow menu)
- Developer guide: Project structure, architecture overview, development guidelines
- Evaluator guide: Validation checklist, testing procedures, traceability matrix

**Design Alternatives Considered:**
1. Single-layer vs three-layer → Rejected monolithic (violates Principle III, hard to evolve)
2. click library vs stdlib → Rejected click (external dependency violates Phase I constraint)
3. JSON persistence vs in-memory → Rejected persistence (violates Phase I constraint, contradicts SC-008)
4. List index as ID vs auto-increment → Rejected index (IDs change on deletion, non-deterministic)

**Constitutional Re-Check (Post-Design):**
All 6 principles validated again after architecture design:
✅ Spec-Driven: Design traceable to spec (FR-001 to FR-012, NFR-001 to NFR-014)
✅ Phase Evolution: Data layer swappable for DB (Phase II), Logic reusable in FastAPI
✅ Separation: Three layers, no circular dependencies, independently testable
✅ Deterministic: ID assignment sequential, state transitions explicit
✅ Documentation: 5 artifacts complete (plan, research, data-model, contracts, quickstart)
✅ Testing: Optional per spec, architecture supports future tests

## Outcome

- ✅ Impact: Complete implementation plan with architecture, data model, contracts, and quickstart guide ready for task generation
- 🧪 Tests: N/A (planning stage, no code implementation yet)
- 📁 Files: Created 5 planning artifacts (plan.md, research.md, data-model.md, cli-commands.md, quickstart.md)
- 🔁 Next prompts: `/sp.tasks` to generate implementation tasks from architecture
- 🧠 Reflection: Architecture successfully balances Phase I simplicity (in-memory, console) with Phase II+ evolution (layered structure). All constitutional checks pass. No blocking issues identified.

## Evaluation notes (flywheel)

- Failure modes observed: None - all constitutional gates passed, design complete
- Graders run and results (PASS/FAIL): Constitutional Check PASS (6/6 principles validated twice)
- Prompt variant (if applicable): N/A (standard planning workflow)
- Next experiment (smallest change to try): Proceed to `/sp.tasks` to validate architecture completeness through concrete task decomposition
