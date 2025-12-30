---
id: 0002
title: Phase III Architectural Planning
stage: plan
date: 2025-12-21
surface: agent
model: claude-sonnet-4-5
feature: 004-phase-iii-ai-chatbot
branch: 004-phase-iii-ai-chatbot
user: aimon
command: /sp.plan
labels: ["phase-iii", "agentic-ai", "planning", "architecture", "reusable-intelligence", "mcp-tools", "database-schema"]
links:
  spec: specs/004-phase-iii-ai-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-phase-iii-ai-chatbot/plan.md
  - specs/004-phase-iii-ai-chatbot/research.md
  - specs/004-phase-iii-ai-chatbot/data-model.md
  - specs/004-phase-iii-ai-chatbot/contracts/add_task.json
  - specs/004-phase-iii-ai-chatbot/contracts/list_tasks.json
  - specs/004-phase-iii-ai-chatbot/contracts/complete_task.json
  - specs/004-phase-iii-ai-chatbot/contracts/delete_task.json
  - specs/004-phase-iii-ai-chatbot/contracts/update_task.json
  - specs/004-phase-iii-ai-chatbot/quickstart.md
  - CLAUDE.md (updated with Phase III technologies)
tests:
  - N/A (planning stage, no code tests)
  - Constitutional validation: 14/14 principles PASSED
  - Reusable Intelligence cataloged: 40+ Phase II components
---

## Prompt

User requested continuation from specification phase to proceed with architectural planning:

"First: Launch Explore agent to catalog Phase II RI components and Then: Run /sp.plan with RI context"

Key user emphasis:
- Use Reusable Intelligence from Phase II (100% backend reuse per FR-007, SC-006)
- Use existing subagents (Explore, Plan) rather than creating new ones
- Break Phase III into granular steps for perfect tracking
- Align with constitution and hackathon Phase III requirements

Context from previous session:
- Phase III specification complete (spec.md with 5 clarifications integrated)
- User approved proceeding with planning after agent strategy confirmation
- Constitutional alignment verified (all critical principles satisfied)
- Phase II fully merged to main branch

## Response snapshot

Executed constitutional `/sp.plan` workflow in 3 major phases:

### Phase 0: Research (research.md)
Created comprehensive research document (324 lines) with:
- **9 Architectural Decisions**:
  - R1: Conversation Lifecycle (one active + history UI)
  - R2: Message Size Limits (4000 char, 500 messages, auto-archive)
  - R3: OpenAI Model Fallback (GPT-4 → GPT-3.5-turbo)
  - R4: Observability Signals (comprehensive: logs, traces, metrics, cost)
  - R5: Data Retention (automated daily cleanup, 90 days)
  - R6: Agents SDK Integration (stateless, run() method, tool auto-selection)
  - R7: MCP Server Architecture (same backend process, direct function calls)
  - R8: Frontend ChatKit Integration (replace Phase II UI completely)
  - R9: Context Reconstruction (fetch last 50 messages from DB)
- **27 Alternatives Evaluated**: Each decision documented with alternatives considered and rejected with rationale
- **Technology Stack Decisions**: Backend (FastAPI, OpenAI Agents SDK, MCP SDK), Frontend (Next.js, ChatKit), AI (GPT-4/3.5-turbo)
- **5 Risk Mitigation Strategies**: Cost control, intent accuracy, context loss, performance degradation, error handling
- **Dependencies & Integration**: 4 external (OpenAI API, ChatKit, Agents SDK, MCP SDK), 4 internal (Phase II RI components)

### Phase 1: Design (data-model.md, contracts/, quickstart.md)

**data-model.md** (508 lines):
- **2 New Tables**: Conversation (5 fields), Message (6 fields)
- **6 Indexes**: 3 on Conversation (user_id, user_id+is_active, created_at), 3 on Message (conversation_id, user_id, conversation_id+created_at)
- **4 Foreign Keys**: Conversation→User, Message→Conversation, Message→User (CASCADE deletes)
- **6 Data Access Patterns**: Active conversation lookup, message retrieval (last 50), message creation, auto-archive trigger, history pagination, 90-day cleanup
- **SQLModel Schemas**: Full Python class definitions with relationships
- **Alembic Migration**: Complete SQL for CREATE TABLE and indexes
- **Performance Analysis**: Query latency targets (<25ms), scaling estimates (1000 users, 10 conversations/user, 200 messages/conversation = ~2M messages = ~200MB)

**contracts/ directory** (5 MCP tool JSON schemas):
- **add_task.json**: Create task tool with user_id, title, description parameters
- **list_tasks.json**: List tasks tool with user_id, status filter (all/pending/completed)
- **complete_task.json**: Complete task tool with user_id, task_id, multi-step planning notes
- **delete_task.json**: Delete task tool with user_id, task_id, confirmation guidance
- **update_task.json**: Update task tool with user_id, task_id, partial update support
- Each schema includes: JSON Schema validation, examples, return types, error codes, agent_notes for tool chaining, implementation mapping to Phase II TaskService

