---
name: click-cli
description: Build Click CLI commands with proper error handling, validation, user input, and output formatting. Use when creating console commands or CLI interfaces for Phase I.
allowed-tools: Read, Write, Edit
---

# Click CLI Builder Skill

Patterns for building robust Click CLI commands for Phase I console app.

## Basic Command Structure

```python
import click
from typing import Optional

@click.command()
@click.option('--user', '-u', required=True, help='Username for task operation')
@click.argument('task_id', type=int)
@click.pass_context
def complete(ctx: click.Context, user: str, task_id: int) -> None:
    """Mark a task as complete or incomplete (toggle).

    TASK_ID: The ID of the task to complete

    Examples:
        $ todo complete --user alice 5
        $ todo complete -u bob 12
    """
    try:
        # Business logic
        task = mark_task_complete(user, task_id)

        # Success output
        click.echo(click.style(
            f"✓ Task {task_id} marked {'complete' if task.completed else 'incomplete'}",
            fg='green'
        ))

    except TaskNotFound:
        click.echo(
            click.style(f"✗ Task {task_id} not found", fg='red'),
            err=True
        )
        raise click.Abort()

    except Exception as e:
        click.echo(click.style(f"✗ Error: {e}", fg='red'), err=True)
        raise click.Abort()
```

## Click Command Types

### 1. Simple Command

```python
@click.command()
@click.option('--user', '-u', required=True)
def view(user: str) -> None:
    """View all tasks for a user."""
    tasks = get_user_tasks(user)

    if not tasks:
        click.echo("No tasks found.")
        return

    for task in tasks:
        status = "✓" if task.completed else " "
        click.echo(f"[{status}] {task.id}: {task.title}")
```

### 2. Command with Arguments

```python
@click.command()
@click.option('--user', '-u', required=True)
@click.argument('title')  # Positional argument
def add(user: str, title: str) -> None:
    """Add a new task.

    TITLE: The task title (1-200 characters)
    """
    task = create_task(user_id=user, title=title)
    click.echo(click.style(f"✓ Task {task.id} added", fg='green'))
```

### 3. Command with Multiple Arguments

```python
@click.command()
@click.option('--user', '-u', required=True)
@click.argument('task_id', type=int)
@click.argument('new_title')
def update(user: str, task_id: int, new_title: str) -> None:
    """Update a task's title.

    TASK_ID: The ID of the task to update
    NEW_TITLE: The new title for the task
    """
    task = update_task_title(user, task_id, new_title)
    click.echo(click.style(f"✓ Task {task_id} updated", fg='green'))
```

### 4. Command with Optional Flags

```python
@click.command()
@click.option('--user', '-u', required=True)
@click.option('--completed', is_flag=True, help='Show only completed tasks')
@click.option('--pending', is_flag=True, help='Show only pending tasks')
def view(user: str, completed: bool, pending: bool) -> None:
    """View tasks with optional filtering."""
    if completed and pending:
        click.echo(
            click.style("✗ Cannot use both --completed and --pending", fg='red'),
            err=True
        )
        raise click.Abort()

    tasks = get_user_tasks(user, completed=completed, pending=pending)

    for task in tasks:
        click.echo(f"{task.id}: {task.title}")
```

## Click Options and Arguments

### Options (--flag or -f)

```python
# Required option
@click.option('--user', '-u', required=True, help='Username')

# Optional with default
@click.option('--limit', type=int, default=20, help='Number of tasks to show')

# Boolean flag
@click.option('--verbose', is_flag=True, help='Enable verbose output')

# Multiple values
@click.option('--tag', multiple=True, help='Filter by tag (can specify multiple)')

# Choice from options
@click.option('--priority', type=click.Choice(['low', 'medium', 'high']))

# Prompt for input
@click.option('--password', prompt=True, hide_input=True)

# Confirmation prompt
@click.option('--yes', is_flag=True, callback=abort_if_false, expose_value=False,
              prompt='Are you sure?')
```

### Arguments (Positional)

```python
# Single argument
@click.argument('task_id', type=int)

# Multiple arguments
@click.argument('task_id', type=int)
@click.argument('title')

# Variable arguments
@click.argument('titles', nargs=-1)  # Accepts any number

# File argument
@click.argument('input_file', type=click.File('r'))
@click.argument('output_file', type=click.File('w'))
```

## Error Handling Patterns

### Pattern 1: Specific Exception Handling

