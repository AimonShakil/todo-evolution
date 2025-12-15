---
name: constitution-check
description: Verify code and specifications comply with project constitution's 28 principles. Use when reviewing code, specifications, architectural decisions, or validating implementation. Critical for all development work.
allowed-tools: Read, Grep, Glob, Bash
---

# Constitution Compliance Checker Skill

Validates compliance with all 28 constitutional principles from `.specify/memory/constitution.md`.

## Constitutional Principles Summary

### Core Principles (I-V)
1. **Spec-Driven Development**: spec.md → plan.md → tasks.md before code
2. **User Data Isolation**: All queries filter by `user_id`
3. **Stateless Architecture**: No in-memory state
4. **Smallest Viable Change**: No unnecessary refactoring
5. **Human-as-Tool Strategy**: Ask questions when uncertain

### Technology Stack (Non-Negotiable)
- Python 3.13+ with UV
- FastAPI (Phase II+)
- SQLModel ORM (no raw SQL)
- Next.js 16+ App Router (Phase II+)
- Better Auth with JWT (Phase II+)

### Architecture & Design (VI-VIII)
6. **Database Standards**: SQLModel, Alembic migrations, user_id + timestamps
7. **API Design**: RESTful, `/api/{user_id}/resource`, Pydantic validation
8. **MCP Tool Design**: Stateless tools (Phase III+)

### Code Quality & Testing (IX-X)
9. **Code Quality**: Type hints, docstrings, PEP 8, async I/O
10. **Testing**: 80% coverage minimum, pytest/Jest, TDD encouraged

### Security & Data Protection (XI-XV)
11. **Data Privacy & Retention**: GDPR-aligned, export/deletion endpoints
12. **Security Principles**: No secrets in code, input validation, HTTPS
13. **Dependency Security**: Weekly scans, 48hr critical CVE patching
14. **Authentication & Authorization**: Better Auth, JWT, token verification
15. **API Rate Limiting**: 100 req/min per user

### Performance & Observability (XVI-XIX)
16. **Error Handling & Logging**: Structured JSON logs, graceful degradation
17. **Frontend Accessibility**: WCAG 2.1 AA, keyboard navigation, Lighthouse ≥90
18. **Performance Standards**: p95 <500ms, FCP <1.5s, 80% coverage
19. **Monitoring & Observability**: Health checks, metrics, structured logs

### Cloud-Native (XX-XXV)
20. **Database Backup & DR**: Daily backups, RTO <4hr, monthly restore tests
21. **Event-Driven Architecture**: Kafka events (Phase V)
22. **Dapr Integration**: Pub/sub, state management (Phase V)
23. **Containerization**: Multi-stage builds, non-root user, health checks
24. **Kubernetes & Helm**: Resource limits, HPA, ConfigMaps/Secrets
25. **CI/CD Pipeline**: GitHub Actions, lint → test → build → deploy

### Development Workflow (XXVI-XXVIII)
26. **Conversation Persistence**: Database-backed chat (Phase III+)
27. **Documentation Standards**: README, OpenAPI, ADRs, PHRs
28. **Git & Version Control**: Conventional commits, atomic commits, `.gitignore`

## Validation Checklist

### Spec-Driven Development (Principle I)
- [ ] spec.md exists in `specs/<feature>/`
- [ ] plan.md exists with architecture decisions
- [ ] tasks.md exists with testable tasks
- [ ] PHR will be created after this session
- [ ] ADR suggested (not auto-created) if significant decisions made

**Grep Check**:
```bash
# Verify spec files exist
ls -la specs/<feature>/spec.md
ls -la specs/<feature>/plan.md
ls -la specs/<feature>/tasks.md
```

### User Data Isolation (Principle II) - SECURITY CRITICAL
- [ ] All API endpoints include `/api/{user_id}/resource`
- [ ] All database queries filter by `user_id`
- [ ] JWT token verification middleware exists
- [ ] Cross-user access tests exist

