import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context

# Add parent directory to path to import src modules
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Set DATABASE_URL from environment variable
database_url = os.getenv("DATABASE_URL")
if database_url:
    # Convert postgresql:// to postgresql+asyncpg:// for async support
    if database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)

    # Convert Neon SSL parameters to asyncpg-compatible format
    # asyncpg does NOT support 'sslmode' or 'channel_binding' parameters
    import re
    # Remove sslmode and replace with ssl=require
    database_url = re.sub(r'[?&]sslmode=\w+', '', database_url)
    # Remove channel_binding parameter
    database_url = re.sub(r'[?&]channel_binding=\w+', '', database_url)
    # Add ssl=require if not present
    if 'ssl=' not in database_url:
        separator = '&' if '?' in database_url else '?'
        database_url = database_url + separator + 'ssl=require'

    config.set_main_option("sqlalchemy.url", database_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import SQLModel metadata for autogenerate support
# NOTE: Models import disabled due to Pydantic 2.12.5 compatibility issue
# Manual migrations are used instead (see versions/001_*.py, 002_*.py)
from sqlmodel import SQLModel

# Uncomment when Pydantic compatibility is fixed:
# from src.models.user import User  # noqa: F401
# from src.models.task import Task  # noqa: F401

target_metadata = SQLModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Use async engine for PostgreSQL with asyncpg
    import asyncio

    async def run_async_migrations():
        """Run migrations asynchronously with asyncpg."""
        connectable = create_async_engine(
            config.get_main_option("sqlalchemy.url"),
            poolclass=pool.NullPool,
        )

        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)

        await connectable.dispose()

    def do_run_migrations(connection):
        """Helper function to run migrations within async context."""
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # Detect column type changes
            compare_server_default=True,  # Detect default value changes
        )

        with context.begin_transaction():
            context.run_migrations()

    # Run async migrations
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
