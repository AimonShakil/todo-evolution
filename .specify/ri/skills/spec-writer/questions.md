# Discovery Questions: Specification Writer

**Version**: 1.0.0
**Created**: 2025-12-11
**Last Updated**: 2025-12-11

---

## Purpose

These questions guide the **requirement elicitation** process. Use them to uncover:
- Hidden assumptions
- Edge cases
- Non-functional requirements
- Constitutional constraints
- Prioritization criteria

---

## Question Categories

### 1. Scoping Questions 🎯

**Purpose**: Define boundaries and context

#### Q1.1: What is the feature's primary value proposition?
- What problem does this feature solve?
- What pain point does it address?
- What outcome does the user expect?

**Example Answers**:
- "Users need to track completed tasks to measure productivity"
- "Users want to prioritize tasks to focus on what's important"

#### Q1.2: Who are the users?
- What user personas will use this feature?
- What is their skill level? (Beginner, intermediate, expert)
- What devices/platforms will they use? (Desktop, mobile, CLI)

**Example Answers**:
- "Individual users managing personal tasks via console app"
- "Technical users comfortable with CLI commands"

#### Q1.3: What are the boundaries (IN scope vs. OUT of scope)?
- What is explicitly INCLUDED in this feature?
- What is explicitly EXCLUDED?
- What is deferred to future phases?

**Example Answers**:
- IN: Add, view, complete, update, delete tasks
- OUT: Task sharing, team collaboration, attachments
- DEFERRED: Recurring tasks (Phase V), due dates (Phase V)

#### Q1.4: What phase is this for?
- Phase I (Console app - SQLite, Click CLI)
- Phase II (Web app - FastAPI, Next.js, Neon DB)
- Phase III (AI Chatbot - MCP, OpenAI Agents)
- Phase IV (Kubernetes - Minikube, Helm)
- Phase V (Cloud - Kafka, Dapr, advanced features)

**Why it matters**: Phase determines complexity, tech stack, and feature scope.

---

### 2. Requirement Questions 📋

**Purpose**: Define what success looks like

#### Q2.1: What does success look like?
- How does the user know the feature is working correctly?
- What is the visible outcome?
- What state changes occur?

**Example Answers**:
- "User sees task marked as complete with ✓ indicator"
- "Task list updates to show new task at bottom"

#### Q2.2: What are the priority levels?
- **P1 (MVP)**: Shippable alone; core value; must have
- **P2 (Important)**: Significantly improves UX; should have
- **P3 (Future)**: Nice-to-have; could have; deferred

**Example Answers**:
- P1: Add task, view tasks, mark complete
- P2: Update task title, delete task
- P3: Task descriptions, tags, priorities

#### Q2.3: What are the acceptance criteria?
- What specific conditions must be met?
- How can we objectively verify success?
- What observable outcomes confirm correctness?

**Example Answers**:
- "Task appears in database with user_id='alice' after add command"
- "CLI returns exit code 0 and success message"
- "Task count increases by 1 in view command output"

#### Q2.4: What workflows are involved?
- What are the step-by-step user actions?
- Are there dependencies on other features?
- What is the typical user journey?

**Example Answers**:
- User adds task → views task list → marks task complete → views updated list
- Requires: User authentication (console: --user flag)

---

### 3. Constraint Questions 🚧

**Purpose**: Identify non-negotiable requirements

#### Q3.1: What constitutional principles apply?
Review against all 28 principles:
- **Principle II (User Isolation)**: How is data scoped per user?
- **Principle VI (Database Standards)**: What tables/fields are needed?
- **Principle IX (Code Quality)**: What quality standards apply?
- **Principle X (Testing)**: What tests are required?
- **Principle XII (Security)**: What security measures are needed?

**Example Answers**:
- "All queries MUST filter by user_id (Principle II)"
- "Task model MUST include user_id, created_at, updated_at (Principle VI)"

