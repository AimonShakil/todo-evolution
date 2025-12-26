# Phase III Quickstart Guide

**Feature**: Agentic AI Chatbot
**Prerequisites**: Phase II backend and frontend fully functional
**Estimated Setup Time**: 30-45 minutes

---

## Overview

This guide covers:
1. Environment setup (OpenAI API key)
2. Backend setup (new dependencies, database migration)
3. Frontend setup (OpenAI ChatKit integration)
4. Running the application
5. Testing the agent
6. Deployment considerations

---

## Prerequisites

**Phase II Must Be Working**:
- ✅ Backend running on `http://localhost:8000`
- ✅ Frontend running on `http://localhost:3000`
- ✅ Database (Neon PostgreSQL) accessible
- ✅ User authentication (Better Auth + JWT) functional

**New Requirements**:
- OpenAI API key with GPT-4 access
- Python 3.13+ (already required from Phase II)
- Node.js 18+ (already required from Phase II)

---

## Step 1: OpenAI API Key Setup

### 1.1 Obtain API Key

1. Create account at https://platform.openai.com/
2. Navigate to API Keys section
3. Create new secret key (starts with `sk-`)
4. Copy key immediately (shown only once)

### 1.2 Configure Environment

**Backend** (`backend/.env`):
```bash
# Existing Phase II variables (do not change)
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=...
JWT_SECRET=...

# NEW: Phase III variables
OPENAI_API_KEY=sk-...  # Your OpenAI API key
OPENAI_MODEL_PRIMARY=gpt-4  # Primary model (can use gpt-4-turbo or gpt-4o)
OPENAI_MODEL_FALLBACK=gpt-3.5-turbo  # Fallback model
```

**Frontend** (`frontend/.env.local`):
```bash
# Existing Phase II variables (do not change)
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=...  # Same as backend

# NEW: Phase III variables (ChatKit configuration handled in code)
```

**⚠️ Security**: Never commit `.env` files to git. Ensure `.env` is in `.gitignore`.

---

## Step 2: Backend Setup

### 2.1 Install New Dependencies

```bash
cd backend

# Install OpenAI Agents SDK and MCP SDK
pip install openai>=1.60.0  # OpenAI Agents SDK
pip install mcp>=0.1.0      # Model Context Protocol SDK (Official)

# Verify installations
python -c "import openai; print(openai.__version__)"
python -c "import mcp; print(mcp.__version__)"
```

### 2.2 Database Migration

```bash
cd backend

# Generate migration for Conversation and Message tables
alembic revision --autogenerate -m "Add conversation and message tables"

# Review the generated migration in backend/alembic/versions/003_*.py
# Verify it includes:
# - CREATE TABLE conversation (id, user_id, is_active, created_at, updated_at)
# - CREATE TABLE message (id, conversation_id, user_id, role, content, created_at)
# - 6 indexes (3 on conversation, 3 on message)

# Apply migration
alembic upgrade head

# Verify tables created
python -c "
from sqlalchemy import create_engine, inspect
import os
engine = create_engine(os.getenv('DATABASE_URL'))
inspector = inspect(engine)
tables = inspector.get_table_names()
print('Tables:', tables)
assert 'conversation' in tables, 'conversation table missing'
assert 'message' in tables, 'message table missing'
print('✅ Migration successful')
"
```

### 2.3 Verify Backend Structure

Ensure new files exist (created during implementation):
```bash
# Models
ls -la backend/src/models/conversation.py
ls -la backend/src/models/message.py

# Services
ls -la backend/src/services/conversation_service.py
ls -la backend/src/services/message_service.py
ls -la backend/src/services/agent_service.py

# MCP Server
ls -la backend/src/mcp/tools.py
ls -la backend/src/mcp/server.py

# Routes
ls -la backend/src/routes/chat.py
```

### 2.4 Start Backend

```bash
cd backend

# Start FastAPI server with hot reload
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Expected output:
# INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
# INFO:     Application startup complete.
```

