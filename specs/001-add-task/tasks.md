# Tasks: Add Task Feature

**Input**: Design documents from `/specs/001-add-task/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/add-task.md

**Tests**: This feature follows TDD approach with ≥80% coverage target (Constitutional Principle X)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description | Spec Ref | Acceptance`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- **Spec Ref**: Traceability to spec.md (FR-XXX, SC-XXX, US-X.AC-Y)
- **Acceptance**: Testable completion criterion (what artifact proves this is done?)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- All paths are relative to project root

---

## 🚦 CHECKPOINT PATTERN GUIDE

After each phase, you MUST pause for human approval:

**Agent Says**: "Phase X complete: [summary of artifacts]. Ready for Phase Y?"
**You Review**: Check artifacts are present and testable
**You Approve**: "Looks good! Committing Phase X." → `git commit`
**You Continue**: "Proceed to Phase Y"

**⚠️ NEVER skip checkpoints** - they prevent wasted work and ensure alignment

---

## Phase 1: Setup (Project Foundation)

**Purpose**: Initialize project structure and configuration files

**Why This Phase**: Creates the skeleton that all implementation depends on (FR-006: database location, FR-001: CLI entry point)

### Tasks

- [X] **T001** Create project directory structure
  - **Files**: `src/`, `tests/`, `src/models/`, `src/services/`, `src/cli/`, `src/cli/commands/`, `src/lib/`
  - **Spec**: FR-006 (project structure for SQLite persistence)
  - **Acceptance**: Run `ls -la src/ tests/` and verify all directories exist
  - **Time**: 5 minutes

- [X] **T002** Create Python package markers
  - **Files**: `src/__init__.py`, `src/models/__init__.py`, `src/services/__init__.py`, `src/cli/__init__.py`, `src/cli/commands/__init__.py`, `src/lib/__init__.py`
  - **Spec**: Plan (Python package structure)
  - **Acceptance**: Run `python -c "import src.models"` and verify no ImportError
  - **Time**: 5 minutes

- [X] **T003** Initialize Python project with UV
  - **Command**: `uv init` to create pyproject.toml
  - **Spec**: Plan (UV package manager requirement)
  - **Acceptance**: Run `cat pyproject.toml` and verify [project] section exists with name, version, description
  - **Time**: 5 minutes

- [X] **T004** Add core dependencies to pyproject.toml
  - **Dependencies**: SQLModel >=0.0.14, Click >=8.1.0, Python >=3.13
  - **Spec**: Constitutional Principle VI (SQLModel), Plan (Click for CLI), Constitutional (Python 3.13+)
  - **Acceptance**: Run `cat pyproject.toml` and verify [project.dependencies] contains all 3 packages
  - **Time**: 10 minutes

- [X] **T005** Add development dependencies to pyproject.toml
  - **Dev Dependencies**: pytest >=7.4.0, pytest-cov >=4.1.0, black >=23.0.0, mypy >=1.5.0, pydocstyle >=6.3.0
  - **Spec**: Plan (TDD testing tools), Constitutional Principle X (≥80% coverage)
  - **Acceptance**: Run `cat pyproject.toml` and verify [project.optional-dependencies.dev] contains all 5 packages
  - **Time**: 10 minutes

- [X] **T006** [P] Configure CLI entry point in pyproject.toml
  - **Config**: `[project.scripts]` with `todo = "src.cli.main:cli"`
  - **Spec**: FR-001 (CLI command `todo add`), Plan lines 105-126
  - **Acceptance**: Run `cat pyproject.toml` and verify [project.scripts] section with todo entry point
  - **Time**: 10 minutes

- [X] **T007** [P] Configure linting and formatting tools
  - **Config**: Add `[tool.black]`, `[tool.mypy]`, `[tool.pydocstyle]` sections to pyproject.toml
  - **Spec**: Constitutional Principle X (code quality standards)
  - **Acceptance**: Run `cat pyproject.toml` and verify all 3 tool sections exist with target-version, strict flags
  - **Time**: 15 minutes

- [X] **T008** [P] Create .gitignore
  - **Entries**: `todo.db`, `.venv`, `__pycache__`, `.pytest_cache`, `.coverage`, `htmlcov/`, `.env`
  - **Spec**: FR-006 (ignore database file), Plan (ignore test artifacts)
  - **Acceptance**: Run `cat .gitignore` and verify all 7 patterns listed
  - **Time**: 5 minutes

- [X] **T009** [P] Create .env.example template
  - **Content**: Empty file with comment "# Phase II: Add DATABASE_URL here"
  - **Spec**: Plan (Phase II migration path to PostgreSQL)
  - **Acceptance**: Run `cat .env.example` and verify comment exists
  - **Time**: 5 minutes

- [X] **T010** Install dependencies with UV
  - **Command**: `uv sync --dev`
  - **Spec**: Plan (UV package manager)
  - **Acceptance**: Run `uv pip list` and verify SQLModel, Click, pytest are installed
  - **Time**: 10 minutes

### 🚦 CHECKPOINT 1: Setup Complete

**Agent Deliverables**:
- ✓ Project structure: 6 directories created (src/, tests/, models/, services/, cli/, lib/)
- ✓ Configuration: pyproject.toml with 3 core deps + 5 dev deps + CLI entry point
- ✓ Environment: .gitignore, .env.example created
- ✓ Dependencies: All packages installed via `uv sync --dev`

**Human Review**:
1. Run `tree -L 2 -a` → Verify directory structure matches spec
2. Run `cat pyproject.toml` → Verify dependencies and entry point correct
3. Run `uv pip list` → Verify SQLModel, Click, pytest installed

**Human Approval Required**: "Looks good! Committing Phase 1." → `git commit -m "feat: project setup and configuration"`

**Next Command**: "Proceed to Phase 2: Foundational Infrastructure"

**Estimated Time**: 1.5 hours

---

## Phase 2: Foundational Infrastructure (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST exist before ANY user story can be implemented

**Why This Phase**: Database and test infrastructure are foundational - no user story can function without them (FR-006: persistence, SC-003: data durability)

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Tasks

#### Database Infrastructure

- [X] **T011** Create custom exceptions module
  - **File**: `src/lib/exceptions.py`
  - **Classes**: `DatabaseUnavailableError(Exception)`, `DataIntegrityError(Exception)`
  - **Spec**: Plan lines 582-609 (error handling strategy)
  - **Acceptance**: Run `python -c "from src.lib.exceptions import DatabaseUnavailableError, DataIntegrityError"` and verify no ImportError
  - **Time**: 15 minutes

- [X] **T012** Write unit test for init_db() function
  - **File**: `tests/unit/test_db.py`
  - **Test**: `test_init_db_creates_tables()` - creates in-memory database, calls init_db(), verifies Task table exists
  - **Spec**: FR-006 (database initialization), TDD approach
  - **Acceptance**: Run `pytest tests/unit/test_db.py::test_init_db_creates_tables` and verify it FAILS (TDD red phase)
  - **Time**: 15 minutes

- [X] **T013** Implement database engine and session configuration
  - **File**: `src/services/db.py`
  - **Code**: Define `ENGINE` (create_engine with SQLite URL), `DATABASE_URL = "sqlite:///todo.db"`
  - **Spec**: FR-006 (SQLite database in current directory), Plan lines 192-239
  - **Acceptance**: Run `python -c "from src.services.db import ENGINE, DATABASE_URL; print(DATABASE_URL)"` and verify output is "sqlite:///todo.db"
  - **Time**: 15 minutes

- [X] **T014** Configure WAL mode for SQLite concurrency
  - **File**: `src/services/db.py`
  - **Code**: Add `@event.listens_for(ENGINE, "connect")` to execute `PRAGMA journal_mode=WAL`
  - **Spec**: Plan ADR-0004 (WAL mode for concurrency), Edge Case: concurrent operations
  - **Acceptance**: Run `sqlite3 todo.db "PRAGMA journal_mode"` after init and verify output is "wal"
  - **Time**: 15 minutes

