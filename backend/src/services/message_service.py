"""
Message service for Phase III - Agentic AI Chatbot.

This module provides CRUD operations for messages with user isolation.
All operations enforce Constitutional Principle II (User Data Isolation).

Constitutional Alignment:
- Principle II: User Data Isolation (all queries filter by user_id)
- Principle III: Stateless Architecture (database-backed message state)
- Principle IX: Code Quality Standards (type hints, docstrings)
- Principle XXVI: Conversation Persistence (message history reconstruction)
"""

from datetime import datetime

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.models.conversation import Conversation
from src.models.message import Message


async def create_message(
    session: AsyncSession,
    conversation_id: int,
    user_id: int,
    role: str,
    content: str,
) -> Message:
    """
    Create a new message in a conversation.

    Constitutional Principle II: Message automatically linked to user via user_id.
    Updates conversation.updated_at timestamp as side effect.

    Args:
        session: Async database session
        conversation_id: Parent conversation ID
        user_id: User ID (owner, must match conversation owner)
        role: Message role ("user", "assistant", or "tool")
        content: Message content (1-4000 characters)

    Returns:
        Created message object with generated ID

    Example:
        >>> message = await create_message(
        ...     session,
        ...     conversation_id=1,
        ...     user_id=1,
        ...     role="user",
        ...     content="Hello, create a task for buying milk"
        ... )
        >>> message.id
        1
        >>> message.role
        'user'
    """
    message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role=role,
        content=content,
    )
    session.add(message)

    # Update conversation.updated_at timestamp
    conversation = await session.get(Conversation, conversation_id)
    if conversation:
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)

    await session.commit()
    await session.refresh(message)
    return message


async def get_conversation_messages(
    session: AsyncSession,
    conversation_id: int,
    user_id: int,
    limit: int = 50,
) -> list[Message]:
    """
    Get messages for a conversation (last N messages in chronological order).

    Constitutional Principle II: Verifies conversation belongs to user.
    Used for agent context reconstruction (ADR-002: last 50 messages).
    Uses composite index (conversation_id, created_at) for optimal performance.

    Args:
        session: Async database session
        conversation_id: Conversation ID to fetch messages from
        user_id: User ID (owner filter, data isolation check)
        limit: Maximum number of messages to return (default: 50)

    Returns:
        List of messages in chronological order (oldest first), limited to N most recent

    Example:
        >>> messages = await get_conversation_messages(
        ...     session,
        ...     conversation_id=1,
        ...     user_id=1,
        ...     limit=50
        ... )
        >>> len(messages)
        10
        >>> messages[0].created_at < messages[-1].created_at
        True
    """
    # First, verify conversation belongs to user (data isolation)
    conv_statement = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id,
    )
    conv_result = await session.execute(conv_statement)
    conversation = conv_result.scalar_one_or_none()

    if not conversation:
        return []

    # Fetch last N messages in reverse chronological order, then reverse
    statement = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.desc())
        .limit(limit)
    )
    result = await session.execute(statement)
    messages = result.scalars().all()

    # Return in chronological order (oldest first)
    return list(reversed(messages))


async def count_messages(
    session: AsyncSession,
    conversation_id: int,
    user_id: int,
) -> int:
    """
    Count total messages in a conversation.

    Constitutional Principle II: Verifies conversation belongs to user.
    Used to enforce 500 message limit (triggers auto-archive when reached).

    Args:
        session: Async database session
        conversation_id: Conversation ID to count messages for
        user_id: User ID (owner filter, data isolation check)

    Returns:
        Total number of messages in the conversation

    Example:
        >>> count = await count_messages(session, conversation_id=1, user_id=1)
        >>> count
        42
    """
    # First, verify conversation belongs to user (data isolation)
    conv_statement = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id,
    )
    conv_result = await session.execute(conv_statement)
    conversation = conv_result.scalar_one_or_none()

    if not conversation:
        return 0

    # Count messages
    count_statement = select(func.count(Message.id)).where(
        Message.conversation_id == conversation_id
    )
    result = await session.execute(count_statement)
    return result.scalar_one()
