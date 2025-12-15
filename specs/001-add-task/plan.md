# Implementation Plan: Add Task Feature

**Branch**: `001-add-task` | **Date**: 2025-12-12 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/001-add-task/spec.md`

## Summary

This plan implements the **Add Task** feature for Phase I (console application). Users can create tasks with titles via CLI command `todo add --user <user_id> <title>`. The feature includes input validation, user data isolation, and persistence to SQLite database. This is the foundational CRUD operation that establishes patterns for all future task operations.

**Technical Approach**: Python 3.13+ console application using Click for CLI framework, SQLModel for ORM, and SQLite for local persistence. Architecture prioritizes simplicity (Phase I constraints) while establishing patterns that scale to Phase II web application (FastAPI + PostgreSQL migration path).

## Technical Context

**Language/Version**: Python 3.13+ (constitutional requirement per Principle III)
**Primary Dependencies**: Click (CLI framework), SQLModel 0.0.14+ (ORM with Pydantic validation), sqlite3 (bundled with Python)
**Storage**: SQLite database file (`todo.db` in current working directory)
**Testing**: pytest 8.0+ with pytest-cov for coverage (target: ≥80% per Principle X)
**Target Platform**: Console (Linux, macOS, Windows with WSL2)
**Project Type**: Single-project console application (Phase I - no web components)
**Performance Goals**: p95 latency <100ms for task creation (Principle XVIII Phase I target)
**Constraints**: Single-user concurrent access per user_id, no distributed locking, <5MB memory footprint
**Scale/Scope**: Phase I target: 1000 tasks per user, 10 concurrent users (simulated via tests)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Critical Principles (NON-NEGOTIABLE)

- ✅ **Principle I (Spec-Driven Development)**: spec.md exists and complete before this plan
- ✅ **Principle II (User Data Isolation)**: All queries MUST filter by user_id, CLI requires --user flag
- ✅ **Principle III (Python 3.13+)**: Using Python 3.13+ per constitutional requirement
- ✅ **Principle VI (Database Standards)**: Task model includes id, user_id, created_at, updated_at
- ✅ **Principle IX (Code Quality)**: Type hints, docstrings, mypy --strict compliance
- ✅ **Principle X (Testing)**: pytest with ≥80% coverage, TDD approach
- ✅ **Principle XII (Security)**: User isolation, input validation, no secrets in code
- ✅ **Principle XVIII (Performance)**: p95 latency <100ms target for Phase I

### Phase I Applicability

**Not Applicable for Phase I Console**:
- Principle VII (API Design) - No REST API in Phase I
- Principle VIII (MCP Tool Design) - Deferred to Phase III
- Principle XIV (Authentication & Authorization) - No password auth in Phase I (--user flag is trusted)
- Principle XV (API Rate Limiting) - No HTTP API in Phase I
- Principle XVII (Frontend Accessibility) - No UI in Phase I
- Principle XIX-XXV (Cloud-Native, K8s, Dapr) - Deferred to Phase IV-V

**GATE STATUS**: ✅ **PASS** - All applicable principles satisfied, no violations to justify

## Project Structure

### Documentation (this feature)

```text
specs/001-add-task/
├── spec.md              # Feature requirements (completed)
├── plan.md              # This file (architectural design)
├── research.md          # Technology decisions and rationale
├── data-model.md        # Task entity schema
├── contracts/           # CLI command contracts
│   └── add-task.md      # CLI command specification
├── quickstart.md        # Usage examples and integration guide
└── tasks.md             # Implementation tasks (/sp.tasks - NOT created yet)
```

### Source Code (repository root)

**Phase I uses Option 1: Single Project (Console Application)**

```text
src/
├── models/
│   ├── __init__.py
│   └── task.py          # Task SQLModel with validation
├── services/
│   ├── __init__.py
│   ├── db.py            # Database connection, session management
│   └── task_service.py  # Task CRUD operations (user-scoped)
├── cli/
│   ├── __init__.py
│   ├── main.py          # Click app entry point
│   └── commands/
│       ├── __init__.py
│       └── add.py       # `todo add` command implementation
└── lib/
    ├── __init__.py
    └── validators.py    # Shared validation logic

tests/
├── unit/
│   ├── test_task_model.py        # Task validation tests
│   ├── test_task_service.py      # Service logic tests
│   └── test_validators.py        # Validator unit tests
├── integration/
│   └── test_add_task_integration.py  # Full workflow tests
└── conftest.py          # pytest fixtures (test DB)

pyproject.toml           # UV dependency management + CLI entry point
todo.db                  # SQLite database (created on first run, gitignored)
.env.example             # Environment template (no secrets)
.gitignore               # Ignore .env, todo.db, __pycache__, .venv
```

**CLI Packaging Configuration** (`pyproject.toml`):

```toml
[project.scripts]
todo = "src.cli.main:cli"  # Entry point: makes `todo` command available after `uv sync`
```

After running `uv sync`, the `todo` command is installed in the virtual environment and can be invoked from anywhere:
```bash
$ todo --help
$ todo add --user alice "Buy groceries"
```

**Testing**: Use Click's `CliRunner` (not subprocess) for integration tests:
```python
from click.testing import CliRunner
from src.cli.main import cli

runner = CliRunner()
result = runner.invoke(cli, ['add', '--user', 'alice', 'Buy milk'])
assert result.exit_code == 0
```

**Structure Decision**: Single project structure is appropriate for Phase I console application. All code resides in `src/` with clear separation: models (data), services (business logic), cli (user interface), lib (utilities). Tests mirror source structure. This layout scales naturally to Phase II by adding `backend/` and `frontend/` directories while preserving existing src/ as CLI client.

---

## Component Dependency Graph

**Purpose**: Explicit dependency ordering for implementation. Components MUST be built in dependency order to avoid import errors and enable incremental testing.

### Build Order (Sequential Dependencies)

```
Layer 0: Database Infrastructure (FIRST)
├── src/services/db.py (connection, session, init_db)
└── Dependencies: None (uses stdlib + sqlmodel)

Layer 1: Data Models (DEPENDS ON: Layer 0)
├── src/models/task.py (Task SQLModel class)
└── Dependencies: db.py for engine/session

Layer 2a: Validators (INDEPENDENT - Can run PARALLEL with Layer 2b)
├── src/lib/validators.py (validate_title, validate_user_id)
└── Dependencies: None (pure validation logic, no Task imports)

