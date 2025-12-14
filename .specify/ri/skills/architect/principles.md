# Design Principles: Architect

**Version**: 1.0.0
**Created**: 2025-12-12
**Last Updated**: 2025-12-12

---

## Purpose

These principles guide **architectural decision-making** when creating plan.md. They ensure:
- Constitutional compliance (all 28 principles)
- Technology choices with clear rationale
- Measurable NFRs (performance, security, reliability)
- Risk-aware design (failure modes, mitigations)
- Forward compatibility (phase evolution)

---

## 1. Architectural Decision Standards

### 1.1 Technology Selection Standard
**Principle**: Every technology choice has documented alternatives, tradeoffs, and rationale.

**Verification Checklist**:
- [ ] At least 2 alternatives considered (incumbent vs. new)
- [ ] Tradeoffs documented (performance, complexity, cost, maturity)
- [ ] Rationale explains WHY chosen (ties to requirements, constraints)
- [ ] Phase appropriateness validated (not over/under-engineered)
- [ ] Constitutional alignment checked (ORM, auth, type safety)

**Decision Template**:
```markdown
## Technology: [Component Name]

### Options Considered:
1. **[Option A]** - [Brief description]
2. **[Option B]** - [Brief description]
3. **[Option C]** - [Brief description]

### Decision: [Chosen Option]
**Rationale**:
- [Requirement 1]: [How option satisfies]
- [Requirement 2]: [How option satisfies]

**Trade-offs**:
- ✅ [Pro 1]: [Benefit]
- ✅ [Pro 2]: [Benefit]
- ❌ [Con 1]: [Drawback] — Mitigation: [How we address]
- ❌ [Con 2]: [Drawback] — Acceptable because: [Justification]

**Constitutional Alignment**:
- Principle [N]: [How this choice enforces principle]

**ADR**: [Link if significant decision]
```

**Example**:
```markdown
## Database: PostgreSQL (Neon DB)

### Options Considered:
1. **SQLite** (Phase I incumbent)
2. **PostgreSQL (Neon DB)** (managed cloud)
3. **MongoDB Atlas** (NoSQL managed)

### Decision: PostgreSQL (Neon DB)
**Rationale**:
- Spec requires ACID guarantees (task completion consistency)
- Constitutional Principle VI: SQLModel ORM (PostgreSQL-native)
- Phase II scalability: Multi-user web app (SQLite single-file limitation)

**Trade-offs**:
- ✅ ACID guarantees (vs. MongoDB eventual consistency)
- ✅ Managed service (no ops overhead vs. self-hosted)
- ✅ Mature replication (Phase IV HA support)
- ❌ Higher cost ($20/month vs. $0 SQLite) — Acceptable for Phase II production
- ❌ Vendor lock-in (Neon DB) — Mitigated: Standard PostgreSQL, easy migration

**Constitutional Alignment**:
- Principle VI: SQLModel ORM ✅ (PostgreSQL dialect)
- Principle XVIII: Performance ✅ (connection pooling, indexes)

**ADR**: See `history/adr/004-database-postgresql-neon.md`
```

### 1.2 ADR (Architectural Decision Record) Standard
**Principle**: Significant decisions documented with alternatives, consequences, and reversibility.

**3-Part Test for ADR Significance**:
1. **Impact**: Does this have long-term consequences? (framework, data model, platform)
2. **Alternatives**: Were multiple viable options considered?
3. **Scope**: Is this cross-cutting or does it influence system design?

**If ALL three are true → Create ADR**

**ADR Template**:
```markdown
# ADR [N]: [Decision Title]

**Status**: Accepted | Proposed | Deprecated | Superseded by ADR-[X]
**Date**: YYYY-MM-DD
**Deciders**: [Names or roles]
**Context**: [Phase, feature, requirement]

## Context and Problem Statement
[What is the issue we're trying to address?]

## Decision Drivers
- [Driver 1: requirement, constraint, or goal]
- [Driver 2]
- [Driver 3]

## Considered Options
1. **[Option A]**
2. **[Option B]**
3. **[Option C]**

## Decision Outcome
**Chosen option**: "[Option]"

**Rationale**:
- [Reason 1]
- [Reason 2]

### Positive Consequences
- [Benefit 1]
- [Benefit 2]

### Negative Consequences
- [Drawback 1] — Mitigation: [How we address]
- [Drawback 2] — Acceptable because: [Justification]

## Alternatives Analysis

### Option A: [Name]
- **Pros**: [List benefits]
- **Cons**: [List drawbacks]
- **Why not chosen**: [Reason]

### Option B: [Name]
- **Pros**: [List benefits]
- **Cons**: [List drawbacks]
- **Why not chosen**: [Reason]

## Links
- **Spec**: `specs/[feature]/spec.md`
- **Plan**: `specs/[feature]/plan.md`
- **Related ADRs**: ADR-[X], ADR-[Y]
```

