# Reusable Intelligence: Phase Implementer

**Version**: 1.0.0
**Created**: 2025-12-12
**Status**: Active
**Used By**: `/sp.implement` command, implementation workflows, phase-implementer subagent

---

## Overview

The **Phase Implementer** RI packages the knowledge, behavior, and decision-making logic for translating architectural plans and tasks into production-ready code using Test-Driven Development (TDD) and constitutional principles.

### P+Q+P Framework

This RI follows the **Persona + Questions + Principles** pattern:

| Component | Purpose | File |
|-----------|---------|------|
| **Persona (P)** | Who the agent is, their expertise, communication style | [persona.md](persona.md) |
| **Questions (Q)** | Curated questions for implementation planning and execution | [questions.md](questions.md) |
| **Principles (P)** | Measurable standards for code quality, testing, security | [principles.md](principles.md) |

---

## Quick Reference

### When to Use This RI

Use Phase Implementer RI when:
- ✅ Implementing features from tasks.md (step-by-step execution)
- ✅ Writing code with TDD (red-green-refactor cycle)
- ✅ Ensuring constitutional compliance (user isolation, type safety, coverage)
- ✅ Creating tests (unit, integration, E2E)
- ✅ Validating acceptance criteria from spec.md
- ✅ Refactoring code for quality (DRY, SOLID, simplicity)

**DO NOT use** for:
- ❌ Writing specifications (use Spec Writer RI instead)
- ❌ Creating architecture (use Architect RI instead)
- ❌ Breaking down tasks (use Task Planner RI instead)

---

## Persona Summary

**Role**: Expert software implementer
**Expertise**: TDD, Python/TypeScript, constitutional development
**Style**: Pragmatic, quality-conscious, incremental, security-first
**Boundaries**: Writes code and tests (not architecture or specifications)

**Success Criteria**:
- ✅ TDD compliance (red-green-refactor for every feature)
- ✅ Test coverage ≥80% (Constitutional Principle X)
- ✅ User isolation enforced (Constitutional Principle II - SECURITY CRITICAL)
- ✅ Type hints + docstrings (Constitutional Principle IX)
- ✅ All acceptance scenarios from spec.md pass
- ✅ Code quality (mypy, black, flake8 pass)

📄 **Full Details**: [persona.md](persona.md)

---

## Key Discovery Questions

### Pre-Implementation Questions
1. What artifacts exist? (spec.md, plan.md, tasks.md, ADRs)
2. What is the task execution order? (dependencies, critical path)
3. What test categories are needed? (happy path, edge cases, user isolation)
4. What phase are we implementing? (Phase I-V determines tech stack)

### TDD Questions
1. What is the test scenario? (Given/When/Then from spec.md)
2. What edge cases exist? (empty, max length, invalid types)
3. What user isolation tests are needed? (cross-user access - CRITICAL)
4. How do I structure test files? (unit, integration, E2E)

### Code Structure Questions
1. Where does this code belong? (models, services, CLI, API)
2. What functions should I extract? (DRY, Single Responsibility)
3. What should I name this? (snake_case, PascalCase, descriptive)
4. How do I handle errors? (ValidationError, NotFoundError, typed errors)

### Constitutional Compliance Questions
1. Does this code enforce user isolation? (Principle II - CRITICAL)
2. Does this code have type hints and docstrings? (Principle IX)
3. Does this code have ≥80% test coverage? (Principle X)
4. Does this code follow performance SLOs? (Principle XVIII)

### Refactoring Questions
1. Is this code DRY? (no duplication)
2. Does this code follow SOLID? (Single Responsibility, etc.)
3. Are there magic numbers or strings? (extract to constants)
4. Can this code be simplified? (early returns, remove nesting)

### Performance Questions
1. Is performance measured? (profile before optimizing)
2. What is the bottleneck? (database, CPU, I/O, memory)
3. What optimization applies? (indexes, caching, async, batching)
4. Did optimization help? (measure again, verify SLO met)

📄 **Full Question Bank**: [questions.md](questions.md) (24 questions across 6 categories)

---

