"""Input validation functions for the todo application."""


def validate_todo_text(text: str) -> str:
    """Validate and sanitize todo text.

    Args:
        text: Raw text input from user

    Returns:
        Stripped text

    Raises:
        ValueError: If text is empty after stripping
    """
    text = text.strip()
    if not text:
        raise ValueError("Todo text cannot be empty")
    return text


def validate_todo_id(id_str: str) -> int:
    """Validate and parse todo ID from string input.

    Args:
        id_str: String representation of todo ID

    Returns:
        Parsed integer ID

    Raises:
        ValueError: If id_str is not a valid positive integer
    """
    try:
        todo_id = int(id_str)
        if todo_id <= 0:
            raise ValueError("Todo ID must be a positive number")
        return todo_id
    except (ValueError, TypeError):
        raise ValueError("Todo ID must be a valid number")
