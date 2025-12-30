# Implementation Plan: Phase III - Agentic AI Chatbot

**Branch**: `004-phase-iii-ai-chatbot` | **Date**: 2025-12-19 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-phase-iii-ai-chatbot/spec.md`

**Note**: This plan incorporates 100% Reusable Intelligence from Phase II (40+ components) per FR-007 and SC-006.

## Summary

Phase III transforms the Todo Evolution web application from traditional CRUD to an Agentic AI system using natural language interaction. Users will converse with an AI agent via OpenAI ChatKit instead of clicking buttons. The agent autonomously selects and chains MCP tools (add_task, list_tasks, complete_task, delete_task, update_task) to fulfill user intent, demonstrating true autonomy through multi-step planning, context awareness, and error recovery.

**Technical Approach**:
- **Frontend**: Replace Phase II UI with OpenAI ChatKit conversational interface
- **Agent Layer**: OpenAI Agents SDK orchestrates tool selection and multi-step workflows
- **MCP Server**: 5 tools wrap Phase II TaskService (100% backend reuse, zero code changes)
- **Conversation Persistence**: Database-backed conversation history enables stateless architecture
- **Model Strategy**: Primary GPT-4 with automatic GPT-3.5-turbo fallback (cost + reliability)

**Key Architectural Shift**: Automation → Autonomy (agent decides HOW, not just executes WHAT)

## Technical Context

**Language/Version**: Python 3.13+ (backend), TypeScript 5.x (frontend)
**Primary Dependencies**:
- **Backend**: FastAPI 0.115+, OpenAI Agents SDK (Python), MCP SDK (Official), SQLModel 0.0.22
- **Frontend**: Next.js 16+, React 19, OpenAI ChatKit, Better Auth
- **AI**: OpenAI API (GPT-4 primary, GPT-3.5-turbo fallback)

**Storage**: Neon PostgreSQL (existing tables + new Conversation/Message tables)
**Testing**: pytest (backend 83% coverage), Jest/Vitest (frontend TBD)
**Target Platform**: Web application (Linux backend server, modern browsers)
**Project Type**: Full-stack web (backend/ + frontend/ monorepo)
**Performance Goals**:
- p95 latency <2s for agent responses (SC-001)
- ≥90% intent recognition accuracy (SC-002)
- 100 concurrent conversations supported (SC-005)
- <$0.10 per conversation cost (SC-009)

**Constraints**:
- 100% Phase II backend reuse (FR-007, SC-006) - zero code changes
- Stateless backend architecture (FR-005) - conversation state in database
- 4000 char/message, 500 messages/conversation limits (FR-017)
- JWT authentication from Phase II (FR-010) - no auth changes

**Scale/Scope**:
- 5 MCP tools (fixed scope for Phase III)
- 4 prioritized user stories (P1-P4)
- 2 new database tables (Conversation, Message)
- 1 new API endpoint (POST /api/{user_id}/chat)
- Reuse: TaskService (6 functions), Auth Service (2 functions), Database layer, API middleware

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Verification |
|-----------|--------|--------------|
| **I. Spec-Driven Development** | ✅ PASS | spec.md created, clarified (5 questions), validated before planning |
| **II. User Data Isolation** | ✅ PASS | All MCP tools include `user_id` parameter, delegate to Phase II TaskService (already enforces isolation), JWT verification reused |
| **III. Stateless Architecture** | ✅ PASS | FR-005: Conversation state persists to database (Conversation/Message tables), MCP tools stateless, agent reconstructs context from DB |
| **IV. Smallest Viable Change** | ✅ PASS | Zero Phase II backend code changes (FR-007), only additions (MCP server, agent service, new models) |
| **V. Human-as-Tool Strategy** | ✅ PASS | 5 clarification questions asked during spec phase, plan presented for approval |
| **VIII. MCP Tool Design** | ✅ PASS | 5 tools defined with JSON schemas, `user_id` in all tools, stateless design, structured responses |
| **IX. Code Quality Standards** | ⚠️ PENDING | Will enforce: type hints, docstrings, async/await, black formatting (verified in testing phase) |
| **X. Testing Requirements** | ✅ PASS | Target ≥80% coverage (Phase II: 83%), integration tests for agent workflows, user isolation tests reused |
| **XII. Security Principles** | ✅ PASS | OPENAI_API_KEY in .env, JWT auth reused (no new secrets), input validation via Pydantic, MCP tools validate user_id |
| **XIV. Authentication & Authorization** | ✅ PASS | Better Auth + JWT reused (FR-010), chat endpoint requires Bearer token, no auth changes needed |
| **XV. API Rate Limiting** | ✅ PASS | Phase II slowapi rate limiting (100 req/min) applies to chat endpoint |
| **XVI. Error Handling & Logging** | ✅ PASS | FR-008: Graceful error handling, SC-007: 100% error recovery, FR-019: Comprehensive observability (logs, traces, metrics) |
| **XVIII. Performance Standards** | ✅ PASS | SC-001: p95 <2s latency target, async operations throughout, connection pooling reused from Phase II |
| **XXVI. Conversation Persistence** | ✅ PASS | FR-005/FR-006: Conversations + Messages in database, stateless chat endpoint, workflow documented |

**Overall Gate Status**: ✅ **PASS** - All critical principles satisfied

**Post-Design Re-Check**:
- After Phase 1 design completion, verify data-model.md includes proper indexes on `user_id`, `conversation_id`
- Verify contracts/ includes MCP tool JSON schemas with proper validation
- Verify observability requirements (FR-019) mapped to logging strategy

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

**Structure**: Web application (frontend + backend monorepo)

```text
backend/
├── src/
│   ├── models/
│   │   ├── user.py               # Phase II (REUSED)
│   │   ├── task.py               # Phase II (REUSED)
│   │   ├── conversation.py       # Phase III (NEW) - Conversation model
│   │   └── message.py            # Phase III (NEW) - Message model
│   ├── services/
│   │   ├── task_service.py       # Phase II (REUSED) - 6 CRUD functions
│   │   ├── auth_service.py       # Phase II (REUSED) - 5 auth functions
│   │   ├── conversation_service.py  # Phase III (NEW) - Conversation CRUD
│   │   ├── message_service.py    # Phase III (NEW) - Message CRUD
│   │   └── agent_service.py      # Phase III (NEW) - OpenAI Agents SDK integration
│   ├── mcp/
│   │   ├── __init__.py           # Phase III (NEW)
│   │   ├── tools.py              # Phase III (NEW) - 5 MCP tools
│   │   └── server.py             # Phase III (NEW) - MCP server setup
│   ├── routes/
│   │   ├── auth.py               # Phase II (REUSED) - 2 auth endpoints
│   │   ├── tasks.py              # Phase II (REUSED) - 6 task endpoints
│   │   └── chat.py               # Phase III (NEW) - POST /api/{user_id}/chat
│   ├── lib/
│   │   └── database.py           # Phase II (REUSED) - DB connection
│   ├── alembic/
│   │   ├── versions/
│   │   │   ├── 001_*.py          # Phase II (EXISTING)
│   │   │   ├── 002_*.py          # Phase II (EXISTING)
│   │   │   └── 003_add_conversation_message.py  # Phase III (NEW)
│   │   └── env.py                # Phase II (REUSED)
│   └── main.py                   # Phase II (MODIFIED) - Add chat route
└── tests/
    ├── conftest.py               # Phase II (REUSED) - Test fixtures
    ├── unit/
    │   ├── test_task_service.py  # Phase II (REUSED)
    │   ├── test_auth_service.py  # Phase II (REUSED)
    │   ├── test_conversation_service.py  # Phase III (NEW)
    │   ├── test_message_service.py  # Phase III (NEW)
    │   └── test_agent_service.py  # Phase III (NEW)
    ├── integration/
    │   ├── test_task_routes.py   # Phase II (REUSED)
    │   ├── test_auth_routes.py   # Phase II (REUSED)
    │   ├── test_chat_route.py    # Phase III (NEW)
    │   └── test_mcp_tools.py     # Phase III (NEW)
    └── contract/
        └── test_mcp_schemas.py   # Phase III (NEW) - Validate tool schemas

