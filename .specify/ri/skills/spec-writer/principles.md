# Design Principles: Specification Writer

**Version**: 1.0.0
**Created**: 2025-12-11
**Last Updated**: 2025-12-11

---

## Purpose

These principles guide **decision-making** when writing specifications. They ensure:
- Constitutional compliance (all 28 principles)
- Testability (every requirement verifiable)
- Clarity (no ambiguous terms)
- Completeness (all edge cases covered)

---

## 1. Quality Standards

### 1.1 Completeness Standard
**Principle**: Every user story has complete acceptance scenarios.

**Verification Checklist**:
- [ ] User story has "As a [user], I need [feature] so that [value]"
- [ ] At least 3 acceptance scenarios (happy path + edge cases)
- [ ] Each scenario has Given/When/Then format
- [ ] Edge cases documented with expected behavior
- [ ] Non-functional requirements specified (performance, security)

**Example**:
```markdown
## User Story 1: Add Task

**Description**: As a user, I need to add tasks to my list so that I can track work.

**Acceptance Scenarios**:
1. Given I am user "alice", When I add "Buy milk", Then task is created with id=1
2. Given I provide empty title, When I add task, Then error "Title cannot be empty"
3. Given I provide 201-char title, When I add task, Then error "Title must be 1-200 chars"
```

### 1.2 Testability Standard
**Principle**: Every acceptance scenario is objectively verifiable (pass/fail, no ambiguity).

**Verification**:
- Can a test assert this? → Yes ✅ (testable)
- Can two people disagree on outcome? → No ✅ (objective)

**Examples**:
- ✅ **Testable**: "Task count increases by 1" (objective: query database)
- ❌ **Not testable**: "UI looks good" (subjective: what is "good"?)
- ✅ **Testable**: "Button has bg-blue-500 class" (objective: inspect DOM)
- ❌ **Not testable**: "System is fast" (vague: how fast?)
- ✅ **Testable**: "Response time <500ms (p95)" (objective: measure latency)

### 1.3 Clarity Standard
**Principle**: No ambiguous terms without quantification.

**Ambiguous Terms to Avoid**:
| ❌ Ambiguous | ✅ Quantified |
|-------------|--------------|
| "fast" | "p95 latency <500ms" |
| "reliable" | "99.9% uptime SLO" |
| "secure" | "JWT auth with 1-hour expiry, TLS 1.2+" |
| "scalable" | "Supports 1000 concurrent users" |
| "user-friendly" | "Task creation in ≤3 clicks" |
| "responsive" | "Mobile breakpoint at 640px (Tailwind default)" |

**Example Transformation**:
```markdown
❌ BAD: "The system should be fast and reliable."

✅ GOOD:
"Performance Requirements:
- API latency: p50 <100ms, p95 <500ms, p99 <1000ms
- Throughput: 100 requests/second sustained
- Availability: 99.9% uptime (max 43 minutes downtime/month)"
```

### 1.4 Traceability Standard
**Principle**: Every requirement maps to constitutional principles and test cases.

**Verification**:
- Each user story → maps to constitutional principle(s)
- Each acceptance scenario → maps to test case
- Each edge case → maps to error handling test

**Example**:
```markdown
## User Story 2: View Tasks (Priority: P1)

**Constitutional Alignment**:
- Principle II (User Isolation): All queries filter by user_id ✅
- Principle IX (Code Quality): Type hints, docstrings required ✅
- Principle X (Testing): Requires test_view_tasks() with 80% coverage ✅

**Test Cases Required**:
- test_view_tasks_returns_user_tasks()
- test_view_tasks_excludes_other_user_tasks() ← User isolation
- test_view_empty_task_list()
- test_view_with_1000_tasks() ← Performance edge case
```

---

## 2. Specification Structure Standards

### 2.1 User Story Format
**Template**:
```markdown
## User Story [N]: [Feature Name] (Priority: P1/P2/P3) [🎯 MVP if P1]

**Description**: As a [user persona], I need [feature] so that [value/benefit].

**Why this priority**: [Justification for P1/P2/P3 classification]

**Independent Test**: [How to test this story in isolation]

**Acceptance Scenarios**:
1. **Given** [context], **When** [action], **Then** [outcome]
2. **Given** [error condition], **When** [action], **Then** [error handling]
```

