---
name: adr-detector
description: Detect architecturally significant decisions during planning and suggest ADR documentation. Use during plan.md creation or when making framework, database, API, security, or platform decisions. Constitutional requirement to suggest (not auto-create) ADRs.
allowed-tools: Read
---

# ADR Significance Detector Skill

Tests architectural decisions against the three-part significance criteria and suggests ADR creation.

## Constitutional Requirement

Per Constitution Section "Architectural Decision Record (ADR) Process":
- **SUGGEST** ADRs for significant decisions (do NOT auto-create)
- **WAIT** for user consent before creating
- **GROUP** related decisions into one ADR when appropriate

## Three-Part Significance Test

A decision is architecturally significant if **ALL THREE** criteria are true:

### 1. Impact: Long-Term Consequences?

Decision affects one or more of:
- **Framework/Technology**: Choosing FastAPI, Next.js, SQLModel, Better Auth
- **Data Model**: Database schema, relationships, persistence strategy
- **API Design**: RESTful structure, authentication approach, versioning
- **Security**: Auth mechanism, encryption, data isolation strategy
- **Platform**: Deployment target (Docker, Kubernetes, cloud provider)
- **Integration**: External services (OpenAI, Kafka, Dapr)
- **Performance**: Caching strategy, async patterns, optimization approach
- **Scalability**: Horizontal scaling, load balancing, stateless design

❌ **NOT significant**: Variable naming, minor refactoring, test structure

### 2. Alternatives: Multiple Viable Options Considered?

Decision involved evaluating **2 or more** reasonable alternatives with tradeoffs:

✅ **Significant Examples**:
- "FastAPI vs Flask vs Django for REST API"
- "SQLModel vs SQLAlchemy vs Django ORM"
- "PostgreSQL vs MySQL vs MongoDB"
- "JWT vs Session cookies vs OAuth"
- "Docker Compose vs Kubernetes for local dev"
- "Kafka vs RabbitMQ vs NATS for events"

❌ **NOT significant**: Only one obvious choice (e.g., "Python 3.13 because constitution requires it")

### 3. Scope: Cross-Cutting and Influences System Design?

Decision affects **multiple components** or **multiple phases** of the system:

✅ **Cross-cutting examples**:
- Authentication affects frontend, backend, database, API
- Database choice affects ORM, migrations, backups, performance
- Event streaming affects all services, scalability, resilience
- Containerization affects dev, test, staging, production

❌ **NOT cross-cutting**: Single component, single file, localized change

## Detection Process

When reviewing `plan.md` or architectural discussions:

### Step 1: Identify Decisions

Look for statements like:
- "We will use [X]"
- "Choose [X] over [Y]"
- "[X] is selected because..."
- "Technology stack: [X]"
- "Authentication approach: [X]"

### Step 2: Apply Three-Part Test

For each decision, check:
1. ✅ Impact: Does it affect framework/data/API/security/platform?
2. ✅ Alternatives: Were 2+ options considered?
3. ✅ Scope: Does it affect multiple components/phases?

### Step 3: Suggest ADR (Do Not Auto-Create)

If **ALL THREE** are true:

```
📋 Architectural decision detected: [brief-description]
   Document reasoning and tradeoffs? Run `/sp.adr [decision-title]`
```

**Never auto-create the ADR**. Wait for user to run `/sp.adr` command.

### Step 4: Group Related Decisions

If multiple related decisions detected, suggest grouping:

```
📋 Multiple related architectural decisions detected:
   - Authentication mechanism (Better Auth + JWT)
   - Authorization strategy (user_id in URL)
   - Token storage (httpOnly cookies vs localStorage)

   Document as single ADR? Run `/sp.adr authentication-and-authorization-strategy`
```

## Common Significant Decisions by Phase

### Phase I (Console App)
- **Database**: SQLite vs in-memory vs file-based (✅ significant)
- **CLI Framework**: Click vs argparse vs Typer (✅ significant)
- **User Isolation**: Command-line arg vs env var vs config file (✅ significant)

### Phase II (Web App)
- **Backend Framework**: FastAPI vs Flask vs Django (✅ significant)
- **Frontend Framework**: Next.js vs React+Vite vs SvelteKit (✅ significant)
- **Authentication**: Better Auth vs Auth.js vs Clerk vs custom JWT (✅ significant)
- **Database**: Neon vs Supabase vs PlanetScale vs self-hosted PostgreSQL (✅ significant)
- **ORM**: SQLModel vs Prisma vs SQLAlchemy (✅ significant)

### Phase III (AI Chatbot)
- **AI Framework**: OpenAI Agents SDK vs LangChain vs custom (✅ significant)
- **MCP Implementation**: Official SDK vs custom protocol (✅ significant)
- **Conversation Storage**: Database vs vector DB vs Redis (✅ significant)
- **Chat UI**: OpenAI ChatKit vs custom vs Vercel AI SDK UI (✅ significant)

### Phase IV (Local K8s)
- **Container Orchestration**: Kubernetes vs Docker Swarm vs Nomad (✅ significant)
- **Local K8s**: Minikube vs kind vs k3s vs Docker Desktop K8s (✅ significant)
- **Package Manager**: Helm vs Kustomize vs raw YAML (✅ significant)