frontend/
├── app/
│   ├── (auth)/
│   │   ├── login/page.tsx        # Phase II (REUSED)
│   │   └── register/page.tsx     # Phase II (REUSED)
│   ├── tasks/
│   │   └── page.tsx              # Phase II (REMOVED) - Replaced by chat
│   ├── chat/
│   │   └── page.tsx              # Phase III (NEW) - OpenAI ChatKit integration
│   ├── layout.tsx                # Phase II (MODIFIED) - Update navigation
│   └── page.tsx                  # Phase II (REUSED) - Landing page
├── components/
│   ├── ui/                       # Phase II (REUSED) - Shadcn components
│   ├── ChatInterface.tsx         # Phase III (NEW) - ChatKit wrapper
│   ├── ConversationList.tsx      # Phase III (NEW) - History sidebar
│   └── ConversationSwitcher.tsx  # Phase III (NEW) - Switch conversations
├── lib/
│   ├── auth.ts                   # Phase II (REUSED) - Better Auth client
│   ├── api.ts                    # Phase II (MODIFIED) - Add chat endpoint
│   └── chatkit-config.ts         # Phase III (NEW) - ChatKit configuration
└── tests/
    └── (TBD)                     # Phase III - Frontend testing deferred
```

**Structure Decision**: Web application monorepo with backend (FastAPI + Python) and frontend (Next.js + TypeScript). Phase III adds 13 new backend files (models, services, MCP server, routes, tests) and 5 new frontend files (chat UI, conversation management), while reusing 15+ Phase II files unchanged. Key additions:

- **Backend New**: `conversation.py`, `message.py`, `agent_service.py`, `mcp/tools.py`, `mcp/server.py`, `chat.py` route, Alembic migration, 5 test files
- **Backend Reused**: TaskService (6 functions), AuthService (5 functions), database layer, all Phase II routes, test fixtures
- **Frontend New**: `app/chat/page.tsx` (ChatKit), `ChatInterface.tsx`, `ConversationList.tsx`, `ConversationSwitcher.tsx`, `chatkit-config.ts`
- **Frontend Reused**: Auth pages, layout, Better Auth integration, UI components

---

## Implementation Phases

**Phasing Strategy**: Backend-first approach with parallel frontend setup, followed by integration and production readiness.

### Phase 3.1: Database Foundation (Days 1-2)

**Goal**: Conversation/Message tables available for services

**Deliverables**:
- `backend/src/models/conversation.py` - Conversation SQLModel with relationships
- `backend/src/models/message.py` - Message SQLModel with relationships
- `backend/alembic/versions/003_add_conversation_message.py` - Migration script
- `backend/tests/unit/test_conversation_model.py` - Model validation tests
- `backend/tests/unit/test_message_model.py` - Model validation tests

**Success Gate**:
- ✅ `alembic upgrade head` succeeds without errors
- ✅ Tables created with 6 indexes (3 conversation, 3 message)
- ✅ Foreign key constraints validated (cascade deletes work)
- ✅ Unit tests pass (100% coverage on models)

**Dependencies**:
- Phase II database layer (connection pooling, async_session_maker)
- Neon PostgreSQL accessible

**Parallel Work**: Frontend ChatKit setup can begin (independent)

---

### Phase 3.2: Service Layer (Days 2-3)

**Goal**: CRUD operations for Conversation/Message entities

**Deliverables**:
- `backend/src/services/conversation_service.py` - 4 functions (create, get_active, list_user_conversations, archive)
- `backend/src/services/message_service.py` - 3 functions (create, get_conversation_messages, count_messages)
- `backend/tests/unit/test_conversation_service.py` - Service unit tests
- `backend/tests/unit/test_message_service.py` - Service unit tests

**Success Gate**:
- ✅ All CRUD operations pass unit tests
- ✅ Data access patterns from data-model.md implemented (Patterns 1-6)
- ✅ User data isolation enforced (user_id validation)
- ✅ Test coverage ≥80% on service layer

**Dependencies**:
- Phase 3.1 complete (Conversation/Message models exist)

**Parallel Work**: MCP tool contracts can be converted to stubs (independent)

---

### Phase 3.3: MCP Server (Days 3-5)

**Goal**: 5 MCP tools callable and contract-compliant

**Deliverables**:
- `backend/src/mcp/__init__.py` - Package initialization
- `backend/src/mcp/tools.py` - 5 MCP tools (add_task, list_tasks, complete_task, delete_task, update_task)
- `backend/src/mcp/server.py` - MCP server setup (tool registration)
- `backend/tests/contract/test_mcp_schemas.py` - JSON schema validation tests
- `backend/tests/integration/test_mcp_tools.py` - Tool integration tests

**Success Gate**:
- ✅ All 5 tools pass contract tests (JSON schemas validated)
- ✅ All 5 tools delegate to Phase II TaskService (100% reuse verified)
- ✅ Tools enforce user_id validation (Principle II: User Data Isolation)
- ✅ Tool responses include confirmation messages (SC-010)
- ✅ Agent notes in contracts guide multi-step planning (SC-003)

**Dependencies**:
- Phase II TaskService (6 CRUD functions)
- contracts/*.json schemas

**Parallel Work**: Agent service can be stubbed (tools can be mocked initially)

---

### Phase 3.4: Agent Service (Days 5-6)

**Goal**: OpenAI Agents SDK integrated, agent responds to user input

**Deliverables**:
- `backend/src/services/agent_service.py` - Agent orchestration (Agents SDK, context reconstruction, model fallback)
- `backend/tests/unit/test_agent_service.py` - Agent unit tests (mocked OpenAI API)
- `backend/tests/integration/test_agent_intent.py` - Intent recognition tests (real API)

**Success Gate**:
- ✅ Agent selects correct tool for P1 test case ("Add task: Buy milk" → add_task)
- ✅ Context reconstruction fetches last 50 messages from DB
- ✅ Model fallback logic works (GPT-4 → GPT-3.5 on rate limit)
- ✅ Intent recognition ≥90% accuracy on test dataset (SC-002)
- ✅ Multi-step planning works (list → complete for "Mark grocery task done") (SC-003)

**Dependencies**:
- Phase 3.2 complete (Message service for context reconstruction)
- Phase 3.3 complete (MCP tools registered)
- OPENAI_API_KEY configured

**Implementation Details** (per ADR-002, ADR-003):
- Fetch last 50 messages ordered by created_at DESC
- Try GPT-4 first, catch rate_limit_exceeded, retry with GPT-3.5
- Pass tools list to Agents SDK run() method

---

### Phase 3.5: Chat API Endpoint (Days 6-7)

**Goal**: POST /api/{user_id}/chat endpoint functional

**Deliverables**:
- `backend/src/routes/chat.py` - Chat endpoint (JWT auth, agent invocation, conversation persistence)
- `backend/src/main.py` - Add chat route registration
- `backend/tests/integration/test_chat_route.py` - API integration tests for P1-P4 user stories

**Success Gate**:
- ✅ Endpoint requires JWT authentication (Principle XIV)
- ✅ All P1-P4 acceptance scenarios pass via API tests:
  - P1: "Remember to buy milk" → task created
  - P2: "What tasks do I have?" → tasks listed
  - P3: "Mark grocery task done" → task completed
  - P4: "Actually, make it almond milk" → task updated
- ✅ Error handling graceful (SC-007: 100% error recovery)
- ✅ p95 latency <2s validated (SC-001)

**Dependencies**:
- Phase 3.4 complete (Agent service)
- Phase II auth middleware (JWT verification)

**Parallel Work**: Frontend ChatKit integration can begin (API endpoint ready)

---

### Phase 3.6: Frontend ChatKit (Days 7-9)

**Goal**: Users can interact via ChatKit UI, conversation switching works

**Deliverables**:
- `frontend/app/chat/page.tsx` - ChatKit integration page
- `frontend/components/ChatInterface.tsx` - ChatKit wrapper component
- `frontend/components/ConversationList.tsx` - History sidebar
- `frontend/components/ConversationSwitcher.tsx` - Switch conversations UI
- `frontend/lib/chatkit-config.ts` - ChatKit configuration
- `frontend/lib/api.ts` - Add chat endpoint method
- `frontend/app/layout.tsx` - Update navigation (Tasks → Chat)
- `frontend/tests/e2e/test_chat_flows.spec.ts` - E2E tests (Playwright)

**Success Gate**:
- ✅ User can complete P1 user story via UI (type "I need to buy groceries", see task created)
- ✅ Conversation history accessible (FR-016)
- ✅ Conversation switching works (create new conversation, view previous)
- ✅ ChatKit loads without CORS errors (domain allowlist configured)
- ✅ E2E tests pass for all 4 user stories

**Dependencies**:
- Phase 3.5 complete (Chat API endpoint)
- OpenAI ChatKit domain allowlist approved (external dependency)

**Frontend Testing Strategy** (deferred from plan.md):
- **Framework**: Playwright for E2E tests
- **Coverage**: P1-P4 user stories (4 test scenarios)
- **Environment**: Uses backend API in test mode (mocked OpenAI responses for deterministic tests)
- **Scope**: UI interaction only (backend thoroughly tested in Phase 3.5)

---

### Phase 3.7: Observability & Production Readiness (Days 9-10)

**Goal**: Comprehensive observability, automated cleanup, performance validation

**Deliverables**:
- `backend/src/lib/logging.py` - Structured JSON logging setup
- `backend/src/lib/metrics.py` - Metrics collection (latency, intent accuracy, cost)
- `backend/scripts/cleanup_old_conversations.py` - 90-day retention cleanup
- `backend/tests/integration/test_observability.py` - Logging/metrics validation
- `.github/workflows/cleanup-cron.yml` or K8s CronJob manifest

**Success Gate (FR-019 Observability)**:
- ✅ **Request/response logs**: JSON format with user_id, conversation_id, timestamp, user_input, agent_output
- ✅ **Tool call traces**: Log tool name, parameters, result, duration
- ✅ **Latency metrics**: p50, p95, p99 tracked per endpoint
- ✅ **Intent accuracy tracking**: Log successful/failed tool selections, calculate accuracy rate
- ✅ **Error rate monitoring**: Log all exceptions with stack traces
- ✅ **Cost tracking**: Log OpenAI API usage (model, input/output tokens, cost per conversation)

**Success Gate (All 10 Success Criteria)**:
- ✅ SC-001: p95 latency <2s (measured via metrics)
- ✅ SC-002: ≥90% intent accuracy (calculated from logs)
- ✅ SC-003: Multi-step workflows work (validated in Phase 3.5)
- ✅ SC-004: Context maintained 10+ exchanges (tested in E2E)
- ✅ SC-005: 100 concurrent conversations (load test with k6/Locust)
- ✅ SC-006: Zero Phase II backend changes (verified in code review)
- ✅ SC-007: 100% error recovery (all error paths tested)
- ✅ SC-008: Cross-device access (tested in E2E)
- ✅ SC-009: <$0.10/conversation (tracked via cost metrics)
- ✅ SC-010: 100% confirmations (validated in contract tests)

**Dependencies**:
- Phase 3.6 complete (full stack working)

**Observability Schema** (implementation details):

**Log Format** (JSON):
```json
{
  "timestamp": "2025-12-21T10:30:00.123Z",
  "level": "INFO",
  "logger": "agent_service",
  "user_id": 42,
  "conversation_id": 123,
  "message_id": 456,
  "event": "agent_response",
  "intent": "create_task",
  "tool_called": "add_task",
  "tool_parameters": {"user_id": 42, "title": "Buy milk"},
  "tool_result": {"success": true, "task_id": 789},
  "latency_ms": 1250,
  "model_used": "gpt-4",
  "tokens_input": 500,
  "tokens_output": 150,
  "cost_usd": 0.0082,
  "success": true,
  "error": null
}
```

**Metrics Schema** (Prometheus format):
```
# Latency histogram
agent_response_latency_seconds{endpoint="/api/{user_id}/chat", model="gpt-4"} 1.25

