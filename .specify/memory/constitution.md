<!--
  SYNC IMPACT REPORT

  Version Change: template → 1.0.0 → 1.1.0

  Improvements in v1.1.0 (2025-12-06):
  ════════════════════════════════════

  VAGUE STANDARDS MADE TESTABLE:
  - I. Spec-Driven Development: Added "Permitted Manual Edits" exceptions and "Verification" section
  - II. User Data Isolation: Added "Testable Verification" with specific integration tests
  - IX. Code Quality Standards: Added "Verified by" for each requirement (mypy, pydocstyle, flake8, etc.)
  - X. Testing Requirements: Added specific coverage commands, CI/CD gates, required test categories
  - XIV → XVIII. Performance Standards: Added measurable SLOs (p95 < 500ms under 100 users, 1000 tasks)
    and specific verification tools (Lighthouse CI, pytest performance tests)

  NEW PRINCIPLES ADDED (Missing Categories):
  - XI. Data Privacy & Retention (GDPR-Aligned) - export, deletion, audit logging
  - XIII. Dependency Security & Updates - npm audit, pip-audit, CVE patching SLAs
  - XV. API Rate Limiting - 100 req/min, 429 responses, rate limit headers
  - XVII. Frontend Accessibility & Responsiveness - WCAG 2.1 AA, Lighthouse ≥90, responsive breakpoints
  - XX. Database Backup & Disaster Recovery - RTO < 4hr, RPO < 24hr, monthly restore tests

  UNREALISTIC CONSTRAINTS FIXED:
  - I. Spec-Driven Development: Changed "NO code may be written manually" to "Application code generation"
    with explicit exceptions (config, docs, hotfixes, test data, CI/CD)
  - II. User Data Isolation: Added exception "(except system/admin tables)" for database queries

  RENUMBERED PRINCIPLES (due to additions):
  - XI → XII: Security Principles (NON-NEGOTIABLE)
  - XII → XIV: Authentication & Authorization
  - XIII → XVI: Error Handling & Logging
  - XIV → XVIII: Performance Standards
  - XV → XIX: Monitoring & Observability
  - XVI → XXI: Event-Driven Architecture (Phase V)
  - XVII → XXII: Dapr Integration (Phase V)
  - XVIII → XXIII: Containerization Standards
  - XIX → XXIV: Kubernetes & Helm Standards
  - XX → XXV: CI/CD Pipeline Standards
  - XXI → XXVI: Conversation Persistence (Phase III)
  - XXII → XXVII: Documentation Standards
  - XXIII → XXVIII: Git & Version Control

  Total Principles: 28 (was 23 in v1.0.0)

  Sections Added:
  - Technology Stack Requirements (Non-Negotiable)
  - Phase Progression & Feature Levels
  - Monorepo Structure Standards
  - Development Environment Requirements
  - Deployment Targets

  Templates Requiring Updates:
  ✅ .specify/templates/spec-template.md - Reviewed, compatible
  ✅ .specify/templates/plan-template.md - Reviewed, Constitution Check section aligns
  ✅ .specify/templates/tasks-template.md - Reviewed, task organization aligns

  Follow-up TODOs: None
-->

# Evolution of Todo Constitution

**Project**: Evolution of Todo - 5-Phase Cloud-Native AI System

**Mission**: Build production-quality software that evolves from a simple Python console app
to a distributed, cloud-native, AI-powered system deployed on Kubernetes with event-driven
architecture, using spec-driven development with Claude Code and Spec-Kit Plus.

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)

Every feature MUST begin with a specification. Application code generation is performed by
Claude Code based on refined specifications.

**Requirements**:
- MUST write spec.md before any application code
- Every feature requires: spec.md → plan.md → tasks.md workflow
- Specifications must be iteratively refined until Claude Code generates correct output
- Constitution lives at `.specify/memory/constitution.md`
- PHR (Prompt History Record) MUST be created after EVERY user interaction
- ADR (Architecture Decision Record) suggestions (never auto-create) for significant
  architectural decisions

**Permitted Manual Edits** (exceptions to spec-driven approach):
- Configuration files (YAML, JSON, .env.example, Dockerfiles)
- Documentation (README.md, comments, ADRs, PHRs)
- Emergency hotfixes (must be followed by spec update and regeneration)
- Test fixtures and mock data
- CI/CD workflow definitions

**Verification**: Each feature MUST have corresponding spec.md, plan.md, and tasks.md files
in `specs/<feature>/` directory.

**Rationale**: Spec-driven development ensures clear requirements, reduces ambiguity,
enables AI-assisted code generation, and creates a traceable artifact trail for learning
and compliance. Exceptions enable practical development workflow.

### II. User Data Isolation (SECURITY CRITICAL)

