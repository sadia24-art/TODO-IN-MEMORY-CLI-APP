# TODO App - Phase I

An in-memory Python console application for managing todo items.

## Features

- Add new todos
- View all todos with ID, text, and completion status
- Mark todos as complete
- Update todo text
- Delete todos
- Clean console interface with menu-driven navigation

## Requirements

- Python 3.13+
- UV (Python package manager)

## Setup

1. Install UV if not already installed:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Run the application:
   ```bash
   uv run src/main.py
   ```

## Usage

The application presents a menu with 6 options:

1. **Add todo**: Create a new todo item
2. **View all todos**: Display all todos with their status
3. **Mark todo as complete**: Mark a specific todo as done
4. **Update todo**: Edit the text of an existing todo
5. **Delete todo**: Remove a todo from the list
6. **Exit**: Close the application

⚠️ **Warning**: All data is stored in memory only. All todos will be lost when the application exits.

## Project Structure

```
src/
├── main.py              # Application entry point
├── cli/                 # CLI Layer: User interface
│   ├── menu.py          # Menu display & input handling
│   └── commands.py      # Command handlers
├── logic/               # Logic Layer: Business rules
│   ├── todo_service.py  # Todo operations
│   └── validators.py    # Input validation
└── data/                # Data Layer: Storage
    ├── todo_repository.py  # In-memory storage
    └── models.py        # Todo data structure
```

## Documentation

See `specs/001-phase-1-console-todo/` for:
- Feature specification
- Architecture plan
- Data model
- Research notes
- Quick start guide

## License

MIT