# Intent accuracy counter
agent_intent_accuracy_total{outcome="success"} 45
agent_intent_accuracy_total{outcome="failure"} 5

# Cost gauge
agent_cost_per_conversation_usd{model="gpt-4"} 0.08
agent_cost_per_conversation_usd{model="gpt-3.5-turbo"} 0.02

# Error rate counter
agent_errors_total{type="rate_limit", severity="warning"} 3
agent_errors_total{type="tool_failure", severity="error"} 1
```

**Metrics Storage**:
- Development: In-memory (Python `prometheus_client`)
- Production: Prometheus server (scraped every 15s)

**Dashboards**:
- Grafana dashboard with 6 panels:
  1. Agent response latency (p50, p95, p99)
  2. Intent accuracy rate (% successful tool selections)
  3. Cost per conversation ($ by model)
  4. Error rate (errors/min by type)
  5. Conversation volume (active conversations, messages/min)
  6. Model fallback rate (% GPT-4 vs GPT-3.5)

---

## Dependency Graph

### Critical Path (Sequential - 10 days)

```
Day 1-2:  Phase 3.1 (Database Foundation)
            ↓ BLOCKS Phase 3.2, 3.4
Day 2-3:  Phase 3.2 (Service Layer)
            ↓ BLOCKS Phase 3.4 (context reconstruction needs message_service)
