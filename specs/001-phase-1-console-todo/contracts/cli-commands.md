# CLI Command Contracts: In-Memory Python Console Todo Application (Phase I)

**Date**: 2026-01-01
**Feature**: [spec.md](../spec.md)
**Plan**: [plan.md](../plan.md)

## Purpose

Define the command-line interface contracts for Phase I todo application. Specifies menu structure, command flows, input/output formats, and error handling. Serves as the interface specification between CLI layer and Logic layer.

---

## Menu Structure

### Main Menu Display

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

**Display Requirements**:
- Clear header with application name and phase
- Numbered options (1-6) for easy selection
- Data loss warning visible on every menu display
- Input prompt clearly indicates valid range

**User Interaction**:
- User types number (1-6) and presses Enter
- Invalid input (non-numeric, out of range) shows error and re-displays menu
- Menu loops until user selects option 6 (Exit)

---

## Command Specifications

### Command 1: Add Todo

**Purpose**: Create a new todo item with user-provided text

**Flow**:
```
User selects: 1
App prompts:  Enter todo description:
User types:   Buy groceries
App responds: ✅ Added todo #1: "Buy groceries"
App action:   Return to main menu
```

**Input Requirements**:
- **Prompt**: `"Enter todo description: "`
- **Input**: String (any length, UTF-8 encoded)
- **Processing**: Text stripped of leading/trailing whitespace before validation

**Output Success**:
```
✅ Added todo #<ID>: "<text>"
```
- `<ID>`: Auto-assigned sequential ID
- `<text>`: The actual todo text (after stripping)

**Output Error**:
```
❌ Error: Todo text cannot be empty
💡 Suggestion: Enter a description for your todo
```

**Error Conditions**:
1. **Empty Input**: User presses Enter without typing anything
2. **Whitespace Only**: User types only spaces/tabs (e.g., "   ")

**Contract**:
```python
# CLI Layer calls Logic Layer
try:
    todo = service.add_todo(user_input)
    display_success(f"✅ Added todo #{todo.id}: \"{todo.text}\"")
except ValueError as e:
    display_error(f"❌ Error: {e}")
    display_suggestion("💡 Suggestion: Enter a description for your todo")
```

**Acceptance Criteria** (from spec.md User Story 1):
1. User adds todo "Buy groceries" → System confirms with ID
2. User provides empty text → System shows error, does not create todo

---

### Command 2: View All Todos

**Purpose**: Display all todo items with their ID, text, and completion status

**Flow**:
```
User selects: 2
App displays: (see format below)
App action:   Return to main menu
```

**Output Format (With Todos)**:
```
==========================================
            Your Todos
==========================================

ID   Status   Description
--   ------   -----------
1    [ ]      Buy groceries
2    [✓]      Call mom
3    [ ]      Finish project

------------------------------------------
Total: 3 todos (1 completed, 2 pending)
==========================================
```

**Output Format (Empty List)**:
```
==========================================
            Your Todos
==========================================

No todos yet!
💡 Suggestion: Select 'Add todo' (option 1) to create your first task

==========================================
```

**Display Requirements**:
- **ID Column**: Left-aligned, shows todo ID
- **Status Column**: `[ ]` for incomplete, `[✓]` for complete
- **Description Column**: Left-aligned, todo text (truncate if > 50 chars, add "...")
- **Summary Line**: Total count, completed count, pending count
- **Empty State**: Helpful message with suggestion

**Contract**:
```python
# CLI Layer calls Logic Layer
todos = service.view_all()  # Returns List[Todo]

if not todos:
    display_empty_state()
else:
    display_todo_table(todos)
    display_summary(len(todos), count_completed(todos))
```

**Acceptance Criteria** (from spec.md User Story 1):
1. User views list with 3 todos → System displays all 3 with id, text, status

---

### Command 3: Mark Todo as Complete

**Purpose**: Change a todo's completion status from incomplete to complete

**Flow**:
```
User selects: 3
App prompts:  Enter todo ID to mark complete:
User types:   1
App responds: ✅ Marked todo #1 as complete
App action:   Return to main menu
```

**Input Requirements**:
- **Prompt**: `"Enter todo ID to mark complete: "`
- **Input**: Positive integer (todo ID)
- **Processing**: Convert to int, validate exists

**Output Success**:
```
✅ Marked todo #<ID> as complete
```

**Output Error (ID Not Found)**:
```
❌ Error: Todo ID <ID> not found
💡 Suggestion: Use 'View all todos' (option 2) to see valid IDs
```

**Output Error (Non-Numeric Input)**:
```
❌ Error: Invalid input - please enter a number
💡 Suggestion: Enter the ID number of the todo you want to complete
```

**Idempotent Behavior**:
- Marking an already-completed todo as complete again succeeds without error
- Same success message displayed: `"✅ Marked todo #<ID> as complete"`
- Rationale: User intent is "ensure todo is complete" (idempotent operation)

