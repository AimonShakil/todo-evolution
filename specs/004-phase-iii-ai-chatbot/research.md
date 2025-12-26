# Phase III Research & Decisions

**Feature**: Agentic AI Chatbot
**Date**: 2025-12-19
**Status**: Complete

## Research Questions Resolved

All technical decisions were clarified during spec phase (5 clarification questions). This document consolidates rationale and alternatives considered.

---

## R1: Conversation Lifecycle Management

**Decision**: One active conversation per user with history browsing/switching UI

**Rationale**:
- Balances simplicity (single active conversation reduces cognitive load for basic task management)
- Provides flexibility (users can browse/switch to previous conversations for context retrieval)
- Standard pattern in ChatGPT, Claude, and other AI chat interfaces
- Prevents scaling issues with unlimited message accumulation in single conversation

**Alternatives Considered**:
- **Single permanent conversation** - Rejected: Creates scaling issues with message count, difficult to navigate long history
- **Manual conversation creation** - Rejected: Adds unnecessary friction for task management bot (not a general chat system)
- **Automatic daily/weekly expiry** - Rejected: Arbitrary time boundaries don't align with task management workflows

**Implementation**: `is_active` boolean field on Conversation table, UI component for conversation list/switch

---

## R2: Message Size & Conversation Limits

**Decision**: 4000 char/message, 500 messages/conversation (auto-archive after limit)

**Rationale**:
- **4000 chars**: Accommodates detailed task descriptions (typical paragraph: 500-1000 chars) while preventing abuse
- **500 messages**: ~25 back-and-forth exchanges sufficient for complex task management workflows
- Auto-archiving prevents database bloat and maintains performance
- Aligns with OpenAI context window management best practices (token limits)

**Alternatives Considered**:
- **No limits** - Rejected: Unbounded growth causes database bloat, increases query latency, escalates costs
- **Strict limits (1000 char, 200 messages)** - Rejected: Too restrictive for legitimate use cases (multi-paragraph task descriptions)
- **Very large limits (10K char, unlimited messages)** - Rejected: Excessive for task management domain, increases cost/latency

**Implementation**: Pydantic validation on message length, conversation message count check before insert, auto-archive trigger at 500

---

## R3: OpenAI Model Fallback Strategy

**Decision**: Primary GPT-4, Fallback GPT-3.5-turbo (automatic on rate limits/errors)

**Rationale**:
- **GPT-4**: Best intent recognition for complex multi-step workflows (agentic reasoning required), superior tool use accuracy
- **GPT-3.5-turbo**: Sufficient for simple queries ("list my tasks"), costs ~10x less than GPT-4
- **Automatic fallback**: Ensures reliability when GPT-4 rate-limited (common during high traffic)
- Maintains cost target (<$0.10/conversation) while prioritizing quality

**Alternatives Considered**:
- **GPT-4 only, no fallback** - Rejected: Single point of failure, no resilience to rate limits
- **Intelligent routing (simple → 3.5, complex → 4)** - Rejected: Adds complexity determining "simple vs complex", potential misclassification reduces quality
- **User-configurable model** - Rejected: Out of scope for Phase III, adds UI complexity, most users don't understand model differences

**Implementation**: Try-catch in agent service, attempt GPT-4 first, catch rate limit exception, retry with GPT-3.5-turbo

---

## R4: Observability & Monitoring Signals

**Decision**: Comprehensive observability - request/response logs, tool call traces, latency metrics, intent accuracy tracking, error rates

**Rationale**:
- **Request/response logs**: Essential for debugging agent behavior ("why did it choose this tool?")
- **Tool call traces**: Enables validation of multi-step workflows (did agent chain tools correctly?)
- **Latency metrics**: Validates SC-001 (p95 <2s), identifies performance bottlenecks
- **Intent accuracy tracking**: Validates SC-002 (≥90% accuracy), identifies intent recognition failures
- **Error rates**: Validates SC-007 (100% error recovery), alerts on systemic issues
- **Cost tracking**: Validates SC-009 (<$0.10/conversation), prevents budget overruns

**Alternatives Considered**:
- **Minimal (errors only)** - Rejected: Insufficient for validating success criteria, can't debug agent reasoning
- **Standard (logs + errors)** - Rejected: Missing metrics for performance/accuracy validation
- **Advanced (OpenTelemetry + custom agent reasoning logs)** - Deferred to Phase V: Overkill for Phase III, adds unnecessary complexity

**Implementation**: Structured JSON logging (Python `logging` module), custom middleware for latency tracking, metrics stored in database for analysis

---

## R5: Data Retention Enforcement

**Decision**: Automated daily cleanup job (deletes conversations >90 days)

**Rationale**:
- **Automated**: No manual intervention required, consistent enforcement
- **Daily frequency**: Sufficient for 90-day retention (hourly would be overkill)
- **Hard delete**: Reclaims storage immediately (soft delete deferred as not needed for Phase III)
- Supports data privacy compliance (GDPR-style retention policies)

