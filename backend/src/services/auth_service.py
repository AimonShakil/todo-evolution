"""
Authentication service for Phase II Web App.

This module provides password hashing, JWT token generation/validation,
and user authentication logic.

Constitutional Alignment:
- Principle III: Authentication & Authorization (Better Auth integration)
- Principle XII: Security Principles (bcrypt password hashing, parameterized queries)
- Principle IX: Code Quality Standards (type hints, docstrings)
"""

import os
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
JWT_SECRET = os.getenv("JWT_SECRET")
if not JWT_SECRET:
    raise ValueError(
        "JWT_SECRET environment variable is not set. "
        "Please add JWT_SECRET to your .env file."
    )

JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_DAYS = 7


def hash_password(password: str) -> str:
    """
    Hash a plain text password using bcrypt.

    Args:
        password: Plain text password to hash

    Returns:
        Bcrypt hashed password (60 characters)

    Example:
        >>> hashed = hash_password("mysecretpassword")
        >>> len(hashed)
        60
        >>> hashed.startswith("$2b$")
        True
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a bcrypt hash.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Bcrypt hash to compare against

    Returns:
        True if password matches, False otherwise

    Example:
        >>> hashed = hash_password("mysecretpassword")
        >>> verify_password("mysecretpassword", hashed)
        True
        >>> verify_password("wrongpassword", hashed)
        False
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: int, email: str) -> str:
    """
    Create a JWT access token for a user.

    The token contains:
    - sub: user_id (subject)
    - email: user email
    - exp: expiration timestamp (7 days from now)

    Args:
        user_id: User's database ID
        email: User's email address

    Returns:
        JWT token string

    Example:
        >>> token = create_access_token(user_id=1, email="alice@example.com")
        >>> len(token) > 100
        True
    """
    expire = datetime.utcnow() + timedelta(days=JWT_EXPIRATION_DAYS)
    to_encode = {
        "sub": str(user_id),  # Subject (user ID)
        "email": email,
        "exp": expire,
    }
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode and validate a JWT access token.

    Args:
        token: JWT token string

    Returns:
        Token payload dict with keys: sub (user_id), email, exp
        Returns None if token is invalid or expired

    Example:
        >>> token = create_access_token(user_id=1, email="alice@example.com")
        >>> payload = decode_access_token(token)
        >>> payload["sub"]
        '1'
        >>> payload["email"]
        'alice@example.com'
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        return None


def get_user_id_from_token(token: str) -> Optional[int]:
    """
    Extract user_id from a JWT token.

    Args:
        token: JWT token string

    Returns:
        User ID (integer) if token is valid, None otherwise

    Example:
        >>> token = create_access_token(user_id=42, email="alice@example.com")
        >>> get_user_id_from_token(token)
        42
    """
    payload = decode_access_token(token)
    if not payload:
        return None

    user_id_str = payload.get("sub")
    if not user_id_str:
        return None

    try:
        return int(user_id_str)
    except ValueError:
        return None
