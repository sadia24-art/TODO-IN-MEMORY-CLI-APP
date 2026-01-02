"""Command handlers for CLI operations."""

from src.logic.todo_service import TodoService
from src.logic.validators import validate_todo_id


def display_error(message: str):
    """Display an error message in standard format.

    Args:
        message: The error message to display
    """
    print(f"❌ Error: {message}")


def display_suggestion(message: str):
    """Display a suggestion message in standard format.

    Args:
        message: The suggestion message to display
    """
    print(f"💡 Suggestion: {message}")


def handle_add_todo(service: TodoService):
    """Handle the 'Add todo' command.

    Args:
        service: TodoService instance for business operations
    """
    print("\n--- Add Todo ---")
    text = input("Enter todo description: ").strip()

    try:
        todo = service.add_todo(text)
        print(f"✅ Success: Added todo #{todo.id}: {todo.text}")
    except ValueError as e:
        display_error(str(e))
        display_suggestion("Enter a description for your todo")


def handle_view_todos(service: TodoService):
    """Handle the 'View all todos' command.

    Args:
        service: TodoService instance for business operations
    """
    print("\n--- All Todos ---")
    todos = service.view_all()

    if not todos:
        print("No todos yet.")
        display_suggestion("Select 'Add todo' to create one")
        return

    print("\nID  | Status | Description")
    print("-" * 50)
    for todo in todos:
        status = "✓" if todo.completed else " "
        print(f"{todo.id:<3} | [{status}]    | {todo.text}")
    print()


def handle_mark_complete(service: TodoService):
    """Handle the 'Mark complete' command.

    Args:
        service: TodoService instance for business operations
    """
    print("\n--- Mark Todo as Complete ---")
    id_str = input("Enter todo ID: ").strip()

    try:
        todo_id = validate_todo_id(id_str)
        todo = service.mark_complete(todo_id)
        print(f"✅ Success: Marked todo #{todo.id} as complete")
    except ValueError as e:
        display_error(str(e))
        display_suggestion("Enter a valid todo ID number")
    except KeyError as e:
        display_error(str(e))
        display_suggestion("Use 'View all todos' to see valid IDs")


def handle_update_todo(service: TodoService):
    """Handle the 'Update todo' command.

    Args:
        service: TodoService instance for business operations
    """
    print("\n--- Update Todo ---")
    id_str = input("Enter todo ID: ").strip()

    try:
        todo_id = validate_todo_id(id_str)
        new_text = input("Enter new description: ").strip()
        todo = service.update_todo(todo_id, new_text)
        print(f"✅ Success: Updated todo #{todo.id}: {todo.text}")
    except ValueError as e:
        display_error(str(e))
        display_suggestion("Enter a valid todo ID and non-empty description")
    except KeyError as e:
        display_error(str(e))
        display_suggestion("Use 'View all todos' to see valid IDs")


def handle_delete_todo(service: TodoService):
    """Handle the 'Delete todo' command.

    Args:
        service: TodoService instance for business operations
    """
    print("\n--- Delete Todo ---")
    id_str = input("Enter todo ID: ").strip()

    try:
        todo_id = validate_todo_id(id_str)
        service.delete_todo(todo_id)
        print(f"✅ Success: Deleted todo #{todo_id}")
    except ValueError as e:
        display_error(str(e))
        display_suggestion("Enter a valid todo ID number")
    except KeyError as e:
        display_error(str(e))
        display_suggestion("Use 'View all todos' to see valid IDs")
