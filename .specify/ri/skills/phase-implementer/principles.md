# Design Principles: Phase Implementer

**Version**: 1.0.0
**Created**: 2025-12-12
**Last Updated**: 2025-12-12

---

## Purpose

These principles guide **implementation decision-making** when writing code. They ensure:
- Constitutional compliance (all 28 principles enforced in code)
- Test-driven development (TDD: red-green-refactor)
- Code quality (type-safe, documented, maintainable)
- Security-first (user isolation, input validation)
- Performance-aware (meet SLOs, optimize only when needed)

---

## 1. Test-Driven Development (TDD) Principles

### 1.1 Red-Green-Refactor Standard (MANDATORY)
**Principle**: ALWAYS write test first, then implement, then refactor.

**TDD Cycle**:
```
1. RED: Write failing test (verify it fails for the right reason)
2. GREEN: Write minimum code to pass (don't over-engineer)
3. REFACTOR: Improve code quality (DRY, SOLID, extract functions)
4. REPEAT: Next test scenario
```

**Verification**:
- ✅ Every feature has test written BEFORE implementation
- ✅ Test fails initially (red) for correct reason (not typo, not import error)
- ✅ Test passes after implementation (green)
- ✅ Tests still pass after refactoring

**Example**:
```python
# STEP 1: RED (Write Failing Test)
def test_create_task_with_valid_title():
    """Test creating task with valid title."""
    task = create_task(user_id="alice", title="Buy milk")
    assert task.title == "Buy milk"
    # Run test → FAILS (create_task doesn't exist)

# STEP 2: GREEN (Minimum Implementation)
def create_task(user_id: str, title: str) -> Task:
    return Task(user_id=user_id, title=title)
    # Run test → PASSES

# STEP 3: REFACTOR (Add Validation, Docstrings)
def create_task(user_id: str, title: str) -> Task:
    """Create a new task with validation.

    Args:
        user_id: User ID (not empty)
        title: Task title (1-200 chars)

    Returns:
        Task: Created task

    Raises:
        ValidationError: If title invalid
    """
    _validate_user_id(user_id)
    _validate_title(title)
    return Task(user_id=user_id, title=title)
    # Run test → STILL PASSES
```

### 1.2 Test Coverage Standard (≥80% MANDATORY)
**Principle**: Code coverage must meet or exceed 80% per Constitutional Principle X.

**Coverage Categories**:
- **Happy Path**: Normal usage scenarios
- **Edge Cases**: Boundary conditions (empty, max length, special chars)
- **Error Conditions**: Invalid inputs, exceptions
- **User Isolation**: Cross-user access attempts (SECURITY CRITICAL)
- **Integration**: End-to-end flows

**Coverage Command**:
```bash
pytest tests/ --cov=backend --cov-report=term-missing --cov-fail-under=80
```

**Verification**:
- ✅ Coverage report shows ≥80%
- ✅ All critical paths covered (user isolation, validation, error handling)
- ✅ No untested branches (if/else, try/except)

### 1.3 Test Quality Standard
**Principle**: Tests must be fast, isolated, deterministic, and readable.

**FIRST Principles**:
- **Fast**: <1s per test, <10s for full suite
- **Isolated**: No shared state between tests (independent execution)
- **Repeatable**: Same result every time (no randomness, no external dependencies)
- **Self-Validating**: Clear pass/fail (no manual inspection)
- **Timely**: Written before implementation (TDD)

**Bad Test Example**:
```python
# ❌ BAD: Slow, not isolated, not repeatable
def test_create_task():
    # Slow: Sleeps for 5 seconds
    time.sleep(5)

    # Not isolated: Depends on test_add_user() running first
    user = get_user("alice")  # Assumes alice exists

    # Not repeatable: Uses current time (changes every run)
    task = create_task(user.id, f"Task at {datetime.now()}")

    # Not self-validating: Requires manual DB check
    print(f"Task created: {task.id}")  # No assert!
```

