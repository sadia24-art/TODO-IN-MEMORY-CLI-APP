"""Main entry point for the TODO application."""

from src.data.todo_repository import TodoRepository
from src.logic.todo_service import TodoService
from src.cli.menu import (
    display_header,
    display_main_menu,
    get_menu_choice,
    display_goodbye
)
from src.cli.commands import (
    handle_add_todo,
    handle_view_todos,
    handle_mark_complete,
    handle_update_todo,
    handle_delete_todo
)


def main():
    """Main application loop."""
    # Initialize data and service layers
    repository = TodoRepository()
    service = TodoService(repository)

    # Display welcome header
    display_header()

    try:
        # Main menu loop
        while True:
            display_main_menu()
            choice = get_menu_choice()

            if choice == "1":
                handle_add_todo(service)
            elif choice == "2":
                handle_view_todos(service)
            elif choice == "3":
                handle_mark_complete(service)
            elif choice == "4":
                handle_update_todo(service)
            elif choice == "5":
                handle_delete_todo(service)
            elif choice == "6":
                display_goodbye()
                break

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\n\nInterrupted by user.")
        display_goodbye()
    except Exception as e:
        # Catch unexpected errors
        print(f"\n❌ Unexpected error: {e}")
        print("💡 Please report this issue if it persists.")
    finally:
        # Clean exit
        return 0


if __name__ == "__main__":
    exit(main())
