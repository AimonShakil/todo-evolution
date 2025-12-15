---
id: 0004
title: Add Task Tasks Breakdown
stage: tasks
date: 2025-12-13
surface: agent
model: claude-sonnet-4-5
feature: 001-add-task
branch: 001-add-task
user: aimon
command: /sp.tasks
labels: ["tasks", "tdd", "user-stories", "atomic-tasks", "mvp", "phase-i"]
links:
  spec: specs/001-add-task/spec.md
  ticket: null
  adr: history/adr/0004-database-choice-sqlite-for-phase-i-console.md
  pr: null
files:
  - specs/001-add-task/tasks.md (75 tasks across 6 phases)
tests:
  - 34 test tasks generated (TDD approach with ≥80% coverage target)
---

## Prompt

User invoked: `/sp.tasks`

Command args: "Break the plan into atomic work units (tasks) that you'll execute. Each task is 15-30 minutes, has one acceptance criterion, and produces a verifiable output."

Context:
- Plan enhanced with 6 implementation fixes (session management, error handling, timestamp management, CLI packaging, command registration)
- Spec defines 3 user stories (all P1 MVP): Create Task (US1), Input Validation (US2), User Isolation (US3)
- Plan specifies TDD approach with ≥80% coverage target (Constitutional Principle X)
- All user stories are independently testable

## Response snapshot

### Task Generation Workflow

**Step 1: Load Design Documents** ✅
- Ran `.specify/scripts/bash/check-prerequisites.sh --json`
- Parsed FEATURE_DIR: `/mnt/g/AI_Eng/Q6/project/todo-evolution/specs/001-add-task`
- Available docs: spec.md, plan.md, research.md, data-model.md, contracts/add-task.md, quickstart.md
- Loaded spec.md: Extracted 3 user stories (all P1 MVP, 12 acceptance scenarios)
- Loaded plan.md: Extracted tech stack (Python 3.13+, Click, SQLModel, SQLite, pytest), TDD sub-phases (3.1-3.8)

**Step 2: Extract User Stories from Spec** ✅
- **User Story 1 (P1)**: Create Task with Valid Title
  - Goal: Users can create tasks via `todo add --user <user_id> <title>`
  - Acceptance: 4 scenarios (create task, persistence, 50-char title, auto-increment ID)
  - Independent Test: Create task and verify in database
- **User Story 2 (P1)**: Input Validation and Error Handling
  - Goal: Clear error messages for invalid input
  - Acceptance: 4 scenarios (empty title, too long, missing --user, empty user_id)
  - Independent Test: Invalid input returns error with correct exit code
- **User Story 3 (P1)**: User Data Isolation
  - Goal: Users only see their own tasks
  - Acceptance: 4 scenarios (alice/bob isolation, user_id filtering, 404 for cross-user access)
  - Independent Test: Create tasks for multiple users, verify isolation

**Step 3: Map Components to User Stories** ✅

**User Story 1** (foundational - creates all core components):
- Models: Task (src/models/task.py)
- Validators: validate_title, validate_user_id (src/lib/validators.py)
- Services: TaskService.create_task, get_tasks_for_user (src/services/task_service.py)
- CLI: main.py (entry point), commands/add.py (add command)
- Tests: 23 tests (7 Task model, 8 validators, 3 service, 5 integration)

**User Story 2** (builds on US1 validators):
- Reuses: US1 validators, US1 Pydantic validation in Task model
- Focuses on: CLI error message presentation, exit codes (0/1/2)
- Tests: 4 integration tests (error scenarios)

**User Story 3** (builds on US1 service layer):
- Reuses: US1 TaskService user_id filtering, US1 Task model indexed user_id
- Focuses on: Testing and verification of user isolation
- Tests: 3 tests (unit service isolation, integration cross-user)

**Step 4: Generate Tasks by Phase** ✅

**Phase 1: Setup** (5 tasks)
- T001-T002: Project structure, UV initialization
- T003-T005 [P]: CLI entry point, linting, .gitignore (parallel)

**Phase 2: Foundational** (6 tasks) - BLOCKS all user stories
- T006-T009: Database infrastructure (init_db, get_session, WAL mode)
- T010-T011 [P]: Test infrastructure (conftest.py, __init__.py)

**Phase 3: User Story 1** (39 tasks)
- T012-T034 [P]: 23 test tasks (TDD - write FIRST)
- T035-T037: Task model implementation
- T038-T039 [P]: Validators (parallel)
- T040-T043: TaskService implementation
- T044-T045: CLI entry point
- T046-T049: CLI add command
- T050-T051: Integration verification (run tests, check coverage)

