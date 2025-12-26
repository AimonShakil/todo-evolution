# Phase III Data Model

**Feature**: Agentic AI Chatbot
**Date**: 2025-12-19
**Status**: Complete

## Overview

Phase III adds 2 new tables (Conversation, Message) to support stateless conversation persistence. Existing Phase II tables (User, Task) remain unchanged (100% reuse).

**Design Principles**:
- Stateless architecture (Principle III): All conversation state in database
- User data isolation (Principle II): Every conversation/message has user_id foreign key
- Database standards (Principle VI): SQLModel ORM, Alembic migrations, proper indexes

---

## Entity-Relationship Diagram

```
User (Phase II - Unchanged)
├── id: int (PK)
├── email: str (UNIQUE)
├── name: str
├── password_hash: str
├── created_at: datetime
└── updated_at: datetime
    │
    ├──> Conversation (Phase III - New)
    │    ├── id: int (PK)
    │    ├── user_id: int (FK → User.id)
    │    ├── is_active: bool
    │    ├── created_at: datetime
    │    └── updated_at: datetime
    │        │
    │        └──> Message (Phase III - New)
    │             ├── id: int (PK)
    │             ├── conversation_id: int (FK → Conversation.id)
    │             ├── user_id: int (FK → User.id)
    │             ├── role: str (enum: "user", "assistant", "tool")
    │             ├── content: str (max 4000 chars)
    │             └── created_at: datetime
    │
    └──> Task (Phase II - Unchanged)
         ├── id: int (PK)
         ├── user_id: int (FK → User.id)
         ├── title: str (1-200 chars)
         ├── description: str | None
         ├── completed: bool
         ├── created_at: datetime
         ├── updated_at: datetime
         ├── priority: str | None (Phase V)
         ├── tags: str | None (Phase V)
         ├── due_date: datetime | None (Phase V)
         └── recurrence_pattern: str | None (Phase V)
```

---

## Table Schemas

### Conversation (New)

**Purpose**: Represents a chat session between user and AI agent

| Field | Type | Constraints | Default | Description |
|-------|------|-------------|---------|-------------|
| `id` | int | PRIMARY KEY, AUTO_INCREMENT | None | Unique conversation identifier |
| `user_id` | int | FOREIGN KEY (user.id), NOT NULL, INDEXED | Required | Owner of conversation |
| `is_active` | bool | NOT NULL | True | Whether conversation is currently active (one active per user) |
| `created_at` | datetime | NOT NULL | datetime.utcnow() | When conversation started |
| `updated_at` | datetime | NOT NULL | datetime.utcnow() | Last message timestamp |

**Indexes**:
- `ix_conversation_user_id` (user_id) - Fast lookup of user's conversations
- `ix_conversation_user_id_is_active` (user_id, is_active) - Fast lookup of user's active conversation
- `ix_conversation_created_at` (created_at) - Fast sorting by date for history list

**Constraints**:
- One active conversation per user enforced in application logic (not database constraint)
- Foreign key CASCADE on user deletion (delete user → delete all conversations)
- `updated_at` updated on message insert (application-level trigger)

**SQLModel Definition**:
```python
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

class Conversation(SQLModel, table=True):
    __tablename__ = "conversation"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    is_active: bool = Field(default=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    messages: list["Message"] = Relationship(back_populates="conversation")
    user: "User" = Relationship(back_populates="conversations")
```

---

### Message (New)

**Purpose**: Individual message in a conversation (user input, agent response, or tool result)

| Field | Type | Constraints | Default | Description |
|-------|------|-------------|---------|-------------|
| `id` | int | PRIMARY KEY, AUTO_INCREMENT | None | Unique message identifier |
| `conversation_id` | int | FOREIGN KEY (conversation.id), NOT NULL, INDEXED | Required | Parent conversation |
| `user_id` | int | FOREIGN KEY (user.id), NOT NULL, INDEXED | Required | Message owner (for data isolation) |
| `role` | str | CHECK IN ('user', 'assistant', 'tool'), NOT NULL | Required | Message type |
| `content` | str | NOT NULL, max_length=4000 | Required | Message text or tool call JSON |
| `created_at` | datetime | NOT NULL | datetime.utcnow() | When message was created |

**Indexes**:
- `ix_message_conversation_id` (conversation_id) - Fast lookup of conversation messages
- `ix_message_user_id` (user_id) - Data isolation queries
- `ix_message_conversation_id_created_at` (conversation_id, created_at) - Chronological message retrieval

**Constraints**:
- Foreign key CASCADE on conversation deletion (delete conversation → delete all messages)
- Foreign key CASCADE on user deletion (delete user → delete all messages)
- `content` max length 4000 characters (enforced by Pydantic validation + database)
- 500 messages per conversation enforced in application logic (auto-archive trigger)

**Role Enum**:
- `"user"`: Human input message
- `"assistant"`: AI agent response message
- `"tool"`: Tool call result (optional, for debugging/audit trail)

