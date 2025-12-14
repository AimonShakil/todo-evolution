---
name: test-coverage
description: Ensure test coverage meets constitutional 80% minimum and validate test quality. Use when writing tests, reviewing coverage reports, or validating test completeness. Applies Constitutional Principle X.
allowed-tools: Read, Write, Bash, Grep
---

# Test Coverage Guardian Skill

Ensures 80% test coverage with quality validation (Principle X: Testing Requirements).

## Constitutional Requirement

**Minimum 80% line coverage** - measured by `pytest-cov` (Python) and `c8` (TypeScript).

## Coverage Commands

### Python (Backend)
```bash
# Run tests with coverage
pytest --cov=backend --cov-report=term-missing --cov-fail-under=80

# Generate HTML report
pytest --cov=backend --cov-report=html

# View HTML report
open htmlcov/index.html
```

### TypeScript (Frontend - Phase II+)
```bash
# Run tests with coverage
npm test -- --coverage --coverageThreshold='{"global": {"lines":80}}'

# View coverage report
open coverage/lcov-report/index.html
```

## Coverage Exclusions

Per Constitution, exclude these from coverage metrics:

- **Database migrations** (`alembic/versions/*.py`)
- **Configuration files** (`config.py`, `settings.py`)
- **Type stubs** (`*.pyi` files)
- **Main entry points** (`if __name__ == "__main__"` blocks)
- **Test files themselves** (`test_*.py`, `*_test.py`, `*.test.ts`)

```python
# .coveragerc (Python)
[run]
omit =
    */tests/*
    */test_*.py
    */alembic/versions/*
    */config.py
    */__main__.py

[report]
exclude_lines =
    pragma: no cover
    if __name__ == .__main__.:
    if TYPE_CHECKING:
    @abstractmethod
```

```json
// package.json (TypeScript)
{
  "jest": {
    "coveragePathIgnorePatterns": [
      "/node_modules/",
      "/tests/",
      "/.next/",
      "/dist/"
    ]
  }
}
```

## Test Structure: Unit → Integration → E2E

### Unit Tests (Target: 90%+ coverage)
- **Scope**: Pure functions, isolated components, business logic
- **No external dependencies**: Mock database, network, file system
- **Fast**: Run in milliseconds

```python
# ✅ GOOD - Unit test (isolated)
from unittest.mock import Mock
import pytest

def test_validate_task_title():
    """Unit test: validate_task_title with various inputs."""
    # Valid title
    assert validate_task_title("Buy groceries") == "Buy groceries"

    # Empty title
    with pytest.raises(ValueError, match="Title cannot be empty"):
        validate_task_title("")

    # Title too long
    with pytest.raises(ValueError, match="Title must be 1-200 characters"):
        validate_task_title("x" * 201)
```

### Integration Tests (Target: 80%+ coverage)
- **Scope**: API endpoints, database interactions, multi-component workflows
- **Real dependencies**: Use test database, real HTTP requests
- **Medium speed**: Run in seconds

```python
# ✅ GOOD - Integration test (real database)
import pytest
from sqlmodel import Session, create_engine, SQLModel
from fastapi.testclient import TestClient

@pytest.fixture
def test_db():
    """Create test database."""
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

def test_create_task_endpoint(test_db, client):
    """Integration test: POST /api/{user_id}/tasks."""
    response = client.post(
        "/api/alice/tasks",
        json={"title": "Buy groceries"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy groceries"
    assert data["user_id"] == "alice"

    # Verify persisted to database
    task = test_db.exec(select(Task).where(Task.id == data["id"])).first()
    assert task is not None
    assert task.title == "Buy groceries"
```

### E2E Tests (Minimum: happy path for each user story)
- **Scope**: Complete user journeys from UI to database
- **Real system**: Browser, full stack, real database
- **Slow**: Run in tens of seconds

