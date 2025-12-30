# ADR-0006: Agent Context Reconstruction with Last 50 Messages

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-21
- **Feature:** 004-phase-iii-ai-chatbot
- **Context:** Agent is stateless (Principle III) and must reconstruct conversation context from database on each request. Decision needed on how much message history to fetch: all messages vs limited window vs summarization strategy.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅ YES - Affects user experience (context accuracy), OpenAI API costs (token usage), and performance (query latency)
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅ YES - 4 alternatives evaluated (fetch all, last 50, summarization, in-memory caching)
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅ YES - Impacts agent service, database queries, API costs, and success criteria (SC-001, SC-004, SC-009)
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

Fetch last 50 messages ordered by `created_at DESC`, reverse array for chronological order, pass to agent as context.

**Components**:
- Database query in `backend/src/services/message_service.py` (get_conversation_messages)
- Context reconstruction in `backend/src/services/agent_service.py` (get_conversation_context)
- Database index: `ix_message_conversation_id_created_at` (composite index for fast retrieval)
- Token budget management: 50 messages ≈ 5K-15K tokens (well within GPT-4 128K context window)

**Query Pattern**:
```python
SELECT * FROM message
WHERE conversation_id = :conversation_id
ORDER BY created_at DESC
LIMIT 50
```
Then reverse array for chronological order [oldest → newest].

## Consequences

### Positive

- **Predictable latency**: <50ms query time with composite index (validates SC-001: p95 <2s)
- **Sufficient context**: 50 messages ≈ 5-10 conversation turns = enough for multi-step planning (validates SC-004: 10+ exchanges)
- **Manageable cost**: 5K-15K context tokens × $0.001/1K = $0.005-0.015 per request (validates SC-009: <$0.10/conversation)
- **Simple implementation**: No summarization logic, no caching invalidation complexity
- **Stateless design**: Server survives restarts, no in-memory state (Principle III compliance)
- **Database performance**: Composite index on (conversation_id, created_at) enables fast seeks

### Negative

- **Context truncation**: Conversations >50 messages lose older context (rare with 500-message limit + auto-archive at 500)
- **Token overhead**: Always fetches 50 messages even if user only needs last 5 (slight cost inefficiency)
- **No summarization**: Long conversations (100+ messages) not optimized (deferred to Phase V)
- **Fixed window**: Cannot dynamically adjust based on conversation complexity

**Mitigation Strategies**:
- 500-message conversation limit (FR-017) + auto-archive reduces likelihood of >50 message conversations
- FR-019 observability tracks conversations exceeding 50 messages (metric: `long_conversation_count`)
- Edge case handling: If conversation has >100 messages, log warning and track via metrics
- Phase V improvement: Implement sliding window summarization for messages 50-100

## Alternatives Considered

**Alternative 1: Fetch All Messages**
- **Approach**: Query all messages in conversation, pass entire history to agent
- **Rejected because**:
  - Unbounded token usage: 500-message conversation = 50K-150K tokens (exceeds GPT-4 128K context window)
  - Unbounded cost: $0.05-0.15 per request in worst case (exceeds SC-009: <$0.10/conversation)
  - Performance: Query latency increases linearly with message count (affects SC-001)
- **When to revisit**: Never - violates cost and performance constraints

**Alternative 2: Summarization of Old Messages**
- **Approach**: Fetch all messages, summarize messages 50-100 into condensed context, keep last 50 as-is
- **Evaluated**: Provides better context retention for long conversations
- **Deferred to Phase V because**:
  - Adds complexity: Requires summarization logic (GPT call or extractive summarization)
  - Increases cost: Additional GPT call for summarization ($0.01-0.02 per summary)
  - Not needed for Phase III: 500-message limit + auto-archive makes >50 message conversations rare
  - Can implement later if FR-019 metrics show >10% of conversations exceed 50 messages
- **When to revisit**: Phase V if metrics show >10% of conversations losing important context

**Alternative 3: In-Memory Caching**
- **Approach**: Cache conversation history in Redis/in-memory, fetch from cache instead of DB
- **Rejected because**:
  - Violates Principle III (Stateless Architecture): Introduces cache invalidation complexity
  - Cache invalidation: Must invalidate on new message, conversation switch, multi-device access
  - Scaling complexity: Requires cache warming, TTL management, cache server maintenance
  - Minimal performance benefit: Composite index already provides <50ms query time
- **When to revisit**: Never for Phase III - violates core architectural principle

**Alternative 4: Dynamic Window (Last N Based on Token Budget)**
- **Approach**: Fetch messages until cumulative tokens reach budget (e.g., 10K tokens), dynamically adjust N
- **Evaluated**: Optimizes cost by fetching only what fits in token budget
- **Rejected because**:
  - Complexity: Requires token counting logic before fetching (need to estimate message sizes)
  - Unpredictable behavior: Window size varies per conversation (harder to debug)
  - Marginal benefit: Fixed 50-message window already manages cost effectively
  - Over-engineering: Adds complexity without significant cost savings for Phase III
- **When to revisit**: Phase V if cost metrics show token budget optimization needed

## References

- Feature Spec: [specs/004-phase-iii-ai-chatbot/spec.md](../../specs/004-phase-iii-ai-chatbot/spec.md) (FR-005, FR-015, SC-004)
- Implementation Plan: [specs/004-phase-iii-ai-chatbot/plan.md](../../specs/004-phase-iii-ai-chatbot/plan.md) (Phase 3.4: Agent Service, Edge Case 5)
- Research Document: [specs/004-phase-iii-ai-chatbot/research.md](../../specs/004-phase-iii-ai-chatbot/research.md) (R9: Conversation Context Reconstruction Strategy, lines 167-183)
- Data Model: [specs/004-phase-iii-ai-chatbot/data-model.md](../../specs/004-phase-iii-ai-chatbot/data-model.md) (Pattern 2: Fetch Conversation Messages, lines 258-281)
- Related ADRs: None
- Evaluator Evidence: Decision validated against SC-001 (p95 <2s latency), SC-004 (context maintained 10+ exchanges), SC-009 (<$0.10/conversation cost)