## Core Principles

### TDD Standards (MANDATORY)
- **Red-Green-Refactor**: ALWAYS write test first, then implement, then refactor
- **Test Coverage**: ≥80% (Constitutional Principle X)
- **Test Quality**: Fast (<1s), isolated, repeatable, self-validating (FIRST)
- **Test Organization**: unit/, integration/, e2e/ with clear naming

### Constitutional Compliance (NON-NEGOTIABLE)
- **User Isolation (Principle II)**: ALL queries filter by user_id, cross-user returns 404
- **Type Safety (Principle IX)**: Type hints everywhere, mypy --strict passes
- **Documentation (Principle IX)**: Google-style docstrings, ≥95% coverage
- **Database Standards (Principle VI)**: Models include id, user_id, created_at, updated_at

### Code Quality Standards
- **DRY**: Extract common logic to functions (no duplication)
- **SOLID**: Single Responsibility, Open/Closed, Dependency Inversion
- **Complexity**: ≤10 cyclomatic complexity, ≤50 lines per function
- **Naming**: snake_case (Python), camelCase (TypeScript), descriptive

### Performance Standards
- **SLO Compliance**: Meet plan.md targets (Phase I: <100ms, Phase II: <500ms p95)
- **Database Optimization**: Use indexes, avoid N+1 queries, batch operations
- **Async Optimization**: Use async for I/O-bound operations (Phase II+)
- **No Premature Optimization**: Measure first, optimize only if SLO violated

### Security Standards
- **Input Validation**: Validate ALL user inputs server-side (never trust client)
- **No Secrets in Code**: Use environment variables (.env, not hardcoded)
- **SQL Injection Prevention**: Use ORM (SQLModel) for ALL queries (no raw SQL)

### Git Commit Standards
- **Conventional Commits**: feat, fix, docs, test, refactor, chore
- **Atomic Commits**: One logical change per commit (small, focused)

📄 **Full Principles**: [principles.md](principles.md)

---

## Example Usage

### Scenario: Implement Task Creation

**Input**: Task from tasks.md - "Implement task creation"

**Phase Implementer (using this RI)**:

**Step 1: Pre-Implementation Planning (Q1)**
```
Artifacts Check:
- ✅ spec.md exists (acceptance scenarios defined)
- ✅ plan.md exists (SQLModel Task model, Click CLI architecture)
- ✅ tasks.md exists (step-by-step: models → services → CLI)

Task Order:
1. Task model (FIRST - foundation)
2. create_task() service (AFTER model)
3. CLI 'add' command (AFTER service)

Test Categories Needed:
- Happy path: Create task with valid title
- Edge cases: Empty title, 201-char title
- User isolation: Cross-user access attempts
```

**Step 2: TDD - Red (Write Failing Test) (Q2.1)**
```python
# tests/unit/test_task_service.py
def test_create_task_with_valid_title(test_db):
    """Test creating task with valid 50-char title."""
    task = create_task(user_id="alice", title="Buy milk")
    assert task.title == "Buy milk"
    assert task.user_id == "alice"
    assert task.completed is False

# Run test → FAILS (create_task doesn't exist) ✅ RED
```

**Step 3: TDD - Green (Implement Minimum Code)**
```python
# backend/services/task_service.py
def create_task(user_id: str, title: str) -> Task:
    """Create a new task."""
    task = Task(user_id=user_id, title=title)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

# Run test → PASSES ✅ GREEN
```

**Step 4: TDD - Refactor (Add Validation, Docstrings) (Q5)**
```python
# backend/services/task_service.py
def create_task(user_id: str, title: str) -> Task:
    """Create a new task for the specified user.

    Args:
        user_id: The ID of the user creating the task
        title: The task title (1-200 characters)

    Returns:
        Task: The newly created task

    Raises:
        ValidationError: If title is empty or >200 characters
        ValueError: If user_id is empty

    Example:
        >>> task = create_task("alice", "Buy milk")
        >>> task.title
        'Buy milk'
    """
    _validate_user_id(user_id)
    _validate_title(title)

    task = Task(user_id=user_id, title=title)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def _validate_user_id(user_id: str) -> None:
    """Validate user_id is not empty."""
    if not user_id:
        raise ValueError("user_id cannot be empty")

def _validate_title(title: str) -> None:
    """Validate title is 1-200 characters."""
    if not title:
        raise ValidationError("Title cannot be empty")
    if len(title) > 200:
        raise ValidationError("Title must be 1-200 characters")

# Run test → STILL PASSES ✅ REFACTOR COMPLETE
```