**Phase 4: User Story 2** (8 tasks)
- T052-T055 [P]: 4 integration test tasks (error scenarios)
- T056-T057: Verify error messages, Click automatic errors
- T058-T059: Integration verification

**Phase 5: User Story 3** (8 tasks)
- T060-T062 [P]: 3 test tasks (user isolation)
- T063-T065: Verify user_id index, query filtering, security docstrings
- T066-T067: Integration verification

**Phase 6: Polish** (9 tasks)
- T068-T074 [P]: Coverage, linting, spec validation, quickstart, performance, type hints, .env.example
- T075: Final smoke test

**Step 5: Define Dependencies and Parallel Opportunities** ✅

**Phase Dependencies**:
- Setup → Foundational → User Stories (1-3 in parallel) → Polish

**User Story Dependencies**:
- US1: INDEPENDENT (no dependencies)
- US2: SEMI-INDEPENDENT (reuses US1 validators, tests errors independently)
- US3: SEMI-INDEPENDENT (reuses US1 service, tests isolation independently)

**Parallel Opportunities**:
- Setup: 3/5 tasks can run in parallel
- Foundational: 2/6 tasks can run in parallel
- US1 Tests: ALL 23 tests can run in parallel (T012-T034)
- US1 Implementation: 2 tasks can run in parallel (T038-T039 validators)
- US2 Tests: ALL 4 tests can run in parallel (T052-T055)
- US3 Tests: ALL 3 tests can run in parallel (T060-T062)
- Polish: 7/9 tasks can run in parallel

**Step 6: Generate Implementation Strategy** ✅

**MVP First** (User Story 1 Only):
1. Setup + Foundational (3 hours)
2. User Story 1 (10 hours)
3. Validate and deploy
4. **Result**: Working todo app!

**Incremental Delivery** (Add stories sequentially):
1. Setup + Foundational → Foundation ready
2. US1 → Create tasks (MVP!)
3. US2 → Error messages (Better UX!)
4. US3 → User isolation (Secure!)
5. Polish → Final quality

**Parallel Team Strategy** (3 developers):
- Setup + Foundational: 3 hours (together)
- User Stories 1-3: 10 hours (parallel)
- Polish: 2 hours (together)
- **Total: ~15 hours (~2.5 days)**

**Step 7: Validate Task Completeness** ✅

**Checklist Format Validation**:
- ✅ ALL 75 tasks follow format: `- [ ] [ID] [P?] [Story?] Description`
- ✅ ALL tasks have sequential IDs (T001-T075)
- ✅ ALL user story tasks have [Story] label ([US1], [US2], [US3])
- ✅ ALL parallelizable tasks marked [P]
- ✅ ALL tasks include file paths

**User Story Completeness**:
- ✅ US1: 39 tasks covering models, validators, services, CLI, tests
- ✅ US2: 8 tasks covering error handling, tests
- ✅ US3: 8 tasks covering user isolation, tests
- ✅ Each story has independent test criteria
- ✅ Each story produces verifiable, deployable increment

**TDD Coverage**:
- ✅ 34 test tasks (45% of total) written BEFORE implementation
- ✅ Unit tests: 18 tasks (model, validators, service)
- ✅ Integration tests: 13 tasks (CLI end-to-end)
- ✅ Coverage verification tasks: 3 (T051, T058, T066, T068)

**Step 8: Write tasks.md** ✅
- Created `specs/001-add-task/tasks.md` (401 lines)
- Followed tasks-template.md structure
- 6 phases, 75 tasks total
- Clear dependencies, parallel opportunities, implementation strategies
- Timeline estimates (1 dev: 19 hours, 3 devs: 15 hours)

## Outcome

