---
name: sqlmodel-schemas
description: Generate SQLModel database schemas with constitutional requirements (user_id, created_at, updated_at, indexes). Use when creating or modifying database models for any phase.
allowed-tools: Read, Write, Edit
---

# SQLModel Schema Patterns Skill

Standard schema patterns following Constitutional Principle VI (Database Standards).

## Constitutional Requirements

Every SQLModel table MUST include:

1. **id**: Primary key (auto-increment)
2. **user_id**: Foreign key for user isolation (indexed)
3. **created_at**: Timestamp of creation
4. **updated_at**: Timestamp of last modification
5. **Indexes**: On user_id, status/priority fields, due_date

## Base Task Model Template

```python
"""Database models using SQLModel."""
from sqlmodel import Field, SQLModel, Index
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    """Task model with user isolation and timestamps.

    All fields comply with Constitutional Principle VI.
    """

    __tablename__ = "tasks"

    # ===== REQUIRED FIELDS (Constitutional) =====
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, foreign_key="users.id")  # User isolation
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # ===== TASK-SPECIFIC FIELDS =====
    title: str = Field(max_length=200, min_length=1)
    description: Optional[str] = Field(default=None, max_length=2000)
    completed: bool = Field(default=False)

    # ===== INDEXES (Constitutional requirement) =====
    __table_args__ = (
        # Composite index for common query pattern
        Index('ix_tasks_user_id_completed', 'user_id', 'completed'),
        Index('ix_tasks_user_id_created_at', 'user_id', 'created_at'),
    )

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"Task(id={self.id}, user_id='{self.user_id}', title='{self.title[:30]}...')"
```

## Extended Task Model (Phase V: Intermediate & Advanced Features)

```python
from enum import Enum

class Priority(str, Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class RecurrencePattern(str, Enum):
    """Task recurrence patterns."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

class Task(SQLModel, table=True):
    """Extended task model with intermediate and advanced features."""

    __tablename__ = "tasks"

    # ===== REQUIRED FIELDS (Constitutional) =====
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # ===== BASIC FEATURES (Phase I-V) =====
    title: str = Field(max_length=200, min_length=1)
    description: Optional[str] = Field(default=None, max_length=2000)
    completed: bool = Field(default=False)

    # ===== INTERMEDIATE FEATURES (Phase V) =====
    priority: Priority = Field(default=Priority.MEDIUM)
    tags: Optional[str] = Field(default=None, max_length=500)  # Comma-separated

    # ===== ADVANCED FEATURES (Phase V) =====
    due_date: Optional[datetime] = Field(default=None)
    reminder_at: Optional[datetime] = Field(default=None)
    recurrence_pattern: Optional[RecurrencePattern] = Field(default=None)
    recurrence_end_date: Optional[datetime] = Field(default=None)

    # ===== INDEXES (Constitutional requirement) =====
    __table_args__ = (
        Index('ix_tasks_user_id_completed', 'user_id', 'completed'),
        Index('ix_tasks_user_id_priority', 'user_id', 'priority'),
        Index('ix_tasks_user_id_due_date', 'user_id', 'due_date'),
        Index('ix_tasks_user_id_created_at', 'user_id', 'created_at'),
    )

    def __repr__(self) -> str:
        return f"Task(id={self.id}, title='{self.title[:30]}...', priority={self.priority})"
```

## User Model (Phase II+: Better Auth Integration)

```python
class User(SQLModel, table=True):
    """User model managed by Better Auth.

    Note: Better Auth creates its own users table.
    This is for reference/joins only.
    """

    __tablename__ = "users"

    # ===== REQUIRED FIELDS =====
    id: str = Field(primary_key=True)  # Better Auth uses UUID strings
    email: str = Field(unique=True, index=True, max_length=255)
    name: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # ===== INDEXES =====
    __table_args__ = (
        Index('ix_users_email', 'email'),
    )

    def __repr__(self) -> str:
        return f"User(id='{self.id}', email='{self.email}')"
```

