"""Repository for managing todo items in memory."""

from typing import List
from .models import Todo


class TodoRepository:
    """Manages in-memory storage and retrieval of todo items.

    This class encapsulates the storage implementation so it can be swapped
    for a database-backed version in Phase II without affecting other layers.

    Attributes:
        _todos: Private list storing all todo items
        _next_id: Auto-increment counter for unique ID assignment
    """

    def __init__(self):
        """Initialize an empty todo repository."""
        self._todos: List[Todo] = []
        self._next_id: int = 1

    def add(self, text: str) -> Todo:
        """Create and add a new todo item.

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

    def get_all(self) -> List[Todo]:
        """Retrieve all todos.

        Returns:
            List of all Todo items (may be empty)
        """
        return self._todos.copy()

    def get_by_id(self, todo_id: int) -> Todo:
        """Retrieve a specific todo by ID.

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

    def update(self, todo_id: int, text: str) -> Todo:
        """Update a todo's text.

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

        todo = self.get_by_id(todo_id)
        todo.text = text
        return todo

    def delete(self, todo_id: int) -> None:
        """Delete a todo by ID.

        Args:
            todo_id: The ID of the todo to delete

        Raises:
            KeyError: If no todo with that ID exists
        """
        todo = self.get_by_id(todo_id)
        self._todos.remove(todo)

    def mark_complete(self, todo_id: int) -> Todo:
        """Mark a todo as complete.

        This operation is idempotent - calling it on an already-completed
        todo succeeds without error.

        Args:
            todo_id: The ID of the todo to mark complete

        Returns:
            The updated Todo

        Raises:
            KeyError: If no todo with that ID exists
        """
        todo = self.get_by_id(todo_id)
        todo.completed = True
        return todo
