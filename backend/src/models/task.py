"""
Task entity with Phase II schema (user_id as foreign key).

Phase I → Phase II Migration:
- user_id: str (username) → int (foreign key to users.id)
- Added description field (nullable)

Constitutional Alignment:
- Principle I: Future-proof schema (Phase V fields remain nullable)
- Principle II: User isolation (foreign key enforces ownership)
- Principle IV: Stateless (PostgreSQL-backed, no in-memory state)
- Principle IX: Type safety (Pydantic validation + mypy type hints)
"""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Task(SQLModel, table=True):
    """
    Task entity with Phase II schema.

    Phase II Active Fields:
        id: Unique task identifier
        user_id: Foreign key to users.id (owner)
        title: Task description (1-200 characters)
        description: Detailed task description (nullable, Phase II feature)
        completed: Task completion status (default: False)
        created_at: Task creation timestamp (UTC)
        updated_at: Last update timestamp (UTC)

    Phase V Fields (nullable, unused in Phase II):
        priority: Task priority (high/medium/low)
        tags: Task tags/categories (JSON-encoded array)
        due_date: Task deadline
        recurrence_pattern: Recurring task pattern (e.g., "daily", "weekly")

    Constitutional Principles:
        - Principle I: Spec-Driven Development (future-proof schema)
        - Principle II: User Data Isolation (user_id foreign key)
        - Principle IV: Stateless Architecture (database-backed)
        - Principle IX: Code Quality Standards (type hints, docstrings)

    Example:
        >>> task = Task(
        ...     user_id=1,
        ...     title="Buy groceries",
        ...     description="Get milk, eggs, and bread"
        ... )
        >>> session.add(task)
        >>> session.commit()
    """

    __tablename__ = "task"

    # === Phase II Active Fields ===

    # Primary key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Foreign key to user table
    user_id: int = Field(foreign_key="user.id", index=True)

    # Task details
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # === Future-Proof Phase V Fields (nullable, unused in Phase II) ===

    priority: Optional[str] = Field(default=None)
    tags: Optional[str] = Field(default=None)
    due_date: Optional[datetime] = Field(default=None)
    recurrence_pattern: Optional[str] = Field(default=None)
