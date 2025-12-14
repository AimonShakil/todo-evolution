"""Task model for Todo Evolution.

This module defines the Task entity with SQLModel ORM mapping
and Pydantic validation.
"""

from datetime import datetime, timezone
from typing import Annotated, Optional

from pydantic import AfterValidator
from sqlmodel import Field, SQLModel


def validate_title(v: str) -> str:
    """Validate title is not empty and within length limits."""
    if not v or len(v) == 0:
        raise ValueError("Title cannot be empty")
    if len(v) > 200:
        raise ValueError("Title must be 1-200 characters")
    return v


def validate_user_id(v: str) -> str:
    """Validate user_id is not empty or whitespace-only."""
    if not v or v.strip() == "":
        raise ValueError("User ID cannot be empty")
    return v


TitleStr = Annotated[str, AfterValidator(validate_title)]
UserIdStr = Annotated[str, AfterValidator(validate_user_id)]


class Task(SQLModel, table=True):
    """Task entity representing a user's todo item.

    Attributes:
        id: Auto-incrementing primary key.
        user_id: User identifier for task ownership (indexed for filtering).
        title: Task description (1-200 characters).
        completed: Task completion status (default: False).
        created_at: Timestamp when task was created.
        updated_at: Timestamp when task was last modified.
    """

    model_config = {"validate_assignment": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: UserIdStr = Field(index=True)  # FR-007: indexed for user isolation queries
    title: TitleStr
    completed: bool = Field(default=False)  # FR-005: default=false
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))  # FR-005
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))  # FR-005