```python
# ✅ GOOD - E2E test (Phase II+ with Playwright MCP)
@pytest.mark.e2e
async def test_user_can_add_and_complete_task():
    """E2E: User adds task and marks it complete."""
    # Use Playwright MCP server
    await browser_navigate(url="http://localhost:3000")

    # Login
    await browser_click(element="login button", ref="...")
    await browser_type(element="email input", ref="...", text="alice@example.com")
    await browser_type(element="password input", ref="...", text="password123")
    await browser_click(element="submit button", ref="...")

    # Add task
    await browser_type(element="task input", ref="...", text="Buy groceries")
    await browser_click(element="add task button", ref="...")

    # Verify task appears
    snapshot = await browser_snapshot()
    assert "Buy groceries" in snapshot

    # Complete task
    await browser_click(element="complete task checkbox", ref="...")

    # Verify marked complete
    snapshot = await browser_snapshot()
    assert "completed" in snapshot  # Or check for strikethrough styling
```

## Required Test Categories

Per Constitution, these tests are **MANDATORY**:

### 1. User Data Isolation Tests
```python
def test_user_cannot_access_other_user_tasks(test_db, client):
    """Constitutional requirement: user isolation."""
    # Alice creates task
    alice_response = client.post(
        "/api/alice/tasks",
        json={"title": "Alice's task"}
    )
    alice_task_id = alice_response.json()["id"]

    # Bob tries to access Alice's task
    bob_response = client.get(f"/api/bob/tasks/{alice_task_id}")

    # Must return 404 (not 401 to avoid information disclosure)
    assert bob_response.status_code == 404

def test_user_cannot_update_other_user_tasks(test_db, client):
    """Bob cannot update Alice's task."""
    alice_task_id = create_task(user_id="alice", title="Alice's task")

    response = client.patch(
        f"/api/bob/tasks/{alice_task_id}",
        json={"title": "Bob hacked this"}
    )

    assert response.status_code == 404

def test_user_cannot_delete_other_user_tasks(test_db, client):
    """Bob cannot delete Alice's task."""
    alice_task_id = create_task(user_id="alice", title="Alice's task")

    response = client.delete(f"/api/bob/tasks/{alice_task_id}")

    assert response.status_code == 404
```

### 2. Authentication Tests (Phase II+)
```python
def test_jwt_validation_rejects_invalid_token(client):
    """Invalid JWT token rejected."""
    response = client.get(
        "/api/alice/tasks",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401

def test_jwt_validation_rejects_expired_token(client):
    """Expired JWT token rejected."""
    expired_token = create_expired_jwt()
    response = client.get(
        "/api/alice/tasks",
        headers={"Authorization": f"Bearer {expired_token}"}
    )
    assert response.status_code == 401

def test_missing_authorization_header_rejected(client):
    """Request without Authorization header rejected."""
    response = client.get("/api/alice/tasks")
    assert response.status_code == 401
```

### 3. CRUD Operations Tests
```python
def test_create_task(test_db, client):
    """Create task returns 201 with task data."""
    response = client.post(
        "/api/alice/tasks",
        json={"title": "Buy groceries"}
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Buy groceries"

def test_read_task(test_db, client):
    """Read task returns 200 with task data."""
    task_id = create_task(user_id="alice", title="Buy groceries")
    response = client.get(f"/api/alice/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Buy groceries"

def test_update_task(test_db, client):
    """Update task returns 200 with updated data."""
    task_id = create_task(user_id="alice", title="Buy groceries")
    response = client.patch(
        f"/api/alice/tasks/{task_id}",
        json={"title": "Buy milk"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Buy milk"

def test_delete_task(test_db, client):
    """Delete task returns 204."""
    task_id = create_task(user_id="alice", title="Buy groceries")
    response = client.delete(f"/api/alice/tasks/{task_id}")
    assert response.status_code == 204

    # Verify deleted
    response = client.get(f"/api/alice/tasks/{task_id}")
    assert response.status_code == 404
```

