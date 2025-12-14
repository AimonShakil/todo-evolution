"""Main entry point for Todo Evolution CLI.

This module provides a simple entry point compatible with `uv run python src/main.py`.
"""

from src.cli.main import cli

if __name__ == "__main__":
    cli()