Multi-tenant data isolation is mandatory to prevent cross-user data leakage.

**Requirements**:
- ALL API endpoints MUST include `user_id` in path: `/api/{user_id}/resource`
- ALL database queries MUST filter by `user_id` (except system/admin tables)
- JWT token user MUST match URL `user_id` (verify and reject mismatches with 401
  Unauthorized)
- Each user sees ONLY their own data
- ZERO cross-user data leakage tolerance

**Testable Verification**:
- Integration test: Create users A and B, create task for A, verify B cannot access via
  GET `/api/B/tasks/{A's-task-id}` (expect 404, not 401 to avoid information disclosure)
- Integration test: User A's JWT token cannot access `/api/B/tasks` (expect 401)
- Code review: All SQLModel queries on user-scoped tables include `.filter(user_id=...)`
- Security audit: Run automated scanner to detect endpoints missing user_id path parameter

**Rationale**: User data isolation is a fundamental security requirement. A single breach
exposing another user's data is a critical failure. This principle enforces defense in
depth: URL structure, query filters, and token verification.

### III. Stateless Architecture

API servers MUST NOT hold in-memory state to enable horizontal scaling and resilience.

**Requirements**:
- API servers hold NO in-memory session or conversation state
- All persistent state (conversations, tasks) persists to database
- MCP tools are stateless (read/write to database)
- Server restarts MUST NOT lose data
- Any server instance can handle any request

**Rationale**: Stateless servers enable horizontal scaling, simplify deployment, improve
fault tolerance, and are essential for cloud-native applications running on Kubernetes.

### IV. Smallest Viable Change

Every code change MUST be the minimum necessary to achieve the stated requirement.

**Requirements**:
- NO refactoring of unrelated code
- Fix only what is broken
- Add only what is requested
- NO premature optimization
- NO unnecessary abstractions
- Three similar lines of code > premature abstraction

**Rationale**: Smallest viable change reduces risk, simplifies review, accelerates
delivery, and prevents scope creep. Premature abstraction creates complexity without
proven value.

### V. Human-as-Tool Strategy

Claude Code MUST invoke the user for clarification when encountering ambiguity or
uncertainty rather than making assumptions.

**Invocation Triggers**:
- **Ambiguous Requirements**: User intent is unclear → Ask 2-3 targeted clarifying
  questions before proceeding
- **Unforeseen Dependencies**: Dependencies discovered that weren't mentioned in spec →
  Surface them and ask for prioritization
- **Architectural Uncertainty**: Multiple valid approaches exist with significant
  tradeoffs → Present options and get user's preference
- **Completion Checkpoint**: After major milestones → Summarize what was done and confirm
  next steps

**Rationale**: Human judgment is superior to AI guessing for domain-specific decisions.
Asking clarifying questions prevents costly rework and ensures alignment with user intent.

## Technology Stack Requirements (Non-Negotiable)

The following technology stack is MANDATORY for all phases:

**Core Stack**:
- **Python**: 3.13+ with UV package manager for dependency management
- **Backend Framework**: FastAPI with async/await
- **ORM**: SQLModel (no raw SQL permitted)
- **Database**: Neon Serverless PostgreSQL
- **Frontend**: Next.js 16+ (App Router) with TypeScript
- **Authentication**: Better Auth with JWT tokens

**AI & Chatbot (Phase III+)**:
- **Chatbot UI**: OpenAI ChatKit
- **AI Framework**: OpenAI Agents SDK
- **MCP Server**: Official MCP SDK (Model Context Protocol)

**Infrastructure (Phase IV+)**:
- **Containerization**: Docker with Docker Desktop
- **Orchestration**: Kubernetes (Minikube for local, DOKS/GKE/AKS for cloud)
- **Package Manager**: Helm Charts
- **Event Streaming**: Kafka (Redpanda Cloud recommended)
- **Distributed Runtime**: Dapr (Phase V)

**DevOps**:
- **AIOps Tools**: kubectl-ai, Kagent, Gordon (Docker AI Agent)
- **CI/CD**: GitHub Actions
- **Development**: Claude Code + Spec-Kit Plus

**Rationale**: Technology stack standardization ensures consistency, simplifies learning,
enables reusable patterns, and aligns with hackathon requirements.

## Phase Progression & Feature Levels

### Phase Evolution

1. **Phase I**: Python console app (in-memory storage, Basic features)
2. **Phase II**: Full-stack web app (FastAPI + Next.js + Neon DB + Better Auth, Basic
   features)
3. **Phase III**: AI Chatbot (MCP server + OpenAI Agents + ChatKit, stateless, Basic
   features)
