"""Simple test script to verify the TODO application works."""

import sys
import io

# Force UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from src.data.todo_repository import TodoRepository
from src.data.models import Todo
from src.logic.todo_service import TodoService
from src.logic.validators import validate_todo_text, validate_todo_id


def test_todo_model():
    """Test Todo model creation and string representation."""
    print("Testing Todo model...")
    todo = Todo(id=1, text="Test task", completed=False)
    assert todo.id == 1
    assert todo.text == "Test task"
    assert todo.completed == False
    assert "[" in str(todo)  # Check status display
    print("✓ Todo model works correctly")


def test_repository():
    """Test TodoRepository CRUD operations."""
    print("\nTesting TodoRepository...")
    repo = TodoRepository()

    # Test add
    todo1 = repo.add("First task")
    assert todo1.id == 1
    assert todo1.text == "First task"

    todo2 = repo.add("Second task")
    assert todo2.id == 2

    # Test get_all
    all_todos = repo.get_all()
    assert len(all_todos) == 2

    # Test get_by_id
    found = repo.get_by_id(1)
    assert found.text == "First task"

    # Test update
    updated = repo.update(1, "Updated task")
    assert updated.text == "Updated task"

    # Test mark_complete
    completed = repo.mark_complete(1)
    assert completed.completed == True

    # Test delete
    repo.delete(2)
    assert len(repo.get_all()) == 1

    # Test error cases
    try:
        repo.add("")  # Empty text
        assert False, "Should raise ValueError"
    except ValueError:
        pass

    try:
        repo.get_by_id(999)  # Non-existent ID
        assert False, "Should raise KeyError"
    except KeyError:
        pass

    print("✓ TodoRepository works correctly")


def test_validators():
    """Test validation functions."""
    print("\nTesting validators...")

    # Test validate_todo_text
    assert validate_todo_text("  test  ") == "test"
    try:
        validate_todo_text("   ")
        assert False, "Should raise ValueError"
    except ValueError:
        pass

    # Test validate_todo_id
    assert validate_todo_id("5") == 5
    try:
        validate_todo_id("abc")
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    try:
        validate_todo_id("-1")
        assert False, "Should raise ValueError"
    except ValueError:
        pass

    print("✓ Validators work correctly")


def test_service():
    """Test TodoService operations."""
    print("\nTesting TodoService...")
    repo = TodoRepository()
    service = TodoService(repo)

    # Test add_todo
    todo1 = service.add_todo("Service task")
    assert todo1.id == 1

    # Test view_all
    todos = service.view_all()
    assert len(todos) == 1

    # Test mark_complete
    completed = service.mark_complete(1)
    assert completed.completed == True

    # Test update_todo
    updated = service.update_todo(1, "Updated service task")
    assert updated.text == "Updated service task"

    # Add another todo for delete test
    todo2 = service.add_todo("To be deleted")
    assert len(service.view_all()) == 2

    # Test delete_todo
    service.delete_todo(2)
    assert len(service.view_all()) == 1

    print("✓ TodoService works correctly")


def test_id_stability():
    """Test that IDs remain stable after deletions."""
    print("\nTesting ID stability...")
    repo = TodoRepository()

    # Add 3 todos
    todo1 = repo.add("Task 1")
    todo2 = repo.add("Task 2")
    todo3 = repo.add("Task 3")

    assert todo1.id == 1
    assert todo2.id == 2
    assert todo3.id == 3

    # Delete middle todo
    repo.delete(2)

    # Check remaining todos still have original IDs
    remaining = repo.get_all()
    assert len(remaining) == 2
    assert remaining[0].id == 1
    assert remaining[1].id == 3

    # Add new todo - should get ID 4, not reuse ID 2
    todo4 = repo.add("Task 4")
    assert todo4.id == 4

    print("✓ ID stability verified")


def test_empty_state():
    """Test handling of empty todo list."""
    print("\nTesting empty state...")
    repo = TodoRepository()
    service = TodoService(repo)

    # Empty list should work fine
    todos = service.view_all()
    assert len(todos) == 0
    assert isinstance(todos, list)

    print("✓ Empty state handled correctly")


def test_large_list():
    """Test performance with 100 todos."""
    print("\nTesting with 100 todos...")
    repo = TodoRepository()

    # Add 100 todos
    for i in range(100):
        repo.add(f"Task {i + 1}")

    # Verify all added
    todos = repo.get_all()
    assert len(todos) == 100

    # Test operations still work
    repo.mark_complete(50)
    todo_50 = repo.get_by_id(50)
    assert todo_50.completed == True

    repo.update(75, "Updated task 75")
    todo_75 = repo.get_by_id(75)
    assert todo_75.text == "Updated task 75"

    repo.delete(25)
    assert len(repo.get_all()) == 99

    print("✓ Large list handling verified")


if __name__ == "__main__":
    print("=" * 60)
    print("TODO APPLICATION TEST SUITE")
    print("=" * 60)

    try:
        test_todo_model()
        test_repository()
        test_validators()
        test_service()
        test_id_stability()
        test_empty_state()
        test_large_list()

        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nThe application is ready to use.")
        print("Run: python src/main.py")
        print("=" * 60 + "\n")

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
