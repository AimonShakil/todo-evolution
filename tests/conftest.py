"""Pytest configuration and shared fixtures.

This module provides test fixtures used across the test suite,
including database session fixtures for isolation.
"""

import os
from typing import Generator

import pytest
from sqlmodel import Session, SQLModel, create_engine


@pytest.fixture(autouse=True, scope="function")
def cleanup_integration_db() -> Generator[None, None, None]:
    """Clean up integration test database files before each test.

    This autouse fixture ensures test isolation by removing any todo.db
    files created during integration tests, preventing state leakage
    between tests.
    """
    # Clean up before test
    for file in ["todo.db", "todo.db-shm", "todo.db-wal"]:
        if os.path.exists(file):
            try:
                os.remove(file)
            except (OSError, PermissionError):
                pass  # File might be locked, will be cleaned up later

    yield

    # Clean up after test
    for file in ["todo.db", "todo.db-shm", "todo.db-wal"]:
        if os.path.exists(file):
            try:
                os.remove(file)
            except (OSError, PermissionError):
                pass


@pytest.fixture
def test_db() -> Generator[Session, None, None]:
    """Provide a clean in-memory database session for testing.

    This fixture creates an isolated in-memory SQLite database for each test,
    ensuring test independence and fast execution.

    Yields:
        Session: A SQLModel Session connected to an in-memory database.

    Example:
        >>> def test_create_task(test_db):
        ...     task = Task(title="Test")
        ...     test_db.add(task)
        ...     test_db.commit()
        ...     assert task.id is not None
    """
    # Create in-memory database
    engine = create_engine("sqlite:///:memory:")

    # Create all tables
    SQLModel.metadata.create_all(engine)

    # Create session
    session = Session(engine)

    try:
        yield session
    finally:
        session.close()
