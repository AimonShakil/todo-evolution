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


# ============================================================
# User Story 3: User Data Isolation Tests
# ============================================================


def test_user_isolation(test_db) -> None:
    """Test that users only see their own tasks (Constitutional Principle II).

    Verifies US-3.AC-1: Alice's tasks are invisible to Bob and vice versa.
    This is a security-critical test ensuring zero data leakage between users.
    """
    service = TaskService(test_db)

    # Alice creates her task
    alice_task = service.create_task(user_id="alice", title="Alice's task")

    # Bob creates his task
    bob_task = service.create_task(user_id="bob", title="Bob's task")

    # Verify Alice only sees her task
    alice_tasks = service.get_tasks_for_user(user_id="alice")
    assert len(alice_tasks) == 1
    assert alice_tasks[0].title == "Alice's task"
    assert alice_tasks[0].user_id == "alice"

    # Verify Bob only sees his task
    bob_tasks = service.get_tasks_for_user(user_id="bob")
    assert len(bob_tasks) == 1
    assert bob_tasks[0].title == "Bob's task"
    assert bob_tasks[0].user_id == "bob"

    # Critical: Bob should NOT see Alice's task
    assert alice_task.id not in [task.id for task in bob_tasks]
    # Critical: Alice should NOT see Bob's task
    assert bob_task.id not in [task.id for task in alice_tasks]


def test_user_id_filter_enforcement(test_db) -> None:
    """Test that user_id filtering is enforced across multiple users.

    Verifies US-3.AC-3: Filter by user_id returns exact count for each user.
    Tests with 3 users to ensure filtering works at scale.
    """
    service = TaskService(test_db)

    # Create tasks for three different users
    service.create_task(user_id="alice", title="Alice task 1")
    service.create_task(user_id="alice", title="Alice task 2")
    service.create_task(user_id="alice", title="Alice task 3")

    service.create_task(user_id="bob", title="Bob task 1")
    service.create_task(user_id="bob", title="Bob task 2")

    service.create_task(user_id="charlie", title="Charlie task 1")

    # Verify each user sees only their tasks
    alice_tasks = service.get_tasks_for_user(user_id="alice")
    assert len(alice_tasks) == 3
    assert all(task.user_id == "alice" for task in alice_tasks)

    bob_tasks = service.get_tasks_for_user(user_id="bob")
    assert len(bob_tasks) == 2
    assert all(task.user_id == "bob" for task in bob_tasks)

    charlie_tasks = service.get_tasks_for_user(user_id="charlie")
    assert len(charlie_tasks) == 1
    assert all(task.user_id == "charlie" for task in charlie_tasks)
