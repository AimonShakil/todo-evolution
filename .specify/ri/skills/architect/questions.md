# Discovery Questions: Architect

**Version**: 1.0.0
**Created**: 2025-12-12
**Last Updated**: 2025-12-12

---

## Purpose

These questions guide the **architecture design** process. Use them to uncover:
- Technology stack choices with tradeoff analysis
- API contract specifications
- Data model designs with migrations
- Non-functional requirements (performance, security, reliability)
- Integration patterns and deployment strategies
- Risk mitigation and observability plans

---

## Question Categories

### 1. Technology Stack Questions 🛠️

**Purpose**: Select optimal technologies with clear rationale

#### Q1.1: What phase are we in?
- Phase I: Console (SQLite, Click CLI, simple)
- Phase II: Web (FastAPI, Next.js, Better Auth, Neon DB)
- Phase III: AI (MCP, OpenAI Agents)
- Phase IV: Kubernetes (Minikube, Helm)
- Phase V: Cloud (Kafka, Dapr, distributed)

**Why it matters**: Phase determines complexity, tech stack, and feature scope.

#### Q1.2: What are the framework requirements?
- **Backend**: FastAPI (async), Flask (sync), Django (batteries-included)?
- **Frontend**: Next.js 15 (SSR, RSC), React SPA, Vue, Svelte?
- **CLI**: Click (decorators), argparse (standard library)?
- **Rationale**: Match framework to phase requirements and constitutional principles

**Example Answers**:
- Phase I: Click CLI (simple, Pythonic)
- Phase II: FastAPI (async, OpenAPI, type-safe) + Next.js 15 (React 19, RSC)

#### Q1.3: What database technology fits?
- **Relational**: SQLite (Phase I), PostgreSQL (Phase II+), MySQL?
- **NoSQL**: MongoDB (document), Redis (cache), DynamoDB?
- **Managed vs Self-Hosted**: Neon DB, Supabase, RDS vs. self-managed?
- **ORM**: SQLModel (constitutional requirement), SQLAlchemy, Prisma?

**Tradeoff Criteria**:
- ACID guarantees needed?
- Query complexity (joins, transactions)?
- Scalability requirements (read/write throughput)?
- Operational complexity (backups, replication)?
- Cost (managed service vs. self-hosted)?

**Example Decision**:
```markdown
PostgreSQL (Neon DB) chosen over MongoDB:
- ✅ ACID guarantees (task completion consistency)
- ✅ Mature replication (Phase IV HA)
- ✅ SQLModel integration (constitutional ORM)
- ✅ Managed service (no ops overhead)
- ❌ Higher cost than self-hosted ($20/month vs. $0)
- ❌ Vendor lock-in (mitigated: standard PostgreSQL, easy migration)
```

#### Q1.4: What libraries are required?
- **Authentication**: Better Auth, NextAuth.js, Supabase Auth?
- **Validation**: Pydantic (constitutional), Zod (TypeScript)?
- **Testing**: pytest, Jest, Playwright?
- **Async**: asyncio, Celery, Bull queue?

**Constitutional Requirements**:
- Python 3.13+ (Principle III)
- Type hints everywhere (Principle IX)
- SQLModel ORM (Principle VI)
- Better Auth for Next.js (Principle XVI)

---

### 2. API Design Questions 🌐

**Purpose**: Define clear, versioned, idempotent API contracts

#### Q2.1: What are the API endpoints?
- List all operations (CRUD, business logic)
- Group by resource (tasks, users, auth)
- Define HTTP methods (GET, POST, PUT/PATCH, DELETE)

**Example**:
```
Tasks:
- POST   /api/{user_id}/tasks          (create)
- GET    /api/{user_id}/tasks          (list)
- GET    /api/{user_id}/tasks/{id}     (get)
- PATCH  /api/{user_id}/tasks/{id}     (update)
- DELETE /api/{user_id}/tasks/{id}     (delete)
```

