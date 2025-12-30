---

description: "Task list for Phase III - Agentic AI Chatbot implementation"
---

# Tasks: Phase III - Agentic AI Chatbot

**Input**: Design documents from `/specs/004-phase-iii-ai-chatbot/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/, research.md

**Tests**: Tests are NOT explicitly requested in spec.md, so test tasks are included as optional parallel work but not blocking implementation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Web app monorepo**: `backend/src/`, `frontend/app/`, `frontend/components/`
- All paths are relative to repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and environment setup

- [X] T001 Install Python dependencies (openai, mcp SDK) in backend/requirements.txt
- [X] T002 [P] Install frontend dependencies (@openai/chatkit-react v1.4.0) in frontend/package.json
- [X] T003 [P] Add OPENAI_API_KEY to backend/.env and update backend/.env.example
- [X] T004 [P] Configure OpenAI ChatKit domain allowlist in OpenAI dashboard (external dependency - see note below)

**Checkpoint**: Environment ready - dependencies installed, API keys configured

**Validation Commands**:
```bash
# Verify Python dependencies installed
pip list | grep openai  # Should show openai>=1.0.0

# Verify frontend dependencies installed
cd frontend && npm list | grep chatkit-react  # Should show @openai/chatkit-react@^1.4.0

# Verify API key configured
test -f backend/.env && grep OPENAI_API_KEY backend/.env  # Should show key

# Test OpenAI import works
python -c "import openai; print('OpenAI SDK ready')"
```

**T004 Note - ChatKit Domain Allowlist**:
- **Development**: ChatKit works on `localhost:3000` without domain configuration
- **Production**: Before deploying, configure domain allowlist:
  1. Go to https://platform.openai.com/settings/organization/domains
  2. Add your production domain (e.g., `https://app.yourapp.com`)
  3. Verify ChatKit loads without CORS errors
- **Status**: Deferred to production deployment (not blocking development)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database Foundation (Blocks all stories - conversation persistence needed)

- [ ] T005 Create Conversation model in backend/src/models/conversation.py with SQLModel schema per data-model.md
- [ ] T006 [P] Create Message model in backend/src/models/message.py with SQLModel schema per data-model.md
- [ ] T007 Create Alembic migration 003_add_conversation_message.py with indexes per data-model.md
- [ ] T008 Run alembic upgrade head and verify tables created with foreign keys and indexes
- [ ] T009 Update User model in backend/src/models/user.py to add conversations and messages relationships

### Service Layer & MCP Tools (Parallel after T009) ⚡ OPTIMIZED

**Note**: Service layer and MCP tools can run in parallel - MCP tools only need Phase II TaskService, NOT ConversationService/MessageService

#### Service Layer (Blocks agent service - context reconstruction needed)

- [ ] T010a [P] Implement ConversationService.create_conversation() in backend/src/services/conversation_service.py
- [ ] T010b [P] Implement ConversationService.get_active_conversation() in backend/src/services/conversation_service.py
- [ ] T010c [P] Implement ConversationService.list_user_conversations() in backend/src/services/conversation_service.py
- [ ] T010d [P] Implement ConversationService.archive_conversation() in backend/src/services/conversation_service.py
- [ ] T011a [P] Implement MessageService.create_message() in backend/src/services/message_service.py
- [ ] T011b [P] Implement MessageService.get_conversation_messages() in backend/src/services/message_service.py
- [ ] T011c [P] Implement MessageService.count_messages() in backend/src/services/message_service.py

#### MCP Tools (Parallel with Service Layer - independent of T010-T011) ⚡

- [ ] T012 [P] Create MCP package initialization in backend/src/mcp/__init__.py
- [ ] T013 [P] Implement add_task MCP tool in backend/src/mcp/tools.py per contracts/add_task.json
- [ ] T014 [P] Implement list_tasks MCP tool in backend/src/mcp/tools.py per contracts/list_tasks.json
- [ ] T015 [P] Implement complete_task MCP tool in backend/src/mcp/tools.py per contracts/complete_task.json
- [ ] T016 [P] Implement delete_task MCP tool in backend/src/mcp/tools.py per contracts/delete_task.json
- [ ] T017 [P] Implement update_task MCP tool in backend/src/mcp/tools.py per contracts/update_task.json
- [ ] T018 Create MCP server setup in backend/src/mcp/server.py to register all 5 tools (depends on T013-T017)

