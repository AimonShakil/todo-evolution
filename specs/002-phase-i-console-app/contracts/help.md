# Command Contract: help

**Purpose**: Display usage help and available commands

**Functional Requirement**: FR-020 (Help command with usage examples)

## Command Signature

```bash
todo --help
# or
todo help
```

## Output Format

```
Todo CLI - Multi-user task management

Usage:
  todo [COMMAND] [OPTIONS]

Commands:
  add       Add a new task
  view      View all your tasks
  update    Update task title
  delete    Delete a task
  complete  Mark task complete/incomplete
  help      Show this help message

Examples:
  todo add --username alice "Buy groceries"
  todo view --username alice
  todo complete --username alice 1
  todo update --username alice 1 "Buy milk"
  todo delete --username alice 1

For more info: todo [COMMAND] --help
```

## Exit Code

- Always 0 (help is not an error)
