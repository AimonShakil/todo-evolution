---
name: user-isolation
description: Validate user data isolation in code and tests following constitutional security requirement (Principle II). Use when reviewing database queries, API endpoints, CLI commands, or writing isolation tests. SECURITY CRITICAL.
allowed-tools: Read, Grep, Bash
---

# User Isolation Validator Skill

Validates Constitutional Principle II: User Data Isolation (SECURITY CRITICAL).

## Constitutional Requirement

Per Principle II:
> "Multi-tenant data isolation is mandatory to prevent cross-user data leakage.
> ALL database queries MUST filter by `user_id`.
> **ZERO cross-user data leakage tolerance**."

## Core Principles

### 1. EVERY Query MUST Filter by user_id

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

# ❌ BAD - Security violation (cross-user leak)
tasks = session.exec(select(Task)).all()  # No user_id filter!

task = session.exec(
    select(Task).where(Task.id == task_id)  # Missing user_id!
).first()
```

### 2. API Endpoints Include user_id in Path (Phase II+)

```python
# ✅ GOOD - user_id in URL path
@app.get("/api/{user_id}/tasks")
async def get_tasks(user_id: str):
    tasks = await get_user_tasks(user_id)
    return tasks

# ❌ BAD - user_id not in path
@app.get("/api/tasks")
async def get_tasks(user_id: str):  # From JWT, but not in URL
    # URL doesn't enforce user_id
```

### 3. JWT Token user MUST Match URL user_id (Phase II+)

```python
# ✅ GOOD - Verify token matches URL
@app.get("/api/{user_id}/tasks")
async def get_tasks(
    user_id: str,
    current_user: str = Depends(get_current_user)
):
    if current_user != user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    tasks = await get_user_tasks(user_id)
    return tasks

# ❌ BAD - No verification
@app.get("/api/{user_id}/tasks")
async def get_tasks(user_id: str):
    # Anyone can access any user_id!
    tasks = await get_user_tasks(user_id)
    return tasks
```

## Detection: Finding Violations

### Grep for Missing user_id Filters

```bash
# Find select() queries without user_id (Python)
grep -r "select(Task)" backend/ --include="*.py" | grep -v "user_id"

# Find queries on other models
grep -r "select(Conversation)" backend/ --include="*.py" | grep -v "user_id"
grep -r "select(Message)" backend/ --include="*.py" | grep -v "user_id"

# Find API routes missing {user_id} parameter (FastAPI - Phase II+)
grep -r "@app\." backend/ --include="*.py" | grep "/api/" | grep -v "{user_id}"
```

### Grep for Dangerous Patterns

```bash
# Find .all() without filtering
grep -r "\.all()" backend/ --include="*.py"

# Find .first() without user_id filter
grep -r "\.first()" backend/ --include="*.py"

# Find raw SQL (should use SQLModel ORM)
grep -r "execute(" backend/ --include="*.py"
grep -r "\"SELECT" backend/ --include="*.py"
```

## Code Review Checklist

### Phase I (Console App)

```python
# ✅ GOOD - CLI command with user isolation
@click.command()
@click.option('--user', '-u', required=True)
def view(user: str):
    """View tasks for user."""
    with get_session() as session:
        tasks = session.exec(
            select(Task).where(Task.user_id == user)  # ✓ user_id filter
        ).all()

    for task in tasks:
        click.echo(f"{task.id}: {task.title}")

# ❌ BAD - No user filter
@click.command()
def view():
    """View all tasks (SECURITY VIOLATION)."""
    with get_session() as session:
        tasks = session.exec(select(Task)).all()  # ✗ No user_id filter!

    for task in tasks:
        click.echo(f"{task.id}: {task.title}")
```

### Phase II+ (Web API)

```python
# ✅ GOOD - API endpoint with full isolation
@app.get("/api/{user_id}/tasks")
async def get_tasks(
    user_id: str,
    current_user: User = Depends(get_current_user)  # From JWT
):
    # Verify JWT user matches URL user_id
    if current_user.id != user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Query with user_id filter
    async with get_session() as session:
        tasks = await session.exec(
            select(Task).where(Task.user_id == user_id)  # ✓ user_id filter
        )
        return tasks.all()

# ❌ BAD - Missing JWT verification
@app.get("/api/{user_id}/tasks")
async def get_tasks(user_id: str):
    # No JWT verification - anyone can access any user_id!
    async with get_session() as session:
        tasks = await session.exec(
            select(Task).where(Task.user_id == user_id)
        )
        return tasks.all()

# ❌ WORSE - No user_id in query
@app.get("/api/tasks")
async def get_tasks():
    # No user_id filter at all!
    async with get_session() as session:
        tasks = await session.exec(select(Task))
        return tasks.all()
```

## Required Integration Tests

Per Constitution, these tests are **MANDATORY**:

### Test 1: Cross-User Task Access Blocked

```python
def test_cross_user_task_access_blocked(test_db):
    """Alice cannot access Bob's tasks.

    Constitutional requirement: Principle II (User Data Isolation).
    """
    # Alice creates task
    alice_task = Task(user_id="alice", title="Alice's private task")
    test_db.add(alice_task)
    test_db.commit()

    # Bob queries for tasks (should not see Alice's)
    bob_tasks = test_db.exec(
        select(Task).where(Task.user_id == "bob")
    ).all()

    assert len(bob_tasks) == 0
    assert alice_task not in bob_tasks


