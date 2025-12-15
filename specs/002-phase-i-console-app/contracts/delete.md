# Command Contract: delete

**Purpose**: Delete a task permanently

**User Story**: US4 - Delete Tasks (Priority: P2)

**Functional Requirement**: FR-008 (Delete task with user verification)

## Command Signature

```bash
todo delete --username <USERNAME> <TASK_ID>
```

## Behavior

- Permanent deletion (no undo)
- Confirmation message on success

## Exit Codes

- Success: 0
- Task not found: 1

## User Isolation

✅ **Enforced**: `WHERE id = ? AND user_id = ?`
