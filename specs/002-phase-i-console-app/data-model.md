# Data Model: Phase I - Console Todo App

**Feature**: Phase I - Console Todo App
**Date**: 2025-12-08
**Branch**: 002-phase-i-console-app
**Phase**: Phase 1 - Data Model Design

---

## Overview

Phase I uses a **single entity model** (Task) with a **future-proof schema** including all Phase V fields as nullable columns. This prevents schema migrations when progressing through phases II-V (constitutional principle I: spec-driven development).

**Key Design Decisions**:
1. **Future-Proof from Day 1**: All Phase V fields (description, priority, tags, due_date, recurrence_pattern) included as nullable
2. **User Isolation**: `user_id` field (string in Phase I, migrates to integer foreign key in Phase II)
3. **Stateless Architecture**: No in-memory state; all data persisted to SQLite database
4. **Type Safety**: SQLModel (Pydantic + SQLAlchemy) provides runtime and compile-time validation

---

## Entity: Task

**Purpose**: Represents a single todo task with title, completion status, and user ownership

**Phase I Usage**: Core entity for all CRUD operations (add, view, update, delete, complete tasks)

**Phase II-V Evolution**:
- Phase I: title, completed, user_id (string)
- Phase II: +description (text field)
- Phase V Intermediate: +priority, +tags, +due_date
- Phase V Advanced: +recurrence_pattern

### Attributes

| Field | Type | Constraints | Phase | Description |
|-------|------|-------------|-------|-------------|
| `id` | Integer | Primary key, auto-increment | All | Unique task identifier |
| `user_id` | String | Required, indexed | I (string) → II+ (int FK) | Username in Phase I, migrates to user.id foreign key in Phase II |
| `title` | String | Required, 1-200 characters | All | Task description (what needs to be done) |
| `description` | String | Nullable | II+ | Detailed task description (unused in Phase I) |
| `completed` | Boolean | Default: false | All | Task completion status |
| `priority` | String | Nullable, enum: high/medium/low | V Intermediate | Task priority level (unused in Phase I-IV) |
| `tags` | String | Nullable, JSON-encoded array | V Intermediate | Task tags/categories (unused in Phase I-IV) |
| `due_date` | DateTime | Nullable | V Intermediate | Task deadline (unused in Phase I-IV) |
| `recurrence_pattern` | String | Nullable, e.g., "daily", "weekly", cron | V Advanced | Recurring task pattern (unused in Phase I-IV) |
| `created_at` | DateTime | Auto-set on creation (UTC) | All | Timestamp when task was created |
| `updated_at` | DateTime | Auto-update on modification (UTC) | All | Timestamp of last update |

### SQLModel Implementation

```python
from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime

class Task(SQLModel, table=True):
    """
    Task entity with future-proof schema for all phases (I-V).

    Phase I Active Fields:
    - id, user_id, title, completed, created_at, updated_at

    Phase V Fields (nullable, unused in Phase I):
    - description, priority, tags, due_date, recurrence_pattern

    Constitutional Alignment:
    - Principle I: Future-proof schema (no migrations Phase I-V)
    - Principle II: User isolation (user_id indexed for fast filtering)
    - Principle IV: Stateless (database-backed, no in-memory state)
    - Principle IX: Type safety (Pydantic validation + mypy type hints)
    """

    # === Phase I Active Fields ===
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, min_length=1)  # Username string in Phase I
    title: str = Field(min_length=1, max_length=200)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # === Future-Proof Phase V Fields (nullable, unused in Phase I) ===
    description: Optional[str] = Field(default=None)  # Phase II+
    priority: Optional[str] = Field(default=None)  # Phase V Intermediate (enum: high/medium/low)
    tags: Optional[str] = Field(default=None)  # Phase V Intermediate (JSON-encoded array)
    due_date: Optional[datetime] = Field(default=None)  # Phase V Intermediate
    recurrence_pattern: Optional[str] = Field(default=None)  # Phase V Advanced (e.g., "daily", "weekly")

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": "alice",
                "title": "Buy groceries",
                "completed": False,
                "created_at": "2025-12-08T10:30:00Z",
                "updated_at": "2025-12-08T10:30:00Z",
                "description": None,  # Unused in Phase I
                "priority": None,     # Unused in Phase I
                "tags": None,         # Unused in Phase I
                "due_date": None,     # Unused in Phase I
                "recurrence_pattern": None,  # Unused in Phase I
            }
        }
```