**Verify Backend Health**:
```bash
curl http://localhost:8000/health
# Expected: {"status": "healthy"}

curl http://localhost:8000/docs
# Expected: OpenAPI documentation page (open in browser)
```

---

## Step 3: Frontend Setup

### 3.1 Install New Dependencies

```bash
cd frontend

# Install OpenAI ChatKit
npm install @openai/chat-kit

# Verify installation
npm list @openai/chat-kit
```

### 3.2 Configure ChatKit

**File**: `frontend/lib/chatkit-config.ts`
```typescript
export const CHATKIT_CONFIG = {
  apiEndpoint: process.env.NEXT_PUBLIC_API_URL + '/api/{user_id}/chat',
  authTokenKey: 'auth_token',  // Better Auth JWT token key
  enableHistory: true,
  enableConversationSwitching: true,
  maxMessageLength: 4000,
};
```

### 3.3 Start Frontend

```bash
cd frontend

# Start Next.js development server
npm run dev

# Expected output:
# ▲ Next.js 16.x.x
# - Local:   http://localhost:3000
# ✓ Ready in XXXms
```

**Verify Frontend**:
- Open http://localhost:3000
- Login with existing Phase II credentials
- Navigate to `/chat` page
- Should see OpenAI ChatKit interface

---

## Step 4: Testing the Agent

### 4.1 Manual Testing Workflow

**Test 1: Natural Language Task Creation (P1 User Story)**
```
User: "I need to buy groceries"
Expected Agent Response: "✅ Added task: Buy groceries"

Verification:
- Check database: SELECT * FROM task WHERE title LIKE '%groceries%';
- Should see new task created with user_id matching authenticated user
```

**Test 2: Natural Language Task Queries (P2 User Story)**
```
User: "What tasks do I have?"
Expected Agent Response: "You have 1 pending task:
1. Buy groceries"

Verification:
- Agent should call list_tasks tool
- Should return formatted list (not raw JSON)
```

**Test 3: Multi-Step Planning (P3 User Story)**
```
User: "Mark the grocery task as done"
Expected Agent Response: "✅ Completed task: Buy groceries"

Verification:
- Agent should:
  1. Call list_tasks to find task matching "grocery"
  2. Call complete_task with found task_id
  3. Confirm completion
```

**Test 4: Context Awareness (P4 User Story)**
```
User: "Add task: Buy milk"
Agent: "✅ Added task: Buy milk"
User: "Actually, make it almond milk"
Expected Agent Response: "✅ Updated task: Buy almond milk"

Verification:
- Agent remembers last-created task from conversation history
- Calls update_task with correct task_id
```

### 4.2 Error Handling Tests

**Test 5: Ambiguous Intent**
```
User: "milk"
Expected Agent Response: "Did you want to:
1. Add a new task about milk?
2. Search for existing tasks containing 'milk'?
Please clarify."
```

**Test 6: Task Not Found**
```
User: "Complete the dentist task"
Expected Agent Response (if no matching task): "I couldn't find a task matching 'dentist'. Would you like me to create one?"
```

**Test 7: OpenAI API Failure**
```
# Simulate: Stop OpenAI API or use invalid key
User: "Add task: Test"
Expected Agent Response: "AI assistant temporarily unavailable. Please try again in a moment."
```

### 4.3 Automated Testing

```bash
# Run backend tests
cd backend
pytest tests/integration/test_chat_route.py -v
pytest tests/integration/test_mcp_tools.py -v
pytest tests/unit/test_agent_service.py -v

# Check coverage (target ≥80%)
pytest --cov=src --cov-report=term-missing
```

---

## Step 5: Conversation History

### 5.1 Verify Conversation Persistence

**Database Query**:
```sql
-- Check active conversation for user
SELECT id, user_id, is_active, created_at, updated_at
FROM conversation
WHERE user_id = 1 AND is_active = true;

-- Check messages in conversation
SELECT id, conversation_id, role, LEFT(content, 50) AS content_preview, created_at
FROM message
WHERE conversation_id = <conversation_id>
ORDER BY created_at ASC;
```