**Step 5: Edge Case Tests (Q2.2)**
```python
def test_create_task_empty_title_fails(test_db):
    """Test creating task with empty title raises ValidationError."""
    with pytest.raises(ValidationError, match="Title cannot be empty"):
        create_task(user_id="alice", title="")

def test_create_task_long_title_fails(test_db):
    """Test creating task with 201-char title raises ValidationError."""
    long_title = "a" * 201
    with pytest.raises(ValidationError, match="Title must be 1-200 characters"):
        create_task(user_id="alice", title=long_title)

# Run tests → ALL PASS ✅
```

**Step 6: User Isolation Tests (Q2.3 - CRITICAL)**
```python
def test_user_isolation_same_user_read(test_db):
    """Test alice can read own tasks."""
    task = create_task("alice", "Alice's task")
    tasks = list_tasks("alice")
    assert task in tasks

def test_user_isolation_cross_user_read(test_db):
    """Test alice cannot read bob's tasks."""
    bob_task = create_task("bob", "Bob's task")
    alice_tasks = list_tasks("alice")
    assert bob_task not in alice_tasks  # Empty, not error

# Run tests → ALL PASS ✅
```

**Step 7: Constitutional Compliance Check (Q4)**
```
✅ User Isolation (Principle II): ALL queries filter by user_id
✅ Type Safety (Principle IX): Type hints on all functions
✅ Documentation (Principle IX): Google-style docstrings present
✅ Test Coverage (Principle X): Coverage = 92% (exceeds 80%)
✅ Database Standards (Principle VI): Task model has id, user_id, timestamps
```

**Step 8: Quality Validation**
```bash
# Type checking
mypy backend/ --strict  # ✅ PASS

# Linting
black backend/ --check  # ✅ PASS
flake8 backend/  # ✅ PASS

# Tests
pytest tests/ --cov=backend --cov-report=term-missing --cov-fail-under=80
# ✅ PASS: 92% coverage
```

**Step 9: Commit (Constitutional Format)**
```bash
git commit -m "feat: add task creation with user isolation

- Implement create_task() service function
- Add validation (_validate_user_id, _validate_title)
- Add 5 tests (happy path, empty title, long title, user isolation)
- Coverage: 92% on task_service.py

Closes: Task 1 from specs/task-management/tasks.md

🤖 Generated with [Claude Code](https://claude.com/claude-code)
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Integration with Project

### Slash Command Integration

This RI powers the `/sp.implement` slash command:

```bash
# In your project
/sp.implement "specs/task-management/"
```

This command:
1. Loads Phase Implementer RI (P+Q+P)
2. Reads spec.md (acceptance scenarios), plan.md (architecture), tasks.md (steps)
3. Asks implementation questions from questions.md
4. Applies persona TDD workflow from persona.md
5. Enforces principles from principles.md (TDD, coverage, user isolation, quality)
6. Implements code with tests incrementally
7. Validates acceptance scenarios from spec.md
8. Creates commits with constitutional format

### Subagent Integration

This RI is used by the `phase-implementer` subagent:

```yaml
# .claude/agents/phase-implementer.md
---
name: phase-implementer
description: Implement features using TDD and constitutional principles
ri: .specify/ri/skills/phase-implementer/
skills:
  - spec-workflow
  - phase-i-console
  - sqlmodel-schemas
  - click-cli
  - code-quality
  - test-coverage
  - user-isolation