**Example ADRs**:
- ADR-001: Python 3.13+ (constitutional requirement)
- ADR-002: SQLModel ORM (constitutional requirement)
- ADR-003: Better Auth for Next.js (authentication)
- ADR-004: PostgreSQL (Neon DB) for Phase II (database)
- ADR-005: Click CLI framework for Phase I (CLI)

**Non-ADR Decisions** (too small, localized):
- Variable naming conventions (covered by Principle IX)
- Test file organization (covered by test standards)
- Logging format (unless distributed tracing involved)

---

## 2. API Design Principles

### 2.1 RESTful Contract Standard
**Principle**: All APIs follow REST conventions with explicit contracts.

**REST Conventions**:
- **GET**: Read (idempotent, cacheable, no side effects)
- **POST**: Create (not idempotent)
- **PUT/PATCH**: Update (PUT = full replace, PATCH = partial update, both idempotent)
- **DELETE**: Delete (idempotent)

**HTTP Status Codes**:
- **2xx Success**: 200 OK, 201 Created, 204 No Content
- **4xx Client Error**: 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 429 Too Many Requests
- **5xx Server Error**: 500 Internal Server Error, 503 Service Unavailable

**Endpoint Naming**:
```
✅ GOOD:
- GET    /api/{user_id}/tasks          (list tasks)
- POST   /api/{user_id}/tasks          (create task)
- GET    /api/{user_id}/tasks/{id}     (get task)
- PATCH  /api/{user_id}/tasks/{id}     (update task)
- DELETE /api/{user_id}/tasks/{id}     (delete task)

❌ BAD:
- GET  /api/getTasks                   (verb in URL)
- POST /api/tasks/create               (redundant /create)
- GET  /api/{user_id}/tasks/{id}/view  (redundant /view)
```

### 2.2 User Isolation Standard (CRITICAL)
**Principle**: All API endpoints scoped by user_id to enforce data isolation (Constitutional Principle II).

**Pattern**:
```
✅ GOOD: /api/{user_id}/tasks
- user_id in path enforces scoping
- All queries filter by user_id
- 404 Not Found for cross-user access attempts (not 401/403 to avoid info disclosure)

❌ BAD: /api/tasks?user_id={user_id}
- user_id in query param (can be manipulated)
- Does not enforce scoping at route level
```

**Implementation**:
```python
@router.get("/api/{user_id}/tasks")
async def list_tasks(
    user_id: str,
    current_user: User = Depends(get_current_user)
):
    # CRITICAL: Verify current_user matches user_id
    if current_user.id != user_id:
        raise HTTPException(404, "Not found")  # Not 403 (info disclosure)

    # Query automatically scoped by user_id
    tasks = await session.exec(
        select(Task).where(Task.user_id == user_id)
    ).all()
    return tasks
```

### 2.3 Error Response Standard
**Principle**: Consistent, typed error responses with actionable messages.

**Error Response Format**:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Title must be 1-200 characters",
    "details": {
      "field": "title",
      "provided": "",
      "constraint": "min_length=1"
    },
    "timestamp": "2025-12-12T10:30:00Z",
    "request_id": "abc123"
  }
}
```

**Error Codes** (typed enum):
```python
class ErrorCode(str, Enum):
    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    UNAUTHORIZED = "UNAUTHORIZED"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    INTERNAL_ERROR = "INTERNAL_ERROR"
```

### 2.4 Versioning & Idempotency Standard
**Principle**: APIs versioned for backward compatibility, idempotent where applicable.

**Versioning**:
```
Phase I: No versioning (console app, no API)
Phase II: /api/v1/{user_id}/tasks (URL versioning)
Phase V: /api/v2/{user_id}/tasks (breaking changes, maintain v1 for 6 months)
```

**Idempotency**:
```
✅ Idempotent (safe to retry):
- GET, PUT, DELETE (same result on multiple calls)
- POST with idempotency key (Phase V: `Idempotency-Key` header)