### Agent Service Foundation (Blocks chat endpoint - agent orchestration needed)

**Dependencies**: Requires T011b (get_conversation_messages for context) and T018 (MCP server for tools)

- [ ] T019 Create AgentService skeleton in backend/src/services/agent_service.py with OpenAI Agents SDK imports and basic structure
- [ ] T020 Implement context reconstruction logic (fetch last 50 messages) in AgentService.get_context() per ADR-002
- [ ] T021 Implement agent invocation with tool registration in AgentService.invoke_agent()
- [ ] T022 Implement model fallback logic (GPT-4 → GPT-3.5-turbo) in AgentService.invoke_agent() per ADR-003
- [ ] T023 Implement ambiguous intent detection in AgentService.invoke_agent() (Edge Case 1 from plan.md)
- [ ] T024 Implement intent determination logic in AgentService.invoke_agent() (Edge Case 2 from plan.md)

**Checkpoint**: Foundation ready - database schema, services, MCP tools, and agent orchestration all functional

**Validation Commands**:
```bash
# Verify database migration applied
alembic current  # Should show revision 003_add_conversation_message

# Verify tables exist with correct schema
psql $DATABASE_URL -c "\d conversation"  # Should show columns: id, user_id, is_active, created_at, updated_at
psql $DATABASE_URL -c "\d message"  # Should show columns: id, conversation_id, user_id, role, content, created_at

# Verify indexes created
psql $DATABASE_URL -c "\di" | grep conversation  # Should show 3 indexes
psql $DATABASE_URL -c "\di" | grep message  # Should show 3 indexes

# Test ConversationService imports
python -c "from backend.src.services.conversation_service import ConversationService; print('ConversationService ready')"

# Test MessageService imports
python -c "from backend.src.services.message_service import MessageService; print('MessageService ready')"

# Test MCP tools import
python -c "from backend.src.mcp.tools import add_task, list_tasks, complete_task, delete_task, update_task; print('All 5 MCP tools ready')"

# Test AgentService imports
python -c "from backend.src.services.agent_service import AgentService; print('AgentService ready')"

# Integration test: Create conversation and message
python -c "
from backend.src.services.conversation_service import ConversationService
from backend.src.services.message_service import MessageService
# Test create conversation, add message, fetch messages (basic CRUD)
"
```

---

## Phase 3: User Story 1 - Natural Language Task Creation (Priority: P1) 🎯 MVP

**Goal**: Users can create tasks via natural language conversation ("Remember to buy milk tomorrow" → task created with confirmation)

**Independent Test**: User can open chat interface, type "I need to buy groceries", and see task created with confirmation message

**Dependencies**: Requires Phase 2 complete (T005-T024) - Foundation must be ready

### Chat API Endpoint for User Story 1

- [ ] T025 [US1] Create ChatRouter in backend/src/routes/chat.py with POST /api/{user_id}/chat endpoint
- [ ] T026 [US1] Implement JWT authentication middleware for chat endpoint (reuse Phase II auth)
- [ ] T027 [US1] Implement request validation (4000 char limit) using Pydantic in ChatRouter
- [ ] T028 [US1] Implement conversation lifecycle logic (find or create active conversation) in chat endpoint
- [ ] T029 [US1] Implement agent invocation with user message in chat endpoint
- [ ] T030 [US1] Implement message persistence (user + assistant messages) in chat endpoint
- [ ] T031 [US1] Implement error handling for tool failures and API errors in chat endpoint (Edge Cases 4, 7, 8)
- [ ] T032 [US1] Register chat route in backend/src/main.py

### Frontend ChatKit Integration for User Story 1

**Note**: Frontend can run in parallel with backend endpoint development (T025-T032) using mocked responses

- [ ] T033 [P] [US1] Create ChatKit configuration in frontend/lib/chatkit-config.ts
- [ ] T034 [P] [US1] Create chat API method in frontend/lib/api.ts for POST /api/{user_id}/chat
- [ ] T035 [US1] Create ChatInterface component in frontend/components/ChatInterface.tsx wrapping OpenAI ChatKit
- [ ] T036 [US1] Create chat page in frontend/app/chat/page.tsx integrating ChatInterface component
- [ ] T037 [US1] Update navigation in frontend/app/layout.tsx (Tasks → Chat)

