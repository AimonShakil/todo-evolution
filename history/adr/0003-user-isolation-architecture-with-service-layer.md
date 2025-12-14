# ADR-0003: User Isolation Architecture with Service Layer

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-08
- **Feature:** Phase I - Console Todo App
- **Context:** Constitutional Principle II mandates user data isolation - users must only access their own tasks, never other users' data. Phase I uses username strings for user identification (no authentication). Phase II will migrate to user_id integer foreign keys with Better Auth. The isolation mechanism must be foolproof (impossible for developers to forget), testable, and map cleanly to Phase II REST API patterns (`/api/{user_id}/tasks`).

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅ YES - Security-critical, affects all data access
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅ YES - Service layer vs repository vs manual filtering vs database RLS
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅ YES - Every CRUD operation must enforce isolation
-->

## Decision

**Adopt Service Layer pattern with mandatory user_id parameter on all CRUD methods to enforce user data isolation.**

**Architecture Components**:

1. **Service Layer**: `src/services/task_service.py`
   - All CRUD operations centralized in `TaskService` class
   - Every method requires `user_id: str` parameter (impossible to forget)
   - All database queries include `WHERE Task.user_id == user_id` filter
   - Single source of truth for isolation logic

2. **Database Indexing**: `user_id` column indexed for performance
   - `user_id: str = Field(index=True)` in Task model
   - Enables fast filtering with 10,000+ tasks per user

3. **CLI Integration**: Commands pass username to service layer
   - `todo add --username alice "Buy groceries"` → `task_service.add_task(user_id="alice", title="...")`
   - CLI layer has zero direct database access (must use service)

4. **Testing Strategy**: Integration tests verify isolation
   - `test_user_isolation.py`: User A cannot access User B's tasks
   - `test_user_isolation.py`: Attempting to access other user's task returns None/error

**Implementation Pattern**:
```python
class TaskService:
    def __init__(self, session: Session):
        self.session = session

    def get_all_tasks(self, user_id: str) -> list[Task]:
        """Get all tasks for user (enforces isolation)."""
        statement = select(Task).where(Task.user_id == user_id)
        return self.session.exec(statement).all()

    def get_task(self, user_id: str, task_id: int) -> Optional[Task]:
        """Get single task with ownership verification."""
        statement = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id  # Isolation enforced
        )
        return self.session.exec(statement).first()
```

## Consequences

### Positive

- **Foolproof Enforcement**: Mandatory `user_id` parameter means developers cannot forget to filter (compile-time safety via type hints)
- **Single Source of Truth**: All isolation logic in one place (task_service.py), easy to audit and test
- **Constitutional Compliance**: Satisfies Principle II (User Data Isolation) with explicit, testable enforcement
- **Phase II Migration Path**: Service methods map directly to FastAPI dependency injection:
  - Phase I: `task_service.get_all_tasks(user_id="alice")`
  - Phase II: `@app.get("/api/{user_id}/tasks")` with `task_service.get_all_tasks(user_id=user_id)`
- **Testability**: Service layer easily unit-testable with mock sessions, integration tests verify real isolation
- **Performance**: Database index on `user_id` enables <500ms operations with 10K tasks (SC-010)
- **Clear Boundaries**: CLI layer (presentation) separated from business logic (service) from data layer (model)

### Negative

- **Abstraction Overhead**: Additional layer between CLI and database (could be simpler with direct queries)
- **Session Management**: Service layer requires database session to be created and passed to constructor
- **Boilerplate**: Every CRUD method includes `WHERE user_id = ?` clause (repetitive but necessary)
- **Trust Boundary**: Still requires CLI layer to pass correct username (no authentication in Phase I)
- **Testing Duplication**: Both unit tests (service methods) and integration tests (user isolation) needed for full coverage

## Alternatives Considered

### Alternative 1: Repository Pattern with Generic Base
**Approach**: Create generic `Repository<T>` base class with user-scoped methods, inherit for `TaskRepository`.

**Architecture**:
```python
class Repository[T]:
    def find_by_user(self, user_id: str) -> list[T]: ...
    def get_by_id(self, user_id: str, id: int) -> Optional[T]: ...

class TaskRepository(Repository[Task]):
    # Inherits user-scoped methods
```