### Validation Rules

**Enforced by SQLModel/Pydantic**:
- ✅ `title`: 1-200 characters (Field validation)
- ✅ `user_id`: Non-empty string (Field validation)
- ✅ `completed`: Boolean type (Pydantic type coercion)
- ✅ `created_at`, `updated_at`: Valid datetime (Pydantic type validation)

**Enforced by Application Logic**:
- ✅ Phase I fields must NOT be null (id, user_id, title, completed, created_at, updated_at)
- ✅ Phase V fields MUST be null in Phase I (description, priority, tags, due_date, recurrence_pattern)
- ✅ `updated_at` automatically set on modification (application-managed or database trigger)

**Business Rules**:
- Title cannot be empty string (min_length=1)
- Title cannot exceed 200 characters (max_length=200)
- Username cannot be empty (min_length=1)
- Completed defaults to false on creation
- All nullable Phase V fields default to None in Phase I

### Relationships

**Phase I**: No relationships (standalone entity)
- `user_id` is a string (username), not a foreign key
- No users table in Phase I

**Phase II Migration**:
```python
# Phase II: user_id becomes foreign key
user_id: int = Field(foreign_key="users.id", index=True)

# Relationship to User entity
user: Optional["User"] = Relationship(back_populates="tasks")
```

**Phase V Advanced Migration** (optional):
```python
# Team collaboration: many-to-many with users
team_members: List["User"] = Relationship(link_model=TaskTeamLink)

# Task dependencies: self-referential many-to-many
depends_on: List["Task"] = Relationship(link_model=TaskDependency)
```

### Database Schema (SQLite)

```sql
CREATE TABLE task (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    title TEXT NOT NULL CHECK(length(title) BETWEEN 1 AND 200),
    completed BOOLEAN NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Future-proof Phase V fields (nullable, unused in Phase I)
    description TEXT,
    priority TEXT,  -- Will be CHECK(priority IN ('high', 'medium', 'low')) in Phase V
    tags TEXT,  -- JSON-encoded array in Phase V
    due_date DATETIME,
    recurrence_pattern TEXT
);

-- Performance optimization: Index on user_id for fast filtering
CREATE INDEX idx_task_user_id ON task(user_id);

-- Phase II migration will add:
-- ALTER TABLE task ADD CONSTRAINT fk_task_user FOREIGN KEY (user_id) REFERENCES users(id);
```

### State Transitions

**Completion Status Lifecycle**:
```
[Created] → completed = False (default)
    ↓
[Mark Complete] → completed = True
    ↓
[Toggle Incomplete] → completed = False
    ↓
[Toggle Complete] → completed = True
    (repeatable)
```

**No Other State Machines in Phase I**:
- No draft/published states
- No archived/deleted states (delete is permanent)
- No approval workflows

---

## Data Validation Examples

### Valid Task Creation

```python
# Example 1: Minimal valid task
task = Task(
    user_id="alice",
    title="Buy groceries"
)
# Result: ✅ Valid
# - completed defaults to False
# - created_at, updated_at auto-set
# - All Phase V fields default to None

# Example 2: Maximum length title
task = Task(
    user_id="bob",
    title="A" * 200  # Exactly 200 characters
)
# Result: ✅ Valid

# Example 3: Special characters and emojis
task = Task(
    user_id="charlie",
    title="Buy milk & eggs (2 gallons) for $5.99 🥛"
)
# Result: ✅ Valid (Unicode support)
```

### Invalid Task Creation (Validation Errors)

```python
# Example 1: Empty title
task = Task(user_id="alice", title="")
# Result: ❌ ValidationError: title must be at least 1 character

# Example 2: Title too long
task = Task(user_id="alice", title="A" * 201)
# Result: ❌ ValidationError: title must be at most 200 characters

# Example 3: Empty username
task = Task(user_id="", title="Buy groceries")
# Result: ❌ ValidationError: user_id must be at least 1 character

# Example 4: Missing required field
task = Task(title="Buy groceries")  # No user_id
# Result: ❌ ValidationError: field required
```

---

