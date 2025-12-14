# Research: Phase I - Console Todo App

**Feature**: Phase I - Console Todo App
**Date**: 2025-12-08
**Branch**: 002-phase-i-console-app
**Phase**: Phase 0 - Technology Research & Best Practices

---

## Research Questions

### 1. Python ORM Selection for SQLite with Future-Proof Schema

**Question**: Which ORM best supports future-proof schema design (nullable Phase V fields) while maintaining type safety and validation?

**Options Considered**:
1. **SQLModel** (SQLAlchemy + Pydantic)
2. Raw SQLAlchemy
3. Peewee
4. No ORM (raw sqlite3)

**Decision**: ✅ **SQLModel**

**Rationale**:
- **Type Safety**: Pydantic integration provides runtime validation + mypy static type checking (constitutional requirement IX)
- **Future-Proof Support**: Nullable fields handled elegantly with `Optional[type] = None` syntax
- **Migration Path**: Phase II will use FastAPI (Pydantic-based), SQLModel provides seamless transition
- **Developer Experience**: Single class definition serves as both ORM model and Pydantic schema (DRY principle)
- **Constitutional Alignment**: Built-in validation eliminates manual checks, reducing code complexity

**Alternatives Rejected**:
- Raw SQLAlchemy: More verbose, requires separate Pydantic schemas for validation
- Peewee: Lightweight but lacks Pydantic integration, harder Phase II migration
- Raw sqlite3: No type safety, manual validation, high error risk (violates principle IX)

**Example Code**:
```python
from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)  # Username string in Phase I
    title: str = Field(min_length=1, max_length=200)

    # Phase I active fields
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Future-proof Phase V fields (nullable)
    description: Optional[str] = None  # Phase II+
    priority: Optional[str] = None  # Phase V (enum: high/medium/low)
    tags: Optional[str] = None  # Phase V (JSON-encoded array)
    due_date: Optional[datetime] = None  # Phase V
    recurrence_pattern: Optional[str] = None  # Phase V Advanced
```

**References**:
- SQLModel docs: https://sqlmodel.tiangolo.com/
- Constitutional Principle IX (Code Quality): Type hints mandatory

---

### 2. CLI Framework: Click vs Argparse

**Question**: Which CLI framework provides the best user experience and developer ergonomics for Phase I console app?

**Options Considered**:
1. **Click** (decorators, composability)
2. Argparse (stdlib, no dependencies)
3. Typer (Click + type hints)

**Decision**: ✅ **Click**

**Rationale**:
- **User Experience**: Automatic help generation, colored output support (better error messages - FR-013)
- **Developer Experience**: Decorator-based commands more readable than argparse boilerplate
- **Error Handling**: Built-in validation with clear error messages (SC-008: 100% human-readable errors)
- **Composability**: Subcommands pattern scales to Phase II if needed (though Phase II will use FastAPI)
- **Exit Codes**: Easy to handle with `sys.exit(0)` and `sys.exit(1)` (FR-019)

**Alternatives Rejected**:
- Argparse: Verbose boilerplate, manual help formatting, harder to maintain
- Typer: Excellent but adds dependency; Click sufficient for Phase I needs

**Example Code**:
```python
import click

@click.group()
def cli():
    """Todo CLI - Multi-user task management"""
    pass

@cli.command()
@click.option('--username', required=True, help='Your username')
@click.argument('title')
def add(username: str, title: str):
    """Add a new task"""
    if len(title) < 1 or len(title) > 200:
        click.echo("Error: Title must be 1-200 characters", err=True)
        sys.exit(1)

    # Add task logic...
    click.echo(f"✓ Task added with ID {task_id}")
    sys.exit(0)
```

**References**:
- Click docs: https://click.palletsprojects.com/
- FR-013 (Human-readable errors), FR-019 (Exit codes), SC-008 (100% human-readable)

---

### 3. Database Schema Auto-Creation Strategy

**Question**: How to automatically create database schema on first run while supporting future migrations to Phase II PostgreSQL?

