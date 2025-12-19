"""
Pytest fixtures for Phase II Web App tests.

This module provides shared test fixtures for database sessions,
test clients, and sample data.

Constitutional Alignment:
- Principle X: Testing Requirements (proper test isolation)
- Principle II: User Data Isolation (test fixtures for multiple users)
"""

import os
import pytest
import pytest_asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from httpx import AsyncClient

from src.main import app
from src.lib.database import get_session
from src.models.user import User
from src.models.task import Task
from src.services.auth_service import hash_password, create_access_token


# Test database URL (in-memory SQLite for fast tests)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


# Async engine for tests
@pytest_asyncio.fixture(scope="function")
async def test_engine():
    """Create async test database engine."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        future=True,
    )

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield engine

    # Drop all tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await engine.dispose()


# Async session for tests
@pytest_asyncio.fixture(scope="function")
async def session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """
    Create async test database session.

    Yields:
        Async database session for tests
    """
    async_session_maker = sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session_maker() as test_session:
        yield test_session


# Override get_session dependency
@pytest_asyncio.fixture(scope="function")
async def client(session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    Create test HTTP client with overridden database session.

    Args:
        session: Test database session

    Yields:
        Async HTTP client for API testing
    """

    async def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(app=app, base_url="http://test") as test_client:
        yield test_client

    app.dependency_overrides.clear()


# Test user fixtures
@pytest_asyncio.fixture(scope="function")
async def user_alice(session: AsyncSession) -> User:
    """
    Create test user: Alice.

    Returns:
        User object for alice@example.com
    """
    user = User(
        email="alice@example.com",
        name="Alice Smith",
        password_hash=hash_password("password123"),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@pytest_asyncio.fixture(scope="function")
async def user_bob(session: AsyncSession) -> User:
    """
    Create test user: Bob.

    Returns:
        User object for bob@example.com
    """
    user = User(
        email="bob@example.com",
        name="Bob Jones",
        password_hash=hash_password("password456"),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


# JWT token fixtures
@pytest.fixture(scope="function")
def token_alice(user_alice: User) -> str:
    """
    Generate JWT token for Alice.

    Args:
        user_alice: Alice's user object

    Returns:
        JWT token string
    """
    return create_access_token(user_id=user_alice.id, email=user_alice.email)


@pytest.fixture(scope="function")
def token_bob(user_bob: User) -> str:
    """
    Generate JWT token for Bob.

    Args:
        user_bob: Bob's user object

    Returns:
        JWT token string
    """
    return create_access_token(user_id=user_bob.id, email=user_bob.email)


# Task fixtures
@pytest_asyncio.fixture(scope="function")
async def task_alice_1(session: AsyncSession, user_alice: User) -> Task:
    """
    Create test task for Alice.

    Returns:
        Task object owned by Alice
    """
    task = Task(
        user_id=user_alice.id,
        title="Alice's Task 1",
        description="Buy groceries",
        completed=False,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


@pytest_asyncio.fixture(scope="function")
async def task_alice_2(session: AsyncSession, user_alice: User) -> Task:
    """
    Create second test task for Alice.

    Returns:
        Task object owned by Alice
    """
    task = Task(
        user_id=user_alice.id,
        title="Alice's Task 2",
        description="Walk the dog",
        completed=True,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


@pytest_asyncio.fixture(scope="function")
async def task_bob_1(session: AsyncSession, user_bob: User) -> Task:
    """
    Create test task for Bob.

    Returns:
        Task object owned by Bob
    """
    task = Task(
        user_id=user_bob.id,
        title="Bob's Task 1",
        description="Fix the car",
        completed=False,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task