## Phase Migration Strategy

### Phase I → Phase II Migration

**Data Migration**:
1. Create `users` table in PostgreSQL
2. Migrate username strings to user records (insert into users table)
3. Update tasks table: `user_id` (string) → `user_id` (integer foreign key)

```python
# Migration pseudocode
for task in tasks:
    # Find or create user by username
    user = get_or_create_user(email=f"{task.user_id}@example.com")

    # Update task.user_id from string to integer
    task.user_id = user.id  # Type changes from str to int

# Add foreign key constraint
ALTER TABLE task ADD CONSTRAINT fk_task_user FOREIGN KEY (user_id) REFERENCES users(id);
```

**Code Changes**:
```python
# Phase I
class Task(SQLModel, table=True):
    user_id: str = Field(index=True)

# Phase II
class Task(SQLModel, table=True):
    user_id: int = Field(foreign_key="users.id", index=True)
    user: Optional["User"] = Relationship(back_populates="tasks")
```

### Phase II → Phase V Migration

**Data Migration**: None required (fields already exist as nullable)

**Code Changes**: Update validation to enforce Phase V constraints
```python
# Phase V Intermediate: Enable priority, tags, due_date
class Task(SQLModel, table=True):
    # ... existing fields ...

    priority: Optional[str] = Field(
        default=None,
        regex="^(high|medium|low)$"  # Enum validation
    )
    tags: Optional[str] = Field(default=None)  # JSON validation in service layer
    due_date: Optional[datetime] = Field(default=None)  # Future dates only

# Phase V Advanced: Enable recurrence_pattern
    recurrence_pattern: Optional[str] = Field(
        default=None,
        regex="^(daily|weekly|monthly|yearly|custom)$"
    )
```

---

## Database Queries Examples

### User Isolation Queries

```python
from sqlmodel import Session, select

# Get all tasks for user (user isolation enforced)
def get_all_tasks(session: Session, user_id: str) -> list[Task]:
    statement = select(Task).where(Task.user_id == user_id)
    return session.exec(statement).all()

# Get single task with user ownership verification
def get_task(session: Session, user_id: str, task_id: int) -> Optional[Task]:
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id  # User isolation: prevents access to other users' tasks
    )
    return session.exec(statement).first()

# Update task title with user ownership verification
def update_task_title(session: Session, user_id: str, task_id: int, new_title: str) -> Optional[Task]:
    task = get_task(session, user_id, task_id)
    if not task:
        return None  # Task not found OR belongs to different user

    task.title = new_title
    task.updated_at = datetime.utcnow()  # Update timestamp
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

### Performance-Optimized Queries

```python
# Index on user_id enables fast filtering (SC-010: <500ms with 10,000 tasks)
statement = select(Task).where(Task.user_id == user_id)

# Query plan with index:
# SCAN TABLE task USING INDEX idx_task_user_id (user_id=?)
# vs without index:
# SCAN TABLE task (full table scan - slow with 10,000+ rows)
```

---

## Constitutional Alignment

| Principle | Implementation | Verification |
|-----------|---------------|-------------|
| **I. Spec-Driven** | Future-proof schema (all Phase V fields from day 1) | ✅ No schema migrations needed Phase I-V |
| **II. User Isolation** | `user_id` field indexed, all queries filter by user_id | ✅ Integration tests verify user A cannot access user B's tasks |
| **IV. Stateless** | Database-backed state, no in-memory caching | ✅ All data persists to SQLite |
| **IX. Code Quality** | SQLModel with type hints, Pydantic validation | ✅ mypy --strict, runtime validation |
| **X. Testing** | Unit tests for validation rules, integration tests for queries | ✅ ≥80% coverage (pytest --cov) |
| **XII. Security** | Parameterized queries via SQLModel ORM | ✅ SQL injection prevention |

---

## Next Steps

1. **Phase 1: Contracts** - Generate `contracts/` with CLI command interface definitions
2. **Phase 1: Quickstart** - Generate `quickstart.md` with setup and usage guide
3. **Phase 1: Agent Context Update** - Run `.specify/scripts/bash/update-agent-context.sh claude`
4. **Constitution Re-Check** - Validate Phase 1 design against all applicable principles

---

**Data Model Complete** - Ready to proceed to Contracts generation