#### Q2.2: What are the request/response schemas?
- Define exact JSON structure (all fields, types, constraints)
- Document optional vs required fields
- Specify default values
- Define validation rules (min/max length, regex, enum)

**Example**:
```json
POST /api/{user_id}/tasks
Request:
{
  "title": "string (1-200 chars, required)",
  "description": "string (0-2000 chars, optional)",
  "priority": "low|medium|high (optional, default: medium)"
}

Response (201 Created):
{
  "id": 123,
  "user_id": "alice",
  "title": "Buy groceries",
  "description": null,
  "priority": "medium",
  "completed": false,
  "created_at": "2025-12-12T10:30:00Z",
  "updated_at": "2025-12-12T10:30:00Z"
}
```

#### Q2.3: What is the error taxonomy?
- **4xx Client Errors**: 400 (bad request), 401 (unauthorized), 403 (forbidden), 404 (not found), 429 (rate limit)
- **5xx Server Errors**: 500 (internal error), 503 (service unavailable)
- **Error Response Format**: Consistent JSON structure with error code, message, details

**Example Error Response**:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Title must be 1-200 characters",
    "details": {
      "field": "title",
      "provided": "",
      "constraint": "min_length=1"
    }
  }
}
```

#### Q2.4: What are the API contracts for versioning, idempotency, timeouts?
- **Versioning**: URL versioning (/api/v1/), header versioning, no versioning (Phase I)?
- **Idempotency**: Which endpoints must be idempotent (PUT, DELETE)?
- **Timeouts**: Client timeout (30s), server timeout (60s)?
- **Retries**: Retry policy (exponential backoff, max 3 retries)?
- **Rate Limiting**: Requests per minute (100/min per user)?

**Example**:
```markdown
API Versioning: URL-based (/api/v1/) for clarity
Idempotency: PUT, DELETE safe to retry (idempotency keys for POST in Phase V)
Timeouts: Client 30s, server 60s
Rate Limiting: 100 req/min per user_id (429 status on exceed)
```

---

### 3. Data Modeling Questions 💾

**Purpose**: Design normalized, indexed, migration-ready schemas

#### Q3.1: What are the entities and relationships?
- Identify all domain entities (Task, User, Tag, etc.)
- Define relationships (one-to-many, many-to-many)
- Determine foreign keys and cascading deletes

**Example**:
```
User (1) ─── (many) Task
User (1) ─── (many) Tag
Task (many) ─── (many) Tag (via TaskTag join table)
```

#### Q3.2: What fields are required per entity?
- **Constitutional Fields** (all models): id, user_id, created_at, updated_at
- **Entity-Specific Fields**: title, description, priority, completed, etc.
- **Field Constraints**: NOT NULL, UNIQUE, CHECK, DEFAULT, min/max length

**Example**:
```python
class Task(SQLModel, table=True):
    # Constitutional required
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Task-specific
    title: str = Field(min_length=1, max_length=200)
    completed: bool = Field(default=False)
```

#### Q3.3: What indexes are needed for performance?
- **Primary Indexes**: id (always indexed)
- **Foreign Key Indexes**: user_id (always indexed for user isolation)
- **Query Indexes**: Identify common queries, add composite indexes
- **Unique Indexes**: Enforce uniqueness (e.g., username)

**Example**:
```sql
-- User isolation queries (most common)
INDEX idx_user_tasks (user_id, created_at DESC)

-- Priority sorting
INDEX idx_user_priority (user_id, priority, created_at DESC)

-- Completion filtering
INDEX idx_user_completed (user_id, completed, created_at DESC)
```

#### Q3.4: What is the migration strategy?
- **Phase I → Phase II**: SQLite to PostgreSQL (export/import script)
- **Schema Evolution**: Alembic migrations (Phase II+), version control
- **Rollback Strategy**: Test rollback, keep last 3 migrations
- **Data Retention**: How long to keep data (indefinitely unless user deletes)?

**Example**:
```markdown
Phase I → Phase II Migration:
1. Export SQLite: `sqlite3 todo.db .dump > tasks.sql`
2. Import to PostgreSQL: `psql -d todo_db -f tasks.sql`
3. Validate: Compare row counts, test queries
4. Rollback: Keep SQLite file as backup for 30 days

