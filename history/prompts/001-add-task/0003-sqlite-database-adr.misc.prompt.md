---
id: 0003
title: SQLite Database ADR
stage: misc
date: 2025-12-12
surface: agent
model: claude-sonnet-4-5
feature: 001-add-task
branch: 001-add-task
user: aimon
command: /sp.adr
labels: ["adr", "database", "sqlite", "postgresql", "migration", "phase-i", "architecture"]
links:
  spec: specs/001-add-task/spec.md
  ticket: null
  adr: history/adr/0004-database-choice-sqlite-for-phase-i-console.md
  pr: null
files:
  - history/adr/0004-database-choice-sqlite-for-phase-i-console.md
tests:
  - No tests created (ADR documentation only)
---

## Prompt

User invoked: `/sp.adr "Database Choice: SQLite for Phase I Console"`

Context:
- Architectural planning completed in previous session (/sp.plan)
- Database decision identified as architecturally significant (passed 3-part ADR test)
- ADR suggestion provided: "📋 Architectural decision detected: Database choice (SQLite vs. PostgreSQL for Phase I) — Document reasoning and tradeoffs? Run `/sp.adr \"Database Choice: SQLite for Phase I Console\"`"
- User explicitly requested ADR creation for database decision

## Response snapshot

### ADR Creation Process

**Step 1: Load Planning Context** ✅
- Ran `.specify/scripts/bash/check-prerequisites.sh --json`
- Parsed FEATURE_DIR: `/mnt/g/AI_Eng/Q6/project/todo-evolution/specs/001-add-task`
- Read plan.md (lines 190-239 for database decision section)
- Read research.md (lines 45-144 for database research with 3 alternatives)

**Step 2: Check Existing ADRs** ✅
- Listed `history/adr/` directory
- Found 3 existing ADRs:
  - ADR-0001: Future-proof data architecture
  - ADR-0002: Phase I Technology Stack (includes SQLite on line 24 as part of clustered stack)
  - ADR-0003: User Isolation Architecture
- Read ADR-0002 in full to check database decision coverage

**Step 3: Analysis** ✅
- Database decision IS documented in ADR-0002 as part of integrated technology stack
- However, user explicitly requested separate database-focused ADR
- Decision: Create ADR-0004 as **complementary** ADR (not duplicate):
  - ADR-0002 clusters SQLite with other Phase I technologies (Python, Click, SQLModel, pytest) - correct per Architect RI clustering principle
  - ADR-0004 provides deeper database-specific details: migration strategy, storage layer trade-offs, Phase II PostgreSQL transition path

**Step 4: Create ADR-0004** ✅
- Initial attempt: `.specify/scripts/bash/create-adr.sh "Database Choice: SQLite for Phase I Console"`
  - Error: Exit code 1, "Error: --title is required"
- Fixed: `.specify/scripts/bash/create-adr.sh --title "Database Choice: SQLite for Phase I Console" --json`
  - Success: Created template at `history/adr/0004-database-choice-sqlite-for-phase-i-console.md`

**Step 5: Fill ADR-0004** ✅ (~246 lines)
- Added note explaining relationship to ADR-0002 (complementary, focuses on database-specific migration strategy)
- **Context**: Phase I requirements (zero-config setup, ACID guarantees, user isolation, migration path to Phase II PostgreSQL, 1000 tasks/user with p95 <100ms)
- **Decision**: Use SQLite 3.x as embedded database with structured migration path to PostgreSQL (Neon DB) in Phase II
- **Database Configuration**:
  - Engine: SQLite 3.x (bundled with Python 3.13, sqlite3 module)
  - File Location: `todo.db` in current working directory (spec FR-006)
  - Mode: WAL (Write-Ahead Logging) for better concurrency
  - ORM: SQLModel 0.0.14+ (constitutional requirement Principle VI)
  - Schema: Task table with constitutional fields (id, user_id, created_at, updated_at, title, completed)
  - Indexes: PRIMARY KEY (id), INDEX (user_id) - mandatory for user isolation (Principle II)
- **Migration Strategy** (6-step overview for Phase I → Phase II):
  1. Schema Abstraction: SQLModel ORM abstracts database dialect
  2. Migration Tool: Alembic for versioned schema migrations
  3. Data Export: `sqlite3 todo.db .dump > dump.sql`
  4. Import to PostgreSQL: Custom import script (handles dialect differences)
  5. Validation: Verify user isolation, data integrity, performance post-migration
  6. Timeline: Phase II spec creation triggers migration planning