**Good Test Example**:
```python
# ✅ GOOD: Fast, isolated, repeatable, self-validating
def test_create_task(test_db):
    """Test creating task with valid inputs."""
    # Fast: No sleeps, in-memory DB
    # Isolated: test_db fixture creates clean DB per test
    # Repeatable: Fixed inputs ("alice", "Buy milk")
    task = create_task(user_id="alice", title="Buy milk")

    # Self-validating: Clear assertions
    assert task.user_id == "alice"
    assert task.title == "Buy milk"
    assert task.completed is False
```

### 1.4 Test Organization Standard
**Principle**: Tests organized by layer and purpose.

**Directory Structure**:
```
tests/
├── conftest.py                 # Fixtures (test_db, sample_users)
├── unit/                       # Unit tests (test single function/class)
│   ├── test_task_service.py    # Service layer
│   ├── test_validators.py      # Validation logic
│   └── test_models.py          # SQLModel models
├── integration/                # Integration tests (test components together)
│   ├── test_cli.py             # CLI commands (Phase I)
│   ├── test_api.py             # API endpoints (Phase II)
│   └── test_database.py        # Database operations
└── e2e/                        # End-to-end tests (Phase II+)
    └── test_user_workflows.py  # Full user journeys
```

**Naming Convention**:
```python
# Pattern: test_<function_name>_<scenario>
def test_create_task_with_valid_title(): ...
def test_create_task_with_empty_title_fails(): ...
def test_create_task_with_long_title_fails(): ...
def test_create_task_enforces_user_isolation(): ...
```

---

## 2. Constitutional Compliance Principles

### 2.1 User Isolation Standard (Principle II - CRITICAL)
**Principle**: ALL database queries MUST filter by user_id. Cross-user access ALWAYS returns 404.

**Enforcement**:
```python
# ✅ CORRECT: User isolation enforced
def list_tasks(user_id: str) -> List[Task]:
    """List tasks for specific user."""
    return session.exec(
        select(Task).where(Task.user_id == user_id)
    ).all()

def get_task(user_id: str, task_id: int) -> Task:
    """Get task by ID for specific user."""
    task = session.exec(
        select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id  # CRITICAL: Both filters
        )
    ).first()

    if not task:
        # 404 (not 401/403 to avoid info disclosure)
        raise NotFoundError(f"Task {task_id} not found")

    return task

# ❌ SECURITY VIOLATION: No user_id filter
def list_tasks() -> List[Task]:
    return session.exec(select(Task)).all()  # Leaks all users' tasks!

def get_task(task_id: int) -> Task:
    return session.exec(
        select(Task).where(Task.id == task_id)  # Missing user_id filter!
    ).first()
```

**Required Tests**:
```python
def test_user_isolation_same_user_read(test_db):
    """Test alice can read own tasks."""
    alice_task = create_task("alice", "Alice's task")
    tasks = list_tasks("alice")
    assert alice_task in tasks

def test_user_isolation_cross_user_read(test_db):
    """Test alice cannot read bob's tasks."""
    bob_task = create_task("bob", "Bob's task")
    alice_tasks = list_tasks("alice")
    assert bob_task not in alice_tasks  # Empty, not error

def test_user_isolation_cross_user_update(test_db):
    """Test alice cannot update bob's task."""
    bob_task = create_task("bob", "Bob's task")
    with pytest.raises(NotFoundError):  # 404, not 403
        update_task("alice", bob_task.id, title="Hacked!")

def test_user_isolation_cross_user_delete(test_db):
    """Test alice cannot delete bob's task."""
    bob_task = create_task("bob", "Bob's task")
    with pytest.raises(NotFoundError):  # 404, not 403
        delete_task("alice", bob_task.id)
```

### 2.2 Type Safety Standard (Principle IX)
**Principle**: All functions have type hints. mypy --strict passes.

