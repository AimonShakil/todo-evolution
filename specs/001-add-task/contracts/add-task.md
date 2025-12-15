# CLI Contract: `todo add`

**Command**: `todo add`
**Feature**: Add Task (Phase I Console)
**Branch**: `001-add-task`
**Date**: 2025-12-12
**Phase**: Phase 1 (Contracts)

---

## Command Signature

```bash
todo add --user <user_id> <title>
```

---

## Parameters

### `--user` (Required Option)

- **Type**: String
- **Required**: YES (spec FR-001)
- **Validation**:
  - Cannot be empty string (spec FR-003)
  - Max length: 255 characters
  - Whitespace-only values rejected
- **Purpose**: Identifies which user owns the task (user isolation - Principle II)
- **Example Values**: `"alice"`, `"bob123"`, `"user@example.com"`
- **Error if Missing**: Exit code 2, message: `Error: Missing option '--user'` (spec FR-010)

### `<title>` (Required Argument)

- **Type**: String
- **Required**: YES (spec FR-001)
- **Validation**:
  - Min length: 1 character (spec FR-002)
  - Max length: 200 characters (spec FR-002)
  - Emojis allowed (spec edge case)
  - Special characters allowed (quotes, apostrophes)
  - Newlines/tabs sanitized or rejected
- **Purpose**: Task description
- **Example Values**:
  - `"Buy groceries"`
  - `"Call dentist at 2pm tomorrow"`
  - `"Buy 🥛 milk"` (emoji)
  - `"Read 'The Great Gatsby'"` (quotes)
- **Error if Empty**: Exit code 1, message: `Title cannot be empty` (spec FR-009)
- **Error if Too Long**: Exit code 1, message: `Title must be 1-200 characters` (spec FR-009)

---

## Success Response

**Exit Code**: 0 (spec FR-010)

**Output Format** (spec FR-008):
```
✓ Task created successfully
  ID: <task_id>
  Title: "<title>"
  User: <user_id>
  Created: <timestamp in YYYY-MM-DD HH:MM:SS UTC format>
```

**Example**:
```
✓ Task created successfully
  ID: 42
  Title: "Buy groceries"
  User: alice
  Created: 2025-12-12 10:30:00 UTC
```

---

## Error Responses

### Validation Errors (Exit Code 1)

| Error Condition | Exit Code | Message | Spec Reference |
|-----------------|-----------|---------|----------------|
| Empty title | 1 | `Title cannot be empty` | FR-002, FR-009 |
| Title too long (>200 chars) | 1 | `Title must be 1-200 characters` | FR-002, FR-009 |
| Empty user_id | 1 | `User ID cannot be empty` | FR-003, FR-009 |
| Database error | 1 | `Failed to create task: <error_message>` | FR-010 |

**Error Output Format**:
```
Error: <error_message>
```
**Error Stream**: stderr (not stdout)

### Missing Required Option (Exit Code 2)

| Error Condition | Exit Code | Message | Spec Reference |
|-----------------|-----------|---------|----------------|
| Missing `--user` flag | 2 | `Error: Missing option '--user'` | FR-010 |

**Error Output Format**:
```
Error: Missing option '--user'
```
**Error Stream**: stderr (not stdout)

---

## Examples

### Example 1: Successful Task Creation

**Command**:
```bash
$ todo add --user alice "Buy groceries"
```

**Output** (stdout, exit code 0):
```
✓ Task created successfully
  ID: 1
  Title: "Buy groceries"
  User: alice
  Created: 2025-12-12 10:30:00 UTC
```

**Side Effects**:
- Task record created in `todo.db` with:
  - id=1 (auto-generated)
  - user_id="alice"
  - title="Buy groceries"
  - completed=false
  - created_at=2025-12-12T10:30:00 UTC
  - updated_at=2025-12-12T10:30:00 UTC

---

### Example 2: Empty Title (Validation Error)

**Command**:
```bash
$ todo add --user alice ""
```

**Output** (stderr, exit code 1):
```
Error: Title cannot be empty
```

**Side Effects**: No task created

---

### Example 3: Title Too Long (Validation Error)

**Command**:
```bash
$ todo add --user alice "$(python -c 'print("a" * 201)')"
```

**Output** (stderr, exit code 1):
```
Error: Title must be 1-200 characters
```

**Side Effects**: No task created

---

### Example 4: Missing --user Flag

**Command**:
```bash
$ todo add "Buy groceries"
```

**Output** (stderr, exit code 2):
```
Error: Missing option '--user'
```

**Side Effects**: No task created

---

### Example 5: Empty User ID

**Command**:
```bash
$ todo add --user "" "Buy milk"
```

**Output** (stderr, exit code 1):
```
Error: User ID cannot be empty
```

**Side Effects**: No task created

---

### Example 6: Title with Emoji (Edge Case)

**Command**:
```bash
$ todo add --user alice "Buy 🥛 milk"
```

**Output** (stdout, exit code 0):
```
✓ Task created successfully
  ID: 2
  Title: "Buy 🥛 milk"
  User: alice
  Created: 2025-12-12 10:31:00 UTC
```

**Side Effects**: Task created with emoji preserved

---

### Example 7: Title with Special Characters (Edge Case)

**Command**:
```bash
$ todo add --user alice "Read 'The Great Gatsby'"
```

**Output** (stdout, exit code 0):
```
✓ Task created successfully
  ID: 3
  Title: "Read 'The Great Gatsby'"
  User: alice
  Created: 2025-12-12 10:32:00 UTC
```

