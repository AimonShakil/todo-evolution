---
name: sqlite-testing
description: Create pytest tests for SQLite databases with fixtures, isolation, and user data separation validation. Use when writing tests for Phase I console app or any SQLite-based application.
allowed-tools: Read, Write, Edit, Bash
---

# SQLite Testing Patterns Skill

pytest patterns for SQLite with user isolation testing (Phase I).

## Test Database Fixture (In-Memory)

```python
# tests/conftest.py
import pytest
from sqlmodel import create_engine, SQLModel, Session
from backend.models import Task

@pytest.fixture
def test_db():
    """Create in-memory SQLite database for testing.

    Each test gets a fresh database that is automatically cleaned up.
    """
    # Create in-memory engine (faster, isolated)
    engine = create_engine("sqlite:///:memory:", echo=False)

    # Create all tables
    SQLModel.metadata.create_all(engine)

    # Provide session to test
    with Session(engine) as session:
        yield session

    # Cleanup (drop tables)
    SQLModel.metadata.drop_all(engine)
```

## Factory Pattern for Test Data

```python
# tests/factories.py
from datetime import datetime
from sqlmodel import Session
from backend.models import Task

def create_task(
    session: Session,
    user_id: str = "testuser",
    title: str = "Test task",
    completed: bool = False
) -> Task:
    """Factory for creating test tasks.

    Args:
        session: Database session
        user_id: User ID for the task
        title: Task title
        completed: Whether task is completed

    Returns:
        Created Task instance
    """
    task = Task(
        user_id=user_id,
        title=title,
        completed=completed,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

## User Isolation Tests (MANDATORY)

Per Constitutional Principle II, these tests are REQUIRED:

### Test 1: Cross-User Task Access Blocked

```python
# tests/test_user_isolation.py
from sqlmodel import select
from backend.models import Task

def test_user_cannot_access_other_user_tasks(test_db):
    """Verify Alice cannot access Bob's tasks.

    Constitutional requirement: User data isolation (Principle II).
    """
    # Alice creates a task
    alice_task = Task(user_id="alice", title="Alice's private task")
    test_db.add(alice_task)
    test_db.commit()

    # Bob queries for tasks (should not see Alice's task)
    bob_tasks = test_db.exec(
        select(Task).where(Task.user_id == "bob")
    ).all()

    # Verify Bob sees no tasks
    assert len(bob_tasks) == 0
    assert alice_task not in bob_tasks


def test_multiple_users_isolated(test_db):
    """Verify isolation with multiple users."""
    # Create tasks for three users
    alice_task = create_task(test_db, user_id="alice", title="Alice's task")
    bob_task = create_task(test_db, user_id="bob", title="Bob's task")
    charlie_task = create_task(test_db, user_id="charlie", title="Charlie's task")

    # Each user should only see their own task
    alice_tasks = test_db.exec(
        select(Task).where(Task.user_id == "alice")
    ).all()
    assert len(alice_tasks) == 1
    assert alice_tasks[0].id == alice_task.id

    bob_tasks = test_db.exec(
        select(Task).where(Task.user_id == "bob")
    ).all()
    assert len(bob_tasks) == 1
    assert bob_tasks[0].id == bob_task.id

    charlie_tasks = test_db.exec(
        select(Task).where(Task.user_id == "charlie")
    ).all()
    assert len(charlie_tasks) == 1
    assert charlie_tasks[0].id == charlie_task.id
```

### Test 2: Task Operations Respect User Isolation

```python
def test_update_task_respects_user_isolation(test_db):
    """Alice cannot update Bob's task."""
    # Bob creates a task
    bob_task = create_task(test_db, user_id="bob", title="Bob's task")

    # Alice tries to update Bob's task (should fail)
    alice_query = test_db.exec(
        select(Task).where(
            Task.id == bob_task.id,
            Task.user_id == "alice"  # Alice's user_id filter
        )
    ).first()

    # Alice's query returns None (task not found for her)
    assert alice_query is None


def test_delete_task_respects_user_isolation(test_db):
    """Alice cannot delete Bob's task."""
    # Bob creates a task
    bob_task = create_task(test_db, user_id="bob", title="Bob's task")

    # Alice tries to delete Bob's task
    alice_query = test_db.exec(
        select(Task).where(
            Task.id == bob_task.id,
            Task.user_id == "alice"
        )
    ).first()

    # Alice cannot find Bob's task
    assert alice_query is None

    # Verify Bob's task still exists
    bob_verification = test_db.exec(
        select(Task).where(
            Task.id == bob_task.id,
            Task.user_id == "bob"
        )
    ).first()

    assert bob_verification is not None
```

## CRUD Operation Tests

### Create Tests

```python
# tests/test_task_crud.py
def test_create_task(test_db):
    """Test creating a task."""
    task = Task(
        user_id="alice",
        title="Buy groceries",
        completed=False
    )
    test_db.add(task)
    test_db.commit()
    test_db.refresh(task)

    # Verify task was created
    assert task.id is not None
    assert task.user_id == "alice"
    assert task.title == "Buy groceries"
    assert task.completed is False
    assert task.created_at is not None
    assert task.updated_at is not None


