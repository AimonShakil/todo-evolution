---
name: spec-workflow
description: Guide spec-driven development workflow (spec → plan → tasks → implement). Use when creating specifications, planning features, generating task lists, or implementing features. Constitutional requirement for all development.
allowed-tools: Read, Write, Glob, Grep, Edit
ri:
  - .specify/ri/skills/spec-writer/
  - .specify/ri/skills/architect/
  - .specify/ri/skills/phase-implementer/
---

# Spec Workflow Manager Skill

Orchestrates the spec-driven development process following Constitutional Principle I.

## Constitutional Workflow

```
spec.md → plan.md → tasks.md → implementation → testing
```

**MANDATORY**: No code may be written before spec.md exists.

## Stage 1: Specification Creation

### Input
- User feature description
- Project constitution
- Existing specs for patterns

### Process
1. Read template: `.specify/templates/spec-template.md`
2. Create `specs/<feature-name>/spec.md`
3. Include:
   - User scenarios with acceptance criteria
   - Edge cases
   - Non-functional requirements
   - Data model
   - API contracts (if applicable)
4. Validate: All acceptance scenarios are testable

### Verification
- Spec includes P1 (MVP) user stories
- Each scenario has Given/When/Then format
- Edge cases documented
- Spec aligns with constitution principles

### Tools
Use `/sp.specify` slash command if available, or create manually with template.

## Stage 2: Plan Development

### Input
- Completed spec.md
- Constitution principles
- Technology stack requirements

### Process
1. Read template: `.specify/templates/plan-template.md`
2. Create `specs/<feature-name>/plan.md`
3. Include:
   - Scope and dependencies
   - Key decisions with rationale
   - Interfaces and contracts
   - Non-functional requirements
   - Data management
   - Operational readiness
   - Risk analysis
   - **Constitution Check**: Map each decision to constitutional principles

### ADR Detection
Test each significant decision:
- **Impact**: Long-term consequences?
- **Alternatives**: Multiple options considered?
- **Scope**: Cross-cutting influence?

If ALL true, suggest (do NOT auto-create):
```
📋 Architectural decision detected: [brief]
   Document reasoning and tradeoffs? Run `/sp.adr [title]`
```

### Tools
Use `/sp.plan` slash command if available.

## Stage 3: Task Generation

### Input
- Completed plan.md
- Spec.md acceptance scenarios

### Process
1. Read template: `.specify/templates/tasks-template.md`
2. Create `specs/<feature-name>/tasks.md`
3. Include:
   - Atomic, testable tasks
   - Test cases for each task
   - Dependency order
   - Constitution compliance checks

### Validation
- Each task maps to spec acceptance scenario
- Tasks are atomic (smallest viable change)
- Test cases included
- No premature optimization

### Tools
Use `/sp.tasks` slash command if available.

## Stage 4: Implementation

### Input
- Completed tasks.md
- Constitution code standards

### Process
1. Read tasks.md
2. Execute tasks incrementally
3. For each task:
   - Write tests first (Red-Green-Refactor)
   - Implement minimal code
   - Validate against acceptance criteria
   - Run tests
   - Update tasks.md status

### Constitution Compliance
- Type hints (Python) / strict types (TypeScript)
- Docstrings / JSDoc
- User isolation (filter by user_id)
- Async I/O
- Input validation
- No secrets in code

### Tools
Use `/sp.implement` slash command if available.

## Stage 5: Validation & Review

### Checks
1. **Tests pass**: Coverage ≥ 80%
2. **Constitution compliance**: All 28 principles validated
3. **User isolation**: Cross-user access tests pass
4. **Code quality**: Linting, formatting, type checking pass
5. **Documentation**: README updated if needed

### Tools
- Run `pytest --cov` (Python) or `npm test -- --coverage` (TypeScript)
- Use constitution-check skill
- Use test-coverage skill
- Use code-quality skill

## Directory Structure

```
specs/<feature-name>/
├── spec.md           # Requirements (Stage 1)
├── plan.md           # Architecture (Stage 2)
├── tasks.md          # Implementation tasks (Stage 3)
├── data-model.md     # Optional: detailed schema
├── contracts/        # Optional: API contracts
├── checklists/       # Optional: custom checklists
└── research.md       # Optional: technical research
```

## Common Patterns

### New Feature Flow
```
User: "Add task priority feature"
  ↓
You: Read constitution, existing specs
  ↓
You: Create spec.md with user scenarios
  ↓
You: Create plan.md with architecture decisions
  ↓
You: Detect ADR significance, suggest if needed
  ↓
You: Create tasks.md with atomic tasks
  ↓
You: Implement incrementally with tests
  ↓
You: Create PHR after completion
```

### Bug Fix Flow
```
User: "Fix task deletion not working for user isolation"
  ↓
You: Read existing spec.md and plan.md
  ↓
You: Add bug scenario to spec.md
  ↓
You: Create tasks.md with fix tasks
  ↓
You: Write test exposing bug (Red)
  ↓
You: Fix bug (Green)
  ↓
You: Refactor if needed
  ↓
You: Create PHR after completion
```

## Workflow Validation Checklist

Before considering workflow complete:

- [ ] spec.md exists and is complete
- [ ] plan.md exists with architecture decisions
- [ ] tasks.md exists with testable tasks
- [ ] All tasks implemented and tested
- [ ] Tests pass with ≥80% coverage
- [ ] Constitution compliance validated
- [ ] ADR created if significant decisions made
- [ ] PHR created for session
- [ ] Git commit with conventional message

## MCP Server Integration

### Context7 (Library Documentation)
When planning or implementing, use context7 MCP server to fetch up-to-date documentation:
```
User: "Plan FastAPI authentication with Better Auth"
  ↓
You: Use mcp__context7__resolve-library-id for "fastapi" and "better-auth"
  ↓
You: Use mcp__context7__get-library-docs for API reference
  ↓
You: Include official patterns in plan.md
```

## Anti-Patterns to Avoid

❌ **Writing code before spec.md exists**
❌ **Skipping plan.md for "simple" features**
❌ **Creating tasks without acceptance criteria**
❌ **Implementing without tests**
❌ **Refactoring unrelated code**
❌ **Auto-creating ADRs without user consent**
❌ **Skipping PHR creation**

## Success Metrics

✅ Spec → Plan → Tasks → Code flow followed
✅ All acceptance scenarios have tests
✅ Constitution compliance validated
✅ ADRs created for significant decisions
✅ PHRs created for learning
✅ Zero user data isolation violations