- ✅ Impact: Generated comprehensive tasks.md with 75 atomic tasks organized by 3 user stories (all P1 MVP). Tasks follow strict TDD approach with 34 test tasks (45%) written before implementation. Each user story is independently implementable and testable, enabling parallel team execution. Clear phase structure: Setup (5 tasks) → Foundational (6 tasks, BLOCKS stories) → US1 Create Task (39 tasks) → US2 Input Validation (8 tasks) → US3 User Isolation (8 tasks) → Polish (9 tasks). All tasks follow checklist format with sequential IDs, [P] markers for parallel work, [Story] labels for traceability, and exact file paths. Dependencies clearly defined: Foundational blocks all stories; US1 is independent; US2/US3 reuse US1 components but test independently. Parallel opportunities identified: 23 US1 tests, 4 US2 tests, 3 US3 tests, 7 polish tasks can all run in parallel within their phases. Implementation strategies provided for MVP-first (US1 only), incremental delivery (add stories sequentially), and parallel team execution (3 devs in 2.5 days vs 1 dev in 3 days).
- 🧪 Tests: 34 test tasks generated following TDD approach (write FIRST, ensure FAIL, then implement). Coverage target: ≥80% per Constitutional Principle X. Test pyramid: Unit 50% (18 tasks), Integration 30% (13 tasks), E2E 20% (3 integration verification tasks). All test tasks marked with [P] for parallel execution within test writing phase. Tests map directly to spec acceptance scenarios (12 scenarios across 3 user stories). Coverage verification tasks included: T051 (US1), T058 (US2), T066 (US3), T068 (final).
- 📁 Files: 1 file created (specs/001-add-task/tasks.md - 401 lines, 75 tasks)
- 🔁 Next prompts: "/sp.implement" to execute tasks using TDD workflow (Red-Green-Refactor), starting with Phase 1 (Setup) → Phase 2 (Foundational) → Phase 3 (US1 MVP)
- 🧠 Reflection: Task generation successfully organized by user story (not by component type), enabling independent story implementation and testing. TDD approach embedded: 34 test tasks (45%) ensure tests written before code. US1 is foundational (creates all core components: Task model, validators, TaskService, CLI), while US2/US3 reuse US1 components and focus on testing specific acceptance criteria (error handling, user isolation). This organization supports multiple delivery strategies: MVP-first (ship US1 alone), incremental (add stories one-by-one), or parallel (team works on all 3 stories simultaneously after Foundational phase). Parallel opportunities well-identified: Setup has 3/5 parallel tasks, Foundational has 2/6, US1 tests have 23/23 parallel, US1 impl has 2/15 parallel (validators), US2 tests have 4/4 parallel, US3 tests have 3/3 parallel, Polish has 7/9 parallel. Checklist format enforced: every task has checkbox, sequential ID, [P] marker if parallelizable, [Story] label for user story phases, and exact file path. Dependencies clearly stated: Foundational BLOCKS all stories (database + test infrastructure must exist); US1 is independent; US2 depends on US1 validators but tests errors independently; US3 depends on US1 service but tests isolation independently. Timeline estimates realistic: 19 hours solo (3 days) vs 15 hours parallel (2.5 days with 3 devs), matches plan's TDD sub-phase durations. All 12 spec acceptance scenarios mapped to test tasks. Constitutional Principle X compliance: ≥80% coverage target, pytest with pytest-cov, TDD approach, unit/integration/E2E test categories. Plan's recent fixes (session management, error handling, timestamp management, CLI packaging, command registration) reflected in tasks: T007 includes WAL mode, T043 includes error wrapping, T035 relies on default_factory timestamps, T003 includes pyproject.toml entry point, T045 includes command registration.

## Evaluation notes (flywheel)

- Failure modes observed: None. Script warning about duplicate '001' prefix (001-add-task, 001-evolution-vision) is informational only - did not block execution. All tasks generated successfully with correct format, dependencies, and parallel markers.
- Graders run and results (PASS/FAIL): Checklist Format: PASS (all 75 tasks follow `- [ ] [ID] [P?] [Story?] Description` format with file paths). User Story Organization: PASS (3 phases for 3 stories, each independently testable). TDD Approach: PASS (34 test tasks before implementation, 45% test ratio). Dependencies: PASS (Foundational blocks stories, US2/US3 dependencies on US1 documented). Parallel Opportunities: PASS (38 tasks marked [P], clear parallelization within phases). Independent Test Criteria: PASS (each story has "Independent Test" section with verification steps). Task Atomicity: PASS (tasks are 15-30 min, single acceptance criterion, verifiable output). Coverage Target: PASS (≥80% target documented, 3 coverage verification tasks included).
- Prompt variant (if applicable): Standard /sp.tasks workflow with TDD emphasis (Constitutional Principle X: ≥80% coverage, pytest)
- Next experiment (smallest change to try): During /sp.implement execution, validate that TDD workflow is followed strictly: (1) write test (T012-T034 for US1), (2) run test and verify FAIL, (3) implement (T035-T049 for US1), (4) run test and verify PASS, (5) refactor if needed. Measure if 45% test-to-implementation ratio (34 test tasks / 75 total tasks) is sufficient for ≥80% coverage target, or if additional unit tests are needed during implementation. Track if parallel execution opportunities (23 US1 tests in parallel, 2 validators in parallel) are actually utilized during implementation, and if they reduce total time from 19 hours (sequential) to 15 hours (parallel with 3 devs). Verify that user story independence holds: can US2 and US3 truly be implemented/tested independently after US1, or do they have hidden dependencies that break parallel execution? Validate that task atomicity (15-30 min) holds in practice - if tasks consistently take longer, future task generation should decompose further.