**Type Hint Requirements**:
```python
# ✅ CORRECT: Full type hints
def create_task(
    user_id: str,
    title: str,
    completed: bool = False
) -> Task:
    """Create task with type-safe params."""
    return Task(user_id=user_id, title=title, completed=completed)

# Use Optional for nullable
from typing import Optional

def get_task(user_id: str, task_id: int) -> Optional[Task]:
    """Get task or None if not found."""
    return session.exec(...).first()

# Use List, Dict for collections
from typing import List, Dict

def list_tasks(user_id: str) -> List[Task]:
    """Return list of tasks."""
    return session.exec(...).all()

def task_to_dict(task: Task) -> Dict[str, Any]:
    """Convert task to dictionary."""
    return {"id": task.id, "title": task.title}

# ❌ BAD: No type hints
def create_task(user_id, title, completed=False):  # Missing types!
    return Task(user_id=user_id, title=title, completed=completed)
```

**Mypy Validation**:
```bash
mypy backend/ --strict
# Must pass with 0 errors
```

### 2.3 Documentation Standard (Principle IX)
**Principle**: All functions have Google-style docstrings. Coverage ≥95%.

**Docstring Template**:
```python
def function_name(param1: Type1, param2: Type2) -> ReturnType:
    """One-line summary of what function does.

    Optional detailed description explaining complex logic, assumptions,
    or important context. Can span multiple lines.

    Args:
        param1: Description of param1 (what it is, constraints)
        param2: Description of param2

    Returns:
        ReturnType: Description of return value

    Raises:
        ExceptionType: When and why this exception is raised
        AnotherException: Another error condition

    Example:
        >>> result = function_name("value1", 42)
        >>> result.attribute
        'expected_value'

    Note:
        Additional context, warnings, or related functions.
    """
    # Implementation...
```

**Real Example**:
```python
def create_task(user_id: str, title: str) -> Task:
    """Create a new task for the specified user.

    Validates user_id and title before creating task. Task is created
    with completed=False by default.

    Args:
        user_id: The ID of the user creating the task. Must not be empty.
        title: The task title. Must be 1-200 characters.

    Returns:
        Task: The newly created task with assigned ID, timestamps populated.

    Raises:
        ValueError: If user_id is empty or None.
        ValidationError: If title is empty or exceeds 200 characters.

    Example:
        >>> task = create_task("alice", "Buy groceries")
        >>> task.title
        'Buy groceries'
        >>> task.user_id
        'alice'
        >>> task.completed
        False

    Note:
        This function commits to the database. Ensure you're in a
        transaction context if you need rollback capability.
    """
    _validate_user_id(user_id)
    _validate_title(title)

    task = Task(user_id=user_id, title=title, completed=False)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

### 2.4 Database Standards (Principle VI)
**Principle**: All models include constitutional required fields.

**Required Fields** (MANDATORY for all models):
```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    """Task model with constitutional required fields."""
    __tablename__ = "tasks"

    # REQUIRED (Constitutional Principle VI)
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, max_length=255)  # INDEXED for queries
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Task-specific fields
    title: str = Field(min_length=1, max_length=200)
    completed: bool = Field(default=False)

    # Auto-update updated_at on modification
    @validator('updated_at', always=True)
    def set_updated_at(cls, v):
        return datetime.utcnow()
```

**Validation**:
- ✅ Model has id (primary key)
- ✅ Model has user_id (indexed)
- ✅ Model has created_at (auto-populated)
- ✅ Model has updated_at (auto-updated)

---

## 3. Code Quality Principles

### 3.1 DRY (Don't Repeat Yourself) Standard
**Principle**: No duplicated code. Extract common logic to functions.

**Refactoring Pattern**:
```python
# ❌ BAD: Duplicated validation
def create_task(user_id, title):
    if not title or len(title) > 200:
        raise ValidationError("Title must be 1-200 characters")
    # ...

def update_task(task_id, title):
    if not title or len(title) > 200:  # DUPLICATED!
        raise ValidationError("Title must be 1-200 characters")
    # ...

# ✅ GOOD: Extracted validation
def _validate_title(title: str) -> None:
    """Validate title is 1-200 characters.

    Args:
        title: Title to validate

    Raises:
        ValidationError: If title is invalid
    """
    if not title:
        raise ValidationError("Title cannot be empty")
    if len(title) > 200:
        raise ValidationError("Title must be 1-200 characters")

