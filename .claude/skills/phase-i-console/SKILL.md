---
name: phase-i-console
description: Provide Phase I console app technical patterns including SQLite, Click CLI, SQLModel, and user isolation. Use when implementing Phase I console features or working with the Phase I codebase.
allowed-tools: Read, Write, Bash, Grep, Edit
---

# Phase I Console Patterns Skill

Technical guidance for Python console app with SQLite (Phase I of Evolution).

## Phase I Technology Stack

Per Constitution and spec (`specs/002-phase-i-console-app/spec.md`):

- **Python**: 3.13+ (constitutional requirement)
- **ORM**: SQLModel (SQL Alchemy-based with Pydantic validation)
- **Database**: SQLite local file (`todo.db` in current working directory)
- **CLI Framework**: Click or argparse
- **Package Manager**: UV with `pyproject.toml`

## Project Structure

```
todo-evolution/
├── backend/  (or app/ or todo_app/)
│   ├── __init__.py
│   ├── main.py           # CLI entry point
│   ├── models.py         # SQLModel models
│   ├── db.py             # Database engine and session
│   ├── cli.py            # Click command definitions
│   └── services/
│       └── task_service.py  # Business logic
├── tests/
│   ├── test_models.py
│   ├── test_task_service.py
│   └── conftest.py       # Pytest fixtures
├── pyproject.toml        # UV dependencies
├── README.md
└── todo.db               # SQLite database (created at runtime)
```

## Database Setup Pattern

### 1. Define Engine and Session (db.py)

```python
"""Database configuration and session management."""
from sqlmodel import create_engine, Session, SQLModel
from pathlib import Path

# Database file in current working directory
DATABASE_PATH = Path.cwd() / "todo.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Create engine
engine = create_engine(DATABASE_URL, echo=False)

def init_db() -> None:
    """Initialize database schema."""
    SQLModel.metadata.create_all(engine)

def get_session() -> Session:
    """Get database session."""
    return Session(engine)
```

### 2. Define Models (models.py)

```python
"""Database models using SQLModel."""
from sqlmodel import Field, SQLModel, Index
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    """Task model with user isolation."""

    __tablename__ = "tasks"

    # Required fields (constitutional)
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)  # MANDATORY for user isolation
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Task-specific fields
    title: str = Field(max_length=200)
    completed: bool = Field(default=False)

    # Indexes for performance
    __table_args__ = (
        Index('ix_tasks_user_id_completed', 'user_id', 'completed'),
    )
```

### 3. Initialize on First Run (main.py)

```python
"""CLI entry point."""
import click
from backend.db import init_db, get_session
from backend import cli as cli_commands

@click.group()
@click.pass_context
def cli(ctx):
    """Todo CLI application."""
    # Initialize database on first run
    init_db()
    ctx.ensure_object(dict)

if __name__ == "__main__":
    cli()
```

## Click CLI Patterns

### Command Structure