**Side Effects**: Task created with quotes preserved

---

### Example 8: Maximum Length Title (Boundary)

**Command**:
```bash
$ todo add --user alice "$(python -c 'print("x" * 200)')"
```

**Output** (stdout, exit code 0):
```
✓ Task created successfully
  ID: 4
  Title: "xxxxxxxxxxxx..." (200 chars)
  User: alice
  Created: 2025-12-12 10:33:00 UTC
```

**Side Effects**: Task created with 200-character title

---

## Implementation Reference

### Click Command (`src/cli/commands/add.py`)

```python
import click
from src.services.task_service import TaskService
from src.lib.validators import validate_title, validate_user_id

@click.command()
@click.option('--user', required=True, help='User ID (owner of the task)')
@click.argument('title')
def add(user: str, title: str) -> None:
    """Create a new task with the given title.

    Examples:
        todo add --user alice "Buy groceries"
        todo add --user bob "Call dentist at 2pm"
    """
    try:
        # Validation (Principle IX: input validation)
        validate_user_id(user)  # Raises ValueError if empty
        validate_title(title)    # Raises ValueError if empty or >200 chars

        # Create task (user-scoped service call)
        service = TaskService()
        task = service.create_task(user_id=user, title=title)

        # Success output (spec FR-008)
        click.echo("✓ Task created successfully")
        click.echo(f"  ID: {task.id}")
        click.echo(f"  Title: \"{task.title}\"")
        click.echo(f"  User: {task.user_id}")
        click.echo(f"  Created: {task.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}")

    except ValueError as e:
        # Validation errors (spec FR-009, FR-010 exit code 1)
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    except Exception as e:
        # Database errors (spec FR-010 exit code 1)
        click.echo(f"Failed to create task: {e}", err=True)
        raise SystemExit(1)
```

---

## Test Cases

### Integration Tests (`tests/integration/test_add_task_integration.py`)

```python
from click.testing import CliRunner
from src.cli.commands.add import add

def test_add_task_success():
    """Test successful task creation (User Story 1, Scenario 1)."""
    runner = CliRunner()
    result = runner.invoke(add, ['--user', 'alice', 'Buy groceries'])

    assert result.exit_code == 0
    assert "✓ Task created successfully" in result.output
    assert 'Title: "Buy groceries"' in result.output
    assert "User: alice" in result.output

def test_add_task_empty_title():
    """Test empty title validation (User Story 2, Scenario 1)."""
    runner = CliRunner()
    result = runner.invoke(add, ['--user', 'alice', ''])

    assert result.exit_code == 1
    assert "Error: Title cannot be empty" in result.output

def test_add_task_title_too_long():
    """Test title length validation (User Story 2, Scenario 2)."""
    runner = CliRunner()
    long_title = "a" * 201
    result = runner.invoke(add, ['--user', 'alice', long_title])

    assert result.exit_code == 1
    assert "Error: Title must be 1-200 characters" in result.output

def test_add_task_missing_user():
    """Test missing --user flag (User Story 2, Scenario 3)."""
    runner = CliRunner()
    result = runner.invoke(add, ['Buy milk'])

    assert result.exit_code == 2
    assert "Error: Missing option '--user'" in result.output

def test_add_task_empty_user_id():
    """Test empty user_id validation (User Story 2, Scenario 4)."""
    runner = CliRunner()
    result = runner.invoke(add, ['--user', '', 'Buy milk'])

    assert result.exit_code == 1
    assert "Error: User ID cannot be empty" in result.output

def test_add_task_with_emoji():
    """Test title with emoji (edge case)."""
    runner = CliRunner()
    result = runner.invoke(add, ['--user', 'alice', 'Buy 🥛 milk'])

    assert result.exit_code == 0
    assert 'Title: "Buy 🥛 milk"' in result.output

def test_add_task_max_length_title():
    """Test maximum length title (boundary case)."""
    runner = CliRunner()
    max_title = "x" * 200
    result = runner.invoke(add, ['--user', 'alice', max_title])

    assert result.exit_code == 0
    assert result.exit_code == 0
```

---

## Help Text

**Command**:
```bash
$ todo add --help
```

**Output**:
```
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

## Constitutional Alignment

| Principle | Compliance | Evidence |
|-----------|------------|----------|
| **II: User Isolation** | ✅ PASS | --user flag required, enforces user scoping |
| **IX: Code Quality** | ✅ PASS | Clear error messages, validation before DB access |
| **XII: Security** | ✅ PASS | Input validation, no SQL injection (SQLModel ORM) |
| **XVIII: Performance** | ✅ PASS | CLI completes in <100ms (p95 target) |

---

## Related Artifacts

- **Spec**: [spec.md](../spec.md) - User stories and acceptance criteria
- **Plan**: [plan.md](../plan.md) - Architectural decisions
- **Data Model**: [data-model.md](../data-model.md) - Task entity schema
- **Quickstart**: [quickstart.md](../quickstart.md) - Usage examples

---

## Next Steps

1. ✅ **CLI Contract Complete**: Command specification documented
2. ⏭️ **Create Quickstart Guide**: `quickstart.md` with usage examples
3. ⏭️ **Implement CLI Command**: `src/cli/commands/add.py`
4. ⏭️ **Write Integration Tests**: `tests/integration/test_add_task_integration.py`
5. ⏭️ **Validate Against Spec**: Verify all acceptance scenarios pass
