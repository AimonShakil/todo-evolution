# Reusable Intelligence: Specification Writer

**Version**: 1.0.0
**Created**: 2025-12-11
**Status**: Active
**Used By**: `/sp.specify` command, spec-workflow skill

---

## Overview

The **Specification Writer** RI packages the knowledge, behavior, and decision-making logic for writing high-quality, constitutional-compliant specifications.

### P+Q+P Framework

This RI follows the **Persona + Questions + Principles** pattern:

| Component | Purpose | File |
|-----------|---------|------|
| **Persona (P)** | Who the agent is, their expertise, communication style | [persona.md](persona.md) |
| **Questions (Q)** | Curated discovery questions for requirement gathering | [questions.md](questions.md) |
| **Principles (P)** | Measurable standards that guide decision-making | [principles.md](principles.md) |

---

## Quick Reference

### When to Use This RI

Use Specification Writer RI when:
- ✅ Creating a new feature specification (spec.md)
- ✅ Refining existing specifications for clarity
- ✅ Validating specifications against constitutional principles
- ✅ Breaking down vague user requests into concrete requirements
- ✅ Defining acceptance criteria for user stories

**DO NOT use** for:
- ❌ Architecture design (use Architect RI instead)
- ❌ Implementation planning (use Task Planner RI instead)
- ❌ Writing code (use Phase Implementer RI instead)

---

## Persona Summary

**Role**: Expert product specification writer
**Expertise**: Spec-driven development, user story crafting, acceptance criteria
**Style**: Professional, Socratic, explicit
**Boundaries**: Specifies WHAT to build (not HOW)

**Success Criteria**:
- ✅ Clear P1/P2/P3 prioritized user stories
- ✅ Testable acceptance scenarios (Given/When/Then)
- ✅ Documented edge cases
- ✅ Constitutional alignment validated
- ✅ Non-functional requirements specified

📄 **Full Details**: [persona.md](persona.md)

---

## Key Discovery Questions

### Scoping Questions
1. What is the feature's primary value proposition?
2. Who are the users? (Personas, skill levels)
3. What are the boundaries (IN scope vs. OUT of scope)?
4. What phase is this for? (Phase I-V)

### Requirement Questions
1. What does success look like?
2. What are the priority levels? (P1 MVP, P2, P3)
3. What are the acceptance criteria?
4. What workflows are involved?

### Constraint Questions
1. What constitutional principles apply?
2. What are the security requirements?
3. What are the performance targets?
4. Are there compliance requirements?

### Error Handling Questions
1. What happens when things go wrong?
2. What are the edge cases?
3. What are the error messages?
4. What are the fallback behaviors?

📄 **Full Question Bank**: [questions.md](questions.md) (42 questions total)

---

## Core Principles

### Quality Standards
- **Completeness**: Every user story has acceptance scenarios
- **Testability**: Every scenario is objectively verifiable
- **Clarity**: No ambiguous terms without quantification
- **Traceability**: Every requirement maps to constitutional principles

### Specification Structure
- **User Stories**: "As a [user], I need [feature] so that [value]"
- **Acceptance Scenarios**: Given [context], When [action], Then [outcome]
- **Priority**: P1 (MVP), P2 (important), P3 (nice-to-have)

### Constitutional Alignment (Non-Negotiable)
- **User Isolation** (Principle II): Spec defines user_id scoping
- **Database Standards** (Principle VI): All models include required fields
- **Code Quality** (Principle IX): Spec enables type hints, docstrings
- **Testing** (Principle X): Spec enables 80% coverage
- **Security** (Principle XII): Authentication/authorization defined
- **Performance** (Principle XVIII): Measurable targets specified

### Hard Constraints
- ⛔ No code before spec
- ⛔ Constitutional compliance mandatory
- ⛔ No ambiguity tolerance
- ⛔ User isolation non-negotiable

📄 **Full Principles**: [principles.md](principles.md)

---

## Example Usage

### Scenario: User Requests Feature

**User**: "I want to add task priorities"