Layer 2b: Services (DEPENDS ON: Layer 0, Layer 1)
├── src/services/task_service.py (TaskService.create_task)
└── Dependencies: db.py (session), models/task.py (Task class)

Layer 3: CLI Commands (DEPENDS ON: Layer 2a, Layer 2b)
├── src/cli/commands/add.py (Click command)
└── Dependencies: validators.py, task_service.py

Layer 4: CLI Entry Point (DEPENDS ON: Layer 3)
├── src/cli/main.py (Click app, calls init_db on startup)
└── Dependencies: commands/add.py, db.py (init_db)

Layer 5: Tests (DEPENDS ON: All above)
├── tests/conftest.py (MUST be created BEFORE test files)
├── tests/unit/*.py (depends on models, validators, services)
└── tests/integration/*.py (depends on full stack)
```

### Critical Dependencies

**Database Initialization** (`init_db()` call):
- **Where**: `src/cli/main.py` startup (before any commands execute)
- **Why**: Tables MUST exist before TaskService.create_task runs
- **Implementation**:
  ```python
  # src/cli/main.py
  import click
  from src.services.db import init_db
  from src.cli.commands.add import add  # Import command

  @click.group()
  @click.version_option(version="0.1.0")
  def cli():
      """Todo CLI application."""
      init_db()  # Called once per CLI invocation

  # Register commands
  cli.add_command(add)  # Makes `todo add` available

  if __name__ == "__main__":
      cli()
  ```

**Command Registration**:
- Import command from `src.cli.commands.add`
- Register with `cli.add_command(add)` after `@click.group()` decorator
- Click auto-discovers command name from function name (`add` → `todo add`)

**Test Fixtures** (`conftest.py`):
- **Status**: MUST be created BEFORE any test files are written
- **Why**: Test files import fixtures via pytest magic; missing conftest.py causes import errors
- **Location**: `tests/conftest.py`
- **Provides**: `test_db` session, `test_user` data, in-memory SQLite (`:memory:`)

### Independence Matrix (Parallel Work Candidates)

| Component | Can Build in Parallel With | Cannot Build Until |
|-----------|----------------------------|-------------------|
| db.py | Nothing (foundation) | - |
| task.py | Nothing | db.py complete |
| validators.py | task.py, task_service.py | - (independent) |
| task_service.py | validators.py | db.py, task.py complete |
| commands/add.py | Nothing | validators.py, task_service.py complete |
| Unit tests | Integration tests, validators.py | Component being tested exists |
| Integration tests | Unit tests | Full stack complete |

---

## Complexity Tracking

**No violations detected** - Constitution Check passed without justifications needed. Phase I design aligns with all applicable principles.

---

## Technology Stack

### Programming Language: Python 3.13+

**Options Considered**:
1. Python 3.11 (widely adopted, stable)
2. Python 3.12 (performance improvements)
3. **Python 3.13+ (CHOSEN)** - Constitutional requirement

**Decision Rationale**:
- **Constitutional Mandate**: Principle III explicitly requires Python 3.13+
- Performance improvements: 10-15% faster than 3.11 (PEP 709 comprehension inlining)
- Better error messages and type system improvements
- Prepares codebase for future Python features

**Trade-offs**:
- ✅ Latest features, best performance, constitutional compliance
- ✅ Free threading improvements (GIL optimizations for future async work)
- ❌ Smaller ecosystem (some libraries may not support 3.13 yet) - **Mitigated**: Core dependencies (Click, SQLModel, pytest) all support 3.13
- ❌ Installation burden (users must upgrade) - **Acceptable**: Development team controls environment

**ADR**: Not required (constitutional mandate, no alternatives evaluated)

---

### CLI Framework: Click 8.1+

**Options Considered**:
1. **Click 8.1+ (CHOSEN)** - Decorator-based, rich help, composable
2. argparse (built-in, no dependencies) - Standard library, widely known
3. Typer - Type-hint based, built on Click, modern

**Decision Rationale**:
- **User Experience**: Click provides rich help text, argument validation, and user-friendly error messages (aligns with spec FR-009)
- **Decorator Syntax**: Clean, composable commands (`@click.command()`)
- **Validation**: Built-in type coercion and validation (integers, choices, required options)
- **Error Handling**: Automatic exit codes (aligns with spec FR-010: 0=success, 1=error, 2=missing options)
- **Ecosystem**: Widely adopted in Python CLI tools (pytest, Flask, Black all use Click)

**Trade-offs**:
- ✅ Excellent UX, automatic help generation, strong validation
- ✅ Exit code management (0, 1, 2) built-in
- ✅ Extensible for future commands (list, complete, delete)
- ❌ External dependency vs. argparse (built-in) - **Acceptable**: Click is lightweight (<50KB), stable, well-maintained
- ❌ Slightly steeper learning curve than argparse - **Mitigated**: Well-documented, team expertise

**Why Not Typer**: Typer is excellent but adds minimal value over Click for Phase I. Type hints are already enforced via mypy; Click's decorator syntax is clearer for simple commands.

**ADR**: Not required (tactical library choice, limited cross-cutting impact)

---

### ORM: SQLModel 0.0.14+

**Options Considered**:
1. **SQLModel 0.0.14+ (CHOSEN)** - Pydantic + SQLAlchemy fusion, type-safe
2. SQLAlchemy 2.0 (mature, powerful) - Industry standard ORM
3. Peewee (lightweight, simple) - Minimal ORM for small projects

**Decision Rationale**:
- **Constitutional Requirement**: Principle VI mandates SQLModel
- **Type Safety**: Pydantic integration enforces validation at model level (aligns with spec FR-002: title 1-200 chars)
- **Dual Mode**: Same model for database (SQLAlchemy) and validation (Pydantic)
- **Modern Syntax**: Type hints drive schema (Python 3.13+ compatible)
- **Migration Path**: Scales naturally to FastAPI (Phase II) which also uses Pydantic

**Trade-offs**:
- ✅ Type-safe, validates data at model layer, constitutional compliance
- ✅ Single source of truth (model defines both DB schema and validation rules)
- ✅ Phase II compatibility (FastAPI + SQLModel is canonical stack)
- ❌ Less mature than SQLAlchemy (v0.0.14 vs v2.0) - **Acceptable**: Built on SQLAlchemy, proven foundation
- ❌ Smaller community - **Mitigated**: Created by FastAPI author, active development

**Why Not Raw SQLAlchemy**: SQLModel provides Pydantic validation layer "for free" (reduces boilerplate for title length validation). Constitutional requirement seals decision.

**ADR**: Not required (constitutional mandate per Principle VI)

---

### Database: SQLite 3 (bundled with Python)

**Options Considered**:
1. **SQLite 3 (CHOSEN)** - File-based, zero-config, bundled
2. PostgreSQL (Neon DB) - Production-grade, constitutional target for Phase II
3. MongoDB - NoSQL, flexible schema

**Decision Rationale**:
- **Phase I Simplicity**: Console app with local file persistence (spec scope: single machine, no remote access)
- **Zero Configuration**: No separate database server, no connection strings, no network
- **Bundled**: Ships with Python 3.13 (sqlite3 module), no installation required
- **Development Velocity**: Immediate persistence testing without infrastructure setup
- **Migration Path**: SQLModel abstracts database (Phase II migration to PostgreSQL is straightforward via Alembic)

**Trade-offs**:
- ✅ Zero setup, bundled, perfect for Phase I local console app
- ✅ ACID guarantees (spec SC-003: 100% persistence across restarts)
- ✅ WAL mode supports concurrent reads (spec edge case: concurrent task creation)
- ✅ Migration path to PostgreSQL is well-documented (SQLModel + Alembic)
- ❌ Single-file limits concurrency (write locks) - **Acceptable**: Phase I has no multi-user concurrent writes
- ❌ No remote access (can't share database across machines) - **Expected**: Phase I scope is local console
- ❌ Limited to ~1 TB (file size limit) - **Non-issue**: 1000 tasks/user = <1MB

**Why Not PostgreSQL in Phase I**: Over-engineering. Console app doesn't need network database. SQLite meets all Phase I requirements. Phase II spec will explicitly call for PostgreSQL when web app demands it.

**ADR**: **REQUIRED** - This is architecturally significant:
- **Impact**: Storage layer affects data durability, concurrency, Phase II migration
- **Alternatives**: Multiple viable options (PostgreSQL, MongoDB)
- **Scope**: Cross-cutting (affects models, services, testing strategy)

**ADR Created**: `history/adr/001-sqlite-phase-i-console.md`

---

### Testing Framework: pytest 8.0+ with pytest-cov

**Options Considered**:
1. **pytest 8.0+ (CHOSEN)** - De facto standard, fixture-based, extensible
2. unittest (built-in) - Standard library, OOP-style tests
3. nose2 - unittest extension, less popular

**Decision Rationale**:
- **Constitutional Requirement**: Principle X specifies pytest for Python testing
- **Fixtures**: Database session management for tests (conftest.py)
- **Coverage**: pytest-cov integration measures coverage (target: ≥80% per Principle X)
- **Parametrization**: Test edge cases efficiently (1 char, 200 chars, 201 chars titles)
- **CI/CD Compatibility**: Standard in Python CI pipelines

**Trade-offs**:
- ✅ Powerful fixtures, parametrization, coverage integration, constitutional compliance
- ✅ Test discovery (auto-finds test_*.py files)
- ✅ Rich assertion introspection (better error messages than unittest)
- ❌ External dependency vs. unittest (built-in) - **Acceptable**: Pytest is Python testing standard
- ❌ Fixture magic can be non-obvious - **Mitigated**: Well-documented patterns, team training

**ADR**: Not required (constitutional mandate, tactical testing tool)

---

### Dependency Management: UV (uv package manager)

**Options Considered**:
1. **UV (CHOSEN)** - Fast Rust-based package manager, modern
2. pip + venv - Traditional Python dependency management
3. Poetry - Dependency resolver with lock files
4. PDM - PEP 582-compliant package manager

**Decision Rationale**:
- **Speed**: 10-100x faster than pip (Rust implementation)
- **Lock Files**: `uv.lock` ensures reproducible builds
- **PEP 621 Compliance**: Uses `pyproject.toml` (modern Python packaging standard)
- **Constitutional Alignment**: Principle IX encourages modern tooling
- **Phase II Compatibility**: UV works with FastAPI, Next.js projects

**Trade-offs**:
- ✅ Fast dependency resolution, reproducible builds, modern standard
- ✅ Smaller lock files than Poetry
- ✅ Works with existing pip ecosystem
- ❌ Newer tool (less mature than pip) - **Acceptable**: Backed by Astral (ruff creators), rapidly adopted
- ❌ Installation requirement (not bundled) - **Mitigated**: Single install command, team-controlled environment

**ADR**: Not required (tactical tooling choice)

---

## Technology Stack Summary

| Category | Choice | Rationale |
|----------|--------|-----------|
| **Language** | Python 3.13+ | Constitutional mandate (Principle III) |
| **CLI Framework** | Click 8.1+ | User-friendly errors, exit codes, extensibility |
| **ORM** | SQLModel 0.0.14+ | Constitutional mandate (Principle VI), type-safe validation |
| **Database** | SQLite 3 | Phase I simplicity, zero-config, migration path to PostgreSQL |
| **Testing** | pytest 8.0+ | Constitutional mandate (Principle X), fixture power, coverage |
| **Package Manager** | UV | Speed, reproducible builds, modern Python standard |

**ADRs Required**: 1 total
1. `history/adr/001-sqlite-phase-i-console.md` - Database choice (SQLite vs. PostgreSQL)

---

## Data Model

### Task Entity

**Purpose**: Represents a single todo item with title, completion status, and audit timestamps.

**SQLModel Schema** (`src/models/task.py`):

```python
from datetime import datetime
from sqlmodel import Field, SQLModel
from typing import Optional

class Task(SQLModel, table=True):
    """Task model with user isolation and constitutional fields.

    Constitutional Compliance (Principle VI):
    - id: Auto-incrementing primary key
    - user_id: User isolation (SECURITY CRITICAL)
    - created_at: Audit timestamp (creation)
    - updated_at: Audit timestamp (last modification)
    """
    __tablename__ = "tasks"

    # Constitutional fields (Principle VI)
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, nullable=False, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Domain fields (from spec)
    title: str = Field(min_length=1, max_length=200, nullable=False)
    completed: bool = Field(default=False, nullable=False)
```

**Field Specifications**:

| Field | Type | Constraints | Purpose | Spec Reference |
|-------|------|-------------|---------|----------------|
| `id` | Integer | PK, auto-increment | Unique identifier | FR-004 |
| `user_id` | String(255) | NOT NULL, indexed | User isolation | FR-003, FR-007, Principle II |
| `created_at` | Timestamp | NOT NULL, default=UTC now | Audit trail | FR-005, Principle VI |
| `updated_at` | Timestamp | NOT NULL, default=UTC now | Audit trail | FR-005, Principle VI |
| `title` | String(200) | 1-200 chars, NOT NULL | Task description | FR-001, FR-002 |
| `completed` | Boolean | NOT NULL, default=FALSE | Completion status | FR-005 |

**Indexes**:
- **PRIMARY KEY** (`id`) - Unique task identification
- **INDEX** (`user_id`) - **MANDATORY** for user isolation (Principle II), enables fast user-scoped queries
- **Composite Index** (`user_id`, `created_at DESC`) - Future optimization for listing tasks (Phase I foundation)

**Validation Rules** (Pydantic via SQLModel):
- `title`: Length 1-200 characters (spec FR-002)
- `user_id`: Not empty, max 255 characters (spec FR-003)
- `completed`: Boolean only (no NULL)
- `created_at`, `updated_at`: Timestamp behavior (see below)

**Timestamp Behavior** (Implementation Strategy):

**Phase I Approach** (Simplicity):
- `created_at`: Set once on INSERT via `default_factory=datetime.utcnow()`, never modified
- `updated_at`: Set on INSERT via `default_factory=datetime.utcnow()`, **NOT auto-updated in Phase I**
  - Rationale: Phase I has no UPDATE operations (no edit/complete features), so auto-update not needed
  - Simplicity: Avoid SQLAlchemy event listeners for Phase I console app

**Phase II Enhancement** (Auto-Update):
- `updated_at`: Auto-updated on UPDATE via SQLAlchemy event listener
- Implementation:
  ```python
  from sqlalchemy import event
  from sqlalchemy.orm import Session as AlchemySession

  @event.listens_for(Task, 'before_update')
  def receive_before_update(mapper, connection, target):
      target.updated_at = datetime.utcnow()
  ```

**Immutability** (Phase I):
- **Not enforced** via Pydantic validators (adds complexity without value)
- **Enforced** via code review (service layer does NOT set timestamps manually)
- **Acceptable because**: Phase I has no UPDATE code paths (only INSERT)

**Phase II Migration Path**:
- Add `description` field (TEXT, nullable) - Deferred per spec scope
- Add `priority` field (ENUM: low/medium/high) - Deferred to Phase II
- Add `due_date` field (TIMESTAMP, nullable) - Deferred to Phase II
- Add `tags` field (ARRAY or junction table) - Deferred to Phase II

---

## CLI Command Contracts

### Command: `todo add`

**Usage**:
```bash
todo add --user <user_id> <title>
```

**Arguments**:
- `--user` (REQUIRED): User ID string (non-empty, max 255 chars)
- `<title>` (REQUIRED): Task title (1-200 characters)

**Success Response** (Exit Code 0):
```
✓ Task created successfully
  ID: 42
  Title: "Buy groceries"
  User: alice
  Created: 2025-12-12 10:30:00 UTC
```

**Error Responses**:

| Error Condition | Exit Code | Message | Spec Reference |
|-----------------|-----------|---------|----------------|
| Missing `--user` flag | 2 | `Error: Missing option '--user'` | FR-010 |
| Empty `user_id` | 1 | `User ID cannot be empty` | FR-003, FR-009 |
| Empty title | 1 | `Title cannot be empty` | FR-002, FR-009 |
| Title too long (>200 chars) | 1 | `Title must be 1-200 characters` | FR-002, FR-009 |
| Database error | 1 | `Failed to create task: <error>` | FR-010 |

**Examples**:

```bash
# Success case
$ todo add --user alice "Buy groceries"
✓ Task created successfully
  ID: 1
  Title: "Buy groceries"
  User: alice
  Created: 2025-12-12 10:30:00 UTC

# Validation error: empty title
$ todo add --user alice ""
Error: Title cannot be empty
Exit code: 1

# Validation error: title too long (201 chars)
$ todo add --user alice "$(python -c 'print("a" * 201)')"
Error: Title must be 1-200 characters
Exit code: 1

# Missing required option
$ todo add "Buy groceries"
Error: Missing option '--user'
Exit code: 2

# Empty user_id
$ todo add --user "" "Buy milk"
Error: User ID cannot be empty
Exit code: 1
```

**Click Implementation Sketch** (`src/cli/commands/add.py`):

```python
import click
from src.services.task_service import TaskService
from src.lib.validators import validate_title, validate_user_id

@click.command()
@click.option('--user', required=True, help='User ID (owner of the task)')
@click.argument('title')
def add(user: str, title: str) -> None:
    """Create a new task with the given title.

    Examples:
        todo add --user alice "Buy groceries"
        todo add --user bob "Call dentist at 2pm"
    """
    try:
        # Validation (Principle IX: input validation)
        validate_user_id(user)  # Raises ValueError if empty
        validate_title(title)    # Raises ValueError if empty or >200 chars

        # Create task (user-scoped service call)
        service = TaskService()
        task = service.create_task(user_id=user, title=title)

        # Success output (spec FR-008)
        click.echo(f"✓ Task created successfully")
        click.echo(f"  ID: {task.id}")
        click.echo(f"  Title: \"{task.title}\"")
        click.echo(f"  User: {task.user_id}")
        click.echo(f"  Created: {task.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}")

    except ValueError as e:
        # Validation errors (spec FR-009, FR-010 exit code 1)
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    except Exception as e:
        # Database errors (spec FR-010 exit code 1)
        click.echo(f"Failed to create task: {e}", err=True)
        raise SystemExit(1)
```

---

## Service Layer

### TaskService (`src/services/task_service.py`)

**Purpose**: Business logic for task operations, enforces user isolation.

**Key Methods**:

```python
from sqlmodel import Session, select
from src.models.task import Task
from src.services.db import get_session
from datetime import datetime

class TaskService:
    """Task CRUD operations with user isolation (Principle II).

    **Session Management Pattern**:
    - **Phase I Approach**: Service creates session internally (`with get_session()`)
    - **Rationale**: Simplicity - each method is atomic, no caller coordination needed
    - **Trade-off**: Cannot compose multiple service calls in single transaction (acceptable for Phase I)
    - **Phase II Migration**: Add optional `session: Session = None` parameter for transaction injection
    - **Auto-commit**: Each service method commits before returning (no manual commit needed by caller)
    """

    def create_task(self, user_id: str, title: str) -> Task:
        """Create a new task for the given user.

        Args:
            user_id: User ID (not empty, validated by caller)
            title: Task title (1-200 chars, validated by caller)

        Returns:
            Task: Created task with auto-generated ID and timestamps

        Raises:
            ValueError: If validation fails (input validation)
            DatabaseUnavailableError: Database locked (SQLite write contention) - Caller should retry
            DataIntegrityError: Constraint violation (unique, foreign key, etc.)

        **Error Handling Strategy** (Service Layer):

        **Exceptions Raised**:
        - `ValueError`: Input validation failed (bubbles up from Pydantic/validators)
        - `DatabaseUnavailableError`: Database locked (SQLite write contention) - **Caller should retry**
        - `DataIntegrityError`: Constraint violation (foreign key, unique, check constraints)

        **Exceptions NOT Caught**:
        - Pydantic `ValidationError`: Bubble up to caller (CLI displays user-friendly message)
        - SQLite `OperationalError` ("database is locked"): Wrap as `DatabaseUnavailableError` with retry hint

        **Retry Logic**: Service does NOT retry (stateless design). CLI layer handles retry with exponential backoff.

        **Logging**: Service does NOT log (logging is CLI concern). Errors contain diagnostic info for caller to log.

        **Implementation Pattern**:
        ```python
        from sqlalchemy.exc import OperationalError, IntegrityError

        try:
            session.commit()
        except OperationalError as e:
            if "database is locked" in str(e):
                raise DatabaseUnavailableError("Database busy, please retry") from e
            raise  # Re-raise other operational errors
        except IntegrityError as e:
            raise DataIntegrityError(f"Constraint violation: {e}") from e
        ```

        Constitutional Compliance:
        - Principle II: Task scoped to user_id
        - Principle VI: Sets created_at, updated_at
        - Principle IX: Type hints, docstring
        """
        with get_session() as session:
            # Create task (constitutional fields auto-populated)
            # Timestamp Management: Rely on Task model default_factory (single source of truth)
            # DO NOT manually set created_at/updated_at (avoids clock skew, enforces model contract)
            task = Task(
                user_id=user_id,
                title=title,
                completed=False  # Spec FR-005: default=false
                # created_at and updated_at auto-populated by SQLModel default_factory=datetime.utcnow
            )

            # Persist to database
            session.add(task)
            session.commit()
            session.refresh(task)  # Populate auto-generated ID

            return task

    def get_tasks_for_user(self, user_id: str) -> list[Task]:
        """Retrieve all tasks for a specific user (user isolation).

        Args:
            user_id: User ID

        Returns:
            list[Task]: All tasks owned by user (empty if none)

        Constitutional Compliance:
        - Principle II: MANDATORY user_id filter
        """
        with get_session() as session:
            statement = select(Task).where(Task.user_id == user_id)
            tasks = session.exec(statement).all()
            return list(tasks)
```

**User Isolation Enforcement** (Principle II - SECURITY CRITICAL):
- ✅ ALL queries filter by `user_id` (no cross-user access possible)
- ✅ `create_task` accepts `user_id` as required parameter
- ✅ `get_tasks_for_user` enforces `WHERE user_id = ?` clause
- ✅ Future methods (update, delete) will verify `user_id` ownership before mutation

---

## Database Management

### Connection & Session Management (`src/services/db.py`)

```python
from sqlmodel import create_engine, Session, SQLModel
from contextlib import contextmanager
from pathlib import Path

# Database file path (spec FR-006: current working directory)
DATABASE_PATH = Path.cwd() / "todo.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Create engine with WAL mode for better concurrency
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL logging in development
    connect_args={"check_same_thread": False}  # SQLite thread safety
)

def init_db() -> None:
    """Initialize database schema (create tables if not exist).

    Called on application startup (spec edge case: first run).
    """
    SQLModel.metadata.create_all(engine)

@contextmanager
def get_session() -> Session:
    """Provide database session with automatic cleanup.

    Usage:
        with get_session() as session:
            task = session.query(Task).first()
    """
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
```

**Configuration**:
- **WAL Mode**: Write-Ahead Logging for better concurrent read performance (spec edge case: concurrent operations)
- **Auto-init**: Call `init_db()` on first run (spec edge case: database doesn't exist)
- **Thread Safety**: `check_same_thread=False` allows multi-threaded testing

---

## Non-Functional Requirements (NFRs)

### Performance

**Phase I Targets** (Spec SC-005, Principle XVIII):
- **Task Creation Latency**: p95 <100ms (from CLI invocation to success message)
- **Database Write**: p95 <50ms (INSERT operation)
- **Startup Time**: <500ms (CLI to prompt)

**Measurement**:
- Pytest performance tests in `tests/performance/test_latency.py`
- Assert p95 latency <100ms under load (100 concurrent task creations)

**Optimization Strategies**:
- Index on `user_id` (fast filtering)
- WAL mode (concurrent reads don't block writes)
- Connection pooling (Phase II: use SQLAlchemy pool)

### Reliability

**Data Persistence** (Spec SC-003):
- **Zero Data Loss**: All committed tasks MUST survive application restart
- **ACID Guarantees**: SQLite transactions ensure atomicity
- **Durability**: WAL mode with fsync ensures disk persistence

**Error Handling** (Spec FR-009, Principle XII):
- Validation errors return clear messages (not stack traces)
- Database errors caught and logged (no crashes)
- Graceful degradation (if DB locked, retry with exponential backoff)

### Security

**User Isolation** (Spec SC-004, Principle II - SECURITY CRITICAL):
- ✅ **100% Isolation**: Users see ONLY their own tasks
- ✅ **No Information Disclosure**: Attempting to access another user's task returns generic "not found" (not "permission denied")
- ✅ **Query Enforcement**: ALL Task queries filter by `user_id` (verified via integration tests)

**Input Validation** (Spec FR-002, FR-003, Principle XII):
- Title length: 1-200 characters (Pydantic validation)
- User ID: Non-empty string (validation before database access)
- SQL Injection Prevention: SQLModel ORM uses parameterized queries

**Secrets Management** (Principle XII):
- No secrets needed in Phase I (SQLite is local file)
- `.env.example` template for future secrets (Phase II: DATABASE_URL)

### Maintainability

**Code Quality** (Principle IX):
- ✅ Type hints on ALL functions (enforced by `mypy --strict`)
- ✅ Google-style docstrings (enforced by `pydocstyle`)
- ✅ PEP 8 compliance (enforced by `black` formatter)
- ✅ Maximum function length: 50 lines

**Testing** (Principle X):
- ✅ Coverage target: ≥80% (measured by `pytest-cov`)
- ✅ Test categories: Unit (models, validators), Integration (CLI end-to-end)
- ✅ Test database: In-memory SQLite (`:memory:`) for speed

---

## Testing Strategy

### Test Pyramid

```
         /\
        /E2E\      Integration: 20% (CLI end-to-end workflows)
       /------\
      /  INT   \    Integration: 30% (Service + DB)
     /----------\
    /    UNIT    \  Unit: 50% (Models, validators, pure logic)
   /--------------\
```

### Test Categories

**Unit Tests** (Target: 90% coverage):
- `tests/unit/test_task_model.py`: Task validation (empty title, >200 chars, field constraints)
- `tests/unit/test_validators.py`: Title/user_id validation edge cases
- `tests/unit/test_task_service.py`: Service logic (mocked database)

**Integration Tests** (Target: 80% coverage):
- `tests/integration/test_add_task_integration.py`: Full workflow (CLI → Service → DB → Output)
- Test database: In-memory SQLite (`:memory:`) for isolation
- Fixtures: `test_db` session, `test_user` data

**E2E Tests** (Target: 100% of user stories):
- Spec User Story 1: Create task, verify persistence across restarts
- Spec User Story 2: Validation errors (empty title, too long, missing --user)
- Spec User Story 3: User isolation (alice creates task, bob can't see it)

### Example Test (User Isolation - Spec User Story 3):

```python
def test_user_isolation(test_db):
    """Test that users only see their own tasks (Principle II)."""
    service = TaskService()

    # Alice creates task
    alice_task = service.create_task(user_id="alice", title="Alice's task")

    # Bob creates task
    bob_task = service.create_task(user_id="bob", title="Bob's task")

    # Verify alice sees only her task
    alice_tasks = service.get_tasks_for_user(user_id="alice")
    assert len(alice_tasks) == 1
    assert alice_tasks[0].title == "Alice's task"
    assert alice_task.id not in [t.id for t in service.get_tasks_for_user(user_id="bob")]

    # Verify bob sees only his task
    bob_tasks = service.get_tasks_for_user(user_id="bob")
    assert len(bob_tasks) == 1
    assert bob_tasks[0].title == "Bob's task"
```

---

## Implementation Roadmap

**Phase 0: Research** (already complete via this plan)
- ✅ Technology stack decisions documented
- ✅ ADR candidate identified (SQLite choice)

**Phase 1: Design & Contracts** (next step)
- Create `data-model.md` with Task entity details
- Create `contracts/add-task.md` with CLI command specification
- Create `quickstart.md` with usage examples
- Update `CLAUDE.md` with new technologies (Python 3.13, Click, SQLModel, SQLite, pytest, UV)

**Phase 2: Tasks Breakdown** (deferred to `/sp.tasks` command)
- Generate `tasks.md` with TDD implementation steps
- Sequence: Setup → Models → Validators → Services → CLI → Tests → Integration

**Phase 3: Implementation** (deferred to `/sp.implement` command)

**TDD Sub-Phases** (each follows Red-Green-Refactor cycle):

*Phase 3.1: Database Infrastructure*
- **RED**: Write `test_init_db()` → fails (no `db.py` exists)
- **GREEN**: Implement `src/services/db.py` (engine, session, init_db) → test passes
- **REFACTOR**: Extract DATABASE_URL constant, add WAL mode configuration
- **Validation**: Can create tables, get session, close cleanly

*Phase 3.2: Task Model*
- **RED**: Write `test_task_creation_valid()` → fails (no Task class)
- **GREEN**: Implement `src/models/task.py` (Task SQLModel with 6 fields) → test passes
- **REFACTOR**: Add Pydantic validators (@validator decorators for title/user_id)
- **Validation**: Task instances can be created with valid data, invalid data raises ValueError

*Phase 3.3: Validators*
- **RED**: Write `test_validate_title_empty()`, `test_validate_user_id_empty()` → fail (no validators.py)
- **GREEN**: Implement `src/lib/validators.py` (validate_title, validate_user_id) → tests pass
- **REFACTOR**: Extract common "not empty" validation logic to helper function
- **Validation**: Edge cases pass (1 char, 200 chars, 201 chars, empty string)

*Phase 3.4: Task Service*
- **RED**: Write `test_create_task()`, `test_get_tasks_for_user()` → fail (no TaskService)
- **GREEN**: Implement `src/services/task_service.py` (create_task, get_tasks_for_user) → tests pass
- **REFACTOR**: Extract session management to context manager, add error handling
- **Validation**: User isolation verified (alice's tasks ≠ bob's tasks), timestamps auto-populated

*Phase 3.5: CLI Entry Point*
- **RED**: Write `test_cli_help()` → fails (no main.py)
- **GREEN**: Implement `src/cli/main.py` (Click group, init_db call) → test passes
- **REFACTOR**: Add --version flag, extract init_db to startup hook
- **Validation**: `todo --help` displays command list

*Phase 3.6: CLI Add Command*
- **RED**: Write `test_add_missing_user()` → fails (no add.py)
- **GREEN**: Implement `src/cli/commands/add.py` (Click decorators, help text) → test passes
- **REFACTOR**: Extract success message formatting to helper function
- **Validation**: `todo add --help` works, error handling shows correct exit codes (0/1/2)

*Phase 3.7: Integration Wiring*
- **RED**: Write `test_add_task_integration()` (full CLI → DB workflow) → fails (components not wired)
- **GREEN**: Wire validators → CLI, TaskService → CLI, CLI → main → test passes
- **REFACTOR**: DRY - extract common error formatting logic
- **Validation**: E2E workflow `todo add --user alice "test"` creates task in DB, confirmation displayed

*Phase 3.8: Spec Validation*
- Run all acceptance scenarios from spec.md (12 scenarios across 3 user stories)
- Verify ≥80% coverage (`pytest --cov=src --cov-report=term-missing`)
- Validate performance (p95 <100ms for task creation)
- Fix any failures discovered during acceptance testing

---

## Parallel Work Opportunities

**Purpose**: Maximize team velocity by identifying independent workstreams that can execute concurrently. Use this section for task assignment when multiple developers are available.

### Phase 1: Design & Contracts (4 Independent Workstreams)

**Prerequisite**: `research.md` MUST complete first (provides technology decisions for all other artifacts).

**After research.md completes, these can run in PARALLEL**:

```
Workstream 1A: Data Model Specification
├── Artifact: data-model.md
├── Owner: Backend specialist
├── Duration: ~1 hour
├── Dependencies: research.md (SQLModel, SQLite decisions)
└── Deliverable: Task entity schema with validation rules

Workstream 1B: CLI Contract Specification
├── Artifact: contracts/add-task.md
├── Owner: CLI/UX specialist
├── Duration: ~1 hour
├── Dependencies: research.md (Click framework decision)
└── Deliverable: Command signature, exit codes, error messages

Workstream 1C: User Documentation
├── Artifact: quickstart.md
├── Owner: Documentation specialist
├── Duration: ~45 minutes
├── Dependencies: research.md (installation steps, tech stack)
└── Deliverable: Installation guide, usage examples, troubleshooting

Workstream 1D: ADR Creation (Can overlap with 1A/1B/1C)
├── Artifact: history/adr/0004-database-choice-sqlite-for-phase-i-console.md
├── Owner: Architect
├── Duration: ~30 minutes
├── Dependencies: research.md (database alternatives analysis)
└── Deliverable: SQLite vs PostgreSQL decision rationale
```

**Merge Point**: All Phase 1 workstreams complete before `/sp.tasks` (task breakdown generation).

---

### Phase 3: Implementation (4 Concurrent Workstreams with Sync Points)

**TDD Approach**: Each workstream follows Red-Green-Refactor cycle.

#### Workstream A: Backend Foundation (CRITICAL PATH - starts first)

```
Step A1: Database Infrastructure (Red-Green-Refactor)
├── RED: Write test_init_db() → fails (no db.py)
├── GREEN: Implement src/services/db.py (engine, session, init_db)
├── REFACTOR: Extract connection string to constant
├── Duration: 30 minutes
└── Output: Working database connection

Step A2: Task Model (Red-Green-Refactor)
├── RED: Write test_task_creation_valid() → fails (no Task model)
├── GREEN: Implement src/models/task.py (Task SQLModel)
├── REFACTOR: Add Pydantic validators for title/user_id
├── Duration: 45 minutes
├── Dependencies: Step A1 complete
└── Output: Task model with validation

Step A3: Task Service (Red-Green-Refactor)
├── RED: Write test_create_task() → fails (no TaskService)
├── GREEN: Implement src/services/task_service.py (create_task, get_tasks_for_user)
├── REFACTOR: Extract session management to context manager
├── Duration: 45 minutes
├── Dependencies: Step A1, A2 complete
└── Output: TaskService with user isolation
```

**Workstream A Timeline**: ~2 hours (sequential)

#### Workstream B: Validation Layer (PARALLEL with A2, A3 - INDEPENDENT)

```
Step B1: Validators (Red-Green-Refactor)
├── RED: Write test_validate_title_empty() → fails (no validators.py)
├── GREEN: Implement src/lib/validators.py (validate_title, validate_user_id)
├── REFACTOR: DRY - extract common "not empty" logic
├── Duration: 30 minutes
├── Dependencies: NONE (pure validation logic, no Task imports)
└── Output: Standalone validation functions

Step B2: Validator Unit Tests (Red-Green complete)
├── Test cases: empty title, 1 char, 200 chars, 201 chars, empty user_id
├── Duration: 20 minutes
├── Dependencies: Step B1 complete
└── Output: 100% validator coverage
```

**Workstream B Timeline**: ~50 minutes (can start immediately in parallel with A1)

#### Workstream C: CLI Skeleton (PARALLEL with A3, B - starts after A2)

```
Step C1: CLI Entry Point (Red-Green-Refactor)
├── RED: Write test_cli_help() → fails (no main.py)
├── GREEN: Implement src/cli/main.py (Click group, init_db call)
├── REFACTOR: Add --version flag
├── Duration: 20 minutes
├── Dependencies: Step A1 complete (needs init_db)
└── Output: `todo --help` works

Step C2: Add Command Skeleton (Red-Green-Refactor)
├── RED: Write test_add_missing_user() → fails (no add.py)
├── GREEN: Implement src/cli/commands/add.py (Click decorators, help text only)
├── REFACTOR: Extract help examples to constant
├── Duration: 25 minutes
├── Dependencies: NONE (just Click structure)
└── Output: `todo add --help` works

Step C3: Wire Validators (Red-Green)
├── RED: test_add_empty_title() → fails (no validation)
├── GREEN: Import validators.py, call validate_title/validate_user_id
├── Duration: 15 minutes
├── Dependencies: Step B1, C2 complete
└── Output: CLI rejects invalid input

Step C4: Wire Service (Red-Green)
├── RED: test_add_success() → fails (no TaskService call)
├── GREEN: Import TaskService, call create_task, format output
├── Duration: 20 minutes
├── Dependencies: Step A3, C3 complete
└── Output: Full CLI workflow works
```

**Workstream C Timeline**: ~1.5 hours (can start C1, C2 in parallel with A2)

#### Workstream D: Test Infrastructure (PARALLEL with all - starts first)

```
Step D1: Test Configuration (Red-Green)
├── GREEN: Implement tests/conftest.py (test_db fixture, in-memory SQLite)
├── Duration: 20 minutes
├── Dependencies: NONE (can start immediately)
└── Output: Test database available for all tests

Step D2: Unit Test Files (PARALLEL - after components exist)
├── tests/unit/test_task_model.py (after A2 complete)
├── tests/unit/test_validators.py (after B1 complete)
├── tests/unit/test_task_service.py (after A3 complete)
├── Duration: ~30 minutes total (10 min each)
├── Dependencies: Respective components (A2, B1, A3)
└── Output: ~90% unit test coverage

Step D3: Integration Tests (SYNC POINT - all workstreams complete)
├── tests/integration/test_add_task_integration.py
├── Duration: 45 minutes
├── Dependencies: ALL of A, B, C complete
└── Output: E2E workflow validated
```

**Workstream D Timeline**: ~1.5 hours (overlaps with A/B/C, finishes last)

---

### Parallelization Strategy (Gantt Chart)

```
Time →  0min   30min   60min   90min   120min  150min  180min
        |       |       |       |       |       |       |
A       [─ A1 ─][──── A2 ────][──── A3 ────]
B       [─── B1 ───][─ B2 ─]
C               [C1][── C2 ──][─ C3 ─][─ C4 ─]
D       [D1][────── D2 (incremental) ──────][──── D3 ────]
        |       |       |       |       |       |       |
Sync    START   -       -       -       -       -       ALL DONE
Points                                                  (MERGE)
```

**Key Insights**:
- **Workstream B** (Validators) completes earliest → can start C3 wire-up early
- **Workstream A** is critical path (longest sequential dependency chain)
- **Workstream C** has natural wait points (C3 waits for B1, C4 waits for A3)
- **Workstream D** (Tests) runs continuously, filling gaps while waiting for components

**Team Size Optimization**:
- **1 developer**: Follow A → B → C → D sequentially (~5 hours)
- **2 developers**: Dev1=A, Dev2=B∥D (~2.5 hours with handoffs at C)
- **3 developers**: Dev1=A, Dev2=B, Dev3=C∥D (~2 hours with careful coordination)
- **4 developers**: Dev1=A, Dev2=B, Dev3=C, Dev4=D (~2 hours, minimal blocking)

---

### Sync Points (Merge Gates)

**Sync Point 1**: After A2 (Task Model) + B1 (Validators) complete
- **Action**: Start C3 (Wire Validators into CLI)
- **Validation**: Unit tests for Task model and validators pass

**Sync Point 2**: After A3 (TaskService) complete
- **Action**: Start C4 (Wire Service into CLI)
- **Validation**: TaskService unit tests pass, user isolation verified

**Sync Point 3**: After ALL workstreams (A, B, C, D2) complete
- **Action**: Start D3 (Integration Tests)
- **Validation**: `todo add --user alice "test"` works end-to-end
- **Deliverable**: Ready for spec validation against acceptance scenarios

---

## Risks & Mitigations

### Risk 1: SQLite File Corruption (Medium Likelihood, High Impact)

**Failure Mode**: Improper shutdown corrupts `todo.db` file
**Blast Radius**: All tasks lost for all users
**Mitigation**:
- ✅ Use WAL mode (more resilient to crashes)
- ✅ Implement backup command (future: `todo backup`) - Deferred to Phase I expansion
- ✅ Document recovery procedure (delete corrupted file, recreate from backup)
- ✅ Test abnormal shutdown scenarios (kill -9 during write)

### Risk 2: Concurrent Write Conflicts (Low Likelihood, Medium Impact)

**Failure Mode**: Two processes write to `todo.db` simultaneously, one blocks/fails
**Blast Radius**: Single task creation fails with "database locked" error
**Mitigation**:
- ✅ WAL mode reduces lock contention (readers don't block writers)
- ✅ Retry logic with exponential backoff (3 retries, 100ms → 200ms → 400ms delays)
- ✅ User-friendly error message: "Database busy, please try again"
- ✅ Phase I scope limits concurrent writes (single-user console app)

### Risk 3: Title Encoding Issues (Low Likelihood, Low Impact)

**Failure Mode**: Emojis or special characters cause encoding errors (spec edge case: "Buy 🥛 milk")
**Blast Radius**: Single task creation fails with encoding error
**Mitigation**:
- ✅ SQLite uses UTF-8 by default (supports emojis)
- ✅ Pydantic validation preserves Unicode characters
- ✅ Integration test: Create task with emoji, verify roundtrip

---

## Constitutional Alignment (Re-Check)

Post-design validation against constitutional principles:

| Principle | Compliance | Evidence |
|-----------|------------|----------|
| **I: Spec-Driven** | ✅ PASS | This plan.md follows completed spec.md |
| **II: User Isolation** | ✅ PASS | All queries filter by user_id, index enforced, integration tests verify |
| **III: Python 3.13+** | ✅ PASS | Explicitly required in tech stack |
| **VI: Database Standards** | ✅ PASS | Task model includes id, user_id, created_at, updated_at |
| **IX: Code Quality** | ✅ PASS | Type hints, docstrings, mypy/black/pydocstyle enforced |
| **X: Testing** | ✅ PASS | pytest, ≥80% coverage, TDD approach |
| **XII: Security** | ✅ PASS | Input validation, SQLModel prevents injection, user isolation |
| **XVIII: Performance** | ✅ PASS | p95 <100ms target, performance tests planned |

**GATE STATUS**: ✅ **PASS** - All principles satisfied post-design

---

## ADR Summary

**ADR Created**: 1
1. **`history/adr/001-sqlite-phase-i-console.md`** - Database Choice (SQLite vs. PostgreSQL)
   - **Decision**: Use SQLite for Phase I console application
   - **Rationale**: Zero-config, bundled, appropriate for local console app, migration path to PostgreSQL
   - **Alternatives**: PostgreSQL (over-engineered for Phase I), MongoDB (schema flexibility not needed)

**Suggested ADR Text** (for user approval):
```
📋 Architectural decision detected: Database choice (SQLite vs. PostgreSQL for Phase I)
   Document reasoning and tradeoffs? Run `/sp.adr "Database Choice: SQLite for Phase I Console"`
```

---

## Next Steps

1. ✅ **Plan Complete**: This plan.md documents all architectural decisions
2. ⏭️ **Create Supporting Artifacts** (Phase 1 of `/sp.plan`):
   - `research.md` - Consolidate technology research and decisions
   - `data-model.md` - Detailed Task entity specification
   - `contracts/add-task.md` - CLI command contract
   - `quickstart.md` - Usage examples and integration guide
3. ⏭️ **Update Agent Context**: Run `.specify/scripts/bash/update-agent-context.sh` to add technologies to CLAUDE.md
4. ⏭️ **Create ADR**: User approval to run `/sp.adr "Database Choice: SQLite for Phase I Console"`
5. ⏭️ **Generate Tasks**: Run `/sp.tasks` to create implementation breakdown
6. ⏭️ **Implement**: Run `/sp.implement` to build with TDD