**Options Considered**:
1. **SQLModel `create_all()`** (simple, handles schema creation)
2. Alembic migrations (production-grade, Phase II-ready)
3. Manual SQL scripts

**Decision**: ✅ **SQLModel `create_all()` for Phase I**

**Rationale**:
- **Simplicity**: One-line schema creation, no migration files for Phase I
- **Idempotency**: Safe to call multiple times (creates only if not exists)
- **Future-Proof**: Schema includes all Phase V fields from day 1 (no Phase I → Phase V migrations)
- **Phase II Migration Path**: Alembic will be introduced in Phase II for PostgreSQL schema management

**Implementation**:
```python
from sqlmodel import create_engine, SQLModel

def init_database():
    """Initialize database and create schema if needed."""
    engine = create_engine("sqlite:///todo.db")
    SQLModel.metadata.create_all(engine)  # Idempotent
    return engine
```

**Alternatives Rejected**:
- Alembic in Phase I: Over-engineering for local SQLite, adds complexity without benefit
- Manual SQL: Harder to maintain, violates DRY (schema defined twice)

**References**:
- FR-011 (Auto-create schema), FR-012 (Future-proof schema)

---

### 4. User Isolation Pattern: Query Filtering Strategy

**Question**: How to enforce `WHERE user_id = ?` on all queries without repetition?

**Options Considered**:
1. **Service Layer Pattern** (centralized CRUD methods with user_id parameter)
2. Repository Pattern (abstraction over data access)
3. Manual WHERE clauses in each query

**Decision**: ✅ **Service Layer Pattern**

**Rationale**:
- **Centralization**: All user_id filtering logic in `task_service.py`, single source of truth
- **Testability**: Service methods easily unit-testable with mock database
- **Constitutional Alignment**: Principle II (User Data Isolation) enforced in one place
- **Phase II Migration**: Service layer maps directly to FastAPI dependency injection

**Implementation**:
```python
# services/task_service.py
from sqlmodel import Session, select
from models.task import Task

class TaskService:
    def __init__(self, session: Session):
        self.session = session

    def get_all_tasks(self, user_id: str) -> list[Task]:
        """Get all tasks for a user (enforces user isolation)."""
        statement = select(Task).where(Task.user_id == user_id)
        return self.session.exec(statement).all()

    def add_task(self, user_id: str, title: str) -> Task:
        """Add a task for a user."""
        task = Task(user_id=user_id, title=title)
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    # ... other CRUD methods with user_id parameter
```

**Alternatives Rejected**:
- Repository Pattern: Over-abstraction for Phase I, adds boilerplate without value
- Manual WHERE clauses: Error-prone, risk of forgetting user_id filter (violates principle II)

**References**:
- FR-010 (User data isolation), Principle II (Constitutional)

---

### 5. Error Handling: Human-Readable Messages Strategy

**Question**: How to ensure 100% human-readable error messages (SC-008) without exposing stack traces?

**Options Considered**:
1. **Try/Except with Custom Error Messages** (explicit)
2. Centralized error handler middleware
3. Let exceptions propagate (default Python behavior)

**Decision**: ✅ **Try/Except with Custom Error Messages**

**Rationale**:
- **User Experience**: Clear, actionable error messages (e.g., "Task 999 not found" vs "NoResultFound exception")
- **Security**: No stack trace leaks (prevents exposing internal implementation details)
- **Constitutional Alignment**: FR-013 (user-friendly errors), SC-008 (100% human-readable)
- **Exit Codes**: Easy to control exit codes (0 success, 1 error) per FR-019

**Implementation**:
```python
# cli/commands.py
import click
import sys

@cli.command()
@click.option('--username', required=True)
@click.argument('task_id', type=int)
def delete(username: str, task_id: int):
    """Delete a task by ID."""
    try:
        task_service = get_task_service()
        task = task_service.get_task(user_id=username, task_id=task_id)

        if not task:
            click.echo(f"Error: Task {task_id} not found", err=True)
            sys.exit(1)

        task_service.delete_task(task)
        click.echo(f"✓ Task {task_id} deleted")
        sys.exit(0)

    except Exception as e:
        # Catch unexpected errors, convert to user-friendly message
        click.echo(f"Error: Unable to delete task. {str(e)}", err=True)
        sys.exit(1)
```