## Conversation Model (Phase III+: AI Chatbot)

```python
class Conversation(SQLModel, table=True):
    """Conversation model for chatbot persistence."""

    __tablename__ = "conversations"

    # ===== REQUIRED FIELDS (Constitutional) =====
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # ===== CONVERSATION-SPECIFIC FIELDS =====
    title: Optional[str] = Field(default=None, max_length=200)  # Auto-generated
    archived: bool = Field(default=False)

    # ===== INDEXES =====
    __table_args__ = (
        Index('ix_conversations_user_id_created_at', 'user_id', 'created_at'),
        Index('ix_conversations_user_id_archived', 'user_id', 'archived'),
    )


class Message(SQLModel, table=True):
    """Message model for conversation history."""

    __tablename__ = "messages"

    # ===== REQUIRED FIELDS (Constitutional) =====
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, foreign_key="users.id")  # Denormalized for queries
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # ===== MESSAGE-SPECIFIC FIELDS =====
    conversation_id: int = Field(foreign_key="conversations.id")
    role: str = Field(max_length=20)  # "user" or "assistant"
    content: str = Field(max_length=10000)

    # ===== INDEXES =====
    __table_args__ = (
        Index('ix_messages_conversation_id_created_at', 'conversation_id', 'created_at'),
        Index('ix_messages_user_id_created_at', 'user_id', 'created_at'),
    )
```

## Field Validation Patterns

### String Fields with Constraints

```python
from pydantic import field_validator

class Task(SQLModel, table=True):
    title: str = Field(max_length=200, min_length=1)

    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        """Validate title is not empty or whitespace."""
        if not v or len(v.strip()) == 0:
            raise ValueError("Title cannot be empty")
        return v.strip()

    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v: Optional[str]) -> Optional[str]:
        """Validate tags format (comma-separated)."""
        if v is None:
            return None

        # Check max number of tags
        tags = [tag.strip() for tag in v.split(',')]
        if len(tags) > 10:
            raise ValueError("Maximum 10 tags allowed")

        # Check tag length
        for tag in tags:
            if len(tag) > 50:
                raise ValueError("Each tag must be ≤50 characters")

        return ','.join(tags)
```

### Datetime Fields with Validation

```python
class Task(SQLModel, table=True):
    due_date: Optional[datetime] = Field(default=None)
    reminder_at: Optional[datetime] = Field(default=None)

    @field_validator('due_date')
    @classmethod
    def due_date_not_past(cls, v: Optional[datetime]) -> Optional[datetime]:
        """Validate due date is not in the past."""
        if v is not None and v < datetime.utcnow():
            raise ValueError("Due date cannot be in the past")
        return v

    @field_validator('reminder_at')
    @classmethod
    def reminder_before_due(cls, v: Optional[datetime], info) -> Optional[datetime]:
        """Validate reminder is before due date."""
        if v is None:
            return None

        due_date = info.data.get('due_date')
        if due_date and v > due_date:
            raise ValueError("Reminder must be before due date")

        return v
```

## Relationships (Phase II+)

```python
from sqlmodel import Relationship
from typing import List

class User(SQLModel, table=True):
    """User with relationships to tasks and conversations."""
    id: str = Field(primary_key=True)
    email: str = Field(unique=True, index=True)

    # Relationships
    tasks: List["Task"] = Relationship(back_populates="user")
    conversations: List["Conversation"] = Relationship(back_populates="user")


class Task(SQLModel, table=True):
    """Task with relationship to user."""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id")

    # Relationship
    user: Optional[User] = Relationship(back_populates="tasks")
```

## Database Migrations with Alembic (Phase II+)

### Setup Alembic

```bash
# Install Alembic
uv pip install alembic

# Initialize Alembic
alembic init alembic

# Configure env.py to use SQLModel
```

### alembic/env.py Configuration