❌ Not Idempotent:
- POST without idempotency key (creates duplicate resources)
```

---

## 3. Data Modeling Principles

### 3.1 Constitutional Fields Standard (MANDATORY)
**Principle**: All database models include required fields per Constitutional Principle VI.

**Required Fields**:
```python
class [Entity](SQLModel, table=True):
    # REQUIRED (Constitutional Principle VI)
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, max_length=255)  # CRITICAL: User isolation
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Entity-specific fields
    [additional fields...]
```

**Validation**:
- ✅ All models have id, user_id, created_at, updated_at
- ✅ user_id always indexed (performance for isolation queries)
- ✅ updated_at auto-updates on modification (validator or database trigger)

### 3.2 Index Strategy Standard
**Principle**: Indexes optimized for query patterns, especially user_id filtering.

**Required Indexes**:
1. **Primary Key**: id (auto-indexed)
2. **User Isolation**: user_id (MANDATORY for all queries)
3. **Query-Specific**: Based on common WHERE, ORDER BY, JOIN clauses

**Index Naming**:
```sql
-- Pattern: idx_{table}_{columns}
INDEX idx_tasks_user_created (user_id, created_at DESC)
INDEX idx_tasks_user_priority (user_id, priority, created_at DESC)
INDEX idx_tasks_user_completed (user_id, completed, created_at DESC)
```

**Index Guidelines**:
- Single-column user_id index for simple filtering
- Composite indexes for multi-column queries (user_id always first)
- DESC for timestamp sorting (most recent first)
- Max 5 indexes per table (trade-off: read speed vs. write overhead)

### 3.3 Normalization Standard
**Principle**: Data normalized to 3NF (Third Normal Form) unless denormalization justified.

**Normalization Rules**:
- **1NF**: Atomic values (no arrays in columns)
- **2NF**: No partial dependencies (all non-key fields depend on entire primary key)
- **3NF**: No transitive dependencies (non-key fields depend only on primary key)

**When to Denormalize** (must document in ADR):
- Read-heavy queries (cache frequently joined data)
- Performance requirements not met by normalized schema (document metrics)
- Acceptable staleness (denormalized data updated async)

**Example**:
```markdown
Normalized (3NF):
- User: id, username, email
- Task: id, user_id (FK), title, completed

Denormalized (if justified):
- Task: id, user_id, username (denormalized), title, completed
- Justification: 90% of queries need username (avoid JOIN)
- Trade-off: Update username in 2 tables (acceptable, usernames rarely change)
- ADR: See `history/adr/006-denormalize-username.md`
```

### 3.4 Migration Strategy Standard
**Principle**: All schema changes versioned with tested rollback.

**Migration Workflow**:
1. **Write migration**: Alembic auto-generate or manual
2. **Test rollback**: Ensure migration can be reversed
3. **Review**: Check for data loss, locking issues
4. **Deploy**: Apply migration in staging, then production
5. **Monitor**: Watch for query performance degradation

**Migration Template** (Alembic):
```python
"""Add priority field to tasks

Revision ID: 20251212_1030
Revises: 20251211_1500
Create Date: 2025-12-12 10:30:00
"""

def upgrade():
    op.add_column('tasks', sa.Column('priority', sa.String(10), nullable=False, server_default='medium'))
    op.create_index('idx_tasks_user_priority', 'tasks', ['user_id', 'priority', 'created_at'])

def downgrade():
    op.drop_index('idx_tasks_user_priority', table_name='tasks')
    op.drop_column('tasks', 'priority')
```

**Rollback Testing**:
```bash
# Test migration forward
alembic upgrade head

# Test rollback
alembic downgrade -1

# Verify data integrity
SELECT COUNT(*) FROM tasks WHERE priority IS NULL;  # Should be 0
```

---

## 4. Non-Functional Requirements (NFR) Principles

### 4.1 Performance SLO Standard
**Principle**: All performance requirements quantified with p50, p95, p99 latencies.

**SLO Template**:
```markdown
Performance Targets:
- **Latency**: p50 <[X]ms, p95 <[Y]ms, p99 <[Z]ms
- **Throughput**: [N] req/sec
- **Concurrent Users**: [M] simultaneous users
- **Data Volume**: [K] records per user, [L] total users
```

**Phase-Specific Targets**:
```markdown
Phase I (Console):
- CLI command latency: p95 <100ms (local SQLite)
- Data volume: 1000 tasks/user

