"""
Task routes for Phase II Web App.

This module provides CRUD endpoints for task management with JWT authentication.

Constitutional Alignment:
- Principle II: User Data Isolation (all endpoints verify JWT user matches {user_id})
- Principle III: Authentication & Authorization (JWT token required)
- Principle XVI: Error Handling (user-friendly error messages)
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.lib.database import get_session
from src.models.task import Task
from src.services.auth_service import get_user_id_from_token
from src.services import task_service

router = APIRouter(prefix="", tags=["Tasks"])
security = HTTPBearer()


# Request/Response models
class TaskResponse(BaseModel):
    """Task response model."""

    id: int
    user_id: int
    title: str
    description: str | None
    completed: bool
    created_at: str
    updated_at: str

    @classmethod
    def from_task(cls, task: Task) -> "TaskResponse":
        """Convert Task model to response."""
        return cls(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at.isoformat(),
            updated_at=task.updated_at.isoformat(),
        )


class CreateTaskRequest(BaseModel):
    """Create task request."""

    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(None)


class UpdateTaskRequest(BaseModel):
    """Update task request."""

    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = Field(None)
    completed: bool | None = Field(None)


# Dependency: Get current user from JWT token
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> int:
    """
    Extract and validate JWT token, return user_id.

    Constitutional Principle III: Authentication required for all task endpoints.

    Args:
        credentials: HTTP Bearer token from Authorization header

    Returns:
        User ID from JWT token

    Raises:
        HTTPException 401: Invalid or missing token
    """
    token = credentials.credentials
    user_id = get_user_id_from_token(token)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    return user_id


# Dependency: Verify JWT user matches URL user_id
async def verify_user_access(
    user_id: int,
    current_user: int = Depends(get_current_user)
) -> int:
    """
    Verify that JWT user matches URL {user_id} parameter.

    Constitutional Principle II: User Data Isolation enforcement.

    Args:
        user_id: User ID from URL path parameter
        current_user: User ID from JWT token

    Returns:
        User ID if authorized

    Raises:
        HTTPException 403: User ID mismatch (trying to access another user's data)
    """
    if current_user != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access another user's tasks",
        )
    return current_user


@router.get("/{user_id}/tasks", response_model=List[TaskResponse])
async def get_tasks(
    user_id: int,
    verified_user: int = Depends(verify_user_access),
    session: AsyncSession = Depends(get_session),
) -> List[TaskResponse]:
    """
    Get all tasks for a user.

    Constitutional Principle II: Returns only tasks belonging to authenticated user.

    Args:
        user_id: User ID from URL (verified against JWT)
        verified_user: User ID after JWT verification
        session: Database session

    Returns:
        List of tasks (may be empty)

    Example:
        GET /api/1/tasks
        Authorization: Bearer <jwt_token>

        Response 200:
        [
            {
                "id": 1,
                "user_id": 1,
                "title": "Buy groceries",
                "description": "Get milk and eggs",
                "completed": false,
                "created_at": "2025-12-15T10:00:00",
                "updated_at": "2025-12-15T10:00:00"
            }
        ]
    """
    tasks = await task_service.get_all_tasks(session, verified_user)
    return [TaskResponse.from_task(task) for task in tasks]


@router.post("/{user_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: int,
    request: CreateTaskRequest,
    verified_user: int = Depends(verify_user_access),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """
    Create a new task.

    Args:
        user_id: User ID from URL (verified against JWT)
        request: Task creation data
        verified_user: User ID after JWT verification
        session: Database session

    Returns:
        Created task

    Example:
        POST /api/1/tasks
        Authorization: Bearer <jwt_token>
        {
            "title": "Buy groceries",
            "description": "Get milk and eggs"
        }

        Response 201:
        {
            "id": 1,
            "user_id": 1,
            "title": "Buy groceries",
            "description": "Get milk and eggs",
            "completed": false,
            ...
        }
    """
    task = await task_service.create_task(
        session,
        user_id=verified_user,
        title=request.title,
        description=request.description,
    )
    return TaskResponse.from_task(task)


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: int,
    task_id: int,
    verified_user: int = Depends(verify_user_access),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """
    Get a specific task by ID.

    Constitutional Principle II: Returns 404 if task doesn't exist OR
    belongs to another user (prevents information leakage).

    Args:
        user_id: User ID from URL (verified against JWT)
        task_id: Task ID to retrieve
        verified_user: User ID after JWT verification
        session: Database session

    Returns:
        Task details

    Raises:
        HTTPException 404: Task not found or not owned by user

    Example:
        GET /api/1/tasks/10
        Authorization: Bearer <jwt_token>

        Response 200:
        {
            "id": 10,
            "title": "Buy groceries",
            ...
        }
    """
    task = await task_service.get_task(session, verified_user, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return TaskResponse.from_task(task)


@router.patch("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: int,
    task_id: int,
    request: UpdateTaskRequest,
    verified_user: int = Depends(verify_user_access),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """
    Update a task's fields.

    Args:
        user_id: User ID from URL (verified against JWT)
        task_id: Task ID to update
        request: Update data (title, description, completed)
        verified_user: User ID after JWT verification
        session: Database session

    Returns:
        Updated task

    Raises:
        HTTPException 404: Task not found or not owned by user

    Example:
        PATCH /api/1/tasks/10
        Authorization: Bearer <jwt_token>
        {
            "title": "Buy groceries and supplies"
        }

        Response 200:
        {
            "id": 10,
            "title": "Buy groceries and supplies",
            ...
        }
    """
    task = await task_service.update_task(
        session,
        user_id=verified_user,
        task_id=task_id,
        title=request.title,
        description=request.description,
        completed=request.completed,
    )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return TaskResponse.from_task(task)


@router.post("/{user_id}/tasks/{task_id}/toggle", response_model=TaskResponse)
async def toggle_task(
    user_id: int,
    task_id: int,
    verified_user: int = Depends(verify_user_access),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """
    Toggle a task's completion status.

    Args:
        user_id: User ID from URL (verified against JWT)
        task_id: Task ID to toggle
        verified_user: User ID after JWT verification
        session: Database session

    Returns:
        Updated task with toggled status

    Raises:
        HTTPException 404: Task not found or not owned by user

    Example:
        POST /api/1/tasks/10/toggle
        Authorization: Bearer <jwt_token>

        Response 200:
        {
            "id": 10,
            "completed": true,
            ...
        }
    """
    task = await task_service.toggle_task_completed(session, verified_user, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return TaskResponse.from_task(task)


@router.delete("/{user_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user_id: int,
    task_id: int,
    verified_user: int = Depends(verify_user_access),
    session: AsyncSession = Depends(get_session),
) -> None:
    """
    Delete a task.

    Args:
        user_id: User ID from URL (verified against JWT)
        task_id: Task ID to delete
        verified_user: User ID after JWT verification
        session: Database session

    Returns:
        None (204 No Content)

    Raises:
        HTTPException 404: Task not found or not owned by user

    Example:
        DELETE /api/1/tasks/10
        Authorization: Bearer <jwt_token>

        Response 204 (no content)
    """
    success = await task_service.delete_task(session, verified_user, task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
