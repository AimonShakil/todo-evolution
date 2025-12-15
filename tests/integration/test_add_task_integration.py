"""Integration tests for add task workflow."""

from click.testing import CliRunner

from src.cli.main import cli
from src.services.db import ENGINE, init_db
from src.services.task_service import TaskService
from sqlmodel import Session, select
from src.models.task import Task


def test_add_success() -> None:
    """Test successful task creation via CLI.

    Verifies the full end-to-end workflow: CLI command parsing,
    validation, database storage, and success message output.
    """
    runner = CliRunner()

    with runner.isolated_filesystem():
        init_db()

        result = runner.invoke(cli, ["add", "--user", "alice", "Buy groceries"])

        assert result.exit_code == 0
        assert "Task" in result.output
        assert "created" in result.output.lower()
        assert "Buy groceries" in result.output

        # Clean up
        ENGINE.dispose()


def test_add_persistence() -> None:
    """Test that created tasks persist across database sessions.

    Verifies that tasks are durably stored and survive database
    restart (close and reopen connection).
    """
    runner = CliRunner()

    with runner.isolated_filesystem():
        # Initialize database
        init_db()

        # Create task
        result = runner.invoke(cli, ["add", "--user", "alice", "Buy milk"])
        assert result.exit_code == 0

        # Close and reopen database (simulating restart)
        ENGINE.dispose()

        # Verify task persists
        with Session(ENGINE) as session:
            tasks = session.exec(select(Task).where(Task.user_id == "alice")).all()
            assert len(tasks) == 1
            assert tasks[0].title == "Buy milk"

        # Clean up
        ENGINE.dispose()


def test_add_auto_increment_id() -> None:
    """Test that task IDs auto-increment correctly.

    Verifies that creating multiple tasks results in sequential
    ID assignment starting from the highest existing ID.
    """
    runner = CliRunner()

    with runner.isolated_filesystem():
        init_db()

        # Create 10 tasks
        for i in range(10):
            result = runner.invoke(cli, ["add", "--user", "alice", f"Task {i+1}"])
            assert result.exit_code == 0

        # Create 11th task and verify ID
        result = runner.invoke(cli, ["add", "--user", "alice", "Task 11"])
        assert result.exit_code == 0

        # Verify 11th task has ID=11
        with Session(ENGINE) as session:
            tasks = session.exec(select(Task).where(Task.user_id == "alice")).all()
            assert len(tasks) == 11
            # The last task created should have ID=11
            max_id = max(task.id for task in tasks if task.id is not None)
            assert max_id == 11

        # Clean up
        ENGINE.dispose()


# ============================================================
# User Story 2: Input Validation and Error Handling Tests
# ============================================================


def test_add_empty_title() -> None:
    """Test that adding a task with empty title produces error.

    Verifies US-2.AC-1: Empty title validation error message
    and exit code 1.
    """
    runner = CliRunner()

    result = runner.invoke(cli, ["add", "--user", "alice", ""])

    assert result.exit_code == 1
    assert "Title cannot be empty" in result.output


def test_add_title_too_long() -> None:
    """Test that adding a task with title >200 chars produces error.

    Verifies US-2.AC-2: Title length validation error message
    and exit code 1.
    """
    runner = CliRunner()

    # Create a 201-character title
    long_title = "x" * 201

    result = runner.invoke(cli, ["add", "--user", "alice", long_title])

    assert result.exit_code == 1
    assert "Title must be 1-200 characters" in result.output


def test_add_missing_user() -> None:
    """Test that adding a task without --user flag produces error.

    Verifies US-2.AC-3: Missing required option error message
    and exit code 2 (Click framework convention).
    """
    runner = CliRunner()

    result = runner.invoke(cli, ["add", "Buy milk"])

    assert result.exit_code == 2
    assert "Missing option '--user'" in result.output or 'Missing option "--user"' in result.output


def test_add_empty_user_id() -> None:
    """Test that adding a task with empty user ID produces error.

    Verifies US-2.AC-4: Empty user_id validation error message
    and exit code 1.
    """
    runner = CliRunner()

    result = runner.invoke(cli, ["add", "--user", "", "Buy milk"])

    assert result.exit_code == 1
    assert "User ID cannot be empty" in result.output


# ============================================================
# User Story 3: User Data Isolation Tests
# ============================================================


def test_cross_user_isolation() -> None:
    """Test that tasks are created with correct user_id (US-3.AC-2).

    Verifies Constitutional Principle II: User isolation is enforced
    at the database level with correct user_id assignment.
    """
    runner = CliRunner()

    with runner.isolated_filesystem():
        init_db()

        # Alice creates her task
        result_alice = runner.invoke(cli, ["add", "--user", "alice", "Alice task"])
        assert result_alice.exit_code == 0

        # Bob creates his task
        result_bob = runner.invoke(cli, ["add", "--user", "bob", "Bob task"])
        assert result_bob.exit_code == 0

        # Verify database has 2 tasks with correct user_id values
        with Session(ENGINE) as session:
            all_tasks = session.exec(select(Task)).all()
            assert len(all_tasks) == 2

            # Find Alice's and Bob's tasks
            alice_task = next((t for t in all_tasks if t.user_id == "alice"), None)
            bob_task = next((t for t in all_tasks if t.user_id == "bob"), None)

            assert alice_task is not None, "Alice's task should exist"
            assert bob_task is not None, "Bob's task should exist"

            assert alice_task.title == "Alice task"
            assert alice_task.user_id == "alice"

            assert bob_task.title == "Bob task"
            assert bob_task.user_id == "bob"

            # Critical: Tasks have different IDs (proper isolation)
            assert alice_task.id != bob_task.id

        # Clean up
        ENGINE.dispose()
