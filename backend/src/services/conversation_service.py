"""
Conversation service for Phase III - Agentic AI Chatbot.

This module provides CRUD operations for conversations with user isolation.
All operations enforce Constitutional Principle II (User Data Isolation).

Constitutional Alignment:
- Principle II: User Data Isolation (all queries filter by user_id)
- Principle III: Stateless Architecture (database-backed conversation state)
- Principle IX: Code Quality Standards (type hints, docstrings)
- Principle XXVI: Conversation Persistence (database-backed history)
"""

from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.models.conversation import Conversation


async def create_conversation(session: AsyncSession, user_id: int) -> Conversation:
    """
    Create a new conversation for a user.

    Constitutional Principle II: Conversation automatically linked to user via user_id.

    Args:
        session: Async database session
        user_id: User ID (owner)

    Returns:
        Created conversation object with generated ID

    Example:
        >>> conversation = await create_conversation(session, user_id=1)
        >>> conversation.id
        1
        >>> conversation.is_active
        True
    """
    conversation = Conversation(
        user_id=user_id,
        is_active=True,
    )
    session.add(conversation)
    await session.commit()
    await session.refresh(conversation)
    return conversation


async def get_active_conversation(
    session: AsyncSession, user_id: int
) -> Optional[Conversation]:
    """
    Get the active conversation for a user.

    Constitutional Principle II: Returns only conversations belonging to the user.
    Uses composite index (user_id, is_active) for O(1) lookup performance.

    Args:
        session: Async database session
        user_id: User ID (owner filter)

    Returns:
        Active conversation if found, None otherwise

    Example:
        >>> conversation = await get_active_conversation(session, user_id=1)
        >>> conversation.is_active if conversation else None
        True
    """
    statement = (
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .where(Conversation.is_active == True)
    )
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def list_user_conversations(
    session: AsyncSession,
    user_id: int,
    page: int = 1,
    limit: int = 20,
) -> list[Conversation]:
    """
    List all conversations for a user with pagination.

    Constitutional Principle II: Returns only conversations belonging to the user.
    Ordered by updated_at DESC (most recent first).

    Args:
        session: Async database session
        user_id: User ID (owner filter)
        page: Page number (1-indexed)
        limit: Number of conversations per page (default: 20)

    Returns:
        List of conversations belonging to the user (may be empty)

    Example:
        >>> conversations = await list_user_conversations(session, user_id=1, page=1)
        >>> len(conversations)
        5
        >>> conversations[0].updated_at > conversations[1].updated_at
        True
    """
    offset = (page - 1) * limit
    statement = (
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())
        .offset(offset)
        .limit(limit)
    )
    result = await session.execute(statement)
    return list(result.scalars().all())


async def archive_conversation(
    session: AsyncSession, user_id: int, conversation_id: int
) -> Optional[Conversation]:
    """
    Archive a conversation (set is_active = False).

    Constitutional Principle II: Only archives if conversation belongs to user.
    Used when 500 message limit reached or user manually archives.

    Args:
        session: Async database session
        user_id: User ID (owner filter)
        conversation_id: Conversation ID to archive

    Returns:
        Archived conversation if found and owned by user, None otherwise

    Example:
        >>> conversation = await archive_conversation(session, user_id=1, conversation_id=5)
        >>> conversation.is_active if conversation else None
        False
    """
    statement = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id,
    )
    result = await session.execute(statement)
    conversation = result.scalar_one_or_none()

    if not conversation:
        return None

    conversation.is_active = False
    conversation.updated_at = datetime.utcnow()

    session.add(conversation)
    await session.commit()
    await session.refresh(conversation)
    return conversation