```python
@click.command()
@click.option('--user', '-u', required=True)
@click.argument('task_id', type=int)
def delete(user: str, task_id: int) -> None:
    """Delete a task."""
    try:
        delete_task(user, task_id)
        click.echo(click.style(f"✓ Task {task_id} deleted", fg='green'))

    except TaskNotFound:
        click.echo(
            click.style(f"✗ Task {task_id} not found", fg='red'),
            err=True
        )
        raise click.Abort()

    except PermissionDenied:
        click.echo(
            click.style(f"✗ Access denied to task {task_id}", fg='red'),
            err=True
        )
        raise click.Abort()

    except Exception as e:
        click.echo(click.style(f"✗ Unexpected error: {e}", fg='red'), err=True)
        raise click.Abort()
```

### Pattern 2: Validation Errors

```python
@click.command()
@click.option('--user', '-u', required=True)
@click.argument('title')
def add(user: str, title: str) -> None:
    """Add a task with validation."""
    try:
        # Validate input
        if not title or len(title.strip()) == 0:
            raise ValueError("Title cannot be empty")
        if len(title) > 200:
            raise ValueError("Title must be 1-200 characters")

        # Create task
        task = create_task(user, title.strip())
        click.echo(click.style(f"✓ Task {task.id} added", fg='green'))

    except ValueError as e:
        click.echo(click.style(f"✗ Validation error: {e}", fg='red'), err=True)
        raise click.Abort()

    except Exception as e:
        click.echo(click.style(f"✗ Error: {e}", fg='red'), err=True)
        raise click.Abort()
```

## Output Formatting

### Colored Output

```python
# Success (green)
click.echo(click.style("✓ Task completed", fg='green'))

# Error (red)
click.echo(click.style("✗ Task not found", fg='red'), err=True)

# Warning (yellow)
click.echo(click.style("⚠ Task overdue", fg='yellow'))

# Info (blue)
click.echo(click.style("ℹ 5 tasks remaining", fg='blue'))

# Bold
click.echo(click.style("Important", bold=True))

# Dim
click.echo(click.style("Additional info", dim=True))
```

### Formatted Tables

```python
def view(user: str) -> None:
    """View tasks in formatted table."""
    tasks = get_user_tasks(user)

    if not tasks:
        click.echo("No tasks found.")
        return

    # Header
    click.echo(f"\nTasks for {click.style(user, bold=True)}:")
    click.echo("─" * 70)
    click.echo(f"{'ID':<5} {'Status':<8} {'Title':<50}")
    click.echo("─" * 70)

    # Rows
    for task in tasks:
        status = click.style("✓ Done", fg='green') if task.completed else "  Pending"
        click.echo(f"{task.id:<5} {status:<15} {task.title[:50]}")

    # Footer
    click.echo("─" * 70)
    completed = sum(1 for t in tasks if t.completed)
    click.echo(f"Total: {len(tasks)} tasks ({completed} completed, {len(tasks) - completed} pending)")
```

### Progress Bars

```python
@click.command()
@click.option('--user', '-u', required=True)
def export(user: str) -> None:
    """Export tasks with progress bar."""
    tasks = get_user_tasks(user)

    with click.progressbar(tasks, label='Exporting tasks') as bar:
        for task in bar:
            export_task_to_file(task)

    click.echo(click.style(f"✓ Exported {len(tasks)} tasks", fg='green'))
```

## Command Groups

### Main CLI Group

```python
@click.group()
@click.version_option(version='0.1.0')
@click.pass_context
def cli(ctx):
    """Todo CLI - Manage your tasks from the command line.

    Examples:
        todo add --user alice "Buy groceries"
        todo view --user alice
        todo complete --user alice 5
    """
    # Initialize context object
    ctx.ensure_object(dict)

    # Initialize database
    from backend.db import init_db
    init_db()

if __name__ == '__main__':
    cli()
```

### Register Commands with Group

```python
# commands/task.py
@click.command()
@click.option('--user', '-u', required=True)
def add(user: str, title: str):
    """Add a task."""
    pass

@click.command()
@click.option('--user', '-u', required=True)
def view(user: str):
    """View tasks."""
    pass

# main.py
from backend.commands import task

cli.add_command(task.add)
cli.add_command(task.view)
cli.add_command(task.complete)
cli.add_command(task.update)
cli.add_command(task.delete)
```

### Nested Command Groups

