"""Unit tests for TaskService."""

from src.models.task import Task
from src.services.task_service import TaskService


def test_create_task_valid(test_db) -> None:
    """Test creating a task with valid data.

    Verifies that TaskService.create_task creates a task with all
    required fields populated and assigns an auto-incrementing ID.
    """
    service = TaskService(test_db)

    task = service.create_task(user_id="alice", title="Buy milk")

    assert task.id is not None
    assert task.user_id == "alice"
    assert task.title == "Buy milk"
    assert task.completed is False


def test_create_task_timestamps_populated(test_db) -> None:
    """Test that timestamps are automatically populated on task creation.

    Verifies that created_at and updated_at are set to non-null
    timestamp values when a task is created.
    """
    service = TaskService(test_db)

    task = service.create_task(user_id="alice", title="Buy milk")

    assert task.created_at is not None
    assert task.updated_at is not None
    assert isinstance(task.created_at, type(task.updated_at))


def test_get_tasks_for_user(test_db) -> None:
    """Test retrieving tasks filtered by user_id.

    Verifies that get_tasks_for_user returns only tasks belonging
    to the specified user, demonstrating user isolation.
    """
    service = TaskService(test_db)

    # Create tasks for different users
    service.create_task(user_id="alice", title="Alice task 1")
    service.create_task(user_id="alice", title="Alice task 2")
    service.create_task(user_id="bob", title="Bob task 1")

    # Get tasks for alice
    alice_tasks = service.get_tasks_for_user(user_id="alice")

    assert len(alice_tasks) == 2
    assert all(task.user_id == "alice" for task in alice_tasks)
    assert {task.title for task in alice_tasks} == {"Alice task 1", "Alice task 2"}
