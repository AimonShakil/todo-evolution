# Data Model: Phase II - Web Todo App

**Feature**: Phase II - Web Todo App
**Date**: 2025-12-15
**Branch**: 003-phase-ii-web-app
**Phase**: STEP 0.6 - Database Migration Strategy

---

## Overview

Phase II migrates from **SQLite (Phase I)** to **PostgreSQL (Neon)** and introduces multi-user authentication with **Better Auth**. This requires:

1. **New Entity**: `User` table for Better Auth integration
2. **Schema Change**: Task `user_id` field migrates from `string` (username) to `int` (foreign key to User.id)
3. **Reusable Intelligence (RI)**: Preserve Phase I Task model, validators, TaskService patterns

**Key Design Decisions**:
1. **Zero Breaking Changes**: Phase V fields (description, priority, tags, due_date, recurrence_pattern) remain nullable
2. **User Isolation Preserved**: All queries still filter by `user_id` (Constitutional Principle II)
3. **Stateless Architecture Maintained**: No in-memory state, PostgreSQL-backed (Constitutional Principle IV)
4. **Type Safety Enhanced**: SQLModel with async PostgreSQL support (asyncpg)

---

## Migration Strategy: SQLite → PostgreSQL

### Option Evaluation

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| **1. Fresh Start** | Clean PostgreSQL schema from day 1 | Loses Phase I data, requires manual re-entry | ❌ Rejected - data loss unacceptable |
| **2. SQLite → PostgreSQL Data Export** | Preserves existing data, one-time migration | Complex data transformation (user_id string → int) | ✅ **Selected** - preserves data + enables Better Auth |
| **3. Dual Support (SQLite + PostgreSQL)** | Gradual migration, no data loss | Increases complexity, violates simplicity principle | ❌ Rejected - unnecessary complexity |

**Selected Approach**: **One-time data migration** from SQLite to PostgreSQL with automatic user creation.

### Migration Steps

**1. Export Phase I SQLite Data**
```bash
# Run in Phase I environment (if Phase I implementation exists)
sqlite3 todo.db ".mode insert tasks" ".output tasks_export.sql"
sqlite3 todo.db ".dump tasks"
```

**Alternative (No Phase I data exists)**: Skip export, start with empty PostgreSQL database.

**2. Create Users from Unique user_id Values**
```python
# Pseudocode for migration script (backend/scripts/migrate_sqlite_to_postgres.py)
import sqlite3
from sqlmodel import Session, create_engine, select
from src.models.user import User
from src.models.task import Task

# Step 1: Extract unique usernames from SQLite
sqlite_conn = sqlite3.connect("todo.db")
cursor = sqlite_conn.execute("SELECT DISTINCT user_id FROM task")
usernames = [row[0] for row in cursor.fetchall()]

# Step 2: Create User records in PostgreSQL
pg_engine = create_engine(DATABASE_URL)  # Neon PostgreSQL
with Session(pg_engine) as session:
    user_mapping = {}  # username → user.id

    for username in usernames:
        # Create user with placeholder email
        user = User(
            email=f"{username}@migrated.local",  # Placeholder email
            name=username,
            password_hash="MIGRATED_NO_PASSWORD"  # Must reset password on first login
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        user_mapping[username] = user.id

# Step 3: Migrate tasks with updated user_id
cursor = sqlite_conn.execute("SELECT id, user_id, title, completed, created_at, updated_at FROM task")
for row in cursor.fetchall():
    task_id, username, title, completed, created_at, updated_at = row
    task = Task(
        id=task_id,
        user_id=user_mapping[username],  # String → Integer FK
        title=title,
        completed=bool(completed),
        created_at=created_at,
        updated_at=updated_at,
        # Phase V fields remain NULL
        description=None,
        priority=None,
        tags=None,
        due_date=None,
        recurrence_pattern=None,
    )
    session.add(task)

session.commit()
sqlite_conn.close()
```

**3. Verification Queries**
```sql
-- Verify user count matches unique SQLite user_id count
SELECT COUNT(*) FROM users;

-- Verify task count matches SQLite task count
SELECT COUNT(*) FROM tasks;

-- Verify user_id foreign key integrity
SELECT t.id, t.title, u.email
FROM tasks t
JOIN users u ON t.user_id = u.id
LIMIT 10;
```

**4. Deployment Strategy**

- **Option A (Clean Slate)**: Start Phase II with empty PostgreSQL database (no migration needed)
- **Option B (Data Migration)**: If Phase I data exists, run migration script ONCE before Phase II launch
  - Store migration script in `backend/scripts/migrate_sqlite_to_postgres.py`
  - Document in README.md under "Phase I → Phase II Migration"
  - Execute BEFORE running `alembic upgrade head`