Day 3-5:  Phase 3.3 (MCP Server)
            ↓ BLOCKS Phase 3.4 (agent needs tools registered)
Day 5-6:  Phase 3.4 (Agent Service)
            ↓ BLOCKS Phase 3.5 (chat route needs agent)
Day 6-7:  Phase 3.5 (Chat API)
            ↓ BLOCKS Phase 3.6 (frontend needs API endpoint)
Day 7-9:  Phase 3.6 (Frontend ChatKit)
            ↓ BLOCKS Phase 3.7 (E2E validation needed)
Day 9-10: Phase 3.7 (Observability)
            ↓ READY FOR DEPLOYMENT
```

### Parallel Work Opportunities (Saves ~3 days)

```
┌─────────────────────────────────────────────────────────┐
│ Day 1-2: Database Foundation                            │
│          ║                                               │
│          ║ PARALLEL: Frontend ChatKit Setup             │
│          ║ - Install @openai/chat-kit                   │
│          ║ - Create chatkit-config.ts (stub API)        │
│          ║ - Create ChatInterface.tsx (mock data)       │
│          ║ (Saves 1 day - frontend ready when API done) │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ Day 3-5: MCP Server                                     │
│          ║                                               │
│          ║ PARALLEL: Agent Service Stubs                │
│          ║ - Create agent_service.py skeleton           │
│          ║ - Mock OpenAI API for unit tests             │
│          ║ (Saves 1 day - integration faster)           │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ Day 9-10: Observability                                 │
│           ║                                              │
│           ║ PARALLEL: Cleanup Job                       │
│           ║ - Create cleanup_old_conversations.py       │
│           ║ - Setup CronJob manifest                    │
│           ║ (Saves 0.5 day - independent tasks)         │
└─────────────────────────────────────────────────────────┘

