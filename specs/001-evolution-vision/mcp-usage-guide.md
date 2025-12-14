# MCP Server Usage Guide - Evolution of Todo Project

**Feature**: Evolution Vision (All 5 Phases)
**Created**: 2025-12-08
**Purpose**: Comprehensive guide for when and how to use MCP servers throughout project development

---

## 📋 MCP Servers Status

| MCP Server | Status | Configuration Required | Security Level |
|------------|--------|----------------------|----------------|
| **Playwright** | ✅ Connected | None | ⭐⭐⭐ High (sandboxed) |
| **Context7** | ✅ Connected | None | ⭐⭐⭐ High (read-only) |
| **GitHub** | ✅ Connected | GITHUB_TOKEN env var | ⭐⭐ Medium (requires PAT) |
| **PostgreSQL** | ⚠️ Not Configured | DATABASE_URL env var | ⭐ Low (requires credentials) |

---

## 🎯 Phase-by-Phase MCP Usage

### Phase I: Console Todo App (Python 3.13+, SQLite)

**Primary MCPs Used**:
- ✅ **Context7**: Fetch latest Python 3.13+, SQLModel, pytest documentation
- ✅ **GitHub**: Commit Phase I implementation, create PR

**When to Use**:

1. **Context7 Documentation Queries**:
   ```bash
   # When implementing SQLModel models
   "What are the latest SQLModel best practices for Python 3.13?"
   "How to implement nullable fields in SQLModel for future-proof schemas?"

   # When writing pytest tests
   "What's the latest pytest syntax for parametrized tests?"
   "How to configure pytest-cov for 80% coverage threshold?"

   # When configuring mypy
   "What are the mypy --strict requirements for Python 3.13?"
   ```

2. **GitHub MCP Operations**:
   ```bash
   # After completing Phase I implementation
   - Create feature branch: 002-phase-i-console-app
   - Commit with message referencing spec sections
   - Create PR with template linking to spec.md
   - Link PR to constitution principles validated
   ```

**Not Used in Phase I**:
- ❌ Playwright (no web UI yet)
- ❌ PostgreSQL (using SQLite locally)

---

### Phase II: Full-Stack Web App (FastAPI, Next.js 16+, Neon PostgreSQL)

**Primary MCPs Used**:
- ✅ **Context7**: Fetch latest FastAPI, Next.js 16+, Better Auth, Neon PostgreSQL docs
- ✅ **Playwright**: E2E testing of web UI (login, task CRUD, JWT validation)
- ✅ **PostgreSQL**: Validate migration from SQLite, inspect schema
- ✅ **GitHub**: Commit Phase II implementation, create PR

**When to Use**:

1. **Context7 Documentation Queries**:
   ```bash
   # FastAPI implementation
   "How to implement Better Auth with FastAPI in 2025?"
   "What's the latest FastAPI JWT middleware pattern?"
   "How to configure CORS for Next.js 16+ frontend?"

   # Next.js frontend
   "What are Next.js 16 React Server Components best practices?"
   "How to implement Lighthouse-optimized Next.js pages?"

   # Neon PostgreSQL
   "How to connect FastAPI to Neon PostgreSQL with connection pooling?"
   "What's the Neon PostgreSQL migration strategy from SQLite?"
   ```

2. **Playwright E2E Testing**:
   ```bash
   # After frontend implementation
   - Navigate to http://localhost:3000
   - Test login flow with Better Auth
   - Verify JWT token in localStorage
   - Test task CRUD operations (add, view, update, delete, complete)
   - Validate user data isolation (user A cannot see user B's tasks)
   - Measure page load times for Lighthouse validation
   ```

3. **PostgreSQL MCP Queries** (⚠️ Configure DATABASE_URL first):
   ```sql
   # Validate migration success
   SELECT COUNT(*) FROM tasks GROUP BY user_id;

   # Inspect schema for future-proof fields
   SELECT column_name, data_type, is_nullable
   FROM information_schema.columns
   WHERE table_name = 'tasks';

   # Validate user data isolation
   SELECT user_id, COUNT(*) as task_count FROM tasks GROUP BY user_id;
   ```

4. **GitHub MCP Operations**:
   ```bash
   # After completing Phase II implementation
   - Create feature branch: 003-phase-ii-web-app
   - Commit REST API endpoints with spec references
   - Commit Next.js frontend with Lighthouse report
   - Create PR with migration validation results
   - Link PR to constitutional principles (Auth, Accessibility, Rate Limiting)
   ```