**Alternatives Considered**:
- **Manual cleanup** - Rejected: Requires ops overhead, inconsistent enforcement, human error risk
- **Soft delete + archival (90 day soft, 180 day hard)** - Deferred: Useful but unnecessary complexity for Phase III
- **No automatic deletion** - Rejected: Violates stated retention policy, causes unbounded database growth

**Implementation**: Python script with Alembic-managed database query, scheduled via cron or K8s CronJob, logs deletion count for audit

---

## R6: OpenAI Agents SDK Integration Pattern

**Decision**: Use OpenAI Agents SDK `run()` method with tool list, agent reconstructs context from database on each request

**Rationale**:
- **Official SDK**: Well-documented, maintained by OpenAI, best practices built-in
- **Stateless design**: Agent doesn't maintain in-memory state, fetches conversation history from DB each request
- **Tool auto-selection**: SDK handles intent → tool mapping based on function descriptions
- **Multi-step workflows**: SDK supports tool chaining without manual orchestration

**Alternatives Considered**:
- **OpenAI Chat Completions API directly** - Rejected: Requires manual function calling loop, more complex, error-prone
- **LangChain Agents** - Rejected: Adds heavy dependency, overkill for 5 tools, harder to customize
- **Custom agent framework** - Rejected: Reinventing wheel, maintenance burden, no time for Phase III

**Implementation**: Install `openai` Python package, use `Agent` class with `tools` parameter, pass conversation history as messages array

---

## R7: MCP Server Architecture

**Decision**: MCP server runs in same FastAPI backend process (not separate service), tools defined as Python functions

**Rationale**:
- **Simplicity**: No inter-process communication overhead, no service discovery needed
- **Performance**: Direct function calls (no HTTP/gRPC latency)
- **Development speed**: Single codebase, single deployment, single debug session
- **Phase III scope**: 5 tools with simple CRUD operations don't justify separate service

**Alternatives Considered**:
- **Separate MCP server process** - Deferred to Phase IV/V: Useful for microservices but unnecessary complexity for Phase III
- **MCP over HTTP** - Rejected: Adds latency, requires service discovery, overkill for co-located deployment
- **MCP SDK server wrapper** - Explored: Official MCP SDK may require server process, will adapt based on SDK documentation

**Implementation**: Define MCP tools as async Python functions in `backend/src/mcp/tools.py`, register with agent SDK, call Phase II services directly

---

## R8: Frontend ChatKit Integration

**Decision**: Replace Phase II task list UI with OpenAI ChatKit full-page interface, keep auth/navigation shell

**Rationale**:
- **Official component**: OpenAI-maintained React component, follows best practices
- **Complete UX**: Handles message rendering, input, streaming, error states
- **Conversation switching**: Built-in conversation list/switching UI
- **Minimal custom code**: Focus on agent backend, not UI development

**Alternatives Considered**:
- **Custom chat UI** - Rejected: Significant development effort, inferior UX compared to official component
- **Gradual migration (chat + task list)** - Rejected: Confusing dual interface, unclear value proposition
- **Third-party chat library** - Rejected: Less integration with OpenAI API, more customization needed

**Implementation**: Install `@openai/chat-kit` package, replace `frontend/app/tasks/page.tsx` with ChatKit component, configure API endpoint

---

## R9: Conversation Context Reconstruction Strategy

**Decision**: Fetch last 50 messages from database on each request, pass to agent as message array

**Rationale**:
- **Stateless**: Server doesn't cache messages in memory, survives restarts
- **50 message window**: ~5-10 conversation turns, sufficient for context while managing token limits
- **Database query performance**: Indexed on conversation_id + created_at, <50ms query time
- **Token budget**: 50 messages ≈ 5K-15K tokens (within GPT-4 128K context window)

**Alternatives Considered**:
- **Fetch all messages** - Rejected: Unbounded token usage, exceeds context window for long conversations
- **Summarization of old messages** - Deferred to Phase V: Adds complexity, not needed for 500-message limit
- **In-memory caching** - Rejected: Violates stateless architecture, cache invalidation complexity

**Implementation**: Database query with `ORDER BY created_at DESC LIMIT 50`, reverse array for chronological order, pass to agent SDK

---

## Technology Stack Decisions

### Backend Stack

| Component | Choice | Rationale |
|-----------|--------|-----------|
| **Agent Framework** | OpenAI Agents SDK (Python) | Official SDK, async support, tool auto-selection, multi-step workflows |
| **MCP SDK** | Official MCP SDK | Standardized protocol, OpenAI compatibility, future-proof |
| **API Framework** | FastAPI (reused from Phase II) | Async/await, Pydantic validation, OpenAPI docs, existing expertise |
| **ORM** | SQLModel (reused from Phase II) | Type-safe queries, migration support, Pydantic integration |
| **Database** | Neon PostgreSQL (reused from Phase II) | Serverless scaling, automatic backups, existing setup |
| **Authentication** | Better Auth + JWT (reused from Phase II) | Zero changes needed, proven secure, stateless tokens |