def test_create_multiple_tasks(test_db):
    """Test creating multiple tasks for same user."""
    tasks = [
        Task(user_id="alice", title=f"Task {i}")
        for i in range(5)
    ]

    for task in tasks:
        test_db.add(task)
    test_db.commit()

    # Verify all tasks created
    alice_tasks = test_db.exec(
        select(Task).where(Task.user_id == "alice")
    ).all()

    assert len(alice_tasks) == 5
```

### Read Tests

```python
def test_read_task_by_id(test_db):
    """Test reading a specific task."""
    task = create_task(test_db, user_id="alice", title="Buy milk")

    # Read task
    retrieved = test_db.exec(
        select(Task).where(
            Task.id == task.id,
            Task.user_id == "alice"
        )
    ).first()

    assert retrieved is not None
    assert retrieved.id == task.id
    assert retrieved.title == "Buy milk"


def test_read_all_user_tasks(test_db):
    """Test reading all tasks for a user."""
    # Create 3 tasks for Alice
    for i in range(3):
        create_task(test_db, user_id="alice", title=f"Task {i}")

    # Create 2 tasks for Bob
    for i in range(2):
        create_task(test_db, user_id="bob", title=f"Bob Task {i}")

    # Alice should see only her 3 tasks
    alice_tasks = test_db.exec(
        select(Task).where(Task.user_id == "alice")
    ).all()

    assert len(alice_tasks) == 3
```

### Update Tests

```python
def test_update_task_title(test_db):
    """Test updating task title."""
    task = create_task(test_db, user_id="alice", title="Buy grocceries")

    # Update title
    task.title = "Buy groceries"  # Fixed typo
    task.updated_at = datetime.utcnow()
    test_db.add(task)
    test_db.commit()

    # Verify update
    updated = test_db.get(Task, task.id)
    assert updated.title == "Buy groceries"


def test_update_task_completion_status(test_db):
    """Test marking task as complete."""
    task = create_task(test_db, user_id="alice", completed=False)

    # Mark complete
    task.completed = True
    task.updated_at = datetime.utcnow()
    test_db.add(task)
    test_db.commit()

    # Verify completion
    updated = test_db.get(Task, task.id)
    assert updated.completed is True
```

### Delete Tests

```python
def test_delete_task(test_db):
    """Test deleting a task."""
    task = create_task(test_db, user_id="alice", title="Temporary task")

    # Delete task
    test_db.delete(task)
    test_db.commit()

    # Verify deletion
    deleted = test_db.get(Task, task.id)
    assert deleted is None


def test_delete_task_by_id(test_db):
    """Test deleting task by querying first."""
    task = create_task(test_db, user_id="alice", title="Delete me")

    # Query and delete
    to_delete = test_db.exec(
        select(Task).where(
            Task.id == task.id,
            Task.user_id == "alice"
        )
    ).first()

    assert to_delete is not None

    test_db.delete(to_delete)
    test_db.commit()

    # Verify deleted
    verify = test_db.get(Task, task.id)
    assert verify is None
```

## Validation Tests

```python
# tests/test_validation.py
import pytest
from pydantic import ValidationError

def test_task_title_required(test_db):
    """Test title is required."""
    with pytest.raises(ValidationError):
        task = Task(user_id="alice")  # Missing title


def test_task_title_max_length(test_db):
    """Test title max length (200 chars)."""
    long_title = "x" * 201

    with pytest.raises(ValidationError):
        task = Task(user_id="alice", title=long_title)


def test_task_completed_defaults_to_false(test_db):
    """Test completed defaults to False."""
    task = Task(user_id="alice", title="Test")

    assert task.completed is False


def test_task_timestamps_auto_generated(test_db):
    """Test timestamps are automatically generated."""
    task = Task(user_id="alice", title="Test")
    test_db.add(task)
    test_db.commit()
    test_db.refresh(task)

    assert task.created_at is not None
    assert task.updated_at is not None
    assert task.created_at == task.updated_at
```

## Edge Case Tests

```python
# tests/test_edge_cases.py
def test_empty_database(test_db):
    """Test querying empty database."""
    tasks = test_db.exec(select(Task)).all()

    assert len(tasks) == 0


def test_user_with_no_tasks(test_db):
    """Test user with no tasks."""
    # Create task for Alice
    create_task(test_db, user_id="alice", title="Alice's task")

    # Bob has no tasks
    bob_tasks = test_db.exec(
        select(Task).where(Task.user_id == "bob")
    ).all()

    assert len(bob_tasks) == 0


def test_task_id_auto_increment(test_db):
    """Test task IDs auto-increment."""
    task1 = create_task(test_db, user_id="alice", title="Task 1")
    task2 = create_task(test_db, user_id="alice", title="Task 2")
    task3 = create_task(test_db, user_id="alice", title="Task 3")

    assert task2.id == task1.id + 1
    assert task3.id == task2.id + 1


