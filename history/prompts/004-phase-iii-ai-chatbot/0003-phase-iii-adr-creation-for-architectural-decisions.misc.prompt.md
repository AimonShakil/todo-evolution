---
id: 0003
title: Phase III ADR Creation for Architectural Decisions
stage: misc
date: 2025-12-21
surface: agent
model: claude-sonnet-4-5
feature: 004-phase-iii-ai-chatbot
branch: 004-phase-iii-ai-chatbot
user: aimon
command: /sp.adr
labels: ["phase-iii", "adr", "architecture", "decision-records", "mcp-server", "context-reconstruction", "model-fallback"]
links:
  spec: specs/004-phase-iii-ai-chatbot/spec.md
  ticket: null
  adr: history/adr/0005-mcp-server-co-located-with-fastapi-backend.md, history/adr/0006-agent-context-reconstruction-with-last-50-messages.md, history/adr/0007-openai-model-fallback-gpt-4-to-gpt-3-5-turbo.md
  pr: null
files:
  - history/adr/0005-mcp-server-co-located-with-fastapi-backend.md
  - history/adr/0006-agent-context-reconstruction-with-last-50-messages.md
  - history/adr/0007-openai-model-fallback-gpt-4-to-gpt-3-5-turbo.md
tests:
  - ADR significance test: 3/3 PASSED (all pass impact, alternatives, scope criteria)
  - Clustering check: PASSED (decisions grouped as architectural clusters, not atomic choices)
  - Alternatives evaluation: PASSED (each ADR documents 3-4 alternatives with rationale)
  - Consequences analysis: PASSED (positive/negative outcomes documented with mitigation strategies)
---

## Prompt

User requested creation of 3 ADRs as part of comprehensive plan improvement workflow:

"do all the six recommended actions and also A & B"

Context:
- User reviewing Phase III plan and identified gaps in implementation phasing, dependency graph, edge case logic, observability schema, frontend testing strategy, and ADR documentation
- Plan analysis revealed 3 architecturally significant decisions from research.md that pass constitutional 3-part test (impact, alternatives, scope)
- ADR creation part of systematic plan completion before proceeding to /sp.tasks

User initiated /sp.adr command with specific focus: "MCP Server Co-located with FastAPI Backend"

Command triggered /sp.adr workflow to document all significant Phase III architectural decisions.

## Response snapshot

Executed constitutional `/sp.adr` workflow for Phase III architectural decision documentation:

### Step 1-2: Extract & Analyze Decisions

Loaded planning artifacts:
- plan.md (implementation phases, dependency graph, edge cases)
- research.md (9 architectural decisions with alternatives)
- data-model.md (database schema, query patterns)

Identified 3 architecturally significant decision clusters passing significance test:

**Decision 1: MCP Server Architecture** (user-requested)
- **Context**: 5 MCP tools wrapping Phase II TaskService - co-located vs separate service
- **Documented**: research.md R7 (lines 129-145), plan.md Phase 3.3
- **Significance**: ✅ Impact (deployment model, scaling), ✅ Alternatives (3 evaluated), ✅ Scope (cross-cutting)

**Decision 2: Agent Context Reconstruction**
- **Context**: Stateless agent must fetch conversation history - how much to fetch?
- **Documented**: research.md R9 (lines 167-183), data-model.md Pattern 2
- **Significance**: ✅ Impact (cost, performance, UX), ✅ Alternatives (4 evaluated), ✅ Scope (affects SC-001, SC-004, SC-009)

**Decision 3: OpenAI Model Fallback**
- **Context**: GPT-4 rate limits/outages - fallback strategy needed
- **Documented**: research.md R3 (lines 51-67), plan.md Edge Case 4
- **Significance**: ✅ Impact (reliability, cost), ✅ Alternatives (4 evaluated), ✅ Scope (affects SC-002, SC-007, SC-009)

### Step 3: Check Existing ADRs

Scanned history/adr/ directory:
- Existing: ADR-0001 to ADR-0004 (Phase I/II decisions)
- **No conflicts** detected with Phase III decisions

### Step 4: Significance Test Validation ✅

All 3 decisions passed constitutional 3-part test:
- ✅ **Impact**: Long-term consequences for architecture/platform
- ✅ **Alternatives**: Multiple viable options considered with tradeoffs
- ✅ **Scope**: Cross-cutting concerns affecting multiple components

### Step 5: Create ADRs