```python
"""CLI commands for task management."""
import click
from sqlmodel import select, Session
from backend.models import Task
from backend.db import get_session

@click.command()
@click.option('--user', '-u', required=True, help='Username')
@click.argument('title')
def add(user: str, title: str) -> None:
    """Add a new task.

    Usage: python -m backend.main add --user alice "Buy groceries"
    """
    try:
        with get_session() as session:
            task = Task(user_id=user, title=title)
            session.add(task)
            session.commit()
            session.refresh(task)

            click.echo(click.style(
                f"✓ Task {task.id} added: {task.title}",
                fg='green'
            ))

    except Exception as e:
        click.echo(click.style(f"✗ Error: {e}", fg='red'), err=True)
        raise click.Abort()


@click.command()
@click.option('--user', '-u', required=True, help='Username')
def view(user: str) -> None:
    """View all tasks for the user.

    Usage: python -m backend.main view --user alice
    """
    try:
        with get_session() as session:
            # CRITICAL: Filter by user_id (user isolation)
            tasks = session.exec(
                select(Task).where(Task.user_id == user).order_by(Task.id)
            ).all()

            if not tasks:
                click.echo("No tasks found.")
                return

            click.echo(f"\nTasks for {user}:")
            click.echo("-" * 60)

            for task in tasks:
                status = "✓" if task.completed else " "
                click.echo(
                    f"[{status}] {task.id}: {task.title}"
                )

            click.echo("-" * 60)
            click.echo(f"Total: {len(tasks)} tasks")

    except Exception as e:
        click.echo(click.style(f"✗ Error: {e}", fg='red'), err=True)
        raise click.Abort()


@click.command()
@click.option('--user', '-u', required=True, help='Username')
@click.argument('task_id', type=int)
def complete(user: str, task_id: int) -> None:
    """Mark a task as complete.

    Usage: python -m backend.main complete --user alice 1
    """
    try:
        with get_session() as session:
            # CRITICAL: Filter by user_id (user isolation)
            task = session.exec(
                select(Task).where(
                    Task.id == task_id,
                    Task.user_id == user
                )
            ).first()

            if not task:
                click.echo(
                    click.style(f"✗ Task {task_id} not found", fg='red'),
                    err=True
                )
                raise click.Abort()

            # Toggle completion status
            task.completed = not task.completed
            task.updated_at = datetime.utcnow()
            session.add(task)
            session.commit()

            status = "complete" if task.completed else "incomplete"
            click.echo(click.style(
                f"✓ Task {task_id} marked {status}",
                fg='green'
            ))

    except Exception as e:
        click.echo(click.style(f"✗ Error: {e}", fg='red'), err=True)
        raise click.Abort()


@click.command()
@click.option('--user', '-u', required=True, help='Username')
@click.argument('task_id', type=int)
@click.argument('new_title')
def update(user: str, task_id: int, new_title: str) -> None:
    """Update task title.

    Usage: python -m backend.main update --user alice 1 "Buy milk"
    """
    try:
        # Validate title
        if not new_title or len(new_title.strip()) == 0:
            raise ValueError("Title cannot be empty")
        if len(new_title) > 200:
            raise ValueError("Title must be 1-200 characters")

        with get_session() as session:
            # CRITICAL: Filter by user_id (user isolation)
            task = session.exec(
                select(Task).where(
                    Task.id == task_id,
                    Task.user_id == user
                )
            ).first()

            if not task:
                click.echo(
                    click.style(f"✗ Task {task_id} not found", fg='red'),
                    err=True
                )
                raise click.Abort()

            task.title = new_title.strip()
            task.updated_at = datetime.utcnow()
            session.add(task)
            session.commit()

            click.echo(click.style(
                f"✓ Task {task_id} updated: {task.title}",
                fg='green'
            ))

    except ValueError as e:
        click.echo(click.style(f"✗ Validation error: {e}", fg='red'), err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(click.style(f"✗ Error: {e}", fg='red'), err=True)
        raise click.Abort()


@click.command()
@click.option('--user', '-u', required=True, help='Username')
@click.argument('task_id', type=int)
def delete(user: str, task_id: int) -> None:
    """Delete a task.

    Usage: python -m backend.main delete --user alice 1
    """
    try:
        with get_session() as session:
            # CRITICAL: Filter by user_id (user isolation)
            task = session.exec(
                select(Task).where(
                    Task.id == task_id,
                    Task.user_id == user
                )
            ).first()

            if not task:
                click.echo(
                    click.style(f"✗ Task {task_id} not found", fg='red'),
                    err=True
                )
                raise click.Abort()

            session.delete(task)
            session.commit()

            click.echo(click.style(
                f"✓ Task {task_id} deleted",
                fg='green'
            ))

    except Exception as e:
        click.echo(click.style(f"✗ Error: {e}", fg='red'), err=True)
        raise click.Abort()


# Register commands with CLI group
def register_commands(cli_group):
    """Register all commands with the CLI group."""
    cli_group.add_command(add)
    cli_group.add_command(view)
    cli_group.add_command(complete)
    cli_group.add_command(update)
    cli_group.add_command(delete)
```

## User Isolation Pattern (CRITICAL)

**Every query MUST filter by `user_id`** to prevent cross-user data access.

```python
# ✅ GOOD - User isolation enforced
tasks = session.exec(
    select(Task).where(Task.user_id == user_id)
).all()

task = session.exec(
    select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id  # CRITICAL
    )
).first()

# ❌ BAD - Missing user_id filter (security violation)
tasks = session.exec(select(Task)).all()  # Cross-user leak!

task = session.exec(
    select(Task).where(Task.id == task_id)  # Missing user_id!
).first()
```

## CLI Error Handling Pattern

```python
@click.command()
@click.option('--user', '-u', required=True)
def command(user: str):
    """Command with proper error handling."""
    try:
        # Business logic here
        with get_session() as session:
            # ... database operations ...
            pass

        # Success output
        click.echo(click.style("✓ Success message", fg='green'))

    except ValueError as e:
        # Validation errors (user input issues)
        click.echo(click.style(f"✗ Validation error: {e}", fg='red'), err=True)
        raise click.Abort()

    except Exception as e:
        # Unexpected errors
        click.echo(click.style(f"✗ Error: {e}", fg='red'), err=True)
        raise click.Abort()
```

## Dependency Management with UV

### pyproject.toml