---

### Phase III: AI Chatbot Integration (OpenAI Agents SDK, MCP)

**Primary MCPs Used**:
- ✅ **Context7**: Fetch latest OpenAI Agents SDK, MCP specification docs
- ✅ **Playwright**: Test AI chatbot UI interactions
- ✅ **PostgreSQL**: Inspect conversation/message tables
- ✅ **GitHub**: Commit Phase III implementation, create PR

**When to Use**:

1. **Context7 Documentation Queries**:
   ```bash
   # OpenAI Agents SDK
   "What's the latest OpenAI Agents SDK API for Python in 2025?"
   "How to implement stateless conversation with OpenAI Agents SDK?"
   "What are the OpenAI API rate limiting best practices?"

   # MCP Tool Design
   "What's the official MCP specification for tool definitions?"
   "How to implement MCP servers for task CRUD operations?"
   "How to handle MCP tool errors gracefully with fallbacks?"
   ```

2. **Playwright UI Testing**:
   ```bash
   # After chatbot UI implementation
   - Navigate to chatbot interface
   - Send natural language command: "Add buy groceries to my tasks"
   - Verify task appears in task list
   - Test confirmation flow: "Delete all tasks" → verify confirmation prompt
   - Test fallback: disable OpenAI API → verify pattern matching works
   ```

3. **PostgreSQL MCP Queries**:
   ```sql
   # Inspect conversation state
   SELECT c.id, c.user_id, COUNT(m.id) as message_count
   FROM conversations c
   LEFT JOIN messages m ON c.id = m.conversation_id
   GROUP BY c.id, c.user_id;

   # Debug AI tool calls
   SELECT role, content, tool_calls
   FROM messages
   WHERE conversation_id = ?
   ORDER BY created_at DESC
   LIMIT 10;

   # Validate stateless architecture (no orphaned sessions)
   SELECT COUNT(*) FROM conversations WHERE updated_at < NOW() - INTERVAL '24 hours';
   ```

4. **GitHub MCP Operations**:
   ```bash
   # After completing Phase III implementation
   - Create feature branch: 004-phase-iii-ai-chatbot
   - Commit MCP tool definitions with spec references
   - Commit AI intent classification tests (≥90% accuracy)
   - Create PR with OpenAI API error handling documentation
   - Link PR to constitutional principle V (MCP Tool Design)
   ```

---

### Phase IV: Local Kubernetes Deployment (Kind, Minikube, k3d)

**Primary MCPs Used**:
- ✅ **Context7**: Fetch latest Kubernetes, Docker, Kind/Minikube docs
- ✅ **Playwright**: Validate Ingress endpoints with TLS
- ✅ **PostgreSQL**: Test database connectivity from K8s pods
- ✅ **GitHub**: Commit Phase IV manifests, create PR

**When to Use**:

1. **Context7 Documentation Queries**:
   ```bash
   # Kubernetes deployment
   "What are Kubernetes 1.30+ best practices for health checks?"
   "How to configure HPA (Horizontal Pod Autoscaler) with CPU metrics?"
   "What's the latest Ingress controller setup for local K8s?"

   # Docker containerization
   "How to create multi-stage Dockerfiles for FastAPI apps?"
   "What are the Docker security best practices for Python apps?"

   # Kind/Minikube setup
   "How to set up Kind cluster with local registry?"
   "How to configure Minikube ingress addon?"
   ```

2. **Playwright Ingress Testing**:
   ```bash
   # After Ingress setup
   - Navigate to https://todo.local (or configured hostname)
   - Verify TLS certificate valid
   - Test frontend loads correctly through Ingress
   - Test API endpoints accessible via Ingress
   - Measure latency through Ingress vs direct Service access
   ```

3. **PostgreSQL MCP Queries** (from K8s pod):
   ```sql
   # Validate pod can connect to Neon PostgreSQL
   SELECT version();

   # Test connection pooling from multiple pods
   SELECT COUNT(*) FROM pg_stat_activity WHERE application_name LIKE 'fastapi%';

   # Validate secrets mounted correctly (without exposing credentials)
   -- Query should succeed if DATABASE_URL from Secret is correct
   SELECT 1;
   ```