### Optional Tests for User Story 1

- [ ] T038 [P] [US1] Write contract test for add_task MCP tool in backend/tests/contract/test_mcp_schemas.py
- [ ] T039 [P] [US1] Write integration test for chat endpoint task creation in backend/tests/integration/test_chat_route.py
- [ ] T040 [P] [US1] Write unit test for AgentService in backend/tests/unit/test_agent_service.py (mocked OpenAI API)

**Checkpoint**: User Story 1 complete - users can create tasks via natural language with confirmation

**Validation Commands**:
```bash
# Verify backend endpoint exists and responds
curl -X POST http://localhost:8000/api/1/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"message":"Add task: Buy milk"}' \
  # Should return 200 with agent response

# Verify frontend loads
curl http://localhost:3000/chat  # Should return 200 with ChatKit UI

# Manual test: Complete user story acceptance scenario
# 1. Open http://localhost:3000/chat in browser
# 2. Type: "I need to buy groceries"
# 3. Expected: Agent creates task and responds "Added task: Buy groceries"
# 4. Verify task created: Check Phase II task list or database

# Check conversation persisted
psql $DATABASE_URL -c "SELECT COUNT(*) FROM conversation WHERE user_id=1;"  # Should be >= 1
psql $DATABASE_URL -c "SELECT COUNT(*) FROM message WHERE user_id=1;"  # Should be >= 2 (user + assistant)
```

---

## Phase 4: User Story 2 - Natural Language Task Queries (Priority: P2)

**Goal**: Users can ask about tasks in natural language ("What tasks do I have?" → formatted task list)

**Independent Test**: User can type "What do I need to do today?" and receive formatted list of pending tasks

**Dependencies**: Requires US1 complete (T025-T040) for chat endpoint foundation

### Implementation for User Story 2

- [ ] T041 [US2] Implement task query formatting logic in AgentService (convert JSON array to conversational format)
- [ ] T042 [US2] Implement status filter handling in list_tasks tool (all/pending/completed)
- [ ] T043 [US2] Implement empty task list response in AgentService (Edge Case: no tasks)
- [ ] T044 [US2] Update ChatInterface to handle long task lists (pagination or scrolling) in frontend/components/ChatInterface.tsx

### Optional Tests for User Story 2

- [ ] T045 [P] [US2] Write contract test for list_tasks MCP tool in backend/tests/contract/test_mcp_schemas.py
- [ ] T046 [P] [US2] Write integration test for task query scenarios in backend/tests/integration/test_chat_route.py

**Checkpoint**: User Story 2 complete - users can query tasks and see formatted lists

**Validation Commands**:
```bash
# Manual test: Query tasks scenario
# 1. Open http://localhost:3000/chat
# 2. Type: "What tasks do I have?"
# 3. Expected: Agent lists all tasks in conversational format
# 4. Type: "Show me only pending tasks"
# 5. Expected: Agent filters and shows only incomplete tasks
```

---

## Phase 5: User Story 3 - Natural Language Task Management (Priority: P3)

**Goal**: Users can complete/delete/update tasks via conversation with multi-step planning ("Mark grocery task done" → agent finds task → marks complete)

**Independent Test**: User can type "Complete the milk task" and agent finds matching task and marks it complete

**Dependencies**: Requires US1 + US2 complete (multi-step chaining builds on query + action)

### Implementation for User Story 3

- [ ] T047 [US3] Implement multi-task match handling in complete_task tool (Edge Case 3 from plan.md)
- [ ] T048 [P] [US3] Implement multi-task match handling in delete_task tool (Edge Case 3 from plan.md)
- [ ] T049 [P] [US3] Implement multi-task match handling in update_task tool (Edge Case 3 from plan.md)
- [ ] T050 [US3] Implement task not found handling with offer to create (Edge Case 3 from plan.md)
- [ ] T051 [US3] Enhance AgentService to support multi-step tool chaining (list → complete, list → delete, list → update)

### Optional Tests for User Story 3

