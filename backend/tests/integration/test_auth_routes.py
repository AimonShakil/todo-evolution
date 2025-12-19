"""
Integration tests for authentication routes.

Tests signup and signin endpoints with HTTP client.

Constitutional Alignment:
- Principle X: Testing Requirements (integration tests for API)
- Principle III: Authentication & Authorization (verify auth flows work)
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User


@pytest.mark.asyncio
class TestSignup:
    """Test POST /api/auth/signup endpoint."""

    async def test_signup_success(self, client: AsyncClient):
        """Test successful user signup."""
        response = await client.post(
            "/api/auth/signup",
            json={
                "email": "newuser@example.com",
                "name": "New User",
                "password": "securepassword123",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["name"] == "New User"
        assert "token" in data
        assert len(data["token"]) > 100  # JWT token

    async def test_signup_duplicate_email(
        self, client: AsyncClient, user_alice: User
    ):
        """Test signup with existing email returns 400."""
        response = await client.post(
            "/api/auth/signup",
            json={
                "email": user_alice.email,  # Already exists
                "name": "Duplicate User",
                "password": "password123",
            },
        )

        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()

    async def test_signup_invalid_email(self, client: AsyncClient):
        """Test signup with invalid email returns 422."""
        response = await client.post(
            "/api/auth/signup",
            json={
                "email": "not-an-email",  # Invalid format
                "name": "Test User",
                "password": "password123",
            },
        )

        assert response.status_code == 422  # Validation error

    async def test_signup_short_password(self, client: AsyncClient):
        """Test signup with password < 8 chars returns 422."""
        response = await client.post(
            "/api/auth/signup",
            json={
                "email": "test@example.com",
                "name": "Test User",
                "password": "short",  # Less than 8 characters
            },
        )

        assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
class TestSignin:
    """Test POST /api/auth/signin endpoint."""

    async def test_signin_success(self, client: AsyncClient, user_alice: User):
        """Test successful user signin."""
        response = await client.post(
            "/api/auth/signin",
            json={
                "email": user_alice.email,
                "password": "password123",  # From fixture
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == user_alice.email
        assert data["name"] == user_alice.name
        assert data["user_id"] == user_alice.id
        assert "token" in data

    async def test_signin_wrong_password(self, client: AsyncClient, user_alice: User):
        """Test signin with wrong password returns 401."""
        response = await client.post(
            "/api/auth/signin",
            json={
                "email": user_alice.email,
                "password": "wrongpassword",
            },
        )

        assert response.status_code == 401
        assert "Invalid email or password" in response.json()["detail"]

    async def test_signin_nonexistent_user(self, client: AsyncClient):
        """Test signin with non-existent email returns 401."""
        response = await client.post(
            "/api/auth/signin",
            json={
                "email": "nonexistent@example.com",
                "password": "password123",
            },
        )

        assert response.status_code == 401
        assert "Invalid email or password" in response.json()["detail"]