- [X] **T015** Implement init_db() function
  - **File**: `src/services/db.py`
  - **Code**: `def init_db() -> None:` calls `SQLModel.metadata.create_all(ENGINE)`
  - **Spec**: FR-006 (create database tables), SC-003 (persistence)
  - **Acceptance**: Run `pytest tests/unit/test_db.py::test_init_db_creates_tables` and verify it PASSES (TDD green phase)
  - **Time**: 15 minutes

- [X] **T016** Write unit test for get_session() context manager
  - **File**: `tests/unit/test_db.py`
  - **Test**: `test_get_session_yields_session()` - verifies get_session() yields a Session object and auto-closes
  - **Spec**: Plan lines 559-565 (session management pattern), TDD approach
  - **Acceptance**: Run `pytest tests/unit/test_db.py::test_get_session_yields_session` and verify it FAILS (TDD red phase)
  - **Time**: 15 minutes

- [X] **T017** Implement get_session() context manager
  - **File**: `src/services/db.py`
  - **Code**: `@contextmanager def get_session() -> Generator[Session, None, None]:` yields session, closes on exit
  - **Spec**: Plan lines 559-565 (session management), Edge Case: resource cleanup
  - **Acceptance**: Run `pytest tests/unit/test_db.py::test_get_session_yields_session` and verify it PASSES (TDD green phase)
  - **Time**: 15 minutes

#### Test Infrastructure

- [X] **T018** [P] Create pytest configuration with test database fixture
  - **File**: `tests/conftest.py`
  - **Code**: `@pytest.fixture def test_db()` creates in-memory SQLite (`:memory:`), yields session, cleans up
  - **Spec**: Plan (test infrastructure with in-memory database for speed)
  - **Acceptance**: Run `pytest --co -q` and verify conftest.py is loaded (shows "test session starts")
  - **Time**: 20 minutes

- [X] **T019** [P] Create test package markers
  - **Files**: `tests/__init__.py`, `tests/unit/__init__.py`, `tests/integration/__init__.py`
  - **Spec**: Plan (test discovery for pytest)
  - **Acceptance**: Run `pytest --co` and verify pytest discovers test directories
  - **Time**: 5 minutes

### 🚦 CHECKPOINT 2: Foundational Infrastructure Complete

**Agent Deliverables**:
- ✓ Database: ENGINE configured with SQLite + WAL mode (src/services/db.py)
- ✓ Initialization: init_db() creates tables (FR-006)
- ✓ Session Management: get_session() context manager (Plan session pattern)
- ✓ Exceptions: DatabaseUnavailableError, DataIntegrityError (Plan error handling)
- ✓ Test Infrastructure: conftest.py with test_db fixture
- ✓ TDD Verified: 2 tests written FIRST, then implementation made them PASS

**Human Review**:
1. Run `pytest tests/unit/test_db.py -v` → Verify 2 tests PASS (test_init_db, test_get_session)
2. Run `python -c "from src.services.db import init_db; init_db()"` → Verify no errors
3. Run `ls todo.db` → Verify database file created
4. Run `sqlite3 todo.db "PRAGMA journal_mode"` → Verify output is "wal"

**Human Approval Required**: "Foundation verified! Committing Phase 2." → `git commit -m "feat: database and test infrastructure"`

**Next Command**: "Proceed to Phase 3: User Story 1 (MVP)"

**Estimated Time**: 2 hours

**🎯 CRITICAL GATE**: User story implementation can now begin in parallel after this checkpoint

---

## Phase 3: User Story 1 - Create Task with Valid Title (Priority: P1) 🎯 MVP

**Goal**: Users can create tasks with titles via CLI command `todo add --user <user_id> <title>` and see confirmation with task details

**Why This Priority**: P1 (MVP) - Core value proposition. Without task creation, the application has no purpose (spec lines 14-15)

**Spec Traceability**: US-1, FR-001, FR-002, FR-004, FR-005, FR-006, FR-008, SC-001, SC-003, SC-005

**Independent Test**: Run `todo add --user alice "Buy groceries"` and verify task is created with ID, stored in database, and persists across restarts (US-1 Independent Test)

### Tests for User Story 1 (TDD - Write FIRST, ensure they FAIL)

#### Unit Tests - Task Model (7 tests)

- [X] **T020** [P] [US1] Write test_task_creation_valid()
  - **File**: `tests/unit/test_task_model.py`
  - **Test**: Create Task(user_id="alice", title="Buy milk", completed=False), verify all fields populated
  - **Spec**: US-1.AC-1 (task creation), FR-005 (6 required fields)
  - **Acceptance**: Run test and verify it FAILS with "NameError: name 'Task' is not defined" (no model exists yet)
  - **Time**: 15 minutes

- [X] **T021** [P] [US1] Write test_task_title_empty_rejected()
  - **File**: `tests/unit/test_task_model.py`
  - **Test**: Create Task with title="", verify raises ValidationError
  - **Spec**: US-2.AC-1 (empty title validation), FR-002 (1-200 chars)
  - **Acceptance**: Run test and verify it FAILS (no validation exists yet)
  - **Time**: 10 minutes

- [X] **T022** [P] [US1] Write test_task_title_too_long_rejected()
  - **File**: `tests/unit/test_task_model.py`
  - **Test**: Create Task with title="x"*201, verify raises ValidationError
  - **Spec**: US-2.AC-2 (title too long), FR-002 (max 200 chars), Edge Case line 66
  - **Acceptance**: Run test and verify it FAILS (no validation exists yet)
  - **Time**: 10 minutes

- [X] **T023** [P] [US1] Write test_task_user_id_empty_rejected()
  - **File**: `tests/unit/test_task_model.py`
  - **Test**: Create Task with user_id="", verify raises ValidationError
  - **Spec**: US-2.AC-4 (empty user_id), FR-003 (user_id not empty)
  - **Acceptance**: Run test and verify it FAILS (no validation exists yet)
  - **Time**: 10 minutes

- [X] **T024** [P] [US1] Write test_task_boundary_1_char()
  - **File**: `tests/unit/test_task_model.py`
  - **Test**: Create Task with title="a" (1 char), verify succeeds
  - **Spec**: Edge Case line 64 (boundary: exactly 1 character should succeed)
  - **Acceptance**: Run test and verify it FAILS (no model exists yet)
  - **Time**: 10 minutes

- [X] **T025** [P] [US1] Write test_task_boundary_200_chars()
  - **File**: `tests/unit/test_task_model.py`
  - **Test**: Create Task with title="x"*200, verify succeeds
  - **Spec**: Edge Case line 65 (boundary: exactly 200 characters should succeed)
  - **Acceptance**: Run test and verify it FAILS (no model exists yet)
  - **Time**: 10 minutes

- [X] **T026** [P] [US1] Write test_task_emoji_in_title()
  - **File**: `tests/unit/test_task_model.py`
  - **Test**: Create Task with title="Buy 🥛 milk", verify emoji preserved
  - **Spec**: Edge Case line 69 (special characters: emojis should succeed and be preserved)
  - **Acceptance**: Run test and verify it FAILS (no model exists yet)
  - **Time**: 10 minutes

#### Unit Tests - Validators (8 tests)

- [X] **T027** [P] [US1] Write test_validate_title_empty()
  - **File**: `tests/unit/test_validators.py`
  - **Test**: Call validate_title(""), verify raises ValueError with message "Title cannot be empty"
  - **Spec**: US-2.AC-1 (empty title error), FR-002, FR-009 (clear error messages)
  - **Acceptance**: Run test and verify it FAILS with "NameError: name 'validate_title' is not defined"
  - **Time**: 15 minutes