**Alternatives Rejected**:
- Centralized error handler: Over-engineering for Phase I CLI (useful in Phase II web API)
- Propagate exceptions: Violates SC-008 (100% human-readable errors)

**References**:
- FR-013 (User-friendly errors), FR-019 (Exit codes), SC-008 (100% human-readable)

---

### 6. Testing Strategy: Achieving 80% Coverage

**Question**: How to structure tests to achieve ≥80% coverage (SC-101) with minimum duplication?

**Options Considered**:
1. **Three-Layer Testing** (Unit → Integration → Contract)
2. Two-Layer (Unit + Integration only)
3. End-to-End only

**Decision**: ✅ **Three-Layer Testing**

**Rationale**:
- **Unit Tests**: Fast feedback, test business logic in isolation (models, validators, service layer)
- **Integration Tests**: Test user isolation (SC-105), persistence (SC-007), database interactions
- **Contract Tests**: Verify CLI commands match `contracts/` specifications
- **Coverage**: Three layers ensure comprehensive coverage without redundant tests

**Test Organization**:
```text
tests/
├── contract/
│   └── test_cli_commands.py  # Verify CLI matches contracts/ (help text, arg names, exit codes)
├── integration/
│   ├── test_user_isolation.py  # SC-105: User A cannot access User B's tasks
│   └── test_persistence.py     # SC-007: Data persists across restarts
└── unit/
    ├── test_task_model.py      # Pydantic validation (title 1-200 chars, etc.)
    ├── test_task_service.py    # CRUD operations, edge cases (empty title, invalid ID)
    └── test_validators.py      # Username non-empty, title length validation
```

**Coverage Exclusions** (per constitutional principle X):
- Configuration files (no application logic)
- `if __name__ == "__main__":` blocks (entry points)

**References**:
- SC-101 (pytest --cov-fail-under=80), Constitutional Principle X (Testing Requirements)

---

### 7. Performance Optimization: Meeting <500ms Operation Target

**Question**: How to ensure all operations complete in <500ms with 10,000 tasks (SC-010)?

**Options Considered**:
1. **Database Indexes on user_id** (query optimization)
2. In-memory caching
3. No optimization (trust SQLite)

**Decision**: ✅ **Database Indexes on user_id**

**Rationale**:
- **Query Performance**: Index on `user_id` column enables fast filtering (constitutional principle XVIII)
- **Simplicity**: Single-line change in SQLModel (`Field(index=True)`)
- **Stateless**: No in-memory state required (aligns with principle IV)
- **Scalability**: Handles 10,000 tasks per SC-010 without degradation

**Implementation**:
```python
class Task(SQLModel, table=True):
    user_id: str = Field(index=True)  # Index for WHERE user_id = ? queries
    # ... other fields
```

**Testing**:
```python
# Verify performance with 10,000 tasks
def test_performance_at_scale():
    # Add 10,000 tasks for user 'alice'
    for i in range(10000):
        task_service.add_task(user_id='alice', title=f'Task {i}')

    # Measure view operation
    start = time.time()
    tasks = task_service.get_all_tasks(user_id='alice')
    elapsed = time.time() - start

    assert elapsed < 0.5  # SC-010: <500ms
    assert len(tasks) == 10000
```

**Alternatives Rejected**:
- In-memory caching: Violates principle IV (stateless architecture)
- No optimization: Risk of missing SC-010 performance target

**References**:
- SC-010 (All operations <500ms with 10,000 tasks), Principle IV (Stateless)

---

## Technology Stack Summary