**ADR-0005: MCP Server Co-located with FastAPI Backend**
- Decision: MCP server runs in same FastAPI backend process (not separate service)
- Alternatives: Separate HTTP service (rejected - latency), gRPC service (rejected - complexity), MCP SDK wrapper (deferred - SDK evolving)
- Positive consequences: Simplicity, performance (<1ms overhead), 100% Phase II reuse, single deployment
- Negative consequences: Scaling granularity, resource sharing, deployment coupling
- Mitigation: Stateless design enables horizontal scaling, deferred separation to Phase IV/V if tool count >10

**ADR-0006: Agent Context Reconstruction with Last 50 Messages**
- Decision: Fetch last 50 messages ordered by created_at DESC, reverse for chronological order
- Alternatives: Fetch all (rejected - unbounded cost), summarization (deferred - complexity), in-memory caching (rejected - violates stateless), dynamic window (rejected - over-engineering)
- Positive consequences: Predictable latency (<50ms), sufficient context (5-10 turns), manageable cost ($0.005-0.015/request)
- Negative consequences: Context truncation >50 messages, fixed window, no summarization
- Mitigation: 500-message limit + auto-archive reduces likelihood, FR-019 tracks long conversations, Phase V summarization

**ADR-0007: OpenAI Model Fallback GPT-4 to GPT-3.5-Turbo**
- Decision: Automatic fallback from GPT-4 (primary) to GPT-3.5-turbo on rate limits/errors
- Alternatives: GPT-4 only (rejected - violates SC-007), intelligent routing (rejected - complexity), user-configurable (rejected - out of scope), queueing (rejected - violates SC-001)
- Positive consequences: High availability (SC-007), cost optimization (10x cheaper fallback), simple implementation
- Negative consequences: Accuracy variance (GPT-3.5 ~85% vs GPT-4 ~95%), UX inconsistency, no user notification
- Mitigation: FR-019 tracks fallback rate + accuracy per model, alert if fallback >10%, Phase V user notification

All ADRs include:
- Explicit status (Accepted), date (2025-12-21), feature context
- Decision components with implementation details
- Positive/negative consequences with mitigation strategies
- 3-4 alternatives with rejection rationale and "when to revisit" guidance
- References to spec.md, plan.md, research.md, data-model.md
- Evaluator evidence (success criteria validation)

## Outcome

- ✅ Impact: 3 ADRs created documenting architecturally significant Phase III decisions - provides permanent record of why decisions were made, alternatives considered, and consequences accepted before implementation
- 🧪 Tests: ADR significance test PASSED (3/3 pass impact/alternatives/scope criteria), clustering check PASSED (decisions grouped appropriately), alternatives evaluation PASSED (3-4 alternatives per ADR), consequences analysis PASSED (positive/negative with mitigation)
- 📁 Files: ADR-0005 (MCP Server Architecture), ADR-0006 (Context Reconstruction), ADR-0007 (Model Fallback) - total 3 new ADRs in history/adr/ directory
- 🔁 Next prompts: All 6 recommended actions completed (implementation phasing, dependency graph, edge case logic, observability schema, frontend testing, ADRs) - ready for `/sp.tasks` to generate granular implementation tasks
- 🧠 Reflection: Constitutional ADR workflow executed successfully - identified decisions from planning artifacts, applied significance test, created comprehensive ADRs with alternatives and consequences, no conflicts with existing ADRs, all ADRs pass quality criteria (clustered, alternatives documented, consequences analyzed with mitigation)

## Evaluation notes (flywheel)

- Failure modes observed: Initial script call failed (wrong flag syntax --title vs expecting positional), resolved with correct --title flag; Stage "adr" not recognized by create-phr.sh, used "misc" stage successfully
- Graders run and results (PASS/FAIL): Significance test PASS (3/3 decisions pass all 3 criteria), Clustering check PASS (architectural clusters not atomic choices), Alternatives evaluation PASS (each ADR documents 3-4 alternatives with rationale), Consequences analysis PASS (positive/negative outcomes with mitigation strategies documented)
- Prompt variant (if applicable): /sp.adr (constitutional workflow) - architectural decision record creation per Principle (ADR documentation) from CLAUDE.md constitution
- Next experiment (smallest change to try): Proceed to /sp.tasks for task generation - use ADRs as input to implementation planning (reference ADR-0005 for MCP server deployment model, ADR-0006 for context reconstruction implementation, ADR-0007 for model fallback error handling logic), ensure tasks align with documented decisions and mitigation strategies