def create_task(user_id, title):
    _validate_title(title)  # Reuse!
    # ...

def update_task(task_id, title):
    _validate_title(title)  # Reuse!
    # ...
```

### 3.2 SOLID Principles
**Principle**: Follow SOLID for maintainable code.

**S - Single Responsibility**:
```python
# ❌ BAD: Function does too much
def create_and_email_task(user_id, title, email):
    # Validate
    if not title:
        raise ValidationError(...)
    # Create
    task = Task(user_id=user_id, title=title)
    session.add(task)
    session.commit()
    # Email (DIFFERENT RESPONSIBILITY!)
    send_email(email, f"Task created: {title}")
    return task

# ✅ GOOD: Separate responsibilities
def create_task(user_id: str, title: str) -> Task:
    """Create task (single responsibility)."""
    _validate_title(title)
    task = Task(user_id=user_id, title=title)
    session.add(task)
    session.commit()
    return task

def notify_task_created(task: Task, email: str) -> None:
    """Send email notification (single responsibility)."""
    send_email(email, f"Task created: {task.title}")

# Usage
task = create_task("alice", "Buy milk")
notify_task_created(task, "alice@example.com")
```

**O - Open/Closed** (open for extension, closed for modification):
```python
# ✅ GOOD: Extend with subclasses/decorators, don't modify
class TaskFormatter:
    """Base formatter."""
    def format(self, task: Task) -> str:
        return f"{task.id}: {task.title}"

class VerboseTaskFormatter(TaskFormatter):
    """Extended formatter without modifying base."""
    def format(self, task: Task) -> str:
        return f"[{task.id}] {task.title} (completed: {task.completed})"
```

**D - Dependency Inversion** (depend on abstractions):
```python
# ✅ GOOD: Inject dependencies (easier to test, mock)
class TaskService:
    def __init__(self, session: Session):
        self.session = session  # Injected dependency

    def create_task(self, user_id: str, title: str) -> Task:
        task = Task(user_id=user_id, title=title)
        self.session.add(task)
        self.session.commit()
        return task

# Usage
service = TaskService(session=test_session)  # Inject test DB
task = service.create_task("alice", "Buy milk")
```

### 3.3 Code Complexity Standard
**Principle**: Keep functions simple. Cyclomatic complexity ≤10.

**Complexity Metrics**:
- **Lines per function**: ≤50 (ideally ≤20)
- **Nesting depth**: ≤3 levels
- **Cyclomatic complexity**: ≤10 (number of decision points)

**Refactoring Example**:
```python
# ❌ BAD: Complex nested logic (complexity = 8)
def process_task(user_id, task_id, action):
    task = get_task(task_id)
    if task:
        if task.user_id == user_id:
            if action == "complete":
                if not task.completed:
                    task.completed = True
                    return "completed"
                else:
                    return "already completed"
            elif action == "delete":
                session.delete(task)
                return "deleted"
        else:
            raise PermissionError(...)
    else:
        raise NotFoundError(...)

# ✅ GOOD: Early returns, extracted functions (complexity = 3)
def process_task(user_id, task_id, action):
    """Process task action."""
    task = _get_and_validate_task(user_id, task_id)

    if action == "complete":
        return _complete_task(task)
    elif action == "delete":
        return _delete_task(task)
    else:
        raise ValueError(f"Unknown action: {action}")

def _get_and_validate_task(user_id, task_id):
    """Get task and validate ownership."""
    task = get_task(task_id)
    if not task:
        raise NotFoundError(f"Task {task_id} not found")
    if task.user_id != user_id:
        raise NotFoundError(f"Task {task_id} not found")  # 404, not 403
    return task

def _complete_task(task):
    """Mark task as complete."""
    if task.completed:
        return "already completed"
    task.completed = True
    return "completed"

def _delete_task(task):
    """Delete task."""
    session.delete(task)
    return "deleted"
```

---

## 4. Performance Principles

### 4.1 SLO Compliance Standard
**Principle**: Code must meet performance SLOs from plan.md.

**Phase-Specific SLOs**:
```
Phase I (Console):
- CLI commands: p95 <100ms