- [ ] T052 [P] [US3] Write contract test for complete_task MCP tool in backend/tests/contract/test_mcp_schemas.py
- [ ] T053 [P] [US3] Write contract test for delete_task MCP tool in backend/tests/contract/test_mcp_schemas.py
- [ ] T054 [P] [US3] Write contract test for update_task MCP tool in backend/tests/contract/test_mcp_schemas.py
- [ ] T055 [P] [US3] Write integration test for multi-step workflows in backend/tests/integration/test_chat_route.py

**Checkpoint**: User Story 3 complete - users can manage tasks with multi-step agent workflows

**Validation Commands**:
```bash
# Manual test: Multi-step task management
# 1. Create test task: "Add task: Buy groceries"
# 2. Type: "Complete the grocery task"
# 3. Expected: Agent lists matching tasks, selects correct one, marks complete
# 4. Type: "Delete my grocery task"
# 5. Expected: Agent finds completed task and deletes it
```

---

## Phase 6: User Story 4 - Conversation Context Awareness (Priority: P4)

**Goal**: Users can reference previous messages using pronouns ("Actually, make it almond milk" → agent updates last-created task)

**Independent Test**: User creates task, then says "change it to [new title]" and agent successfully updates the last-created task

**Dependencies**: Requires US1-US3 complete (context builds on all prior interactions)

### Implementation for User Story 4

- [ ] T056 [US4] Implement pronoun resolution logic in AgentService (track last task created/listed/completed)
- [ ] T057 [US4] Enhance context reconstruction to include recent tool call results in message history
- [ ] T058 [US4] Implement long conversation handling (>50 messages) with truncation in AgentService (Edge Case 5)
- [ ] T059 [US4] Implement cross-device conversation access (verify JWT token works across devices) - validation only

### Conversation History UI for User Story 4

- [ ] T060 [P] [US4] Create ConversationList component in frontend/components/ConversationList.tsx (history sidebar)
- [ ] T061 [P] [US4] Create ConversationSwitcher component in frontend/components/ConversationSwitcher.tsx (switch active conversation)
- [ ] T062 [US4] Integrate ConversationList and ConversationSwitcher into chat page frontend/app/chat/page.tsx
- [ ] T063 [US4] Implement conversation list API endpoint GET /api/{user_id}/conversations in backend/src/routes/chat.py

### Auto-Archive for User Story 4

- [ ] T064 [US4] Implement 500-message auto-archive trigger in MessageService (Edge Case 9 from plan.md)
- [ ] T065 [US4] Test auto-archive functionality (create conversation with 500 messages and verify archival)

### Optional Tests for User Story 4

- [ ] T066 [P] [US4] Write integration test for pronoun resolution in backend/tests/integration/test_chat_route.py
- [ ] T067 [P] [US4] Write integration test for conversation history retrieval in backend/tests/integration/test_chat_route.py
- [ ] T068 [P] [US4] Write E2E test for cross-device access using Playwright in frontend/tests/e2e/test_chat_flows.spec.ts

**Checkpoint**: User Story 4 complete - users can converse naturally with context awareness and conversation history

**Validation Commands**:
```bash
# Manual test: Context awareness
# 1. Type: "Add task: Buy milk"
# 2. Expected: Task created
# 3. Type: "Actually, make it almond milk"
# 4. Expected: Agent updates the last-created task to "Buy almond milk"
# 5. Verify conversation history sidebar shows previous exchanges
```

---

## Phase 7: Observability & Production Readiness (Cross-Cutting)

**Purpose**: Comprehensive observability, automated cleanup, performance validation

**Note**: This phase can run in PARALLEL with User Story implementation (independent infrastructure)

### Observability Implementation (FR-019)

- [ ] T069 [P] Create structured logging setup in backend/src/lib/logging.py (JSON format per plan.md)
- [ ] T070 [P] Create metrics collection in backend/src/lib/metrics.py (latency, intent accuracy, cost tracking per plan.md)
- [ ] T071 Integrate logging into AgentService (request/response logs, tool call traces)
- [ ] T072 Integrate metrics into chat endpoint (latency tracking, error rates)
- [ ] T073 Implement cost tracking in AgentService (OpenAI token usage per conversation)

### Data Retention & Cleanup (FR-020)

