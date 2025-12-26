"""
MCP tools for task management in Phase III - Agentic AI Chatbot.

These tools wrap the Phase II TaskService functions and provide JSON schemas
for the OpenAI agent to use. All tools enforce user data isolation and follow
the contracts defined in specs/004-phase-iii-ai-chatbot/contracts/*.json.

Constitutional Alignment:
- Principle II: User Data Isolation (all tools require user_id parameter)
- Principle IX: Code Quality Standards (type hints, docstrings, validation)
- Principle XXVI: Agent Tools (MCP integration for natural language interaction)
"""

from typing import Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.services.task_service import (
    create_task as service_create_task,
    delete_task as service_delete_task,
    get_all_tasks,
    toggle_task_completed,
    update_task as service_update_task,
)


async def add_task(
    session: AsyncSession,
    user_id: int,
    title: str,
    description: Optional[str] = None,
) -> dict[str, Any]:
    """
    Create a new task for the authenticated user.

    MCP Tool Contract: specs/004-phase-iii-ai-chatbot/contracts/add_task.json

    Args:
        session: Async database session
        user_id: Authenticated user's ID (from JWT token)
        title: Task title (1-200 characters)
        description: Optional task description (max 1000 characters)

    Returns:
        Dict with:
        - success: bool
        - task: created task object (dict)
        - message: user-friendly confirmation message

    Example:
        >>> result = await add_task(session, user_id=1, title="Buy milk")
        >>> result["success"]
        True
        >>> result["message"]
        'Added task: Buy milk'
    """
    try:
        task = await service_create_task(
            session=session,
            user_id=user_id,
            title=title,
            description=description,
        )

        return {
            "success": True,
            "task": {
                "id": task.id,
                "user_id": task.user_id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat(),
            },
            "message": f"Added task: {task.title}",
        }
    except Exception as e:
        return {
            "success": False,
            "task": None,
            "message": f"Failed to create task: {str(e)}",
        }


async def list_tasks(
    session: AsyncSession,
    user_id: int,
    status: str = "all",
) -> dict[str, Any]:
    """
    Retrieve all tasks or filtered tasks for the authenticated user.

    MCP Tool Contract: specs/004-phase-iii-ai-chatbot/contracts/list_tasks.json

    Args:
        session: Async database session
        user_id: Authenticated user's ID (from JWT token)
        status: Filter by status ("all", "pending", "completed")

    Returns:
        Dict with:
        - success: bool
        - tasks: list of task objects (dicts)
        - count: number of tasks returned
        - message: user-friendly summary

    Example:
        >>> result = await list_tasks(session, user_id=1, status="pending")
        >>> result["count"]
        3
        >>> result["message"]
        'You have 3 pending tasks'
    """
    try:
        all_tasks = await get_all_tasks(session=session, user_id=user_id)

        # Filter by status
        if status == "pending":
            filtered_tasks = [t for t in all_tasks if not t.completed]
        elif status == "completed":
            filtered_tasks = [t for t in all_tasks if t.completed]
        else:  # "all"
            filtered_tasks = all_tasks

        # Convert to dicts
        task_dicts = [
            {
                "id": task.id,
                "user_id": task.user_id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat(),
            }
            for task in filtered_tasks
        ]

        # Generate friendly message (T043 - handle empty lists)
        pending_count = sum(1 for t in all_tasks if not t.completed)
        completed_count = sum(1 for t in all_tasks if t.completed)

        if status == "all":
            if len(all_tasks) == 0:
                message = "You have no tasks yet. Create your first task to get started!"
            else:
                message = f"You have {pending_count} pending tasks and {completed_count} completed tasks"
        elif status == "pending":
            if pending_count == 0:
                message = "You have no pending tasks. Great job staying on top of things!"
            else:
                message = f"You have {pending_count} pending tasks"
        else:  # "completed"
            if completed_count == 0:
                message = "You haven't completed any tasks yet. Keep working on your list!"
            else:
                message = f"You have {completed_count} completed tasks"

        return {
            "success": True,
            "tasks": task_dicts,
            "count": len(task_dicts),
            "message": message,
        }
    except Exception as e:
        return {
            "success": False,
            "tasks": [],
            "count": 0,
            "message": f"Failed to retrieve tasks: {str(e)}",
        }