**Why Rejected**:
- ❌ **Over-Abstraction**: Generic repository adds complexity without value for Phase I (only 1 entity)
- ❌ **Phase II Misalignment**: FastAPI typically uses service layer pattern, not repository pattern
- ❌ **Boilerplate**: Repository requires interface definition + concrete implementation (more code than service layer)
- ✅ **Reusability**: If Phase II had 10+ entities, repository pattern would reduce duplication
- **Decision**: YAGNI - Service layer sufficient for Phase I, repository premature optimization

### Alternative 2: Manual WHERE Clauses in CLI Commands
**Approach**: CLI command functions directly query database with hand-written `WHERE user_id = ?` filters.

**Architecture**:
```python
@cli.command()
def view(username: str):
    session = get_session()
    statement = select(Task).where(Task.user_id == username)
    tasks = session.exec(statement).all()
    # Display tasks...
```

**Why Rejected**:
- ❌ **Error-Prone**: Developers can forget `WHERE user_id = ?` clause (security vulnerability)
- ❌ **No Single Source of Truth**: Isolation logic duplicated across 6 CLI commands
- ❌ **Hard to Test**: Must test CLI commands end-to-end, cannot unit test isolation logic separately
- ❌ **Tight Coupling**: CLI layer directly coupled to database schema (violates separation of concerns)
- ❌ **Phase II Migration**: No clean mapping to REST API (would need to rewrite all business logic)
- ✅ **Simplicity**: Fewer files, less abstraction
- **Decision**: Security risk and maintainability issues outweigh simplicity benefit

### Alternative 3: Database Row-Level Security (RLS)
**Approach**: Use SQLite triggers or PostgreSQL RLS policies to enforce user isolation at database level.

**Architecture**:
- Phase I: SQLite triggers reject queries without `user_id` filter (complex, error-prone)
- Phase II: PostgreSQL RLS policies: `CREATE POLICY user_isolation ON tasks USING (user_id = current_user_id())`

**Why Rejected**:
- ❌ **SQLite Limitations**: No native RLS support, triggers are hacky workaround, poor error messages
- ❌ **Testing Complexity**: Must set session variables for current_user_id, harder to write unit tests
- ❌ **Migration Risk**: Phase I SQLite triggers won't transfer to Phase II PostgreSQL (rewrite needed)
- ❌ **Debugging Difficulty**: Database-level enforcement makes debugging harder (queries fail silently)
- ✅ **Defense in Depth**: Database enforces isolation even if application code forgets
- ✅ **PostgreSQL RLS**: Would be excellent for Phase II multi-tenant web app
- **Decision**: Too complex for Phase I SQLite, revisit RLS as *additional* layer in Phase II (not primary mechanism)

### Alternative 4: Query Builder with Fluent API
**Approach**: Create fluent query builder that automatically adds user_id filters.

**Architecture**:
```python
tasks = TaskQuery(session).for_user(username).get_all()
task = TaskQuery(session).for_user(username).find_by_id(task_id)
```

**Why Rejected**:
- ❌ **Custom Implementation**: Requires building query builder abstraction (maintenance burden)
- ❌ **SQLModel Duplication**: Reimplements functionality SQLModel already provides
- ❌ **Harder to Debug**: Fluent API chains harder to debug than explicit service methods
- ✅ **Readability**: Fluent API reads well, clear intent
- **Decision**: Not worth custom implementation when service layer provides same guarantees with less code

## References

- Feature Spec: `specs/002-phase-i-console-app/spec.md`
  - FR-010: User data isolation with `WHERE user_id = ?`
  - US1 Scenario 3: User isolation testing (alice cannot see bob's tasks)
  - US5: Multi-user support
- Implementation Plan: `specs/002-phase-i-console-app/plan.md` (lines 35-36: Constitution check for Principle II)
- Research: `specs/002-phase-i-console-app/research.md`
  - Decision 4: User Isolation Pattern (lines 154-203)
  - Best Practice 2: User Data Isolation Enforcement (lines 374-377)
- Data Model: `specs/002-phase-i-console-app/data-model.md`
  - Lines 315-343: User isolation queries examples
  - Line 76: `user_id` indexed for performance
- Constitution: `.specify/memory/constitution.md` (Principle II: User Data Isolation)
- Related ADRs:
  - ADR-0002 (Technology Stack) - SQLModel sessions integrate with service layer
  - ADR-0001 (Future-Proof Data Architecture) - user_id migration from string to integer FK in Phase II
- PHR: `history/prompts/002-phase-i-console-app/0002-phase-i-implementation-planning.plan.prompt.md`
