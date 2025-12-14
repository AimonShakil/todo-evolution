---
id: 007
title: Reusable Intelligence (RI) Setup - P+Q+P Framework
stage: misc
date: 2025-12-12
surface: agent
model: claude-sonnet-4-5
feature: none
branch: 002-phase-i-console-app
user: aimon
command: general
labels: ["reusable-intelligence", "p+q+p-framework", "spec-writer", "architect", "phase-implementer", "project-setup"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/ri/skills/spec-writer/persona.md
  - .specify/ri/skills/spec-writer/questions.md
  - .specify/ri/skills/spec-writer/principles.md
  - .specify/ri/skills/spec-writer/README.md
  - .specify/ri/skills/architect/persona.md
  - .specify/ri/skills/architect/questions.md
  - .specify/ri/skills/architect/principles.md
  - .specify/ri/skills/architect/README.md
  - .specify/ri/skills/phase-implementer/persona.md
  - .specify/ri/skills/phase-implementer/questions.md
  - .specify/ri/skills/phase-implementer/principles.md
  - .specify/ri/skills/phase-implementer/README.md
  - .claude/skills/spec-workflow/SKILL.md (updated with RI references)
  - .claude/agents/phase-implementer.md (updated with RI reference)
  - .claude/commands/sp.specify.md (updated with RI reference)
  - .claude/commands/sp.plan.md (updated with RI reference)
  - .claude/commands/sp.implement.md (updated with RI reference)
tests:
  - No tests created (infrastructure setup)
---

## Prompt

User continued from previous conversation summary and requested:

1. **Initial continuation**: "continue with option 1" (meaning: complete remaining 2 RI - architect and phase-implementer)

2. **After architect and phase-implementer RI creation**: "from next step complete step 1 and 2 and then share the next steps"
   - Step 1: Link RI to existing skills and subagents
   - Step 2: Create PHR for RI setup

**Context from Summary**:
- User had previously chosen "Option B" to create top 3 critical RI (spec-writer, architect, phase-implementer)
- User emphasized: "remember it your self when we will be applying rest of the RI don not forget so that we get best ot the project"
- Spec-writer RI was already completed (1 of 3)
- User wanted to complete remaining 2 RI before Phase I implementation

## Response snapshot

### Reusable Intelligence (RI) Created

**Created 3 complete RI packages** using P+Q+P (Persona + Questions + Principles) framework:

#### 1. Spec Writer RI (`.specify/ri/skills/spec-writer/`)
**Purpose**: Transform vague user requests into concrete, testable specifications (spec.md)

**Files** (4):
- `persona.md` - Expert product specification writer (Socratic, explicit, 10+ years experience)
- `questions.md` - 42 discovery questions across 6 categories (Scoping, Requirements, Constraints, Errors, Data, Risks)
- `principles.md` - Quality standards (completeness, testability, clarity, traceability), constitutional alignment
- `README.md` - Aggregated P+Q+P guide with examples

**Key Capabilities**:
- Socratic requirement elicitation (ask, don't dictate)
- Given/When/Then acceptance scenarios
- P1/P2/P3 prioritization (MVP vs. important vs. future)
- Constitutional compliance (28 principles)
- Edge case identification

**Example Question Flow**:
```
Q1.4: "What phase is this for?" → Phase I console
  ↓
Q2.2: "Is this P1 MVP, P2, or P3?" → P2
  ↓
Q2.1: "How many priority levels?" → Low/Med/High
  ↓
Write acceptance scenarios with testable criteria
```

#### 2. Architect RI (`.specify/ri/skills/architect/`)
**Purpose**: Create robust architectural plans (plan.md) from specifications

**Files** (4):
- `persona.md` - Expert software architect (15+ years, cloud-native, distributed systems)
- `questions.md` - 24 architecture questions across 6 categories (Technology, API, Data, NFRs, Integration, Risks)
- `principles.md` - Technology selection (alternatives/tradeoffs), API design (RESTful, user-scoped), data modeling (constitutional fields, indexes), NFR standards (p95 latency, uptime SLO), ADR criteria (3-part test)
- `README.md` - Aggregated P+Q+P guide with examples

**Key Capabilities**:
- Technology stack selection with documented alternatives and tradeoffs
- API contract specification (RESTful conventions, user_id scoping)
- Data model design (constitutional fields: id, user_id, created_at, updated_at)
- NFR quantification (p50/p95/p99 latency, throughput, uptime SLO, cost budgets)
- ADR creation (3-part test: impact + alternatives + scope = ALL true → create ADR)

**Example Decision Template**:
```markdown
## Database: PostgreSQL (Neon DB)

### Options Considered:
1. SQLite (Phase I incumbent)
2. PostgreSQL (Neon DB) - CHOSEN
3. MongoDB Atlas

### Decision Rationale:
- ACID guarantees (task completion consistency)
- SQLModel ORM (constitutional requirement)
- Phase II scalability (multi-user web app)

### Trade-offs:
- ✅ ACID, managed service, mature replication
- ❌ Higher cost ($20/month vs. $0) - Acceptable for production
- ❌ Vendor lock-in - Mitigated: standard PostgreSQL

### ADR: history/adr/004-database-postgresql-neon.md
```

#### 3. Phase Implementer RI (`.specify/ri/skills/phase-implementer/`)
**Purpose**: Translate architectural plans into production-ready code with TDD

**Files** (4):
- `persona.md` - Expert software implementer (TDD specialist, 10+ years, Python/TypeScript)
- `questions.md` - 24 implementation questions across 6 categories (Pre-Implementation, TDD, Code Structure, Constitutional, Refactoring, Performance)
- `principles.md` - TDD standards (red-green-refactor), coverage (≥80%), code quality (DRY, SOLID, complexity ≤10), security (validation, no secrets, SQL injection prevention), Git commit standards (conventional commits)
- `README.md` - Aggregated P+Q+P guide with examples

**Key Capabilities**:
- Test-Driven Development (red-green-refactor cycle - MANDATORY)
- Coverage ≥80% (Constitutional Principle X)
- User isolation enforcement (Principle II - SECURITY CRITICAL, ALL queries filter by user_id)
- Type safety + docstrings (Principle IX, mypy --strict passes)
- Constitutional compliance validation (28 principles enforced in code)

**TDD Workflow Example**:
```python
# STEP 1: RED (Write Failing Test)
def test_create_task_with_valid_title(test_db):
    task = create_task(user_id="alice", title="Buy milk")
    assert task.title == "Buy milk"
    # Run test → FAILS ✅

# STEP 2: GREEN (Minimum Implementation)
def create_task(user_id: str, title: str) -> Task:
    return Task(user_id=user_id, title=title)
    # Run test → PASSES ✅

# STEP 3: REFACTOR (Add Validation, Docstrings)
def create_task(user_id: str, title: str) -> Task:
    """Create a new task with validation.

    Args:
        user_id: User ID (not empty)
        title: Task title (1-200 chars)

    Returns:
        Task: Created task

    Raises:
        ValidationError: If title invalid
    """
    _validate_user_id(user_id)
    _validate_title(title)
    return Task(user_id=user_id, title=title)
    # Run test → STILL PASSES ✅
```

### Integration with Project

**RI Linked to**:
1. **spec-workflow skill** → References all 3 RI (spec-writer, architect, phase-implementer)
2. **phase-implementer subagent** → References phase-implementer RI
3. **/sp.specify command** → References spec-writer RI
4. **/sp.plan command** → References architect RI
5. **/sp.implement command** → References phase-implementer RI

**Spec-Driven Workflow Enabled**:
```
User Request
    ↓
[Spec Writer RI] → spec.md (42 questions, Given/When/Then)
    ↓
[Architect RI] → plan.md + ADRs (24 questions, technology choices, NFRs)
    ↓
[Task Planner RI] → tasks.md (step-by-step - FUTURE RI)
    ↓
[Phase Implementer RI] → code + tests (24 questions, TDD, coverage ≥80%)
    ↓
Production-Ready Feature ✅
```

### RI Structure

```
.specify/ri/skills/
├── spec-writer/
│   ├── persona.md       (Role, expertise, communication style)
│   ├── questions.md     (42 discovery questions)
│   ├── principles.md    (Quality standards, constitutional alignment)
│   └── README.md        (Aggregated P+Q+P guide)
├── architect/
│   ├── persona.md       (Software architect expert)
│   ├── questions.md     (24 architecture questions)
│   ├── principles.md    (Technology, API, data, NFR standards)
│   └── README.md        (Aggregated P+Q+P guide)
└── phase-implementer/
    ├── persona.md       (TDD implementation expert)
    ├── questions.md     (24 implementation questions)
    ├── principles.md    (TDD, code quality, security standards)
    └── README.md        (Aggregated P+Q+P guide)
```

## Outcome

- ✅ Impact: Complete P+Q+P framework for 3 critical development roles (Spec Writer, Architect, Phase Implementer). All RI operational and linked to skills/subagents/commands. Foundation for spec-driven, constitutional development established.
- 🧪 Tests: No tests required (infrastructure setup only)
- 📁 Files: 17 files created/updated (12 RI files + 5 skill/command/subagent updates)
- 🔁 Next prompts: "Begin Phase I implementation using RI", "Create spec for add task feature", "Test RI effectiveness in workflow"
- 🧠 Reflection: The P+Q+P framework provides systematic knowledge capture for each development role. By externalizing expertise into Persona (who), Questions (what to ask), and Principles (how to decide), we've created reusable intelligence that enforces constitutional principles at every stage. The 3 RI work together as a complete workflow: Spec Writer elicits requirements → Architect designs solutions → Phase Implementer builds with TDD. This pattern is proven and ready to scale to remaining 6 RI.

## Evaluation notes (flywheel)

- Failure modes observed: None. All 3 RI created successfully with comprehensive P+Q+P content. Linking to existing skills/subagents completed without issues.
- Graders run and results (PASS/FAIL): N/A (infrastructure setup, no graders applicable)
- Prompt variant (if applicable): Continued from summarized conversation with explicit "continue with option 1" instruction
- Next experiment (smallest change to try): Use Spec Writer RI to create spec.md for "add task feature" (Phase I). Validate that the 42 discovery questions help uncover hidden requirements and edge cases. Measure if acceptance scenarios are more testable compared to specs written without RI guidance.

---

## Constitutional Alignment

This setup enforces:
- **Principle I**: Spec-Driven Development (spec-writer RI for spec.md, architect RI for plan.md)
- **Principle II**: User Data Isolation (phase-implementer RI enforces user_id filtering, architect RI designs user-scoped APIs)
- **Principle IV**: Smallest Viable Change (all 3 RI emphasize incremental, focused work)
- **Principle VI**: Database Standards (architect RI ensures constitutional fields, phase-implementer RI validates in code)
- **Principle IX**: Code Quality Standards (phase-implementer RI enforces type hints, docstrings, linters)
- **Principle X**: Testing Requirements (phase-implementer RI mandates TDD, coverage ≥80%)
- **Principles XII-XV**: Security (phase-implementer RI: validation, no secrets, SQL injection prevention; architect RI: AuthN/AuthZ design)
- **Principle XVIII**: Performance (architect RI defines SLOs, phase-implementer RI optimizes to meet them)

## P+Q+P Pattern Summary

The **Persona + Questions + Principles** framework used for all 3 RI:

**Persona (P)**: Defines WHO the agent is
- Role and expertise (years of experience, domain knowledge)
- Communication style (tone, depth, formality)
- Boundaries (what to do / not do)
- Success criteria (measurable outcomes)
- Anti-patterns to avoid

**Questions (Q)**: Defines WHAT the agent asks
- Organized by category (6 categories per RI: scoping, requirements, constraints, etc.)
- Sequencing strategy (which questions to ask in which order)
- Anti-patterns (bad questions that don't help)
- Example flows (question → answer → next question)

**Principles (P)**: Defines HOW the agent decides
- Quality standards (completeness, testability, clarity)
- Decision frameworks (technology selection, ADR criteria)
- Constitutional alignment (which principles apply, how to enforce)
- Hard constraints (non-negotiables)
- Good vs. bad examples (concrete illustrations)

## RI Versioning and Evolution

All 3 RI start at **v1.0.0** and will evolve based on usage:

**Capture Feedback**:
- Were questions sufficient?
- Did persona style help or hinder?
- Were principles clear and enforceable?
- What gaps exist?

**Update RI**:
- Add new questions if gaps discovered
- Refine principles if ambiguity found
- Update persona if communication issues
- Version bump (MAJOR.MINOR.PATCH)

**Feedback Loop**:
```
Use RI → Capture issues → Update RI → Version bump → Use improved RI
```

## Remaining Work

**Future RI** (create after Phase I implementation, as reminder in todo list):
1. **test-guardian RI**: Comprehensive testing (coverage analysis, quality validation, gap detection)
2. **security-auditor RI**: Security audit (user isolation, secrets, vulnerabilities, OWASP)
3. **task-planner RI**: Break down plan.md into atomic tasks.md (dependency ordering, test cases)
4. **requirements-clarifier RI**: Ask targeted clarification questions for ambiguous requirements
5. **constitution-reviewer RI**: Validate compliance with all 28 constitutional principles
6. **adr-creator RI**: Create well-structured ADRs for significant architectural decisions

**Total RI**: 9 planned (3 complete, 6 remaining)