**Contract**:
```python
# CLI Layer
user_input = input("Enter todo ID to mark complete: ").strip()

if not user_input.isdigit():
    display_error("❌ Error: Invalid input - please enter a number")
    display_suggestion("💡 Suggestion: Enter the ID number of the todo you want to complete")
    return

todo_id = int(user_input)

# Logic Layer
try:
    todo = service.mark_complete(todo_id)
    display_success(f"✅ Marked todo #{todo.id} as complete")
except KeyError:
    display_error(f"❌ Error: Todo ID {todo_id} not found")
    display_suggestion("💡 Suggestion: Use 'View all todos' (option 2) to see valid IDs")
```

**Acceptance Criteria** (from spec.md User Story 2):
1. User marks todo 1 as complete → Status updated, confirmation shown
2. User attempts to mark already-complete todo → Handled gracefully (success message)
3. User provides non-existent ID → Error shown with suggestion

---

### Command 4: Update Todo

**Purpose**: Change the text description of an existing todo

**Flow**:
```
User selects: 4
App prompts:  Enter todo ID to update:
User types:   1
App prompts:  Enter new description:
User types:   Buy organic groceries
App responds: ✅ Updated todo #1
App action:   Return to main menu
```

**Input Requirements**:
- **First Prompt**: `"Enter todo ID to update: "`
- **First Input**: Positive integer (todo ID)
- **Second Prompt**: `"Enter new description: "`
- **Second Input**: String (any length, UTF-8 encoded)
- **Processing**: Text stripped, ID validated

**Output Success**:
```
✅ Updated todo #<ID>
```

**Output Error (ID Not Found)**:
```
❌ Error: Todo ID <ID> not found
💡 Suggestion: Use 'View all todos' (option 2) to see valid IDs
```

**Output Error (Empty Text)**:
```
❌ Error: Todo text cannot be empty
💡 Suggestion: Enter a new description for the todo
```

**Output Error (Non-Numeric ID)**:
```
❌ Error: Invalid input - please enter a number
💡 Suggestion: Enter the ID number of the todo you want to update
```

**Contract**:
```python
# CLI Layer
id_input = input("Enter todo ID to update: ").strip()

if not id_input.isdigit():
    display_error("❌ Error: Invalid input - please enter a number")
    display_suggestion("💡 Suggestion: Enter the ID number of the todo you want to update")
    return

todo_id = int(id_input)
new_text = input("Enter new description: ")

# Logic Layer
try:
    todo = service.update_todo(todo_id, new_text)
    display_success(f"✅ Updated todo #{todo.id}")
except KeyError:
    display_error(f"❌ Error: Todo ID {todo_id} not found")
    display_suggestion("💡 Suggestion: Use 'View all todos' (option 2) to see valid IDs")
except ValueError as e:
    display_error(f"❌ Error: {e}")
    display_suggestion("💡 Suggestion: Enter a new description for the todo")
```

**Acceptance Criteria** (from spec.md User Story 3):
1. User updates todo 1 text → Text changed, confirmation shown
2. User provides non-existent ID → Error shown
3. User provides empty text → Error shown, todo unchanged

---

### Command 5: Delete Todo

**Purpose**: Remove a todo item from the list permanently

**Flow**:
```
User selects: 5
App prompts:  Enter todo ID to delete:
User types:   1
App responds: ✅ Deleted todo #1
App action:   Return to main menu
```

**Input Requirements**:
- **Prompt**: `"Enter todo ID to delete: "`
- **Input**: Positive integer (todo ID)
- **Processing**: Convert to int, validate exists

**Output Success**:
```
✅ Deleted todo #<ID>
```

**Output Error (ID Not Found)**:
```
❌ Error: Todo ID <ID> not found
💡 Suggestion: Use 'View all todos' (option 2) to see valid IDs
```

**Output Error (Non-Numeric Input)**:
```
❌ Error: Invalid input - please enter a number
💡 Suggestion: Enter the ID number of the todo you want to delete
```

**Permanent Action**:
- Deletion is immediate and irreversible (no undo in Phase I)
- ID is not reused (auto-increment counter never decrements)
- Other todos' IDs remain unchanged

**Contract**:
```python
# CLI Layer
user_input = input("Enter todo ID to delete: ").strip()

if not user_input.isdigit():
    display_error("❌ Error: Invalid input - please enter a number")
    display_suggestion("💡 Suggestion: Enter the ID number of the todo you want to delete")
    return

todo_id = int(user_input)

# Logic Layer
try:
    service.delete_todo(todo_id)
    display_success(f"✅ Deleted todo #{todo_id}")
except KeyError:
    display_error(f"❌ Error: Todo ID {todo_id} not found")
    display_suggestion("💡 Suggestion: Use 'View all todos' (option 2) to see valid IDs")
```

**Acceptance Criteria** (from spec.md User Story 4):
1. User deletes todo 1 → Todo removed, confirmation shown
2. User provides non-existent ID → Error shown
3. User deletes todo 2 from list [1, 2, 3] → Only todo 2 removed, IDs 1 and 3 remain

---

### Command 6: Exit

**Purpose**: Gracefully terminate the application with data loss warning