4. **Phase IV**: Local Kubernetes (Minikube + Helm, Basic features)
5. **Phase V**: Cloud deployment (DOKS/GKE/AKS + Kafka + Dapr, ALL features: Basic +
   Intermediate + Advanced)

**Constitution Review**: This constitution MUST be reviewed before transitioning to each
new phase to ensure principles remain aligned with phase requirements.

### Feature Levels

- **Basic** (Phases I-V): Add Task, Delete Task, Update Task, View Task List, Mark as
  Complete
- **Intermediate** (Phase V only): Priorities & Tags, Search & Filter, Sort Tasks
- **Advanced** (Phase V only): Recurring Tasks, Due Dates & Time Reminders, Timeline

**Rationale**: Progressive feature complexity aligns with architectural complexity. Basic
features establish core patterns; advanced features demonstrate production-readiness.

## Architecture & Design Standards

### VI. Database Standards

All database interactions MUST use SQLModel ORM with proper schema management.

**Requirements**:
- SQLModel ORM exclusively (NO raw SQL queries)
- Database migrations via Alembic
- ALL models MUST include: `user_id`, `id`, `created_at`, `updated_at`
- Foreign key constraints MUST be enforced
- Indexes MUST be created on: `user_id`, `status`, `due_date`

**Schema**:
- **users**: Better Auth managed (id, email, name, created_at)
- **tasks**: user_id FK, title, description, completed, priority, tags, due_date,
  recurrence_pattern
- **conversations**: user_id FK, created_at, updated_at (Phase III+)
- **messages**: user_id FK, conversation_id FK, role, content, created_at (Phase III+)

**Rationale**: ORM usage prevents SQL injection, standardizes queries, enables type
safety, and simplifies database portability. Migrations ensure schema evolution is
versioned and reversible.

### VII. API Design Standards

All APIs MUST follow RESTful conventions with consistent structure.

**Requirements**:
- **RESTful Methods**: GET (read), POST (create), PUT (full update), PATCH (partial
  update), DELETE (remove)
- **URL Pattern**: `/api/{user_id}/resource` and `/api/{user_id}/resource/{id}`
- **Request/Response**: JSON bodies with Pydantic model validation
- **Error Format**: `{error: string, details?: object}` (consistent across all endpoints)
- **Status Codes**:
  - 200 OK (success)
  - 201 Created (resource created)
  - 400 Bad Request (validation failure)
  - 401 Unauthorized (missing/invalid token)
  - 404 Not Found (resource not found)
  - 500 Internal Server Error (unexpected failure)
- **Pagination**: List endpoints MUST support `?page=1&limit=20`
- **Filtering**: Query params for filtering: `?status=pending&priority=high`

**Rationale**: RESTful design provides predictable, discoverable APIs. Consistent error
handling improves client experience. Pagination prevents large response payloads.

### VIII. MCP Tool Design (Phase III+)

MCP tools expose task operations to AI agents with standardized interfaces.

**Requirements**:
- Each tool MUST have clear JSON schema with descriptions
- Tools MUST be stateless (all state in database)
- Required tools: `add_task`, `list_tasks`, `complete_task`, `delete_task`, `update_task`
- All tools MUST accept `user_id` parameter
- Tools MUST return structured responses: `{task_id, status, ...}`
- Error handling MUST be included in tool responses

**Rationale**: MCP provides a standardized protocol for AI agents to interact with
applications. Stateless tools enable scalability. Structured schemas improve AI tool
selection accuracy.

## Code Quality & Testing

### IX. Code Quality Standards

All code MUST adhere to language-specific quality standards with automated enforcement.

**Python (Backend)**:
- Type hints MANDATORY (Python 3.13+) - **Verified by**: `mypy --strict`
- Docstrings for all public functions/classes (Google style) - **Verified by**:
  `pydocstyle` or `interrogate` (minimum 95% coverage)
- Maximum function length: 50 lines (excluding docstrings, blank lines) - **Verified by**:
  `pylint` or `flake8` with max-complexity rules
- PEP 8 compliance - **Enforced by**: `black` formatter + `flake8` linter
- UV for dependency management via `pyproject.toml` - **Verified by**: presence of
  `pyproject.toml`, absence of `requirements.txt`
- Structured error handling (NO bare `except`) - **Verified by**: `flake8` rule E722
- Async/await for all I/O operations - **Code review**: database calls, HTTP requests,
  file I/O use `async/await`

**TypeScript (Frontend)**:
- Strict mode enabled in `tsconfig.json` - **Verified by**: `"strict": true` in config
- All props explicitly typed - **Verified by**: `tsc --noImplicitAny`
- Server Components by default (mark `'use client'` only when needed) - **Code review**:
  Client components justify interactivity