```python
@click.group()
def cli():
    """Todo CLI."""
    pass

@cli.group()
def task():
    """Task management commands."""
    pass

@task.command('add')
def task_add():
    """Add a task."""
    pass

@task.command('list')
def task_list():
    """List tasks."""
    pass

# Usage:
# $ todo task add "Buy groceries"
# $ todo task list
```

## User Input and Confirmation

### Prompt for Input

```python
@click.command()
def add_interactive():
    """Add a task interactively."""
    user = click.prompt('Your username', type=str)
    title = click.prompt('Task title', type=str)
    confirm = click.confirm('Add this task?', default=True)

    if not confirm:
        click.echo("Cancelled.")
        raise click.Abort()

    task = create_task(user, title)
    click.echo(click.style(f"✓ Task {task.id} added", fg='green'))
```

### Confirmation Prompt

```python
@click.command()
@click.option('--user', '-u', required=True)
@click.argument('task_id', type=int)
@click.confirmation_option(prompt='Are you sure you want to delete this task?')
def delete(user: str, task_id: int):
    """Delete a task with confirmation."""
    delete_task(user, task_id)
    click.echo(click.style(f"✓ Task {task_id} deleted", fg='green'))
```

### Choice Selection

```python
priority = click.prompt(
    'Task priority',
    type=click.Choice(['low', 'medium', 'high']),
    default='medium'
)
```

## Context Management

### Passing Context Between Commands

```python
@click.group()
@click.option('--config', type=click.Path(), help='Config file path')
@click.pass_context
def cli(ctx, config):
    """CLI with shared context."""
    ctx.ensure_object(dict)
    ctx.obj['config'] = load_config(config) if config else {}

@cli.command()
@click.pass_context
def status(ctx):
    """Show status using shared config."""
    config = ctx.obj['config']
    click.echo(f"Config: {config}")
```

## Testing Click Commands

```python
from click.testing import CliRunner
import pytest

def test_add_task():
    """Test add command."""
    runner = CliRunner()

    result = runner.invoke(cli, ['add', '--user', 'alice', 'Buy groceries'])

    assert result.exit_code == 0
    assert 'Task' in result.output
    assert 'added' in result.output

def test_add_task_empty_title():
    """Test add command with validation error."""
    runner = CliRunner()

    result = runner.invoke(cli, ['add', '--user', 'alice', ''])

    assert result.exit_code != 0
    assert 'Validation error' in result.output

def test_delete_task_with_confirmation():
    """Test delete command with confirmation."""
    runner = CliRunner()

    # Provide 'y' to confirmation prompt
    result = runner.invoke(cli, ['delete', '--user', 'alice', '1'], input='y\n')

    assert result.exit_code == 0
    assert 'deleted' in result.output
```

## Entry Point Configuration

### pyproject.toml

```toml
[project.scripts]
todo = "backend.main:cli"
```

### Running the CLI

```bash
# Development (Python module)
python -m backend.main add --user alice "Buy groceries"

# Installed (entry point)
todo add --user alice "Buy groceries"
```

## Common Patterns

### Help Text

```python
@click.command()
@click.option('--user', '-u', required=True, help='Username')
@click.argument('task_id', type=int)
def complete(user: str, task_id: int):
    """Mark a task as complete.

    This command toggles the completion status of a task.
    If the task is incomplete, it will be marked complete.
    If the task is complete, it will be marked incomplete.

    Examples:

        \b
        $ todo complete --user alice 5
        $ todo complete -u bob 12

    """
    pass
```

### Custom Validators

```python
def validate_username(ctx, param, value):
    """Validate username format."""
    if not value or len(value) < 3:
        raise click.BadParameter('Username must be at least 3 characters')
    if not value.isalnum():
        raise click.BadParameter('Username must be alphanumeric')
    return value.lower()

@click.command()
@click.option('--user', '-u', callback=validate_username, required=True)
def add(user: str):
    """Add task with validated username."""
    pass
```

## Constitutional Compliance

- ✅ **User isolation**: Always require `--user` parameter
- ✅ **Error handling**: Proper try/except with user-friendly messages
- ✅ **Type hints**: All function parameters typed
- ✅ **Docstrings**: All commands documented with examples
- ✅ **Exit codes**: Use `raise click.Abort()` on errors

## MCP Integration (Context7)

For advanced Click patterns, fetch official documentation:

```
Complex command groups?
  → mcp__context7__get-library-docs("/pallets/click", topic="commands")

Advanced options?
  → mcp__context7__get-library-docs("/pallets/click", topic="options")
```

## Complete Example

See `phase-i-console` skill for complete CLI implementation with all commands.
