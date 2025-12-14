# ADR-0002: Phase I Technology Stack

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-08
- **Feature:** Phase I - Console Todo App
- **Context:** Phase I requires a Python-based console application with multi-user task management, SQLite persistence, 80% test coverage, strict type checking, and performance targets (<2s startup, <500ms operations with 10K tasks). The technology stack must align with constitutional principles (code quality, testing, security) while enabling smooth migration to Phase II web application (FastAPI + Next.js).

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅ YES - Determines development patterns, Phase II migration path
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅ YES - Multiple ORM, CLI, testing frameworks evaluated
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅ YES - Affects every file engineers write
-->

## Decision

**Adopt integrated Python 3.13+ stack optimized for type safety, developer experience, and Phase II migration.**

**Technology Stack Components**:

- **Language**: Python 3.13+ (constitutional requirement, type hints, pattern matching)
- **ORM/Validation**: SQLModel (SQLAlchemy + Pydantic integration)
- **Database**: SQLite 3.x (bundled, local file storage, zero config)
- **CLI Framework**: Click 8.x (decorator-based, colored output, automatic help)
- **Testing**: pytest 8.x + pytest-cov 5.x (fixture support, ≥80% coverage enforcement)
- **Type Checking**: mypy 1.x (strict mode, static type validation)
- **Code Formatting**: black 24.x (consistent formatting, zero config)
- **Linting**: flake8 7.x (PEP 8 compliance, complexity checks)

**Integration Rationale**: These technologies work together as a cohesive ecosystem - SQLModel provides Pydantic models that work seamlessly with FastAPI (Phase II), Click provides CLI patterns that map to REST endpoints, pytest fixtures translate to FastAPI TestClient, and mypy strict mode enforces type safety across the entire stack.

## Consequences

### Positive

- **Type Safety End-to-End**: SQLModel (Pydantic) provides runtime validation + mypy provides compile-time checking (constitutional principle IX)
- **Phase II Migration Path**: SQLModel → FastAPI transition is seamless (same Pydantic models), Click commands → REST endpoints mapping is straightforward
- **Developer Experience**: Decorator-based patterns (Click, pytest), automatic validation (Pydantic), zero-config tools (black)
- **Constitutional Compliance**: Built-in coverage enforcement (pytest-cov --cov-fail-under=80), strict type checking (mypy --strict), PEP 8 compliance (flake8)
- **Proven Ecosystem**: All technologies are mature, well-documented, widely adopted in Python community
- **Testing Integration**: pytest fixtures work perfectly with SQLModel sessions, Click CliRunner enables CLI testing
- **Performance**: SQLite handles 10K+ tasks efficiently with proper indexing, no external database setup required

### Negative

- **Learning Curve**: SQLModel is less common than raw SQLAlchemy (team needs to learn Pydantic patterns)
- **Dependency Weight**: 8 primary dependencies vs minimal stdlib approach (argparse + sqlite3 only)
- **Framework Lock-in**: Click patterns don't translate well to non-Python ecosystems (Phase V may use different languages)
- **SQLModel Maturity**: Newer than SQLAlchemy (less battle-tested, smaller community)
- **Type Checking Overhead**: mypy --strict mode can be demanding (requires thorough type annotations)
- **Black Opinionated**: No configuration flexibility (some teams prefer customizable formatters)
- **SQLite Limitations**: Not production-ready for Phase II web app (will require PostgreSQL migration)

## Alternatives Considered

### Alternative 1: Minimal Stdlib Stack (SQLAlchemy + argparse)
**Approach**: Use only Python standard library where possible, SQLAlchemy for ORM.

**Stack Components**:
- Language: Python 3.13+
- ORM: SQLAlchemy Core + separate Pydantic schemas for validation
- Database: sqlite3 (stdlib)
- CLI: argparse (stdlib)
- Testing: unittest (stdlib)
- Type Checking: mypy (same)
- Formatting: Manual or autopep8

**Why Rejected**:
- ❌ **Verbose Boilerplate**: SQLAlchemy Core + Pydantic requires duplicate model definitions (violates DRY)
- ❌ **argparse Boilerplate**: Manual help text, error handling, argument parsing (100+ lines vs 20 with Click)
- ❌ **unittest Limitations**: No fixture support, less readable than pytest, harder to parametrize tests
- ❌ **Phase II Migration**: FastAPI expects Pydantic models, SQLAlchemy Core doesn't integrate well
- ✅ **Fewer Dependencies**: Only SQLAlchemy + Pydantic added (vs SQLModel + Click + pytest)

### Alternative 2: Modern Python Stack (SQLAlchemy 2.0 + Typer + Pydantic)
**Approach**: Use latest SQLAlchemy 2.0 with modern type hints, Typer (Click-based but type-hint focused).

**Stack Components**:
- Language: Python 3.13+
- ORM: SQLAlchemy 2.0 + Pydantic v2 (separate models)
- Database: SQLite
- CLI: Typer (Click wrapper with type hints)
- Testing: pytest
- Type Checking: mypy
- Formatting: black

**Why Rejected**:
- ❌ **Duplicate Models**: Still requires separate SQLAlchemy + Pydantic models (SQLModel eliminates this)
- ❌ **Typer Overkill**: Typer's advanced features (Rich integration, async commands) not needed for Phase I CLI
- ✅ **Better Type Hints**: Typer has superior type hint support vs Click
- ✅ **SQLAlchemy 2.0**: More modern than SQLModel's SQLAlchemy 1.4 base
- **Decision**: SQLModel's DRY benefit outweighs Typer's type hint advantages; Click sufficient for Phase I

### Alternative 3: Django Management Commands
**Approach**: Use Django ORM + management command framework for CLI.

**Stack Components**:
- Framework: Django 5.x
- ORM: Django ORM (built-in)
- Database: SQLite (Django default)
- CLI: Django management commands
- Testing: Django TestCase + pytest-django
- Type Checking: mypy + django-stubs

**Why Rejected**:
- ❌ **Massive Overkill**: Django brings entire web framework (middleware, templates, admin, auth) for simple console app
- ❌ **Configuration Complexity**: Requires settings.py, INSTALLED_APPS, migrations infrastructure
- ❌ **Performance Overhead**: Django ORM + app loading adds 3-5 seconds to startup (<2s target)
- ❌ **Phase II Migration**: Phase II uses FastAPI (not Django), so no migration advantage
- ✅ **Integrated Admin**: Django admin could be useful for Phase II web UI
- **Decision**: Complexity far exceeds Phase I needs; FastAPI alignment more valuable

## References

- Feature Spec: `specs/002-phase-i-console-app/spec.md` (20 functional requirements)
- Implementation Plan: `specs/002-phase-i-console-app/plan.md` (lines 14-24: Technical Context)
- Research: `specs/002-phase-i-console-app/research.md` (7 technology decisions with detailed rationale)
  - Decision 1: SQLModel selection (lines 12-63)
  - Decision 2: Click selection (lines 66-113)
  - Decision 6: Testing strategy (lines 262-297)
- Constitution: `.specify/memory/constitution.md` (Principle IX: Code Quality Standards)
- Related ADRs:
  - ADR-0001 (Future-Proof Data Architecture) - SQLModel enables nullable field validation
  - ADR-0003 (User Isolation Architecture) - Service layer integrates with SQLModel sessions
- PHR: `history/prompts/002-phase-i-console-app/0002-phase-i-implementation-planning.plan.prompt.md`