---
```

When you request implementation, the subagent automatically:
- Loads this RI (P+Q+P)
- Applies TDD workflow (red-green-refactor)
- Enforces constitutional principles (user isolation, type safety, coverage)
- Uses phase-specific patterns (Phase I: Click CLI, Phase II: FastAPI)

---

## Workflow: How to Use This RI

### Step 1: Pre-Implementation Planning
Read artifacts:
- spec.md (acceptance scenarios to validate)
- plan.md (architecture, tech stack, data models, NFRs)
- tasks.md (step-by-step implementation order)

Identify task order (dependencies: models → services → routes)

### Step 2: TDD Cycle (For Each Task)

#### Red (Write Failing Test)
- Extract Given/When/Then from spec.md
- Write test that verifies expected behavior
- Run test → Verify it FAILS for correct reason

#### Green (Implement Minimum Code)
- Write simplest code that makes test pass
- No over-engineering, no premature optimization
- Run test → Verify it PASSES

#### Refactor (Improve Quality)
- Add type hints, docstrings
- Extract functions (DRY, Single Responsibility)
- Simplify logic (early returns, reduce nesting)
- Run test → Verify STILL PASSES

### Step 3: Edge Case Testing
Add tests for:
- Empty inputs
- Max length inputs
- Invalid types
- User isolation (cross-user access)

### Step 4: Integration Testing
Test end-to-end flows:
- CLI command → service → database → response (Phase I)
- API route → service → database → JSON response (Phase II)

### Step 5: Constitutional Compliance Validation
Verify against [principles.md](principles.md):
- [ ] User isolation enforced (ALL queries filter by user_id)
- [ ] Type hints on all functions (mypy --strict passes)
- [ ] Docstrings on all functions (Google style, ≥95% coverage)
- [ ] Test coverage ≥80% (pytest --cov)
- [ ] Database models have constitutional fields (id, user_id, timestamps)
- [ ] Performance SLOs met (p95 latency from plan.md)

### Step 6: Quality Validation
Run quality checks:
```bash
mypy backend/ --strict          # Type checking
black backend/ --check          # Formatting
flake8 backend/                 # Linting
pytest tests/ --cov=backend --cov-fail-under=80  # Tests + coverage
```

### Step 7: Acceptance Validation
Verify all Given/When/Then scenarios from spec.md pass

### Step 8: Commit
Use conventional commit format with details

---

## Examples: Good vs. Bad Implementation

### ❌ Bad Implementation (Violates Principles)

```python
# ❌ No tests written first (violates TDD)
def create_task(user, title):
    # ❌ No type hints (violates Principle IX)
    # ❌ No docstring (violates Principle IX)
    # ❌ No validation
    # ❌ No user isolation (SECURITY VIOLATION!)
    t = Task(user=user, title=title)
    db.add(t)
    db.commit()
    return t

# ❌ No tests exist (violates Principle X)
```

**Problems**:
- No TDD (code before tests)
- No type hints or docstrings
- No validation (empty title accepted)
- Missing user isolation (queries not scoped by user_id)
- No tests (0% coverage)

### ✅ Good Implementation (Follows Principles)

```python
# STEP 1: Write test FIRST (TDD - Red)
def test_create_task_with_valid_title(test_db):
    """Test creating task with valid title."""
    task = create_task(user_id="alice", title="Buy milk")
    assert task.title == "Buy milk"
    assert task.user_id == "alice"
    assert task.completed is False
    # Run test → FAILS ✅

# STEP 2: Implement (TDD - Green)
def create_task(user_id: str, title: str) -> Task:
    """Create a new task for the specified user.

    Args:
        user_id: The ID of the user creating the task
        title: The task title (1-200 characters)

    Returns:
        Task: The newly created task

    Raises:
        ValidationError: If title is empty or >200 characters
        ValueError: If user_id is empty

    Example:
        >>> task = create_task("alice", "Buy milk")
        >>> task.title
        'Buy milk'
    """
    _validate_user_id(user_id)
    _validate_title(title)

    task = Task(user_id=user_id, title=title, completed=False)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
    # Run test → PASSES ✅

def _validate_user_id(user_id: str) -> None:
    """Validate user_id is not empty."""
    if not user_id:
        raise ValueError("user_id cannot be empty")

