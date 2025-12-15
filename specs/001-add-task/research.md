# Technology Research: Add Task Feature

**Feature**: Add Task (Phase I Console)
**Branch**: `001-add-task`
**Date**: 2025-12-12
**Research Phase**: Phase 0 (Technology Selection)

---

## Overview

This document consolidates all technology research and decisions made during architectural planning for the "Add Task" feature. All decisions are traceable to spec requirements or constitutional principles.

---

## Decision Summary

| Technology Area | Decision | Rationale | Source |
|-----------------|----------|-----------|--------|
| **Programming Language** | Python 3.13+ | Constitutional mandate (Principle III) | Constitution.md |
| **CLI Framework** | Click 8.1+ | User-friendly errors, exit codes, validation | Architecture research |
| **ORM** | SQLModel 0.0.14+ | Constitutional mandate (Principle VI), type-safe | Constitution.md |
| **Database** | SQLite 3 | Phase I simplicity, zero-config, migration path | Architecture research |
| **Testing** | pytest 8.0+ | Constitutional mandate (Principle X) | Constitution.md |
| **Package Manager** | UV | Fast, reproducible builds, modern standard | Architecture research |

---

## Research: CLI Framework

**Question**: What CLI framework provides the best balance of user experience, validation, and error handling for Phase I console app?

**Options Evaluated**:
1. **Click 8.1+** ✅ CHOSEN
2. argparse (built-in)
3. Typer

**Research Findings**:

### Click 8.1+
- **Pros**:
  - Decorator-based syntax (`@click.command()`) - clean, composable
  - Automatic help text generation (`todo add --help`)
  - Built-in validation (types, choices, required options)
  - Exit code management (0=success, 1=error, 2=missing options) - aligns with spec FR-010
  - Rich error messages (user-friendly, not stack traces) - aligns with spec FR-009
  - Widely adopted (pytest, Flask, Black all use Click)
- **Cons**:
  - External dependency (vs. argparse built-in)
  - Slightly steeper learning curve
- **Verdict**: Best fit for user experience and spec requirements

### argparse (built-in)
- **Pros**:
  - No external dependency (standard library)
  - Widely known
- **Cons**:
  - More verbose syntax (class-based or manual parser setup)
  - Less friendly error messages
  - Manual exit code management
- **Verdict**: Too manual for Phase I needs

### Typer
- **Pros**:
  - Type-hint based (very modern)
  - Built on top of Click (inherits benefits)
  - Automatic validation from type hints
- **Cons**:
  - Minimal advantage over Click for Phase I (type hints already enforced via mypy)
  - Adds abstraction layer on top of Click
- **Verdict**: Over-engineered for Phase I; Click is more direct

**Decision**: Click 8.1+
**Rationale**: Best alignment with spec FR-009 (clear error messages) and FR-010 (exit codes). Decorator syntax is cleaner for simple commands.
**Trade-offs Accepted**: External dependency (minimal risk - Click is stable, widely adopted)

---

## Research: Database for Phase I

**Question**: What database technology is appropriate for Phase I console application?

**Options Evaluated**:
1. **SQLite 3** ✅ CHOSEN
2. PostgreSQL (Neon DB)
3. MongoDB

**Research Findings**:

### SQLite 3
- **Pros**:
  - Zero configuration (no database server, no connection strings)
  - Bundled with Python 3.13 (sqlite3 module)
  - File-based persistence (meets spec FR-006: store in current directory)
  - ACID guarantees (meets spec SC-003: 100% persistence across restarts)
  - WAL mode supports concurrent reads (meets spec edge case: concurrent operations)
  - Migration path to PostgreSQL is well-documented (SQLModel + Alembic)
  - Perfect for local console app (no network overhead)
