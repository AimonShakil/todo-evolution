"""Custom exceptions for Todo Evolution.

This module defines domain-specific exceptions for error handling
throughout the application.
"""


class DatabaseUnavailableError(Exception):
    """Raised when the database is unavailable or cannot be accessed.

    This typically indicates issues with database connectivity,
    file permissions, or initialization failures.
    """

    pass


class DataIntegrityError(Exception):
    """Raised when data integrity constraints are violated.

    This includes foreign key violations, unique constraint violations,
    or other data consistency issues.
    """

    pass