**Grep Check**:
```bash
# Find queries missing user_id filter (Python)
grep -r "select(Task)" --include="*.py" | grep -v "user_id"

# Find API routes missing {user_id} parameter (Python)
grep -r "@app\." --include="*.py" | grep -v "{user_id}"
```

**Integration Test Required**:
```python
def test_cross_user_isolation():
    """User A cannot access User B's tasks."""
    task_a = create_task(user_id="alice")
    result = get_task(user_id="bob", task_id=task_a.id)
    assert result is None  # Bob cannot see Alice's task
```

### Stateless Architecture (Principle III)
- [ ] No in-memory session state
- [ ] All persistent state in database
- [ ] Server restarts don't lose data

**Grep Check**:
```bash
# Find in-memory session storage (anti-pattern)
grep -r "session_store\s*=\s*{}" --include="*.py"
grep -r "global.*session" --include="*.py"
```

### Code Quality Standards (Principle IX)

**Python**:
- [ ] Type hints on all functions
- [ ] Docstrings (Google style) on public functions/classes
- [ ] PEP 8 compliance
- [ ] Async/await for all I/O
- [ ] No bare `except` clauses

**Automated Checks**:
```bash
# Type checking
mypy --strict .

# Docstring coverage
interrogate -v .

# PEP 8 compliance
black --check .
flake8 .

# Find bare except (anti-pattern)
grep -r "except:" --include="*.py"
```

**TypeScript** (Phase II+):
- [ ] Strict mode enabled in `tsconfig.json`
- [ ] All props explicitly typed
- [ ] Server Components by default
- [ ] Tailwind CSS (no inline styles)

**Automated Checks**:
```bash
# Type checking
tsc --noImplicitAny

# Linting
eslint .

# Formatting
prettier --check .
```

### Testing Requirements (Principle X)
- [ ] 80% minimum coverage
- [ ] Unit tests for pure functions
- [ ] Integration tests for API endpoints
- [ ] E2E tests for critical user journeys
- [ ] User isolation tests exist

**Coverage Check**:
```bash
# Python
pytest --cov=backend --cov-report=term-missing --cov-fail-under=80

# TypeScript
npm test -- --coverage --coverageThreshold='{"global": {"lines":80}}'
```

**Required Test Categories**:
```python
# User isolation
def test_user_isolation(): ...

# Authentication
def test_jwt_validation(): ...

# CRUD operations
def test_create_task(): ...
def test_read_task(): ...
def test_update_task(): ...
def test_delete_task(): ...

# Error handling
def test_404_not_found(): ...
def test_401_unauthorized(): ...
def test_400_bad_request(): ...
```

### Security Principles (Principle XII) - NON-NEGOTIABLE
- [ ] No secrets in code (use `.env`)
- [ ] `.env` in `.gitignore`
- [ ] Input validation on all endpoints (Pydantic)
- [ ] SQLModel ORM (prevents SQL injection)
- [ ] CORS configured
- [ ] Rate limiting enabled

**Grep Check**:
```bash
# Find hardcoded secrets (anti-pattern)
grep -ri "api_key\s*=\s*['\"]" --include="*.py" --include="*.ts"
grep -ri "password\s*=\s*['\"]" --include="*.py" --include="*.ts"

# Verify .env in .gitignore
grep "^\.env$" .gitignore
```

### Database Standards (Principle VI)
- [ ] SQLModel models only (no raw SQL)
- [ ] All models include: `user_id`, `id`, `created_at`, `updated_at`
- [ ] Indexes on: `user_id`, `status`, `due_date`
- [ ] Foreign key constraints defined

**Model Template Validation**:
```python
class Task(SQLModel, table=True):
    # Required fields
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)  # MANDATORY
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Task-specific fields
    title: str = Field(max_length=200)
    completed: bool = Field(default=False)
```

