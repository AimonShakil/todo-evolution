"""
Task service for Phase II Web App.

This module provides CRUD operations for tasks with user isolation.
All operations enforce Constitutional Principle II (User Data Isolation).

Constitutional Alignment:
- Principle II: User Data Isolation (all queries filter by user_id)
- Principle IX: Code Quality Standards (type hints, docstrings)
- Principle IV: Stateless Architecture (database-backed operations)
"""

from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.models.task import Task


async def get_all_tasks(session: AsyncSession, user_id: int) -> list[Task]:
    """
    Get all tasks for a specific user.

    Constitutional Principle II: User isolation enforced via WHERE user_id = ?

    Args:
        session: Async database session
        user_id: User ID (owner filter)

    Returns:
        List of tasks belonging to the user (may be empty)

    Example:
        >>> tasks = await get_all_tasks(session, user_id=1)
        >>> len(tasks)
        5
    """
    statement = select(Task).where(Task.user_id == user_id)
    result = await session.execute(statement)
    return list(result.scalars().all())


async def get_task(
    session: AsyncSession, user_id: int, task_id: int
) -> Optional[Task]:
    """
    Get a single task by ID with user ownership verification.

    Constitutional Principle II: Returns None if task doesn't exist OR
    belongs to a different user (prevents access to other users' tasks).

    Args:
        session: Async database session
        user_id: User ID (owner filter)
        task_id: Task ID to retrieve

    Returns:
        Task object if found and owned by user, None otherwise

    Example:
        >>> task = await get_task(session, user_id=1, task_id=10)
        >>> task.title if task else "Not found"
        'Buy groceries'
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def create_task(
    session: AsyncSession,
    user_id: int,
    title: str,
    description: Optional[str] = None,
) -> Task:
    """
    Create a new task for a user.

    Args:
        session: Async database session
        user_id: User ID (owner)
        title: Task title (1-200 characters)
        description: Optional detailed description (Phase II feature)

    Returns:
        Created task object with generated ID

    Example:
        >>> task = await create_task(
        ...     session,
        ...     user_id=1,
        ...     title="Buy groceries",
        ...     description="Get milk, eggs, and bread"
        ... )
        >>> task.id
        1
        >>> task.completed
        False
    """
    task = Task(
        user_id=user_id,
        title=title,
        description=description,
        completed=False,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def update_task(
    session: AsyncSession,
    user_id: int,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    completed: Optional[bool] = None,
) -> Optional[Task]:
    """
    Update a task's fields.

    Constitutional Principle II: Only updates if task belongs to user.

    Args:
        session: Async database session
        user_id: User ID (owner filter)
        task_id: Task ID to update
        title: New title (optional)
        description: New description (optional)
        completed: New completion status (optional)

    Returns:
        Updated task object if found and owned by user, None otherwise

    Example:
        >>> task = await update_task(
        ...     session,
        ...     user_id=1,
        ...     task_id=10,
        ...     title="Buy groceries and supplies"
        ... )
        >>> task.title if task else "Not found"
        'Buy groceries and supplies'
    """
    task = await get_task(session, user_id, task_id)
    if not task:
        return None

    # Update fields if provided
    if title is not None:
        task.title = title
    if description is not None:
        task.description = description
    if completed is not None:
        task.completed = completed

    task.updated_at = datetime.utcnow()

    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def toggle_task_completed(
    session: AsyncSession, user_id: int, task_id: int
) -> Optional[Task]:
    """
    Toggle a task's completion status (completed ↔ incomplete).

    Constitutional Principle II: Only toggles if task belongs to user.

    Args:
        session: Async database session
        user_id: User ID (owner filter)
        task_id: Task ID to toggle

    Returns:
        Updated task object if found and owned by user, None otherwise

    Example:
        >>> task = await toggle_task_completed(session, user_id=1, task_id=10)
        >>> task.completed if task else None
        True
    """
    task = await get_task(session, user_id, task_id)
    if not task:
        return None

    task.completed = not task.completed
    task.updated_at = datetime.utcnow()

    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def delete_task(session: AsyncSession, user_id: int, task_id: int) -> bool:
    """
    Delete a task.

    Constitutional Principle II: Only deletes if task belongs to user.

    Args:
        session: Async database session
        user_id: User ID (owner filter)
        task_id: Task ID to delete

    Returns:
        True if task was deleted, False if not found or not owned by user

    Example:
        >>> success = await delete_task(session, user_id=1, task_id=10)
        >>> success
        True
    """
    task = await get_task(session, user_id, task_id)
    if not task:
        return False

    await session.delete(task)
    await session.commit()
    return True
