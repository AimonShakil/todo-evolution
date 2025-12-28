"""
Database configuration and session management for Phase II.

This module provides async PostgreSQL connection setup using SQLModel and asyncpg.

Constitutional Alignment:
- Principle IV: Stateless Architecture (database-backed state)
- Principle IX: Code Quality Standards (type hints, docstrings)
"""

import os
from typing import AsyncGenerator

# Load environment variables
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

load_dotenv()

# Get DATABASE_URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL environment variable is not set. "
        "Please create a .env file with DATABASE_URL=postgresql://..."
    )

# Convert postgresql:// to postgresql+asyncpg:// for async support
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# Convert Neon SSL parameters to asyncpg-compatible format
# asyncpg does NOT support 'sslmode' or 'channel_binding' parameters
import re

# Remove sslmode parameter
DATABASE_URL = re.sub(r"[?&]sslmode=\w+", "", DATABASE_URL)
# Remove channel_binding parameter
DATABASE_URL = re.sub(r"[?&]channel_binding=\w+", "", DATABASE_URL)
# Add ssl=require if not present
if "ssl=" not in DATABASE_URL:
    separator = "&" if "?" in DATABASE_URL else "?"
    DATABASE_URL = DATABASE_URL + separator + "ssl=require"

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL query logging (development only)
    future=True,
)

# Create async session factory
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function to get async database session.

    Yields an AsyncSession that is automatically closed after use.
    Used with FastAPI's Depends() for automatic session management.

    Yields:
        AsyncSession: Database session for executing queries

    Example:
        >>> @app.get("/tasks")
        >>> async def get_tasks(session: AsyncSession = Depends(get_session)):
        ...     statement = select(Task)
        ...     result = await session.execute(statement)
        ...     return result.scalars().all()
    """
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db() -> None:
    """
    Initialize database schema (create all tables).

    This function should be called once at application startup to create
    all tables defined in SQLModel metadata. In production, use Alembic
    migrations instead.

    Note:
        This is primarily for development/testing. Production deployments
        should use Alembic migrations (alembic upgrade head).

    Example:
        >>> @app.on_event("startup")
        >>> async def on_startup():
        ...     await init_db()
    """
    async with engine.begin() as conn:
        # Import models to register them with SQLModel metadata
        from src.models import Task, User  # noqa: F401

        # Create all tables
        await conn.run_sync(SQLModel.metadata.create_all)


async def close_db() -> None:
    """
    Close database engine and dispose of connection pool.

    This function should be called at application shutdown to gracefully
    close all database connections.

    Example:
        >>> @app.on_event("shutdown")
        >>> async def on_shutdown():
        ...     await close_db()
    """
    await engine.dispose()
