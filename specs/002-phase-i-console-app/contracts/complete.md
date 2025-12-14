# Command Contract: complete

**Purpose**: Mark task as complete or toggle back to incomplete

**User Story**: US2 - Mark Tasks Complete (Priority: P1 MVP)

**Functional Requirements**: FR-005 (mark complete), FR-006 (toggle incomplete)

---

## Command Signature

```bash
todo complete --username <USERNAME> <TASK_ID>
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--username` | String | ✅ Yes | User's username |
| `<TASK_ID>` | Integer | ✅ Yes | Task ID to mark complete/incomplete |

## Behavior

**Toggle Logic**: If task is incomplete → mark complete. If task is complete → mark incomplete (FR-006)

## Examples

```bash
# Mark task 1 as complete
$ todo complete --username alice 1
✓ Task 1 marked complete

# Toggle task 1 back to incomplete
$ todo complete --username alice 1
✓ Task 1 marked incomplete
```

## Error Cases

```bash
# Task not found (or belongs to different user)
$ todo complete --username alice 999
Error: Task 999 not found
```

## Exit Codes

- Success: 0
- Task not found or error: 1

## User Isolation

✅ **Enforced**: Query `WHERE id = ? AND user_id = ?` prevents accessing other users' tasks (Principle II)

## Database Operations

1. **Query**: `SELECT * FROM task WHERE id = ? AND user_id = ?`
2. **Update**: `completed = NOT completed`, `updated_at = current UTC`
3. **Commit**