- Tailwind CSS for styling (NO inline styles) - **Verified by**: ESLint rule
  `no-inline-styles`
- Component files in `/components` or `/app` - **Verified by**: directory structure check
- API client abstraction in `/lib/api.ts` - **Code review**: No direct `fetch()` in
  components

**Automated Quality Gates** (CI/CD must pass):
- Python: `black --check`, `mypy`, `flake8`, `pydocstyle`
- TypeScript: `tsc`, `eslint`, `prettier --check`

**Rationale**: Type safety prevents runtime errors. Formatting consistency improves
readability. Async I/O prevents blocking operations. Automated enforcement ensures
compliance without manual review overhead.

### X. Testing Requirements

Testing is essential for production readiness with measurable coverage targets.

**Requirements**:
- **Frameworks**: pytest (Python), Jest/Vitest (TypeScript)
- **Coverage Target**: Minimum 80% line coverage (measured by `pytest-cov` and `c8`)
- **Coverage Exclusions**: Migrations, config files, type stubs, `if __name__ ==
  "__main__"` blocks
- **Test Structure**: Unit → Integration → E2E
- **TDD Encouraged**: Write tests first when possible (Red-Green-Refactor)
- **Test Location**: Test files alongside source: `test_*.py`, `*.test.ts`
- **Mocking**: Mock external dependencies (OpenAI API, database in unit tests)

**Testable Verification**:
- **Backend**: Run `pytest --cov=backend --cov-report=term-missing --cov-fail-under=80`
- **Frontend**: Run `npm test -- --coverage --coverageThreshold='{"global":
  {"lines":80}}'`
- **CI/CD Gate**: Tests must pass and coverage ≥80% before merge to main

**Test Categories**:
- **Unit Tests**: Pure function logic, isolated components (target: 90%+ coverage)
- **Integration Tests**: API endpoints, database interactions (target: 80%+ coverage)
- **E2E Tests**: Critical user journeys (minimum: happy path for each user story)

**Required Tests** (minimum set):
- User data isolation (cross-user access attempts blocked)
- Authentication (token validation, expiry)
- CRUD operations for each entity
- Error handling (400, 401, 404, 500 responses)

**Rationale**: Measurable coverage targets ensure quality. Exclusions prevent gaming
metrics. CI/CD gates prevent untested code in production. Required tests cover security
and core functionality.

## Security & Data Protection

### XI. Data Privacy & Retention (GDPR-Aligned)

User data privacy and retention policies MUST be clearly defined and enforceable.

**Requirements**:
- **Data Retention**: Task data retained indefinitely unless user requests deletion
- **User Data Export**: Users can export all their data in JSON format via
  `/api/{user_id}/export` endpoint
- **Right to Deletion**: Users can delete their account and all associated data via
  `/api/{user_id}/delete-account` (soft delete with 30-day recovery window)
- **Data Minimization**: Collect only necessary data (no tracking pixels, analytics
  without consent)
- **Audit Logging**: User data access/modifications logged with timestamp, user_id,
  action (retention: 90 days)

**Testable Verification**:
- **Export Test**: Call export endpoint, verify JSON contains all user tasks,
  conversations, messages
- **Deletion Test**: Delete account, verify data marked as deleted, inaccessible after 30
  days
- **Audit Test**: Create task, verify audit log entry exists with correct timestamp

**Rationale**: Data privacy is a legal requirement (GDPR, CCPA) and ethical obligation.
Users must control their own data. Audit logs enable compliance verification and security
incident response.

### XII. Security Principles (NON-NEGOTIABLE)

Security MUST be built in from the start, not added later.

**Requirements**:
- NO secrets in code (use `.env` files, MUST be in `.gitignore`)
- Environment variables for: `DATABASE_URL`, `OPENAI_API_KEY`, `BETTER_AUTH_SECRET`,
  `JWT_SECRET`
- Input validation on ALL API endpoints (Pydantic models)
- SQL injection prevention (SQLModel ORM handles)
- XSS prevention (Next.js handles)
- CORS configuration for production
- Rate limiting on API endpoints
- HTTPS in production (HTTP redirect)
- Kubernetes secrets: use Dapr secretstore or K8s Secrets

**Rationale**: Security breaches destroy user trust and violate compliance requirements.
Environment variables prevent secret leakage. Input validation prevents injection attacks.
Rate limiting prevents DoS.

### XIII. Dependency Security & Updates

Third-party dependencies MUST be regularly scanned and updated for vulnerabilities.