- [X] **T028** [P] [US1] Write test_validate_title_valid()
  - **File**: `tests/unit/test_validators.py`
  - **Test**: Call validate_title("Buy milk"), verify returns "Buy milk" unchanged
  - **Spec**: FR-002 (valid title 1-200 chars)
  - **Acceptance**: Run test and verify it FAILS (no function exists yet)
  - **Time**: 10 minutes

- [X] **T029** [P] [US1] Write test_validate_title_boundary_1_char()
  - **File**: `tests/unit/test_validators.py`
  - **Test**: Call validate_title("a"), verify returns "a"
  - **Spec**: Edge Case line 64 (boundary value: 1 char)
  - **Acceptance**: Run test and verify it FAILS (no function exists yet)
  - **Time**: 10 minutes

- [X] **T030** [P] [US1] Write test_validate_title_boundary_200_chars()
  - **File**: `tests/unit/test_validators.py`
  - **Test**: Call validate_title("x"*200), verify returns full string
  - **Spec**: Edge Case line 65 (boundary value: 200 chars)
  - **Acceptance**: Run test and verify it FAILS (no function exists yet)
  - **Time**: 10 minutes

- [X] **T031** [P] [US1] Write test_validate_title_too_long()
  - **File**: `tests/unit/test_validators.py`
  - **Test**: Call validate_title("x"*201), verify raises ValueError with "Title must be 1-200 characters"
  - **Spec**: US-2.AC-2 (too long), Edge Case line 66, FR-009
  - **Acceptance**: Run test and verify it FAILS (no function exists yet)
  - **Time**: 10 minutes

- [X] **T032** [P] [US1] Write test_validate_user_id_empty()
  - **File**: `tests/unit/test_validators.py`
  - **Test**: Call validate_user_id(""), verify raises ValueError with "User ID cannot be empty"
  - **Spec**: US-2.AC-4 (empty user_id), FR-003, FR-009
  - **Acceptance**: Run test and verify it FAILS (no function exists yet)
  - **Time**: 10 minutes

- [X] **T033** [P] [US1] Write test_validate_user_id_whitespace()
  - **File**: `tests/unit/test_validators.py`
  - **Test**: Call validate_user_id("   "), verify raises ValueError
  - **Spec**: FR-003 (user_id not empty - whitespace counts as empty)
  - **Acceptance**: Run test and verify it FAILS (no function exists yet)
  - **Time**: 10 minutes

- [X] **T034** [P] [US1] Write test_validate_user_id_valid()
  - **File**: `tests/unit/test_validators.py`
  - **Test**: Call validate_user_id("alice"), verify returns "alice"
  - **Spec**: FR-003 (valid user_id), US-1.AC-1
  - **Acceptance**: Run test and verify it FAILS (no function exists yet)
  - **Time**: 10 minutes

#### Unit Tests - Task Service (3 tests)

- [X] **T035** [P] [US1] Write test_create_task_valid()
  - **File**: `tests/unit/test_task_service.py`
  - **Test**: Call TaskService.create_task(user_id="alice", title="Buy milk"), verify Task returned with ID assigned
  - **Spec**: US-1.AC-1 (create task), FR-004 (auto-incrementing ID), FR-005 (all fields)
  - **Acceptance**: Run test and verify it FAILS with "NameError: name 'TaskService' is not defined"
  - **Time**: 20 minutes

- [X] **T036** [P] [US1] Write test_create_task_timestamps_populated()
  - **File**: `tests/unit/test_task_service.py`
  - **Test**: Call create_task(), verify created_at and updated_at are non-null timestamps
  - **Spec**: FR-005 (timestamps), Plan lines 425-448 (timestamp management via default_factory)
  - **Acceptance**: Run test and verify it FAILS (no service exists yet)
  - **Time**: 15 minutes

- [X] **T037** [P] [US1] Write test_get_tasks_for_user()
  - **File**: `tests/unit/test_task_service.py`
  - **Test**: Create 2 tasks for alice, 1 for bob, call get_tasks_for_user("alice"), verify returns 2 tasks
  - **Spec**: FR-007 (filter by user_id), US-3.AC-1 (user isolation)
  - **Acceptance**: Run test and verify it FAILS (no service exists yet)
  - **Time**: 20 minutes

#### Integration Tests - CLI End-to-End (5 tests)

- [X] **T038** [P] [US1] Write test_add_success()
  - **File**: `tests/integration/test_add_task_integration.py`
  - **Test**: Use CliRunner to invoke `todo add --user alice "Buy groceries"`, verify exit code 0 and success message
  - **Spec**: US-1.AC-1 (full workflow), FR-001 (CLI command), FR-010 (exit code 0), FR-008 (success message)
  - **Acceptance**: Run test and verify it FAILS with "Command 'todo' not found" (no CLI exists yet)
  - **Time**: 20 minutes

- [X] **T039** [P] [US1] Write test_add_persistence()
  - **File**: `tests/integration/test_add_task_integration.py`
  - **Test**: Create task, close database, reopen, verify task still exists
  - **Spec**: US-1.AC-2 (persistence across restarts), SC-003 (100% persistence), FR-006
  - **Acceptance**: Run test and verify it FAILS (no CLI exists yet)
  - **Time**: 20 minutes

- [X] **T040** [P] [US1] Write test_add_auto_increment_id()
  - **File**: `tests/integration/test_add_task_integration.py`
  - **Test**: Create 10 tasks, verify 11th task gets ID=11
  - **Spec**: US-1.AC-4 (auto-increment from highest ID), FR-004
  - **Acceptance**: Run test and verify it FAILS (no CLI exists yet)
  - **Time**: 15 minutes

- [X] **T041** [P] [US1] Write test_cli_help()
  - **File**: `tests/unit/test_cli_main.py`
  - **Test**: Use CliRunner to invoke `todo --help`, verify displays "add" command
  - **Spec**: FR-001 (CLI usability), Plan (Click framework auto-help)
  - **Acceptance**: Run test and verify it FAILS (no CLI exists yet)
  - **Time**: 15 minutes

- [X] **T042** [P] [US1] Write test_cli_version()
  - **File**: `tests/unit/test_cli_main.py`
  - **Test**: Use CliRunner to invoke `todo --version`, verify displays version "0.1.0"
  - **Spec**: Plan lines 175-197 (version option)
  - **Acceptance**: Run test and verify it FAILS (no CLI exists yet)
  - **Time**: 10 minutes

### 🚦 CHECKPOINT 3A: User Story 1 Tests Complete (TDD Red Phase)

**Agent Deliverables**:
- ✓ Test Files Created: 4 files (test_task_model.py, test_validators.py, test_task_service.py, test_add_task_integration.py, test_cli_main.py)
- ✓ Test Count: 23 tests written (7 model + 8 validators + 3 service + 5 integration)
- ✓ All Tests FAIL: Verified red phase (tests fail because no implementation exists)

**Human Review**:
1. Run `pytest tests/unit/test_task_model.py -v` → Verify 7 tests FAIL with expected errors
2. Run `pytest tests/unit/test_validators.py -v` → Verify 8 tests FAIL
3. Run `pytest tests/unit/test_task_service.py -v` → Verify 3 tests FAIL
4. Run `pytest tests/integration/ -v` → Verify 5 tests FAIL
5. Run `pytest --co -q` → Verify 23 tests discovered

**Human Approval Required**: "All 23 tests failing as expected (TDD red phase)! Committing tests." → `git commit -m "test(US1): add 23 failing tests for task creation"`

**Next Command**: "Proceed to User Story 1 Implementation"

**Estimated Time**: 4 hours

---

### Implementation for User Story 1

#### Task Model

