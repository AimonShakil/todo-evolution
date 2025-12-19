"""
Unit tests for SQLModel entities.

Tests validation rules and model behavior for User and Task models.

Constitutional Alignment:
- Principle X: Testing Requirements (unit tests for models)
- Principle IX: Code Quality Standards (validate type hints work)
"""

import pytest
from datetime import datetime
from pydantic import ValidationError

from src.models.user import User
from src.models.task import Task


class TestUserModel:
    """Test cases for User model validation."""

    def test_user_creation_valid(self):
        """Test creating a valid user."""
        user = User(
            email="test@example.com",
            name="Test User",
            password_hash="$2b$12$abcdefghijklmnopqrstuvwxyz123456789",
        )
        assert user.email == "test@example.com"
        assert user.name == "Test User"
        assert user.id is None  # Not yet saved to database

    def test_user_email_validation_min_length(self):
        """Test email minimum length validation (3 characters)."""
        with pytest.raises(ValidationError):
            User(
                email="a@",  # Too short
                name="Test",
                password_hash="hash",
            )

    def test_user_name_validation_required(self):
        """Test name is required."""
        with pytest.raises(ValidationError):
            User(
                email="test@example.com",
                name="",  # Empty name not allowed
                password_hash="hash",
            )

    def test_user_password_hash_required(self):
        """Test password_hash is required."""
        with pytest.raises(ValidationError):
            User(
                email="test@example.com",
                name="Test User",
                password_hash="",  # Empty hash not allowed
            )

    def test_user_timestamps_auto_set(self):
        """Test created_at and updated_at are auto-set."""
        user = User(
            email="test@example.com",
            name="Test User",
            password_hash="hash",
        )
        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)
        assert user.created_at == user.updated_at


class TestTaskModel:
    """Test cases for Task model validation."""

    def test_task_creation_valid(self):
        """Test creating a valid task."""
        task = Task(
            user_id=1,
            title="Buy groceries",
            description="Get milk and eggs",
        )
        assert task.user_id == 1
        assert task.title == "Buy groceries"
        assert task.description == "Get milk and eggs"
        assert task.completed is False  # Default value
        assert task.id is None  # Not yet saved

    def test_task_title_validation_min_length(self):
        """Test title minimum length (1 character)."""
        with pytest.raises(ValidationError):
            Task(
                user_id=1,
                title="",  # Empty title not allowed
            )

    def test_task_title_validation_max_length(self):
        """Test title maximum length (200 characters)."""
        with pytest.raises(ValidationError):
            Task(
                user_id=1,
                title="A" * 201,  # Too long
            )

    def test_task_title_exactly_200_chars(self):
        """Test title with exactly 200 characters (boundary)."""
        task = Task(
            user_id=1,
            title="A" * 200,  # Exactly 200 chars
        )
        assert len(task.title) == 200

    def test_task_description_nullable(self):
        """Test description is optional (nullable)."""
        task = Task(
            user_id=1,
            title="Test task",
        )
        assert task.description is None

    def test_task_completed_default_false(self):
        """Test completed defaults to False."""
        task = Task(
            user_id=1,
            title="Test task",
        )
        assert task.completed is False

    def test_task_phase_v_fields_nullable(self):
        """Test Phase V fields are nullable and default to None."""
        task = Task(
            user_id=1,
            title="Test task",
        )
        assert task.priority is None
        assert task.tags is None
        assert task.due_date is None
        assert task.recurrence_pattern is None

    def test_task_timestamps_auto_set(self):
        """Test created_at and updated_at are auto-set."""
        task = Task(
            user_id=1,
            title="Test task",
        )
        assert isinstance(task.created_at, datetime)
        assert isinstance(task.updated_at, datetime)
        assert task.created_at == task.updated_at
