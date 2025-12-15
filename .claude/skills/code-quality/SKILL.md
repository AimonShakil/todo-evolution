---
name: code-quality
description: Enforce code quality standards from constitution including type hints, docstrings, formatting, async patterns, and linting. Use when writing or reviewing Python or TypeScript code. Applies Constitutional Principle IX.
allowed-tools: Read, Bash, Grep
---

# Code Quality Enforcer Skill

Enforces constitutional code quality requirements (Principle IX: Code Quality Standards).

## Python Standards (Backend)

### Type Hints (MANDATORY)
- **Requirement**: Python 3.13+ type hints on ALL functions and classes
- **Verification**: `mypy --strict`

```python
# ✅ GOOD
def create_task(user_id: str, title: str) -> Task:
    """Create a new task for the user."""
    pass

# ❌ BAD - missing type hints
def create_task(user_id, title):
    pass
```

### Docstrings (Google Style)
- **Requirement**: Docstrings for all public functions/classes
- **Coverage**: Minimum 95%
- **Verification**: `pydocstyle` or `interrogate`

```python
# ✅ GOOD
def create_task(user_id: str, title: str) -> Task:
    """Create a new task for the user.

    Args:
        user_id: The user's unique identifier
        title: The task title (1-200 characters)

    Returns:
        The created Task object

    Raises:
        ValueError: If title is empty or too long
    """
    pass

# ❌ BAD - missing docstring
def create_task(user_id: str, title: str) -> Task:
    pass
```

### Maximum Function Length
- **Limit**: 50 lines (excluding docstrings, blank lines, comments)
- **Verification**: `pylint` or `flake8` with max-complexity rules

```python
# ✅ GOOD - focused function
def validate_task_title(title: str) -> str:
    """Validate task title length and content."""
    if not title or len(title.strip()) == 0:
        raise ValueError("Title cannot be empty")
    if len(title) > 200:
        raise ValueError("Title must be 1-200 characters")
    return title.strip()

# ❌ BAD - function too long (>50 lines)
def create_task_with_validation_and_persistence(...):
    # 80 lines of code mixing validation, business logic, persistence
    pass
```

### PEP 8 Compliance
- **Enforcer**: `black` formatter (automatic)
- **Linter**: `flake8`

```bash
# Format code
black .

# Check formatting
black --check .

# Lint code
flake8 .
```

### Async/Await for I/O Operations
- **Requirement**: All I/O operations must be async
- **Verification**: Code review - no synchronous database calls, HTTP requests, file I/O

```python
# ✅ GOOD - async database call
async def get_task(task_id: int, user_id: str) -> Task | None:
    """Retrieve a task by ID for the user."""
    async with AsyncSession(engine) as session:
        result = await session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        )
        return result.first()

# ❌ BAD - synchronous database call
def get_task(task_id: int, user_id: str) -> Task | None:
    with Session(engine) as session:
        result = session.exec(...)  # Blocking I/O
        return result.first()
```

### No Bare Except Clauses
- **Requirement**: Always specify exception type
- **Verification**: `flake8` rule E722

```python
# ✅ GOOD - specific exception
try:
    task = get_task(task_id)
except TaskNotFound as e:
    logger.error(f"Task not found: {e}")
    raise

# ❌ BAD - bare except
try:
    task = get_task(task_id)
except:  # Catches KeyboardInterrupt, SystemExit - dangerous!
    pass
```

### UV Dependency Management
- **Requirement**: Use UV with `pyproject.toml`
- **Verification**: `pyproject.toml` exists, no `requirements.txt`

```toml
# pyproject.toml
[project]
name = "todo-backend"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = [
    "fastapi>=0.100.0",
    "sqlmodel>=0.0.14",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "mypy>=1.7.0",
    "black>=23.0.0",
    "flake8>=6.0.0",
]
```

## TypeScript Standards (Frontend - Phase II+)