async def complete_task(
    session: AsyncSession,
    user_id: int,
    task_id: Optional[int] = None,
    search_term: Optional[str] = None,
) -> dict[str, Any]:
    """
    Mark a task as completed for the authenticated user.

    MCP Tool Contract: specs/004-phase-iii-ai-chatbot/contracts/complete_task.json

    Args:
        session: Async database session
        user_id: Authenticated user's ID (from JWT token)
        task_id: ID of the task to complete (if known)
        search_term: Search term to find task by title (if task_id not provided)

    Returns:
        Dict with:
        - success: bool
        - task: updated task object (dict) or None
        - message: user-friendly confirmation message
        - matches: list of matching tasks (if multiple matches found)

    Example:
        >>> result = await complete_task(session, user_id=1, task_id=42)
        >>> result["success"]
        True
        >>> result["message"]
        'Completed task: Buy milk'

        >>> result = await complete_task(session, user_id=1, search_term="milk")
        >>> # Finds task automatically if only 1 match
    """
    try:
        # T047: Multi-task match handling (Edge Case 3)
        if task_id is None and search_term:
            # Search for matching tasks by title
            all_tasks = await get_all_tasks(session=session, user_id=user_id)
            matching_tasks = [
                t for t in all_tasks
                if search_term.lower() in t.title.lower() and not t.completed
            ]

            if len(matching_tasks) == 0:
                return {
                    "success": False,
                    "task": None,
                    "message": f"I couldn't find a pending task matching '{search_term}'. Would you like me to create one?",
                    "matches": [],
                }

            if len(matching_tasks) > 1:
                task_list = "\n".join(
                    [f"{i+1}. {task.title} (ID: {task.id})" for i, task in enumerate(matching_tasks)]
                )
                return {
                    "success": False,
                    "task": None,
                    "message": f"I found {len(matching_tasks)} pending tasks matching '{search_term}':\n{task_list}\n\nPlease specify which one you want to complete.",
                    "matches": [
                        {
                            "id": t.id,
                            "title": t.title,
                            "description": t.description,
                        }
                        for t in matching_tasks
                    ],
                }

            # Exactly 1 match - proceed
            task_id = matching_tasks[0].id

        # Proceed with completion
        if task_id is None:
            return {
                "success": False,
                "task": None,
                "message": "Please provide either a task_id or search_term to complete a task.",
            }

        # Mark task as completed
        task = await toggle_task_completed(
            session=session,
            user_id=user_id,
            task_id=task_id,
        )

        if not task:
            return {
                "success": False,
                "task": None,
                "message": f"Task {task_id} not found or does not belong to you",
            }

        # Ensure task is marked as completed (toggle might have uncompleted it)
        if not task.completed:
            task = await toggle_task_completed(
                session=session,
                user_id=user_id,
                task_id=task_id,
            )

        return {
            "success": True,
            "task": {
                "id": task.id,
                "user_id": task.user_id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat(),
            },
            "message": f"Completed task: {task.title}",
        }
    except Exception as e:
        return {
            "success": False,
            "task": None,
            "message": f"Failed to complete task: {str(e)}",
        }


async def delete_task(
    session: AsyncSession,
    user_id: int,
    task_id: Optional[int] = None,
    search_term: Optional[str] = None,
) -> dict[str, Any]:
    """
    Permanently delete a task for the authenticated user.

    MCP Tool Contract: specs/004-phase-iii-ai-chatbot/contracts/delete_task.json

    Args:
        session: Async database session
        user_id: Authenticated user's ID (from JWT token)
        task_id: ID of the task to delete (if known)
        search_term: Search term to find task by title (if task_id not provided)

    Returns:
        Dict with:
        - success: bool
        - deleted_task_id: ID of deleted task or None
        - message: user-friendly confirmation message
        - matches: list of matching tasks (if multiple matches found)

    Example:
        >>> result = await delete_task(session, user_id=1, task_id=42)
        >>> result["success"]
        True
        >>> result["message"]
        'Deleted task: Buy milk'

        >>> result = await delete_task(session, user_id=1, search_term="milk")
        >>> # Finds task automatically if only 1 match
    """
    try:
        # T048: Multi-task match handling (Edge Case 3)
        if task_id is None and search_term:
            # Search for matching tasks by title
            all_tasks = await get_all_tasks(session=session, user_id=user_id)
            matching_tasks = [
                t for t in all_tasks
                if search_term.lower() in t.title.lower()
            ]

            if len(matching_tasks) == 0:
                return {
                    "success": False,
                    "deleted_task_id": None,
                    "message": f"I couldn't find a task matching '{search_term}'.",
                    "matches": [],
                }

            if len(matching_tasks) > 1:
                task_list = "\n".join(
                    [f"{i+1}. {task.title} (ID: {task.id})" for i, task in enumerate(matching_tasks)]
                )
                return {
                    "success": False,
                    "deleted_task_id": None,
                    "message": f"I found {len(matching_tasks)} tasks matching '{search_term}':\n{task_list}\n\nPlease specify which one you want to delete.",
                    "matches": [
                        {
                            "id": t.id,
                            "title": t.title,
                            "description": t.description,
                        }
                        for t in matching_tasks
                    ],
                }

            # Exactly 1 match - proceed
            task_id = matching_tasks[0].id

        # Proceed with deletion
        if task_id is None:
            return {
                "success": False,
                "deleted_task_id": None,
                "message": "Please provide either a task_id or search_term to delete a task.",
            }

        # Get task title before deletion for message
        from src.services.task_service import get_task

        task = await get_task(session=session, user_id=user_id, task_id=task_id)

        if not task:
            return {
                "success": False,
                "deleted_task_id": None,
                "message": f"Task {task_id} not found or does not belong to you",
            }

        task_title = task.title
        success = await service_delete_task(
            session=session,
            user_id=user_id,
            task_id=task_id,
        )

        if success:
            return {
                "success": True,
                "deleted_task_id": task_id,
                "message": f"Deleted task: {task_title}",
            }
        else:
            return {
                "success": False,
                "deleted_task_id": None,
                "message": f"Failed to delete task {task_id}",
            }
    except Exception as e:
        return {
            "success": False,
            "deleted_task_id": None,
            "message": f"Failed to delete task: {str(e)}",
        }