def test_unicode_task_title(test_db):
    """Test Unicode characters in task title."""
    task = create_task(test_db, user_id="alice", title="买菜 🛒")

    retrieved = test_db.get(Task, task.id)
    assert retrieved.title == "买菜 🛒"


def test_very_long_user_id(test_db):
    """Test very long user_id (edge case)."""
    long_user_id = "a" * 255

    task = create_task(test_db, user_id=long_user_id, title="Test")

    retrieved = test_db.exec(
        select(Task).where(Task.user_id == long_user_id)
    ).first()

    assert retrieved is not None
```

## Test Coverage Configuration

```python
# .coveragerc
[run]
source = backend
omit =
    */tests/*
    */test_*.py
    */__pycache__/*

[report]
exclude_lines =
    pragma: no cover
    if __name__ == .__main__.:
    if TYPE_CHECKING:
    @abstractmethod

precision = 2
```

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_user_isolation.py

# Run specific test
pytest tests/test_user_isolation.py::test_user_cannot_access_other_user_tasks

# Run with coverage
pytest --cov=backend --cov-report=term-missing --cov-fail-under=80

# Run with verbose output
pytest -v

# Run tests matching pattern
pytest -k "isolation"

# Run only fast tests (exclude slow integration tests)
pytest -m "not slow"
```

## Pytest Markers

```python
# tests/conftest.py
import pytest

def pytest_configure(config):
    """Configure custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )

# Usage in tests
@pytest.mark.slow
def test_large_dataset(test_db):
    """Test with 10,000 tasks (slow)."""
    pass

@pytest.mark.integration
def test_full_crud_workflow(test_db):
    """Integration test: create, read, update, delete."""
    pass
```

## Parametrized Tests

```python
import pytest

@pytest.mark.parametrize("user_id,title", [
    ("alice", "Task 1"),
    ("bob", "Task 2"),
    ("charlie", "Task 3"),
])
def test_create_task_for_different_users(test_db, user_id, title):
    """Test creating tasks for different users."""
    task = create_task(test_db, user_id=user_id, title=title)

    assert task.user_id == user_id
    assert task.title == title


@pytest.mark.parametrize("invalid_title", [
    "",           # Empty string
    "   ",        # Whitespace only
    "x" * 201,    # Too long
])
def test_invalid_task_titles(test_db, invalid_title):
    """Test validation rejects invalid titles."""
    with pytest.raises((ValidationError, ValueError)):
        task = Task(user_id="alice", title=invalid_title)
        test_db.add(task)
        test_db.commit()
```

## Fixtures with Autouse

```python
# tests/conftest.py
@pytest.fixture(autouse=True)
def reset_database():
    """Auto-reset database before each test.

    This fixture runs automatically for every test.
    """
    # Setup: Initialize database
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    yield

    # Teardown: Drop all tables
    SQLModel.metadata.drop_all(engine)
```

## Testing CLI Commands

```python
# tests/test_cli.py
from click.testing import CliRunner
from backend.main import cli

def test_add_command():
    """Test CLI add command."""
    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(cli, ['add', '--user', 'alice', 'Buy groceries'])

        assert result.exit_code == 0
        assert 'Task' in result.output
        assert 'added' in result.output


def test_view_command_empty(test_db):
    """Test CLI view command with no tasks."""
    runner = CliRunner()

    result = runner.invoke(cli, ['view', '--user', 'alice'])

    assert result.exit_code == 0
    assert 'No tasks found' in result.output


def test_complete_command(test_db):
    """Test CLI complete command."""
    runner = CliRunner()

    # First, add a task
    runner.invoke(cli, ['add', '--user', 'alice', 'Buy milk'])

    # Then complete it
    result = runner.invoke(cli, ['complete', '--user', 'alice', '1'])

    assert result.exit_code == 0
    assert 'complete' in result.output.lower()
```

## Test Organization

```
tests/
├── conftest.py              # Shared fixtures
├── factories.py             # Test data factories
├── test_models.py           # Model tests
├── test_user_isolation.py   # User isolation tests (MANDATORY)
├── test_task_crud.py        # CRUD operation tests
├── test_validation.py       # Input validation tests
├── test_edge_cases.py       # Edge case tests
└── test_cli.py              # CLI command tests
```

## Constitutional Compliance

Per Principle X (Testing Requirements):

- [ ] **80% coverage minimum**: Run `pytest --cov --cov-fail-under=80`
- [ ] **User isolation tests**: MANDATORY (Principle II)
- [ ] **CRUD tests**: All operations tested
- [ ] **Validation tests**: Input validation tested
- [ ] **Edge cases**: Empty DB, no tasks, Unicode, etc.

## Quick Testing Checklist

Before considering tests complete:

- [ ] User isolation tests pass (cross-user access blocked)
- [ ] All CRUD operations tested (Create, Read, Update, Delete)
- [ ] Validation tests for invalid inputs
- [ ] Edge cases covered (empty DB, Unicode, long strings)
- [ ] CLI commands tested (if applicable)
- [ ] Coverage ≥ 80% (`pytest --cov`)
- [ ] All tests pass (`pytest`)
- [ ] No flaky tests (run multiple times to verify)
