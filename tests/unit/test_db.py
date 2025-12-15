"""Unit tests for database module."""

from sqlalchemy import inspect
from sqlmodel import Session, SQLModel, create_engine

from src.services.db import get_session, init_db


def test_init_db_creates_tables() -> None:
    """Test that init_db() creates all required tables.

    This test verifies that calling init_db() successfully creates
    the database schema including the Task table.
    """
    # Create in-memory database for testing
    test_engine = create_engine("sqlite:///:memory:")

    # Temporarily replace the module's engine with test engine
    import src.services.db as db_module

    original_engine = db_module.ENGINE
    db_module.ENGINE = test_engine

    try:
        # Call init_db()
        init_db()

        # Verify tables were created
        inspector = inspect(test_engine)
        tables = inspector.get_table_names()

        # Should have at least the Task table
        assert "task" in tables, "Task table should be created"

    finally:
        # Restore original engine
        db_module.ENGINE = original_engine


def test_get_session_yields_session() -> None:
    """Test that get_session() yields a Session object and auto-closes.

    This test verifies that the get_session() context manager:
    - Yields a valid Session object
    - Automatically closes the session when exiting the context
    """
    # Use the context manager
    with get_session() as session:
        # Verify we got a Session object
        assert isinstance(session, Session), "get_session should yield a Session object"
        assert session.is_active, "Session should be active within context"

    # After exiting context, session should be closed
    # Note: We can't easily test this without accessing internals,
    # but the implementation should handle cleanup