#### Q3.2: What are the security requirements?
- **Authentication**: How are users identified? (JWT, CLI flag, etc.)
- **Authorization**: Who can access this feature? (User only? Admin?)
- **Data Protection**: What data is sensitive? (PII, credentials, etc.)
- **Input Validation**: What inputs need sanitization?

**Example Answers**:
- "User identity via --user flag (Phase I console)"
- "All queries filter by user_id to prevent cross-user access"
- "Title must be 1-200 characters; validate on input"

#### Q3.3: What are the performance targets?
- **Latency**: What is acceptable response time?
- **Throughput**: How many operations per second?
- **Scalability**: How many users? How many tasks per user?
- **Resource Limits**: Memory, CPU, storage constraints?

**Example Answers**:
- "CLI commands complete in <100ms (p95)"
- "Support 1000 tasks per user"
- "Database queries return in <50ms"

#### Q3.4: Are there compliance requirements?
- **GDPR**: Data export, deletion, consent?
- **Accessibility**: WCAG 2.1 AA compliance? (Phase II+ UI)
- **Audit Logging**: Track user actions?
- **Data Retention**: How long to keep data?

**Example Answers**:
- "Tasks stored indefinitely unless user deletes account"
- "User can export all tasks via CLI command (future P3)"

---

### 4. Error Handling & Edge Case Questions 🐛

**Purpose**: Uncover failure scenarios

#### Q4.1: What happens when things go wrong?
- What if the input is invalid?
- What if the resource doesn't exist?
- What if the user lacks permission?
- What if external services fail?

**Example Answers**:
- Invalid input → CLI returns error message and exit code 1
- Task not found → "Task 999 not found" error
- Cross-user access → "Task not found" (404, not 401 to avoid info disclosure)

#### Q4.2: What are the edge cases?
- **Empty Inputs**: What if user enters empty string?
- **Maximum Inputs**: What if title is 1000 characters?
- **Special Characters**: What if title has emojis, Unicode, SQL?
- **Empty State**: What if user has no tasks?
- **First Run**: What if database doesn't exist yet?

**Example Answers**:
- Empty title → Validation error "Title cannot be empty"
- Title >200 chars → Validation error "Title must be 1-200 characters"
- No tasks → "No tasks found" message (not an error)
- First run → Auto-create database file (todo.db)

#### Q4.3: What are the error messages?
- What does the user see when something fails?
- Are error messages actionable? (Tell user how to fix)
- Are error messages user-friendly? (No stack traces to user)

**Example Answers**:
- "✗ Task 999 not found" (clear, actionable)
- "✗ Title cannot be empty" (explains constraint)
- "✗ Database connection failed. Check todo.db permissions" (actionable)

#### Q4.4: What are the fallback behaviors?
- What happens if a feature partially fails?
- Can the user retry?
- Is data rolled back or partially committed?

**Example Answers**:
- Failed task creation → No partial data; transaction rolled back
- Network timeout → User can retry command; idempotent
- Database locked → Retry after 100ms (max 3 attempts)

---

### 5. Data & Integration Questions 💾

**Purpose**: Define data models and dependencies

#### Q5.1: What data needs to be stored?
- What entities are involved? (Tasks, Users, etc.)
- What fields are required? (title, completed, user_id, etc.)
- What relationships exist? (User has many Tasks)
- What constraints apply? (NOT NULL, UNIQUE, CHECK, etc.)

**Example Answers**:
- Task: id, user_id, title, completed, created_at, updated_at
- User: id, username (for Phase I CLI)
- Constraints: user_id NOT NULL, title 1-200 chars

#### Q5.2: What are the API contracts? (Phase II+)
- What endpoints are needed?
- What are the request/response formats?
- What status codes are returned?
- What are the rate limits?

**Example Answers**:
- POST /api/{user_id}/tasks - Create task (201 Created)
- GET /api/{user_id}/tasks - List tasks (200 OK)
- PATCH /api/{user_id}/tasks/{id} - Update task (200 OK)

#### Q5.3: What external dependencies exist?
- Does this feature depend on other features?
- Does it integrate with external services?
- What happens if dependencies are unavailable?

