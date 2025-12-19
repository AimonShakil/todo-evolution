"""
User entity for Better Auth integration (Phase II).

Constitutional Alignment:
- Principle III: Authentication (Better Auth integration)
- Principle II: User isolation (one-to-many with tasks)
- Principle IX: Type safety (Pydantic validation + mypy)
"""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """User entity for Better Auth integration."""

    # Primary key
    id: Optional[int] = Field(default=None, primary_key=True)

    # User credentials
    email: str = Field(
        unique=True,
        index=True,
        min_length=3,
        max_length=255,
    )
    name: str = Field(min_length=1, max_length=100)
    password_hash: str = Field(min_length=1)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