- [X] **T043** [US1] Implement Task SQLModel class with Pydantic validators
  - **File**: `src/models/task.py`
  - **Code**:
    ```python
    class Task(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        user_id: str = Field(index=True)  # FR-007: indexed for user isolation
        title: str
        completed: bool = Field(default=False)  # FR-005: default=false
        created_at: datetime = Field(default_factory=datetime.utcnow)  # FR-005
        updated_at: datetime = Field(default_factory=datetime.utcnow)  # FR-005

        @validator('title')
        def validate_title_length(cls, v):
            if not v or len(v) == 0:
                raise ValueError("Title cannot be empty")  # FR-009
            if len(v) > 200:
                raise ValueError("Title must be 1-200 characters")  # FR-002, FR-009
            return v

        @validator('user_id')
        def validate_user_id_not_empty(cls, v):
            if not v or v.strip() == "":
                raise ValueError("User ID cannot be empty")  # FR-003, FR-009
            return v
    ```
  - **Spec**: FR-005 (6 fields), FR-002 (title validation), FR-003 (user_id validation), FR-007 (user_id index), Plan lines 425-448 (timestamp via default_factory)
  - **Acceptance**: Run `pytest tests/unit/test_task_model.py -v` and verify all 7 tests PASS (TDD green phase)
  - **Time**: 25 minutes

#### Validators

- [X] **T044** [P] [US1] Implement validate_title() function
  - **File**: `src/lib/validators.py`
  - **Code**:
    ```python
    def validate_title(title: str) -> str:
        if not title or len(title) == 0:
            raise ValueError("Title cannot be empty")
        if len(title) > 200:
            raise ValueError("Title must be 1-200 characters")
        return title
    ```
  - **Spec**: FR-002 (1-200 chars), FR-009 (clear error messages), Plan lines 582-609 (validator pattern)
  - **Acceptance**: Run `pytest tests/unit/test_validators.py::test_validate_title* -v` and verify 5 title tests PASS
  - **Time**: 15 minutes

- [X] **T045** [P] [US1] Implement validate_user_id() function
  - **File**: `src/lib/validators.py`
  - **Code**:
    ```python
    def validate_user_id(user_id: str) -> str:
        if not user_id or user_id.strip() == "":
            raise ValueError("User ID cannot be empty")
        return user_id
    ```
  - **Spec**: FR-003 (not empty), FR-009 (clear error messages)
  - **Acceptance**: Run `pytest tests/unit/test_validators.py::test_validate_user_id* -v` and verify 3 user_id tests PASS
  - **Time**: 10 minutes

#### Task Service

- [X] **T046** [US1] Implement TaskService class with session management
  - **File**: `src/services/task_service.py`
  - **Code**:
    ```python
    class TaskService:
        """Task CRUD operations with user isolation (Principle II).

        Session Management: Service creates session internally (with get_session())
        """

        def __init__(self):
            pass  # Stateless service
    ```
  - **Spec**: Plan lines 559-565 (session management pattern), Constitutional Principle II (user isolation)
  - **Acceptance**: Run `python -c "from src.services.task_service import TaskService; TaskService()"` and verify no errors
  - **Time**: 10 minutes

- [X] **T047** [US1] Implement create_task() method
  - **File**: `src/services/task_service.py`
  - **Code**:
    ```python
    def create_task(self, user_id: str, title: str) -> Task:
        with get_session() as session:
            task = Task(
                user_id=user_id,
                title=title,
                completed=False  # FR-005: default=false
                # created_at and updated_at auto-populated by default_factory
            )
            session.add(task)
            session.commit()
            session.refresh(task)  # Get auto-generated ID
            return task
    ```
  - **Spec**: US-1.AC-1 (create task), FR-004 (auto-increment ID), FR-005 (6 fields), Plan lines 617-625 (timestamp management)
  - **Acceptance**: Run `pytest tests/unit/test_task_service.py::test_create_task_valid -v` and verify PASSES
  - **Time**: 20 minutes

- [X] **T048** [US1] Implement get_tasks_for_user() method
  - **File**: `src/services/task_service.py`
  - **Code**:
    ```python
    def get_tasks_for_user(self, user_id: str) -> list[Task]:
        with get_session() as session:
            statement = select(Task).where(Task.user_id == user_id)  # FR-007: filter by user_id
            results = session.exec(statement)
            return results.all()
    ```
  - **Spec**: FR-007 (filter by user_id), US-3.AC-3 (user_id filtering), Constitutional Principle II (user isolation)
  - **Acceptance**: Run `pytest tests/unit/test_task_service.py::test_get_tasks_for_user -v` and verify PASSES
  - **Time**: 15 minutes

- [X] **T049** [US1] Add error handling to create_task()
  - **File**: `src/services/task_service.py`
  - **Code**: Wrap session.commit() with try/except for OperationalError (database locked) and IntegrityError
  - **Spec**: Plan lines 582-609 (error handling strategy), Edge Case: concurrent operations
  - **Acceptance**: Run `pytest tests/unit/test_task_service.py -v` and verify all 3 service tests PASS
  - **Time**: 20 minutes

#### CLI Entry Point

- [X] **T050** [US1] Implement CLI group in src/cli/main.py
  - **File**: `src/cli/main.py`
  - **Code**:
    ```python
    import click
    from src.services.db import init_db

    @click.group()
    @click.version_option(version="0.1.0")
    def cli():
        """Todo CLI application."""
        init_db()  # FR-006: initialize database on every CLI invocation

    if __name__ == "__main__":
        cli()
    ```
  - **Spec**: FR-001 (CLI framework), FR-006 (init database), Plan lines 175-197 (CLI entry point pattern)
  - **Acceptance**: Run `python src/cli/main.py --help` and verify displays usage
  - **Time**: 15 minutes

#### CLI Add Command

- [X] **T051** [US1] Implement add command skeleton
  - **File**: `src/cli/commands/add.py`
  - **Code**:
    ```python
    import click

    @click.command()
    @click.option('--user', required=True, help='User ID')
    @click.argument('title')
    def add(user: str, title: str):
        """Create a new task."""
        pass  # Implementation in next tasks
    ```
  - **Spec**: FR-001 (todo add --user <user_id> <title>), US-2.AC-3 (missing --user returns exit code 2)
  - **Acceptance**: Run `python -c "from src.cli.commands.add import add"` and verify no ImportError
  - **Time**: 15 minutes

- [X] **T052** [US1] Register add command in main.py
  - **File**: `src/cli/main.py`
  - **Code**: Add `from src.cli.commands.add import add` and `cli.add_command(add)` after @click.group()
  - **Spec**: FR-001 (todo add command available), Plan lines 175-197 (command registration)
  - **Acceptance**: Run `python src/cli/main.py --help` and verify "add" command listed
  - **Time**: 10 minutes

- [X] **T053** [US1] Wire validators into add command
  - **File**: `src/cli/commands/add.py`
  - **Code**: Import validate_user_id, validate_title; call both at start of add(); catch ValueError and display error with exit code 1
  - **Spec**: FR-002 (title validation), FR-003 (user_id validation), FR-009 (error messages), FR-010 (exit code 1)
  - **Acceptance**: Run `pytest tests/integration/test_add_task_integration.py::test_add_success -v` and verify closer to passing (validation works)
  - **Time**: 20 minutes

- [X] **T054** [US1] Wire TaskService into add command
  - **File**: `src/cli/commands/add.py`
  - **Code**: Import TaskService; call service.create_task(user, title); format success message "Created task {task.id}: {task.title}"
  - **Spec**: FR-008 (success confirmation with task ID), US-1.AC-1 (full workflow), SC-001 (task creation <3 seconds)
  - **Acceptance**: Run `pytest tests/integration/test_add_task_integration.py::test_add_success -v` and verify PASSES
  - **Time**: 20 minutes

- [X] **T055** [US1] Add exit code handling to add command
  - **File**: `src/cli/commands/add.py`
  - **Code**: Ensure ValueError exits with code 1, success exits with code 0 (Click default), missing --user exits with code 2 (Click automatic)
  - **Spec**: FR-010 (exit codes: 0 success, 1 validation error, 2 missing option)
  - **Acceptance**: Run `pytest tests/integration/ -v` and verify all 5 integration tests PASS
  - **Time**: 15 minutes

