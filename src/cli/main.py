"""CLI main entry point for Todo Evolution.

This module defines the main CLI group and registers all subcommands.
"""

import click

from src.cli.commands.add import add


@click.group()
@click.version_option(version="0.1.0", prog_name="todo")
def cli() -> None:
    """Todo Evolution - A simple task management CLI."""
    pass


# Register commands
cli.add_command(add)
