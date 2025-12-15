# ADR-0004: Database Choice: SQLite for Phase I Console

> **Note**: This ADR provides database-specific migration strategy details that complement ADR-0002 (Phase I Technology Stack). While ADR-0002 documents SQLite as part of the integrated stack, this ADR focuses on the storage layer decision, Phase II migration path, and data durability considerations.

- **Status:** Accepted
- **Date:** 2025-12-12
- **Feature:** 001-add-task (Phase I Console)
- **Context:** Phase I requires persistent task storage for a local console application with requirements: (1) Zero-configuration setup (spec: no database server), (2) ACID guarantees (spec SC-003: 100% persistence across restarts), (3) User isolation (Constitutional Principle II), (4) Migration path to PostgreSQL for Phase II web app, (5) Support for 1000 tasks/user with p95 latency <100ms. The decision must balance Phase I simplicity with Phase II scalability while meeting all constitutional database standards (Principle VI: id, user_id, created_at, updated_at fields).

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅ YES - Storage layer affects data durability, Phase II migration complexity, user data isolation enforcement
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅ YES - PostgreSQL (production-grade), MongoDB (NoSQL), SQLite (embedded)
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅ YES - Affects models, services, testing strategy, deployment, Phase II migration
-->

## Decision

**Use SQLite 3.x as the embedded database for Phase I console application, with structured migration path to PostgreSQL (Neon DB) in Phase II.**

**Database Configuration**:
- **Engine**: SQLite 3.x (bundled with Python 3.13, sqlite3 module)
- **File Location**: `todo.db` in current working directory (spec FR-006)
- **Mode**: WAL (Write-Ahead Logging) for better concurrency (spec edge case: concurrent operations)
- **ORM**: SQLModel 0.0.14+ (constitutional requirement Principle VI)
- **Schema**: Task table with constitutional fields (id, user_id, created_at, updated_at, title, completed)
- **Indexes**: PRIMARY KEY (id), INDEX (user_id) - mandatory for user isolation (Principle II)

**Migration Strategy** (Phase I → Phase II):
1. **Schema Abstraction**: SQLModel ORM abstracts database dialect (SQLite vs PostgreSQL)
2. **Migration Tool**: Alembic for versioned schema migrations
3. **Data Export**: `sqlite3 todo.db .dump > dump.sql` for data extraction
4. **Import to PostgreSQL**: Custom import script (handles dialect differences)
5. **Validation**: Verify user isolation, data integrity, performance post-migration
6. **Timeline**: Phase II spec creation triggers migration planning

## Consequences

### Positive

- **Zero Configuration**: No database server installation, no connection strings, no network setup (meets spec requirement)
- **Bundled with Python**: sqlite3 module ships with Python 3.13 (no external dependency, instant availability)
- **Development Velocity**: Developers can test persistence immediately without infrastructure setup
- **ACID Guarantees**: SQLite provides full ACID transactions (meets spec SC-003: 100% persistence across restarts)
- **WAL Mode Concurrency**: Write-Ahead Logging allows concurrent reads during writes (handles spec edge case)
- **File-Based Portability**: `todo.db` file is portable (copy to another machine, version control for test data)
- **SQLModel Abstraction**: ORM isolates application from database dialect (Phase II migration is code change, not rewrite)
- **User Isolation Enforcement**: user_id index enables fast filtering (Principle II: ALL queries filter by user_id)
- **Test Database Speed**: In-memory SQLite (`:memory:`) for tests is 100x faster than network database
- **Phase II Migration Path**: Alembic + SQLModel provide clear, documented migration to PostgreSQL
- **Cost**: $0 vs $20/month for managed PostgreSQL (acceptable for Phase I local development)

### Negative

- **Single-File Write Locks**: Only one writer at a time (write locks block other writes)
  - **Mitigation**: WAL mode reduces lock duration, Phase I has no multi-user concurrent writes
  - **Acceptable Because**: Spec scope is local console app (no concurrent write requirement)

- **No Remote Access**: Cannot share database across machines (single-file, no network protocol)
  - **Mitigation**: N/A - spec explicitly states local console app
  - **Acceptable Because**: Phase I scope is single-machine usage