**Decision**: **Option A (Clean Slate)** - Phase II starts fresh since Phase I is not yet implemented. Migration script provided as reference for future use.

---

## Entity: User (New in Phase II)

**Purpose**: Represents an authenticated user with email, password, and Better Auth metadata

**Phase II Usage**: Required for Better Auth integration, owns tasks via `tasks` relationship

### Attributes

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | Primary key, auto-increment | Unique user identifier |
| `email` | String | Required, unique, indexed | User email (used for login) |
| `name` | String | Required | User display name |
| `password_hash` | String | Required | Bcrypt password hash (Better Auth managed) |
| `created_at` | DateTime | Auto-set on creation (UTC) | User registration timestamp |
| `updated_at` | DateTime | Auto-update on modification (UTC) | Last profile update timestamp |

### SQLModel Implementation

```python
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from datetime import datetime

class User(SQLModel, table=True):
    """
    User entity for Better Auth integration (Phase II).

    Constitutional Alignment:
    - Principle III: Authentication (Better Auth integration)
    - Principle II: User isolation (one-to-many with tasks)
    - Principle IX: Type safety (Pydantic validation + mypy)
    """
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, min_length=3, max_length=255)
    name: str = Field(min_length=1, max_length=100)
    password_hash: str = Field(min_length=1)  # Bcrypt hash (60 chars)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship: One user has many tasks
    tasks: List["Task"] = Relationship(back_populates="user")
```

### Database Schema (PostgreSQL)

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,  -- Bcrypt hash
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Performance optimization: Index on email for fast login lookups
CREATE UNIQUE INDEX idx_users_email ON users(email);
```

---

## Entity: Task (Updated from Phase I)

**Purpose**: Represents a todo task owned by a user (migrated from Phase I)

**Phase II Changes**:
1. `user_id` type changes: `str` → `int` (foreign key to User.id)
2. Added `description` field (nullable, Phase II feature)
3. Added `user` relationship (SQLModel Relationship)

**Phase V Fields (Unchanged)**: priority, tags, due_date, recurrence_pattern remain nullable

### Attributes (Phase II)

| Field | Type | Constraints | Phase | Description |
|-------|------|-------------|-------|-------------|
| `id` | Integer | Primary key, auto-increment | All | Unique task identifier |
| `user_id` | **Integer** | Foreign key to users.id, indexed | **II+** (was `str` in Phase I) | Owner user ID |
| `title` | String | Required, 1-200 characters | All | Task description |
| `description` | String | Nullable | **II+** (NEW) | Detailed task description |
| `completed` | Boolean | Default: false | All | Task completion status |
| `priority` | String | Nullable, enum: high/medium/low | V Intermediate | Task priority level (unused in Phase II) |
| `tags` | String | Nullable, JSON-encoded array | V Intermediate | Task tags/categories (unused in Phase II) |
| `due_date` | DateTime | Nullable | V Intermediate | Task deadline (unused in Phase II) |
| `recurrence_pattern` | String | Nullable, cron syntax | V Advanced | Recurring task pattern (unused in Phase II) |
| `created_at` | DateTime | Auto-set on creation (UTC) | All | Timestamp when task was created |
| `updated_at` | DateTime | Auto-update on modification (UTC) | All | Timestamp of last update |

### SQLModel Implementation (Phase II)

```python
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from datetime import datetime

class Task(SQLModel, table=True):
    """
    Task entity with Phase II schema (user_id as foreign key).

    Phase I → Phase II Migration:
    - user_id: str (username) → int (foreign key to users.id)
    - Added description field (nullable)
    - Added user relationship (SQLModel Relationship)

    Constitutional Alignment:
    - Principle I: Future-proof schema (Phase V fields remain nullable)
    - Principle II: User isolation (foreign key enforces ownership)
    - Principle IV: Stateless (PostgreSQL-backed, no in-memory state)
    - Principle IX: Type safety (Pydantic validation + mypy type hints)
    """
    __tablename__ = "tasks"

    # === Phase II Active Fields ===
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)  # CHANGED: str → int
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None)  # NEW in Phase II
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # === Future-Proof Phase V Fields (nullable, unused in Phase II) ===
    priority: Optional[str] = Field(default=None)  # Phase V Intermediate
    tags: Optional[str] = Field(default=None)  # Phase V Intermediate (JSON array)
    due_date: Optional[datetime] = Field(default=None)  # Phase V Intermediate
    recurrence_pattern: Optional[str] = Field(default=None)  # Phase V Advanced

    # Relationship: Many tasks belong to one user
    user: Optional["User"] = Relationship(back_populates="tasks")