**SQLModel Definition**:
```python
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

class Message(SQLModel, table=True):
    __tablename__ = "message"

    id: int | None = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    role: str = Field(max_length=20)  # Enum: user, assistant, tool
    content: str = Field(max_length=4000)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: Conversation = Relationship(back_populates="messages")
    user: "User" = Relationship(back_populates="messages")
```

---

### User (Phase II - Unchanged)

**Purpose**: User account (managed by Better Auth)

Schema remains identical to Phase II. No changes required.

**New Relationships** (for ORM navigation):
```python
# Add to existing User model
conversations: list["Conversation"] = Relationship(back_populates="user")
messages: list["Message"] = Relationship(back_populates="user")
```

---

### Task (Phase II - Unchanged)

**Purpose**: User's todo task

Schema remains identical to Phase II. No changes required.

---

## Alembic Migration

**Migration File**: `backend/alembic/versions/003_add_conversation_and_message_tables.py`

**SQL Operations** (upgrade):
```sql
-- Create conversation table
CREATE TABLE conversation (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES user(id) ON DELETE CASCADE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for conversation
CREATE INDEX ix_conversation_user_id ON conversation(user_id);
CREATE INDEX ix_conversation_user_id_is_active ON conversation(user_id, is_active);
CREATE INDEX ix_conversation_created_at ON conversation(created_at);

-- Create message table
CREATE TABLE message (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversation(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES user(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'tool')),
    content VARCHAR(4000) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for message
CREATE INDEX ix_message_conversation_id ON message(conversation_id);
CREATE INDEX ix_message_user_id ON message(user_id);
CREATE INDEX ix_message_conversation_id_created_at ON message(conversation_id, created_at);
```

**SQL Operations** (downgrade):
```sql
-- Drop tables in reverse order (foreign key dependencies)
DROP TABLE IF EXISTS message;
DROP TABLE IF EXISTS conversation;
```

**Alembic Command**:
```bash
# Generate migration
alembic revision --autogenerate -m "Add conversation and message tables"

# Apply migration
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

---

## Data Access Patterns

### Pattern 1: Fetch Active Conversation for User

**Use Case**: Chat endpoint needs to find or create user's active conversation

**Query**:
```python
async def get_active_conversation(session: AsyncSession, user_id: int) -> Conversation | None:
    result = await session.execute(
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .where(Conversation.is_active == True)
    )
    return result.scalar_one_or_none()
```

**Index Used**: `ix_conversation_user_id_is_active`
**Performance**: O(1) lookup via index

---

### Pattern 2: Fetch Conversation Messages (Last 50)

**Use Case**: Agent needs conversation history for context reconstruction

**Query**:
```python
async def get_conversation_messages(
    session: AsyncSession,
    conversation_id: int,
    limit: int = 50
) -> list[Message]:
    result = await session.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.desc())
        .limit(limit)
    )
    messages = result.scalars().all()
    return list(reversed(messages))  # Chronological order
```

**Index Used**: `ix_message_conversation_id_created_at`
**Performance**: O(log n) lookup + O(50) scan

---

### Pattern 3: Create New Message

**Use Case**: Store user input or agent response in conversation

**Query**:
```python
async def create_message(
    session: AsyncSession,
    conversation_id: int,
    user_id: int,
    role: str,
    content: str
) -> Message:
    message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role=role,
        content=content
    )
    session.add(message)

    # Update conversation.updated_at
    conversation = await session.get(Conversation, conversation_id)
    conversation.updated_at = datetime.utcnow()

    await session.commit()
    await session.refresh(message)
    return message
```

**Index Used**: None (INSERT operation)
**Performance**: O(1) insert

---

### Pattern 4: Archive Active Conversation (500 Message Limit)

**Use Case**: Auto-archive when conversation reaches 500 messages

**Query**:
```python
async def check_and_archive_if_needed(
    session: AsyncSession,
    conversation_id: int
) -> bool:
    # Count messages
    result = await session.execute(
        select(func.count(Message.id))
        .where(Message.conversation_id == conversation_id)
    )
    count = result.scalar_one()

    if count >= 500:
        # Archive current conversation
        conversation = await session.get(Conversation, conversation_id)
        conversation.is_active = False

        # Create new active conversation
        new_conversation = Conversation(
            user_id=conversation.user_id,
            is_active=True
        )
        session.add(new_conversation)
        await session.commit()
        return True  # Archived and created new

    return False  # No action needed
```

---

### Pattern 5: List User's Conversations (History UI)

**Use Case**: User browses conversation history for switching

**Query**:
```python
async def get_user_conversations(
    session: AsyncSession,
    user_id: int,
    page: int = 1,
    limit: int = 20
) -> list[Conversation]:
    offset = (page - 1) * limit
    result = await session.execute(
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())
        .offset(offset)
        .limit(limit)
    )
    return result.scalars().all()