Phase II (Web):
- API endpoints: p50 <100ms, p95 <500ms, p99 <1s

Phase V (Cloud):
- API endpoints: p50 <50ms, p95 <200ms, p99 <500ms
```

**Performance Measurement**:
```python
# Add timing to tests
import time

def test_list_tasks_performance(test_db, benchmark):
    """Test list_tasks meets p95 <100ms SLO."""
    # Setup: Create 100 tasks
    for i in range(100):
        create_task("alice", f"Task {i}")

    # Benchmark
    result = benchmark(list_tasks, "alice")

    # Assertion: p95 latency <100ms
    assert benchmark.stats.stats.mean < 0.1  # 100ms
```

### 4.2 Database Optimization Standard
**Principle**: Use indexes, avoid N+1 queries, batch operations.

**Required Optimizations**:
```python
# ✅ GOOD: Query uses index (user_id indexed)
def list_tasks(user_id: str) -> List[Task]:
    return session.exec(
        select(Task).where(Task.user_id == user_id)
    ).all()  # Uses idx_tasks_user_id index

# ✅ GOOD: Eager loading (avoid N+1)
def list_tasks_with_tags(user_id: str) -> List[Task]:
    return session.exec(
        select(Task)
        .options(selectinload(Task.tags))  # Eager load tags
        .where(Task.user_id == user_id)
    ).all()  # 1 query for tasks + 1 query for tags (not N queries)

# ✅ GOOD: Batch operations
def mark_multiple_complete(user_id: str, task_ids: List[int]) -> None:
    session.exec(
        update(Task)
        .where(Task.user_id == user_id, Task.id.in_(task_ids))
        .values(completed=True)
    )  # 1 query (not N queries)
    session.commit()

# ❌ BAD: N+1 query problem
def list_tasks_with_tags_bad(user_id: str) -> List[Dict]:
    tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
    result = []
    for task in tasks:  # N queries!
        tags = session.exec(select(Tag).where(Tag.task_id == task.id)).all()
        result.append({"task": task, "tags": tags})
    return result
```

### 4.3 Async Optimization Standard (Phase II+)
**Principle**: Use async for I/O-bound operations (database, external APIs).

**Async Pattern**:
```python
# Phase II: FastAPI with async
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

@app.post("/api/{user_id}/tasks")
async def create_task_route(
    user_id: str,
    task_data: TaskCreate,
    session: AsyncSession = Depends(get_async_session)
) -> Task:
    """Async route for task creation."""
    task = Task(user_id=user_id, **task_data.dict())
    session.add(task)
    await session.commit()  # Async commit
    await session.refresh(task)
    return task
