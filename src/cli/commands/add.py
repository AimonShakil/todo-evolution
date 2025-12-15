"""Add command for creating tasks."""

import sys

import click
from pydantic import ValidationError

from src.lib.validators import validate_title, validate_user_id
from src.services.db import get_session, init_db
from src.services.task_service import TaskService


@click.command()
@click.option("--user", required=True, help="User ID for task ownership")
@click.argument("title")
def add(user: str, title: str) -> None:
    """Create a new task.

    TITLE: The task description (1-200 characters)
    """
    try:
        # Validate inputs
        validate_user_id(user)
        validate_title(title)

        # Initialize database if needed
        init_db()

        # Create task
        with get_session() as session:
            service = TaskService(session)
            task = service.create_task(user_id=user, title=title)

            # Success message
            click.echo(f"✓ Task {task.id} created: {task.title}")
            sys.exit(0)

    except ValueError as e:
        # Validation error
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    except ValidationError as e:
        # Pydantic validation error
        click.echo(f"Validation error: {e}", err=True)
        sys.exit(1)

    except Exception as e:
        # Unexpected error
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(1)