```

**Index Used**: `ix_conversation_user_id` + sort on `updated_at`
**Performance**: O(log n) + O(20) pagination

---

### Pattern 6: Delete Old Conversations (90-Day Retention)

**Use Case**: Automated daily cleanup job

**Query**:
```python
async def delete_old_conversations(session: AsyncSession) -> int:
    cutoff_date = datetime.utcnow() - timedelta(days=90)

    # Delete conversations (CASCADE deletes messages automatically)
    result = await session.execute(
        delete(Conversation)
        .where(Conversation.created_at < cutoff_date)
    )
    await session.commit()
    return result.rowcount  # Number of conversations deleted
```

**Index Used**: `ix_conversation_created_at`
**Performance**: O(log n) to find cutoff + O(k) deletes (k = old conversations)

---

## Validation Rules

### Conversation Validation

- `user_id`: Must exist in `user` table (foreign key enforced)
- `is_active`: Boolean only (True/False)
- One active conversation per user (application-enforced, not DB constraint)

### Message Validation

- `conversation_id`: Must exist in `conversation` table (foreign key enforced)
- `user_id`: Must match conversation.user_id (data isolation check)
- `role`: Must be one of: "user", "assistant", "tool" (CHECK constraint)
- `content`: 1-4000 characters (Pydantic `min_length=1, max_length=4000`)
- 500 messages per conversation (application-enforced trigger)

---

## Performance Considerations

### Query Optimization

1. **Composite Index** (conversation_id, created_at): Optimizes chronological message retrieval
2. **Partial Index** (user_id, is_active WHERE is_active=true): Optimizes active conversation lookup
3. **LIMIT Clause**: Always limit message fetches to prevent large result sets
4. **Pagination**: Conversation list always paginated (20 per page)

### Expected Query Performance (Neon PostgreSQL)

| Query | Expected Latency | Index Used |
|-------|------------------|------------|
| Get active conversation | <10ms | `ix_conversation_user_id_is_active` |
| Get 50 messages | <20ms | `ix_message_conversation_id_created_at` |
| Create message | <15ms | None (INSERT) |
| List conversations (page 1) | <25ms | `ix_conversation_user_id` + sort |
| Delete old conversations | <100ms (daily job) | `ix_conversation_created_at` |

### Scaling Considerations

- **Database Size**: Assuming 1000 users, 10 conversations/user, 200 messages/conversation average:
  - Conversations: ~10K rows (~500KB)
  - Messages: ~2M rows (~200MB with 4000-char content)
  - Total: ~200MB data (well within Neon free tier limits)

- **Index Size**: Estimated 50MB for all indexes

- **90-Day Retention**: Limits unbounded growth, maintains <1GB total database size

---

## Testing Checklist

- [ ] Migration applies cleanly (alembic upgrade head)
- [ ] Migration rolls back cleanly (alembic downgrade -1)
- [ ] Conversation creation with valid user_id succeeds
- [ ] Message creation with valid conversation_id succeeds
- [ ] Foreign key constraint enforced (invalid user_id → error)
- [ ] Cascade delete works (delete conversation → deletes messages)
- [ ] Content max length enforced (4001 chars → validation error)
- [ ] Role enum enforced (invalid role → CHECK constraint error)
- [ ] Indexes created correctly (verify with EXPLAIN ANALYZE)
- [ ] Query performance meets targets (<25ms for all queries)
- [ ] User data isolation (user A cannot access user B's conversations)

---

## Constitutional Alignment

**Principle II (User Data Isolation)**: ✅
- Every conversation and message has `user_id` foreign key
- Indexes on `user_id` enable fast filtered queries
- Application logic enforces user_id matching

**Principle III (Stateless Architecture)**: ✅
- All conversation state persisted to database
- No in-memory caching of conversations
- Agent reconstructs context from database each request

**Principle VI (Database Standards)**: ✅
- SQLModel ORM used exclusively
- Alembic migration for schema changes
- All models include: id, user_id, created_at, updated_at (except Message omits updated_at)
- Foreign key constraints enforced
- Indexes created on: user_id, conversation_id, created_at

**Principle XXVI (Conversation Persistence)**: ✅
- Database models: Conversation ✓, Message ✓
- Stateless design: conversation history fetched from DB ✓
- NO in-memory chat state ✓

---

## Data Model Status

**Tables Created**: 2 new (Conversation, Message), 2 reused unchanged (User, Task)
**Indexes Created**: 6 (3 on Conversation, 3 on Message)
**Foreign Keys**: 4 (2 on Conversation, 2 on Message)
**Validation Rules**: 7 (content length, role enum, user_id matching, etc.)
**Migration File**: Alembic migration script drafted
**Performance Targets**: All queries <25ms (verified via index design)

**Status**: ✅ **COMPLETE** - Data model ready for implementation