- **Cons**:
  - Single-file limits concurrent writes (write locks)
  - No remote access (can't share database across machines)
  - Limited to ~1 TB file size
- **Phase I Context**:
  - ✅ Spec scope: local console app (no multi-machine access needed)
  - ✅ Spec requirement: 1000 tasks per user = <1MB (file size non-issue)
  - ✅ Spec edge case: concurrent operations handled via WAL mode
- **Verdict**: Ideal for Phase I

### PostgreSQL (Neon DB)
- **Pros**:
  - Production-grade (ACID, replication, high concurrency)
  - Constitutional target for Phase II
  - Managed service (Neon) reduces ops burden
  - SQLModel ORM works with PostgreSQL
- **Cons**:
  - Requires network database server (over-engineered for Phase I console)
  - Configuration overhead (connection strings, secrets)
  - Cost ($20/month vs. $0 for SQLite)
- **Phase I Context**:
  - ❌ Spec scope: local console app (no need for remote database)
  - ❌ Over-engineering: PostgreSQL features (replication, high concurrency) not needed
- **Verdict**: Deferred to Phase II web application

### MongoDB
- **Pros**:
  - Flexible schema (no migrations)
  - JSON-native storage
- **Cons**:
  - No ACID guarantees (eventual consistency)
  - Constitutional Principle VI mandates SQLModel (not compatible with MongoDB)
  - NoSQL not needed (Task schema is fixed, not evolving rapidly)
- **Verdict**: Ruled out by constitutional requirements

**Decision**: SQLite 3 (bundled with Python)
**Rationale**:
- Meets all Phase I requirements (zero-config, local persistence, ACID)
- Enables immediate development velocity (no infrastructure setup)
- Clear migration path to PostgreSQL in Phase II (SQLModel abstracts database layer)
- Constitutional compliance (Principle VI: SQLModel ORM works with SQLite)

**Trade-offs Accepted**:
- Single-file write locks (acceptable - Phase I has no multi-user concurrent writes)
- No remote access (expected - Phase I scope is local console)

**Migration Strategy** (Phase II):
1. Install Alembic for migrations
2. Update DATABASE_URL to point to Neon PostgreSQL
3. Run `alembic upgrade head` to apply schema
4. Export SQLite data, import to PostgreSQL
5. Test user isolation in PostgreSQL environment

**ADR Required**: YES - This decision is architecturally significant:
- **Impact**: Storage layer affects durability, concurrency, Phase II migration
- **Alternatives**: Multiple viable options (PostgreSQL, MongoDB)
- **Scope**: Cross-cutting (affects models, services, testing)

---

## Research: Package Management

**Question**: What package manager provides the best developer experience for Phase I Python project?

**Options Evaluated**:
1. **UV** ✅ CHOSEN
2. pip + venv
3. Poetry
4. PDM

**Research Findings**:

### UV (uv package manager)
- **Pros**:
  - 10-100x faster than pip (Rust implementation)
  - Lock files (`uv.lock`) for reproducible builds
  - PEP 621 compliant (uses `pyproject.toml` standard)
  - Modern tooling aligns with Principle IX (code quality)
  - Works seamlessly with existing pip ecosystem
  - Backed by Astral (creators of ruff linter)
- **Cons**:
  - Newer tool (less mature than pip/Poetry)
  - Requires separate installation (not bundled with Python)
- **Verdict**: Best performance and modern standard

### pip + venv
- **Pros**:
  - Built-in with Python (no installation)
  - Widely known
- **Cons**:
  - Slower dependency resolution
  - No lock files (requirements.txt is version range, not pinned)
  - Manual virtual environment management
- **Verdict**: Functional but less modern

### Poetry
- **Pros**:
  - Dependency resolver with lock files
  - Integrated build system
  - Widely adopted in Python community
- **Cons**:
  - Slower than UV
  - Larger lock files
  - Non-standard virtual environment location (can confuse IDEs)
- **Verdict**: Good but UV is faster

### PDM
- **Pros**:
  - PEP 582 compliant (PEP 621 also supported)
  - Modern dependency management
- **Cons**:
  - Smaller community than Poetry/pip
  - PEP 582 is not yet widely adopted
- **Verdict**: Interesting but less proven

**Decision**: UV (uv package manager)
**Rationale**:
- Speed: 10-100x faster than pip (improves CI/CD times)
- Reproducibility: Lock files ensure identical builds across environments
- Modern standard: PEP 621 `pyproject.toml` is Python's future
- Constitutional alignment: Principle IX encourages modern tooling

**Trade-offs Accepted**:
- Installation requirement (one-time setup per developer)
- Newer tool (acceptable - backed by reputable team, rapidly adopted)

---

## Research: Testing Framework

**Question**: What testing framework best supports Phase I requirements (TDD, coverage, fixtures)?

**Options Evaluated**:
1. **pytest 8.0+** ✅ CHOSEN (Constitutional mandate)
2. unittest (built-in)
3. nose2

**Research Findings**:

### pytest 8.0+
- **Pros**:
  - Fixture-based testing (database session management via `conftest.py`)
  - Parametrization (test edge cases: 1 char, 200 chars, 201 chars titles)
  - pytest-cov integration (measures coverage, enforces ≥80% target)
  - Rich assertion introspection (better error messages)
  - Auto-discovery (finds `test_*.py` files)
  - Constitutional mandate (Principle X)
- **Cons**:
  - External dependency (vs. unittest built-in)
  - Fixture "magic" can be non-obvious to newcomers
- **Verdict**: Mandated by constitution, best-in-class features

### unittest (built-in)
- **Pros**:
  - No external dependency (standard library)
  - OOP-style tests (familiar to Java/C# developers)
- **Cons**:
  - More verbose (class-based test structure)
  - No built-in parametrization
  - Less friendly assertion errors
- **Verdict**: Ruled out by constitutional mandate

### nose2
- **Pros**:
  - unittest extension
  - Plugin system
- **Cons**:
  - Less popular than pytest
  - Not constitutional mandate
- **Verdict**: No advantage over pytest

**Decision**: pytest 8.0+
**Rationale**: Constitutional mandate (Principle X). Provides all needed features (fixtures, parametrization, coverage).
**Trade-offs Accepted**: External dependency (acceptable - pytest is Python testing standard)

---

## Constitutional Alignment Review

All technology decisions aligned with applicable constitutional principles:

| Technology | Constitutional Requirement | Compliance |
|------------|---------------------------|------------|
| Python 3.13+ | Principle III (mandatory) | ✅ PASS |
| SQLModel | Principle VI (mandatory) | ✅ PASS |
| pytest | Principle X (mandatory) | ✅ PASS |
| Click | Principle IX (quality) | ✅ PASS (supports clear errors, exit codes) |
| SQLite | Principle VI (database standards) | ✅ PASS (SQLModel compatible) |
| UV | Principle IX (modern tooling) | ✅ PASS (fast, reproducible) |

**No constitutional violations detected.**

---

## Migration Paths (Phase II)

### Database Migration (SQLite → PostgreSQL)
1. Install Alembic: `uv add alembic`
2. Initialize migrations: `alembic init migrations`
3. Update `alembic.ini` with Neon DATABASE_URL
4. Generate migration: `alembic revision --autogenerate -m "Initial schema"`
5. Apply migration: `alembic upgrade head`
6. Export SQLite data: `sqlite3 todo.db .dump > dump.sql`
7. Import to PostgreSQL: `psql -h neon.db -U user -d db < dump.sql`
8. Test user isolation in PostgreSQL

### CLI → Web API Migration
1. Keep `src/` as CLI client
2. Add `backend/` directory with FastAPI
3. Backend reuses `src/models/task.py` (SQLModel dual mode)
4. Backend reuses `src/services/task_service.py` (same business logic)
5. CLI calls backend API instead of direct database access
6. User isolation enforced in API layer (JWT + user_id in URL)

---

## Open Questions (Resolved)

**Q1**: Should we use SQLite or PostgreSQL for Phase I?
**A1**: SQLite - Phase I is local console app, no need for network database. Migration path to PostgreSQL is well-documented.

**Q2**: Should we use Click or argparse for CLI framework?
**A2**: Click - Better user experience (error messages, exit codes) aligns with spec requirements. Decorator syntax is cleaner.

**Q3**: Should we use Poetry or UV for package management?
**A3**: UV - 10-100x faster, modern standard (PEP 621), reproducible builds via lock files.

**Q4**: How do we ensure user isolation in Phase I?
**A4**:
- `--user` flag required on CLI (spec FR-001)
- ALL TaskService methods filter by `user_id` (Principle II)
- Index on `user_id` for fast queries
- Integration tests verify cross-user access blocked

**Q5**: How do we handle emojis in titles (spec edge case)?
**A5**: SQLite uses UTF-8 by default, supports emojis. Pydantic preserves Unicode. Integration test verifies roundtrip.

---

## Next Steps

1. ✅ **Research Complete**: All technology decisions documented
2. ⏭️ **Create Design Artifacts** (Phase 1):
   - `data-model.md` - Task entity schema
   - `contracts/add-task.md` - CLI command contract
   - `quickstart.md` - Usage examples
3. ⏭️ **Update Agent Context**: Add technologies to CLAUDE.md
4. ⏭️ **Create ADR**: SQLite database choice
5. ⏭️ **Generate Tasks**: Run `/sp.tasks`
6. ⏭️ **Implement**: Run `/sp.implement` with TDD

---

**Research Phase Complete**: All NEEDS CLARIFICATION markers resolved. Ready to proceed to Phase 1 (Design & Contracts).
