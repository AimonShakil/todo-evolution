"""
Authentication routes for Phase II Web App.

This module provides signup and signin endpoints for user authentication.

Constitutional Alignment:
- Principle III: Authentication & Authorization (Better Auth integration)
- Principle XII: Security Principles (bcrypt password hashing)
- Principle XVI: Error Handling (user-friendly error messages)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.lib.database import get_session
from src.models.user import User
from src.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


# Request/Response models
class SignupRequest(BaseModel):
    """Signup request payload."""

    email: EmailStr = Field(..., description="User email address")
    name: str = Field(..., min_length=1, max_length=100, description="User display name")
    password: str = Field(..., min_length=8, description="User password (min 8 characters)")


class SigninRequest(BaseModel):
    """Signin request payload."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class AuthResponse(BaseModel):
    """Authentication response with JWT token."""

    user_id: int = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    name: str = Field(..., description="User display name")
    token: str = Field(..., description="JWT access token")


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    request: SignupRequest,
    session: AsyncSession = Depends(get_session),
) -> AuthResponse:
    """
    Create a new user account.

    Args:
        request: Signup request with email, name, password
        session: Database session (injected)

    Returns:
        AuthResponse with user info and JWT token

    Raises:
        HTTPException 400: Email already registered

    Example:
        POST /api/auth/signup
        {
            "email": "alice@example.com",
            "name": "Alice Smith",
            "password": "securepassword123"
        }

        Response 201:
        {
            "user_id": 1,
            "email": "alice@example.com",
            "name": "Alice Smith",
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        }
    """
    # Check if email already exists
    statement = select(User).where(User.email == request.email)
    result = await session.execute(statement)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Hash password
    password_hash = hash_password(request.password)

    # Create user
    user = User(
        email=request.email,
        name=request.name,
        password_hash=password_hash,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    # Generate JWT token
    token = create_access_token(user_id=user.id, email=user.email)

    return AuthResponse(
        user_id=user.id,
        email=user.email,
        name=user.name,
        token=token,
    )


@router.post("/signin", response_model=AuthResponse)
async def signin(
    request: SigninRequest,
    session: AsyncSession = Depends(get_session),
) -> AuthResponse:
    """
    Sign in to an existing account.

    Args:
        request: Signin request with email, password
        session: Database session (injected)

    Returns:
        AuthResponse with user info and JWT token

    Raises:
        HTTPException 401: Invalid email or password

    Example:
        POST /api/auth/signin
        {
            "email": "alice@example.com",
            "password": "securepassword123"
        }

        Response 200:
        {
            "user_id": 1,
            "email": "alice@example.com",
            "name": "Alice Smith",
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        }
    """
    # Find user by email
    statement = select(User).where(User.email == request.email)
    result = await session.execute(statement)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Verify password
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Generate JWT token
    token = create_access_token(user_id=user.id, email=user.email)

    return AuthResponse(
        user_id=user.id,
        email=user.email,
        name=user.name,
        token=token,
    )
