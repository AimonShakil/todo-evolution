"""Pytest configuration and shared fixtures.

This module provides test fixtures used across the test suite,
including database session fixtures for isolation.
"""

from typing import Generator

import pytest
from sqlmodel import Session, SQLModel, create_engine


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
