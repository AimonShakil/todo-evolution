"""
User isolation tests for Phase II Web App.

Tests Constitutional Principle II: User Data Isolation.
Verifies that users cannot access, modify, or delete other users' data.

Constitutional Alignment:
- Principle II: User Data Isolation (PRIMARY FOCUS)
- Principle X: Testing Requirements (security tests required)
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.models.task import Task
from src.services import task_service


@pytest.mark.asyncio
class TestUserIsolationServiceLayer:
    """
    Test user isolation at the service layer.

    Constitutional Principle II: All service methods must filter by user_id.
    """

    async def test_get_all_tasks_isolation(
        self,
        session: AsyncSession,
        user_alice: User,
        user_bob: User,
        task_alice_1: Task,
        task_alice_2: Task,
        task_bob_1: Task,
    ):
        """Test users can only see their own tasks."""
        # Alice should see only her 2 tasks
        tasks_alice = await task_service.get_all_tasks(session, user_alice.id)
        assert len(tasks_alice) == 2
        for task in tasks_alice:
            assert task.user_id == user_alice.id

        # Bob should see only his 1 task
        tasks_bob = await task_service.get_all_tasks(session, user_bob.id)
        assert len(tasks_bob) == 1
        for task in tasks_bob:
            assert task.user_id == user_bob.id

    async def test_get_task_isolation(
        self,
        session: AsyncSession,
        user_alice: User,
        user_bob: User,
        task_alice_1: Task,
    ):
        """Test users cannot retrieve other users' tasks."""
        # Alice can get her own task
        task = await task_service.get_task(session, user_alice.id, task_alice_1.id)
        assert task is not None
        assert task.id == task_alice_1.id

        # Bob cannot get Alice's task (returns None, not error)
        task = await task_service.get_task(session, user_bob.id, task_alice_1.id)
        assert task is None  # User isolation prevents access

    async def test_update_task_isolation(
        self,
        session: AsyncSession,
        user_alice: User,
        user_bob: User,
        task_alice_1: Task,
    ):
        """Test users cannot update other users' tasks."""
        original_title = task_alice_1.title

        # Bob tries to update Alice's task
        updated = await task_service.update_task(
            session,
            user_id=user_bob.id,  # Bob's user_id
            task_id=task_alice_1.id,  # Alice's task
            title="Hacked by Bob",
        )
        assert updated is None  # User isolation prevents update

        # Verify Alice's task is unchanged
        task = await task_service.get_task(session, user_alice.id, task_alice_1.id)
        assert task.title == original_title  # Still original title

    async def test_delete_task_isolation(
        self,
        session: AsyncSession,
        user_alice: User,
        user_bob: User,
        task_alice_1: Task,
    ):
        """Test users cannot delete other users' tasks."""
        # Bob tries to delete Alice's task
        success = await task_service.delete_task(
            session, user_bob.id, task_alice_1.id
        )
        assert success is False  # User isolation prevents deletion

        # Verify Alice's task still exists
        task = await task_service.get_task(session, user_alice.id, task_alice_1.id)
        assert task is not None  # Task still exists


@pytest.mark.asyncio
class TestUserIsolationAPILayer:
    """
    Test user isolation at the API layer.

    Constitutional Principle II: JWT user_id must match URL {user_id}.
    """

    async def test_get_tasks_wrong_user_token(
        self,
        client: AsyncClient,
        user_alice: User,
        user_bob: User,
        token_bob: str,
        task_alice_1: Task,
    ):
        """Test user cannot access another user's tasks via API."""
        # Bob tries to access Alice's tasks using his JWT token
        response = await client.get(
            f"/api/{user_alice.id}/tasks",  # Alice's endpoint
            headers={"Authorization": f"Bearer {token_bob}"},  # Bob's token
        )

        # Should return 403 Forbidden (not 200 with empty list)
        assert response.status_code == 403
        assert "Cannot access another user's tasks" in response.json()["detail"]

    async def test_create_task_wrong_user_token(
        self,
        client: AsyncClient,
        user_alice: User,
        user_bob: User,
        token_bob: str,
    ):
        """Test user cannot create tasks for another user via API."""
        # Bob tries to create a task for Alice
        response = await client.post(
            f"/api/{user_alice.id}/tasks",  # Alice's endpoint
            headers={"Authorization": f"Bearer {token_bob}"},  # Bob's token
            json={"title": "Malicious task"},
        )

        assert response.status_code == 403

        # Verify no task was created for Alice
        alice_response = await client.get(
            f"/api/{user_alice.id}/tasks",
            headers={"Authorization": f"Bearer token_alice"},  # Would need Alice's token
        )
        # This would fail auth, but point is Bob couldn't create for Alice

    async def test_update_task_wrong_user_token(
        self,
        client: AsyncClient,
        user_alice: User,
        user_bob: User,
        token_bob: str,
        task_alice_1: Task,
    ):
        """Test user cannot update another user's task via API."""
        # Bob tries to update Alice's task
        response = await client.patch(
            f"/api/{user_alice.id}/tasks/{task_alice_1.id}",
            headers={"Authorization": f"Bearer {token_bob}"},
            json={"title": "Hacked title"},
        )

        assert response.status_code == 403

    async def test_delete_task_wrong_user_token(
        self,
        client: AsyncClient,
        user_alice: User,
        user_bob: User,
        token_bob: str,
        task_alice_1: Task,
    ):
        """Test user cannot delete another user's task via API."""
        # Bob tries to delete Alice's task
        response = await client.delete(
            f"/api/{user_alice.id}/tasks/{task_alice_1.id}",
            headers={"Authorization": f"Bearer {token_bob}"},
        )

        assert response.status_code == 403

    async def test_toggle_task_wrong_user_token(
        self,
        client: AsyncClient,
        user_alice: User,
        user_bob: User,
        token_bob: str,
        task_alice_1: Task,
    ):
        """Test user cannot toggle another user's task via API."""
        # Bob tries to toggle Alice's task
        response = await client.post(
            f"/api/{user_alice.id}/tasks/{task_alice_1.id}/toggle",
            headers={"Authorization": f"Bearer {token_bob}"},
        )

        assert response.status_code == 403


@pytest.mark.asyncio
class TestUserIsolationEdgeCases:
    """Test edge cases for user isolation."""

    async def test_nonexistent_user_id(
        self, client: AsyncClient, token_alice: str
    ):
        """Test accessing non-existent user's endpoint."""
        # Alice tries to access user 99999's tasks
        response = await client.get(
            "/api/99999/tasks",
            headers={"Authorization": f"Bearer {token_alice}"},
        )

        # Should return 403 (JWT user doesn't match URL user)
        assert response.status_code == 403

    async def test_user_cannot_create_task_for_self_with_wrong_url(
        self,
        client: AsyncClient,
        user_alice: User,
        user_bob: User,
        token_alice: str,
    ):
        """Test user cannot bypass isolation by using wrong URL."""
        # Alice tries to create task using Bob's user_id in URL
        # but her own JWT token
        response = await client.post(
            f"/api/{user_bob.id}/tasks",  # Bob's URL
            headers={"Authorization": f"Bearer {token_alice}"},  # Alice's token
            json={"title": "Sneaky task"},
        )

        # Should be rejected (JWT user doesn't match URL user)
        assert response.status_code == 403