### 🚦 CHECKPOINT 3B: User Story 1 Implementation Complete (TDD Green Phase)

**Agent Deliverables**:
- ✓ Task Model: Task SQLModel class with 6 fields + Pydantic validators (src/models/task.py)
- ✓ Validators: validate_title(), validate_user_id() (src/lib/validators.py)
- ✓ Service: TaskService with create_task(), get_tasks_for_user() (src/services/task_service.py)
- ✓ CLI: main.py group + add.py command wired together (src/cli/main.py, src/cli/commands/add.py)
- ✓ All 23 Tests PASS: 7 model + 8 validators + 3 service + 5 integration = 23/23 green

**Human Review**:
1. Run `pytest tests/unit/test_task_model.py -v` → Verify 7/7 PASS
2. Run `pytest tests/unit/test_validators.py -v` → Verify 8/8 PASS
3. Run `pytest tests/unit/test_task_service.py -v` → Verify 3/3 PASS
4. Run `pytest tests/integration/ -v` → Verify 5/5 PASS
5. Run `pytest tests/ -v` → Verify **25/25 PASS** (23 US1 + 2 foundational)
6. Run `uv sync && todo add --user alice "Buy groceries"` → Verify success message with task ID
7. Run `sqlite3 todo.db "SELECT * FROM task"` → Verify task persisted with all 6 fields

**Human Approval Required**: "User Story 1 complete and verified! Committing." → `git commit -m "feat(US1): implement task creation with validation"`

**Next Command**: "Proceed to Phase 3 Final Verification"

**Estimated Time**: 3 hours

---

### Integration Verification for User Story 1

- [X] **T056** [US1] Run all User Story 1 tests and verify 100% pass
  - **Command**: `pytest tests/unit/test_task_model.py tests/unit/test_validators.py tests/unit/test_task_service.py tests/integration/test_add_task_integration.py tests/unit/test_cli_main.py -v`
  - **Spec**: TDD verification (green phase), Constitutional Principle X (testing)
  - **Acceptance**: All 23 tests PASS (0 failures, 0 errors)
  - **Time**: 5 minutes

- [X] **T057** [US1] Verify coverage ≥80% for User Story 1
  - **Command**: `pytest --cov=src --cov-report=term-missing --cov-report=html`
  - **Spec**: Constitutional Principle X (≥80% coverage target), SC-002 (quality)
  - **Acceptance**: Coverage report shows ≥80% for src/models/task.py, src/lib/validators.py, src/services/task_service.py, src/cli/
  - **Time**: 10 minutes

- [X] **T058** [US1] Verify all US-1 acceptance scenarios pass manually
  - **Tests**:
    - US-1.AC-1: `todo add --user alice "Buy groceries"` → Success message with ID
    - US-1.AC-2: Create task, restart app, verify task persists
    - US-1.AC-3: `todo add --user alice "Call dentist at 2pm tomorrow"` (50 chars) → Success
    - US-1.AC-4: Create 10 tasks, verify 11th gets ID=11
  - **Spec**: US-1 acceptance scenarios (spec lines 18-23)
  - **Acceptance**: All 4 scenarios produce expected results
  - **Time**: 15 minutes

### 🚦 CHECKPOINT 3C: User Story 1 FULLY COMPLETE

**Agent Deliverables**:
- ✓ Automated Tests: 23/23 PASS (100% pass rate)
- ✓ Coverage: ≥80% for all User Story 1 code
- ✓ Acceptance Scenarios: 4/4 validated manually (US-1.AC-1 through AC-4)
- ✓ MVP Functional: Users can create tasks with `todo add --user <id> <title>`

**Human Review**:
1. Run `pytest tests/ --cov=src --cov-report=html` → Open htmlcov/index.html, verify ≥80% coverage
2. Manual test: `todo add --user alice "Buy groceries"` → Verify success
3. Manual test: Close terminal, reopen, `sqlite3 todo.db "SELECT * FROM task"` → Verify task persists
4. Manual test: Create 10 tasks, verify 11th gets ID=11

**Human Approval Required**: "User Story 1 VERIFIED! This is a deployable MVP." → `git commit -m "test(US1): verify coverage and acceptance scenarios"`

**🎯 Deployment Decision Point**: You now have a working MVP. Options:
- **Option A**: Deploy User Story 1 now (users can create tasks!)
- **Option B**: Continue to User Story 2 (add error handling)
- **Option C**: Continue to User Story 3 (add user isolation verification)

**Next Command**: "Proceed to Phase 4: User Story 2" (or deploy MVP)

**Estimated Time**: 30 minutes

**Phase 3 Total Time**: ~9 hours (4h tests + 3h implementation + 30m verification + 1.5h TDD overhead)

---

## Phase 4: User Story 2 - Input Validation and Error Handling (Priority: P1) 🎯 MVP

**Goal**: Users receive clear error messages when providing invalid input (empty title, too long title, missing --user flag, empty user_id)

**Why This Priority**: P1 (MVP) - Data integrity and UX are critical from day one. Without validation, system could store invalid data (spec lines 30-32)

**Spec Traceability**: US-2, FR-002, FR-003, FR-009, FR-010, SC-002

**Independent Test**: Run `todo add --user alice ""` and verify error "Title cannot be empty" with exit code 1 (US-2 Independent Test)

**Note**: Most validation logic already exists from User Story 1 (Pydantic validators in Task model, validate_title, validate_user_id). This story focuses on CLI error message presentation and exit codes.

### Tests for User Story 2 (TDD - Write FIRST, ensure they FAIL)

#### Integration Tests - Error Handling (4 tests)

- [X] **T059** [P] [US2] Write test_add_empty_title()
  - **File**: `tests/integration/test_add_task_integration.py`
  - **Test**: Invoke `todo add --user alice ""`, verify error message "Title cannot be empty" and exit code 1
  - **Spec**: US-2.AC-1 (empty title error), FR-009 (clear error messages), FR-010 (exit code 1)
  - **Acceptance**: Run test and verify it PASSES (validation already implemented in US1)
  - **Time**: 15 minutes

- [X] **T060** [P] [US2] Write test_add_title_too_long()
  - **File**: `tests/integration/test_add_task_integration.py`
  - **Test**: Invoke `todo add --user alice` with 201-char title, verify error "Title must be 1-200 characters" and exit code 1
  - **Spec**: US-2.AC-2 (title too long), FR-002, FR-009, FR-010
  - **Acceptance**: Run test and verify it PASSES (validation already implemented)
  - **Time**: 15 minutes

- [X] **T061** [P] [US2] Write test_add_missing_user()
  - **File**: `tests/integration/test_add_task_integration.py`
  - **Test**: Invoke `todo add "Buy milk"` (no --user flag), verify error "Error: Missing option '--user'" and exit code 2
  - **Spec**: US-2.AC-3 (missing --user), FR-010 (exit code 2 for missing option)
  - **Acceptance**: Run test and verify it PASSES (Click framework handles this automatically)
  - **Time**: 15 minutes

- [X] **T062** [P] [US2] Write test_add_empty_user_id()
  - **File**: `tests/integration/test_add_task_integration.py`
  - **Test**: Invoke `todo add --user "" "Buy milk"`, verify error "User ID cannot be empty" and exit code 1
  - **Spec**: US-2.AC-4 (empty user_id), FR-003, FR-009, FR-010
  - **Acceptance**: Run test and verify it PASSES (validation already implemented)
  - **Time**: 15 minutes

### 🚦 CHECKPOINT 4A: User Story 2 Tests Complete

**Agent Deliverables**:
- ✓ Test File Extended: 4 new error scenario tests added to test_add_task_integration.py
- ✓ All Tests PASS: 4/4 green (validation logic already exists from US1)

