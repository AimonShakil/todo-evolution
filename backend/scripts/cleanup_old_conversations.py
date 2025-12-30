#!/usr/bin/env python3
"""
Cleanup script for old conversations (90-day retention policy).

This script deletes conversations and their associated messages that are older
than 90 days to enforce data retention policy (FR-020).

Constitutional Alignment:
- Principle II: User Data Isolation (respects user boundaries)
- Principle XVI: Error Handling & Logging (comprehensive logging)
- FR-020: Automated data retention enforcement

Usage:
    # Dry run (preview what would be deleted):
    python backend/scripts/cleanup_old_conversations.py --dry-run

    # Actually delete old conversations:
    python backend/scripts/cleanup_old_conversations.py

    # Custom retention period (e.g., 30 days):
    python backend/scripts/cleanup_old_conversations.py --days 30

    # Verbose output:
    python backend/scripts/cleanup_old_conversations.py --verbose
"""

import argparse
import asyncio
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add backend/src to Python path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.lib.database import async_session_maker
from src.models.conversation import Conversation
from src.models.message import Message


async def get_old_conversations(
    session: AsyncSession, days: int = 90, verbose: bool = False
) -> list[Conversation]:
    """
    Fetch conversations older than specified days.

    Args:
        session: Database session
        days: Number of days for retention (default: 90)
        verbose: Enable verbose logging

    Returns:
        List of conversations to be deleted
    """
    # Use naive UTC datetime to match database schema
    # Database stores created_at as naive datetime (TIMESTAMP WITHOUT TIME ZONE)
    from datetime import UTC
    cutoff_date = datetime.now(UTC).replace(tzinfo=None) - timedelta(days=days)

    if verbose:
        print(f"🔍 Searching for conversations created before {cutoff_date.isoformat()}")

    # Query conversations older than cutoff date
    statement = select(Conversation).where(Conversation.created_at < cutoff_date)
    result = await session.execute(statement)
    conversations = result.scalars().all()

    if verbose:
        print(f"📊 Found {len(conversations)} conversations older than {days} days")

    return list(conversations)


async def count_messages_for_conversation(
    session: AsyncSession, conversation_id: int
) -> int:
    """
    Count messages in a conversation.

    Args:
        session: Database session
        conversation_id: Conversation ID

    Returns:
        Message count
    """
    statement = select(Message).where(Message.conversation_id == conversation_id)
    result = await session.execute(statement)
    messages = result.scalars().all()
    return len(messages)


async def delete_old_conversations(
    session: AsyncSession,
    conversations: list[Conversation],
    dry_run: bool = False,
    verbose: bool = False,
) -> dict:
    """
    Delete old conversations and their messages.

    Args:
        session: Database session
        conversations: List of conversations to delete
        dry_run: If True, only preview deletion without executing
        verbose: Enable verbose logging

    Returns:
        Dictionary with deletion statistics
    """
    total_conversations = len(conversations)
    total_messages = 0

    if total_conversations == 0:
        print("✅ No conversations to delete.")
        return {"conversations_deleted": 0, "messages_deleted": 0}

    # Count messages for each conversation
    for conversation in conversations:
        message_count = await count_messages_for_conversation(
            session, conversation.id
        )
        total_messages += message_count

        if verbose:
            print(
                f"  - Conversation #{conversation.id} (User {conversation.user_id}): "
                f"{message_count} messages, created {conversation.created_at.isoformat()}"
            )

    if dry_run:
        print(f"\n🔍 DRY RUN: Would delete {total_conversations} conversations")
        print(f"   and approximately {total_messages} messages")
        print("\n   Run without --dry-run to actually delete these conversations.")
        return {"conversations_deleted": 0, "messages_deleted": 0}

    # Actually delete conversations
    print(f"\n🗑️  Deleting {total_conversations} conversations...")

    for conversation in conversations:
        # Delete associated messages first (explicit deletion for clarity)
        message_stmt = select(Message).where(
            Message.conversation_id == conversation.id
        )
        message_result = await session.execute(message_stmt)
        messages = message_result.scalars().all()

        for message in messages:
            await session.delete(message)

        # Delete conversation
        await session.delete(conversation)

        if verbose:
            print(f"  ✓ Deleted conversation #{conversation.id}")

    # Commit the transaction
    await session.commit()

    print(f"✅ Successfully deleted {total_conversations} conversations")
    print(f"   and {total_messages} messages")

    return {
        "conversations_deleted": total_conversations,
        "messages_deleted": total_messages,
    }


async def cleanup_main(args: argparse.Namespace) -> None:
    """
    Main cleanup function.

    Args:
        args: Parsed command-line arguments
    """
    print("=" * 60)
    print("🧹 Conversation Cleanup Script")
    print(f"   Retention Period: {args.days} days")
    print(f"   Mode: {'DRY RUN' if args.dry_run else 'EXECUTE'}")
    print("=" * 60)
    print()

    async with async_session_maker() as session:
        try:
            # Fetch old conversations
            conversations = await get_old_conversations(
                session, days=args.days, verbose=args.verbose
            )

            # Delete or preview deletion
            stats = await delete_old_conversations(
                session,
                conversations,
                dry_run=args.dry_run,
                verbose=args.verbose,
            )

            print()
            print("=" * 60)
            print("📊 Cleanup Summary")
            print(f"   Conversations deleted: {stats['conversations_deleted']}")
            print(f"   Messages deleted: {stats['messages_deleted']}")
            print("=" * 60)

        except Exception as e:
            print(f"\n❌ Error during cleanup: {e}", file=sys.stderr)
            if args.verbose:
                import traceback

                traceback.print_exc()
            sys.exit(1)


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Cleanup old conversations (90-day retention policy)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Preview what would be deleted (dry run):
  python backend/scripts/cleanup_old_conversations.py --dry-run

  # Actually delete old conversations:
  python backend/scripts/cleanup_old_conversations.py

  # Custom retention (30 days):
  python backend/scripts/cleanup_old_conversations.py --days 30

  # Verbose output:
  python backend/scripts/cleanup_old_conversations.py --verbose
        """,
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview deletion without actually deleting (default: False)",
    )

    parser.add_argument(
        "--days",
        type=int,
        default=90,
        help="Retention period in days (default: 90)",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output (default: False)",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(cleanup_main(args))
