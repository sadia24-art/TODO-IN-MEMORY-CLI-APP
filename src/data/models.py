"""Data models for the todo application."""

from dataclasses import dataclass


@dataclass
class Todo:
    """Represents a single todo item.

    Attributes:
        id: Unique identifier (sequential, starts at 1)
        text: Description of the todo task
        completed: Completion status (True if done, False otherwise)
    """
    id: int
    text: str
    completed: bool = False

    def __str__(self) -> str:
        """Human-readable representation for CLI display."""
        status = "✓" if self.completed else " "
        return f"{self.id}. [{status}] {self.text}"