### 4. Error Handling Tests
```python
def test_400_bad_request_on_invalid_input(client):
    """Invalid input returns 400."""
    response = client.post(
        "/api/alice/tasks",
        json={"title": ""}  # Empty title
    )
    assert response.status_code == 400
    assert "error" in response.json()

def test_401_unauthorized_on_missing_token(client):
    """Missing auth token returns 401."""
    response = client.get("/api/alice/tasks")
    assert response.status_code == 401

def test_404_not_found_on_nonexistent_task(client):
    """Nonexistent task returns 404."""
    response = client.get("/api/alice/tasks/99999")
    assert response.status_code == 404

def test_500_internal_error_on_unexpected_failure(client, monkeypatch):
    """Unexpected errors return 500."""
    def mock_failure(*args, **kwargs):
        raise Exception("Database connection failed")

    monkeypatch.setattr("backend.db.get_task", mock_failure)

    response = client.get("/api/alice/tasks/1")
    assert response.status_code == 500
    # Verify no stack trace leaked to client
    assert "Exception" not in response.json().get("error", "")
```

## Test Fixtures and Utilities

### Database Fixture (SQLite - Phase I)
```python
# conftest.py
import pytest
from sqlmodel import create_engine, SQLModel, Session

@pytest.fixture
def test_db():
    """Create in-memory SQLite database for testing."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    SQLModel.metadata.drop_all(engine)
```

### FastAPI Test Client (Phase II+)
```python
# conftest.py
import pytest
from fastapi.testclient import TestClient
from backend.main import app

@pytest.fixture
def client(test_db):
    """Create FastAPI test client."""
    # Override database dependency
    def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
```

### Factory Pattern for Test Data
```python
# tests/factories.py
from datetime import datetime
from sqlmodel import Session

def create_task(
    session: Session,
    user_id: str = "testuser",
    title: str = "Test task",
    completed: bool = False
) -> Task:
    """Factory for creating test tasks."""
    task = Task(
        user_id=user_id,
        title=title,
        completed=completed,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

## Coverage Report Interpretation

### Understanding Coverage Metrics

```
Name                      Stmts   Miss  Cover   Missing
-------------------------------------------------------
backend/main.py              45      2    96%   78, 92
backend/models.py            30      0   100%
backend/routes/tasks.py      65      8    88%   45-52, 87
backend/db.py                25      3    88%   18, 34-35
-------------------------------------------------------
TOTAL                       165     13    92%
```

- **Stmts**: Total statements (lines of executable code)
- **Miss**: Statements not covered by tests
- **Cover**: Coverage percentage (Must be ≥80%)
- **Missing**: Line numbers not covered

### Fixing Low Coverage

```python
# If routes/tasks.py:45-52 not covered, add test:

def test_task_pagination(client):
    """Test pagination on task list endpoint."""
    # Create 25 tasks
    for i in range(25):
        create_task(user_id="alice", title=f"Task {i}")

    # Request page 1 (default limit=20)
    response = client.get("/api/alice/tasks?page=1")
    assert len(response.json()) == 20

    # Request page 2
    response = client.get("/api/alice/tasks?page=2")
    assert len(response.json()) == 5
```

## Continuous Integration (CI/CD) Gates

### GitHub Actions Workflow

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.13'

      - name: Install dependencies
        run: |
          pip install uv
          uv pip install -e .[dev]

      - name: Run tests with coverage
        run: |
          pytest --cov=backend --cov-report=term-missing --cov-fail-under=80

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          fail_ci_if_error: true
```

### CI Gate: Block Merge if Coverage < 80%

```yaml
# .github/workflows/test.yml (continued)
      - name: Check coverage threshold
        run: |
          COVERAGE=$(pytest --cov=backend --cov-report=term | grep TOTAL | awk '{print $4}' | sed 's/%//')
          if (( $(echo "$COVERAGE < 80" | bc -l) )); then
            echo "Coverage $COVERAGE% is below 80% threshold"
            exit 1
          fi
```