**quickstart.md** (458 lines):
- **8-Step Setup Guide**: OpenAI API key setup, backend dependencies, database migration, frontend ChatKit installation, testing workflows, monitoring, deployment, automated cleanup
- **4 Manual Test Scenarios**: P1-P4 user stories with expected agent behavior
- **7 Error Handling Tests**: Ambiguous intent, task not found, API failures
- **Production Deployment**: Environment variables, domain allowlist, health checks, Kubernetes CronJob for 90-day retention
- **Troubleshooting Section**: Common issues (rate limits, conversation not found, wrong tool selection, high latency) with solutions
- **Success Criteria Validation**: Checklist for all 10 success criteria (SC-001 to SC-010)

### Phase 2: Plan Documentation (plan.md)

**plan.md** completed with:
- **Summary**: Technical approach (frontend ChatKit replacement, agent layer, MCP server, conversation persistence, model strategy)
- **Technical Context**: Languages (Python 3.13+, TypeScript 5.x), dependencies (FastAPI, Agents SDK, MCP SDK, ChatKit), performance goals (p95 <2s, ≥90% accuracy, 100 concurrent, <$0.10/conversation)
- **Constitution Check**: 14 principles verified, all PASS (Spec-Driven, User Isolation, Stateless, Smallest Change, Human-as-Tool, MCP Design, Testing, Security, Auth, Rate Limiting, Error Handling, Performance, Conversation Persistence)
- **Project Structure**: 18 new files (13 backend, 5 frontend), 15+ reused files (TaskService, AuthService, database layer, auth routes, UI components)
- **Backend Structure**: models/ (conversation.py, message.py), services/ (conversation_service.py, message_service.py, agent_service.py), mcp/ (tools.py, server.py), routes/ (chat.py), tests/ (5 new test files)
- **Frontend Structure**: app/chat/page.tsx (ChatKit), components/ (ChatInterface.tsx, ConversationList.tsx, ConversationSwitcher.tsx), lib/ (chatkit-config.ts)
- **Complexity Tracking**: No violations detected
- **Design Artifacts**: References to research.md, data-model.md, contracts/, quickstart.md
- **Plan Status**: ✅ READY FOR TASK GENERATION

### Phase II Reusable Intelligence Cataloging

Launched Explore agent (very thorough mode) to catalog Phase II components:
- **40+ Components Cataloged**: TaskService (6 CRUD functions), AuthService (5 functions), User/Task models, database layer, 8 API routes, middleware, test infrastructure
- **100% Backend Reuse Verified**: All 6 TaskService functions map directly to MCP tools (no changes needed)
- **Zero Code Changes Required**: Principle IV (Smallest Viable Change) satisfied

### Agent Context Update

Updated CLAUDE.md with:
- Added language: Python 3.13+ (backend), TypeScript 5.x (frontend)
- Added database: Neon PostgreSQL (existing tables + new Conversation/Message tables)
- Preserved manual additions from Phase II

## Outcome

- ✅ Impact: Phase III architectural plan complete - defines HOW to build agentic AI transformation with 100% Phase II backend reuse, comprehensive design artifacts, and clear implementation roadmap
- 🧪 Tests: Constitutional validation PASS (14/14 principles), RI cataloging PASS (40+ components identified), no complexity violations
- 📁 Files: plan.md (207 lines), research.md (324 lines), data-model.md (508 lines), 5 MCP tool contracts (JSON schemas), quickstart.md (458 lines), CLAUDE.md (updated)
- 🔁 Next prompts: `/sp.tasks` to generate tasks.md with granular implementation steps, dependency ordering, and parallel execution opportunities
- 🧠 Reflection: Constitutional planning workflow executed successfully - Phase 0 research documented 9 decisions with 27 alternatives evaluated, Phase 1 design created database schema with 6 indexes + 5 MCP tool contracts + comprehensive quickstart guide, Explore agent cataloged 40+ RI components for 100% reuse, all constitutional principles satisfied, ready for task generation

## Evaluation notes (flywheel)

- Failure modes observed: None - setup script ran successfully, all planning phases completed without errors, agent context update script worked correctly
- Graders run and results (PASS/FAIL): Constitution Check PASS (14/14 principles), Reusable Intelligence PASS (40+ components cataloged, 100% backend reuse verified), Project Structure PASS (18 new files, 15+ reused files documented), Design Artifacts PASS (research.md, data-model.md, contracts/, quickstart.md all created)
- Prompt variant (if applicable): `/sp.plan` (constitutional workflow) - standard architecture planning workflow per Principle I (Spec-Driven Development)
- Next experiment (smallest change to try): Proceed to `/sp.tasks` for task generation - break down implementation into granular steps with acceptance criteria, identify parallel execution opportunities (database migration || MCP tool creation || frontend ChatKit setup), assign priorities based on user story dependencies (P1→P2→P3→P4), ensure ≥80% test coverage targets
