"""
Integration tests for task routes.

Tests task CRUD endpoints with JWT authentication.

Constitutional Alignment:
- Principle X: Testing Requirements (integration tests for API)
- Principle II: User Data Isolation (verify JWT user verification)
- Principle III: Authentication & Authorization (verify auth required)
"""

import pytest
from httpx import AsyncClient

from src.models.user import User
from src.models.task import Task


@pytest.mark.asyncio
class TestGetTasks:
    """Test GET /api/{user_id}/tasks endpoint."""

    async def test_get_tasks_authenticated(
        self,
        client: AsyncClient,
        user_alice: User,
        token_alice: str,
        task_alice_1: Task,
        task_alice_2: Task,
    ):
        """Test getting tasks with valid JWT token."""
        response = await client.get(
            f"/api/{user_alice.id}/tasks",
            headers={"Authorization": f"Bearer {token_alice}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        task_ids = [t["id"] for t in data]
        assert task_alice_1.id in task_ids
        assert task_alice_2.id in task_ids

    async def test_get_tasks_no_token(self, client: AsyncClient, user_alice: User):
        """Test getting tasks without JWT token returns 403."""
        response = await client.get(f"/api/{user_alice.id}/tasks")
        assert response.status_code == 403  # No token provided

    async def test_get_tasks_invalid_token(
        self, client: AsyncClient, user_alice: User
    ):
        """Test getting tasks with invalid token returns 401."""
        response = await client.get(
            f"/api/{user_alice.id}/tasks",
            headers={"Authorization": "Bearer invalid.token.here"},
        )
        assert response.status_code == 401

    async def test_get_tasks_wrong_user(
        self,
        client: AsyncClient,
        user_alice: User,
        user_bob: User,
        token_bob: str,
    ):
        """Test user cannot access another user's tasks (Principle II)."""
        # Bob tries to access Alice's tasks
        response = await client.get(
            f"/api/{user_alice.id}/tasks",  # Alice's user_id
            headers={"Authorization": f"Bearer {token_bob}"},  # Bob's token
        )
        assert response.status_code == 403  # Forbidden


@pytest.mark.asyncio
class TestCreateTask:
    """Test POST /api/{user_id}/tasks endpoint."""

    async def test_create_task_success(
        self, client: AsyncClient, user_alice: User, token_alice: str
    ):
        """Test creating a task with valid JWT token."""
        response = await client.post(
            f"/api/{user_alice.id}/tasks",
            headers={"Authorization": f"Bearer {token_alice}"},
            json={
                "title": "New task from test",
                "description": "Test description",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "New task from test"
        assert data["description"] == "Test description"
        assert data["user_id"] == user_alice.id
        assert data["completed"] is False

    async def test_create_task_no_description(
        self, client: AsyncClient, user_alice: User, token_alice: str
    ):
        """Test creating a task without description."""
        response = await client.post(
            f"/api/{user_alice.id}/tasks",
            headers={"Authorization": f"Bearer {token_alice}"},
            json={"title": "Task without description"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["description"] is None

    async def test_create_task_empty_title(
        self, client: AsyncClient, user_alice: User, token_alice: str
    ):
        """Test creating task with empty title returns 422."""
        response = await client.post(
            f"/api/{user_alice.id}/tasks",
            headers={"Authorization": f"Bearer {token_alice}"},
            json={"title": ""},  # Empty title
        )

        assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
class TestUpdateTask:
    """Test PATCH /api/{user_id}/tasks/{task_id} endpoint."""

    async def test_update_task_title(
        self,
        client: AsyncClient,
        user_alice: User,
        token_alice: str,
        task_alice_1: Task,
    ):
        """Test updating task title."""
        response = await client.patch(
            f"/api/{user_alice.id}/tasks/{task_alice_1.id}",
            headers={"Authorization": f"Bearer {token_alice}"},
            json={"title": "Updated title"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated title"

    async def test_update_task_completed(
        self,
        client: AsyncClient,
        user_alice: User,
        token_alice: str,
        task_alice_1: Task,
    ):
        """Test updating task completed status."""
        response = await client.patch(
            f"/api/{user_alice.id}/tasks/{task_alice_1.id}",
            headers={"Authorization": f"Bearer {token_alice}"},
            json={"completed": True},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is True

    async def test_update_task_not_found(
        self, client: AsyncClient, user_alice: User, token_alice: str
    ):
        """Test updating non-existent task returns 404."""
        response = await client.patch(
            f"/api/{user_alice.id}/tasks/99999",
            headers={"Authorization": f"Bearer {token_alice}"},
            json={"title": "Updated"},
        )

        assert response.status_code == 404


@pytest.mark.asyncio
class TestToggleTask:
    """Test POST /api/{user_id}/tasks/{task_id}/toggle endpoint."""

    async def test_toggle_task_false_to_true(
        self,
        client: AsyncClient,
        user_alice: User,
        token_alice: str,
        task_alice_1: Task,
    ):
        """Test toggling task from False to True."""
        assert task_alice_1.completed is False

        response = await client.post(
            f"/api/{user_alice.id}/tasks/{task_alice_1.id}/toggle",
            headers={"Authorization": f"Bearer {token_alice}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is True

    async def test_toggle_task_true_to_false(
        self,
        client: AsyncClient,
        user_alice: User,
        token_alice: str,
        task_alice_2: Task,
    ):
        """Test toggling task from True to False."""
        assert task_alice_2.completed is True

        response = await client.post(
            f"/api/{user_alice.id}/tasks/{task_alice_2.id}/toggle",
            headers={"Authorization": f"Bearer {token_alice}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is False


@pytest.mark.asyncio
class TestDeleteTask:
    """Test DELETE /api/{user_id}/tasks/{task_id} endpoint."""

    async def test_delete_task_success(
        self,
        client: AsyncClient,
        user_alice: User,
        token_alice: str,
        task_alice_1: Task,
    ):
        """Test deleting a task."""
        response = await client.delete(
            f"/api/{user_alice.id}/tasks/{task_alice_1.id}",
            headers={"Authorization": f"Bearer {token_alice}"},
        )

        assert response.status_code == 204  # No content

        # Verify task is deleted
        get_response = await client.get(
            f"/api/{user_alice.id}/tasks/{task_alice_1.id}",
            headers={"Authorization": f"Bearer {token_alice}"},
        )
        assert get_response.status_code == 404

    async def test_delete_task_not_found(
        self, client: AsyncClient, user_alice: User, token_alice: str
    ):
        """Test deleting non-existent task returns 404."""
        response = await client.delete(
            f"/api/{user_alice.id}/tasks/99999",
            headers={"Authorization": f"Bearer {token_alice}"},
        )

        assert response.status_code == 404