Total Time: 10 days sequential → 7 days with parallelization (30% faster)
```

### Blocking Dependencies

**External** (require approval/setup before starting):
- ✋ **OPENAI_API_KEY** - Must be provisioned before Phase 3.4 (Agent Service)
- ✋ **OpenAI ChatKit Domain Allowlist** - Must be approved before Phase 3.6 (Frontend)
- ✋ **Neon PostgreSQL Plan** - May need upgrade for 100 concurrent connections (SC-005)

**Internal** (must complete in order):
- 🔒 **Database Migration** → Services → MCP Tools → Agent → Chat Route → Frontend
- 🔒 **Phase II TaskService** → MCP Tools (zero changes, but must be functional)
- 🔒 **Phase II Auth Middleware** → Chat Route (JWT validation reused)

---

## Edge Case Handling Logic

**Implementation Strategy** (addresses edge cases from spec.md:88-98):

### Edge Case 1: Ambiguous User Intent

**Scenario**: User types "milk" (unclear if task creation or search)

**Detection Logic**:
```python
# In agent_service.py
def is_intent_ambiguous(user_input: str, tool_confidences: dict) -> bool:
    """
    Determine if user intent is ambiguous based on:
    1. Input length < 5 words
    2. Top 2 tool confidences within 10% (e.g., add_task=0.55, list_tasks=0.52)
    3. No clear action verb (add, create, show, list, complete, delete, update)
    """
    if len(user_input.split()) < 5:
        top_tools = sorted(tool_confidences.items(), key=lambda x: x[1], reverse=True)[:2]
        if len(top_tools) >= 2 and abs(top_tools[0][1] - top_tools[1][1]) < 0.10:
            return True
    return False

