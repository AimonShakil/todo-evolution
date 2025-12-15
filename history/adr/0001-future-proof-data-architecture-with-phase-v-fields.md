# ADR-0001: Future-Proof Data Architecture with Phase V Fields

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-08
- **Feature:** Phase I - Console Todo App
- **Context:** The Evolution of Todo project spans 5 phases (Console → Web → AI Chatbot → Local K8s → Cloud). To maintain spec-driven development workflow integrity and avoid manual database schema migrations across phases, we must design the Phase I data model with future phases in mind. Constitutional Principle I mandates spec-driven development without manual interventions.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅ YES - Affects schema evolution across 5 phases
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅ YES - Minimal schema vs future-proof vs incremental migrations
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅ YES - Impacts all CRUD operations, migrations, validation
-->

## Decision

**Include all Phase V fields in the Phase I Task entity schema as nullable columns from day 1.**

The Task entity will have **11 fields total**:

**Phase I Active Fields (6)**:
- `id` (Integer, primary key, auto-increment)
- `user_id` (String, indexed - username in Phase I, migrates to integer FK in Phase II)
- `title` (String, 1-200 chars, required)
- `completed` (Boolean, default False)
- `created_at` (DateTime, auto-set)
- `updated_at` (DateTime, auto-managed)

**Phase V Future Fields (5 nullable, unused in Phase I-IV)**:
- `description` (String) - Phase II+
- `priority` (String, enum: high/medium/low) - Phase V Intermediate
- `tags` (String, JSON-encoded array) - Phase V Intermediate
- `due_date` (DateTime) - Phase V Intermediate
- `recurrence_pattern` (String) - Phase V Advanced

This design eliminates the need for 4 schema migrations (Phase I→II, II→III, III→IV, IV→V) by including the complete schema from the start.

## Consequences

### Positive

- **Zero Schema Migrations**: No ALTER TABLE operations needed across Phases I-V (only data migrations for user_id type change in Phase II)
- **Spec-Driven Integrity**: Maintains constitutional principle I by avoiding manual database changes outside spec-driven workflow
- **Single Source of Truth**: One Task entity definition serves all 5 phases, preventing schema drift
- **Phase II Migration Simplicity**: Only need to convert user_id from string to integer FK, no new columns
- **Validation Ready**: SQLModel Field definitions exist from day 1, just need to activate validation rules in future phases
- **Testing Consistency**: Same database schema in all test environments across phases
- **Database Portability**: When migrating SQLite → PostgreSQL in Phase II, same schema structure applies

### Negative

- **Upfront Complexity**: 11-field schema (6 active + 5 future) vs simpler 6-field minimal schema
- **Cognitive Overhead**: Engineers see unused nullable fields in Phase I, may be confused about purpose
- **Storage Overhead**: 5 NULL columns per task row (minimal impact - SQLite stores NULLs efficiently)
- **Documentation Burden**: Must document which fields are active vs future in all phases
- **Validation Risk**: Engineers might accidentally populate Phase V fields in Phase I code
- **Over-Engineering Appearance**: Stakeholders may question why we're building for future phases now

## Alternatives Considered

### Alternative 1: Minimal Schema (6 Fields Only)
**Approach**: Start with only Phase I active fields, add columns in each phase as needed.

**Schema Evolution**:
- Phase I: 6 fields (id, user_id, title, completed, created_at, updated_at)
- Phase II: +1 field (description) - **ALTER TABLE ADD COLUMN**
- Phase V Intermediate: +3 fields (priority, tags, due_date) - **ALTER TABLE ADD COLUMN** × 3
- Phase V Advanced: +1 field (recurrence_pattern) - **ALTER TABLE ADD COLUMN**

**Why Rejected**:
- ❌ Requires 4-5 manual ALTER TABLE operations across phases
- ❌ Violates constitutional principle I (spec-driven development without manual DB changes)
- ❌ Each migration requires downtime planning, rollback strategy, data validation
- ❌ Risk of schema drift between environments (dev, staging, prod)
- ❌ Breaking changes if adding NOT NULL columns with existing data

### Alternative 2: Incremental Migrations with Alembic
**Approach**: Use Alembic migration framework from Phase I, define migrations for each phase transition.

**Schema Evolution**:
- Phase I: 6 fields + Alembic infrastructure
- Each phase transition: Create Alembic migration script with ALTER TABLE commands
- Version control migrations in `alembic/versions/`

**Why Rejected**:
- ❌ Over-engineering for Phase I SQLite (Alembic adds complexity without value for local DB)
- ❌ Still requires 4-5 manual migration scripts across phases (same maintenance as Alternative 1)
- ❌ Alembic introduces dependency and learning curve for Phase I console app
- ✅ Will be adopted in Phase II for PostgreSQL (when migrations become necessary)

### Alternative 3: Database Views for Phase Abstraction
**Approach**: Create separate database views per phase exposing only active fields.

**Schema Evolution**:
- Phase I: CREATE VIEW phase_i_tasks AS SELECT id, user_id, title, completed, created_at, updated_at FROM tasks
- Phase II: CREATE VIEW phase_ii_tasks AS SELECT *, description FROM tasks
- Application code queries views, not base table

**Why Rejected**:
- ❌ Views complicate SQLModel ORM mapping (need separate model per view)
- ❌ Write operations require triggers or INSTEAD OF logic (complex)
- ❌ Testing becomes more complex (need to verify view definitions)
- ❌ Doesn't eliminate the need for ALTER TABLE when adding columns
- ❌ Violates YAGNI - unnecessary abstraction for Phase I

## References

- Feature Spec: `specs/002-phase-i-console-app/spec.md` (FR-012: Future-proof schema requirement)
- Implementation Plan: `specs/002-phase-i-console-app/plan.md` (lines 133-138: Future-proof schema justification)
- Data Model: `specs/002-phase-i-console-app/data-model.md` (complete Task entity with 11 fields)
- Research: `specs/002-phase-i-console-app/research.md` (lines 369-372: Best practices applied)
- Constitution: `.specify/memory/constitution.md` (Principle I: Spec-Driven Development)
- Related ADRs: None (first ADR for this project)
- PHR: `history/prompts/002-phase-i-console-app/0002-phase-i-implementation-planning.plan.prompt.md` (planning workflow with constitution check)