### Strict Mode
- **Requirement**: `"strict": true` in `tsconfig.json`
- **Verification**: Check config file

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true
  }
}
```

### Explicit Props Typing
- **Requirement**: All component props explicitly typed
- **Verification**: `tsc --noImplicitAny`

```typescript
// ✅ GOOD
interface TaskListProps {
  userId: string;
  tasks: Task[];
  onTaskComplete: (taskId: number) => Promise<void>;
}

export function TaskList({ userId, tasks, onTaskComplete }: TaskListProps) {
  // ...
}

// ❌ BAD - implicit any
export function TaskList({ userId, tasks, onTaskComplete }) {
  // ...
}
```

### Server Components by Default
- **Requirement**: Mark `'use client'` only when needed
- **Verification**: Code review - justify client components

```typescript
// ✅ GOOD - Server Component (default)
export default async function TasksPage({ params }: { params: { userId: string } }) {
  const tasks = await fetchTasks(params.userId);
  return <TaskList tasks={tasks} />;
}

// ✅ GOOD - Client Component (justified interactivity)
'use client';

import { useState } from 'react';

export function TaskForm() {
  const [title, setTitle] = useState('');
  // Interactive form requires client component
}

// ❌ BAD - unnecessary client component
'use client';

export function TaskList({ tasks }: { tasks: Task[] }) {
  // No interactivity, should be server component
  return <ul>{tasks.map(...)}</ul>;
}
```

### Tailwind CSS (No Inline Styles)
- **Requirement**: Use Tailwind classes, avoid inline styles
- **Verification**: ESLint rule `no-inline-styles`

```typescript
// ✅ GOOD - Tailwind classes
<button className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
  Add Task
</button>

// ❌ BAD - inline styles
<button style={{ padding: '8px 16px', backgroundColor: 'blue', color: 'white' }}>
  Add Task
</button>
```

### API Client Abstraction
- **Requirement**: Centralized API client in `/lib/api.ts`
- **Verification**: No direct `fetch()` in components

```typescript
// ✅ GOOD - lib/api.ts
export class TodoAPI {
  constructor(private baseUrl: string) {}

  async getTasks(userId: string): Promise<Task[]> {
    const response = await fetch(`${this.baseUrl}/api/${userId}/tasks`);
    if (!response.ok) throw new Error('Failed to fetch tasks');
    return response.json();
  }
}

// ✅ GOOD - component uses API client
import { todoApi } from '@/lib/api';

export async function TasksPage({ userId }: { userId: string }) {
  const tasks = await todoApi.getTasks(userId);
  return <TaskList tasks={tasks} />;
}

// ❌ BAD - direct fetch in component
export async function TasksPage({ userId }: { userId: string }) {
  const response = await fetch(`/api/${userId}/tasks`);  // No abstraction
  const tasks = await response.json();
  return <TaskList tasks={tasks} />;
}
```

## Automated Quality Gates (CI/CD)

All quality checks MUST pass before merge.

### Python Quality Pipeline
```bash
# Formatting check
black --check backend/

# Type checking
mypy --strict backend/

# Linting
flake8 backend/

# Docstring coverage
interrogate -v backend/ --fail-under 95

# Security check (bonus)
bandit -r backend/
```

### TypeScript Quality Pipeline (Phase II+)
```bash
# Type checking
tsc --noImplicitAny

# Linting
eslint frontend/

# Formatting check
prettier --check frontend/

# Build check
npm run build
```

### Sample CI/CD Workflow (GitHub Actions)

```yaml
# .github/workflows/quality.yml
name: Code Quality

on: [push, pull_request]

jobs:
  python-quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.13'
      - name: Install dependencies
        run: |
          pip install uv
          uv pip install -e .[dev]
      - name: Format check
        run: black --check backend/
      - name: Type check
        run: mypy --strict backend/
      - name: Lint
        run: flake8 backend/
      - name: Docstring coverage
        run: interrogate -v backend/ --fail-under 95

  typescript-quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '20'
      - name: Install dependencies
        run: npm ci
      - name: Type check
        run: tsc --noImplicitAny
      - name: Lint
        run: eslint .
      - name: Format check
        run: prettier --check .