def test_cross_user_task_access_by_id_blocked(test_db):
    """Alice cannot access Bob's task by ID."""
    # Bob creates task
    bob_task = Task(user_id="bob", title="Bob's task")
    test_db.add(bob_task)
    test_db.commit()

    # Alice tries to access Bob's task by ID
    alice_query = test_db.exec(
        select(Task).where(
            Task.id == bob_task.id,
            Task.user_id == "alice"  # Alice's filter
        )
    ).first()

    # Alice gets None (task not found)
    assert alice_query is None


def test_cross_user_update_blocked(test_db):
    """Alice cannot update Bob's task."""
    # Bob creates task
    bob_task = Task(user_id="bob", title="Bob's task")
    test_db.add(bob_task)
    test_db.commit()

    # Alice tries to query Bob's task for update
    task_to_update = test_db.exec(
        select(Task).where(
            Task.id == bob_task.id,
            Task.user_id == "alice"
        )
    ).first()

    # Alice cannot find Bob's task
    assert task_to_update is None

    # Verify Bob's task unchanged
    bob_verification = test_db.exec(
        select(Task).where(
            Task.id == bob_task.id,
            Task.user_id == "bob"
        )
    ).first()

    assert bob_verification.title == "Bob's task"


def test_cross_user_delete_blocked(test_db):
    """Alice cannot delete Bob's task."""
    # Bob creates task
    bob_task = Task(user_id="bob", title="Bob's task")
    test_db.add(bob_task)
    test_db.commit()

    # Alice tries to query Bob's task for deletion
    task_to_delete = test_db.exec(
        select(Task).where(
            Task.id == bob_task.id,
            Task.user_id == "alice"
        )
    ).first()

    # Alice cannot find Bob's task
    assert task_to_delete is None

    # Verify Bob's task still exists
    bob_verification = test_db.get(Task, bob_task.id)
    assert bob_verification is not None
```

### Test 2: API Endpoint Isolation (Phase II+)

```python
from fastapi.testclient import TestClient

def test_api_get_tasks_enforces_user_isolation(client):
    """GET /api/{user_id}/tasks enforces user isolation."""
    # Alice creates tasks
    alice_token = create_jwt(user_id="alice")
    response = client.post(
        "/api/alice/tasks",
        json={"title": "Alice's task"},
        headers={"Authorization": f"Bearer {alice_token}"}
    )
    assert response.status_code == 201

    # Bob tries to access Alice's tasks with his JWT
    bob_token = create_jwt(user_id="bob")
    response = client.get(
        "/api/alice/tasks",  # Alice's endpoint
        headers={"Authorization": f"Bearer {bob_token}"}  # Bob's token
    )

    # Should return 401 Unauthorized (token mismatch)
    assert response.status_code == 401


def test_api_cannot_access_task_without_user_id_match(client):
    """User cannot access task unless user_id matches JWT."""
    # Alice creates a task
    alice_token = create_jwt(user_id="alice")
    response = client.post(
        "/api/alice/tasks",
        json={"title": "Alice's task"},
        headers={"Authorization": f"Bearer {alice_token}"}
    )
    task_id = response.json()["id"]

    # Bob tries to access Alice's task
    bob_token = create_jwt(user_id="bob")
    response = client.get(
        f"/api/alice/tasks/{task_id}",  # Alice's task
        headers={"Authorization": f"Bearer {bob_token}"}  # Bob's token
    )

    # Should return 401 Unauthorized
    assert response.status_code == 401


def test_api_returns_404_not_401_for_other_user_task(client):
    """API returns 404 (not 401) to avoid information disclosure.

    Returning 404 instead of 401 prevents attackers from probing
    whether task IDs exist for other users.
    """
    # Alice creates a task
    alice_token = create_jwt(user_id="alice")
    response = client.post(
        "/api/alice/tasks",
        json={"title": "Alice's task"},
        headers={"Authorization": f"Bearer {alice_token}"}
    )
    alice_task_id = response.json()["id"]

    # Bob (authenticated) tries to access Alice's task via his own endpoint
    bob_token = create_jwt(user_id="bob")
    response = client.get(
        f"/api/bob/tasks/{alice_task_id}",  # Bob's endpoint, Alice's task ID
        headers={"Authorization": f"Bearer {bob_token}"}
    )

    # Should return 404 (not 401) - task not found for Bob
    assert response.status_code == 404
```

## CLI Command Validation (Phase I)

```python
# tests/test_cli_isolation.py
from click.testing import CliRunner

def test_cli_view_command_user_isolation():
    """CLI view command respects user isolation."""
    runner = CliRunner()

    with runner.isolated_filesystem():
        # Alice adds a task
        runner.invoke(cli, ['add', '--user', 'alice', 'Alice task'])

        # Bob views tasks (should see none)
        result = runner.invoke(cli, ['view', '--user', 'bob'])

        assert result.exit_code == 0
        assert 'No tasks found' in result.output