**Human Review**:
1. Run `pytest tests/integration/test_add_task_integration.py -k "empty_title or too_long or missing_user or empty_user_id" -v` → Verify 4/4 PASS

**Human Approval Required**: "Error handling tests pass! Validation already working from US1." → `git commit -m "test(US2): add 4 error handling integration tests"`

**Next Command**: "Proceed to User Story 2 Verification"

**Estimated Time**: 1 hour

---

### Implementation for User Story 2

- [X] **T063** [US2] Verify error messages in add command match spec exactly
  - **File**: `src/cli/commands/add.py`
  - **Review**: Ensure ValueError messages are "Title cannot be empty", "Title must be 1-200 characters", "User ID cannot be empty" (exact matches to spec)
  - **Spec**: FR-009 (clear error messages), US-2 acceptance scenarios
  - **Acceptance**: Run `pytest tests/integration/ -k "empty_title or too_long or empty_user_id" -v` and verify error messages match spec exactly
  - **Time**: 10 minutes

### Integration Verification for User Story 2

- [X] **T064** [US2] Run all User Story 2 tests and verify 100% pass
  - **Command**: `pytest tests/integration/test_add_task_integration.py -k "empty_title or too_long or missing_user or empty_user_id" -v`
  - **Spec**: US-2 verification, TDD green phase
  - **Acceptance**: All 4 tests PASS (0 failures)
  - **Time**: 5 minutes

- [X] **T065** [US2] Verify all US-2 acceptance scenarios pass manually
  - **Tests**:
    - US-2.AC-1: `todo add --user alice ""` → Error "Title cannot be empty", exit code 1
    - US-2.AC-2: `todo add --user alice` with 201-char title → Error "Title must be 1-200 characters", exit code 1
    - US-2.AC-3: `todo add "Buy milk"` (no --user) → Error "Missing option '--user'", exit code 2
    - US-2.AC-4: `todo add --user "" "Buy milk"` → Error "User ID cannot be empty", exit code 1
  - **Spec**: US-2 acceptance scenarios (spec lines 35-40)
  - **Acceptance**: All 4 scenarios produce expected errors and exit codes
  - **Time**: 15 minutes

### 🚦 CHECKPOINT 4B: User Story 2 FULLY COMPLETE

**Agent Deliverables**:
- ✓ Automated Tests: 4/4 PASS (error handling scenarios)
- ✓ Acceptance Scenarios: 4/4 validated manually (US-2.AC-1 through AC-4)
- ✓ Error Messages: All match spec exactly
- ✓ Exit Codes: 0 (success), 1 (validation error), 2 (missing option) - all correct

**Human Review**:
1. Run `pytest tests/ -v` → Verify **29/29 PASS** (25 from US1 + 4 from US2)
2. Manual test: `todo add --user alice ""` → Verify error message and exit code 1
3. Manual test: `todo add "Buy milk"` → Verify "Missing option '--user'" and exit code 2

**Human Approval Required**: "User Story 2 verified! Error handling complete." → `git commit -m "feat(US2): verify error handling and exit codes"`

**Next Command**: "Proceed to Phase 5: User Story 3"

**Estimated Time**: 30 minutes

**Phase 4 Total Time**: ~1.5 hours

---

## Phase 5: User Story 3 - User Data Isolation (Priority: P1) 🎯 MVP

**Goal**: Users only see their own tasks - alice's tasks are invisible to bob, and vice versa

**Why This Priority**: P1 (MVP) - Security and data privacy are non-negotiable (Constitutional Principle II). User isolation must be built from the start (spec lines 48-49)

**Spec Traceability**: US-3, FR-007, Constitutional Principle II, SC-004

**Independent Test**: Create tasks for alice and bob, then verify alice only sees alice's tasks when querying (US-3 Independent Test)

**Note**: User isolation is already implemented in User Story 1 (TaskService.create_task sets user_id, get_tasks_for_user filters by user_id, Task model has indexed user_id field). This story focuses on testing and verification.

### Tests for User Story 3 (TDD - Write FIRST, ensure they FAIL)

#### Unit Tests - User Isolation (2 tests)

- [X] **T066** [P] [US3] Write test_user_isolation()
  - **File**: `tests/unit/test_task_service.py`
  - **Test**: Alice creates "Alice's task", Bob creates "Bob's task", call get_tasks_for_user("alice"), verify returns only Alice's task (not Bob's)
  - **Spec**: US-3.AC-1 (user sees only own tasks), FR-007 (filter by user_id), SC-004 (zero data leakage)
  - **Acceptance**: Run test and verify it PASSES (isolation already implemented in US1)
  - **Time**: 20 minutes

- [X] **T067** [P] [US3] Write test_user_id_filter_enforcement()
  - **File**: `tests/unit/test_task_service.py`
  - **Test**: Create tasks for alice, bob, charlie. Call get_tasks_for_user("alice"), verify count matches alice's task count only
  - **Spec**: US-3.AC-3 (filter by user_id), FR-007
  - **Acceptance**: Run test and verify it PASSES (filtering already implemented)
  - **Time**: 20 minutes

#### Integration Tests - Cross-User Access (1 test)

- [X] **T068** [P] [US3] Write test_cross_user_isolation()
  - **File**: `tests/integration/test_add_task_integration.py`
  - **Test**: Invoke `todo add --user alice "Alice task"` and `todo add --user bob "Bob task"`, verify database has 2 tasks with correct user_id values
  - **Spec**: US-3.AC-2 (task created with correct user_id), Constitutional Principle II (user isolation)
  - **Acceptance**: Run test and verify it PASSES (user_id assignment already implemented)
  - **Time**: 20 minutes

### 🚦 CHECKPOINT 5A: User Story 3 Tests Complete

**Agent Deliverables**:
- ✓ Test Files Extended: 2 tests in test_task_service.py + 1 test in test_add_task_integration.py
- ✓ All Tests PASS: 3/3 green (user isolation already implemented in US1)

**Human Review**:
1. Run `pytest tests/unit/test_task_service.py -k user_isolation -v` → Verify 2/2 PASS
2. Run `pytest tests/integration/test_add_task_integration.py -k cross_user -v` → Verify 1/1 PASS

**Human Approval Required**: "User isolation tests pass! Security model verified." → `git commit -m "test(US3): add 3 user isolation verification tests"`

**Next Command**: "Proceed to User Story 3 Verification"

**Estimated Time**: 1 hour

---

### Implementation for User Story 3

**Note**: No new implementation needed - User Story 1 already implements all user isolation logic. This phase verifies implementation meets security requirements.

- [X] **T069** [US3] Verify user_id index exists and query filtering works
  - **Files**: Review `src/models/task.py` (user_id field has `index=True`), `src/services/task_service.py` (get_tasks_for_user uses `WHERE user_id = ?`)
  - **Spec**: FR-007 (user_id filtering), US-3.AC-3 (database filters by user_id), Constitutional Principle II (user isolation)
  - **Acceptance**: Run `sqlite3 todo.db ".schema task"` and verify `CREATE INDEX ix_task_user_id ON task (user_id)` exists. Review code confirms all queries filter by user_id.
  - **Time**: 15 minutes

- [X] **T070** [US3] Add security-critical docstrings emphasizing user isolation
  - **Files**: `src/services/task_service.py`, `src/models/task.py`
  - **Docstrings**: Add "SECURITY CRITICAL: ALL queries MUST filter by user_id (Constitutional Principle II)" to TaskService methods
  - **Spec**: Constitutional Principle II (user isolation as non-negotiable), SC-004 (zero data leakage)
  - **Acceptance**: Run `grep -r "SECURITY CRITICAL" src/` and verify docstrings added
  - **Time**: 10 minutes

### Integration Verification for User Story 3

- [X] **T071** [US3] Run all User Story 3 tests and verify 100% pass
  - **Command**: `pytest tests/unit/test_task_service.py -k user_isolation tests/integration/test_add_task_integration.py -k cross_user -v`
  - **Spec**: US-3 verification, Constitutional Principle II
  - **Acceptance**: All 3 tests PASS (0 failures)
  - **Time**: 5 minutes