# Agent response template
if is_intent_ambiguous(user_input, confidences):
    return {
        "role": "assistant",
        "content": "I'm not sure what you'd like to do with 'milk'. Did you want to:\n1. Add a new task about milk?\n2. Search for existing tasks containing 'milk'?\n\nPlease clarify."
    }
```

**Validation**: Track ambiguous intent rate in FR-019 metrics (should be <5% of requests)

---

### Edge Case 2: Agent Can't Determine Intent

**Scenario**: User input completely unclear (e.g., "asdfgh", "??")

**Detection Logic**:
```python
def is_intent_determinable(user_input: str, tool_confidences: dict) -> bool:
    """
    Determine if ANY tool is suitable:
    1. All tool confidences < 30% (no clear match)
    2. Input is gibberish (no dictionary words detected via spaCy)
    """
    max_confidence = max(tool_confidences.values())
    if max_confidence < 0.30:
        return False
    return True

# Agent response template
if not is_intent_determinable(user_input, confidences):
    return {
        "role": "assistant",
        "content": "I didn't understand that. I can help you:\n- Add tasks (e.g., 'Buy groceries')\n- List tasks (e.g., 'What's on my list?')\n- Complete tasks (e.g., 'Mark grocery task done')\n- Update tasks (e.g., 'Change deadline to Friday')\n- Delete tasks (e.g., 'Remove dentist task')\n\nHow can I help?"
    }
