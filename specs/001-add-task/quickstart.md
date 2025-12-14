# Quickstart Guide: Add Task Feature

**Feature**: Add Task (Phase I Console)
**Branch**: `001-add-task`
**Date**: 2025-12-12

---

## Installation

### Prerequisites

- Python 3.13+
- UV package manager

### Setup

```bash
# Clone repository
cd todo-evolution

# Install dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# OR
.venv\Scripts\activate  # Windows
```

---

## Basic Usage

### Create Your First Task

```bash
$ todo add --user alice "Buy groceries"
✓ Task created successfully
  ID: 1
  Title: "Buy groceries"
  User: alice
  Created: 2025-12-12 10:30:00 UTC
```

### Create Another Task

```bash
$ todo add --user alice "Call dentist"
✓ Task created successfully
  ID: 2
  Title: "Call dentist"
  User: alice
  Created: 2025-12-12 10:31:00 UTC
```

---

## Common Patterns

### Tasks with Special Characters

```bash
# Emoji in title
$ todo add --user alice "Buy 🥛 milk"
✓ Task created successfully
  ID: 3
  Title: "Buy 🥛 milk"
  User: alice
  Created: 2025-12-12 10:32:00 UTC

# Quotes in title
$ todo add --user alice "Read 'The Great Gatsby'"
✓ Task created successfully
  ID: 4
  Title: "Read 'The Great Gatsby'"
  User: alice
  Created: 2025-12-12 10:33:00 UTC
```

### Long Task Titles

```bash
# Maximum length: 200 characters
$ todo add --user alice "$(printf 'a%.0s' {1..200})"
✓ Task created successfully
  ID: 5
  Title: "aaaaaaa..." (200 chars)
  User: alice
  Created: 2025-12-12 10:34:00 UTC
```

---

## Multi-User Usage

### User Isolation Demo

```bash
# Alice creates task
$ todo add --user alice "Alice's personal task"
✓ Task created successfully
  ID: 6
  Title: "Alice's personal task"
  User: alice
  Created: 2025-12-12 10:35:00 UTC

# Bob creates task (separate user)
$ todo add --user bob "Bob's work task"
✓ Task created successfully
  ID: 7
  Title: "Bob's work task"
  User: bob
  Created: 2025-12-12 10:36:00 UTC

# Users see only their own tasks (verified via `todo list` - future feature)
```

---

## Error Handling

### Empty Title

```bash
$ todo add --user alice ""
Error: Title cannot be empty
Exit code: 1
```

### Title Too Long (>200 characters)

```bash
$ todo add --user alice "$(printf 'a%.0s' {1..201})"
Error: Title must be 1-200 characters
Exit code: 1
```

### Missing --user Flag

```bash
$ todo add "Buy milk"
Error: Missing option '--user'
Exit code: 2
```

### Empty User ID

```bash
$ todo add --user "" "Buy milk"
Error: User ID cannot be empty
Exit code: 1
```

---

## Help & Documentation

### Command Help

```bash
$ todo add --help
Usage: todo add [OPTIONS] TITLE

  Create a new task with the given title.

  Examples:
      todo add --user alice "Buy groceries"
      todo add --user bob "Call dentist at 2pm"

Options:
  --user TEXT  User ID (owner of the task)  [required]
  --help       Show this message and exit.
```

---

## Database Location

Tasks are stored in `todo.db` in the current working directory:

```bash
$ ls -lh todo.db
-rw-r--r-- 1 user user 12K Dec 12 10:30 todo.db
```

**Important**: `todo.db` is gitignored. Do not commit this file.

---

## Testing

### Run Tests

```bash
# All tests
$ pytest

# Unit tests only
$ pytest tests/unit/

# Integration tests only
$ pytest tests/integration/

# With coverage
$ pytest --cov=src --cov-report=term-missing
```

### Expected Coverage

- Target: ≥80% (Constitutional Principle X)
- Unit tests: ~90% coverage
- Integration tests: ~80% coverage

---

## Troubleshooting

### Issue: "Database is locked"

**Cause**: Multiple processes writing to `todo.db` simultaneously

**Solution**: Wait and retry. WAL mode reduces lock contention.

```bash
# Retry command
$ todo add --user alice "Buy groceries"
```

---

### Issue: "Module not found: src"

**Cause**: Virtual environment not activated or dependencies not installed

**Solution**:
```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
uv sync
```

---

### Issue: "Python version not supported"

**Cause**: Python <3.13 installed

**Solution**: Install Python 3.13+
```bash
# Check Python version
$ python --version
Python 3.13.0

# If <3.13, install via pyenv or system package manager
$ pyenv install 3.13.0
$ pyenv global 3.13.0
```

---

## Next Features (Future)

- `todo list --user <user_id>` - List all tasks
- `todo complete --user <user_id> <task_id>` - Mark task complete
- `todo delete --user <user_id> <task_id>` - Delete task
- `todo update --user <user_id> <task_id> <new_title>` - Edit task title

---

## Related Documentation

- [Spec](spec.md) - Feature requirements and user stories
- [Plan](plan.md) - Architectural decisions
- [Data Model](data-model.md) - Task entity schema
- [CLI Contract](contracts/add-task.md) - Command specification

---

## Support

For issues or questions:
1. Check [spec.md](spec.md) for requirements clarification
2. Check [plan.md](plan.md) for architecture details
3. Run tests: `pytest -v` for detailed output
4. Check database: `sqlite3 todo.db "SELECT * FROM tasks;"`

---

**Ready to implement!** Proceed to `/sp.tasks` to generate implementation tasks.