```toml
[project]
name = "todo-evolution-phase-i"
version = "0.1.0"
description = "Phase I: Console Todo App"
requires-python = ">=3.13"
dependencies = [
    "sqlmodel>=0.0.14",
    "click>=8.1.7",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "mypy>=1.7.0",
    "black>=23.12.0",
    "flake8>=6.1.0",
]

[project.scripts]
todo = "backend.main:cli"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"

[tool.coverage.run]
source = ["backend"]
omit = ["*/tests/*", "*/test_*.py"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
]

[tool.mypy]
python_version = "3.13"
strict = true
warn_return_any = true
warn_unused_configs = true

[tool.black]
line-length = 100
target-version = ['py313']
```

### Installation Commands

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows

# Install dependencies
uv pip install -e .

# Install dev dependencies
uv pip install -e .[dev]

# Run CLI
python -m backend.main --help

# Or use script entry point
todo --help
```

## Running the Application

```bash
# Add task
python -m backend.main add --user alice "Buy groceries"
# or
todo add --user alice "Buy groceries"

# View tasks
python -m backend.main view --user alice

# Complete task
python -m backend.main complete --user alice 1

# Update task
python -m backend.main update --user alice 1 "Buy milk"

# Delete task
python -m backend.main delete --user alice 1
```

## Testing Patterns for Phase I

See `sqlite-testing` skill for comprehensive testing patterns.

### Quick Example

```python
# tests/conftest.py
import pytest
from sqlmodel import create_engine, SQLModel, Session

@pytest.fixture
def test_db():
    """Create in-memory test database."""
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    SQLModel.metadata.drop_all(engine)


# tests/test_user_isolation.py
def test_user_cannot_access_other_user_tasks(test_db):
    """Verify user isolation."""
    # Alice creates task
    alice_task = Task(user_id="alice", title="Alice's task")
    test_db.add(alice_task)
    test_db.commit()

    # Bob's query should not see Alice's task
    bob_tasks = test_db.exec(
        select(Task).where(Task.user_id == "bob")
    ).all()

    assert len(bob_tasks) == 0
    assert alice_task not in bob_tasks
```

## Common Pitfalls to Avoid

### ❌ Missing user_id Filter
```python
# This leaks data across users!
tasks = session.exec(select(Task)).all()
```

### ❌ Hardcoded Database Path
```python
# Don't hardcode paths
engine = create_engine("sqlite:///C:/Users/alice/todo.db")

# Use current working directory
DATABASE_PATH = Path.cwd() / "todo.db"
```

### ❌ Not Handling Errors
```python
# No try/except - crashes ungracefully
@click.command()
def command():
    task = get_task(999)  # May not exist!
    click.echo(task.title)  # AttributeError if None
```

### ❌ Not Using Context Manager for Session
```python
# Manual session management (error-prone)
session = Session(engine)
task = session.get(Task, 1)
session.close()  # May not execute if exception

# Use context manager
with get_session() as session:
    task = session.get(Task, 1)
# Session auto-closes
```

## Performance Considerations

### Index Critical Columns
```python
class Task(SQLModel, table=True):
    # ...
    __table_args__ = (
        Index('ix_tasks_user_id_completed', 'user_id', 'completed'),
        Index('ix_tasks_user_id_created_at', 'user_id', 'created_at'),
    )
```

### Batch Operations
```python
# ✅ GOOD - Single commit
with get_session() as session:
    for title in task_titles:
        task = Task(user_id=user_id, title=title)
        session.add(task)
    session.commit()  # One commit

# ❌ BAD - Multiple commits
for title in task_titles:
    with get_session() as session:
        task = Task(user_id=user_id, title=title)
        session.add(task)
        session.commit()  # Commit per task (slow)
```

## Constitutional Compliance

This skill implements:
- ✅ **Principle I**: Spec-driven (follows spec.md)
- ✅ **Principle II**: User isolation (all queries filter by user_id)
- ✅ **Principle III**: Stateless (SQLite file persistence)
- ✅ **Principle VI**: Database standards (SQLModel, timestamps, indexes)
- ✅ **Principle IX**: Code quality (type hints, docstrings, PEP 8)

## MCP Integration (Context7)

When implementing new features, fetch SQLModel documentation:

```
Implementing relationships?
  → mcp__context7__get-library-docs("/tiangolo/sqlmodel", topic="relationships")

Need advanced queries?
  → mcp__context7__get-library-docs("/tiangolo/sqlmodel", topic="queries")
```

## Next Steps (Phase II Migration)

When transitioning to Phase II:
- Replace SQLite with Neon PostgreSQL
- Replace Click CLI with FastAPI REST endpoints
- Add Better Auth for user management
- Keep SQLModel ORM (seamless transition)
- Reuse Task model with minor adjustments