```

---

### Edge Case 3: Multiple Tasks Match Query

**Scenario**: User says "complete the report task" but has 3 tasks with "report" in title

**Detection Logic** (in MCP tool wrapper):
```python
# In mcp/tools.py - complete_task tool
async def complete_task(user_id: int, task_id: int = None, search_term: str = None):
    """
    If task_id not provided, search by search_term and handle multi-match.
    """
    if task_id is None and search_term:
        matching_tasks = await task_service.search_tasks(user_id, search_term)

        if len(matching_tasks) == 0:
            return {
                "success": False,
                "message": f"I couldn't find a task matching '{search_term}'. Would you like me to create one?"
            }

        if len(matching_tasks) > 1:
            task_list = "\n".join([f"{i+1}. {task.title}" for i, task in enumerate(matching_tasks)])
            return {
                "success": False,
                "message": f"I found {len(matching_tasks)} tasks matching '{search_term}':\n{task_list}\n\nPlease specify which one (e.g., 'complete task 1')."
            }

        # Exactly 1 match - proceed
        task_id = matching_tasks[0].id

    # Rest of completion logic...
```

**Agent Guidance**: MCP contract agent_notes instruct to chain list_tasks first if no task_id

---

### Edge Case 4: OpenAI API Down/Rate-Limited

**Detection & Recovery** (per ADR-003):
```python
# In agent_service.py
async def invoke_agent(user_input: str, conversation_history: list) -> dict:
    try:
        # Try GPT-4 first
        response = await openai.agents.run(
            model="gpt-4",
            messages=conversation_history + [{"role": "user", "content": user_input}],
            tools=mcp_tools
        )
        return response

    except openai.error.RateLimitError as e:
        logger.warning(f"GPT-4 rate limited, falling back to GPT-3.5: {e}")
        metrics.increment("agent_model_fallback", tags={"from": "gpt-4", "to": "gpt-3.5"})

        # Retry with GPT-3.5-turbo
        response = await openai.agents.run(
            model="gpt-3.5-turbo",
            messages=conversation_history + [{"role": "user", "content": user_input}],
            tools=mcp_tools
        )
        return response

    except (openai.error.APIError, openai.error.Timeout) as e:
        logger.error(f"OpenAI API unavailable: {e}")
        return {
            "role": "assistant",
            "content": "AI assistant temporarily unavailable. Please try again in a moment.",
            "error": True
        }
```

**Validation**: SC-007 (100% error recovery) - all API errors must return user-friendly message

---

### Edge Case 5: Long Conversations (100+ messages)

**Strategy** (per ADR-002):
```python
# In agent_service.py - context reconstruction
async def get_conversation_context(conversation_id: int, limit: int = 50) -> list:
    """
    Fetch last N messages. If conversation has 100+ messages, summarize older context.
    """
    messages = await message_service.get_conversation_messages(conversation_id, limit=limit)

    # Edge case: Conversation has >100 messages (rare with 500 limit + auto-archive)
    total_count = await message_service.count_messages(conversation_id)
    if total_count > 100:
        logger.info(f"Long conversation detected: {total_count} messages, fetching last {limit}")
        metrics.increment("long_conversation", tags={"message_count": total_count})
        # Phase III: Simple truncation (fetch last 50)
        # Phase V: Implement summarization of messages 50-100

    return messages