- [ ] T074 Create cleanup script in backend/scripts/cleanup_old_conversations.py (90-day retention per plan.md)
- [ ] T075 Test cleanup script manually (create old test conversations and verify deletion)
- [ ] T076 Create CronJob manifest in .github/workflows/cleanup-cron.yml or K8s manifest for daily execution

### Performance Validation (Success Criteria)

- [ ] T077 Validate SC-001 (p95 latency <2s) using metrics from observability
- [ ] T078 [P] Validate SC-002 (≥90% intent accuracy) by analyzing intent accuracy logs
- [ ] T079 [P] Validate SC-005 (100 concurrent conversations) using load test with k6 or Locust
- [ ] T080 [P] Validate SC-009 (<$0.10/conversation) by analyzing cost metrics
- [ ] T081 Validate SC-010 (100% confirmations) by reviewing MCP tool contract tests

### Optional Integration Tests for Observability

- [ ] T082 [P] Write test for logging validation in backend/tests/integration/test_observability.py
- [ ] T083 [P] Write test for metrics collection in backend/tests/integration/test_observability.py

**Checkpoint**: Production ready - observability, cleanup, and performance validated

**Validation Commands**:
```bash
# Verify observability infrastructure
python -c "from backend.src.lib.logging import setup_logging; print('Logging ready')"
python -c "from backend.src.lib.metrics import MetricsCollector; print('Metrics ready')"

# Test cleanup script
python backend/scripts/cleanup_old_conversations.py --dry-run  # Should show conversations to delete

# Load test (example with k6)
k6 run load-tests/chat-endpoint.js  # Should handle 100 concurrent users

# Check logs and metrics
tail -f backend/logs/agent.log | grep -i "agent_response"  # Should see JSON logs
curl http://localhost:8000/metrics  # Should return Prometheus metrics
```

---

## Phase 8: Polish & Final Validation

**Purpose**: Documentation, cleanup, and final validation

- [ ] T084 [P] Update quickstart.md with Phase III setup instructions (ChatKit, OPENAI_API_KEY, conversation UI)
- [ ] T085 [P] Create or update ADR for MCP server co-location decision (per plan.md)
- [ ] T086 [P] Create or update ADR for agent context reconstruction (per plan.md ADR-002)
- [ ] T087 [P] Create or update ADR for model fallback strategy (per plan.md ADR-003)
- [ ] T088 Code cleanup and formatting (black, isort) across backend/src/
- [ ] T089 Security review (ensure OPENAI_API_KEY not in git, JWT validation in chat endpoint)
- [ ] T090 Run full test suite (pytest backend/tests/) and verify ≥80% coverage
- [ ] T091 Validate all 4 user story acceptance scenarios manually via ChatKit UI

**Checkpoint**: Phase III complete - ready for deployment

**Validation Commands**:
```bash
# Run formatter
black backend/src/ && isort backend/src/

# Security audit
git grep -i "sk-" backend/  # Should return NO matches (no hardcoded API keys)
python -c "import os; assert 'OPENAI_API_KEY' in os.environ"  # Verify key in env only

# Test coverage
pytest backend/tests/ --cov=backend/src --cov-report=term-missing  # Should show ≥80%

# Manual validation: Run all 4 user story scenarios
# US1: "Add task: Buy milk" → task created
# US2: "What tasks do I have?" → tasks listed
# US3: "Complete the milk task" → task marked complete
# US4: "Actually, change it to almond milk" → task updated with context
```

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - **BLOCKS all user stories**
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Observability (Phase 7)**: Can start in parallel with user stories (independent logging/metrics infrastructure)
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - **No dependencies on other stories** - 🎯 MVP
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independently testable (just queries, no task creation needed)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May use US1 (create) + US2 (list) for multi-step workflows but independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Builds on US1-US3 context but conversation history independently testable

### Within Each User Story

- **US1**: Chat endpoint → Frontend integration (sequential, endpoint must exist before UI calls it)
- **US2**: Task query formatting → ChatInterface updates (can be parallel if using mocked data)
- **US3**: Multi-task handling → Multi-step chaining (sequential, logic builds on each other)
- **US4**: Pronoun resolution → Conversation UI → Auto-archive (mostly sequential for pronoun logic)

### Parallel Opportunities

#### Phase 1 (Setup)
- T002 (frontend deps) and T003 (API key) can run in parallel with T001 (backend deps)