| Component | Technology | Version | Rationale |
|-----------|-----------|---------|-----------|
| **Language** | Python | 3.13+ | Constitutional requirement, type hints, pattern matching |
| **ORM** | SQLModel | Latest | Type safety, Pydantic validation, Phase II migration path |
| **Database** | SQLite | 3.x (bundled) | Local file storage, zero config, cross-platform |
| **CLI Framework** | Click | 8.x | Decorator-based, colored output, automatic help generation |
| **Testing** | pytest | 8.x | Fixture support, parametrized tests, coverage integration |
| **Coverage** | pytest-cov | 5.x | Integrated coverage reporting, ≥80% enforcement |
| **Type Checking** | mypy | 1.x | Static type checking with --strict mode (principle IX) |
| **Formatting** | black | 24.x | Consistent code formatting, zero-config (principle IX) |
| **Linting** | flake8 | 7.x | PEP 8 compliance, complexity checks (principle IX) |

---

## Best Practices Applied

### 1. Future-Proof Schema Design
- ✅ All Phase V fields (description, priority, tags, due_date, recurrence_pattern) included as nullable from Phase I
- ✅ Prevents schema migrations in Phase II-V (constitutional principle I)
- ✅ Single source of truth for Task entity across all phases

### 2. User Data Isolation Enforcement
- ✅ Service layer pattern centralizes `WHERE user_id = ?` filtering
- ✅ All CRUD methods require `user_id` parameter (impossible to forget)
- ✅ Integration tests verify user A cannot access user B's data (SC-105)

### 3. Stateless Architecture
- ✅ No in-memory session state or caching
- ✅ All state persisted to SQLite database
- ✅ Database indexes for performance (not in-memory caching)

### 4. Type Safety & Validation
- ✅ SQLModel provides runtime + compile-time type checking
- ✅ Pydantic validation rules in model definition (DRY)
- ✅ mypy --strict enforces type hints (SC-102)

### 5. Human-Readable Error Messages
- ✅ Try/except blocks with custom error messages
- ✅ No stack trace exposure to end users
- ✅ Actionable error messages (e.g., "Title must be 1-200 characters")

### 6. Three-Layer Testing Strategy
- ✅ Unit tests for business logic (fast feedback)
- ✅ Integration tests for user isolation and persistence
- ✅ Contract tests for CLI interface verification

---

## Open Questions for Phase 1 Design

1. **CLI Command Syntax**: Should commands be subcommands (`todo add`) or flags (`todo --add`)? → **Resolved in contracts/**
2. **Task Display Format**: Table view vs list view vs detailed view? → **Resolved in quickstart.md**
3. **Timestamp Display**: ISO 8601 vs human-readable ("2 hours ago")? → **Resolved in contracts/view.md**

These questions will be answered during Phase 1 design (`contracts/` and `quickstart.md` generation).

---

## Constitutional Alignment Verification

| Principle | Research Decision | Alignment |
|-----------|------------------|-----------|
| **I. Spec-Driven** | Future-proof schema in Phase I | ✅ Prevents manual schema changes later |
| **II. User Isolation** | Service layer with user_id filtering | ✅ Centralized enforcement |
| **IV. Stateless** | Database-backed state, indexes not caching | ✅ No in-memory state |
| **IX. Code Quality** | SQLModel (type hints), mypy, black, flake8 | ✅ All quality tools integrated |
| **X. Testing** | Three-layer testing (unit/integration/contract) | ✅ ≥80% coverage achievable |
| **XII. Security** | Parameterized queries (SQLModel ORM) | ✅ SQL injection prevention |
| **XVI. Error Handling** | Try/except with custom messages, exit codes | ✅ 100% human-readable errors |

**Result**: ✅ All research decisions align with applicable constitutional principles

---

## Next Steps

1. **Phase 1: Data Model** - Generate `data-model.md` with complete Task entity schema
2. **Phase 1: Contracts** - Generate `contracts/` with CLI command interface definitions
3. **Phase 1: Quickstart** - Generate `quickstart.md` with setup and usage guide
4. **Phase 1: Agent Context Update** - Run `.specify/scripts/bash/update-agent-context.sh claude`
5. **Constitution Re-Check** - Validate Phase 1 design against all applicable principles

---

**Research Complete** - Ready to proceed to Phase 1 Design