```

## MCP Server Integration (Context7)

When reviewing code that uses external libraries, verify against official documentation:

```
User: "Review this FastAPI endpoint implementation"
  ↓
You: Use mcp__context7__resolve-library-id for "fastapi"
  ↓
You: Use mcp__context7__get-library-docs with topic="routing"
  ↓
You: Compare implementation against official FastAPI patterns
  ↓
You: Suggest corrections if deviating from best practices
```

## Common Code Smells to Detect

### Python
```python
# ❌ Missing type hints
def process(data):
    return data.upper()

# ❌ Bare except
try:
    result = risky_operation()
except:
    pass

# ❌ Synchronous I/O in async context
async def handler():
    data = requests.get(url)  # Should use httpx async

# ❌ Mutable default argument
def add_item(items=[]):  # Dangerous!
    items.append(1)

# ❌ No docstring
def complex_algorithm(x, y, z):
    # 30 lines of code
    pass
```

### TypeScript (Phase II+)
```typescript
// ❌ Implicit any
function process(data) {
  return data.toUpperCase();
}

// ❌ Unnecessary client component
'use client';
function StaticContent() {
  return <div>Hello</div>;  // No interactivity!
}

// ❌ Inline styles
<div style={{ color: 'red' }}>Error</div>

// ❌ Direct fetch in component
async function Component() {
  const data = await fetch('/api/data');  // Use API client!
}
```

## Pre-Commit Hooks (Optional but Recommended)

```bash
# Install pre-commit
pip install pre-commit

# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.0
    hooks:
      - id: black
        language_version: python3.13

  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.0
    hooks:
      - id: mypy
        args: [--strict]

# Install hooks
pre-commit install
```

## Quality Checklist for Code Review

Before approving any code:

- [ ] **Type hints**: All functions/classes have type annotations
- [ ] **Docstrings**: All public APIs documented (Google style)
- [ ] **PEP 8**: Code formatted with `black`, passes `flake8`
- [ ] **Function length**: No functions > 50 lines
- [ ] **Async I/O**: All database/network/file operations are async
- [ ] **Exception handling**: No bare `except:` clauses
- [ ] **Dependencies**: Using UV with `pyproject.toml`
- [ ] **No secrets**: No API keys, passwords in code
- [ ] **Imports organized**: Standard lib → third-party → local
- [ ] **Tests exist**: New code has corresponding tests

## Tools Summary

| Tool | Purpose | Command | Pass Criteria |
|------|---------|---------|---------------|
| **black** | Formatting | `black --check .` | All files formatted |
| **mypy** | Type checking | `mypy --strict .` | No type errors |
| **flake8** | Linting | `flake8 .` | No lint warnings |
| **interrogate** | Docstrings | `interrogate --fail-under 95 .` | ≥95% coverage |
| **bandit** | Security | `bandit -r .` | No security issues |
| **pytest** | Testing | `pytest --cov --cov-fail-under=80` | ≥80% coverage |

## MCP Context7 for Library Patterns

Before implementing with unfamiliar library, fetch official patterns:

```
Planning FastAPI routes?
  → mcp__context7__get-library-docs("/fastapi/fastapi", topic="routing")

Using SQLModel?
  → mcp__context7__get-library-docs("/tiangolo/sqlmodel", topic="queries")

Implementing Next.js pages?
  → mcp__context7__get-library-docs("/vercel/next.js", topic="app-router")
```

This ensures code follows official best practices, not outdated patterns.

## Constitutional Compliance

Principle IX states: "All code MUST adhere to language-specific quality standards with automated enforcement."

**Zero tolerance** for:
- Missing type hints
- Missing docstrings on public APIs
- PEP 8 violations
- Synchronous I/O in async contexts
- Bare except clauses

**All quality gates must pass** before code merges to main.