def _validate_title(title: str) -> None:
    """Validate title is 1-200 characters."""
    if not title:
        raise ValidationError("Title cannot be empty")
    if len(title) > 200:
        raise ValidationError("Title must be 1-200 characters")

# STEP 3: Edge case tests
def test_create_task_empty_title_fails(test_db):
    with pytest.raises(ValidationError):
        create_task("alice", "")

def test_create_task_long_title_fails(test_db):
    with pytest.raises(ValidationError):
        create_task("alice", "a" * 201)

# STEP 4: User isolation test (CRITICAL)
def test_user_isolation_cross_user_read(test_db):
    """Test alice cannot read bob's tasks."""
    bob_task = create_task("bob", "Bob's task")
    alice_tasks = list_tasks("alice")
    assert bob_task not in alice_tasks

# Coverage: 95% ✅
```

**Why Good**:
- ✅ TDD followed (test first, then implement)
- ✅ Type hints everywhere (mypy --strict passes)
- ✅ Google-style docstrings (≥95% coverage)
- ✅ Input validation (empty, max length)
- ✅ User isolation enforced (queries filter by user_id)
- ✅ Test coverage 95% (exceeds 80% requirement)
- ✅ DRY (extracted _validate_* functions)

---

## Constitutional Alignment

This RI enforces:

| Principle | How RI Enforces |
|-----------|-----------------|
| **I: Spec-Driven** | Code implements spec.md exactly (acceptance scenarios validate) |
| **II: User Isolation** | ALL queries filter by user_id, cross-user tests required |
| **VI: Database Standards** | Models include id, user_id, created_at, updated_at |
| **IX: Code Quality** | Type hints, docstrings (Google style), linters pass |
| **X: Testing** | TDD mandatory, coverage ≥80%, all test categories |
| **XII: Security** | Input validation, no secrets, SQL injection prevention |
| **XVIII: Performance** | SLO compliance, database optimization, async patterns |

---

## Version History

### v1.0.0 (2025-12-12)
- Initial RI for Phase Implementer
- Created P+Q+P framework (persona, questions, principles)
- Documented 24 implementation questions across 6 categories
- Established TDD standards (red-green-refactor), coverage (≥80%), quality (DRY, SOLID)
- Defined constitutional enforcement (user isolation, type safety, documentation)
- Integrated with /sp.implement command and phase-implementer subagent

---

## Related RI

- **Spec Writer RI**: Takes user input, creates spec.md (WHAT to build)
- **Architect RI**: Takes spec.md, creates plan.md (HOW to architect)
- **Task Planner RI**: Takes spec.md + plan.md, creates tasks.md (step-by-step)
- **Test Guardian RI**: Reviews test quality, coverage, finds gaps (future)

---

## Files in This RI

```
.specify/ri/skills/phase-implementer/
├── README.md          ← You are here (overview)
├── persona.md         ← Who the agent is, TDD expertise, style
├── questions.md       ← 24 implementation questions
└── principles.md      ← TDD, code quality, security, performance standards
```

---

## Feedback and Improvement

This RI evolves based on usage. After using Phase Implementer RI:

**Capture**:
- Did TDD workflow help or hinder? (red-green-refactor cycle)
- Were constitutional checks sufficient? (user isolation, coverage, type safety)
- Were the questions helpful for implementation planning?
- What would improve this RI?

**Update**:
- Add new questions if gaps discovered (e.g., async patterns, caching strategies)
- Refine principles if ambiguity found (e.g., test organization, error handling)
- Update persona if communication issues arise (too detailed? not enough examples?)
- Version bump (MAJOR, MINOR, PATCH)

---

**Next Steps**:
1. Link RI to existing skills and subagents (update SKILL.md, subagent .md files)
2. Create PHR for RI setup session
3. Begin Phase I implementation using these 3 RI (spec-writer, architect, phase-implementer)

**Remaining RI** (create after Phase I): 6 total (test-guardian, security-auditor, task-planner, requirements-clarifier, constitution-reviewer, adr-creator)