#### Phase 2 (Foundational)
- T006 (Message model) parallel with T005 (Conversation model) - different files
- T014-T017 (MCP tools) all parallel - different tool definitions
- T010 (ConversationService) parallel with T011 (MessageService) - different files

#### User Story 1 (P1)
- T032-T033 (frontend config) parallel with T024-T031 (backend endpoint) - different codebases
- T037-T039 (tests) all parallel - different test files

#### User Story 2 (P2)
- T044-T045 (tests) parallel - different files

#### User Story 3 (P3)
- T047-T048 (delete/update multi-match) parallel with T046 (complete multi-match) - different tools
- T051-T053 (contract tests) all parallel - different test files

#### User Story 4 (P4)
- T059-T060 (ConversationList/Switcher components) parallel - different files
- T065-T067 (tests) all parallel - different test files

#### Phase 7 (Observability)
- T068-T069 (logging/metrics infrastructure) parallel - different files
- T076-T080 (performance validations) all parallel - different metrics

#### Phase 8 (Polish)
- T083-T086 (documentation/ADRs) all parallel - different files

---

## Parallel Execution Examples

### Example 1: Setup Phase (4 tasks → 2 parallel batches)

```bash
# Batch 1 (3 tasks in parallel):
Task T001: Install Python dependencies
Task T002: Install frontend dependencies
Task T003: Add OPENAI_API_KEY

# Batch 2 (sequential - external dependency):
Task T004: Configure ChatKit domain allowlist
```

### Example 2: Foundational Phase - MCP Tools (5 tools → 1 parallel batch)

```bash
# All 5 MCP tools in parallel (different tool definitions):
Task T013: Implement add_task
Task T014: Implement list_tasks
Task T015: Implement complete_task
Task T016: Implement delete_task
Task T017: Implement update_task
```

### Example 3: User Story 1 - Frontend/Backend Split (13 tasks → backend + frontend in parallel)

```bash
# Backend stream (sequential):
T024 → T025 → T026 → T027 → T028 → T029 → T030 → T031

# Frontend stream (parallel with backend):
T032 | T033 → T034 → T035 → T036

# Test stream (parallel with both, if included):
T037 | T038 | T039
```

---

## Implementation Strategy

### MVP First (User Story 1 Only) ⚡ OPTIMIZED

1. **Complete Phase 1**: Setup (T001-T004) - ~0.5 day (parallelized)
2. **Complete Phase 2**: Foundational (T005-T024) - ~3 days (with MCP/Service parallelization)
3. **Complete Phase 3**: User Story 1 (T025-T040) - ~2 days (frontend/backend parallel streams)
4. **STOP and VALIDATE**: Test US1 independently (create task via chat, see confirmation)
5. **Deploy/demo MVP** if ready

**Total MVP Time**: ~6 days (was 7 days - saved 1 day with optimizations)

### Incremental Delivery ⚡ OPTIMIZED

1. Setup + Foundational → Foundation ready (~4 days, was 5)
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!) (+2 days = 6 days total, was 7)
3. Add User Story 2 → Test independently → Deploy/Demo (+1 day = 7 days total, was 8)
4. Add User Story 3 → Test independently → Deploy/Demo (+2 days = 9 days total, was 10)
5. Add User Story 4 → Test independently → Deploy/Demo (+2 days = 11 days total, was 12)
6. Add Observability → Production readiness (+1 day = 12 days total, was 13)
7. Polish → Final validation (+1 day = 13 days total, was 14)

Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1. **Team completes Setup + Foundational together** (~5 days)
2. **Once Foundational is done**, split work:
   - Developer A: User Story 1 (P1) - Task creation
   - Developer B: User Story 2 (P2) - Task queries
   - Developer C: Observability (Phase 7)
3. **After US1 + US2 complete**:
   - Developer A: User Story 3 (P3) - Task management
   - Developer B: User Story 4 (P4) - Context awareness
   - Developer C: Polish (Phase 8)
4. Stories complete and integrate independently

**Parallel Time**: ~6-7 days (vs 13 days sequential) ⚡ OPTIMIZED - saved 1 day with parallel MCP/Service execution

---

## Task Summary