### 2.2 Priority Classification
**P1 (MVP) - Must Have**:
- Shippable alone (provides core value)
- Users can accomplish primary use case
- Without this, product has no purpose
- Example: "Add task" (without this, it's not a todo app)

**P2 (Important) - Should Have**:
- Significantly improves UX
- Users can work around absence (inconvenient but possible)
- Adds meaningful value but not blocking
- Example: "Update task title" (users can delete + re-add as workaround)

**P3 (Future) - Could Have**:
- Nice-to-have; deferred to later phases
- Enhances experience but not essential
- Can be added post-MVP without rework
- Example: "Task descriptions" (title alone is sufficient for MVP)

### 2.3 Edge Case Documentation
**Required Sections**:
1. **Empty State**: What if there's no data?
2. **Maximum Input**: What if input exceeds limits?
3. **Invalid Input**: What if input is malformed?
4. **Permission Denied**: What if user lacks access?
5. **External Failure**: What if dependency fails?

**Example**:
```markdown
### Edge Cases

#### 1. Empty Database on First Run
- **Scenario**: User runs app for first time, no database file exists.
- **Handling**: Auto-create `todo.db` SQLite file, initialize schema.
- **Test**: test_first_run_creates_database()

#### 2. Task Not Found
- **Scenario**: User tries to complete task ID 999 (doesn't exist).
- **Handling**: Return error "Task 999 not found", exit code 1.
- **Test**: test_complete_nonexistent_task_returns_error()

#### 3. Cross-User Access Attempt
- **Scenario**: User "alice" tries to delete task owned by "bob".
- **Handling**: Return error "Task not found" (404, not 401 to avoid info disclosure).
- **Test**: test_cross_user_delete_blocked()
```

---

## 3. Constitutional Alignment Principles

### 3.1 Principle II: User Data Isolation (CRITICAL)
**Requirement**: All specs MUST define how data is scoped per user.

**Specification Checklist**:
- [ ] Data model includes `user_id` field (indexed)
- [ ] All queries documented to filter by `user_id`
- [ ] Cross-user access scenarios documented (must be blocked)
- [ ] User isolation test cases specified

**Example**:
```markdown
## Data Model: Task

**Fields**:
- id: Primary key (auto-increment)
- user_id: Foreign key to users (indexed, NOT NULL) ← User isolation
- title: Task title (1-200 chars)
- completed: Boolean (default: false)
- created_at: Timestamp (auto-generated)
- updated_at: Timestamp (auto-updated)

**Indexes**:
- PRIMARY KEY (id)
- INDEX (user_id, completed) ← Composite index for common query

**User Isolation Requirement**:
ALL queries MUST filter by user_id:
```sql
SELECT * FROM tasks WHERE user_id = 'alice'  -- ✅ GOOD
SELECT * FROM tasks                          -- ❌ VIOLATION
```
```

### 3.2 Principle VI: Database Standards
**Requirements**:
- SQLModel ORM only (no raw SQL)
- All models include: `id`, `user_id`, `created_at`, `updated_at`
- Indexes on: `user_id`, frequently queried columns
- Foreign key constraints enforced

**Specification Template**:
```markdown
## Data Model: [Entity Name]

**Table**: [table_name]

**Fields**:
- id: Optional[int] = Field(default=None, primary_key=True)
- user_id: str = Field(index=True, foreign_key="users.id")
- created_at: datetime = Field(default_factory=datetime.utcnow)
- updated_at: datetime = Field(default_factory=datetime.utcnow)
- [entity-specific fields...]

**Indexes**:
- INDEX (user_id, [frequently_queried_field])

**Constraints**:
- user_id: NOT NULL
- [field]: CHECK constraint (if applicable)
```

### 3.3 Principle IX: Code Quality
**Requirements in Spec**:
- Specify input validation rules (enables type hints, docstrings)
- Define error messages (clear, actionable)
- Document expected behavior (enables quality tests)

**Example**:
```markdown
## Input Validation

**Title Field**:
- Type: String
- Min Length: 1 character (after trimming whitespace)
- Max Length: 200 characters
- Validation: Trim leading/trailing whitespace before storage
- Error Message: "Title cannot be empty" (if empty after trim)
- Error Message: "Title must be 1-200 characters" (if >200 chars)
```

### 3.4 Principle X: Testing Requirements
**Specification MUST enable 80% test coverage**.

**Required Test Categories in Spec**:
1. **Happy Path Tests**: Normal user flow (add → view → complete)
2. **User Isolation Tests**: Cross-user access blocked
3. **Validation Tests**: Empty input, max length, invalid characters
4. **Error Handling Tests**: Not found, unauthorized, server error
5. **Edge Case Tests**: Empty database, first run, Unicode characters

**Example**:
```markdown
## Test Requirements

**Unit Tests** (90% coverage target):
- test_validate_task_title_empty()
- test_validate_task_title_too_long()
- test_validate_task_title_valid()

**Integration Tests** (80% coverage target):
- test_create_task_success()
- test_create_task_with_invalid_title()
- test_user_cannot_view_other_user_tasks() ← User isolation

**E2E Tests** (Happy path minimum):
- test_user_can_add_view_complete_delete_task()
```

### 3.5 Principle XII: Security
**Specification MUST define security requirements**.

**Required Sections**:
1. **Authentication**: How users are identified
2. **Authorization**: Who can access what
3. **Input Validation**: What inputs are sanitized
4. **Data Protection**: What data is sensitive

**Example**:
```markdown
## Security Requirements

**Authentication** (Phase I - Console):
- User identity via `--user <username>` CLI flag
- No password required (local single-user app)
- Phase II+: JWT authentication with Better Auth

**Authorization**:
- Users can ONLY access their own tasks
- ALL queries filter by user_id (enforced in code)
- Cross-user access attempts return "Not Found" (404)

**Input Validation**:
- Task title: Sanitize HTML/SQL (SQLModel ORM prevents SQL injection)
- Username: Alphanumeric + underscore + hyphen only (Phase II+)

**Data Protection**:
- Task data is NOT sensitive (no PII, no financial data)
- User credentials: Not stored in Phase I (CLI flag only)
- Database file: Local `todo.db` (file system permissions apply)
```

### 3.6 Principle XVIII: Performance Standards
**Specification MUST include measurable performance targets**.

**Required Metrics**:
- **Latency**: p50, p95, p99 response times
- **Throughput**: Requests per second
- **Scalability**: Max users, max tasks per user
- **Resource Limits**: Memory, CPU, storage

**Example**:
```markdown
## Performance Requirements

**Latency Targets** (Phase I - Console):
- Add task: <50ms (p95)
- View tasks: <100ms (p95) for 1000 tasks
- Complete task: <50ms (p95)
- Update task: <50ms (p95)
- Delete task: <50ms (p95)

**Scalability Targets**:
- Max tasks per user: 10,000
- Max users: Unlimited (local database per user)

**Database Performance**:
- Query time: <10ms for indexed queries
- Insert time: <5ms per task

**Load Testing** (Phase V):
- 100 concurrent users
- 10 requests/second sustained
- 95% of requests <500ms
```

---

## 4. Preferred Patterns

### 4.1 User-Centric Design
**Principle**: Start with user value, not technical implementation.

**Process**:
1. Identify user persona (who)
2. Define user goal (what they want to achieve)
3. Describe user benefit (why they want it)
4. Specify observable outcome (how they know it worked)

**Example**:
```markdown
❌ BAD (Implementation-focused):
"Implement SQLite database with Task table and CRUD operations."

✅ GOOD (User-focused):
"As a user, I need to add tasks to a list so that I can track my work.
When I add a task, it is saved persistently and appears in my task list."
```

### 4.2 Incremental Delivery
**Principle**: P1 (MVP) should be shippable alone.

**Test**: Can users accomplish core use case with P1 only?

**Example**:
```markdown
✅ GOOD P1 (Shippable):
- Add task
- View tasks
- Mark complete

P2 (Enhances P1):
- Update task title
- Delete task

P3 (Nice-to-have):
- Task descriptions
- Tags, priorities
```

### 4.3 Explicit Over Implicit
**Principle**: State assumptions, don't leave them hidden.

**Required Sections**:
- **Assumptions**: What we're assuming about users, data, infrastructure
- **Out of Scope**: What we're explicitly NOT doing
- **Future Considerations**: What we might add later

**Example**:
```markdown
## Assumptions

1. Users have Python 3.13+ installed
2. Users are comfortable with CLI commands
3. Tasks are text-based (no attachments, images, etc.)
4. Single-user per machine (no multi-user auth in Phase I)
5. Database fits on local disk (<1GB)

## Out of Scope (Phase I)

- Task sharing / collaboration
- Cloud sync
- Mobile app
- Web UI
- User authentication (Phase II+)
```

### 4.4 Error-First Design
**Principle**: Design for failure, not just success.

**Process**:
1. Write happy path scenario
2. For each step, ask: "What could go wrong?"
3. Document error handling for each failure mode

**Example**:
```markdown
## Happy Path:
Given I am user "alice", When I add task "Buy milk", Then task is created.

## Error Paths:
1. **Empty title**: When I add task "", Then error "Title cannot be empty"
2. **Title too long**: When I add task with 201 chars, Then error "Title must be 1-200 characters"
3. **Database locked**: When database is locked by another process, Then retry 3 times, then error "Database unavailable"
4. **Disk full**: When disk is full, Then error "Cannot save task: disk full"
```

---

## 5. Hard Constraints (Non-Negotiable)

### 5.1 No Code Before Spec
**Constraint**: Spec must be approved before implementation starts.

**Process**:
1. Write spec.md
2. Review with stakeholders
3. Validate constitutional compliance
4. **ONLY THEN**: Hand off to Architect for plan.md

### 5.2 Constitutional Compliance Mandatory
**Constraint**: All 28 constitutional principles must be validated.

**Verification**:
- [ ] Principle I: Spec exists before code
- [ ] Principle II: User isolation defined
- [ ] Principle VI: Database standards followed
- [ ] Principle IX: Code quality enabled
- [ ] Principle X: Testing requirements specified
- [ ] Principle XII: Security requirements defined
- [ ] Principle XVIII: Performance targets specified
- [All 28 principles checked...]

### 5.3 No Ambiguity Tolerance
**Constraint**: If two people could interpret differently, it's ambiguous (must clarify).

**Test**: Ask colleague to read spec. Can they implement without asking questions?

**Examples of Ambiguity**:
- ❌ "System should be fast" (How fast? What metric?)
- ❌ "Users can manage tasks" (What operations? Create? Update? Delete?)
- ❌ "Handle errors gracefully" (What errors? How to handle?)

### 5.4 User Isolation Non-Negotiable
**Constraint**: ZERO tolerance for cross-user data leakage.

**Specification MUST**:
- Define user_id in data model
- Specify user_id filtering in all queries
- Document cross-user access tests
- Include error handling for access violations

**Violation Example**:
```markdown
❌ CRITICAL VIOLATION:
"Users can view tasks" (Missing: "Users can view THEIR OWN tasks ONLY")

✅ CORRECT:
"Users can view their own tasks. Cross-user access is blocked.
Attempting to access another user's task returns 'Task not found'."
```

---

## 6. Anti-Patterns to Avoid

### ❌ 6.1 Over-Specification (Implementation Bias)
**Problem**: Spec dictates HOW instead of WHAT.

**Example**:
```markdown
❌ BAD: "Use Redis cache with 5-minute TTL to store task lists."
✅ GOOD: "Task list queries should complete in <100ms (p95).
Cache responses to reduce database load (target: 90% cache hit rate)."
```

### ❌ 6.2 Unmeasurable Requirements
**Problem**: No objective verification possible.

**Example**:
```markdown
❌ BAD: "System should perform well under load."
✅ GOOD: "System must handle 100 concurrent users with p95 latency <500ms."
```

### ❌ 6.3 Missing Edge Cases
**Problem**: Only happy path specified.

**Example**:
```markdown
❌ BAD: "User can delete tasks."
✅ GOOD:
- Happy path: User deletes task ID 5, task removed
- Error: Task ID 999 doesn't exist → error "Task not found"
- Error: User "alice" tries to delete task owned by "bob" → error "Task not found"
```

### ❌ 6.4 Implicit Assumptions
**Problem**: Hidden assumptions not documented.

**Example**:
```markdown
❌ BAD: "User adds task" (Assumes: user is authenticated, database exists, input is valid)
✅ GOOD:
"Given user 'alice' is authenticated via --user flag,
And database is initialized,
When user adds task 'Buy milk' (valid 1-200 char title),
Then task is created with user_id='alice'."
```

---

## Version History

### v1.0.0 (2025-12-11)
- Initial principles for Specification Writer
- Established quality standards (completeness, testability, clarity, traceability)
- Defined specification structure standards
- Documented constitutional alignment principles
- Created preferred patterns and hard constraints
- Listed anti-patterns to avoid

---

## Related Files

- **persona.md**: Role, expertise, communication style
- **questions.md**: Discovery questions for requirement gathering
- **README.md**: Aggregated P+Q+P guide with examples

## Constitutional Alignment

These principles enforce:
- **Principle I**: Spec-Driven Development
- **Principle II**: User Data Isolation
- **Principle VI**: Database Standards
- **Principle IX**: Code Quality
- **Principle X**: Testing Requirements
- **Principle XII**: Security
- **Principle XVIII**: Performance Standards