**Expected**:
- One active conversation per user
- Messages ordered chronologically
- User messages (role='user'), agent responses (role='assistant'), tool results (role='tool')

### 5.2 Test Conversation Switching

1. Have a conversation (5+ messages)
2. Click "New Conversation" in ChatKit UI
3. Previous conversation should be auto-archived (is_active=false)
4. New active conversation created
5. Verify previous conversation accessible in history sidebar

---

## Step 6: Monitoring & Observability

### 6.1 Check Logs

**Backend Logs** (structured JSON):
```bash
tail -f backend/logs/app.log | jq .
```

**Expected Log Entries**:
```json
{
  "timestamp": "2025-12-19T10:30:00Z",
  "level": "INFO",
  "user_id": 1,
  "conversation_id": 42,
  "intent": "create_task",
  "tool_called": "add_task",
  "latency_ms": 1250,
  "success": true
}
```

### 6.2 Metrics to Monitor

**Performance (SC-001)**:
- `p95_latency_ms` should be <2000 (2 seconds)
- Query Prometheus/logs: `quantile(0.95, agent_response_latency_ms)`

**Intent Accuracy (SC-002)**:
- `intent_accuracy_rate` should be ≥90%
- Calculation: `successful_tool_selections / total_requests * 100`

**Cost Tracking (SC-009)**:
- `avg_cost_per_conversation` should be <$0.10
- Track OpenAI API usage via OpenAI dashboard

**Error Recovery (SC-007)**:
- `error_recovery_rate` should be 100%
- No unhandled exceptions, all errors gracefully handled

---

## Step 7: Deployment

### 7.1 Production Environment Variables

**Backend** (Vercel/Railway/Render):
```bash
DATABASE_URL=postgresql://production-db-url
BETTER_AUTH_SECRET=production-secret
JWT_SECRET=production-jwt-secret
OPENAI_API_KEY=sk-production-key
OPENAI_MODEL_PRIMARY=gpt-4
OPENAI_MODEL_FALLBACK=gpt-3.5-turbo
ENVIRONMENT=production
```

**Frontend** (Vercel):
```bash
NEXT_PUBLIC_API_URL=https://api.yourapp.com
BETTER_AUTH_SECRET=production-secret  # Same as backend
```

### 7.2 OpenAI ChatKit Domain Allowlist

1. Go to https://platform.openai.com/settings/organization/domains
2. Add production domain: `https://app.yourapp.com`
3. Verify ChatKit loads without CORS errors

### 7.3 Database Migration (Production)

```bash
# On production server
cd backend
alembic upgrade head

# Verify migration
python -c "
from sqlalchemy import create_engine, inspect
import os
engine = create_engine(os.getenv('DATABASE_URL'))
inspector = inspect(engine)
tables = inspector.get_table_names()
assert 'conversation' in tables
assert 'message' in tables
print('✅ Production migration successful')
"
```

### 7.4 Health Checks

**Backend Health Check** (add to monitoring):
```bash
curl https://api.yourapp.com/health
# Expected: {"status": "healthy", "database": "connected", "openai": "available"}
```

**Frontend Health Check**:
- Visit https://app.yourapp.com/chat
- Verify ChatKit loads
- Send test message: "What tasks do I have?"
- Verify agent responds

---

## Step 8: Automated Cleanup Job (90-Day Retention)

### 8.1 Create Cleanup Script

**File**: `backend/scripts/cleanup_old_conversations.py`
```python
import asyncio
import os
from datetime import datetime, timedelta
from sqlalchemy import delete
from src.lib.database import async_engine, async_session_maker
from src.models.conversation import Conversation

async def cleanup_old_conversations():
    cutoff_date = datetime.utcnow() - timedelta(days=90)

    async with async_session_maker() as session:
        result = await session.execute(
            delete(Conversation).where(Conversation.created_at < cutoff_date)
        )
        await session.commit()
        deleted_count = result.rowcount

    print(f"Deleted {deleted_count} conversations older than 90 days")
    return deleted_count

if __name__ == "__main__":
    asyncio.run(cleanup_old_conversations())
```