**Requirements**:
- **Vulnerability Scanning**: Run `npm audit` (frontend) and `pip-audit` (backend) weekly
- **Automated Updates**: Dependabot or Renovate bot enabled for automated dependency PRs
- **Critical CVEs**: Patch within 48 hours of disclosure
- **High CVEs**: Patch within 7 days
- **Dependency Pinning**: Lock files committed (`package-lock.json`, `uv.lock`)
- **Minimal Dependencies**: Audit new dependencies - justify necessity, check maintenance
  status

**Testable Verification**:
- **CI/CD Gate**: `npm audit --audit-level=high` and `pip-audit` must pass (no high/critical vulns)
- **Monthly Review**: Check dependency update PR queue, merge or justify deferral

**Rationale**: Supply chain attacks are increasing. Vulnerable dependencies are common
attack vectors. Automated scanning and rapid patching reduce exposure window.

### XIV. Authentication & Authorization

Better Auth with JWT provides secure, stateless authentication.

**Requirements**:
- Better Auth for user management (signup/signin)
- JWT tokens for API authentication
- Shared secret between frontend (Better Auth) and backend (FastAPI) via
  `BETTER_AUTH_SECRET`
- ALL API requests MUST include: `Authorization: Bearer <token>` header
- Backend middleware MUST extract and verify JWT on EVERY request
- Token expiry MUST be enforced
- NO API access without valid token (401 Unauthorized)

**Rationale**: JWT tokens enable stateless authentication suitable for horizontally
scaled services. Shared secret verification ensures token authenticity. Token expiry
limits exposure window.

### XV. API Rate Limiting

APIs MUST implement rate limiting to prevent abuse and ensure fair resource allocation.

**Requirements**:
- **Authenticated Users**: 100 requests/minute per user (sliding window)
- **Anonymous Endpoints** (health checks): 10 requests/minute per IP
- **Burst Allowance**: 120 requests in 60 seconds (20% over limit for bursty traffic)
- **Rate Limit Headers**: Include `X-RateLimit-Limit`, `X-RateLimit-Remaining`,
  `X-RateLimit-Reset` in responses
- **429 Response**: Return `429 Too Many Requests` with `Retry-After` header when limit
  exceeded
- **Implementation**: Use FastAPI middleware (slowapi) or Redis-backed rate limiter

**Testable Verification**:
- **Load Test**: Send 120 requests in 10 seconds, verify first 100 succeed, next 20
  return 429
- **Header Test**: Verify rate limit headers present in all API responses
- **Reset Test**: Wait for window reset, verify rate limit counter resets

**Rationale**: Rate limiting prevents DoS attacks, reduces infrastructure costs, and
ensures fair resource allocation across users. Clear headers enable client-side retry
logic.

### XVI. Error Handling & Logging

Errors MUST be handled gracefully with structured logging for observability.

**Requirements**:
- Catch exceptions at API boundary
- Log stack traces for 500 errors (server-side only)
- User-friendly error messages (NO stack traces to client)
- Retry logic for transient failures (network, database connection)
- Circuit breaker pattern for external APIs (OpenAI)
- Graceful degradation when non-critical services fail
- Structured logging in JSON format
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Correlation IDs for request tracing across services

**Rationale**: Proper error handling improves user experience. Structured logging enables
automated analysis. Correlation IDs enable distributed tracing. Circuit breakers prevent
cascade failures.

## Performance & Observability

### XVII. Frontend Accessibility & Responsiveness

Frontend MUST be accessible (WCAG 2.1 Level AA) and responsive across devices.

**Accessibility Requirements**:
- **Semantic HTML**: Use `<button>`, `<nav>`, `<main>`, `<article>` appropriately
- **ARIA Labels**: All interactive elements have accessible names
- **Keyboard Navigation**: All features accessible via keyboard (Tab, Enter, Escape)
- **Color Contrast**: Minimum 4.5:1 for normal text, 3:1 for large text
- **Focus Indicators**: Visible focus outlines (not `outline: none` without replacement)
- **Screen Reader Testing**: Test with NVDA (Windows) or VoiceOver (Mac)

**Responsive Design Requirements**:
- **Breakpoints**: Mobile (< 640px), Tablet (640-1024px), Desktop (> 1024px) - Tailwind
  defaults
- **Touch Targets**: Minimum 44x44px for buttons/links on mobile
- **Viewport Meta**: `<meta name="viewport" content="width=device-width,
  initial-scale=1">`
- **Mobile-First CSS**: Base styles for mobile, use `md:` and `lg:` for larger screens

**Testable Verification**:
- **Lighthouse Accessibility**: Score ≥ 90
- **axe DevTools**: 0 critical violations
- **Manual Test**: Navigate entire app with keyboard only
- **Responsive Test**: Test on iPhone SE (375px), iPad (768px), Desktop (1920px)

**Rationale**: Accessibility is a legal requirement (ADA, Section 508) and moral
imperative. Responsive design ensures usability across devices. 15% of users have
disabilities requiring assistive technology.

