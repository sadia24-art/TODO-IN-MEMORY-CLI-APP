"""Business logic for todo operations."""

from typing import List
from src.data.todo_repository import TodoRepository
from src.data.models import Todo
from .validators import validate_todo_text


class TodoService:
    """Service layer for todo operations.

    This class orchestrates business logic and coordinates between
    the CLI layer and the data layer. It remains stateless - all
    state is managed by the TodoRepository.

    Attributes:
        repository: TodoRepository instance for data operations
    """

    def __init__(self, repository: TodoRepository):
        """Initialize the service with a repository.

        Args:
            repository: TodoRepository instance for data storage
        """
        self.repository = repository

    def add_todo(self, text: str) -> Todo:
        """Add a new todo item.

        Args:
            text: Description of the todo

        Returns:
            The newly created Todo

        Raises:
            ValueError: If text is empty after stripping
        """
        validated_text = validate_todo_text(text)
        return self.repository.add(validated_text)

    def view_all(self) -> List[Todo]:
        """View all todo items.

        Returns:
            List of all Todo items (may be empty)
        """
        return self.repository.get_all()

    def mark_complete(self, todo_id: int) -> Todo:
        """Mark a todo as complete.

        Args:
            todo_id: ID of the todo to mark complete

        Returns:
            The updated Todo

        Raises:
            KeyError: If todo with given ID not found
        """
        return self.repository.mark_complete(todo_id)

    def update_todo(self, todo_id: int, text: str) -> Todo:
        """Update a todo's text.

        Args:
            todo_id: ID of the todo to update
            text: New description

        Returns:
            The updated Todo

        Raises:
            KeyError: If todo with given ID not found
            ValueError: If text is empty after stripping
        """
        validated_text = validate_todo_text(text)
        return self.repository.update(todo_id, validated_text)

    def delete_todo(self, todo_id: int) -> None:
        """Delete a todo.

        Args:
            todo_id: ID of the todo to delete

        Raises:
            KeyError: If todo with given ID not found
        """
        self.repository.delete(todo_id)