### 8.2 Schedule Daily Job

**Kubernetes CronJob** (recommended):
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: cleanup-old-conversations
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM UTC
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: cleanup
            image: your-backend-image
            command: ["python", "scripts/cleanup_old_conversations.py"]
            env:
              - name: DATABASE_URL
                valueFrom:
                  secretKeyRef:
                    name: db-secret
                    key: url
          restartPolicy: OnFailure
```

**Or cron (Linux server)**:
```bash
# Edit crontab
crontab -e

# Add daily cleanup at 2 AM
0 2 * * * cd /path/to/backend && python scripts/cleanup_old_conversations.py >> logs/cleanup.log 2>&1
```

---

## Troubleshooting

### Issue: OpenAI API Rate Limit

**Symptom**: Agent returns "AI assistant temporarily unavailable"

**Solution**:
1. Check OpenAI dashboard for rate limits: https://platform.openai.com/usage
2. Verify fallback to GPT-3.5-turbo is working (check logs)
3. If consistently hitting limits, upgrade OpenAI plan or implement request queuing

### Issue: Conversation Not Found

**Symptom**: User gets "No active conversation found"

**Solution**:
```python
# Check if conversation exists
SELECT * FROM conversation WHERE user_id = <user_id> AND is_active = true;

# If missing, create one manually or restart chat session
```

### Issue: Agent Selecting Wrong Tool

**Symptom**: Agent calls `list_tasks` when user wanted to create a task

**Solution**:
1. Check tool descriptions in `contracts/*.json` are clear
2. Verify MCP server is passing correct tool schemas
3. Review agent service logs for intent classification
4. If accuracy <90%, consider improving tool descriptions or switching to GPT-4

### Issue: High Latency (p95 >2s)

**Symptom**: Agent responses slow

**Solution**:
1. Check OpenAI API latency: https://status.openai.com/
2. Verify database query performance (check indexes on conversation_id, user_id)
3. Reduce message history window from 50 to 30 messages
4. Enable connection pooling for database

---

## Success Criteria Validation

After setup, verify all success criteria:

- ✅ **SC-001**: Agent responds in <2s (p95) - Monitor latency logs
- ✅ **SC-002**: ≥90% intent accuracy - Track successful tool selections
- ✅ **SC-003**: Multi-step workflows work - Test "complete the grocery task"
- ✅ **SC-004**: Context maintained 10+ exchanges - Test "make it almond milk"
- ✅ **SC-005**: 100 concurrent conversations - Load testing with k6/Locust
- ✅ **SC-006**: Zero Phase II backend changes - Verify TaskService unchanged
- ✅ **SC-007**: 100% error recovery - Test API failures, invalid input
- ✅ **SC-008**: Cross-device access - Login from different browser
- ✅ **SC-009**: <$0.10/conversation - Track OpenAI API costs
- ✅ **SC-010**: 100% confirmation messages - Verify all state-changing operations

---

## Next Steps

After completing this quickstart:

1. **Review Logs**: Check `backend/logs/app.log` for observability data
2. **Run Full Test Suite**: `pytest backend/tests/ -v --cov`
3. **Performance Testing**: Use k6 or Locust to simulate 100 concurrent users
4. **User Acceptance Testing**: Have real users test natural language workflows
5. **Monitor Costs**: Track OpenAI API usage daily for first week
6. **Iterate**: Based on intent accuracy metrics, refine tool descriptions

**Ready for Production**: Once all success criteria validated, proceed to deployment.

---

## Additional Resources

- **OpenAI Agents SDK Docs**: https://platform.openai.com/docs/guides/agents
- **MCP Specification**: https://modelcontextprotocol.org/
- **OpenAI ChatKit Docs**: https://github.com/openai/chatkit
- **Phase III Spec**: [spec.md](./spec.md)
- **Phase III Plan**: [plan.md](./plan.md)
- **Data Model**: [data-model.md](./data-model.md)
- **Research Decisions**: [research.md](./research.md)