## MCP Integration (Playwright for E2E)

For Phase II+ frontend testing, use Playwright MCP server:

```python
# E2E test using Playwright MCP
@pytest.mark.e2e
async def test_complete_task_journey():
    """E2E: User adds, views, completes, and deletes a task."""

    # Navigate to app
    await mcp__playwright__browser_navigate(url="http://localhost:3000")

    # Take snapshot to find elements
    snapshot = await mcp__playwright__browser_snapshot()

    # Add task
    await mcp__playwright__browser_type(
        element="task input field",
        ref="<ref-from-snapshot>",
        text="Buy groceries"
    )
    await mcp__playwright__browser_click(
        element="add button",
        ref="<ref-from-snapshot>"
    )

    # Verify task appears
    snapshot = await mcp__playwright__browser_snapshot()
    assert "Buy groceries" in snapshot

    # Complete task
    await mcp__playwright__browser_click(
        element="complete checkbox",
        ref="<ref-from-snapshot>"
    )

    # Delete task
    await mcp__playwright__browser_click(
        element="delete button",
        ref="<ref-from-snapshot>"
    )

    # Verify task removed
    snapshot = await mcp__playwright__browser_snapshot()
    assert "Buy groceries" not in snapshot
```

## Test Quality Checklist

Before considering tests complete:

- [ ] **Coverage ≥ 80%**: Run coverage report, verify threshold met
- [ ] **User isolation**: Cross-user access tests exist and pass
- [ ] **Authentication**: Token validation tests exist (Phase II+)
- [ ] **CRUD operations**: All endpoints tested
- [ ] **Error handling**: 400, 401, 404, 500 responses tested
- [ ] **Edge cases**: Empty inputs, max lengths, invalid data tested
- [ ] **Fast unit tests**: <100ms per test
- [ ] **Reliable**: Tests pass consistently (not flaky)
- [ ] **Isolated**: Tests don't depend on each other
- [ ] **Clear names**: Test names describe what they validate

## TDD Workflow (Red-Green-Refactor)

```python
# RED: Write failing test first
def test_task_title_validation():
    """Task title must be 1-200 characters."""
    with pytest.raises(ValueError):
        create_task(user_id="alice", title="")  # Empty title

# Run test: pytest -v tests/test_task.py::test_task_title_validation
# Result: FAILED (function doesn't validate yet)

# GREEN: Implement minimal code to pass
def create_task(user_id: str, title: str) -> Task:
    """Create a task for the user."""
    if not title or len(title.strip()) == 0:
        raise ValueError("Title cannot be empty")
    if len(title) > 200:
        raise ValueError("Title must be 1-200 characters")

    task = Task(user_id=user_id, title=title.strip())
    session.add(task)
    session.commit()
    return task

# Run test: pytest -v tests/test_task.py::test_task_title_validation
# Result: PASSED

# REFACTOR: Clean up code
def create_task(user_id: str, title: str) -> Task:
    """Create a task for the user."""
    validated_title = _validate_title(title)  # Extract validation

    task = Task(user_id=user_id, title=validated_title)
    session.add(task)
    session.commit()
    return task

def _validate_title(title: str) -> str:
    """Validate and normalize task title."""
    if not title or len(title.strip()) == 0:
        raise ValueError("Title cannot be empty")

    normalized = title.strip()
    if len(normalized) > 200:
        raise ValueError("Title must be 1-200 characters")

    return normalized

# Run test: pytest -v tests/test_task.py::test_task_title_validation
# Result: PASSED (still works after refactor)
```

## Constitutional Compliance

Principle X requires:
- **80% minimum coverage** (enforced by CI/CD)
- **Required test categories** (isolation, auth, CRUD, errors)
- **TDD encouraged** (Red-Green-Refactor)

**Zero tolerance** for:
- Coverage < 80% on merge
- Missing user isolation tests
- Missing authentication tests (Phase II+)
- Flaky or unreliable tests
