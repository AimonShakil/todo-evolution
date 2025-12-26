"""
MCP (Model Context Protocol) tools package for Phase III - Agentic AI Chatbot.

This package provides MCP tools that the OpenAI agent can use to interact with
the task management system. Tools are registered with the agent and wrapped in
JSON schemas for type safety.

Constitutional Alignment:
- Principle II: User Data Isolation (all tools enforce user_id filtering)
- Principle IX: Code Quality Standards (type hints, docstrings, contracts)
- Principle XXVI: Agent Tools (MCP integration for agentic interactions)
"""

from .tools import (
    add_task,
    complete_task,
    delete_task,
    list_tasks,
    update_task,
)

__all__ = [
    "add_task",
    "list_tasks",
    "complete_task",
    "delete_task",
    "update_task",
]
