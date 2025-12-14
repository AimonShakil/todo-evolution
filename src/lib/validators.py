"""Input validation functions for Todo Evolution.

This module provides standalone validation functions for user inputs,
which can be used both in the model layer and CLI layer.
"""


def validate_title(title: str) -> str:
    """Validate task title meets requirements.

    Args:
        title: The title string to validate.

    Returns:
        The validated title (unchanged if valid).

    Raises:
        ValueError: If title is empty or exceeds 200 characters.
    """
    if not title or len(title) == 0:
        raise ValueError("Title cannot be empty")
    if len(title) > 200:
        raise ValueError("Title must be 1-200 characters")
    return title


def validate_user_id(user_id: str) -> str:
    """Validate user_id meets requirements.

    Args:
        user_id: The user_id string to validate.

    Returns:
        The validated user_id (unchanged if valid).

    Raises:
        ValueError: If user_id is empty or contains only whitespace.
    """
    if not user_id or user_id.strip() == "":
        raise ValueError("User ID cannot be empty")
    return user_id