**Flow**:
```
User selects: 6
App displays: ==========================================
              Goodbye! Thanks for using TODO App

              ⚠️  All todos have been lost
              (Data is not saved between sessions)
              ==========================================
App action:   Exit program (return code 0)
```

**Output Requirements**:
- Clear goodbye message
- Explicit data loss reminder
- Clean exit (no error messages)

**Contract**:
```python
# CLI Layer
display_goodbye()
exit(0)  # Return code 0 indicates successful exit
```

**Acceptance Criteria**:
1. User selects exit → Application terminates with goodbye message
2. Data loss warning displayed before exit

---

## Error Handling Standards

### Error Message Format

**Template**:
```
❌ Error: [What went wrong]
💡 Suggestion: [How to fix it]
```

**Requirements** (per spec NFR-005):
- **Clarity**: Specify exact problem ("Todo ID 5 not found" not "Invalid input")
- **Actionable**: Suggest corrective action ("Use 'View all todos' to see valid IDs")
- **User-Friendly**: Plain English, no technical jargon

**Examples**:
```
❌ Error: Todo text cannot be empty
💡 Suggestion: Enter a description for your todo

❌ Error: Todo ID 10 not found
💡 Suggestion: Use 'View all todos' (option 2) to see valid IDs

❌ Error: Invalid input - please enter a number
💡 Suggestion: Enter a number between 1 and 6

❌ Error: Invalid choice
💡 Suggestion: Please select a number between 1 and 6
```

---

### Exception Mapping

| Exception | Meaning | CLI Action |
|-----------|---------|------------|
| `ValueError` | Invalid input (empty text, non-numeric where numeric expected) | Display error + suggestion, return to menu |
| `KeyError` | Todo ID not found | Display error + suggestion, return to menu |
| `RuntimeError` | Unexpected state (shouldn't occur if logic correct) | Display generic error, log for debugging |
| `KeyboardInterrupt` (Ctrl+C) | User forcefully exits | Display goodbye message, clean exit |

---

## Input Validation Rules

### Menu Choice Validation

**Valid Input**: Single digit 1-6
**Invalid Examples**:
- Empty (just Enter)
- Non-numeric ("abc", "one")
- Out of range ("0", "7", "99")
- Multiple digits as non-valid option ("12")

**Validation Flow**:
```python
choice = input("Enter your choice (1-6): ").strip()

if not choice.isdigit():
    display_error("❌ Error: Invalid input - please enter a number")
    display_suggestion("💡 Suggestion: Enter a number between 1 and 6")
    continue

choice_num = int(choice)

if choice_num < 1 or choice_num > 6:
    display_error("❌ Error: Invalid choice")
    display_suggestion("💡 Suggestion: Please select a number between 1 and 6")
    continue

# Valid choice, proceed
```

---

### Todo ID Validation

**Valid Input**: Positive integer matching existing todo ID
**Invalid Examples**:
- Empty
- Non-numeric ("abc")
- Negative ("-1")
- Zero ("0")
- Non-existent ID ("999")

**Validation Flow**:
```python
id_input = input("Enter todo ID: ").strip()

# Format validation (CLI layer)
if not id_input.isdigit():
    display_error("❌ Error: Invalid input - please enter a number")
    return

todo_id = int(id_input)

# Existence validation (Logic layer)
try:
    todo = service.get_todo(todo_id)
    # Proceed with operation
except KeyError:
    display_error(f"❌ Error: Todo ID {todo_id} not found")
    display_suggestion("💡 Suggestion: Use 'View all todos' to see valid IDs")
```

---

### Todo Text Validation

**Valid Input**: Non-empty string after stripping whitespace
**Invalid Examples**:
- Empty ("")
- Whitespace only ("   ", "\t\n")

**Validation Flow**:
```python
text = input("Enter todo description: ")

# Validation in Logic layer
try:
    todo = service.add_todo(text)  # Strips and validates internally
    display_success(f"✅ Added todo #{todo.id}")
except ValueError as e:
    display_error(f"❌ Error: {e}")
    display_suggestion("💡 Suggestion: Enter a description for your todo")
```

---

## Performance Requirements

Per spec NFR-001, NFR-006:

- **Response Time**: All commands respond within 1 second
- **Self-Documenting**: Menu options clear without external help documentation
- **Discoverability**: All features accessible from main menu (no hidden commands)

---

## Accessibility Considerations

Per spec Assumption #4 (users comfortable with console):

- **Plain Text**: No graphics, colors, or special formatting required (optional for enhancement)
- **UTF-8 Support**: International characters allowed in todo text (spec Assumption #5)
- **Screen Reader Compatible**: Text-based interface readable by assistive technology

---

## References

- **Spec**: [spec.md](../spec.md) - User stories and acceptance criteria
- **Plan**: [plan.md](../plan.md) - Architecture and layer responsibilities
- **Data Model**: [data-model.md](../data-model.md) - Todo entity and validation rules

---

## Revision History

| Date | Change | Rationale |
|------|--------|-----------|
| 2026-01-01 | Initial CLI contracts | Phase 1 of `/sp.plan` workflow |