4. **GitHub MCP Operations**:
   ```bash
   # After completing Phase IV implementation
   - Create feature branch: 005-phase-iv-kubernetes
   - Commit Kubernetes manifests (Deployment, Service, ConfigMap, Secret, Ingress)
   - Commit Dockerfile with multi-stage builds
   - Create PR with K8s deployment validation checklist
   - Link PR to constitutional principle XXII (Kubernetes Standards)
   ```

---

### Phase V: Cloud Deployment (DOKS/GKE/AKS, Kafka, Dapr)

**Primary MCPs Used**:
- ✅ **Context7**: Fetch latest Dapr, Kafka/Redpanda, cloud provider (DOKS/GKE/AKS) docs
- ✅ **Playwright**: Validate cloud-hosted endpoints and multi-region routing
- ✅ **PostgreSQL**: Monitor event sourcing, audit logs, multi-region replication
- ✅ **GitHub**: Commit Phase V cloud manifests, CI/CD pipelines, create PR

**When to Use**:

1. **Context7 Documentation Queries**:
   ```bash
   # Dapr integration
   "How to configure Dapr sidecars for Kubernetes 2025?"
   "What are Dapr pub/sub best practices for Kafka?"
   "How to implement Dapr state management with PostgreSQL?"

   # Kafka/Redpanda
   "What's the latest Redpanda cloud setup for Kubernetes?"
   "How to monitor Kafka consumer lag in Prometheus?"
   "What are Kafka event schema evolution best practices?"

   # Cloud providers
   "How to set up DOKS (DigitalOcean Kubernetes) cluster?"
   "What are GKE Autopilot vs Standard mode differences in 2025?"
   "How to configure AKS with Azure AD integration?"

   # CI/CD
   "What's the latest GitHub Actions syntax for Kubernetes deployments?"
   "How to implement blue-green deployments in Kubernetes?"
   ```

2. **Playwright Cloud Endpoint Testing**:
   ```bash
   # After cloud deployment
   - Navigate to production URL (e.g., https://todo.example.com)
   - Verify TLS certificate from cloud provider
   - Test load balancer routing across regions
   - Measure latency from different geographic locations
   - Test WebSocket connections for real-time updates
   - Validate rate limiting (429 responses after 100 req/min)
   ```

3. **PostgreSQL MCP Queries** (Cloud Database):
   ```sql
   # Monitor event sourcing
   SELECT event_type, COUNT(*)
   FROM task_events
   WHERE created_at > NOW() - INTERVAL '1 hour'
   GROUP BY event_type;

   # Validate multi-region replication lag
   SELECT NOW() - MAX(updated_at) as replication_lag
   FROM tasks;

   # Check audit log retention (90 days per constitution)
   SELECT COUNT(*)
   FROM audit_logs
   WHERE created_at < NOW() - INTERVAL '90 days';

   # Monitor database backup status
   SELECT * FROM pg_stat_archiver;
   ```

4. **GitHub MCP Operations**:
   ```bash
   # After completing Phase V implementation
   - Create feature branch: 006-phase-v-cloud-deployment
   - Commit Dapr configuration (pub/sub, state management)
   - Commit Kafka event schemas and consumers
   - Commit CI/CD pipeline (GitHub Actions)
   - Commit monitoring dashboards (Prometheus/Grafana)
   - Create PR with cloud deployment validation checklist
   - Link PR to constitutional principles VI, VII, XVIII, XX, XXI
   ```

---

## 🔒 Security Best Practices

### GitHub MCP Security

**Setup**:
```bash
# Create GitHub Personal Access Token (PAT)
# Go to: https://github.com/settings/tokens
# Scopes: repo, workflow
# Expiration: 90 days (renewable)

# Set environment variable (NEVER commit to repository)
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Verify connection
claude mcp list
# Should show: github: ✓ Connected
```

**Safe Operations**:
- ✅ Create branches
- ✅ Commit changes with spec references
- ✅ Create pull requests
- ✅ Query repository metadata

**Avoid**:
- ❌ Force pushing to main/master
- ❌ Deleting branches without confirmation
- ❌ Committing secrets/credentials

### PostgreSQL MCP Security

**Setup** (Phase II+):
```bash
# Use READ-ONLY user for MCP queries
# Create read-only user in Neon PostgreSQL dashboard:
# Username: claude_readonly
# Permissions: SELECT only on all tables

# Set environment variable with read-only credentials
export DATABASE_URL="postgresql://claude_readonly:password@neon-host/todo_db"

# Verify connection
claude mcp list
# Should show: postgres: ✓ Connected
```

