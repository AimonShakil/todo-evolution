# Quickstart: Phase I - Console Todo App

**Feature**: Phase I - Console Todo App
**Date**: 2025-12-08
**Branch**: 002-phase-i-console-app

---

## Overview

This quickstart guide helps you set up and use the Phase I console todo application. You'll be able to add, view, update, delete, and mark tasks as complete using simple command-line commands.

**Key Features**:
- ✅ Multi-user task management (username-based isolation)
- ✅ Persistent storage (SQLite database)
- ✅ Unicode support (emojis in task titles)
- ✅ Future-proof data model (ready for Phase II-V migration)

---

## Prerequisites

- **Python**: 3.13 or higher
- **Terminal**: bash, zsh, PowerShell, or cmd with UTF-8 support
- **Permissions**: Read/write access to current directory (for `todo.db` file)

---

## Installation

### 1. Clone Repository (if applicable)

```bash
git clone <repository-url>
cd todo-evolution
git checkout 002-phase-i-console-app
```

### 2. Install Dependencies

```bash
# Using UV (recommended for Python 3.13+)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .

# OR using pip
python3.13 -m venv .venv
source .venv/bin/activate
pip install -e .
```

**Dependencies** (defined in `pyproject.toml`):
- SQLModel (ORM with Pydantic validation)
- Click (CLI framework)
- pytest (testing)
- pytest-cov (coverage)
- mypy (type checking)
- black (formatting)
- flake8 (linting)

### 3. Verify Installation

```bash
todo --help
```

Expected output:
```
Todo CLI - Multi-user task management

Usage:
  todo [COMMAND] [OPTIONS]
...
```

---

## Quick Start (5 Minutes)

### Step 1: Add Your First Task

```bash
todo add --username alice "Buy groceries"
```

Output:
```
✓ Task added with ID 1
```

**What happened**:
- SQLite database (`todo.db`) auto-created in current directory
- Task stored with `user_id = "alice"`, `completed = False`
- All Phase V fields (description, priority, tags, due_date, recurrence_pattern) set to NULL

### Step 2: View Your Tasks

```bash
todo view --username alice
```

Output:
```
ID | Title              | Completed | Created
---|--------------------|-----------|---------
1  | Buy groceries      | ✗         | 2025-12-08 10:30:00
```

### Step 3: Mark Task Complete

```bash
todo complete --username alice 1
```

Output:
```
✓ Task 1 marked complete
```

### Step 4: View Updated Status

```bash
todo view --username alice
```

Output:
```
ID | Title              | Completed | Created
---|--------------------|-----------|---------
1  | Buy groceries      | ✓         | 2025-12-08 10:30:00
```

### Step 5: Add More Tasks

```bash
todo add --username alice "Finish report"
todo add --username alice "Call dentist"
```

---

## All Commands Reference

### 1. Add Task

```bash
todo add --username <USERNAME> "<TITLE>"
```

**Examples**:
```bash
# Basic task
todo add --username alice "Buy groceries"

# Unicode and emojis
todo add --username bob "Buy milk & eggs 🥛"

# Maximum length (200 characters)
todo add --username charlie "This is a very long task title..."
```

**Validation**:
- Title: 1-200 characters
- Username: Non-empty string

### 2. View Tasks

```bash
todo view --username <USERNAME>
```

**Example**:
```bash
todo view --username alice
```

**Output Format**:
- Table with columns: ID, Title, Completed (✓/✗), Created
- Empty list shows: "No tasks found"

### 3. Update Task Title

```bash
todo update --username <USERNAME> <TASK_ID> "<NEW_TITLE>"
```

**Example**:
```bash
todo update --username alice 1 "Buy organic groceries"
```

**Validation**:
- New title: 1-200 characters
- Task must exist and belong to user

### 4. Delete Task

```bash
todo delete --username <USERNAME> <TASK_ID>
```

**Example**:
```bash
todo delete --username alice 1
```

**Warning**: Deletion is permanent (no undo)

### 5. Mark Complete/Incomplete (Toggle)

```bash
todo complete --username <USERNAME> <TASK_ID>
```

**Examples**:
```bash
# Mark task 1 complete
todo complete --username alice 1

# Toggle back to incomplete
todo complete --username alice 1
```