**Total Tasks**: 95 (optimized from original 90)
**Setup Phase**: 4 tasks (T001-T004)
**Foundational Phase**: 24 tasks (T005-T024) ⚡ OPTIMIZED (CRITICAL - blocks all stories)
**User Story 1 (P1)**: 16 tasks (T025-T040, including 3 optional tests) 🎯 MVP
**User Story 2 (P2)**: 6 tasks (T041-T046, including 2 optional tests)
**User Story 3 (P3)**: 9 tasks (T047-T055, including 4 optional tests)
**User Story 4 (P4)**: 13 tasks (T056-T068, including 3 optional tests)
**Observability (Phase 7)**: 15 tasks (T069-T083, including 2 optional tests)
**Polish (Phase 8)**: 8 tasks (T084-T091)

**Key Optimizations**:
- ✅ Split T010 (ConversationService) into 4 atomic tasks (T010a-T010d) for true parallelization
- ✅ Split T011 (MessageService) into 3 atomic tasks (T011a-T011c) for true parallelization
- ✅ Split T019 (AgentService) into skeleton (T019) + 5 feature tasks (T020-T024) for clarity
- ✅ Reordered MCP tools (T012-T018) to run PARALLEL with Services, not sequential (saves 2 days)
- ✅ Added explicit validation commands at all checkpoints for fast feedback

**Parallel Opportunities Identified**: 50+ tasks marked [P] can run concurrently (was 45)

**Independent Test Criteria**:
- **US1**: User creates task via chat, sees confirmation (chat endpoint + add_task tool working)
- **US2**: User queries tasks, sees formatted list (list_tasks tool + formatting working)
- **US3**: User completes/deletes/updates task by title, agent finds and executes (multi-step planning working)
- **US4**: User references previous context with pronouns, agent updates correctly (context awareness working)

**Suggested MVP Scope**: Setup + Foundational + User Story 1 (T001-T040) = 44 tasks → ~6 days (with optimizations)

**Time Saved by Optimizations**: ~1-2 days off critical path (MCP tools parallel with services, atomic task splits enable better parallelization)

---

## Parallel Execution Examples ⚡ KEY OPTIMIZATION

### Example 1: Foundational Phase - Service Layer & MCP Tools (MAJOR TIME SAVER)

**OLD APPROACH (Sequential)**: ~5 days
```
T010 (60 min) → T011 (60 min) → T012-T018 (7 tasks × 25 min = 175 min) = ~5 hours sequential
```

**NEW APPROACH (Parallel)**: ~3 days ⚡
```
Batch A - Service Layer (7 tasks in parallel):
  T010a | T010b | T010c | T010d | T011a | T011b | T011c
  ↓ (all complete in ~25 min with 7 developers, or ~3 hours solo)

Batch B - MCP Tools (6 tasks, runs PARALLEL with Batch A):
  T012 → (T013 | T014 | T015 | T016 | T017) → T018
  ↓ (all complete in ~2 hours with parallelization)

Both batches finish in ~3 hours (max of A or B), not 5 hours sequential!
```

**Key Insight**: MCP tools only need Phase II TaskService, NOT ConversationService/MessageService, so they can run at the same time!

### Example 2: User Story 1 - Frontend/Backend Split

```
Backend Stream (sequential - 8 tasks):
  T025 → T026 → T027 → T028 → T029 → T030 → T031 → T032
  (~3 hours)

Frontend Stream (parallel with backend - 5 tasks):
  T033 | T034 → T035 → T036 → T037
  (~2 hours)

Test Stream (parallel with both - 3 tasks):
  T038 | T039 | T040
  (~1 hour)

Total Time: max(3h, 2h, 1h) = 3 hours (not 6 hours sequential!)
```

### Example 3: Setup Phase - All Parallel

```
T001 (Python deps) | T002 (Frontend deps) | T003 (API key) → T004 (External)
  ↓                    ↓                      ↓
All complete in ~15 min (max time of 3 tasks), then wait for T004 approval
```

---

## Notes

- **[P] tasks** = different files, no dependencies, safe to parallelize
- **[Story] label** maps task to specific user story for traceability
- Each user story is independently completable and testable
- Tests are optional (not blocking) but included for quality assurance
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- **Constitutional Compliance**: All tasks enforce user data isolation (Principle II), stateless architecture (Principle III), and 100% Phase II reuse (FR-007, SC-006)
