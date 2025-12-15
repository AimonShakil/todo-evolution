# Discovery Questions: Phase Implementer

**Version**: 1.0.0
**Created**: 2025-12-12
**Last Updated**: 2025-12-12

---

## Purpose

These questions guide the **implementation** process when writing code. Use them to uncover:
- Task dependencies and execution order
- Test scenarios (happy path, edge cases, user isolation)
- Code structure and organization
- Performance optimization opportunities
- Constitutional compliance requirements

---

## Question Categories

### 1. Pre-Implementation Questions 📋

**Purpose**: Plan before writing code

#### Q1.1: What artifacts exist?
- Do we have spec.md? (acceptance scenarios to validate)
- Do we have plan.md? (architecture, tech stack, data models)
- Do we have tasks.md? (step-by-step implementation order)
- Are ADRs referenced? (significant decisions to follow)

**Why it matters**: Ensures spec-driven development (Constitutional Principle I).

#### Q1.2: What is the task execution order?
- Which tasks depend on others? (models before services, services before routes)
- What's the critical path? (P1 MVP tasks first)
- Are there parallelizable tasks? (frontend + backend simultaneously)

**Example Order**:
```
1. Database models (Task, User) - FIRST (foundation)
2. Database migrations (create tables) - AFTER models
3. Service layer (task_service.py) - AFTER models
4. CLI commands (add, list, complete) - AFTER services
5. Integration tests - AFTER CLI commands
```