```

### 4.4 Premature Optimization Standard
**Principle**: Optimize ONLY if SLO violated. Measure first.

**Optimization Workflow**:
```
1. Implement simple solution
2. Measure performance (profiling, APM)
3. Check if SLO violated (p95 latency, throughput)
4. If SLO met → STOP (don't optimize)
5. If SLO violated → Profile bottleneck → Optimize → Re-measure
```

**Example**:
```python
# Step 1: Simple implementation
def list_tasks(user_id: str) -> List[Task]:
    return session.exec(
        select(Task).where(Task.user_id == user_id)
    ).all()

# Step 2: Measure → p95 latency = 450ms (meets Phase II SLO <500ms)
# Step 3: SLO met → DONE (no optimization needed)

# Alternative: If p95 = 600ms (violates SLO)
# Step 4: Profile → Bottleneck: No index on user_id
# Step 5: Add index → CREATE INDEX idx_user_id ON tasks (user_id);
# Step 6: Re-measure → p95 = 80ms ✅
```

---

## 5. Security Principles

### 5.1 Input Validation Standard
**Principle**: Validate ALL user inputs server-side. Never trust client.

**Validation Layers**:
```python
# Layer 1: Pydantic schema validation (FastAPI)
from pydantic import BaseModel, Field, validator

class TaskCreate(BaseModel):
    """Request schema for task creation."""
    title: str = Field(min_length=1, max_length=200)

    @validator('title')
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()

# Layer 2: Business logic validation
def create_task(user_id: str, title: str) -> Task:
    """Create task with additional validation."""
    _validate_user_id(user_id)  # Not empty
    _validate_title(title)  # 1-200 chars, no SQL injection

    task = Task(user_id=user_id, title=title)
    session.add(task)
    session.commit()
    return task

# Layer 3: Database constraints (SQLModel)
class Task(SQLModel, table=True):
    title: str = Field(
        min_length=1,
        max_length=200,
        regex="^[a-zA-Z0-9\\s\\-_.,!?()]+$"  # Allowed chars
    )
```

### 5.2 No Secrets in Code Standard
**Principle**: Never hardcode secrets. Use environment variables.

**Good Practice**:
```python
# ✅ GOOD: Secrets from environment
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
JWT_SECRET = os.getenv("JWT_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# .env file (NOT committed to git)
# DATABASE_URL=postgresql://user:pass@localhost/db
# JWT_SECRET=randomly_generated_secret_key
# OPENAI_API_KEY=sk-...

# ❌ BAD: Hardcoded secrets
DATABASE_URL = "postgresql://admin:password123@prod-db.com/mydb"  # LEAKED!
JWT_SECRET = "my_secret_key"  # INSECURE!
```

### 5.3 SQL Injection Prevention Standard
**Principle**: Use ORM (SQLModel) for ALL queries. Never raw SQL with user input.

**Safe Practice**:
```python
# ✅ GOOD: ORM with parameterized queries
def list_tasks_by_title(user_id: str, title_pattern: str) -> List[Task]:
    return session.exec(
        select(Task).where(
            Task.user_id == user_id,
            Task.title.contains(title_pattern)  # Parameterized
        )
    ).all()

# ❌ BAD: Raw SQL with string formatting (SQL injection!)
def list_tasks_by_title_bad(user_id: str, title_pattern: str) -> List[Task]:
    query = f"SELECT * FROM tasks WHERE user_id = '{user_id}' AND title LIKE '%{title_pattern}%'"
    return session.exec(query).all()  # VULNERABLE!
    # Attack: title_pattern = "'; DROP TABLE tasks; --"
```

---

## 6. Git Commit Standards

### 6.1 Conventional Commits Standard
**Principle**: Use conventional commit format for all commits.

**Format**:
```
<type>: <description>

<optional body>

<optional footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting, no logic change)
- `refactor`: Code change (no feature, no bug fix)
- `test`: Adding/updating tests
- `chore`: Build, dependencies, tooling

**Example**:
```bash
git commit -m "feat: add task creation with user isolation

- Implement create_task() service function
- Add CLI 'add' command with --user flag
- Validate title (1-200 chars) and user_id (not empty)
- Add 5 tests (happy path, edge cases, user isolation)
- Coverage: 92% on task_service.py

Closes: Task 1 from specs/task-management/tasks.md

🤖 Generated with [Claude Code](https://claude.com/claude-code)
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

### 6.2 Atomic Commits Standard
**Principle**: One logical change per commit. Small, focused commits.

**Good Practice**:
```
Commit 1: "feat: add Task model with constitutional fields"
Commit 2: "feat: add create_task service function"
Commit 3: "feat: add CLI 'add' command"
Commit 4: "test: add user isolation tests for task creation"

# Each commit is independently reviewable and revertable
```

**Bad Practice**:
```
Commit 1: "feat: implement entire task management system"
# Too large, mixes concerns, hard to review/revert
```

---

## Version History

### v1.0.0 (2025-12-12)
- Initial principles for Phase Implementer
- Established TDD (red-green-refactor), coverage (≥80%), test quality standards
- Defined constitutional compliance (user isolation, type safety, documentation, database)
- Created code quality (DRY, SOLID, complexity) and performance (SLO, optimization) principles
- Documented security (validation, no secrets, SQL injection prevention) and Git commit standards

---

## Related Files

- **persona.md**: Role, expertise, communication style
- **questions.md**: Implementation discovery questions
- **README.md**: Aggregated P+Q+P guide with examples