- [X] **T072** [US3] Verify all US-3 acceptance scenarios pass manually
  - **Tests**:
    - US-3.AC-1: Create "Alice's task" for alice, "Bob's task" for bob. Query database for alice's tasks only → See only Alice's task
    - US-3.AC-2: `todo add --user alice "Personal task"` → Verify task.user_id="alice" in database
    - US-3.AC-3: Create tasks for alice, bob, charlie. Query for alice → Returns only alice's tasks
  - **Spec**: US-3 acceptance scenarios (spec lines 52-56)
  - **Acceptance**: All 3 scenarios produce expected isolation (alice sees only alice's tasks, bob sees only bob's)
  - **Time**: 15 minutes

### 🚦 CHECKPOINT 5B: User Story 3 FULLY COMPLETE

**Agent Deliverables**:
- ✓ Automated Tests: 3/3 PASS (user isolation verified)
- ✓ Acceptance Scenarios: 3/3 validated manually (US-3.AC-1 through AC-3)
- ✓ Security Verification: user_id index exists, ALL queries filter by user_id
- ✓ Documentation: SECURITY CRITICAL docstrings added

**Human Review**:
1. Run `pytest tests/ -v` → Verify **32/32 PASS** (25 US1 + 4 US2 + 3 US3)
2. Manual test: Create tasks for alice and bob, query database → Verify each user sees only their tasks
3. Run `sqlite3 todo.db ".schema task"` → Verify user_id index exists

**Human Approval Required**: "User Story 3 verified! User isolation secure." → `git commit -m "feat(US3): verify user isolation and security"`

**🎉 ALL USER STORIES COMPLETE**: You now have a fully functional MVP with:
- ✅ User Story 1: Task creation with validation
- ✅ User Story 2: Clear error messages for invalid input
- ✅ User Story 3: User data isolation and security

**Next Command**: "Proceed to Phase 6: Polish & Final Validation"

**Estimated Time**: 45 minutes

**Phase 5 Total Time**: ~2 hours

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and validations across all user stories to ensure production readiness

**Why This Phase**: Quality gates ensure the MVP meets all success criteria (SC-001 through SC-006) and constitutional principles before deployment

### Tasks

- [ ] **T073** [P] Run full test suite and verify ≥80% coverage
  - **Command**: `pytest --cov=src --cov-report=html --cov-report=term-missing`
  - **Spec**: Constitutional Principle X (≥80% coverage target), SC-002 (quality)
  - **Acceptance**: Coverage report shows ≥80% overall. All 32 tests PASS. Open htmlcov/index.html to inspect line-by-line coverage.
  - **Time**: 10 minutes

- [ ] **T074** [P] Run linters and formatters
  - **Commands**: `black src/ tests/`, `mypy src/`, `pydocstyle src/`
  - **Spec**: Constitutional Principle X (code quality standards)
  - **Acceptance**: Black formats code with 0 changes needed. Mypy reports 0 errors. Pydocstyle reports 0 violations.
  - **Time**: 15 minutes

- [ ] **T075** [P] Create acceptance scenario mapping checklist
  - **File**: `specs/001-add-task/acceptance-checklist.md`
  - **Content**: Map all 12 acceptance scenarios (US-1: 4, US-2: 4, US-3: 3) to specific test functions
  - **Spec**: Traceability (lineage from spec → tasks → tests), SC-002 (100% validation coverage)
  - **Acceptance**: Run `cat acceptance-checklist.md` and verify all 12 scenarios mapped to tests
  - **Time**: 20 minutes

- [ ] **T076** [P] Verify all spec acceptance scenarios pass
  - **Manual Tests**: Run through all 12 acceptance scenarios from spec.md manually
  - **Spec**: US-1 (4 scenarios), US-2 (4 scenarios), US-3 (3 scenarios), SC-002 (100% validation)
  - **Acceptance**: Document results in acceptance-checklist.md with ✅ for each scenario
  - **Time**: 30 minutes

- [ ] **T077** [P] Verify performance target (p95 <100ms)
  - **Method**: Manual timing or pytest-benchmark - create 100 tasks, measure p95 latency
  - **Spec**: SC-005 (p95 <100ms for task creation), Constitutional Principle XVIII (Phase I performance)
  - **Acceptance**: p95 latency <100ms documented in performance-results.txt
  - **Time**: 20 minutes

- [ ] **T078** [P] Verify type hints coverage
  - **Command**: `mypy src/ --strict`
  - **Spec**: Constitutional Principle X (code quality - type safety)
  - **Acceptance**: Mypy --strict reports 0 errors (all functions have type hints)
  - **Time**: 15 minutes

- [ ] **T079** [P] Test quickstart.md examples manually
  - **Tests**: Follow quickstart.md installation and basic usage examples step-by-step
  - **Spec**: Documentation accuracy, user onboarding
  - **Acceptance**: All examples in quickstart.md work exactly as documented (no errors)
  - **Time**: 20 minutes

- [ ] **T080** Final integration smoke test
  - **Test**: Create 10 tasks for 3 users (alice, bob, charlie), verify isolation and persistence
  - **Spec**: SC-003 (persistence), SC-004 (isolation), SC-006 (concurrent creation)
  - **Acceptance**: All 30 tasks created, each user sees only their 10 tasks, database contains 30 rows
  - **Time**: 15 minutes

### 🚦 CHECKPOINT 6: Polish & Final Validation Complete

**Agent Deliverables**:
- ✓ Test Coverage: ≥80% verified with HTML report
- ✓ Code Quality: Black, mypy --strict, pydocstyle all pass
- ✓ Acceptance Mapping: 12/12 scenarios mapped to tests in checklist
- ✓ Performance: p95 <100ms verified and documented
- ✓ Documentation: quickstart.md examples validated
- ✓ Smoke Test: 30 tasks across 3 users - isolation and persistence verified

**Human Review**:
1. Run `pytest --cov=src --cov-report=html` → Open htmlcov/index.html, verify ≥80%
2. Run `black src/ tests/ && mypy src/ --strict && pydocstyle src/` → Verify all pass
3. Run `cat specs/001-add-task/acceptance-checklist.md` → Verify 12/12 scenarios ✅
4. Run smoke test: Create 30 tasks for 3 users → Verify isolation works

**Human Approval Required**: "All quality gates passed! MVP ready for deployment." → `git commit -m "chore: final polish and validation"`

**🚀 DEPLOYMENT READY**: All success criteria met:
- ✅ SC-001: Task creation <3 seconds
- ✅ SC-002: 100% invalid input rejection
- ✅ SC-003: 100% persistence (verified with restart tests)
- ✅ SC-004: 100% user isolation (zero data leakage)
- ✅ SC-005: p95 <100ms
- ✅ SC-006: Concurrent creation works (smoke test)

**Next Command**: Tag release and deploy: `git tag v0.1.0-mvp && git push origin 001-add-task --tags`

**Estimated Time**: 2.5 hours

**Phase 6 Total Time**: ~2.5 hours

---

## Total Estimated Timeline

### Sequential Execution (1 Developer)

| Phase | Tasks | Time | Cumulative |
|-------|-------|------|------------|
| Phase 1: Setup | 10 tasks | 1.5h | 1.5h |
| Phase 2: Foundational | 9 tasks | 2h | 3.5h |
| Phase 3: User Story 1 | 39 tasks | 9h | 12.5h |
| Phase 4: User Story 2 | 7 tasks | 1.5h | 14h |
| Phase 5: User Story 3 | 8 tasks | 2h | 16h |
| Phase 6: Polish | 8 tasks | 2.5h | **18.5h** |

**Total: ~18.5 hours (~3 workdays at 6 hours/day)**