Schema Versioning (Phase II+):
- Alembic migrations in `migrations/versions/`
- Version format: `YYYYMMDD_HHMM_description.py`
- Always test rollback before deploying migration
```

---

### 4. Non-Functional Requirements (NFR) Questions ⚡

**Purpose**: Define measurable performance, security, reliability targets

#### Q4.1: What are the performance targets?
- **Latency**: p50, p95, p99 for each endpoint
- **Throughput**: Requests per second
- **Concurrent Users**: How many simultaneous users?
- **Data Volume**: How many tasks per user? Total users?

**Example**:
```markdown
Performance SLOs:
- API Latency: p50 <100ms, p95 <500ms, p99 <1s
- Throughput: 100 req/sec (Phase II), 1000 req/sec (Phase V)
- Concurrent Users: 10 (Phase I), 100 (Phase II), 10,000 (Phase V)
- Data Volume: 1000 tasks/user, 10,000 users (Phase II)
```

#### Q4.2: What are the security requirements?
- **Authentication**: How are users identified (JWT, session, API key)?
- **Authorization**: Who can access what (RBAC, ABAC, user-scoped)?
- **Data Protection**: Encryption at rest, in transit (TLS)?
- **Secrets Management**: How are secrets stored (.env, Vault, AWS Secrets)?
- **Input Validation**: Where is validation enforced (client, server, database)?
- **OWASP Top 10**: Which vulnerabilities apply (injection, XSS, CSRF)?

**Example**:
```markdown
Security Requirements:
- AuthN: JWT access tokens (1-hour expiry, HS256 signed)
- AuthZ: User-scoped (all queries filter by user_id)
- Encryption: TLS 1.3 in transit, no encryption at rest (Phase I/II)
- Secrets: .env (Phase I), AWS Secrets Manager (Phase V)
- Validation: Server-side (FastAPI + Pydantic), database constraints
- OWASP: Mitigate injection (ORM prevents SQL injection), CSRF (SameSite cookies)
```

#### Q4.3: What are the reliability requirements?
- **Uptime SLO**: 99%, 99.9%, 99.99%?
- **Error Budget**: How much downtime is acceptable per month?
- **Degraded Mode**: What happens when dependencies fail (database, external API)?
- **Rollback Strategy**: How to roll back bad deploys (blue-green, canary)?

**Example**:
```markdown
Reliability SLOs:
- Uptime: 99.9% (43 minutes downtime/month)
- Error Budget: 0.1% of requests can fail
- Degraded Mode: Return cached data if database unavailable (stale-while-revalidate)
- Rollback: Blue-green deployment (keep old version running, switch traffic on success)
```

#### Q4.4: What are the cost constraints?
- **Infrastructure Cost**: Cloud services, managed databases, CDN
- **Operational Cost**: DevOps time, monitoring tools
- **Scalability Cost**: Cost per user, cost per request
- **Budget**: What's the monthly budget (Phase I: $0, Phase II: $50, Phase V: $500)?

**Example**:
```markdown
Cost Targets:
- Phase I: $0 (local SQLite, no cloud)
- Phase II: <$50/month (Neon DB $20, Vercel $20, monitoring $10)
- Phase V: <$500/month (managed Kafka, Dapr, multi-region)
Unit Economics: <$0.01 per user per month (1000 users = $10/month)
```

---

### 5. Integration & Deployment Questions 🚀

**Purpose**: Plan external integrations, containerization, orchestration

#### Q5.1: What external dependencies exist?
- External APIs (OpenAI, Stripe, SendGrid)?
- Message queues (Kafka, RabbitMQ, SQS)?
- Caches (Redis, Memcached)?
- What happens if dependencies fail (timeout, retry, circuit breaker)?

**Example**:
```markdown
External Dependencies (Phase III):
- OpenAI API: GPT-4 for task suggestions (timeout: 30s, retry: 3x exponential backoff)
- Fallback: If OpenAI unavailable, disable AI features, show cached suggestions
- Circuit Breaker: After 5 consecutive failures, stop calling for 5 minutes
```

#### Q5.2: What is the deployment architecture?
- **Containerization**: Docker (Dockerfile), Podman?
- **Orchestration**: Kubernetes (Minikube, EKS), Docker Compose, systemd?
- **CI/CD**: GitHub Actions, GitLab CI, Jenkins?
- **Environment Management**: Dev, staging, production (separate databases)?

**Example**:
```markdown
Deployment (Phase IV):
- Containerization: Docker (multi-stage builds for size)
- Orchestration: Kubernetes (Minikube local, EKS production)
- CI/CD: GitHub Actions (lint → test → build → deploy)
- Environments: Dev (local), Staging (Minikube), Prod (EKS)
```

#### Q5.3: What is the observability strategy?
- **Logging**: Structured JSON logs (info, warn, error levels)
- **Metrics**: Prometheus, CloudWatch, Datadog?
- **Tracing**: OpenTelemetry, Jaeger, Zipkin?
- **Alerting**: PagerDuty, Slack, email on SLO violations?

**Example**:
```markdown
Observability:
- Logging: Structured JSON (timestamp, level, message, user_id, request_id)
- Metrics: Prometheus (request_count, latency_histogram, error_rate)
- Tracing: OpenTelemetry (trace_id across services, Phase IV+)
- Alerting: Slack webhook when p95 latency >1s or error rate >5%
```

#### Q5.4: What is the rollback plan?
- **Database Migrations**: Test rollback, keep migration history
- **Feature Flags**: Enable/disable features without redeploy
- **Canary Deploys**: Roll out to 10% traffic, monitor, proceed or rollback
- **Rollback Time**: How fast can we rollback (1 minute, 10 minutes, 1 hour)?

**Example**:
```markdown
Rollback Strategy:
- Database: Test all migrations rollback in staging before production
- Feature Flags: LaunchDarkly (toggle features in <1 minute)
- Deployment: Blue-green (keep old version running, instant switch on failure)
- Rollback SLO: <5 minutes from detection to rollback
```

---

### 6. Risk & Architectural Decision Questions ⚠️

**Purpose**: Identify failure modes, mitigate risks, document decisions

#### Q6.1: What are the top 3 risks?
- Technical risks (scalability bottlenecks, single points of failure)
- Operational risks (deployment failures, data loss, security breaches)
- Business risks (vendor lock-in, cost overruns, timeline delays)

**Example**:
```markdown
Top 3 Risks:
1. **Database Bottleneck** (Phase II):
   - Risk: PostgreSQL can't handle 1000 concurrent users
   - Likelihood: Medium | Impact: High
   - Mitigation: Read replicas (Phase IV), Redis cache (90% hit rate)

