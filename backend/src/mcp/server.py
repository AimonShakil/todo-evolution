"""
MCP server setup for Phase III - Agentic AI Chatbot.

This module registers all MCP tools with the OpenAI Agents SDK. The MCP server
runs co-located with the FastAPI backend (not a separate process) per ADR-005.

Constitutional Alignment:
- Principle IV: Smallest Viable Change (in-process deployment, no microservices)
- Principle IX: Code Quality Standards (clear tool registration)
- Principle XXVI: Agent Tools (MCP integration with OpenAI Agents SDK)

ADR References:
- ADR-005: MCP server co-located with FastAPI backend (simplicity, performance)
"""

from typing import Any, Callable

from sqlalchemy.ext.asyncio import AsyncSession

from .tools import (
    add_task,
    complete_task,
    delete_task,
    list_tasks,
    update_task,
)


def get_tool_schemas() -> list[dict[str, Any]]:
    """
    Get JSON schemas for all MCP tools.

    Returns OpenAI-compatible tool definitions that can be passed to the
    Agents SDK run() method.

    Returns:
        List of tool schemas in OpenAI function calling format

    Example:
        >>> schemas = get_tool_schemas()
        >>> len(schemas)
        5
        >>> schemas[0]["name"]
        'add_task'
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "add_task",
                "description": "Create a new task for the authenticated user. Use when user wants to add, create, remember, or track something. Examples: 'I need to buy milk', 'Remember to call the dentist', 'Add task: finish report'.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "The task title (1-200 characters). Extract from user's natural language input.",
                        },
                        "description": {
                            "type": "string",
                            "description": "Optional detailed description of the task. Use when user provides additional context.",
                        },
                    },
                    "required": ["title"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "list_tasks",
                "description": "Retrieve all tasks or filtered tasks for the authenticated user. Use when user asks about their tasks, wants to see their list, or queries task status. Examples: 'What tasks do I have?', 'Show me my incomplete tasks', 'What's on my list?'.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "enum": ["all", "pending", "completed"],
                            "description": "Filter tasks by completion status. Use 'pending' for incomplete tasks, 'completed' for done tasks, 'all' for both.",
                            "default": "all",
                        },
                    },
                    "required": [],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "complete_task",
                "description": "Mark a task as completed. Use when user indicates they've finished, completed, or done a task. Examples: 'Mark the grocery task as done', 'I finished buying milk', 'Complete my dentist task'. If task_id is not provided, use list_tasks first to find the matching task.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "integer",
                            "description": "The unique ID of the task to complete. If not provided by user, use list_tasks to find matching task by title/description.",
                        },
                    },
                    "required": ["task_id"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "delete_task",
                "description": "Permanently delete a task. Use when user wants to remove, delete, or discard a task. Examples: 'Delete my dentist task', 'Remove the grocery item', 'Get rid of that task'. If task_id is not provided, use list_tasks first to find the matching task.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "integer",
                            "description": "The unique ID of the task to delete. If not provided by user, use list_tasks to find matching task by title/description.",
                        },
                    },
                    "required": ["task_id"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "update_task",
                "description": "Update the title, description, or completion status of an existing task. Use when user wants to modify, change, edit, or update a task. Examples: 'Change my report task to finish by Friday', 'Update the grocery list to include eggs', 'Actually, make it almond milk instead'. If task_id is not provided, use list_tasks first to find the matching task.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "integer",
                            "description": "The unique ID of the task to update. If not provided by user, use list_tasks to find matching task by title/description.",
                        },
                        "title": {
                            "type": "string",
                            "description": "New title for the task (1-200 characters). Only include if user wants to change the title.",
                        },
                        "description": {
                            "type": "string",
                            "description": "New description for the task. Only include if user wants to change the description.",
                        },
                        "completed": {
                            "type": "boolean",
                            "description": "New completion status. Only include if user wants to toggle completion (prefer complete_task for marking as done).",
                        },
                    },
                    "required": ["task_id"],
                },
            },
        },
    ]


def get_tool_implementations() -> dict[str, Callable]:
    """
    Get mapping of tool names to their implementation functions.

    Returns:
        Dict mapping tool names to async callable functions

    Example:
        >>> tools = get_tool_implementations()
        >>> "add_task" in tools
        True
        >>> len(tools)
        5
    """
    return {
        "add_task": add_task,
        "list_tasks": list_tasks,
        "complete_task": complete_task,
        "delete_task": delete_task,
        "update_task": update_task,
    }


async def execute_tool(
    tool_name: str,
    session: AsyncSession,
    user_id: int,
    **kwargs: Any,
) -> dict[str, Any]:
    """
    Execute a tool by name with given parameters.

    This is a convenience function for the AgentService to call tools dynamically.
    All tools receive session and user_id automatically, plus any additional kwargs.

    Args:
        tool_name: Name of the tool to execute
        session: Async database session
        user_id: Authenticated user's ID
        **kwargs: Tool-specific parameters

    Returns:
        Tool execution result (dict with success, message, etc.)

    Raises:
        ValueError: If tool_name is not recognized

    Example:
        >>> result = await execute_tool(
        ...     "add_task",
        ...     session,
        ...     user_id=1,
        ...     title="Buy milk"
        ... )
        >>> result["success"]
        True
    """
    tools = get_tool_implementations()

    if tool_name not in tools:
        return {
            "success": False,
            "message": f"Unknown tool: {tool_name}",
        }

    tool_func = tools[tool_name]
    return await tool_func(session=session, user_id=user_id, **kwargs)
