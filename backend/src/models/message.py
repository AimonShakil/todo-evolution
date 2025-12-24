"""
Message model for Phase III - Agentic AI Chatbot.

Represents individual message in a conversation (user input, agent response, or tool result).

Constitutional Alignment:
- Principle II: User isolation (user_id foreign key for data isolation queries)
- Principle III: Stateless architecture (all message state in database)
- Principle VI: Database standards (SQLModel ORM, proper indexes, CHECK constraints)
- Principle XXVI: Conversation persistence (chronological message history)
"""

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .conversation import Conversation
    from .user import User


class Message(SQLModel, table=True):
    """
    Individual message in a conversation.

    Role types:
    - "user": Human input message
    - "assistant": AI agent response message
    - "tool": Tool call result (optional, for debugging/audit trail)

    Constraints:
    - Content max 4000 characters (enforced by Pydantic validation + database)
    - 500 messages per conversation (application-enforced, triggers auto-archive)
    - user_id must match conversation.user_id (data isolation)
    """

    __tablename__ = "message"

    # Primary key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Foreign keys
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    user_id: int = Field(foreign_key="user.id", index=True)

    # Content
    role: str = Field(max_length=20)  # Enum: user, assistant, tool
    content: str = Field(max_length=4000, min_length=1)

    # Timestamp
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")
    user: "User" = Relationship(back_populates="messages")
