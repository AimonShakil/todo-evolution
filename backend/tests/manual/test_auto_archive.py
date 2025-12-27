"""
Manual test script for T065: Auto-archive functionality validation.

This script creates a conversation with 500 messages and verifies that:
1. Messages are created successfully
2. Conversation is automatically archived at the 500-message threshold
3. Auto-archive triggers exactly at 500 messages (not before, not after)

Constitutional Alignment:
- Principle II: User Data Isolation (uses test user ID)
- Principle IX: Code Quality Standards (async/await, type hints)

Usage:
    cd backend
    python -m tests.manual.test_auto_archive

Expected Output:
    ✓ Created conversation 123 for test user
    ✓ Creating 500 messages...
    ✓ Message count after 499 messages: 499
    ✓ Conversation still active: True
    ✓ Message count after 500 messages: 500
    ✓ Conversation auto-archived: True
    ✓ Auto-archive test PASSED
"""

import asyncio
import sys
from pathlib import Path

# Add backend to Python path for src module imports
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy.ext.asyncio import AsyncSession

from src.lib.database import get_session
from src.models.user import User
from src.services.conversation_service import create_conversation
from src.services.message_service import count_messages, create_message


async def test_auto_archive():
    """Test that conversations are auto-archived at 500 messages."""
    print("Starting auto-archive test...")
    print("-" * 60)

    # Get database session
    async for session in get_session():
        # Create or use test user (user_id=1 for simplicity)
        test_user_id = 1
        print(f"✓ Using test user ID: {test_user_id}")

        # Create a new conversation
        conversation = await create_conversation(session, test_user_id)
        print(f"✓ Created conversation {conversation.id} for test user")

        # Create 499 messages (just before threshold)
        print("✓ Creating 499 messages...")
        for i in range(499):
            role = "user" if i % 2 == 0 else "assistant"
            await create_message(
                session=session,
                conversation_id=conversation.id,
                user_id=test_user_id,
                role=role,
                content=f"Test message {i + 1}",
            )
            if (i + 1) % 100 == 0:
                print(f"  - Created {i + 1} messages...")

        # Verify count and active status after 499 messages
        count_before = await count_messages(
            session, conversation.id, test_user_id
        )
        await session.refresh(conversation)
        active_before = conversation.is_active

        print(f"✓ Message count after 499 messages: {count_before}")
        print(f"✓ Conversation still active: {active_before}")

        # Verify conversation is NOT archived yet
        if not active_before:
            print("✗ FAILED: Conversation archived too early (before 500 messages)")
            return False

        if count_before != 499:
            print(f"✗ FAILED: Expected 499 messages, got {count_before}")
            return False

        # Create the 500th message (should trigger auto-archive)
        print("✓ Creating 500th message (should trigger auto-archive)...")
        await create_message(
            session=session,
            conversation_id=conversation.id,
            user_id=test_user_id,
            role="user",
            content="Test message 500 - this should trigger auto-archive",
        )

        # Verify count and active status after 500 messages
        count_after = await count_messages(
            session, conversation.id, test_user_id
        )
        await session.refresh(conversation)
        active_after = conversation.is_active

        print(f"✓ Message count after 500 messages: {count_after}")
        print(f"✓ Conversation auto-archived: {not active_after}")

        # Validate results
        success = True
        print("-" * 60)
        print("Validation Results:")

        if count_after != 500:
            print(f"  ✗ FAILED: Expected 500 messages, got {count_after}")
            success = False
        else:
            print(f"  ✓ Message count correct: {count_after}")

        if active_after:
            print("  ✗ FAILED: Conversation should be archived after 500 messages")
            success = False
        else:
            print("  ✓ Conversation correctly archived")

        if success:
            print("-" * 60)
            print("✓ Auto-archive test PASSED")
            print(
                "  - Conversation remained active for 499 messages"
            )
            print(
                "  - Conversation auto-archived at exactly 500 messages"
            )
        else:
            print("-" * 60)
            print("✗ Auto-archive test FAILED")

        return success


if __name__ == "__main__":
    success = asyncio.run(test_auto_archive())
    sys.exit(0 if success else 1)
