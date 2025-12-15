"""Task service layer for business logic.

This module provides the TaskService class for managing task operations
with proper session management and error handling.
"""

from sqlmodel import Session, select

from src.lib.exceptions import DatabaseUnavailableError
from src.models.task import Task


class TaskService:
    """Service class for task-related operations.

    This class encapsulates business logic for task management,
    including creation, retrieval, and user isolation.
    """

    def __init__(self, session: Session) -> None:
        """Initialize the TaskService with a database session.

        Args:
            session: SQLModel Session for database operations.
        """
        self.session = session

    def create_task(self, user_id: str, title: str) -> Task:
        """Create a new task for a user.

        SECURITY CRITICAL: This method assigns user_id to the task, establishing
        ownership. ALL queries MUST filter by user_id to enforce user isolation
        (Constitutional Principle II: User Data Isolation).

        Args:
            user_id: The ID of the user creating the task.
            title: The task title (1-200 characters).

        Returns:
            The created Task object with ID assigned.

        Raises:
            ValidationError: If title or user_id fail validation.
            DatabaseUnavailableError: If database operation fails.
        """
        try:
            # Create task (validation happens automatically via Pydantic)
            task = Task(user_id=user_id, title=title, completed=False)

            # Persist to database
            self.session.add(task)
            self.session.commit()
            self.session.refresh(task)

            return task

        except Exception as e:
            self.session.rollback()
            if "ValidationError" in str(type(e)):
                raise  # Re-raise validation errors
            raise DatabaseUnavailableError(f"Failed to create task: {e}") from e

    def get_tasks_for_user(self, user_id: str) -> list[Task]:
        """Retrieve all tasks for a specific user.

        SECURITY CRITICAL: ALL queries MUST filter by user_id to enforce
        user isolation (Constitutional Principle II). This ensures zero data
        leakage between users - alice NEVER sees bob's tasks and vice versa.

        Args:
            user_id: The ID of the user whose tasks to retrieve.

        Returns:
            List of Task objects belonging to the user.

        Raises:
            DatabaseUnavailableError: If database operation fails.
        """
        try:
            statement = select(Task).where(Task.user_id == user_id)
            tasks = self.session.exec(statement).all()
            return list(tasks)

        except Exception as e:
            raise DatabaseUnavailableError(f"Failed to retrieve tasks: {e}") from e