def test_cli_complete_command_user_isolation():
    """CLI complete command respects user isolation."""
    runner = CliRunner()

    with runner.isolated_filesystem():
        # Alice adds task with ID 1
        runner.invoke(cli, ['add', '--user', 'alice', 'Alice task'])

        # Bob tries to complete Alice's task
        result = runner.invoke(cli, ['complete', '--user', 'bob', '1'])

        # Should fail (task not found for Bob)
        assert result.exit_code != 0
        assert 'not found' in result.output.lower()
```

## Common Violation Patterns

### Pattern 1: Admin/System Queries

```python
# ❌ DANGEROUS - Admin query without user_id filter
def get_all_tasks_admin():
    """Get ALL tasks (admin only).

    SECURITY RISK: If this function is ever called from non-admin context,
    it leaks all user data!
    """
    with get_session() as session:
        return session.exec(select(Task)).all()  # No user_id filter

# ✅ BETTER - Explicit admin check
def get_all_tasks_admin(admin_user_id: str):
    """Get ALL tasks (admin only).

    Requires admin verification before calling.
    """
    if not is_admin(admin_user_id):
        raise PermissionDenied("Admin access required")

    with get_session() as session:
        return session.exec(select(Task)).all()
```

### Pattern 2: Aggregation Queries

```python
# ❌ DANGEROUS - Count without user_id filter
def get_total_task_count():
    """Get total task count across ALL users."""
    with get_session() as session:
        return session.exec(select(func.count(Task.id))).scalar()

# ✅ GOOD - Count per user
def get_user_task_count(user_id: str):
    """Get task count for specific user."""
    with get_session() as session:
        return session.exec(
            select(func.count(Task.id)).where(Task.user_id == user_id)
        ).scalar()
```

### Pattern 3: Joins and Relationships

```python
# ❌ DANGEROUS - Join without user_id filter
def get_conversation_messages(conversation_id: int):
    """Get messages for conversation.

    SECURITY RISK: Doesn't verify user owns conversation!
    """
    with get_session() as session:
        return session.exec(
            select(Message).where(Message.conversation_id == conversation_id)
        ).all()

# ✅ GOOD - Verify user owns conversation first
def get_conversation_messages(user_id: str, conversation_id: int):
    """Get messages for user's conversation."""
    with get_session() as session:
        # First verify user owns conversation
        conversation = session.exec(
            select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            )
        ).first()

        if not conversation:
            raise ConversationNotFound()

        # Then get messages
        return session.exec(
            select(Message).where(Message.conversation_id == conversation_id)
        ).all()
```

## Constitutional Exception: System Tables

Per Constitution:
> "ALL database queries MUST filter by `user_id` (except system/admin tables)"

**Allowed exceptions**:
- Schema migrations (`alembic_version` table)
- System configuration tables (no user data)
- Admin-only tables with explicit access control

**NOT allowed**:
- User-generated content (tasks, messages, etc.)
- User metadata (preferences, settings, etc.)

## Security Audit Checklist

Run these checks before deployment:

```bash
# 1. Find queries without user_id
grep -r "select(Task)" backend/ --include="*.py" | grep -v "user_id"

# 2. Find API routes missing {user_id}
grep -r "@app\.(get|post|put|patch|delete)" backend/ --include="*.py" | grep "/api/" | grep -v "{user_id}"

# 3. Find .all() calls (potential leaks)
grep -r "\.all()" backend/ --include="*.py"

# 4. Verify user isolation tests exist
pytest tests/test_user_isolation.py -v

# 5. Check coverage includes isolation tests
pytest --cov=backend --cov-report=term-missing
```

## Automated Security Scanner

```python
# scripts/check_user_isolation.py
import re
import sys
from pathlib import Path

def scan_for_violations(directory: Path):
    """Scan for potential user isolation violations."""
    violations = []

    for py_file in directory.rglob("*.py"):
        if "tests" in str(py_file):
            continue  # Skip test files

        content = py_file.read_text()

        # Check for select() without user_id
        if re.search(r'select\(Task\)', content):
            if 'user_id' not in content:
                violations.append(f"{py_file}: select(Task) without user_id")

    return violations

if __name__ == "__main__":
    violations = scan_for_violations(Path("backend"))

    if violations:
        print("❌ User isolation violations found:")
        for v in violations:
            print(f"  - {v}")
        sys.exit(1)
    else:
        print("✅ No user isolation violations found")
        sys.exit(0)
```

## Constitutional Compliance

Zero tolerance for violations:

- [ ] **ALL queries filter by user_id** (Grep check passes)
- [ ] **API endpoints include {user_id}** in path (Phase II+)
- [ ] **JWT verification** matches URL user_id (Phase II+)
- [ ] **Cross-user access tests** exist and pass
- [ ] **Integration tests** verify isolation end-to-end
- [ ] **Security audit** completed before deployment

**CRITICAL**: User isolation is a SECURITY REQUIREMENT, not a feature.
Violations are **critical failures** that MUST block deployment.
