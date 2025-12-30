# ADR-0007: OpenAI Model Fallback GPT-4 to GPT-3.5-Turbo

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-21
- **Feature:** 004-phase-iii-ai-chatbot
- **Context:** OpenAI API subject to rate limits and outages. Agent must remain reliable when primary model (GPT-4) unavailable. Decision needed on failover strategy: no fallback (fail fast) vs automatic fallback to cheaper model vs intelligent routing based on query complexity.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅ YES - Affects system reliability (SC-007: 100% error recovery), cost management (SC-009), and user experience (SC-002: intent accuracy)
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅ YES - 4 alternatives evaluated (GPT-4 only, intelligent routing, user-configurable, automatic fallback)
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅ YES - Impacts agent service, error handling, cost tracking, observability
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

Automatic model fallback from GPT-4 (primary) to GPT-3.5-turbo (fallback) on rate limits and errors.

**Components**:
- Primary model: GPT-4 (or GPT-4-turbo) for all agent requests
- Fallback model: GPT-3.5-turbo triggered on `RateLimitError` or `APIError`
- Implementation in `backend/src/services/agent_service.py` (invoke_agent function)
- FR-019 observability: Track fallback rate, intent accuracy per model, cost per model

**Error Handling Logic**:
```python
try:
    # Try GPT-4 first
    response = await openai.agents.run(model="gpt-4", ...)
except openai.error.RateLimitError:
    # Automatic fallback to GPT-3.5-turbo
    response = await openai.agents.run(model="gpt-3.5-turbo", ...)
except openai.error.APIError:
    # User-friendly error message
    return "AI assistant temporarily unavailable. Please try again in a moment."
```

## Consequences

### Positive

- **High availability**: Validates SC-007 (100% error recovery) - agent always responds even during GPT-4 outages
- **Cost optimization**: GPT-3.5-turbo costs ~10x less ($0.0002/1K output tokens vs $0.002/1K for GPT-4) - helps maintain SC-009 (<$0.10/conversation)
- **Simple implementation**: Try-catch with model parameter change - no complex routing logic
- **Maintains quality**: GPT-4 used for 95%+ of requests (fallback only on rate limits/errors)
- **Observability**: FR-019 metrics track fallback rate and accuracy per model (enables cost/quality tradeoffs analysis)

### Negative

- **Intent accuracy variance**: GPT-3.5-turbo ~85% accuracy vs GPT-4 ~95% accuracy (may not meet SC-002: ≥90% during fallback periods)
- **User experience inconsistency**: Some users get GPT-4 responses, others get GPT-3.5 (during rate limits)
- **No user notification**: Users not informed when fallback occurs (transparent but potentially confusing if quality drops)
- **Fallback thrashing**: If GPT-4 rate-limited for extended period, all users fall back (no automatic recovery when limit lifts)

**Mitigation Strategies**:
- FR-019 observability alerts if fallback rate >10% (indicates sustained rate limiting - need to upgrade OpenAI plan)
- Intent accuracy tracking per model (if GPT-3.5 accuracy <85%, reconsider fallback strategy)
- SC-002 target (≥90% accuracy) measured across all requests (not per-model) - fallback doesn't invalidate success criteria if rare
- User notification deferred to Phase V (if metrics show fallback rate >5%, add "Using fallback model" indicator)

## Alternatives Considered

**Alternative 1: GPT-4 Only, No Fallback**
- **Approach**: Use GPT-4 exclusively, return error if unavailable
- **Rejected because**:
  - Single point of failure: Violates SC-007 (100% error recovery) - users cannot use app during outages
  - No resilience to rate limits: High traffic periods result in complete service outage
  - Poor user experience: "Service unavailable" errors frustrate users
- **When to revisit**: Never - violates reliability success criteria

**Alternative 2: Intelligent Routing (Simple Queries → GPT-3.5, Complex → GPT-4)**
- **Approach**: Classify user intent as simple/complex, route to appropriate model
- **Evaluated**: Could optimize cost by using GPT-3.5 for "What tasks do I have?" queries
- **Rejected because**:
  - Adds complexity: Requires intent classification logic before model selection (what defines "simple"?)
  - Misclassification risk: If classifier wrong, user gets GPT-3.5 for complex query → poor accuracy
  - Marginal cost savings: 80% of queries are create/update tasks (need GPT-4), only 20% are simple lists
  - Over-engineering: Adds complexity without significant benefit for Phase III
- **When to revisit**: Phase V if cost metrics show GPT-4 usage consistently exceeds budget

**Alternative 3: User-Configurable Model**
- **Approach**: Let users choose between GPT-4 (high quality) or GPT-3.5 (faster, cheaper) in settings
- **Rejected because**:
  - Out of scope for Phase III: Adds UI complexity (settings page, model selection dropdown)
  - User confusion: Most users don't understand model differences or tradeoffs
  - Premature optimization: No evidence users want this control (defer until requested)
- **When to revisit**: Phase V if user research shows demand for model selection

**Alternative 4: No Fallback, Queue Requests During Rate Limits**
- **Approach**: When GPT-4 rate-limited, queue requests and retry with exponential backoff
- **Rejected because**:
  - Violates SC-001 (p95 <2s latency): Queueing adds unbounded latency
  - Poor user experience: Users wait 10-60s for responses during rate limit periods
  - Complexity: Requires queue implementation (Redis/RabbitMQ), worker processes, retry logic
- **When to revisit**: Never for Phase III - latency constraints preclude queueing

## References

- Feature Spec: [specs/004-phase-iii-ai-chatbot/spec.md](../../specs/004-phase-iii-ai-chatbot/spec.md) (FR-018, SC-002, SC-007, SC-009, Edge Case 4)
- Implementation Plan: [specs/004-phase-iii-ai-chatbot/plan.md](../../specs/004-phase-iii-ai-chatbot/plan.md) (Phase 3.4: Agent Service, Edge Case 4: OpenAI API Down/Rate-Limited)
- Research Document: [specs/004-phase-iii-ai-chatbot/research.md](../../specs/004-phase-iii-ai-chatbot/research.md) (R3: OpenAI Model Fallback Strategy, lines 51-67)
- Related ADRs: None
- Evaluator Evidence: Decision validated against SC-007 (100% error recovery), SC-009 (<$0.10/conversation cost), FR-019 (observability requirements)