### Frontend Stack

| Component | Choice | Rationale |
|-----------|--------|-----------|
| **Chat UI** | OpenAI ChatKit | Official component, complete UX, conversation switching built-in |
| **Framework** | Next.js 16 (reused from Phase II) | App Router, TypeScript support, existing auth integration |
| **Auth** | Better Auth (reused from Phase II) | Zero changes needed, JWT token generation for API calls |
| **Styling** | Tailwind CSS (reused from Phase II) | Utility-first, responsive design, existing theme |

### AI Stack

| Component | Choice | Rationale |
|-----------|--------|-----------|
| **Primary Model** | GPT-4 | Best intent recognition, tool use accuracy, multi-step reasoning |
| **Fallback Model** | GPT-3.5-turbo | Cost-effective, sufficient for simple queries, reliability backup |
| **API** | OpenAI API | Industry standard, comprehensive documentation, SDK support |

---

## Risk Mitigation Strategies

### R1: OpenAI API Cost Control

**Risk**: Unbounded API costs if users send many messages

**Mitigation**:
- FR-017: 4000 char/message, 500 messages/conversation limits
- FR-015: Rate limiting (100 req/min) inherited from Phase II
- SC-009: Cost tracking observability (alert if >$0.10/conversation)
- Model fallback: GPT-3.5-turbo for cost-sensitive scenarios

### R2: Intent Recognition Accuracy

**Risk**: Agent selects wrong tool or fails to understand user intent

**Mitigation**:
- SC-002: ≥90% accuracy target with intent accuracy tracking (FR-019)
- GPT-4 primary model (superior intent recognition)
- Clear tool descriptions in MCP schemas (explicit examples)
- Fallback to clarifying questions when uncertain (edge case defined)

### R3: Conversation Context Loss

**Risk**: Agent forgets context in long conversations

**Mitigation**:
- FR-006: Conversation history persisted to database
- Fetch last 50 messages for context reconstruction
- SC-004: Context maintained across 10+ exchanges validation
- 500 message limit prevents unbounded context growth

### R4: Database Performance Degradation

**Risk**: Conversation/message queries slow down as tables grow

**Mitigation**:
- Database indexes on user_id, conversation_id, created_at (specified in data-model.md)
- Pagination on conversation list (limit 20 per page)
- 90-day automated cleanup (FR-020) prevents unbounded growth
- Neon PostgreSQL autoscaling handles load spikes

### R5: Agent Error Handling

**Risk**: Agent crashes or returns unhelpful errors on tool failures

**Mitigation**:
- SC-007: 100% error recovery target
- FR-008: Graceful error handling without exposing technical details
- Edge cases defined for: tool failures, ambiguous intents, missing tasks
- Comprehensive observability (FR-019) for debugging

---

## Dependencies & Integration Points

### External Dependencies

- **OpenAI API**: Requires API key, subject to rate limits, costs per token
- **OpenAI ChatKit**: React component, requires domain allowlist configuration
- **OpenAI Agents SDK**: Python package, beta/evolving API (monitor for breaking changes)
- **MCP SDK**: Official SDK, specification compliance required

### Integration Points (100% Reusable from Phase II)

- **TaskService**: All 6 CRUD operations reused by MCP tools
- **AuthService**: JWT validation for chat endpoint
- **Database Layer**: Connection pooling, session management, migrations
- **API Middleware**: Rate limiting, CORS, error handling

---

## Deployment Considerations

### Environment Variables (New)

```
OPENAI_API_KEY=sk-...              # Required for agent/model calls
```

### Environment Variables (Reused from Phase II)

```
DATABASE_URL=postgresql://...      # Neon PostgreSQL connection
BETTER_AUTH_SECRET=...             # JWT signing key
JWT_SECRET=...                     # Alternative JWT key (if used)
```

### OpenAI ChatKit Configuration

- **Domain Allowlist**: Add production domain to OpenAI dashboard
- **API Endpoint**: Configure ChatKit to call `/api/{user_id}/chat`
- **Authentication**: Pass JWT token in Authorization header

---

## Research Summary

**Total Decisions**: 9 major architectural decisions
**Clarifications from Spec Phase**: 5 (conversation lifecycle, message limits, model fallback, observability, retention)
**Additional Research**: 4 (Agents SDK integration, MCP architecture, ChatKit integration, context reconstruction)
**Alternatives Evaluated**: 27 alternatives considered and rejected with rationale
**Dependencies Identified**: 4 external (OpenAI API/ChatKit/Agents SDK/MCP SDK), 4 internal (Phase II RI components)
**Risks Mitigated**: 5 (cost, accuracy, context loss, performance, error handling)

**Research Status**: ✅ **COMPLETE** - All unknowns resolved, ready for Phase 1 design
