# Command Contract: update

**Purpose**: Update task title

**User Story**: US3 - Update Task Details (Priority: P2)

**Functional Requirement**: FR-007 (Update task title with validation)

## Command Signature

```bash
todo update --username <USERNAME> <TASK_ID> "<NEW_TITLE>"
```

## Validation

- New title: 1-200 characters
- Task must exist and belong to user

## Exit Codes

- Success: 0
- Validation error or task not found: 1

## User Isolation

✅ **Enforced**: `WHERE id = ? AND user_id = ?`