```

### Database Schema (PostgreSQL)

```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL CHECK(LENGTH(title) BETWEEN 1 AND 200),
    description TEXT,  -- NEW in Phase II
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    -- Future-proof Phase V fields (nullable, unused in Phase II)
    priority VARCHAR(10),  -- Will be CHECK(priority IN ('high', 'medium', 'low')) in Phase V
    tags TEXT,  -- JSON-encoded array in Phase V
    due_date TIMESTAMP,
    recurrence_pattern VARCHAR(50)
);

-- Performance optimization: Index on user_id for fast filtering
CREATE INDEX idx_tasks_user_id ON tasks(user_id);

-- Future Phase V indexes (not created in Phase II)
-- CREATE INDEX idx_tasks_due_date ON tasks(due_date) WHERE due_date IS NOT NULL;
-- CREATE INDEX idx_tasks_priority ON tasks(priority) WHERE priority IS NOT NULL;
```

---

## Reusable Intelligence (RI) from Phase I

### What to Preserve

**1. Task Model Patterns** (90% reusable):
- ✅ Validation rules (title 1-200 chars, user_id required)
- ✅ Timestamps (created_at, updated_at)
- ✅ Future-proof schema (Phase V fields remain nullable)
- ⚠️ **Change**: user_id type (`str` → `int`)

**2. Validators** (100% reusable):
```python
# src/lib/validators.py (Phase I)
def validate_title(title: str) -> str:
    """Validate task title is 1-200 characters."""
    if not title or len(title) < 1:
        raise ValueError("Title cannot be empty")
    if len(title) > 200:
        raise ValueError("Title cannot exceed 200 characters")
    return title.strip()

# Phase II: Same validator, works identically
```

**3. TaskService Patterns** (80% reusable):

**Phase I Pattern** (SQLite, synchronous):
```python
def get_all_tasks(session: Session, user_id: str) -> list[Task]:
    statement = select(Task).where(Task.user_id == user_id)
    return session.exec(statement).all()
```

**Phase II Adaptation** (PostgreSQL, async):
```python
async def get_all_tasks(session: AsyncSession, user_id: int) -> list[Task]:
    statement = select(Task).where(Task.user_id == user_id)
    result = await session.execute(statement)
    return result.scalars().all()
```

**Changes**:
- `Session` → `AsyncSession` (async PostgreSQL support)
- `session.exec()` → `await session.execute()` (async execution)
- `user_id: str` → `user_id: int` (type change)
- `result.scalars().all()` (async result handling)

**4. User Isolation Patterns** (100% reusable):
```python
# Phase I & Phase II: Same pattern
def get_task(session: Session, user_id: str | int, task_id: int) -> Optional[Task]:
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id  # Constitutional Principle II
    )
    return session.exec(statement).first()
```

**5. Test Patterns** (100% reusable):
```python
# Phase I test pattern (user isolation)
def test_user_cannot_access_other_user_tasks():
    # User A creates task
    task_a = create_task(user_id="alice", title="Alice's task")

    # User B cannot see User A's tasks
    tasks_b = get_all_tasks(user_id="bob")
    assert task_a.id not in [t.id for t in tasks_b]

# Phase II: Same test, works identically (user_id values change to int)
async def test_user_cannot_access_other_user_tasks():
    # User A creates task
    task_a = await create_task(user_id=1, title="Alice's task")

    # User B cannot see User A's tasks
    tasks_b = await get_all_tasks(user_id=2)
    assert task_a.id not in [t.id for t in tasks_b]
```

### What to Adapt

| Phase I Component | Phase II Adaptation | Effort |
|-------------------|---------------------|--------|
| **Task Model** | Change `user_id: str` → `user_id: int`, add `description` field | Low (5 lines) |
| **TaskService** | Add `async`/`await`, change `Session` → `AsyncSession` | Medium (all methods) |
| **Validators** | No changes needed | None |
| **Database Config** | Change SQLite → PostgreSQL connection string | Low (1 line) |
| **Tests** | Add `async` to test functions, update fixtures | Medium (all tests) |

### RI Savings Estimate

**Without RI** (build from scratch):
- Task model design: 2 hours
- Validators: 1 hour
- Service layer: 4 hours
- User isolation logic: 2 hours
- Test patterns: 3 hours
- **Total**: 12 hours

**With RI** (adapt from Phase I):
- Task model adaptation: 0.5 hours
- Validators: 0 hours (reuse as-is)
- Service layer adaptation: 2 hours
- User isolation logic: 0 hours (reuse as-is)
- Test pattern adaptation: 1 hour
- **Total**: 3.5 hours

**Savings**: **8.5 hours** (70% reduction)

---

## Database Queries (Phase II)

### User Isolation Queries (Updated from Phase I)

```python
from sqlmodel import Session, select
from sqlalchemy.ext.asyncio import AsyncSession

