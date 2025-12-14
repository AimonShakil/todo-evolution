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

    result = runner.invoke(cli, ["add", "--user", "alice", "Buy groceries"])

    assert result.exit_code == 0
    assert "Task" in result.output
    assert "created" in result.output.lower()
    assert "Buy groceries" in result.output


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
