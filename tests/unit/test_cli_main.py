"""Unit tests for CLI main entry point."""

from click.testing import CliRunner

from src.cli.main import cli


def test_cli_help() -> None:
    """Test that CLI help displays available commands.

    Verifies that running 'todo --help' shows the 'add' command
    in the help output.
    """
    runner = CliRunner()

    result = runner.invoke(cli, ["--help"])

    assert result.exit_code == 0
    assert "add" in result.output.lower()
    assert "Commands:" in result.output or "Usage:" in result.output


def test_cli_version() -> None:
    """Test that CLI version displays correct version number.

    Verifies that running 'todo --version' shows the application
    version from pyproject.toml (0.1.0).
    """
    runner = CliRunner()

    result = runner.invoke(cli, ["--version"])

    assert result.exit_code == 0
    assert "0.1.0" in result.output