**Example Answers**:
- Depends on: User authentication (--user flag)
- No external services (Phase I is local)
- Database dependency: SQLite (bundled with Python)

#### Q5.4: What is the data volume?
- How many records per user?
- How fast does data grow?
- What are the storage requirements?

**Example Answers**:
- Assume: 100-1000 tasks per user
- Growth: 1-10 tasks per day per user
- Storage: ~1KB per task = 1MB per 1000 tasks

---

### 6. Risk & Assumption Questions ⚠️

**Purpose**: Identify hidden risks and assumptions

#### Q6.1: What assumptions are we making?
- About users (skill level, device, browser, etc.)
- About data (volume, format, quality)
- About infrastructure (availability, performance)

**Example Assumptions**:
- Users have Python 3.13+ installed
- Users are comfortable with CLI commands
- SQLite can handle 1000 tasks/user without performance issues

#### Q6.2: What could break?
- What are the integration points?
- What external dependencies could fail?
- What happens under high load?

**Example Risks**:
- SQLite file corruption (mitigation: backups)
- User enters SQL injection attempt (mitigation: ORM prevents)
- Disk full (mitigation: graceful error message)

#### Q6.3: What are the performance bottlenecks?
- Where could latency spike?
- What operations are expensive?
- What needs optimization?

**Example Bottlenecks**:
- Query without index on user_id (mitigation: add index)
- Loading 10,000 tasks at once (mitigation: pagination in Phase II+)

#### Q6.4: What's the migration path?
- How do we upgrade from Phase I to Phase II?
- Is the data model forward-compatible?
- Can users export/import data?

**Example Migration**:
- Phase I→II: Export SQLite to PostgreSQL (script provided)
- Data model: Task schema compatible across phases
- User data: Export to JSON for backup/migration

---

## Question Sequencing Strategy

**Start broad, then narrow**:

1. **Scoping** (Q1) → Understand the "what" and "who"
2. **Requirements** (Q2) → Define "done" and priorities
3. **Constraints** (Q3) → Identify non-negotiables
4. **Errors** (Q4) → Plan for failure
5. **Data** (Q5) → Model persistence
6. **Risks** (Q6) → Anticipate problems

**Example Flow**:
```
User: "I want to add task priorities"
  ↓
You: Q1.4 - "What phase is this for?" (Phase I console or Phase II web?)
  ↓
User: "Phase V (advanced features)"
  ↓
You: Q2.2 - "Is this P1 MVP, P2, or P3?" (Clarify priority)
  ↓
User: "P2 - important but not MVP"
  ↓
You: Q2.1 - "How many priority levels?" (Low/Med/High? 1-5 scale?)
  ↓
User: "3 levels: Low, Medium, High"
  ↓
You: Q5.1 - "Should we store as enum or string?" (Data model question)
  ↓
Write acceptance scenarios based on answers
```

---

## Anti-Patterns to Avoid

### ❌ Asking Everything Upfront
**Problem**: Overwhelming user with 50 questions
**Fix**: Ask sequencing questions (2-5 at a time), drill down based on answers

### ❌ Asking Open-Ended Questions
**Problem**: "Tell me about your priorities" (too vague)
**Fix**: "Do you need 3 priority levels (Low/Med/High) or 5 levels (1-5 scale)?"

### ❌ Assuming Without Clarifying
**Problem**: Assuming "priorities" means Low/Med/High
**Fix**: Ask explicitly: "How many levels? What are the labels?"

### ❌ Skipping Edge Cases
**Problem**: Only asking about happy path
**Fix**: Always ask Q4 (What happens when things go wrong?)

---

## Related Files

- **persona.md**: Role, expertise, communication style
- **principles.md**: Design principles and quality standards
- **README.md**: Aggregated P+Q+P guide with examples

## Version History

### v1.0.0 (2025-12-11)
- Initial question framework for Specification Writer
- Organized into 6 categories (Scoping, Requirements, Constraints, Errors, Data, Risks)
- Added sequencing strategy and anti-patterns