### Phase V (Cloud)
- **Cloud Provider**: DigitalOcean vs GCP vs AWS vs Azure (✅ significant)
- **Event Streaming**: Kafka vs RabbitMQ vs NATS vs AWS EventBridge (✅ significant)
- **Distributed Runtime**: Dapr vs custom vs service mesh (Istio) (✅ significant)
- **Managed Kafka**: Redpanda Cloud vs Confluent Cloud vs AWS MSK (✅ significant)

## Non-Significant Decisions (Do NOT suggest ADR)

❌ **Implementation details**:
- Variable naming conventions
- File organization within a module
- Test file naming
- Comment style

❌ **Constitutional mandates** (no alternatives considered):
- "Use Python 3.13+ because constitution requires it"
- "Use SQLModel because constitution requires ORM"
- "Filter by user_id because constitution requires isolation"

❌ **Localized changes**:
- Refactoring a single function
- Adding a utility helper
- Changing log message format

❌ **Obvious choices with no tradeoffs**:
- "Use .gitignore to exclude .env files"
- "Use pytest for testing Python code"
- "Use ESLint for TypeScript linting"

## Example: Significant Decision Detection

### Input (from plan.md)

```markdown
## Technology Decisions

1. **CLI Framework**: We will use Click instead of argparse.
   - Click provides better user experience with automatic help generation
   - Supports command grouping and decorators
   - More Pythonic than argparse

2. **Database**: SQLite for Phase I local storage.
   - SQLModel ORM as required by constitution
   - File-based persistence (todo.db)
   - Lightweight for console app

3. **User Isolation**: Username passed as CLI argument.
   - `--user alice` on every command
   - Filtered in database queries by user_id
```

### Analysis

**Decision 1: Click vs argparse**
- Impact: ✅ Framework choice affects all CLI commands
- Alternatives: ✅ Evaluated Click, argparse (maybe Typer too)
- Scope: ✅ Affects all user interactions across all commands

**Result**: ✅ **SIGNIFICANT** - Suggest ADR

**Decision 2: SQLite**
- Impact: ✅ Database affects persistence, migrations, performance
- Alternatives: ⚠️ Constitution requires SQLModel, but did we consider in-memory vs file-based?
- Scope: ✅ Affects all data operations

**Result**: ⚠️ **MAYBE SIGNIFICANT** - If alternatives (in-memory, JSON file) were considered, suggest ADR. If SQLite was only option for Phase I, not significant.

**Decision 3: User Isolation via CLI arg**
- Impact: ✅ Security mechanism (constitutional requirement)
- Alternatives: ✅ Could use env var, config file, prompt
- Scope: ✅ Affects all commands, all users

**Result**: ✅ **SIGNIFICANT** - Suggest ADR

### Output Suggestion

```
📋 Architectural decisions detected:

1. CLI Framework Selection (Click vs argparse)
   Document reasoning? Run `/sp.adr cli-framework-selection`

2. User Identification Mechanism (CLI arg vs env var vs config)
   Document reasoning? Run `/sp.adr user-identification-mechanism`

Alternatively, group related decisions:
   `/sp.adr phase-i-console-architecture` (CLI + user isolation)
```

## Timing: When to Detect

### During `/sp.plan` (Primary)
- Scan plan.md for technology choices
- Identify framework/database/API decisions
- Suggest ADRs before implementation begins

### During `/sp.tasks` (Secondary)
- If new decisions emerge during task breakdown
- If implementation approach requires architectural choice

### During Implementation (Rare)
- If unforeseen architectural decision required mid-implementation
- Pause, document decision, then continue

## ADR Grouping Guidelines

**Group** related decisions into one ADR when:
- Same concern (e.g., authentication + authorization)
- Same phase transition (e.g., Phase I → Phase II migration)
- Dependent choices (e.g., Kafka + Dapr for event streaming)

**Separate** into multiple ADRs when:
- Independent concerns (e.g., database choice vs frontend framework)
- Different timing (decided weeks/months apart)
- Different stakeholders/reviewers

## MCP Server Integration

When evaluating framework alternatives, use **context7** to fetch docs:

```
User: "Should we use FastAPI or Flask?"
  ↓
You: Use mcp__context7__resolve-library-id for "fastapi" and "flask"
  ↓
You: Use mcp__context7__get-library-docs to compare APIs
  ↓
You: Evaluate alternatives with real documentation
  ↓
You: If significant, suggest ADR
```

## Output Format

### Single Decision
```
📋 Architectural decision detected: [brief-description]
   - Impact: [how it affects system]
   - Alternatives: [options considered]
   - Scope: [what components affected]

   Document reasoning and tradeoffs? Run `/sp.adr [decision-title]`
```

### Multiple Decisions
```
📋 Multiple architectural decisions detected:

1. [Decision 1]: [brief]
   Run `/sp.adr [decision-1-title]`

2. [Decision 2]: [brief]
   Run `/sp.adr [decision-2-title]`

Or group related decisions:
   `/sp.adr [grouped-title]`
```

### No Significant Decisions
```
ℹ️ No architecturally significant decisions detected in this plan.
  Implementation details documented but no ADRs needed.
```

## Constitutional Compliance

From Constitution:
> "ADR suggestions (never auto-create) for significant architectural decisions"

**MUST**:
- ✅ Suggest ADRs when significant
- ✅ Wait for user consent
- ✅ Provide `/sp.adr` command to run

**MUST NOT**:
- ❌ Auto-create ADRs
- ❌ Suggest ADRs for trivial decisions
- ❌ Block work if user declines ADR
