# Command Contract: add

**Purpose**: Add a new task to the user's task list

**User Story**: US1 - Add and View Personal Tasks (Priority: P1 MVP)

**Functional Requirement**: FR-001 (Add task with title and username)

---

## Command Signature

```bash
todo add --username <USERNAME> "<TITLE>"
```

## Parameters

| Parameter | Type | Required | Description | Validation |
|-----------|------|----------|-------------|------------|
| `--username` | String | ✅ Yes | User's username for task ownership | Non-empty string (min 1 char) |
| `<TITLE>` | String | ✅ Yes | Task title (what needs to be done) | 1-200 characters, supports Unicode/emojis |

## Examples

### Success Cases

```bash
# Example 1: Basic task
$ todo add --username alice "Buy groceries"
✓ Task added with ID 1

# Example 2: Unicode and special characters
$ todo add --username bob "Buy milk & eggs (2 gallons) for $5.99 🥛"
✓ Task added with ID 2

# Example 3: Maximum length title (200 characters)
$ todo add --username charlie "This is a very long task title that is exactly two hundred characters long and tests the maximum boundary of what the system will accept for a task title without rejecting it as invalid xxxxxxxxx"
✓ Task added with ID 3
```

### Error Cases

```bash
# Error 1: Empty title
$ todo add --username alice ""
Error: Title cannot be empty

# Error 2: Title too long (201 characters)
$ todo add --username alice "This is a task title that exceeds the maximum length limit of two hundred characters and should be rejected by the validation logic because it violates the business rule that titles must be between one and two hundred chars"
Error: Title must be 1-200 characters

# Error 3: Missing username
$ todo add "Buy groceries"
Error: Username required

# Error 4: Empty username
$ todo add --username "" "Buy groceries"
Error: Username required
```

## Output Format

### Success Output

```
✓ Task added with ID <TASK_ID>
```

- **Symbol**: ✓ (checkmark) for visual success indicator
- **Task ID**: Integer returned immediately for reference in subsequent operations (FR-014)

### Error Output

```
Error: <HUMAN_READABLE_MESSAGE>
```

- **Prefix**: "Error: " for clear error indication
- **Message**: Human-readable, actionable (FR-013, SC-008)
- **No Stack Traces**: 100% human-readable errors (SC-008)

## Exit Codes

| Scenario | Exit Code | Rationale |
|----------|-----------|-----------|
| Task added successfully | 0 | Success (FR-019) |
| Validation error (empty title, title too long, empty username) | 1 | Error (FR-019) |
| Database error (unable to connect, write failure) | 1 | Error (FR-019) |

## Database Operations

1. **Validate** title length (1-200 chars) and username non-empty
2. **Create** Task entity with:
   - `user_id = <USERNAME>` (string)
   - `title = <TITLE>`
   - `completed = False` (default)
   - `created_at = current UTC timestamp`
   - `updated_at = current UTC timestamp`
   - All Phase V fields = NULL
3. **Insert** into `task` table
4. **Return** generated task ID

## User Isolation

✅ **Enforced**: Task is created with `user_id` field set to provided username (Principle II)

## Performance

- **Target**: <500ms execution time (SC-010)
- **Optimization**: Single INSERT operation, no complex queries

## Testing

### Contract Tests

```python
def test_add_command_success():
    result = run_cli(['add', '--username', 'alice', 'Buy groceries'])
    assert result.exit_code == 0
    assert result.output.startswith("✓ Task added with ID ")

def test_add_command_empty_title_error():
    result = run_cli(['add', '--username', 'alice', ''])
    assert result.exit_code == 1
    assert "Error: Title cannot be empty" in result.output

def test_add_command_title_too_long_error():
    long_title = "A" * 201
    result = run_cli(['add', '--username', 'alice', long_title])
    assert result.exit_code == 1
    assert "Error: Title must be 1-200 characters" in result.output

def test_add_command_missing_username_error():
    result = run_cli(['add', 'Buy groceries'])
    assert result.exit_code == 1
    assert "Error: Username required" in result.output
```

### Integration Tests

```python
def test_add_task_persists_to_database():
    run_cli(['add', '--username', 'alice', 'Buy groceries'])

    # Verify task exists in database
    tasks = get_all_tasks(user_id='alice')
    assert len(tasks) == 1
    assert tasks[0].title == "Buy groceries"
    assert tasks[0].completed == False
```

---

**Contract Complete** - Implementation must match this specification exactly
