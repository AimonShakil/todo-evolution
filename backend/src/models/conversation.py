"""
Conversation model for Phase III - Agentic AI Chatbot.

Represents a chat session between user and AI agent. Each user can have multiple
conversations, but only one active conversation at a time.

Constitutional Alignment:
- Principle II: User isolation (user_id foreign key, CASCADE delete)
- Principle III: Stateless architecture (all conversation state in database)
- Principle VI: Database standards (SQLModel ORM, proper indexes)
- Principle XXVI: Conversation persistence (database-backed conversation history)
"""

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .message import Message
    from .user import User


class Conversation(SQLModel, table=True):
    """
    Chat session between user and AI agent.

    Lifecycle:
    - Created when user sends first message without active conversation
    - Active until 500 messages reached (auto-archived) or user creates new
    - Archived conversations remain accessible for 90 days (then auto-deleted)

    Constraints:
    - One active conversation per user (application-enforced)
    - Foreign key CASCADE on user deletion
    """

    __tablename__ = "conversation"

    # Primary key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Foreign keys
    user_id: int = Field(foreign_key="user.id", index=True)

    # Status
    is_active: bool = Field(default=True, index=True)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    messages: list["Message"] = Relationship(back_populates="conversation")
    user: "User" = Relationship(back_populates="conversations")