Phase II (Web):
- API latency: p50 <100ms, p95 <500ms, p99 <1s
- Throughput: 100 req/sec
- Concurrent users: 100
- Data volume: 10,000 users, 1000 tasks/user

Phase V (Cloud):
- API latency: p50 <50ms, p95 <200ms, p99 <500ms
- Throughput: 10,000 req/sec
- Concurrent users: 100,000
- Data volume: 1M users, 1000 tasks/user
```

### 4.2 Security Requirements Standard
**Principle**: Security layered (defense in depth) with explicit AuthN, AuthZ, encryption, validation.

**Security Checklist**:
- [ ] **Authentication**: How users identified (JWT, session, API key)?
- [ ] **Authorization**: Who can access what (RBAC, user-scoped)?
- [ ] **Encryption**: TLS 1.3 in transit, at-rest encryption (if sensitive data)?
- [ ] **Secrets**: How managed (.env, AWS Secrets, Vault)?
- [ ] **Input Validation**: Server-side (never trust client)
- [ ] **Rate Limiting**: Prevent abuse (100 req/min per user)
- [ ] **OWASP Top 10**: Mitigations documented

**Example**:
```markdown
Security Architecture:
- **AuthN**: JWT access tokens (1-hour expiry, HS256 signed)
- **AuthZ**: User-scoped (all queries filter by user_id from JWT claims)
- **Encryption**: TLS 1.3 in transit (Let's Encrypt), no at-rest (no PII)
- **Secrets**: .env (Phase I), AWS Secrets Manager (Phase V)
- **Validation**: FastAPI + Pydantic (server-side), database constraints
- **Rate Limiting**: 100 req/min per user_id (429 status on exceed)
- **OWASP**:
  - Injection: SQLModel ORM (parameterized queries)
  - XSS: React auto-escapes (Next.js)
  - CSRF: SameSite=Strict cookies
```

### 4.3 Reliability SLO Standard
**Principle**: Uptime, error budget, degraded mode, rollback defined.

**SLO Template**:
```markdown
Reliability Targets:
- **Uptime SLO**: [X]% (e.g., 99.9% = 43 min downtime/month)
- **Error Budget**: [Y]% of requests can fail
- **Degraded Mode**: [What happens when dependencies fail]
- **Rollback Time**: <[Z] minutes from detection to rollback
```

**Example**:
```markdown
Reliability (Phase II):
- **Uptime SLO**: 99.9% (43 min downtime/month)
- **Error Budget**: 0.1% of requests (e.g., 100/100,000 can fail)
- **Degraded Mode**: If Neon DB unavailable, return cached tasks (stale-while-revalidate)
- **Rollback**: <5 minutes (blue-green deployment, instant traffic switch)
```

### 4.4 Observability Standard
**Principle**: Structured logging, metrics, tracing, alerting for SLO monitoring.

**Observability Stack**:
```markdown
Logging:
- Format: Structured JSON (timestamp, level, message, user_id, request_id, trace_id)
- Levels: DEBUG (dev), INFO (prod), WARN, ERROR
- Retention: 30 days (Phase II), 90 days (Phase V)

Metrics (Prometheus):
- request_count (counter, labels: endpoint, status_code)
- request_latency_seconds (histogram, labels: endpoint)
- active_users (gauge)
- error_rate (counter, labels: error_code)

Tracing (OpenTelemetry, Phase IV+):
- trace_id across services
- span_id per operation
- Exported to Jaeger (distributed tracing)

Alerting (Slack webhook):
- p95 latency >1s for 5 minutes → WARN
- Error rate >5% for 5 minutes → CRITICAL
- Uptime <99.9% in 24 hours → CRITICAL
```

---

## 5. Phase Evolution Principles

### 5.1 Forward Compatibility Standard
**Principle**: Architecture decisions enable smooth phase transitions (no rewrites).

**Phase Transition Checklist**:
- [ ] **Data Model**: Schema compatible across phases (same SQLModel classes)
- [ ] **Business Logic**: Reusable (extract to services, not tied to CLI/API)
- [ ] **Configuration**: Environment-based (dev, staging, prod separate)
- [ ] **Migration Path**: Documented (scripts, validation steps)

**Example**:
```markdown
Phase I → Phase II Compatibility:
- ✅ SQLModel ORM: Same models, different engine (SQLite → PostgreSQL)
- ✅ Business Logic: Extract to `services/task_service.py` (reused by CLI and API)
- ✅ Data Migration: Script: `scripts/migrate_sqlite_to_postgres.sh`
- ✅ Tests: Same test suite (swap database fixture)
```

### 5.2 Evolutionary Architecture Standard
**Principle**: Start simple, add complexity as requirements grow (no premature optimization).

**Phase Appropriateness**:
```markdown
Phase I (Console):
- Architecture: Monolith CLI (single process, SQLite)
- Rationale: Single-user local app, no need for client-server

Phase II (Web):
- Architecture: Monolith web app (FastAPI + Next.js, PostgreSQL)
- Rationale: Multi-user, need REST API, still manageable as monolith

Phase IV (Kubernetes):
- Architecture: Monolith in containers (Docker, K8s orchestration)
- Rationale: Scaling via replicas, not microservices (yet)

Phase V (Cloud):
- Architecture: Microservices (API gateway, task service, AI service, Kafka events)
- Rationale: Distributed requirements (event-driven, multi-region, independent scaling)
```

**Anti-Pattern**:
```markdown
❌ Phase I with microservices:
- Problem: Over-engineered (single user doesn't need distributed architecture)
- Cost: Complexity (Docker Compose, service discovery, network overhead)

✅ Phase I monolith:
- Right-sized: SQLite + Click CLI (appropriate for phase)
- Evolution: Extract services in Phase V when requirements justify
```

---

## 6. Constitutional Alignment (All 28 Principles)

### Critical Principles for Architecture:

#### Principle I: Spec-Driven Development
- **Enforcement**: Architecture creates plan.md only after spec.md exists
- **Validation**: Every architectural decision traces to a requirement in spec.md

#### Principle II: User Data Isolation
- **Enforcement**: All queries filter by user_id, indexes include user_id
- **Validation**: Security audit checks for cross-user data access vulnerabilities

#### Principle VI: Database Standards
- **Enforcement**: All models include id, user_id, created_at, updated_at
- **Validation**: Schema review ensures constitutional fields present

#### Principle IX: Code Quality
- **Enforcement**: Architecture enables type safety (Pydantic, TypeScript strict)
- **Validation**: Linter enforces type hints, mypy checks pass

#### Principle X: Testing Requirements
- **Enforcement**: Architecture supports dependency injection (mocking, 80% coverage)
- **Validation**: Coverage report ≥80%

#### Principle XII: Security
- **Enforcement**: AuthN/AuthZ defined, secrets management planned, OWASP mitigations
- **Validation**: Security audit before deployment

#### Principle XVIII: Performance
- **Enforcement**: Measurable SLOs (p95 latency), monitoring strategy
- **Validation**: Load testing confirms SLO compliance

---

## 7. Anti-Patterns (AVOID)

### ❌ Resume-Driven Development
**Problem**: Choosing trendy tech without rationale
**Example**: "Use GraphQL because it's modern"
**Fix**: Document why GraphQL over REST (complex client queries? multiple endpoints? data over-fetching?)

### ❌ Premature Optimization
**Problem**: Designing for massive scale when not needed
**Example**: "Phase I console app needs Kafka and Redis"
**Fix**: Start simple (SQLite), add complexity when requirements justify (Phase V)

### ❌ Vague NFRs
**Problem**: Unmeasurable targets
**Example**: "System should be fast and reliable"
**Fix**: "p95 latency <500ms, 99.9% uptime SLO"

### ❌ Missing ADRs
**Problem**: Significant decisions undocumented
**Example**: Switching frameworks without rationale
**Fix**: Create ADR for all decisions passing 3-part test (impact, alternatives, scope)

### ❌ Ignoring Migration Paths
**Problem**: No plan for phase transitions
**Example**: "Phase I uses custom binary format (incompatible with PostgreSQL)"
**Fix**: Use SQLite (compatible schema with PostgreSQL, easy migration)

---

## Version History

### v1.0.0 (2025-12-12)
- Initial principles for Architect
- Established technology selection, ADR, API design standards
- Defined data modeling, NFR, phase evolution principles
- Documented constitutional alignment and anti-patterns

---

## Related Files

- **persona.md**: Role, expertise, communication style
- **questions.md**: Architecture discovery questions
- **README.md**: Aggregated P+Q+P guide with examples
