"""Unit tests for Task model."""

import pytest
from pydantic import ValidationError

from src.models.task import Task


def test_task_creation_valid() -> None:
    """Test creating a Task with valid data.

    Verifies that a Task can be created with all required fields
    and that the fields are correctly populated.
    """
    task = Task(user_id="alice", title="Buy milk", completed=False)

    assert task.user_id == "alice"
    assert task.title == "Buy milk"
    assert task.completed is False
    assert task.id is None  # Not yet persisted
    assert task.created_at is not None
    assert task.updated_at is not None


def test_task_title_empty_rejected() -> None:
    """Test that empty title is rejected.

    Verifies that creating a Task with an empty title
    raises a ValidationError.
    """
    with pytest.raises(ValidationError) as exc_info:
        Task(user_id="alice", title="", completed=False)

    assert "Title cannot be empty" in str(exc_info.value)


def test_task_title_too_long_rejected() -> None:
    """Test that title exceeding 200 characters is rejected.

    Verifies that creating a Task with a title longer than 200 chars
    raises a ValidationError.
    """
    long_title = "x" * 201

    with pytest.raises(ValidationError) as exc_info:
        Task(user_id="alice", title=long_title, completed=False)

    assert "200 characters" in str(exc_info.value).lower()


def test_task_user_id_empty_rejected() -> None:
    """Test that empty user_id is rejected.

    Verifies that creating a Task with an empty user_id
    raises a ValidationError.
    """
    with pytest.raises(ValidationError) as exc_info:
        Task(user_id="", title="Buy milk", completed=False)

    assert "User ID cannot be empty" in str(exc_info.value)


def test_task_boundary_1_char() -> None:
    """Test title boundary: exactly 1 character should succeed.

    Verifies that a title with the minimum valid length (1 char)
    is accepted.
    """
    task = Task(user_id="alice", title="a", completed=False)

    assert task.title == "a"


def test_task_boundary_200_chars() -> None:
    """Test title boundary: exactly 200 characters should succeed.

    Verifies that a title with the maximum valid length (200 chars)
    is accepted.
    """
    max_title = "x" * 200
    task = Task(user_id="alice", title=max_title, completed=False)

    assert task.title == max_title
    assert len(task.title) == 200


def test_task_emoji_in_title() -> None:
    """Test that emoji characters in title are preserved.

    Verifies that special characters like emojis are correctly
    stored and retrieved from the title field.
    """
    task = Task(user_id="alice", title="Buy 🥛 milk", completed=False)

    assert task.title == "Buy 🥛 milk"
    assert "🥛" in task.title