2. **Vendor Lock-in** (Neon DB):
   - Risk: Neon DB price increases or service shuts down
   - Likelihood: Low | Impact: Medium
   - Mitigation: Use standard PostgreSQL (easy migration to RDS/self-hosted)

3. **JWT Secret Compromise**:
   - Risk: Attacker gains access to JWT signing secret
   - Likelihood: Low | Impact: Critical
   - Mitigation: Rotate secrets monthly, use AWS Secrets Manager (Phase V)
```

#### Q6.2: What failure modes exist?
- What happens if database is down?
- What happens if external API is slow?
- What happens under high load (traffic spike)?
- What is the blast radius (entire system, one feature, one user)?

**Example**:
```markdown
Failure Modes:
1. **Database Down**:
   - Blast Radius: Entire application (no read/write)
   - Detection: Health check fails after 3 consecutive timeouts (15s)
   - Recovery: Auto-restart database, alert on-call (PagerDuty)
   - Mitigation: Database replication (Phase IV), read-only mode from replica

2. **OpenAI API Slow** (Phase III):
   - Blast Radius: AI features only (task suggestions)
   - Detection: p95 latency >5s for OpenAI calls
   - Recovery: Circuit breaker (stop calling after 5 failures)
   - Mitigation: Show cached suggestions, degrade gracefully