### XVIII. Performance Standards

Performance targets ensure acceptable user experience with measurable SLOs (Service Level
Objectives).

**Backend Performance**:
- **API Latency**: p95 < 500ms, p99 < 1000ms (measured under 100 concurrent users, 1000
  tasks per user)
- **Database Queries**: NO N+1 queries - **Verified by**: SQLAlchemy query logging in
  tests, max 3 queries per request
- **Pagination**: List endpoints MUST paginate - **Verified by**: default `limit=20`,
  max `limit=100`
- **Connection Pooling**: PostgreSQL pool size 10-20 - **Verified by**: SQLModel engine
  config
- **Async Operations**: All I/O is async - **Verified by**: No synchronous
  `requests.get()`, use `httpx` async client

**Frontend Performance**:
- **Bundle Size**: Main bundle < 200KB gzipped - **Verified by**: `next build` output
- **First Contentful Paint (FCP)**: < 1.5s - **Verified by**: Lighthouse CI
- **Largest Contentful Paint (LCP)**: < 2.5s - **Verified by**: Lighthouse CI
- **Time to Interactive (TTI)**: < 3.5s - **Verified by**: Lighthouse CI
- **Code Splitting**: Route-based splitting enabled - **Verified by**: Next.js automatic
  splitting

**Load Testing** (Phase V):
- Tool: Locust or k6
- Scenario: 100 concurrent users, 10 requests/sec for 5 minutes
- Success Criteria: 95% of requests < 500ms, 0% error rate

**Testable Verification**:
- **Local**: `pytest tests/performance/` runs load tests against local server
- **CI/CD**: Lighthouse CI fails build if FCP > 1.5s or LCP > 2.5s
- **Production**: Prometheus + Grafana dashboards track p95/p99 latency

**Rationale**: Specific, measurable performance targets enable automated enforcement.
Sub-500ms p95 latency feels responsive. Frontend performance impacts SEO and user
retention. Load testing validates production readiness.

### XIX. Monitoring & Observability

Production systems MUST be observable for troubleshooting and optimization.

**Requirements**:
- Structured logging (JSON format)
- Health check endpoints: `/health` (returns 200 OK when healthy)
- Metrics to track: request count, latency, error rate
- Kubernetes logs accessible via `kubectl logs`
- Production consideration: Prometheus + Grafana (optional for Phase V)

**Rationale**: Observability enables rapid incident response. Health checks enable
automated monitoring. Metrics enable capacity planning and performance optimization.

## Cloud-Native Architecture (Phase V)

### XX. Database Backup & Disaster Recovery

Data loss is unacceptable. Automated backups and tested recovery procedures are mandatory.

**Requirements**:
- **Backup Frequency**: Daily automated backups (Neon provides automatic backups)
- **Backup Retention**: 30 days for Phase II-IV, 90 days for Phase V production
- **Point-in-Time Recovery**: Ability to restore to any point within retention window
- **Backup Testing**: Monthly restore test to verify backup integrity
- **Disaster Recovery Plan**: Documented procedure for database restoration
- **Backup Verification**: Automated check that backup completed successfully (alert on
  failure)

**Testable Verification**:
- **Restore Test**: Monthly restore backup to staging environment, verify data integrity
- **Recovery Time Objective (RTO)**: < 4 hours to restore service
- **Recovery Point Objective (RPO)**: < 24 hours of data loss acceptable
- **Backup Alert**: Verify backup failure triggers alert (test by simulating failure)

**Neon-Specific**:
- Verify Neon automatic backups enabled in project settings
- Test branch creation from specific point in time
- Document procedure to restore from Neon backup

**Rationale**: Data is the most valuable asset. Hardware failures, human errors, and
security incidents can cause data loss. Regular, tested backups are the only reliable
recovery mechanism.

## Cloud-Native Architecture (Phase V)

### XXI. Event-Driven Architecture (Phase V)

Kafka enables decoupled, asynchronous communication between services.

**Requirements**:
- **Kafka Topics**: `task-events`, `reminders`, `task-updates`
- All task operations (create, update, delete, complete) MUST publish events
- **Event Schema Standardization**:
  - `task-events`: `{event_type, task_id, task_data, user_id, timestamp}`
  - `reminders`: `{task_id, title, due_at, remind_at, user_id}`
- Services MUST consume events asynchronously
- Event log provides audit trail

**Rationale**: Event-driven architecture decouples services, enables scalability, supports
real-time updates, and provides built-in audit logging. Asynchronous processing prevents
blocking.

### XXII. Dapr Integration (Phase V)

Dapr abstracts infrastructure concerns behind portable APIs.

