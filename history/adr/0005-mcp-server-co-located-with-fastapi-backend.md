# ADR-0005: MCP Server Co-located with FastAPI Backend

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-21
- **Feature:** 004-phase-iii-ai-chatbot
- **Context:** Phase III requires 5 MCP (Model Context Protocol) tools to wrap Phase II TaskService for agentic AI interaction. Decision needed on MCP server deployment model: run in same FastAPI backend process vs deploy as separate service.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅ YES - Affects deployment model, scaling strategy, and debugging approach
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅ YES - 3 alternatives evaluated (same process, separate HTTP service, MCP SDK server wrapper)
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅ YES - Impacts deployment, testing, performance, maintenance
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

MCP server will run in the same FastAPI backend process (not as a separate service).

**Components**:
- MCP server initialization in `backend/src/mcp/server.py`
- Tool definitions in `backend/src/mcp/tools.py` (5 tools: add_task, list_tasks, complete_task, delete_task, update_task)
- Tool registration with agent service in `backend/src/main.py`
- Direct function calls to Phase II TaskService (no IPC/HTTP overhead)

**Deployment Model**: Single container/process deployment (FastAPI app with MCP server embedded)

## Consequences

### Positive

- **Simplicity**: No inter-process communication, no service discovery, no orchestration complexity
- **Performance**: Direct function calls (<1ms overhead) vs HTTP/gRPC latency (10-50ms per tool call)
- **Development speed**: Single codebase, single deployment, single debug session, easier testing
- **Cost**: No additional infrastructure (no separate containers, load balancers, service mesh)
- **Phase II reuse**: 100% reuse achieved (FR-007, SC-006) - MCP tools directly call TaskService methods
- **Stateless design compatibility**: MCP server is stateless (no in-memory state), aligns with Principle III

### Negative

- **Scaling granularity**: MCP server scales with entire backend (cannot scale independently if tool usage >> API usage)
- **Resource sharing**: MCP tools share CPU/memory with FastAPI routes (potential resource contention under high load)
- **Deployment coupling**: Cannot deploy MCP server updates without redeploying entire backend
- **Tooling ecosystem**: Less alignment with microservices patterns if scaling to 20+ tools in future phases

**Mitigation Strategies**:
- Stateless design enables horizontal scaling of entire backend (no session affinity required)
- Async operations prevent blocking (tools don't starve API routes)
- SC-005 target (100 concurrent conversations) achievable with 2-3 backend replicas
- Deferred to Phase IV/V: Separate MCP service if tool complexity increases (>10 tools) or scaling patterns diverge

## Alternatives Considered

**Alternative 1: Separate MCP Server Process (HTTP)**
- **Architecture**: MCP server as standalone FastAPI app, tools exposed via HTTP endpoints
- **Communication**: FastAPI backend → HTTP POST → MCP server → TaskService
- **Rejected because**:
  - Adds latency: HTTP roundtrip (10-50ms) for every tool call (affects SC-001: p95 <2s latency)
  - Requires service discovery: Load balancer, health checks, network policies
  - Increases operational complexity: 2 deployments, 2 container images, inter-service auth
  - Overkill for Phase III: 5 simple CRUD tools don't justify microservices overhead
- **When to revisit**: Phase IV/V if tool count >10 or tools have distinct resource profiles

**Alternative 2: MCP SDK Server Wrapper**
- **Architecture**: Official MCP SDK may provide server process abstraction
- **Evaluated**: MCP specification review shows SDK supports both in-process and server modes
- **Deferred because**:
  - Official Python MCP SDK still in beta (as of Dec 2025), API may change
  - In-process mode supported and simpler for Phase III scope
  - Will adapt based on SDK evolution and best practices
- **When to revisit**: If MCP SDK stabilizes with opinionated server pattern that provides clear benefits

**Alternative 3: Separate MCP Server Process (gRPC)**
- **Architecture**: MCP server as gRPC service, binary protocol for efficiency
- **Rejected because**:
  - Still adds IPC latency (5-15ms, better than HTTP but not zero)
  - Requires gRPC expertise, protobuf schema management
  - No significant benefit over in-process for 5 tools with simple I/O
- **When to revisit**: Never for Phase III scope; only if scaling to 50+ tools with high throughput

## References

- Feature Spec: [specs/004-phase-iii-ai-chatbot/spec.md](../../specs/004-phase-iii-ai-chatbot/spec.md) (FR-003, FR-007, FR-009)
- Implementation Plan: [specs/004-phase-iii-ai-chatbot/plan.md](../../specs/004-phase-iii-ai-chatbot/plan.md) (Phase 3.3: MCP Server)
- Research Document: [specs/004-phase-iii-ai-chatbot/research.md](../../specs/004-phase-iii-ai-chatbot/research.md) (R7: MCP Server Architecture, lines 129-145)
- Related ADRs: None (first MCP architecture decision)
- Evaluator Evidence: Decision validated against Principle IV (Smallest Viable Change), SC-006 (Zero Phase II backend changes), SC-001 (p95 <2s latency)