#### Q1.3: What test categories are needed?
Based on spec.md acceptance scenarios:
- **Happy path**: Normal usage (create task "Buy milk")
- **Edge cases**: Boundary conditions (empty title, 200-char title)
- **Error conditions**: Invalid inputs (201-char title, empty user_id)
- **User isolation**: Cross-user access attempts (alice tries to access bob's task)
- **Integration**: End-to-end flows (CLI command → database → response)

#### Q1.4: What phase are we implementing?
- Phase I: Console (SQLite, Click CLI)
- Phase II: Web (FastAPI, Next.js, PostgreSQL)
- Phase III: AI (MCP, OpenAI Agents)
- Phase IV: Kubernetes (Docker, Helm)
- Phase V: Cloud (Kafka, Dapr)

**Why it matters**: Phase determines tech stack and patterns (from plan.md).

---

### 2. Test-Driven Development (TDD) Questions 🧪

**Purpose**: Write tests first (red-green-refactor)

#### Q2.1: What is the test scenario?
From spec.md acceptance scenario, extract Given/When/Then:
- **Given**: Initial state (user alice, database has 3 tasks)
- **When**: Action (create task "Buy milk")
- **Then**: Expected outcome (task created with id=4, user_id=alice, completed=false)

**Example**:
```python
def test_create_task_happy_path(test_db):
    """Given user alice, When I create task 'Buy milk', Then task created."""
    task = create_task(user_id="alice", title="Buy milk")
    assert task.id is not None
    assert task.user_id == "alice"
    assert task.title == "Buy milk"
    assert task.completed is False
```

#### Q2.2: What edge cases exist?
Review spec.md for edge case scenarios:
- **Empty inputs**: title="" → ValidationError
- **Max length**: title="a" * 201 → ValidationError
- **Invalid types**: title=123 (int, not str) → TypeError
- **Missing required**: user_id=None → ValueError
- **Empty state**: list tasks when user has 0 tasks → empty list (not error)

#### Q2.3: What user isolation tests are needed? (CRITICAL)
Per Constitutional Principle II, ALWAYS test:
- **Same user read**: Alice reads alice's tasks → success
- **Cross-user read**: Alice reads bob's tasks → empty list (404, not 401/403)
- **Cross-user write**: Alice updates bob's task → 404 Not Found
- **Cross-user delete**: Alice deletes bob's task → 404 Not Found

**Example**:
```python
def test_user_isolation_cross_user_read(test_db):
    """Test alice cannot read bob's tasks (returns empty, not error)."""
    # Setup: Create task for bob
    bob_task = create_task(user_id="bob", title="Bob's task")

    # Test: Alice queries for tasks (should not see bob's)
    alice_tasks = list_tasks(user_id="alice")
    assert alice_tasks == []  # Empty, not error
    assert bob_task not in alice_tasks
```

#### Q2.4: How do I structure test files?
- **Unit tests**: `tests/unit/test_task_service.py` (test services in isolation)
- **Integration tests**: `tests/integration/test_cli.py` (test CLI → service → database)
- **Fixtures**: `tests/conftest.py` (shared fixtures: test_db, sample data)

**Example Structure**:
```
tests/
├── conftest.py               # Fixtures (test_db, sample users)
├── unit/
│   ├── test_task_service.py  # Service layer tests
│   └── test_validators.py    # Validation logic tests
└── integration/
    ├── test_cli.py           # CLI command tests
    └── test_api.py           # API endpoint tests (Phase II)
```

---

### 3. Code Structure Questions 🏗️

**Purpose**: Organize code for maintainability

#### Q3.1: Where does this code belong?
Follow plan.md architecture:
- **Models**: `backend/models/task.py` (SQLModel classes)
- **Services**: `backend/services/task_service.py` (business logic)
- **CLI**: `backend/cli.py` (Click commands) - Phase I
- **API**: `backend/routes/task_routes.py` (FastAPI routes) - Phase II
- **Utils**: `backend/utils/validators.py` (shared validation)

**Separation of Concerns**:
```
✅ GOOD:
- Model: Data structure (Task SQLModel class)
- Service: Business logic (create_task, validate input)
- CLI/API: User interface (parse input, call service, format output)

❌ BAD:
- CLI command contains database queries (violates separation)
- Service imports Click (coupling to CLI framework)
```

#### Q3.2: What functions should I extract?
Apply DRY (Don't Repeat Yourself) and Single Responsibility:
- **Validation**: Extract `_validate_title()`, `_validate_user_id()`
- **Formatting**: Extract `_format_task_output()`
- **Queries**: Extract `_get_task_by_id()`, `_list_user_tasks()`

**Example**:
```python
# ❌ BAD: Duplication
def create_task(user_id, title):
    if not title or len(title) > 200:
        raise ValidationError(...)
    # ...

def update_task(task_id, title):
    if not title or len(title) > 200:  # DUPLICATED!
        raise ValidationError(...)
    # ...

# ✅ GOOD: Extract validation
def _validate_title(title: str) -> None:
    """Validate title is 1-200 characters."""
    if not title:
        raise ValidationError("Title cannot be empty")
    if len(title) > 200:
        raise ValidationError("Title must be 1-200 characters")

def create_task(user_id, title):
    _validate_title(title)
    # ...

def update_task(task_id, title):
    _validate_title(title)  # Reuse!
    # ...
```

#### Q3.3: What should I name this?
Follow Python PEP 8 / TypeScript conventions:
- **Functions**: `snake_case` (Python), `camelCase` (TypeScript)
- **Classes**: `PascalCase` (both)
- **Constants**: `UPPER_CASE` (both)
- **Private**: `_leading_underscore` (Python), `#private` or `private` keyword (TypeScript)

**Naming Guidelines**:
- **Verbs for actions**: `create_task`, `list_tasks`, `mark_complete`
- **Nouns for data**: `Task`, `User`, `task_id`
- **Descriptive, not cryptic**: `user_id` not `uid`, `task_title` not `tt`

#### Q3.4: How do I handle errors?
Per plan.md error taxonomy:
- **Validation errors**: Raise `ValidationError` (400 Bad Request)
- **Not found**: Raise `NotFoundError` (404 Not Found)
- **Unauthorized**: Raise `UnauthorizedError` (401 Unauthorized)
- **Internal errors**: Log and raise `InternalError` (500 Internal Server Error)

**Example**:
```python
from backend.exceptions import ValidationError, NotFoundError

def get_task(user_id: str, task_id: int) -> Task:
    """Get task by ID for specific user."""
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if not task:
        # User isolation: 404 (not 403, avoid info disclosure)
        raise NotFoundError(f"Task {task_id} not found")

    return task
```

---

### 4. Constitutional Compliance Questions ⚖️

**Purpose**: Enforce all 28 constitutional principles

#### Q4.1: Does this code enforce user isolation? (Principle II - CRITICAL)
**Checklist**:
- [ ] All queries filter by `user_id`
- [ ] Cross-user access returns 404 (not 401/403)
- [ ] Tests verify user isolation (alice cannot access bob's data)
- [ ] CLI commands require `--user` flag
- [ ] API routes extract `user_id` from JWT claims

**Example**:
```python
# ✅ CORRECT: User isolation enforced
def list_tasks(user_id: str) -> List[Task]:
    """List all tasks for user."""
    return session.exec(
        select(Task).where(Task.user_id == user_id)
    ).all()

# ❌ SECURITY VIOLATION: No user_id filter
def list_tasks() -> List[Task]:
    return session.exec(select(Task)).all()  # Returns ALL users' tasks!
```

#### Q4.2: Does this code have type hints and docstrings? (Principle IX)
**Checklist**:
- [ ] All functions have type hints (params and return type)
- [ ] All functions have Google-style docstrings
- [ ] Docstrings include Args, Returns, Raises, Examples
- [ ] mypy --strict passes

**Example**:
```python
def create_task(user_id: str, title: str) -> Task:
    """Create a new task for the specified user.

    Args:
        user_id: The ID of the user creating the task
        title: The task title (1-200 characters)

    Returns:
        Task: The newly created task with assigned ID

    Raises:
        ValidationError: If title is empty or >200 characters
        ValueError: If user_id is empty

    Example:
        >>> task = create_task("alice", "Buy milk")
        >>> task.title
        'Buy milk'
        >>> task.user_id
        'alice'
    """
    # Implementation...
```

#### Q4.3: Does this code have ≥80% test coverage? (Principle X)
**Checklist**:
- [ ] Happy path tested
- [ ] Edge cases tested (empty, max length, invalid types)
- [ ] Error conditions tested (validation failures)
- [ ] User isolation tested
- [ ] Coverage report shows ≥80%

**Run Coverage**:
```bash
pytest tests/ --cov=backend --cov-report=term-missing --cov-fail-under=80
```

#### Q4.4: Does this code follow performance SLOs? (Principle XVIII)
From plan.md NFRs:
- **Phase I**: CLI commands <100ms (p95)
- **Phase II**: API endpoints <500ms (p95)
- **Phase V**: API endpoints <200ms (p95)

**Performance Checklist**:
- [ ] Queries use indexes (user_id indexed)
- [ ] Avoid N+1 queries (use eager loading, batch queries)
- [ ] Use async where appropriate (FastAPI routes, database sessions)
- [ ] Profile slow functions (cProfile, py-spy)

**Example**:
```python
# ❌ N+1 QUERY PROBLEM
def list_tasks_with_user_details(user_ids: List[str]) -> List[Dict]:
    tasks = []
    for user_id in user_ids:  # N queries!
        user = session.exec(select(User).where(User.id == user_id)).first()
        user_tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
        tasks.append({"user": user, "tasks": user_tasks})
    return tasks

# ✅ OPTIMIZED: Batch query
def list_tasks_with_user_details(user_ids: List[str]) -> List[Dict]:
    # Single query with JOIN
    results = session.exec(
        select(User, Task).join(Task).where(User.id.in_(user_ids))
    ).all()
    # Group results...
```

---

### 5. Refactoring Questions 🔄

**Purpose**: Improve code quality after tests pass

#### Q5.1: Is this code DRY (Don't Repeat Yourself)?
Look for duplicated logic:
- Same validation in multiple functions → Extract to helper
- Same query pattern → Extract to query function
- Same error handling → Extract to decorator

#### Q5.2: Does this code follow SOLID principles?
- **Single Responsibility**: Each function does one thing
- **Open/Closed**: Extend behavior without modifying existing code
- **Liskov Substitution**: Subtypes can replace base types
- **Interface Segregation**: Small, focused interfaces
- **Dependency Inversion**: Depend on abstractions, not concretions

**Example (Single Responsibility)**:
```python
# ❌ BAD: Function does too much
def create_and_notify_task(user_id, title):
    # Validation
    if not title:
        raise ValidationError(...)
    # Create task
    task = Task(user_id=user_id, title=title)
    session.add(task)
    session.commit()
    # Send notification (DIFFERENT RESPONSIBILITY!)
    send_email(user_id, f"Task created: {title}")
    return task

# ✅ GOOD: Separate concerns
def create_task(user_id, title):
    """Create task (single responsibility)."""
    _validate_title(title)
    task = Task(user_id=user_id, title=title)
    session.add(task)
    session.commit()
    return task

def notify_task_created(task: Task):
    """Send notification (separate responsibility)."""
    send_email(task.user_id, f"Task created: {task.title}")

# Usage: Compose in higher-level function or event handler
task = create_task("alice", "Buy milk")
notify_task_created(task)
```

#### Q5.3: Are there magic numbers or strings?
Extract to named constants:
```python
# ❌ BAD: Magic numbers
if len(title) > 200:
    raise ValidationError(...)

# ✅ GOOD: Named constants
MAX_TITLE_LENGTH = 200

if len(title) > MAX_TITLE_LENGTH:
    raise ValidationError(f"Title must be 1-{MAX_TITLE_LENGTH} characters")
```

#### Q5.4: Can this code be simplified?
- Remove unnecessary variables
- Use comprehensions instead of loops
- Use early returns instead of nested ifs

**Example**:
```python
# ❌ COMPLEX: Nested ifs
def get_task(user_id, task_id):
    task = session.exec(...).first()
    if task:
        if task.user_id == user_id:
            return task
        else:
            raise NotFoundError(...)
    else:
        raise NotFoundError(...)

# ✅ SIMPLE: Early returns
def get_task(user_id, task_id):
    task = session.exec(...).first()
    if not task or task.user_id != user_id:
        raise NotFoundError(f"Task {task_id} not found")
    return task
```

---

### 6. Performance Optimization Questions ⚡

**Purpose**: Optimize only if SLO violated (not premature)

#### Q6.1: Is performance measured?
Before optimizing:
- Measure baseline (cProfile, py-spy, APM tools)
- Identify bottleneck (database queries, CPU-bound operations)
- Compare to SLO (p95 latency from plan.md)

**Only optimize if SLO violated**

#### Q6.2: What is the bottleneck?
Common bottlenecks:
- **Database queries**: Missing indexes, N+1 queries
- **CPU-bound**: Complex algorithms, large data processing
- **I/O-bound**: External API calls, file operations
- **Memory**: Large data structures, memory leaks

#### Q6.3: What optimization applies?
Based on bottleneck:
- **Database**: Add indexes, batch queries, use read replicas
- **CPU**: Cache results, use async/multiprocessing, optimize algorithm
- **I/O**: Use async, connection pooling, circuit breakers
- **Memory**: Stream data, use generators, profile with memory_profiler

**Example (Database Optimization)**:
```python
# ❌ SLOW: No index on priority
tasks = session.exec(
    select(Task).where(Task.user_id == user_id).order_by(Task.priority)
).all()

# ✅ FAST: Add composite index
# Migration: CREATE INDEX idx_user_priority ON tasks (user_id, priority);
tasks = session.exec(
    select(Task).where(Task.user_id == user_id).order_by(Task.priority)
).all()  # Uses index, <50ms (vs. 500ms before)
```

#### Q6.4: Did optimization help?
After optimization:
- Measure again (compare to baseline)
- Verify SLO met (p95 latency, throughput)
- Check for regressions (tests still pass?)

---

## Question Sequencing Strategy

**Implementation Order**:

1. **Pre-Implementation** (Q1) → Plan tasks, identify dependencies
2. **TDD - Red** (Q2.1) → Write failing test for scenario
3. **TDD - Green** (Q2.1) → Implement minimum code to pass
4. **TDD - Edge Cases** (Q2.2, Q2.3) → Test edge cases, user isolation
5. **Code Structure** (Q3) → Organize code, extract functions, name clearly
6. **Constitutional Check** (Q4) → Verify user isolation, type hints, coverage, SLOs
7. **Refactor** (Q5) → DRY, SOLID, simplify
8. **Performance** (Q6) → Optimize only if SLO violated
9. **Commit** → Conventional commit with details

**Example Flow**:
```
Task: "Implement task creation"
  ↓
Q1.2: Dependencies? → Need Task model first (done), then service
  ↓
Q2.1: Test scenario? → "Given user alice, When create 'Buy milk', Then task created"
  ↓
Write test → FAILS (red)
  ↓
Implement create_task() → Test PASSES (green)
  ↓
Q2.2: Edge cases? → Empty title, 201-char title, empty user_id
  ↓
Write edge case tests → Implement validation → PASS
  ↓
Q2.3: User isolation? → Cross-user access test
  ↓
Write isolation test → Already passes (user_id filter in query)
  ↓
Q4.1: Constitutional check? → ✅ user_id filter, ✅ type hints, ✅ docstrings, ✅ coverage 92%
  ↓
Q5.1: DRY? → Extract _validate_title()
  ↓
Refactor → Tests still pass
  ↓
Commit with conventional message
```

---

## Anti-Patterns to Avoid

### ❌ Implementing Before Testing
**Problem**: Writing code without test first
**Fix**: ALWAYS write test first (TDD red-green-refactor)

### ❌ Skipping Edge Cases
**Problem**: Only testing happy path
**Fix**: Test empty, max length, invalid types, cross-user access

### ❌ Ignoring User Isolation
**Problem**: Query without user_id filter
**Fix**: ALWAYS filter by user_id, test cross-user access

### ❌ No Docstrings
**Problem**: Functions without documentation
**Fix**: Google-style docstrings with Args, Returns, Raises, Examples

### ❌ Premature Optimization
**Problem**: Optimizing before measuring
**Fix**: Implement simple solution, measure, optimize only if SLO violated

---

## Related Files

- **persona.md**: Role, expertise, communication style
- **principles.md**: Code quality, testing, constitutional standards
- **README.md**: Aggregated P+Q+P guide with examples

## Version History

### v1.0.0 (2025-12-12)
- Initial question framework for Phase Implementer
- Organized into 6 categories (Pre-Implementation, TDD, Code Structure, Constitutional, Refactoring, Performance)
- Added sequencing strategy and anti-patterns