```

**Monitoring**: Track conversations exceeding 50 messages via FR-019 metrics

---

### Edge Case 6: User Switches Devices Mid-Conversation

**Handled by Design** (no special logic needed):
- Conversation/Message tables persist to Neon PostgreSQL (cross-device accessible)
- JWT token stored in browser (user re-authenticates on new device)
- Active conversation retrieved via `get_active_conversation(user_id)` query

**Validation**: SC-008 - test in E2E by logging in from different browser

---

### Edge Case 7: MCP Tool Call Fails

**Error Handling** (in agent_service.py):
```python
async def execute_tool_call(tool_name: str, parameters: dict) -> dict:
    try:
        tool_func = mcp_tools[tool_name]
        result = await tool_func(**parameters)
        return result

    except ValidationError as e:
        logger.error(f"Tool validation error: {tool_name} - {e}")
        return {
            "success": False,
            "error": "validation",
            "message": "Invalid input. Please check your request and try again."
        }

    except DatabaseError as e:
        logger.error(f"Database error in tool {tool_name}: {e}")
        return {
            "success": False,
            "error": "database",
            "message": "I couldn't save that right now. Please try again in a moment."
        }

    except Exception as e:
        logger.error(f"Unexpected error in tool {tool_name}: {e}", exc_info=True)
        return {
            "success": False,
            "error": "unknown",
            "message": "Something went wrong. Our team has been notified."
        }
```

**Agent Integration**: Agent receives error result and communicates to user in natural language

---

### Edge Case 8: Message Exceeds 4000 Characters

**Validation** (Pydantic model + API middleware):
```python
# In routes/chat.py
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)

@router.post("/api/{user_id}/chat")
async def chat_endpoint(user_id: int, request: ChatRequest):
    # Pydantic automatically validates max_length
    # If exceeded, raises ValidationError with 422 status code

    try:
        response = await agent_service.invoke_agent(request.message, ...)
        return response
    except ValidationError as e:
        return JSONResponse(
            status_code=422,
            content={"error": "Message too long. Please keep messages under 4000 characters."}
        )
```

**Frontend**: ChatKit configured with `maxMessageLength: 4000` (client-side validation)

---

### Edge Case 9: Conversation Reaches 500 Message Limit

**Auto-Archive Trigger** (in message_service.py):
```python
async def create_message(conversation_id: int, user_id: int, role: str, content: str):
    # Check message count before creating new message
    message_count = await count_messages(conversation_id)

    if message_count >= 500:
        logger.info(f"Conversation {conversation_id} reached 500 message limit, auto-archiving")

        # Archive current conversation
        await conversation_service.archive_conversation(conversation_id)

        # Create new active conversation
        new_conversation = await conversation_service.create_conversation(user_id)

        # Return system message informing user
        return {
            "role": "assistant",
            "content": "Previous conversation archived (500 message limit). Starting fresh conversation.",
            "conversation_id": new_conversation.id,
            "archived": True
        }

    # Normal message creation
    message = Message(conversation_id=conversation_id, user_id=user_id, role=role, content=content)
    # ... save to DB
```

**User Experience**: Seamless transition, conversation history accessible via ConversationList sidebar

---

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected. All constitutional principles satisfied.

---

## Design Artifacts

**Phase 0 - Research** (Complete):
- [research.md](./research.md) - 9 architectural decisions, alternatives evaluated, risk mitigation strategies, technology stack justification

**Phase 1 - Design** (Complete):
- [data-model.md](./data-model.md) - Conversation/Message schemas, indexes, query patterns, Alembic migration
- [contracts/](./contracts/) - MCP tool JSON schemas (5 tools)
- [quickstart.md](./quickstart.md) - Phase III setup and deployment guide

**Phase 2 - Tasks** (Pending):
- tasks.md - Generated via `/sp.tasks` command (not part of `/sp.plan`)

---

## Plan Status

**Constitution Check**: ✅ PASS (14/14 principles verified)
**Phase 0 Research**: ✅ COMPLETE (research.md created)
**Phase 1 Design**: ✅ COMPLETE (data-model.md, contracts/, quickstart.md created)
**Project Structure**: ✅ COMPLETE (18 new files, 15+ reused files documented)
**Reusable Intelligence**: ✅ CATALOGED (40+ Phase II components identified for 100% reuse)

**Overall Plan Status**: ✅ **READY FOR TASK GENERATION** (`/sp.tasks`)