- **Consequences**:
  - **Positive** (11 benefits):
    - Zero Configuration: No database server installation, no connection strings, no network setup
    - Bundled with Python: sqlite3 module ships with Python 3.13 (no external dependency)
    - Development Velocity: Developers can test persistence immediately without infrastructure
    - ACID Guarantees: Full ACID transactions (meets spec SC-003: 100% persistence across restarts)
    - WAL Mode Concurrency: Write-Ahead Logging allows concurrent reads during writes
    - File-Based Portability: `todo.db` file is portable (copy to another machine, version control for test data)
    - SQLModel Abstraction: ORM isolates application from database dialect (Phase II migration is code change, not rewrite)
    - User Isolation Enforcement: user_id index enables fast filtering (Principle II)
    - Test Database Speed: In-memory SQLite (`:memory:`) for tests is 100x faster than network database
    - Phase II Migration Path: Alembic + SQLModel provide clear, documented migration
    - Cost: $0 vs $20/month for managed PostgreSQL
  - **Negative** (6 drawbacks with mitigations):
    - Single-File Write Locks: Only one writer at a time
      - Mitigation: WAL mode reduces lock duration, Phase I has no multi-user concurrent writes
      - Acceptable Because: Spec scope is local console app (no concurrent write requirement)
    - No Remote Access: Cannot share database across machines
      - Mitigation: N/A - spec explicitly states local console app
      - Acceptable Because: Phase I scope is single-machine usage
    - File Size Limit: ~1 TB maximum
      - Mitigation: 1000 tasks/user × 1KB/task = 1MB (far below limit)
      - Acceptable Because: Spec requirements fit comfortably within limits
    - Phase II Migration Required: Must migrate to PostgreSQL for web app
      - Mitigation: SQLModel + Alembic provide structured migration path
      - Acceptable Because: Phase II explicitly calls for PostgreSQL (planned transition)
    - Limited Concurrency: Not suitable for high-concurrency web app
      - Mitigation: Phase II migration to PostgreSQL resolves this
      - Acceptable Because: Phase I console has sequential operations
    - No Native JSON Queries: SQLite JSON support is limited vs PostgreSQL JSONB
      - Mitigation: N/A - Task schema is relational, no JSON fields in Phase I
      - Acceptable Because: Spec requirements don't include JSON data
