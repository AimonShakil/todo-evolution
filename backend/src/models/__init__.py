"""
SQLModel entities for Phase II Web App.

This module exports all database models for use in application code and Alembic migrations.
"""

from .user import User
from .task import Task

__all__ = ["User", "Task"]