```python
"""Alembic environment configuration."""
from alembic import context
from sqlmodel import SQLModel
from backend.models import Task, User, Conversation, Message  # Import all models

target_metadata = SQLModel.metadata

def run_migrations_online():
    """Run migrations in 'online' mode."""
    from sqlmodel import create_engine
    from backend.db import DATABASE_URL

    connectable = create_engine(DATABASE_URL)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()
```

### Create Migration

```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "add priority and tags to tasks"

# Review generated migration
cat alembic/versions/xxxxx_add_priority_and_tags.py

# Apply migration
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## Schema Evolution Best Practices

### Adding Nullable Columns (Safe)

```python
# Migration: Add optional fields without breaking existing data
class Task(SQLModel, table=True):
    # Existing fields...
    priority: Optional[Priority] = Field(default=None)  # Nullable
    tags: Optional[str] = Field(default=None)  # Nullable
```

### Adding Non-Nullable Columns (Requires Default)

```python
# Migration: Add required field with default value
class Task(SQLModel, table=True):
    # Existing fields...
    priority: Priority = Field(default=Priority.MEDIUM)  # Has default
```

### Renaming Columns (Two-Phase)

```python
# Phase 1: Add new column, backfill data
class Task(SQLModel, table=True):
    title: str = Field(...)  # Old
    task_title: str = Field(...)  # New (backfilled from title)

# Phase 2: Remove old column (after backfill complete)
class Task(SQLModel, table=True):
    task_title: str = Field(...)  # New (now primary)
```

## MCP Integration (Context7)

When working with SQLModel, fetch official documentation:

```
Defining relationships?
  → mcp__context7__get-library-docs("/tiangolo/sqlmodel", topic="relationships")

Advanced queries?
  → mcp__context7__get-library-docs("/tiangolo/sqlmodel", topic="queries")

Migrations?
  → mcp__context7__get-library-docs("/alembic/alembic", topic="autogenerate")
```

## Common Pitfalls

### ❌ Missing Constitutional Fields
```python
# Missing user_id, created_at, updated_at
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str  # Where is user_id?
```

### ❌ No Indexes on Query Columns
```python
# Frequently queried but not indexed
class Task(SQLModel, table=True):
    user_id: str  # Should have index=True
    completed: bool  # Should be indexed for filtering
```

### ❌ Mutable Defaults
```python
# Dangerous! Shares list across instances
class Task(SQLModel, table=True):
    tags: List[str] = Field(default=[])  # BAD

# Use default_factory instead
tags: List[str] = Field(default_factory=list)  # GOOD
```

## Constitutional Compliance Checklist

Before considering schema complete:

- [ ] **user_id** field exists with index
- [ ] **created_at** field with datetime default
- [ ] **updated_at** field with datetime default
- [ ] **Indexes** on user_id and frequently queried columns
- [ ] **Foreign keys** properly defined
- [ ] **Field validation** for critical fields
- [ ] **Type hints** on all fields
- [ ] **Docstrings** on model and validators

## Testing Schemas

```python
def test_task_model_constitutional_fields():
    """Verify all constitutional fields exist."""
    task = Task(user_id="alice", title="Test")

    assert hasattr(task, 'id')
    assert hasattr(task, 'user_id')
    assert hasattr(task, 'created_at')
    assert hasattr(task, 'updated_at')

def test_task_title_validation():
    """Validate title constraints."""
    with pytest.raises(ValueError, match="Title cannot be empty"):
        Task(user_id="alice", title="")

    with pytest.raises(ValueError):
        Task(user_id="alice", title="x" * 201)  # Too long
```

## Phase-Specific Schemas Summary

| Phase | Models | Features |
|-------|--------|----------|
| **I** | Task | Basic CRUD (title, completed) |
| **II** | Task, User | Web app with Better Auth |
| **III** | Task, User, Conversation, Message | AI chatbot persistence |
| **IV** | Same as III | No schema changes (K8s deployment) |
| **V** | Task (extended) | Priority, tags, due dates, recurrence |