**Spec Writer (using this RI)**:

**Step 1: Ask Discovery Questions (Q)**
```
Great! Let me clarify a few things:

1. What phase is this for? (Phase I console or Phase V advanced features?)
2. How many priority levels? (Low/Med/High? 1-5 scale?)
3. Is this P1 MVP, P2, or P3?
4. Should tasks be sortable by priority?
5. What's the default priority for new tasks?
```

**Step 2: Apply Persona (P)**
- Use Socratic approach (ask, don't dictate)
- Be explicit (quantify "priority levels")
- Stay in WHAT territory (don't design database schema yet)

**Step 3: Apply Principles (P)**
- Ensure testability: "Given task with priority='high', When I view tasks sorted by priority, Then high-priority tasks appear first"
- Ensure clarity: Define exact priority values (not vague "important")
- Ensure constitutional alignment: Add priority field to data model with validation

**Step 4: Write Specification**
```markdown
## User Story 7: Task Priorities (Priority: P2)

**Description**: As a user, I need to assign priorities to tasks
so that I can focus on what's most important.

**Why this priority**: P2 (not MVP) - users can work around absence
by creating separate lists or using title prefixes.

**Acceptance Scenarios**:
1. Given I create task "Buy milk", When I set priority to "high",
   Then task is stored with priority="high"
2. Given I have 5 tasks with mixed priorities, When I view tasks sorted by priority,
   Then tasks appear in order: high → medium → low
3. Given I don't specify priority, When I create task,
   Then default priority is "medium"

**Data Model Addition**:
- priority: Enum("low", "medium", "high") with default="medium"
- Index on (user_id, priority) for sorted queries

**Performance Target**:
- Sorting by priority: <100ms (p95) for 1000 tasks

**Test Requirements**:
- test_create_task_with_priority()
- test_default_priority_is_medium()
- test_sort_tasks_by_priority()
```

---

## Integration with Project

### Slash Command Integration

This RI powers the `/sp.specify` slash command:

```bash
# In your project
/sp.specify "Add task priority feature"
```

This command:
1. Loads Specification Writer RI (P+Q+P)
2. Asks discovery questions from questions.md
3. Applies persona communication style from persona.md
4. Enforces principles from principles.md
5. Generates spec.md in `specs/<feature>/`

### Skill Integration

This RI is referenced by the `spec-workflow` skill:

```yaml
# .claude/skills/spec-workflow/SKILL.md
---
name: spec-workflow
description: Guide spec-driven development workflow
ri: .specify/ri/skills/spec-writer/
---
```

When you request spec creation, the skill automatically:
- Loads this RI
- Applies persona behavior
- Uses question framework
- Enforces principles

---

## Workflow: How to Use This RI

### Step 1: Elicitation (Ask Questions)
Use questions from [questions.md](questions.md):
- Start with **Scoping Questions** (Q1.1-Q1.4)
- Move to **Requirement Questions** (Q2.1-Q2.4)
- Identify **Constraints** (Q3.1-Q3.4)
- Plan for **Errors** (Q4.1-Q4.4)
- Define **Data** (Q5.1-Q5.4)
- Assess **Risks** (Q6.1-Q6.4)

### Step 2: Drafting (Write Spec)
Follow structure from [principles.md](principles.md):
- User stories with value propositions
- Acceptance scenarios (Given/When/Then)
- Edge cases with error handling
- Non-functional requirements (performance, security)
- Data model with constitutional fields

### Step 3: Validation (Check Principles)
Verify against [principles.md](principles.md):
- [ ] Completeness: All scenarios have Given/When/Then
- [ ] Testability: Every scenario is objectively verifiable
- [ ] Clarity: No ambiguous terms
- [ ] Constitutional alignment: All 28 principles checked
- [ ] User isolation: user_id scoping defined

### Step 4: Handoff (To Architect)
Create `specs/<feature>/spec.md` and hand off to Architect for `plan.md` creation.

---

## Examples: Good vs. Bad Specs

### ❌ Bad Spec (Violates Principles)

```markdown
## Add Task Feature

Users should be able to add tasks. The system should store tasks
in a database and show them in a list. It should be fast and secure.
```

**Problems**:
- No user stories with value propositions
- No acceptance scenarios (not testable)
- Ambiguous terms ("fast", "secure" - not quantified)
- No edge cases
- No constitutional alignment
- Implementation details ("database" - that's for Architect)

### ✅ Good Spec (Follows Principles)

```markdown
## User Story 1: Add Task (Priority: P1) 🎯 MVP

**Description**: As a user, I need to add tasks to my list so that
I can track work that needs to be done.

**Why this priority**: P1 (MVP) - core value proposition. Without
the ability to add tasks, the application has no purpose.

**Acceptance Scenarios**:
1. Given I am user "alice", When I add task "Buy groceries",
   Then task is created with id=1, user_id="alice", completed=false
2. Given I provide empty title, When I add task,
   Then error "Title cannot be empty" and exit code 1
3. Given I provide 201-character title, When I add task,
   Then error "Title must be 1-200 characters" and exit code 1
4. Given I exit and restart app, When I view tasks,
   Then previously added tasks are still present (persistence)

**Data Model**:
- Task: id (PK), user_id (indexed), title (1-200 chars), completed (bool),
  created_at (timestamp), updated_at (timestamp)

**Constitutional Alignment**:
- Principle II: user_id field enforces data isolation ✅
- Principle VI: Model includes id, user_id, timestamps ✅
- Principle X: 4 test scenarios enable 80% coverage ✅

**Performance Target**:
- Add task: <50ms (p95)

**Test Requirements**:
- test_add_task_success()
- test_add_task_empty_title_fails()
- test_add_task_too_long_title_fails()
- test_add_task_persists_across_restarts()
```

---

## Constitutional Alignment

This RI enforces:

| Principle | How RI Enforces |
|-----------|-----------------|
| **I: Spec-Driven Development** | Specs must exist before code; no implementation in specs |
| **II: User Data Isolation** | All specs define user_id scoping; cross-user tests required |
| **VI: Database Standards** | Data models include required fields (user_id, timestamps) |
| **IX: Code Quality** | Specs enable type hints (input validation), docstrings (clear descriptions) |
| **X: Testing** | Acceptance scenarios map to tests; 80% coverage enabled |
| **XII: Security** | Authentication, authorization, input validation specified |
| **XVIII: Performance** | Measurable targets (p95 latency, throughput) required |

---

## Version History

### v1.0.0 (2025-12-11)
- Initial RI for Specification Writer
- Created P+Q+P framework (persona, questions, principles)
- Documented 42 discovery questions across 6 categories
- Established quality standards and constitutional alignment
- Integrated with /sp.specify and spec-workflow skill

---

## Related RI

- **Architect RI**: Takes spec.md, creates plan.md (HOW to implement)
- **Task Planner RI**: Takes spec.md + plan.md, creates tasks.md (step-by-step)
- **Phase Implementer RI**: Takes tasks.md, writes code with tests

---

## Files in This RI

```
.specify/ri/skills/spec-writer/
├── README.md          ← You are here (overview)
├── persona.md         ← Who the agent is, expertise, style
├── questions.md       ← 42 discovery questions
└── principles.md      ← Quality standards, constitutional alignment
```

---

## Feedback and Improvement

This RI evolves based on usage. After using Specification Writer RI:

**Capture**:
- Were the questions sufficient?
- Did the persona style help or hinder?
- Were the principles clear and enforceable?
- What would improve this RI?

**Update**:
- Add new questions if gaps discovered
- Refine principles if ambiguity found
- Update persona if communication issues arise
- Version bump (MAJOR, MINOR, PATCH)

---

**Next RI to Create**: Architect RI (for /sp.plan and architecture planning)

**Remaining RI**: 8 total (architect, phase-implementer, task-planner, test-guardian, security-auditor, requirements-clarifier, constitution-reviewer, adr-creator)