```

#### Q6.3: Which decisions require ADRs?
Test each significant decision with 3-part criteria:
- **Impact**: Long-term consequences (framework, data model, platform)?
- **Alternatives**: Multiple viable options with tradeoffs?
- **Scope**: Cross-cutting, influences system design?

**If ALL true, create ADR**

**Example Decisions Requiring ADRs**:
- Database choice (PostgreSQL vs. MongoDB) → YES (impact: data model, alternatives: multiple, scope: entire backend)
- Authentication library (Better Auth vs. NextAuth.js) → YES
- CLI framework (Click vs. argparse) → NO (low impact, limited scope)

#### Q6.4: What's the migration path across phases?
- Phase I → Phase II: SQLite to PostgreSQL, CLI to REST API
- Phase II → Phase III: Add AI features (backward compatible)
- Phase IV → Phase V: Monolith to microservices, local to cloud
- Is the data model forward-compatible?

**Example**:
```markdown
Migration Path:
Phase I → Phase II:
- Data: Export SQLite to PostgreSQL (script provided)
- Architecture: SQLModel ORM unchanged (same models, different engine)
- API: CLI commands map to REST endpoints (same business logic)

Phase II → Phase III (backward compatible):
- Data: Add `ai_suggestions` table (no changes to `tasks`)
- API: Add `/api/ai/suggest` endpoint (existing endpoints unchanged)

Phase IV → Phase V (microservices):
- Data: Partition by user_id (shard key), replicate across regions
- Architecture: Extract AI service (separate container, async communication)
```

---

## Question Sequencing Strategy

**Start with constraints, then design outward**:

1. **Technology Stack** (Q1) → Understand phase, frameworks, database
2. **API Design** (Q2) → Define contracts before implementation
3. **Data Modeling** (Q3) → Schema drives application logic
4. **NFRs** (Q4) → Quantify performance, security, reliability
5. **Integration** (Q5) → Plan deployment, observability, rollback
6. **Risks** (Q6) → Identify failures, document decisions

**Example Flow**:
```
Spec Writer: "Users need task priorities (P2)"
  ↓
You: Q1.4 - "What phase?" → Phase I (console)
  ↓
You: Q3.2 - "Add priority field to Task model (low/medium/high enum)"
  ↓
You: Q3.3 - "Index needed: (user_id, priority, created_at DESC)"
  ↓
You: Q4.1 - "Performance target: Sort by priority <100ms (p95)"
  ↓
You: Q2.1 - "CLI command: todo list --priority high"
  ↓
Write plan.md with architecture decisions
```

---

## Anti-Patterns to Avoid

### ❌ Asking About Implementation Details
**Problem**: "How should we implement the caching layer?" (too detailed)
**Fix**: "What performance targets require caching?" (architecture-level)

### ❌ Technology Without Rationale
**Problem**: "Should we use GraphQL?" (no context)
**Fix**: "What are the API complexity requirements? Does REST suffice or do we need GraphQL?" (requirements-driven)

### ❌ Skipping Alternatives
**Problem**: "We'll use PostgreSQL" (no justification)
**Fix**: "PostgreSQL vs. MongoDB: Which better fits our data model and query patterns?" (compare alternatives)

### ❌ Vague NFRs
**Problem**: "System should be fast" (unmeasurable)
**Fix**: "What are acceptable p95 latencies for each endpoint?" (quantify)

---

## Related Files

- **persona.md**: Role, expertise, communication style
- **principles.md**: Design principles and decision frameworks
- **README.md**: Aggregated P+Q+P guide with examples

## Version History

### v1.0.0 (2025-12-12)
- Initial question framework for Architect
- Organized into 6 categories (Technology, API, Data, NFRs, Integration, Risks)
- Added ADR detection criteria (3-part test)
- Documented sequencing strategy and anti-patterns
