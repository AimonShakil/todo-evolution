"""
Unit tests for authentication service.

Tests password hashing, JWT token generation/validation.

Constitutional Alignment:
- Principle X: Testing Requirements (unit tests for services)
- Principle XII: Security Principles (verify password hashing works)
"""

import pytest
from src.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
    get_user_id_from_token,
)


class TestPasswordHashing:
    """Test password hashing and verification."""

    def test_hash_password_returns_bcrypt_hash(self):
        """Test hash_password returns valid bcrypt hash."""
        hashed = hash_password("mysecretpassword")
        assert len(hashed) == 60  # Bcrypt hashes are 60 characters
        assert hashed.startswith("$2b$")  # Bcrypt prefix

    def test_hash_password_different_for_same_input(self):
        """Test hash_password generates different hashes (salt)."""
        hash1 = hash_password("password123")
        hash2 = hash_password("password123")
        assert hash1 != hash2  # Different salts

    def test_verify_password_correct(self):
        """Test verify_password with correct password."""
        password = "mysecretpassword"
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Test verify_password with incorrect password."""
        hashed = hash_password("correctpassword")
        assert verify_password("wrongpassword", hashed) is False

    def test_verify_password_empty(self):
        """Test verify_password with empty password."""
        hashed = hash_password("password123")
        assert verify_password("", hashed) is False


class TestJWTTokens:
    """Test JWT token generation and validation."""

    def test_create_access_token(self):
        """Test create_access_token generates valid JWT."""
        token = create_access_token(user_id=1, email="test@example.com")
        assert isinstance(token, str)
        assert len(token) > 100  # JWT tokens are long

    def test_decode_access_token_valid(self):
        """Test decode_access_token with valid token."""
        token = create_access_token(user_id=42, email="alice@example.com")
        payload = decode_access_token(token)

        assert payload is not None
        assert payload["sub"] == "42"  # user_id as string
        assert payload["email"] == "alice@example.com"
        assert "exp" in payload  # Expiration timestamp

    def test_decode_access_token_invalid(self):
        """Test decode_access_token with invalid token."""
        payload = decode_access_token("invalid.token.here")
        assert payload is None

    def test_decode_access_token_empty(self):
        """Test decode_access_token with empty token."""
        payload = decode_access_token("")
        assert payload is None

    def test_get_user_id_from_token_valid(self):
        """Test get_user_id_from_token with valid token."""
        token = create_access_token(user_id=123, email="test@example.com")
        user_id = get_user_id_from_token(token)
        assert user_id == 123

    def test_get_user_id_from_token_invalid(self):
        """Test get_user_id_from_token with invalid token."""
        user_id = get_user_id_from_token("invalid.token")
        assert user_id is None

    def test_get_user_id_from_token_different_users(self):
        """Test tokens for different users have different user_ids."""
        token1 = create_access_token(user_id=1, email="user1@example.com")
        token2 = create_access_token(user_id=2, email="user2@example.com")

        assert get_user_id_from_token(token1) == 1
        assert get_user_id_from_token(token2) == 2
        assert token1 != token2  # Different tokens
