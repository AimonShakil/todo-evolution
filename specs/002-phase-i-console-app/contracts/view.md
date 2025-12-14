# Command Contract: view

**Purpose**: View all tasks for a user

**User Story**: US1 - Add and View Personal Tasks (Priority: P1 MVP)

**Functional Requirement**: FR-004 (View all tasks for username)

---

## Command Signature

```bash
todo view --username <USERNAME>
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--username` | String | ✅ Yes | User's username |

## Output Format

### Non-Empty Task List

```
ID | Title                          | Completed | Created
---|--------------------------------|-----------|---------
1  | Buy groceries                  | ✗         | 2025-12-08 10:30:00
2  | Finish report                  | ✓         | 2025-12-08 11:15:00
3  | Call dentist                   | ✗         | 2025-12-08 14:20:00
```

- **Checkmark ✓**: Task completed
- **X ✗**: Task incomplete
- **Created**: ISO 8601 format (YYYY-MM-DD HH:MM:SS)

### Empty Task List

```
No tasks found
```

## Exit Codes

- Success (tasks displayed or empty list): 0
- Error (database error): 1

## User Isolation

✅ **Enforced**: Only shows tasks where `user_id = <USERNAME>` (Principle II)

## Database Query

```sql
SELECT * FROM task WHERE user_id = ? ORDER BY id ASC
```

**Performance**: Index on `user_id` enables <500ms with 10,000 tasks (SC-010)