**Requirements**:
- **Pub/Sub Component**: Kafka abstraction (publish/subscribe without Kafka client code)
- **State Management Component**: PostgreSQL abstraction (key-value API)
- **Service Invocation**: Inter-service calls with built-in retries and circuit breaking
- **Input Bindings**: Cron triggers for scheduled reminders
- **Secrets Management**: API keys via Dapr secretstore
- Dapr sidecar pattern in ALL pods
- Configuration via Dapr components (YAML)
- Applications talk to Dapr via HTTP (localhost:3500)

**Rationale**: Dapr abstracts infrastructure (Kafka, database, secrets) behind simple
HTTP APIs. Apps remain infrastructure-agnostic. Swapping backends (e.g., Kafka →
RabbitMQ) requires only YAML config changes, not code changes.

## Deployment & Operations

### XXIII. Containerization Standards

All services MUST be containerized following best practices.

**Requirements**:
- Multi-stage Docker builds (minimize final image size)
- Minimize layer count (combine RUN commands where logical)
- `.dockerignore` to exclude: `.git`, `node_modules`, `__pycache__`, `.env`
- Health check endpoints: `/health` (container health probe)
- Non-root user in containers (security best practice)
- Image tagging: semantic versioning (e.g., `v1.2.3`)
- Use Gordon (Docker AI Agent) when available for assistance

**Rationale**: Multi-stage builds reduce image size. Non-root users reduce attack surface.
Health checks enable automated container management. Semantic versioning enables rollback.

### XXIV. Kubernetes & Helm Standards

Kubernetes deployments MUST use Helm charts for reproducibility.

**Requirements**:
- Helm charts for ALL services
- Values files: `values-dev.yaml`, `values-prod.yaml` (environment-specific config)
- Resource limits and requests defined (CPU, memory)
- Liveness and readiness probes configured
- ConfigMaps for non-sensitive configuration
- Secrets for sensitive data
- Service discovery via Kubernetes DNS
- Horizontal Pod Autoscaling (HPA) for production
- Use kubectl-ai and Kagent for AIOps assistance

**Rationale**: Helm enables repeatable deployments across environments. Resource limits
prevent noisy neighbor issues. Health probes enable automated recovery. HPA handles
traffic spikes.

### XXV. CI/CD Pipeline Standards

Continuous integration and deployment automate quality gates.

**Requirements**:
- GitHub Actions for automation
- Workflow triggers: push to `main`, pull request
- Pipeline steps: lint → test → build → deploy
- Separate pipelines: dev, staging, production
- Automated Docker image builds
- Deploy to Minikube (dev), DOKS/GKE/AKS (production)
- Rollback capability (previous image version)

**Rationale**: CI/CD automation ensures consistent builds, prevents broken main branch,
enables rapid iteration, and enforces quality gates before production deployment.

## Development Workflow

### XXVI. Conversation Persistence (Phase III)

Chatbot conversations MUST persist to database for stateless server operation.

**Requirements**:
- Database models: `Conversation`, `Message`
- Stateless chat endpoint: `POST /api/{user_id}/chat`
- Request includes: `conversation_id` (optional), `message` (required)
- Response includes: `conversation_id`, `response`, `tool_calls`
- Workflow:
  1. Fetch conversation history from database
  2. Build message array (history + new message)
  3. Store user message in database
  4. Run AI agent with MCP tools
  5. Store assistant response in database
  6. Return response to client
- NO in-memory chat state

**Rationale**: Database-backed conversations enable stateless servers, survive restarts,
support conversation resumption, and enable horizontal scaling.

### XXVII. Documentation Standards

Documentation MUST be comprehensive and maintained.

**Requirements**:
- **README.md**: Setup instructions, usage, architecture overview
- **API Documentation**: OpenAPI/Swagger (FastAPI auto-generates)
- **Inline Comments**: Complex logic only (avoid obvious comments)
- **ADRs**: Architecture Decision Records for significant decisions
- **PHRs**: Prompt History Records for ALL user interactions
- **CLAUDE.md**: Root + `frontend/CLAUDE.md` + `backend/CLAUDE.md`

**Rationale**: Good documentation enables onboarding, reduces support burden, and serves
as specification of record. ADRs capture architectural rationale. PHRs enable learning
from AI interactions.

### XXVIII. Git & Version Control

Version control MUST follow conventional commit standards.

**Requirements**:
- **Commit Message Format**: `<type>: <description>`
  - Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
- **Atomic Commits**: Single logical change per commit
- **`.gitignore`**: `.env`, `node_modules`, `__pycache__`, `.venv`, `dist`
- **Branch Strategy**: `main` (production-ready)
- **Release Tags**: Semantic versioning (e.g., `v1.0.0`, `v2.0.0`)

