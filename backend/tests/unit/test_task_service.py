"""
Unit tests for task service.

Tests CRUD operations with user isolation.

Constitutional Alignment:
- Principle X: Testing Requirements (unit tests for services)
- Principle II: User Data Isolation (verify user_id filtering)
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.models.task import Task
from src.services import task_service


@pytest.mark.asyncio
class TestGetAllTasks:
    """Test get_all_tasks with user isolation."""

    async def test_get_all_tasks_empty(self, session: AsyncSession, user_alice: User):
        """Test get_all_tasks returns empty list when no tasks."""
        tasks = await task_service.get_all_tasks(session, user_alice.id)
        assert tasks == []

    async def test_get_all_tasks_single_user(
        self,
        session: AsyncSession,
        user_alice: User,
        task_alice_1: Task,
        task_alice_2: Task,
    ):
        """Test get_all_tasks returns all tasks for user."""
        tasks = await task_service.get_all_tasks(session, user_alice.id)
        assert len(tasks) == 2
        task_ids = [t.id for t in tasks]
        assert task_alice_1.id in task_ids
        assert task_alice_2.id in task_ids

    async def test_get_all_tasks_user_isolation(
        self,
        session: AsyncSession,
        user_alice: User,
        user_bob: User,
        task_alice_1: Task,
        task_bob_1: Task,
    ):
        """Test get_all_tasks enforces user isolation (Principle II)."""
        # Alice should see only her task
        tasks_alice = await task_service.get_all_tasks(session, user_alice.id)
        assert len(tasks_alice) == 1
        assert tasks_alice[0].id == task_alice_1.id

        # Bob should see only his task
        tasks_bob = await task_service.get_all_tasks(session, user_bob.id)
        assert len(tasks_bob) == 1
        assert tasks_bob[0].id == task_bob_1.id


@pytest.mark.asyncio
class TestGetTask:
    """Test get_task with user isolation."""

    async def test_get_task_exists(
        self, session: AsyncSession, user_alice: User, task_alice_1: Task
    ):
        """Test get_task returns task when it exists."""
        task = await task_service.get_task(session, user_alice.id, task_alice_1.id)
        assert task is not None
        assert task.id == task_alice_1.id
        assert task.title == "Alice's Task 1"

    async def test_get_task_not_found(self, session: AsyncSession, user_alice: User):
        """Test get_task returns None when task doesn't exist."""
        task = await task_service.get_task(session, user_alice.id, 99999)
        assert task is None

    async def test_get_task_wrong_user(
        self,
        session: AsyncSession,
        user_alice: User,
        user_bob: User,
        task_alice_1: Task,
    ):
        """Test get_task returns None when user doesn't own task (Principle II)."""
        # Bob tries to access Alice's task
        task = await task_service.get_task(session, user_bob.id, task_alice_1.id)
        assert task is None  # User isolation prevents access


@pytest.mark.asyncio
class TestCreateTask:
    """Test create_task."""

    async def test_create_task_minimal(self, session: AsyncSession, user_alice: User):
        """Test create_task with minimal data."""
        task = await task_service.create_task(
            session,
            user_id=user_alice.id,
            title="New task",
        )
        assert task.id is not None  # Auto-generated ID
        assert task.user_id == user_alice.id
        assert task.title == "New task"
        assert task.description is None
        assert task.completed is False

    async def test_create_task_with_description(
        self, session: AsyncSession, user_alice: User
    ):
        """Test create_task with description."""
        task = await task_service.create_task(
            session,
            user_id=user_alice.id,
            title="Task with details",
            description="Detailed description here",
        )
        assert task.title == "Task with details"
        assert task.description == "Detailed description here"


@pytest.mark.asyncio
class TestUpdateTask:
    """Test update_task."""

    async def test_update_task_title(
        self, session: AsyncSession, user_alice: User, task_alice_1: Task
    ):
        """Test update_task changes title."""
        updated = await task_service.update_task(
            session,
            user_id=user_alice.id,
            task_id=task_alice_1.id,
            title="Updated title",
        )
        assert updated is not None
        assert updated.title == "Updated title"
        assert updated.description == task_alice_1.description  # Unchanged

    async def test_update_task_multiple_fields(
        self, session: AsyncSession, user_alice: User, task_alice_1: Task
    ):
        """Test update_task changes multiple fields."""
        updated = await task_service.update_task(
            session,
            user_id=user_alice.id,
            task_id=task_alice_1.id,
            title="New title",
            description="New description",
            completed=True,
        )
        assert updated.title == "New title"
        assert updated.description == "New description"
        assert updated.completed is True

    async def test_update_task_not_found(
        self, session: AsyncSession, user_alice: User
    ):
        """Test update_task returns None when task not found."""
        updated = await task_service.update_task(
            session,
            user_id=user_alice.id,
            task_id=99999,
            title="Updated",
        )
        assert updated is None

    async def test_update_task_wrong_user(
        self,
        session: AsyncSession,
        user_alice: User,
        user_bob: User,
        task_alice_1: Task,
    ):
        """Test update_task enforces user isolation (Principle II)."""
        # Bob tries to update Alice's task
        updated = await task_service.update_task(
            session,
            user_id=user_bob.id,
            task_id=task_alice_1.id,
            title="Hacked!",
        )
        assert updated is None  # User isolation prevents update


@pytest.mark.asyncio
class TestToggleTaskCompleted:
    """Test toggle_task_completed."""

    async def test_toggle_task_false_to_true(
        self, session: AsyncSession, user_alice: User, task_alice_1: Task
    ):
        """Test toggle changes completed from False to True."""
        assert task_alice_1.completed is False

        toggled = await task_service.toggle_task_completed(
            session, user_alice.id, task_alice_1.id
        )
        assert toggled.completed is True

    async def test_toggle_task_true_to_false(
        self, session: AsyncSession, user_alice: User, task_alice_2: Task
    ):
        """Test toggle changes completed from True to False."""
        assert task_alice_2.completed is True

        toggled = await task_service.toggle_task_completed(
            session, user_alice.id, task_alice_2.id
        )
        assert toggled.completed is False

    async def test_toggle_task_not_found(
        self, session: AsyncSession, user_alice: User
    ):
        """Test toggle returns None when task not found."""
        toggled = await task_service.toggle_task_completed(
            session, user_alice.id, 99999
        )
        assert toggled is None


@pytest.mark.asyncio
class TestDeleteTask:
    """Test delete_task."""

    async def test_delete_task_exists(
        self, session: AsyncSession, user_alice: User, task_alice_1: Task
    ):
        """Test delete_task removes task."""
        success = await task_service.delete_task(
            session, user_alice.id, task_alice_1.id
        )
        assert success is True

        # Verify task is deleted
        task = await task_service.get_task(session, user_alice.id, task_alice_1.id)
        assert task is None

    async def test_delete_task_not_found(
        self, session: AsyncSession, user_alice: User
    ):
        """Test delete_task returns False when task not found."""
        success = await task_service.delete_task(session, user_alice.id, 99999)
        assert success is False

    async def test_delete_task_wrong_user(
        self,
        session: AsyncSession,
        user_alice: User,
        user_bob: User,
        task_alice_1: Task,
    ):
        """Test delete_task enforces user isolation (Principle II)."""
        # Bob tries to delete Alice's task
        success = await task_service.delete_task(
            session, user_bob.id, task_alice_1.id
        )
        assert success is False  # User isolation prevents deletion

        # Verify Alice's task still exists
        task = await task_service.get_task(session, user_alice.id, task_alice_1.id)
        assert task is not None