**Safe Operations**:
- ✅ SELECT queries for validation
- ✅ Schema inspection (DESCRIBE tables)
- ✅ COUNT queries for metrics

**Avoid**:
- ❌ INSERT/UPDATE/DELETE operations (use application code instead)
- ❌ Schema modifications (ALTER TABLE - use migrations)
- ❌ Exposing credentials in queries or logs

### Playwright MCP Security

**Safe Operations**:
- ✅ Navigate to localhost or known URLs
- ✅ Automated testing with test credentials
- ✅ Screenshot capture for debugging

**Avoid**:
- ❌ Storing production credentials in scripts
- ❌ Navigating to untrusted URLs
- ❌ Leaving browser context open with authenticated sessions

### Context7 MCP Security

**Safe Operations**:
- ✅ Fetch public documentation (no credentials needed)
- ✅ Query official library documentation
- ✅ Search for code examples

**No Security Concerns**: Read-only access to public documentation

---

## 📚 Common MCP Usage Patterns

### Pattern 1: Research → Implement → Test → Commit

```bash
# 1. Research with Context7
"What's the latest FastAPI OAuth2 implementation pattern?"

# 2. Implement based on documentation
# Write code in src/auth/oauth2.py

# 3. Test with Playwright (if web UI)
# Or pytest for backend

# 4. Commit with GitHub MCP
# Create branch: 007-oauth2-implementation
# Commit with spec reference: "Implement OAuth2 per FR-203 (spec:142)"
# Create PR linking to spec.md
```

### Pattern 2: Database Validation → Debug → Fix

```bash
# 1. Validate with PostgreSQL MCP
SELECT COUNT(*) FROM tasks WHERE user_id IS NULL;
# Result: 5 tasks with NULL user_id (BUG!)

# 2. Debug application code
# Check task creation endpoint

# 3. Fix validation logic
# Add non-null constraint validation

# 4. Re-validate with PostgreSQL MCP
SELECT COUNT(*) FROM tasks WHERE user_id IS NULL;
# Result: 0 tasks (FIXED!)

# 5. Commit fix with GitHub MCP
```

### Pattern 3: E2E Testing → Performance Measurement → Optimization

```bash
# 1. E2E test with Playwright
# Navigate to /tasks, measure load time

# 2. Measure performance
# Check Lighthouse scores, measure API latency

# 3. Optimize based on metrics
# Add caching, optimize queries, implement code splitting

# 4. Re-test with Playwright
# Verify improvements meet success criteria (Lighthouse ≥90, p95 <500ms)

# 5. Commit optimization with GitHub MCP
```

---

## ⚠️ MCP Limitations and Workarounds

| Limitation | Workaround |
|------------|-----------|
| **Context7**: May not have bleeding-edge (< 1 week old) docs | Use Playwright to browse official docs directly |
| **Playwright**: Cannot test mobile-native apps | Use web app responsive mode, or manual mobile testing |
| **PostgreSQL**: Requires credentials for each environment | Use separate read-only users per environment (dev/staging/prod) |
| **GitHub**: Rate limited to 5000 API calls/hour | Batch operations, use webhooks for notifications instead of polling |

---

## 📖 Next Steps

- **Phase I**: Use Context7 for Python 3.13+, SQLModel, pytest docs
- **Phase II**: Configure PostgreSQL MCP with Neon credentials (read-only user)
- **Phase III**: Use Context7 for OpenAI Agents SDK and MCP specification
- **Phase IV**: Use Context7 for Kubernetes, Docker, Ingress setup
- **Phase V**: Use Context7 for Dapr, Kafka, cloud provider documentation

**Configuration TODOs**:
- [ ] Set `GITHUB_TOKEN` environment variable for GitHub MCP (do this now)
- [ ] Set `DATABASE_URL` environment variable for PostgreSQL MCP (Phase II)
- [ ] Create read-only PostgreSQL user in Neon dashboard (Phase II)
- [ ] Test Playwright MCP with local Next.js dev server (Phase II)

---

**Last Updated**: 2025-12-08
**Related Files**:
- `specs/001-evolution-vision/spec.md` (MCP documentation in Dependencies section)
- `.claude.json` (MCP server configurations)