**Rationale**: Conventional commits improve changelog generation. Atomic commits simplify
revert operations. `.gitignore` prevents secret leakage. Semantic versioning communicates
API compatibility.

## Monorepo Structure Standards

The project MUST follow this monorepo organization:

```
/
├── .specify/
│   ├── memory/constitution.md       # This file
│   ├── templates/                   # Spec-Kit Plus templates
│   └── scripts/                     # Automation scripts
├── specs/
│   └── <feature>/
│       ├── spec.md                  # Feature requirements
│       ├── plan.md                  # Architecture decisions
│       └── tasks.md                 # Implementation tasks
├── history/
│   ├── prompts/
│   │   ├── constitution/            # Constitution-related PHRs
│   │   ├── <feature-name>/          # Feature-specific PHRs
│   │   └── general/                 # General PHRs
│   └── adr/                         # Architecture Decision Records
├── frontend/
│   ├── CLAUDE.md                    # Frontend-specific guidance
│   ├── app/                         # Next.js App Router pages
│   ├── components/                  # React components
│   └── lib/                         # Utilities, API client
├── backend/
│   ├── CLAUDE.md                    # Backend-specific guidance
│   ├── main.py                      # FastAPI entry point
│   ├── models.py                    # SQLModel models
│   ├── routes/                      # API route handlers
│   └── pyproject.toml               # UV dependency config
├── k8s/
│   └── helm/
│       ├── frontend/                # Frontend Helm chart
│       └── backend/                 # Backend Helm chart
├── docker-compose.yml               # Local development
├── CLAUDE.md                        # Root Claude Code guidance
└── README.md                        # Project overview
```

**Rationale**: Monorepo enables single-context development with Claude Code. Layered
CLAUDE.md files provide context-specific guidance. Clear separation of concerns improves
navigation.

## Development Environment Requirements

### Platform Requirements

- **Windows Users**: WSL 2 (Windows Subsystem for Linux) MANDATORY
- **Python**: 3.13+ with UV package manager
- **Node.js**: 20+ for frontend
- **Docker**: Docker Desktop for containers
- **Kubernetes**: kubectl CLI tool
- **Helm**: Helm CLI for chart management

**Rationale**: WSL 2 provides consistent Linux environment on Windows. UV simplifies
Python dependency management. Docker Desktop includes Kubernetes support.

## Deployment Targets

- **Local (Phase II-III)**: Docker Compose
- **Local (Phase IV-V)**: Minikube
- **Cloud (Phase V)**: DigitalOcean Kubernetes (DOKS), Google Kubernetes Engine (GKE),
  or Azure Kubernetes Service (AKS)
- **Frontend Hosting (Phase II-V)**: Vercel
- **Database (All Phases)**: Neon Serverless PostgreSQL
- **Kafka (Phase V)**: Redpanda Cloud Serverless

**Rationale**: Progressive deployment complexity matches architectural complexity. Free
tiers enable cost-effective learning. Cloud platforms provide production-grade
infrastructure.

## Governance

### Constitution Authority

This constitution supersedes all other development guidance. All code generation by Claude
Code MUST comply with these principles.

### Compliance Requirements

- ALL pull requests and code reviews MUST verify constitution compliance
- Violations MUST be justified in plan.md "Complexity Tracking" section
- PHR creation is MANDATORY after every user interaction (except for `/sp.phr` itself)
- ADR suggestions (NOT auto-creation) MUST be made for architecturally significant
  decisions

### Amendment Process

Constitution amendments require version bump following semantic versioning:

- **MAJOR**: Breaking governance changes (principle removals or redefinitions)
- **MINOR**: New principles added or materially expanded guidance
- **PATCH**: Clarifications, wording improvements, typo fixes

### Phase Transition Review

The constitution MUST be reviewed before transitioning to each new phase (I → II → III
→ IV → V) to ensure principles remain aligned with phase-specific requirements.

### Architectural Decision Record (ADR) Process

When significant architectural decisions are made (typically during `/sp.plan` and
sometimes `/sp.tasks`), test for ADR significance:

- **Impact**: Long-term consequences? (e.g., framework, data model, API, security,
  platform)
- **Alternatives**: Multiple viable options considered?
- **Scope**: Cross-cutting and influences system design?

If ALL true, suggest (do NOT auto-create):
```
📋 Architectural decision detected: [brief-description]
   Document reasoning and tradeoffs? Run `/sp.adr [decision-title]`
```

Wait for user consent. Group related decisions (e.g., authentication stack, deployment
strategy) into one ADR when appropriate.

---

**Version**: 1.1.0 | **Ratified**: 2025-12-06 | **Last Amended**: 2025-12-06