# Get all tasks for user (async PostgreSQL)
async def get_all_tasks(session: AsyncSession, user_id: int) -> list[Task]:
    statement = select(Task).where(Task.user_id == user_id)
    result = await session.execute(statement)
    return result.scalars().all()

# Get single task with user ownership verification
async def get_task(session: AsyncSession, user_id: int, task_id: int) -> Optional[Task]:
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id  # User isolation: prevents access to other users' tasks
    )
    result = await session.execute(statement)
    return result.scalar_one_or_none()

# Create task with user ownership
async def create_task(session: AsyncSession, user_id: int, title: str, description: Optional[str] = None) -> Task:
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

# Update task title with user ownership verification
async def update_task_title(session: AsyncSession, user_id: int, task_id: int, new_title: str) -> Optional[Task]:
    task = await get_task(session, user_id, task_id)
    if not task:
        return None  # Task not found OR belongs to different user

    task.title = new_title
    task.updated_at = datetime.utcnow()  # Update timestamp
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task
```

### Authentication Queries (New in Phase II)

```python
# Find user by email (for login)
async def get_user_by_email(session: AsyncSession, email: str) -> Optional[User]:
    statement = select(User).where(User.email == email)
    result = await session.execute(statement)
    return result.scalar_one_or_none()

# Create new user (for signup)
async def create_user(session: AsyncSession, email: str, name: str, password_hash: str) -> User:
    user = User(
        email=email,
        name=name,
        password_hash=password_hash,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
```

---

## Alembic Migration Files (STEP 0.7 Preview)

### Migration 1: Create Users Table

```python
# alembic/versions/001_create_users_table.py
"""Create users table

Revision ID: 001
Revises:
Create Date: 2025-12-15
"""
from alembic import op
import sqlalchemy as sa

def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index('idx_users_email', 'users', ['email'], unique=True)

def downgrade() -> None:
    op.drop_index('idx_users_email', table_name='users')
    op.drop_table('users')
```

### Migration 2: Create Tasks Table

```python
# alembic/versions/002_create_tasks_table.py
"""Create tasks table

Revision ID: 002
Revises: 001
Create Date: 2025-12-15
"""
from alembic import op
import sqlalchemy as sa

def upgrade() -> None:
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        # Phase V fields (nullable)
        sa.Column('priority', sa.String(length=10), nullable=True),
        sa.Column('tags', sa.Text(), nullable=True),
        sa.Column('due_date', sa.DateTime(), nullable=True),
        sa.Column('recurrence_pattern', sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )
    op.create_index('idx_tasks_user_id', 'tasks', ['user_id'])

def downgrade() -> None:
    op.drop_index('idx_tasks_user_id', table_name='tasks')
    op.drop_table('tasks')
```

---

## Constitutional Alignment

| Principle | Implementation | Verification |
|-----------|---------------|-------------|
| **I. Spec-Driven** | Future-proof schema preserved (Phase V fields remain nullable) | ✅ No schema changes needed for Phase III-V |
| **II. User Isolation** | Foreign key enforces ownership, all queries filter by `user_id` | ✅ Integration tests verify user A cannot access user B's tasks |
| **III. Authentication** | Better Auth integration via User entity | ✅ Email/password authentication with JWT tokens |
| **IV. Stateless** | PostgreSQL-backed state, no in-memory caching | ✅ All data persists to Neon PostgreSQL |
| **IX. Code Quality** | SQLModel with type hints, Pydantic validation, async support | ✅ mypy --strict, runtime validation |
| **X. Testing** | Unit tests for models, integration tests for queries, ≥80% coverage | ✅ pytest --cov ≥80% |
| **XII. Security** | Parameterized queries via SQLModel ORM, bcrypt password hashing | ✅ SQL injection prevention, secure password storage |

---

## Next Steps

1. ✅ **STEP 0.6 Complete**: Database migration strategy documented
2. ⏳ **STEP 0.7**: Alembic setup (install, initialize, configure alembic.ini)
3. ⏳ **STEP 1**: Backend Foundation (models, services, routes, migrations)
4. ⏳ **STEP 2**: Backend Testing (unit, integration, ≥80% coverage)

---

**Data Model Complete** - Ready to proceed to STEP 0.7 (Alembic Setup)