**Behavior**: If task is incomplete → mark complete. If complete → mark incomplete.

### 6. Help

```bash
todo --help
# or
todo help
```

---

## Multi-User Support

Each user specifies their username to maintain data isolation:

```bash
# Alice's tasks
todo add --username alice "Alice's task 1"
todo add --username alice "Alice's task 2"
todo view --username alice
# Output: Shows only Alice's 2 tasks

# Bob's tasks
todo add --username bob "Bob's task 1"
todo view --username bob
# Output: Shows only Bob's 1 task

# Isolation verified: Alice cannot see Bob's tasks
todo view --username alice
# Output: Shows only Alice's 2 tasks (Bob's task not visible)
```

**Security Note**: Phase I uses simple username strings (no authentication). Phase II will add Better Auth with password protection.

---

## Database Management

### Database Location

- **File**: `todo.db` (SQLite database)
- **Location**: Current working directory
- **Auto-Created**: Yes (on first run)

### Backup Database

```bash
# Manual backup
cp todo.db todo.db.backup

# Restore from backup
cp todo.db.backup todo.db
```

### View Database Schema

```bash
sqlite3 todo.db ".schema task"
```

Output:
```sql
CREATE TABLE task (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    title TEXT NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -- Future-proof Phase V fields (nullable)
    description TEXT,
    priority TEXT,
    tags TEXT,
    due_date DATETIME,
    recurrence_pattern TEXT
);
CREATE INDEX idx_task_user_id ON task(user_id);
```

### Reset Database (Delete All Data)

```bash
rm todo.db
# Next command will auto-create fresh database
```

---

## Troubleshooting

### Issue: "Error: Unable to connect to database"

**Cause**: `todo.db` file deleted while app was running

**Solution**:
1. Exit the app
2. Restart: `todo view --username <your-username>`
3. Database will auto-create

### Issue: "Error: Username required"

**Cause**: Forgot to specify `--username` option

**Solution**: Add `--username <your-username>` to command
```bash
# Wrong
todo view

# Correct
todo view --username alice
```

### Issue: "Error: Title must be 1-200 characters"

**Cause**: Title is empty or exceeds 200 characters

**Solution**: Shorten title to 200 characters or less
```bash
# Wrong (empty)
todo add --username alice ""

# Correct
todo add --username alice "Buy groceries"
```

### Issue: "Task X not found"

**Possible Causes**:
1. Task ID doesn't exist
2. Task belongs to different user (user isolation enforced)

**Solution**: Verify task ID with `todo view --username <your-username>`

---

## Performance Notes

- **Startup Time**: <2 seconds with 1,000 tasks (SC-009)
- **Operation Time**: <500ms per operation with 10,000 tasks (SC-010)
- **Database Indexing**: `user_id` column indexed for fast filtering

**Scale Tested**: Up to 10,000 tasks per user without performance degradation

---

## Development Workflow

### Run Tests

```bash
# All tests with coverage
pytest --cov=src --cov-fail-under=80

# Specific test category
pytest tests/unit/
pytest tests/integration/
pytest tests/contract/
```

### Type Checking

```bash
mypy --strict src/
```

### Code Formatting

```bash
# Check formatting
black --check src/

# Auto-format
black src/
```

### Linting

```bash
flake8 src/
```

---

## Phase II Migration Preview

Phase I prepares for Phase II web app migration:

**Data Model**:
- ✅ Future-proof schema (all Phase V fields already in database as nullable)
- ✅ `user_id` string → will migrate to integer foreign key in Phase II

**User Isolation Pattern**:
- ✅ `WHERE user_id = ?` (Phase I console) → `/api/{user_id}/tasks` (Phase II REST API)

**Stateless Architecture**:
- ✅ Database-backed state (no in-memory) → Ready for Phase II distributed web app

---

## Next Steps

1. **Use the App**: Add your real tasks and test all commands
2. **Verify Isolation**: Create tasks for multiple users (alice, bob, charlie)
3. **Test Edge Cases**: Try empty titles, 200-char titles, Unicode emojis, deleting all tasks
4. **Run Tests**: Ensure 80% coverage and all quality gates pass
5. **Ready for Phase II**: When comfortable, proceed to Phase II web app specification

---

**Quickstart Complete** - You're ready to use the Phase I console todo app!