async def update_task(
    session: AsyncSession,
    user_id: int,
    task_id: Optional[int] = None,
    search_term: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    completed: Optional[bool] = None,
) -> dict[str, Any]:
    """
    Update the title, description, or completion status of an existing task.

    MCP Tool Contract: specs/004-phase-iii-ai-chatbot/contracts/update_task.json

    Args:
        session: Async database session
        user_id: Authenticated user's ID (from JWT token)
        task_id: ID of the task to update (if known)
        search_term: Search term to find task by title (if task_id not provided)
        title: New title (optional, 1-200 characters)
        description: New description (optional, max 1000 characters)
        completed: New completion status (optional)

    Returns:
        Dict with:
        - success: bool
        - task: updated task object (dict) or None
        - message: user-friendly confirmation message
        - matches: list of matching tasks (if multiple matches found)

    Example:
        >>> result = await update_task(
        ...     session,
        ...     user_id=1,
        ...     task_id=42,
        ...     title="Buy groceries and supplies"
        ... )
        >>> result["success"]
        True
        >>> result["message"]
        'Updated task: Buy groceries and supplies'

        >>> result = await update_task(
        ...     session,
        ...     user_id=1,
        ...     search_term="milk",
        ...     title="Buy organic milk"
        ... )
        >>> # Finds task automatically if only 1 match
    """
    try:
        # T049: Multi-task match handling (Edge Case 3)
        if task_id is None and search_term:
            # Search for matching tasks by title
            all_tasks = await get_all_tasks(session=session, user_id=user_id)
            matching_tasks = [
                t for t in all_tasks
                if search_term.lower() in t.title.lower()
            ]

            if len(matching_tasks) == 0:
                return {
                    "success": False,
                    "task": None,
                    "message": f"I couldn't find a task matching '{search_term}'.",
                    "matches": [],
                }

            if len(matching_tasks) > 1:
                task_list = "\n".join(
                    [f"{i+1}. {task.title} (ID: {task.id})" for i, task in enumerate(matching_tasks)]
                )
                return {
                    "success": False,
                    "task": None,
                    "message": f"I found {len(matching_tasks)} tasks matching '{search_term}':\n{task_list}\n\nPlease specify which one you want to update.",
                    "matches": [
                        {
                            "id": t.id,
                            "title": t.title,
                            "description": t.description,
                        }
                        for t in matching_tasks
                    ],
                }

            # Exactly 1 match - proceed
            task_id = matching_tasks[0].id

        # Proceed with update
        if task_id is None:
            return {
                "success": False,
                "task": None,
                "message": "Please provide either a task_id or search_term to update a task.",
            }

        task = await service_update_task(
            session=session,
            user_id=user_id,
            task_id=task_id,
            title=title,
            description=description,
            completed=completed,
        )

        if not task:
            return {
                "success": False,
                "task": None,
                "message": f"Task {task_id} not found or does not belong to you",
            }

        return {
            "success": True,
            "task": {
                "id": task.id,
                "user_id": task.user_id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat(),
            },
            "message": f"Updated task: {task.title}",
        }
    except Exception as e:
        return {
            "success": False,
            "task": None,
            "message": f"Failed to update task: {str(e)}",
        }