- **File Size Limit**: ~1 TB maximum (SQLite limitation)
  - **Mitigation**: 1000 tasks/user × 1KB/task = 1MB (far below limit)
  - **Acceptable Because**: Spec requirements fit comfortably within limits

- **Phase II Migration Required**: Must migrate to PostgreSQL for web app (additional work)
  - **Mitigation**: SQLModel + Alembic provide structured migration path
  - **Acceptable Because**: Phase II explicitly calls for PostgreSQL (planned transition, not surprise)

- **Limited Concurrency**: Not suitable for high-concurrency web app (dozens of simultaneous writes)
  - **Mitigation**: Phase II migration to PostgreSQL resolves this
  - **Acceptable Because**: Phase I console has sequential operations, not concurrent

- **No Native JSON Queries**: SQLite JSON support is limited vs PostgreSQL JSONB
  - **Mitigation**: N/A - Task schema is relational, no JSON fields in Phase I
  - **Acceptable Because**: Spec requirements don't include JSON data

## Alternatives Considered

### Alternative 1: PostgreSQL (Neon DB)
**Approach**: Use managed PostgreSQL from the start (Neon Serverless PostgreSQL).

**Configuration**:
- Managed Service: Neon DB (auto-scaling, branching, point-in-time recovery)
- Connection: Network via DATABASE_URL environment variable
- Cost: $20/month for hobby tier
- ORM: SQLModel (same as SQLite)

**Pros**:
- ✅ Production-grade (high concurrency, replication, advanced features)
- ✅ No Phase II migration (skip migration effort)
- ✅ Point-in-time recovery (better disaster recovery than SQLite file backups)
- ✅ Branching (test schema changes in isolation)
- ✅ Native JSON support (JSONB with indexes)

**Cons**:
- ❌ **Over-Engineering for Phase I**: Console app doesn't need high concurrency or replication
- ❌ **Network Dependency**: Requires internet connection (spec: local console app)
- ❌ **Configuration Complexity**: DATABASE_URL secrets, connection pooling, network troubleshooting
- ❌ **Development Friction**: Developers need Neon account, database setup before coding
- ❌ **Cost**: $20/month vs $0 for SQLite (minor but adds up across team)
- ❌ **Startup Latency**: Network round-trip adds 10-50ms vs local file access <1ms

**Why Rejected**:
- Complexity far exceeds Phase I needs (console app, local usage, no concurrent writes)
- Violates Principle IV (Smallest Viable Change) - introduces network dependency unnecessarily
- Phase II will require PostgreSQL anyway (web app), so delaying migration is acceptable

### Alternative 2: MongoDB (MongoDB Atlas)
**Approach**: Use NoSQL document database for flexible schema.

**Configuration**:
- Managed Service: MongoDB Atlas (free tier M0)
- ORM: Motor (async MongoDB driver) or Beanie (Pydantic + Motor)
- Schema: Task document with embedded fields

**Pros**:
- ✅ Flexible schema (no migrations for schema evolution)
- ✅ JSON-native (nested documents, arrays)
- ✅ Free tier available (M0: 512MB storage)
- ✅ Horizontal scaling (sharding for massive datasets)

**Cons**:
- ❌ **Constitutional Violation**: Principle VI mandates SQLModel ORM (incompatible with MongoDB)
- ❌ **No ACID Guarantees**: Eventual consistency (violates spec SC-003: 100% persistence)
- ❌ **Network Dependency**: Requires internet (spec: local console app)
- ❌ **Schema Flexibility Not Needed**: Task schema is stable (no rapid evolution)
- ❌ **Phase II Migration**: FastAPI + SQLModel is canonical (MongoDB creates divergence)
- ❌ **Complexity**: Document modeling, denormalization patterns (overkill for simple Task table)