### Parallel Execution (3 Developers)

| Phase | Parallelism | Time | Cumulative |
|-------|-------------|------|------------|
| Phase 1: Setup | Together | 1.5h | 1.5h |
| Phase 2: Foundational | Together | 2h | 3.5h |
| **User Stories (Parallel)** |
| - Dev A: User Story 1 | Parallel | 9h | |
| - Dev B: User Story 2 | Parallel | 1.5h | |
| - Dev C: User Story 3 | Parallel | 2h | |
| Stories Complete | Longest path (US1) | | 12.5h |
| Phase 6: Polish | Together | 2.5h | **15h** |

**Total: ~15 hours (~2.5 workdays with 3 developers)**

---

## Implementation Strategy Options

### MVP First (User Story 1 Only) - FASTEST PATH TO VALUE

1. ✅ Phase 1: Setup → Project ready (1.5h)
2. ✅ Phase 2: Foundational (CRITICAL) → Database ready (2h)
3. ✅ Phase 3: User Story 1 → MVP functional (9h)
4. ✅ Verify independently (T056-T058) → Quality assured (30m)
5. 🚀 **DEPLOY MVP** → Users can create tasks!

**Total: ~13 hours → Working todo app deployed**

**Value Delivered**: Users can create and persist tasks with validation

**What's Missing**: Error message refinement (US2), explicit user isolation verification (US3)

---

### Incremental Delivery (Add Stories Sequentially) - RECOMMENDED

1. ✅ Setup + Foundational → Foundation ready (3.5h)
2. ✅ User Story 1 → Deploy MVP (9h + verify → **12.5h total**)
3. ✅ User Story 2 → Better UX (1.5h → **14h total**)
4. ✅ User Story 3 → Security verified (2h → **16h total**)
5. ✅ Polish → Production ready (2.5h → **18.5h total**)

**Checkpoints**: 5 deployment opportunities (after each phase)

**Value**: Each story adds value without breaking previous stories

---

### Parallel Team Strategy (3 Developers) - FASTEST COMPLETION

**Day 1 (6 hours)**:
- **Everyone Together**: Phase 1 Setup (1.5h) → Phase 2 Foundational (2h) → **3.5h checkpoint**
- **Split Work After Foundational**:
  - Dev A starts User Story 1 (9h total, completes ~2.5h on Day 1)
  - Dev B starts User Story 2 (1.5h total, completes Day 1)
  - Dev C starts User Story 3 (2h total, completes Day 1)

**Day 2 (6 hours)**:
- Dev A continues User Story 1 (6h, completes ~8.5h total by EOD)
- Dev B helps with User Story 1 or starts Polish prep
- Dev C helps with User Story 1 or starts Polish prep

**Day 3 (3 hours)**:
- Dev A finishes User Story 1 (0.5h)
- **Everyone Together**: Phase 6 Polish (2.5h) → **COMPLETE**

**Total: ~15 hours (~2.5 days)**

---

## Dependencies & Execution Order

### Critical Path

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundational) ← BLOCKS ALL USER STORIES
    ↓
    ├─→ User Story 1 (independent) ← LONGEST PATH (9h)
    ├─→ User Story 2 (reuses US1 validators)
    └─→ User Story 3 (reuses US1 service)
    ↓
Phase 6 (Polish)
```

### User Story Dependencies

- **User Story 1**: INDEPENDENT - Implements all foundational components
- **User Story 2**: SEMI-INDEPENDENT - Reuses US1 validators, tests error messages independently
- **User Story 3**: SEMI-INDEPENDENT - Reuses US1 service, tests user isolation independently

**Parallelization**: All 3 user stories CAN run in parallel after Foundational phase completes

### Within Each Phase

**TDD Workflow (MUST FOLLOW)**:
1. Write tests FIRST (red phase - tests fail)
2. Run tests and verify FAILURE
3. Implement minimal code (green phase)
4. Run tests and verify SUCCESS
5. Refactor if needed (keep tests green)

**Checkpoint Pattern (MUST FOLLOW)**:
1. Agent completes phase, announces deliverables
2. Human reviews artifacts (run tests, check files)
3. Human approves: "Looks good! Committing."
4. Human commits: `git commit -m "phase: description"`
5. Human continues: "Proceed to next phase"

---

## Parallel Opportunities

### Phase 1: Setup
- **Sequential**: T001-T005 (project structure, dependencies)
- **Parallel**: T006, T007, T008, T009 (3 tasks - config files)

### Phase 2: Foundational
- **Sequential**: T011-T017 (database infrastructure - dependencies exist)
- **Parallel**: T018, T019 (2 tasks - test infrastructure)

### Phase 3: User Story 1
- **Parallel**: T020-T042 (ALL 23 test tasks can run in parallel - different test files)
- **Sequential**: T043 (Task model) before T047-T049 (service needs model)
- **Parallel**: T044, T045 (2 validator tasks - different functions)
- **Sequential**: T051 (add command) before T052 (register command)

### Phase 4: User Story 2
- **Parallel**: T059-T062 (4 test tasks)

### Phase 5: User Story 3
- **Parallel**: T066-T068 (3 test tasks)

### Phase 6: Polish
- **Parallel**: T073-T079 (7 tasks - coverage, linting, mapping, performance, type hints, quickstart)
- **Sequential**: T080 (smoke test runs after all polish tasks)

---

## Quality Gates (Checkpoints)

### After Setup (Checkpoint 1)
- ✓ Directory structure exists
- ✓ Dependencies installed
- ✓ CLI entry point configured

### After Foundational (Checkpoint 2)
- ✓ Database initializes without errors
- ✓ Test infrastructure works
- ✓ 2 foundational tests PASS

### After User Story 1 Tests (Checkpoint 3A)
- ✓ 23 tests written
- ✓ All 23 tests FAIL (red phase)

### After User Story 1 Implementation (Checkpoint 3B)
- ✓ All 23 tests PASS (green phase)
- ✓ CLI command works manually

### After User Story 1 Verification (Checkpoint 3C)
- ✓ Coverage ≥80%
- ✓ 4 acceptance scenarios validated
- ✓ **DEPLOYABLE MVP**

### After User Story 2 (Checkpoint 4B)
- ✓ 4 error handling tests PASS
- ✓ Exit codes correct (0, 1, 2)

### After User Story 3 (Checkpoint 5B)
- ✓ 3 user isolation tests PASS
- ✓ Security verification complete

### After Polish (Checkpoint 6)
- ✓ All 32 tests PASS
- ✓ Coverage ≥80%
- ✓ All 12 acceptance scenarios ✅
- ✓ Performance target met
- ✓ **PRODUCTION READY**

---

## Notes & Best Practices

### Task Format
- [P] tasks = different files, no dependencies, can run in parallel
- [Story] label maps task to user story for traceability
- Spec Ref traces to FR-XXX, SC-XXX, US-X.AC-Y in spec.md
- Acceptance criterion = testable, verifiable completion proof

### TDD Discipline
- Write tests FIRST, ensure they FAIL
- Implement minimal code to make tests PASS
- Refactor while keeping tests green
- Never skip the red phase (proves test works)

### Checkpoint Discipline
- **NEVER PROCEED WITHOUT HUMAN APPROVAL**
- Agent announces deliverables
- Human reviews and approves
- Human commits to git
- Human says "proceed to next phase"

### Traceability
- Each task links to spec (FR-XXX, US-X.AC-Y)
- Tests reference acceptance scenarios
- Commits reference task IDs
- Acceptance checklist maps scenarios → tests

### Code Quality
- ≥80% coverage (Constitutional Principle X)
- Type hints on all functions (mypy --strict)
- Docstrings (pydocstyle)
- Formatted code (black)

### Avoid
- Skipping checkpoints (causes wasted work)
- Implementing before tests written (breaks TDD)
- Vague acceptance criteria (untestable)
- Cross-story dependencies that break parallelization