### API Design Standards (Principle VII)
- [ ] RESTful methods (GET, POST, PUT, PATCH, DELETE)
- [ ] URL pattern: `/api/{user_id}/resource`
- [ ] JSON request/response with Pydantic
- [ ] Consistent error format: `{error: string, details?: object}`
- [ ] Pagination on list endpoints: `?page=1&limit=20`

**Grep Check**:
```bash
# Find API routes
grep -r "@app\.(get|post|put|patch|delete)" --include="*.py"

# Verify Pydantic models
grep -r "class.*BaseModel" --include="*.py"
```

### Git Standards (Principle XXVIII)
- [ ] Conventional commit format: `<type>: <description>`
- [ ] Types: feat, fix, docs, refactor, test, chore
- [ ] Atomic commits (one logical change)
- [ ] `.gitignore` includes: `.env`, `node_modules`, `__pycache__`, `.venv`

**Commit Message Example**:
```
feat: add user task creation endpoint

Implements POST /api/{user_id}/tasks with Pydantic validation
and user isolation enforcement.

🤖 Generated with Claude Code
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

## Phase-Specific Checks

### Phase I (Console App)
- [ ] Python 3.13+ with UV
- [ ] SQLite database (`todo.db`)
- [ ] SQLModel ORM
- [ ] Click or argparse CLI
- [ ] User isolation in console commands

### Phase II (Web App)
- [ ] FastAPI backend
- [ ] Next.js 16+ frontend
- [ ] Neon PostgreSQL
- [ ] Better Auth with JWT
- [ ] CORS configured

### Phase III (AI Chatbot)
- [ ] MCP server implemented
- [ ] OpenAI Agents SDK
- [ ] Conversation persistence (database)
- [ ] Stateless chat endpoint

### Phase IV (Local K8s)
- [ ] Dockerfiles (multi-stage builds)
- [ ] Helm charts
- [ ] Resource limits defined
- [ ] Health check endpoints

### Phase V (Cloud)
- [ ] Kafka event streaming
- [ ] Dapr integration
- [ ] HPA configured
- [ ] Prometheus metrics

## Compliance Report Format

When validating, generate a report:

```markdown
# Constitution Compliance Report

**Feature**: <feature-name>
**Date**: <date>
**Reviewer**: Claude Code

## ✅ Passing Principles

- [x] I. Spec-Driven Development: spec.md, plan.md, tasks.md exist
- [x] II. User Data Isolation: All queries filter by user_id
- [x] IX. Code Quality: Type hints, docstrings, PEP 8 compliant
- [x] X. Testing: 85% coverage (exceeds 80% minimum)

## ⚠️ Warnings

- [ ] XII. Security: Found 1 potential hardcoded secret in `config.py:42` (needs review)

## ❌ Violations

- [ ] VII. API Design: Missing pagination on GET /api/{user_id}/tasks

## Recommendations

1. Add pagination to task list endpoint (Principle VII)
2. Review potential secret in config.py
3. Add integration test for cross-user access (Principle II)

## Overall Status

**17/20 applicable principles compliant** (85%)
**Action required**: Fix violations before merge
```

## MCP Server Integration

When reviewing dependencies or external libraries, use **context7**:
```
Use mcp__context7__resolve-library-id to find library
Use mcp__context7__get-library-docs to verify API usage matches official docs
```

## Anti-Patterns to Detect

❌ Raw SQL queries instead of SQLModel
❌ Queries without user_id filter
❌ Hardcoded secrets
❌ In-memory session storage
❌ Missing type hints
❌ Bare `except:` clauses
❌ Code without tests
❌ Missing spec.md
❌ Refactoring unrelated code
❌ API endpoints without Pydantic validation

## Constitutional Authority

Per Constitution: "This constitution supersedes all other development guidance."

If constitutional violation detected:
1. **BLOCK** merge/deployment
2. **REPORT** violation with principle reference
3. **SUGGEST** fix aligned with constitution
4. **DOCUMENT** in plan.md if exception needed (with justification)