**Why Rejected**:
- Constitutional Principle VI explicitly requires SQLModel ORM (disqualifies MongoDB)
- Spec requires ACID guarantees (MongoDB's eventual consistency is insufficient)
- Task schema is stable and relational (NoSQL flexibility provides zero value)

### Alternative 3: PostgreSQL (Local with Docker)
**Approach**: Run PostgreSQL locally via Docker Compose (no managed service).

**Configuration**:
- Container: `docker-compose up postgres`
- Connection: localhost:5432
- Cost: $0 (self-hosted)
- ORM: SQLModel (same as SQLite)

**Pros**:
- ✅ No Phase II migration (production PostgreSQL from start)
- ✅ Free (no managed service cost)
- ✅ Production parity (dev/prod use same database engine)

**Cons**:
- ❌ **Docker Dependency**: Requires Docker Desktop installation and running
- ❌ **Developer Friction**: `docker-compose up` before coding, port conflicts, container management
- ❌ **Configuration Complexity**: docker-compose.yml, volume mounts, networking
- ❌ **Startup Overhead**: Container startup adds 3-5 seconds (spec: <2s app startup)
- ❌ **Over-Engineering**: Local PostgreSQL has same concurrency limitations as SQLite for single-user app

**Why Rejected**:
- Docker adds setup complexity without Phase I benefits (single-user console doesn't need PostgreSQL concurrency)
- Violates zero-configuration goal (spec: immediate development without infrastructure)
- Local PostgreSQL provides no advantage over SQLite for Phase I workload

## Migration Plan (SQLite → PostgreSQL)

**Timeline**: Phase II spec creation triggers migration planning

**Migration Steps**:

1. **Install Alembic** (migration tool):
   ```bash
   uv add alembic
   alembic init migrations
   ```

2. **Configure Alembic** for PostgreSQL:
   ```python
   # migrations/env.py
   from src.models import Task  # SQLModel models
   target_metadata = Task.metadata
   ```

3. **Update DATABASE_URL** (environment variable):
   ```bash
   # .env
   DATABASE_URL=postgresql://user:pass@neon.db/todo
   ```

4. **Generate Migration** (Alembic auto-detects schema):
   ```bash
   alembic revision --autogenerate -m "Initial schema"
   ```

5. **Apply Migration** to PostgreSQL:
   ```bash
   alembic upgrade head
   ```

6. **Export SQLite Data**:
   ```bash
   sqlite3 todo.db .dump > dump.sql
   ```

7. **Import to PostgreSQL** (custom script handles dialect differences):
   ```python
   # scripts/migrate_data.py
   # Read dump.sql, transform SQLite syntax to PostgreSQL, insert via SQLModel
   ```

8. **Validation Tests**:
   - Verify task count matches (SQLite vs PostgreSQL)
   - Verify user isolation (query by user_id, ensure cross-user access blocked)
   - Verify performance (p95 latency <500ms for Phase II SLO)

9. **Update Application Code** (minimal changes):
   ```python
   # src/services/db.py
   # Change: DATABASE_URL = "sqlite:///todo.db"
   # To: DATABASE_URL = os.getenv("DATABASE_URL")
   ```

10. **Test Phase II Application** with PostgreSQL:
    - Run full test suite (pytest)
    - Verify ≥80% coverage maintained
    - Load test (100 concurrent users, 1000 tasks/user)

**Rollback Plan** (if migration fails):
- Retain SQLite file as backup
- Revert DATABASE_URL to `sqlite:///todo.db`
- Re-run tests to verify rollback success

**Risk Mitigation**:
- **Test Migration on Staging**: Use Neon branch feature to test migration before production
- **Data Validation**: Automated script compares SQLite vs PostgreSQL row counts
- **Schema Differences**: Alembic auto-generates migration (handles INTEGER vs SERIAL, TEXT vs VARCHAR)

## References

- **Feature Spec**: `specs/001-add-task/spec.md` (FR-006: SQLite persistence, SC-003: 100% data persistence)
- **Implementation Plan**: `specs/001-add-task/plan.md` (lines 192-223: Database decision with alternatives)
- **Research**: `specs/001-add-task/research.md` (lines 79-144: Database research with 3 options evaluated)
- **Data Model**: `specs/001-add-task/data-model.md` (Task schema with constitutional fields)
- **Constitution**: `.specify/memory/constitution.md` (Principle VI: Database Standards, Principle II: User Isolation)
- **Related ADRs**:
  - **ADR-0002**: Phase I Technology Stack (SQLite as part of integrated Python stack)
  - **ADR-0003**: User Isolation Architecture (user_id index enforcement)
- **Evaluator Evidence**: `history/prompts/001-add-task/0002-add-task-architecture-plan.plan.prompt.md` (Constitution Check PASS, technology decisions)