- **Alternatives Considered** (3 alternatives with comprehensive analysis):
  - **Alternative 1: PostgreSQL (Neon DB)**
    - Pros: Production-grade, no Phase II migration, point-in-time recovery, branching, native JSON support
    - Cons: Over-engineering for Phase I, network dependency, configuration complexity, development friction, cost ($20/month), startup latency (10-50ms vs <1ms)
    - Why Rejected: Complexity far exceeds Phase I needs, violates Principle IV (Smallest Viable Change), Phase II will require PostgreSQL anyway
  - **Alternative 2: MongoDB (MongoDB Atlas)**
    - Pros: Flexible schema, JSON-native, free tier, horizontal scaling
    - Cons: Constitutional violation (Principle VI mandates SQLModel ORM - incompatible with MongoDB), no ACID guarantees (violates spec SC-003), network dependency, schema flexibility not needed, Phase II migration creates divergence, complexity overkill
    - Why Rejected: Constitutional Principle VI explicitly requires SQLModel ORM (disqualifies MongoDB), spec requires ACID guarantees (MongoDB's eventual consistency is insufficient), Task schema is stable and relational
  - **Alternative 3: PostgreSQL (Local with Docker)**
    - Pros: No Phase II migration, free (self-hosted), production parity
    - Cons: Docker dependency, developer friction (docker-compose up, port conflicts), configuration complexity (docker-compose.yml, volumes, networking), startup overhead (3-5 seconds vs <2s spec target), over-engineering (local PostgreSQL has same concurrency limitations as SQLite for single-user app)
    - Why Rejected: Docker adds setup complexity without Phase I benefits, violates zero-configuration goal, local PostgreSQL provides no advantage over SQLite for Phase I workload
- **Migration Plan** (10 detailed steps for SQLite → PostgreSQL):
  1. Install Alembic: `uv add alembic && alembic init migrations`
  2. Configure Alembic for PostgreSQL (migrations/env.py with Task metadata)
  3. Update DATABASE_URL environment variable to PostgreSQL connection string
  4. Generate migration: `alembic revision --autogenerate -m "Initial schema"`
  5. Apply migration to PostgreSQL: `alembic upgrade head`
  6. Export SQLite data: `sqlite3 todo.db .dump > dump.sql`
  7. Import to PostgreSQL (custom script handles dialect differences)
  8. Validation tests: Verify task count, user isolation, performance (p95 <500ms for Phase II SLO)
  9. Update application code: Change DATABASE_URL from sqlite:///todo.db to os.getenv("DATABASE_URL")
  10. Test Phase II application with PostgreSQL (full test suite, ≥80% coverage, load test 100 concurrent users)
- **Rollback Plan**: Retain SQLite file as backup, revert DATABASE_URL, re-run tests
- **References**: Linked to spec.md, plan.md, research.md, data-model.md, constitution.md, ADR-0002 (technology stack), ADR-0003 (user isolation), PHR 0002 (planning session)

**Step 6: Create PHR** ⏭️ (Current step)
- Created template: `history/prompts/001-add-task/0003-sqlite-database-adr.misc.prompt.md`
- Filling with complete content now

## Outcome

- ✅ Impact: Created ADR-0004 documenting SQLite database choice for Phase I console application with comprehensive migration strategy to PostgreSQL for Phase II. ADR complements ADR-0002 (technology stack) by providing deeper database-specific analysis: 10-step migration plan, 3 alternative databases evaluated (PostgreSQL Neon, MongoDB, PostgreSQL Docker) with detailed rejection rationale, 11 positive consequences and 6 negative consequences with mitigations, database configuration (WAL mode, user_id index), and Phase II migration timeline. ADR passes 3-part significance test: Impact (storage layer affects data durability and Phase II migration complexity), Alternatives (3 viable options considered), Scope (cross-cutting concern affecting models, services, testing, deployment).
- 🧪 Tests: No tests created (ADR documentation only). ADR references test strategy from plan.md (unit, integration, E2E pyramid with ≥80% coverage target) and specifies migration validation tests (task count verification, user isolation checks, performance testing p95 <500ms).
- 📁 Files: 1 file created (history/adr/0004-database-choice-sqlite-for-phase-i-console.md - 246 lines)
- 🔁 Next prompts: "/sp.tasks" to generate implementation breakdown (tasks.md with TDD steps), then "/sp.implement" for implementation with tests
- 🧠 Reflection: Successfully created complementary ADR-0004 honoring user's explicit request while preserving Architect RI clustering principle in ADR-0002. Technology clustering (ADR-0002) groups SQLite with other Phase I technologies that work together (Python, Click, SQLModel, pytest), while database-specific ADR (ADR-0004) provides deeper migration strategy, storage layer trade-offs, and Phase II PostgreSQL transition details. The 3-part ADR significance test correctly identified database decision as architecturally significant. Migration plan is comprehensive (10 steps) with rollback strategy and validation tests. All 3 alternatives (PostgreSQL Neon, MongoDB, PostgreSQL Docker) rejected with clear rationale aligned to constitutional principles (Principle IV: Smallest Viable Change, Principle VI: SQLModel ORM requirement). Constitutional compliance maintained throughout: Principle II (user_id index for user isolation), Principle VI (SQLModel ORM, constitutional database fields), Principle X (test strategy documented). Phase II migration path preserves architectural flexibility while enabling Phase I development velocity. Note added at top of ADR-0004 clarifies relationship to ADR-0002 to prevent confusion about apparent duplication.

## Evaluation notes (flywheel)

- Failure modes observed: Initial command syntax error (missing --title flag) was quickly self-corrected. Script warning about duplicate '001' prefix (001-add-task, 001-evolution-vision) is informational only and did not block execution.
- Graders run and results (PASS/FAIL): ADR Significance Test (3-part): PASS (Impact: storage layer long-term consequences, Alternatives: 3 viable options evaluated, Scope: cross-cutting concern affecting models/services/testing/deployment). Constitutional Compliance: PASS (Principle II: user_id index for user isolation, Principle VI: SQLModel ORM requirement enforced in alternative evaluation). Migration Strategy: PASS (10-step plan with rollback, validation tests, timeline trigger). Alternatives Analysis: PASS (3 alternatives with pros/cons/rejection rationale aligned to constitutional principles).
- Prompt variant (if applicable): Standard /sp.adr command workflow with explicit user request for database-focused ADR despite existing coverage in ADR-0002 (technology stack clustering)
- Next experiment (smallest change to try): When next ADR is suggested during /sp.tasks or /sp.implement, validate that the 3-part significance test is applied consistently and that technology clustering principle is honored (avoid creating separate ADRs for technologies that work together). Measure whether migration plan level of detail (10 steps with validation) provides sufficient guidance for future Phase II transition without being overly prescriptive. Track whether complementary ADRs (like ADR-0004 complementing ADR-0002) create value or confusion - adjust template to include explicit "Relationship to Other ADRs" section if confusion arises.
