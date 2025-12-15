"""Unit tests for input validators."""

import pytest

from src.lib.validators import validate_title, validate_user_id


def test_validate_title_empty() -> None:
    """Test that empty title is rejected.

    Verifies that validate_title raises ValueError with appropriate
    message when given an empty string.
    """
    with pytest.raises(ValueError) as exc_info:
        validate_title("")

    assert "Title cannot be empty" in str(exc_info.value)


def test_validate_title_valid() -> None:
    """Test that valid title is accepted and returned unchanged.

    Verifies that a valid title (1-200 chars) passes validation
    and is returned as-is.
    """
    result = validate_title("Buy milk")

    assert result == "Buy milk"


def test_validate_title_boundary_1_char() -> None:
    """Test title boundary: exactly 1 character should succeed.

    Verifies that the minimum valid title length (1 char) is accepted.
    """
    result = validate_title("a")

    assert result == "a"


def test_validate_title_boundary_200_chars() -> None:
    """Test title boundary: exactly 200 characters should succeed.

    Verifies that the maximum valid title length (200 chars) is accepted.
    """
    max_title = "x" * 200
    result = validate_title(max_title)

    assert result == max_title
    assert len(result) == 200


def test_validate_title_too_long() -> None:
    """Test that title exceeding 200 characters is rejected.

    Verifies that validate_title raises ValueError when given
    a title longer than 200 characters.
    """
    long_title = "x" * 201

    with pytest.raises(ValueError) as exc_info:
        validate_title(long_title)

    assert "200 characters" in str(exc_info.value).lower()


def test_validate_user_id_empty() -> None:
    """Test that empty user_id is rejected.

    Verifies that validate_user_id raises ValueError with appropriate
    message when given an empty string.
    """
    with pytest.raises(ValueError) as exc_info:
        validate_user_id("")

    assert "User ID cannot be empty" in str(exc_info.value)


def test_validate_user_id_whitespace() -> None:
    """Test that whitespace-only user_id is rejected.

    Verifies that user_id containing only whitespace is rejected.
    """
    with pytest.raises(ValueError) as exc_info:
        validate_user_id("   ")

    assert "User ID cannot be empty" in str(exc_info.value)


def test_validate_user_id_valid() -> None:
    """Test that valid user_id is accepted and returned unchanged.

    Verifies that a valid user_id (non-empty string) passes validation
    and is returned as-is.
    """
    result = validate_user_id("alice")

    assert result == "alice"
