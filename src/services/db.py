"""Database configuration and session management.

This module provides database engine configuration, session management,
and initialization utilities for the Todo Evolution application.
"""

from contextlib import contextmanager
from typing import Generator

from sqlalchemy import event
from sqlmodel import Session, create_engine

# Database configuration
DATABASE_URL = "sqlite:///todo.db"

# Create SQLAlchemy engine
ENGINE = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL query logging during development
    connect_args={"check_same_thread": False},  # Required for SQLite
)


# Configure WAL mode for better concurrency
@event.listens_for(ENGINE, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):  # type: ignore
    """Enable WAL mode for SQLite connections.

    WAL (Write-Ahead Logging) mode allows concurrent reads while writing,
    improving performance for multi-user scenarios.
    """
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.close()


def init_db() -> None:
    """Initialize the database by creating all tables.

    This function creates all tables defined in SQLModel metadata.
    It should be called once when the application starts or during
    database setup.

    Raises:
        DatabaseUnavailableError: If database connection fails.
    """
    from sqlmodel import SQLModel

    from src.lib.exceptions import DatabaseUnavailableError
    from src.models.task import Task  # Import models to register them with metadata

    try:
        SQLModel.metadata.create_all(ENGINE)
    except Exception as e:
        raise DatabaseUnavailableError(f"Failed to initialize database: {e}") from e


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """Provide a transactional scope for database operations.

    This context manager creates a new database session, yields it for use,
    and ensures proper cleanup (commit/rollback and close) when exiting.

    Yields:
        Session: A SQLModel Session object for database operations.

    Example:
        >>> with get_session() as session:
        ...     task = Task(title="Example")
        ...     session.add(task)
        ...     session.commit()
    """
    session = Session(ENGINE)
    try:
        yield session
    finally:
        session.close()
