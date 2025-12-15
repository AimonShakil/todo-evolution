# Feature Specification: Phase I - Console Todo App

**Feature Branch**: `002-phase-i-console-app`
**Created**: 2025-12-08
**Status**: Draft
**Input**: User description: "Phase I: Console Todo App with Basic Features"
**Master Vision**: See `specs/001-evolution-vision/spec.md` for full 5-phase roadmap

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add and View Personal Tasks (Priority: P1) 🎯 MVP

**Description**: As a user, I need to add tasks with titles to my personal task list and view all my tasks, so I can track what I need to do.

**Why this priority**: This is the core value proposition of a todo app. Without the ability to add and view tasks, the application has no purpose. This story alone constitutes a minimal viable product.

**Independent Test**: Can be fully tested by opening the console app, adding 3 tasks with different titles, viewing the task list, and confirming all 3 tasks appear with correct titles.

**Acceptance Scenarios**:

1. **Given** I am a new user named "alice", **When** I add a task "Buy groceries", **Then** the system confirms task was added and assigns it a unique ID
2. **Given** I have added 3 tasks ("Buy groceries", "Finish report", "Call dentist"), **When** I view my tasks, **Then** all 3 tasks are displayed with their IDs, titles, and completion status (all incomplete)
3. **Given** I am user "alice" with 5 tasks, **When** user "bob" views their tasks, **Then** bob sees only their own tasks, not alice's tasks (user isolation)
4. **Given** I have added tasks and exited the app, **When** I restart the app and view tasks, **Then** all previously added tasks are still present (persistence)

---

### User Story 2 - Mark Tasks Complete (Priority: P1) 🎯 MVP

**Description**: As a user, I need to mark tasks as complete or incomplete so I can track my progress and know which tasks are finished.

**Why this priority**: Marking tasks complete is essential for tracking progress. Without this, users cannot distinguish between finished and unfinished tasks, severely limiting the app's usefulness.

**Independent Test**: Can be fully tested by adding 2 tasks, marking one as complete, viewing the task list to confirm completion status changed, then toggling it back to incomplete.

**Acceptance Scenarios**:

1. **Given** I have a task "Buy groceries" with ID 1 that is incomplete, **When** I mark task 1 as complete, **Then** the system confirms the task is now complete and viewing shows it as completed
2. **Given** I have a completed task with ID 2, **When** I mark task 2 as incomplete, **Then** the task returns to incomplete status (toggle behavior)
3. **Given** I attempt to mark task ID 999 as complete (task doesn't exist), **When** I execute the command, **Then** the system displays error "Task 999 not found" and no changes occur
4. **Given** I am user "alice" and try to mark task ID 10 as complete (belongs to user "bob"), **When** I execute the command, **Then** the system displays error "Task 10 not found" (user isolation enforced)

---

### User Story 3 - Update Task Details (Priority: P2)

**Description**: As a user, I need to update task titles so I can correct mistakes or refine task descriptions without deleting and re-creating tasks.

**Why this priority**: Users frequently need to correct typos or refine task descriptions. This improves user experience but is not critical for basic task tracking (users could delete and re-add as a workaround).

**Independent Test**: Can be fully tested by adding a task "Buy grocceries" (typo), updating it to "Buy groceries", and verifying the title changed correctly.

**Acceptance Scenarios**:

1. **Given** I have a task "Buy grocceries" with ID 1, **When** I update task 1 title to "Buy groceries", **Then** the system confirms update and viewing shows the corrected title
2. **Given** I attempt to update task title to an empty string, **When** I execute the update command, **Then** the system displays error "Title cannot be empty" and no changes occur
3. **Given** I attempt to update task title to a 300-character string (exceeds 200-char limit), **When** I execute the update command, **Then** the system displays error "Title must be 1-200 characters" and no changes occur
4. **Given** I am user "alice" and try to update task ID 10 (belongs to user "bob"), **When** I execute the update command, **Then** the system displays error "Task 10 not found" (user isolation enforced)

---

### User Story 4 - Delete Tasks (Priority: P2)

**Description**: As a user, I need to delete tasks I no longer need so my task list stays relevant and uncluttered.

**Why this priority**: Deleting tasks helps manage clutter but is not essential for basic task tracking. Users could work around this by marking unwanted tasks as complete.

**Independent Test**: Can be fully tested by adding 3 tasks, deleting one by ID, viewing the task list to confirm it's gone, and verifying the other 2 tasks remain.

**Acceptance Scenarios**:

1. **Given** I have 3 tasks with IDs 1, 2, 3, **When** I delete task 2, **Then** the system confirms deletion and viewing shows only tasks 1 and 3
2. **Given** I attempt to delete task ID 999 (doesn't exist), **When** I execute the delete command, **Then** the system displays error "Task 999 not found" and no changes occur
3. **Given** I am user "alice" and try to delete task ID 10 (belongs to user "bob"), **When** I execute the delete command, **Then** the system displays error "Task 10 not found" (user isolation enforced)
4. **Given** I delete all my tasks, **When** I view my task list, **Then** the system displays "No tasks found" message (empty state)

---

### User Story 5 - Multi-User Support (Priority: P3)

**Description**: As one of multiple users, I need to specify my username when using the app so my tasks are kept separate from other users' tasks.

**Why this priority**: Multi-user support demonstrates user isolation (constitutional requirement) but is less critical for a console app where each user typically runs their own instance. This prepares for Phase II web app migration.

**Independent Test**: Can be fully tested by running the app as user "alice", adding 2 tasks, then running as user "bob", adding 3 tasks, then viewing both users' task lists separately to confirm isolation.

**Acceptance Scenarios**:

1. **Given** I am user "alice" with 2 tasks, **When** user "bob" adds 3 tasks, **Then** alice still sees only her 2 tasks and bob sees only his 3 tasks
2. **Given** the system stores tasks for users "alice", "bob", "charlie", **When** I view database, **Then** all tasks have user_id field correctly set to respective usernames
3. **Given** I attempt to add a task without specifying username, **When** I execute the command, **Then** the system displays error "Username required" and no task is created
4. **Given** I specify username with special characters (e.g., "user@123"), **When** I add a task, **Then** the system accepts the username and creates the task (usernames are freeform strings in Phase I)

---

### Edge Cases

#### 1. Empty Database on First Run
- **Scenario**: User runs the app for the first time, no database file exists yet.
- **Handling**: System automatically creates `todo.db` SQLite file in the current directory, initializes the tasks table schema, and displays "Welcome! No tasks found. Add your first task to get started."

#### 2. Title with Maximum Length (200 Characters)
- **Scenario**: User adds a task with exactly 200 characters in the title.
- **Handling**: System accepts the task without truncation. If user tries 201 characters, system displays error "Title must be 1-200 characters" and rejects the task.

#### 3. Special Characters in Task Title
- **Scenario**: User adds a task with title "Buy milk & eggs (2 gallons) for $5.99 🥛".
- **Handling**: System accepts all special characters, Unicode emojis, and stores them correctly in SQLite. Display shows full title including emojis if terminal supports Unicode.

#### 4. Database Corruption or Missing File
- **Scenario**: User deletes `todo.db` file while app is running, then tries to add a task.
- **Handling**: System detects missing database connection, displays error "Database error: unable to connect. Check that todo.db exists and is readable.", and exits gracefully with exit code 1.

#### 5. Concurrent Access by Multiple Users
- **Scenario**: Two users (alice and bob) run the app simultaneously on the same machine, sharing the same `todo.db` file.
- **Handling**: SQLite handles concurrent reads automatically. For concurrent writes (both adding tasks at same time), SQLite's built-in locking prevents corruption. One user's write completes first, the other retries automatically (SQLite behavior). Both users' tasks are correctly saved.

#### 6. Very Large Task Lists (10,000+ Tasks)
- **Scenario**: User has accumulated 10,000 tasks over time and views their task list.
- **Handling**: System displays all tasks (no pagination in Phase I). Performance may degrade on slower terminals. If view takes >5 seconds, consider this acceptable for Phase I (pagination is Phase II enhancement).

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide command to add a new task with required title parameter and username parameter, assigning unique auto-incrementing ID
- **FR-002**: System MUST validate task title is 1-200 characters long before creating task, displaying clear error message if validation fails
- **FR-003**: System MUST validate username is non-empty before accepting any task operation, displaying error "Username required" if missing
- **FR-004**: System MUST provide command to view all tasks for a given username, displaying ID, title, and completion status for each task
- **FR-005**: System MUST provide command to mark a task as complete by ID and username, verifying task belongs to that user
- **FR-006**: System MUST provide command to mark a task as incomplete by ID and username (toggle behavior)
- **FR-007**: System MUST provide command to update task title by ID and username, validating new title is 1-200 characters
- **FR-008**: System MUST provide command to delete task by ID and username, verifying task belongs to that user
- **FR-009**: System MUST persist all tasks to local SQLite database file (`todo.db`) in the current directory
- **FR-010**: System MUST enforce user data isolation by filtering all queries with `WHERE user_id = ?` clause, preventing users from accessing other users' tasks
- **FR-011**: System MUST create database and tasks table automatically on first run if `todo.db` does not exist
- **FR-012**: System MUST include all future Phase V fields in Task schema (description, priority, tags, due_date, recurrence_pattern) as nullable columns to prevent schema migrations later
- **FR-013**: System MUST display user-friendly error messages for all validation failures (invalid ID, title too long, empty username, task not found, database errors)
- **FR-014**: System MUST return task ID immediately after successful add operation so user can reference it in subsequent operations
- **FR-015**: System MUST handle empty task lists gracefully by displaying "No tasks found" message instead of empty output
- **FR-016**: System MUST support task titles with Unicode characters including emojis if terminal supports them
- **FR-017**: System MUST prevent SQL injection by using parameterized queries for all database operations
- **FR-018**: System MUST store created_at and updated_at timestamps for all tasks (auto-managed by database triggers or application code)
- **FR-019**: System MUST exit with code 0 on successful operations and non-zero code (1) on errors for scripting compatibility
- **FR-020**: System MUST include help command that displays all available commands with usage examples

### Key Entities

#### Task Entity

**Attributes** (Phase I - Future-Proof Schema):
- `id`: Integer, primary key, auto-increment, uniquely identifies task
- `user_id`: String (username in Phase I, will migrate to integer foreign key in Phase II)
- `title`: String, required, 1-200 characters, describes what needs to be done
- `description`: String, nullable (unused in Phase I, will be used in Phase II+ for detailed task descriptions)
- `completed`: Boolean, default false, indicates if task is finished
- `priority`: String, nullable (unused in Phase I, will be enum high/medium/low in Phase V)
- `tags`: JSON array, nullable (unused in Phase I, will store tags in Phase V)
- `due_date`: DateTime, nullable (unused in Phase I, will store deadline in Phase V)
- `recurrence_pattern`: String, nullable (unused in Phase I, will store pattern like "daily"/"weekly" in Phase V)
- `created_at`: DateTime, auto-set on creation, tracks when task was added
- `updated_at`: DateTime, auto-update on any modification, tracks last change

**Relationships** (Phase I):
- No foreign key relationships (user_id is just a string, not referencing a users table)
- Independent entity (no dependencies on other tables in Phase I)

**Business Rules**:
- Title must be non-empty and ≤200 characters
- User_id must be non-empty string
- Completed defaults to false on creation
- All nullable Phase V fields (description, priority, tags, due_date, recurrence_pattern) must be NULL in Phase I
- Created_at and updated_at must be set automatically (user cannot manually override)

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can add a task with a title and view it in their task list within 10 seconds of app startup (from launch to seeing new task)
- **SC-002**: Users can add 100 tasks, view the list, and see all 100 tasks displayed without errors or data loss
- **SC-003**: Users can mark 10 tasks as complete, view the list, and see completion status correctly reflected for all 10 tasks
- **SC-004**: Users can update a task title 5 times in succession and see the latest title reflected each time
- **SC-005**: Users can delete 20 tasks from a list of 50 tasks and see exactly 30 tasks remaining
- **SC-006**: Two different users (alice and bob) can each add 10 tasks, and each user sees only their own 10 tasks (user isolation verified)
- **SC-007**: Users can exit the app, restart it, and see all previously added tasks still present (persistence verified)
- **SC-008**: Users encounter clear error messages for 10 different error scenarios (invalid ID, title too long, empty username, etc.) with 100% of errors being human-readable (no raw stack traces or database errors exposed to users)
- **SC-009**: System startup time is under 2 seconds on standard hardware (laptop with SSD) when database contains 1,000 tasks
- **SC-010**: All task operations (add, view, update, delete, complete) execute in under 500 milliseconds when database contains 10,000 tasks

### Quality Gates (Constitutional Compliance)

- **SC-101**: Test coverage is ≥80% measured by `pytest --cov-fail-under=80` (Constitutional Principle X)
- **SC-102**: All code passes `mypy --strict` with zero type errors (Constitutional Principle IX)
- **SC-103**: All code passes `black --check` formatting validation (Constitutional Principle IX)
- **SC-104**: All code passes `flake8` linting with zero violations (Constitutional Principle IX)
- **SC-105**: User isolation is verified by integration tests confirming user A cannot view/modify user B's tasks (Constitutional Principle II)
- **SC-106**: Database schema includes all future Phase V fields (nullable) verified by schema inspection showing description, priority, tags, due_date, recurrence_pattern columns (Constitutional Principle I - Future-Proof)

---

## Assumptions

1. **Single Machine Deployment**: Users run the console app on their local machine (not networked). Multiple users means multiple people using the same machine at different times, not concurrent network access.

2. **Terminal Environment**: Users have access to a command-line terminal (bash, zsh, PowerShell, cmd) with UTF-8 support for Unicode characters.

3. **SQLite Availability**: SQLite library is available in the environment (typically bundled with standard library, no separate installation needed).

4. **Working Directory Permissions**: Users have read/write permissions in the directory where they run the app (for creating/accessing `todo.db` file).

5. **Basic Terminal Literacy**: Users understand basic command-line concepts (running commands, reading text output, providing arguments).

6. **Username Convention**: Usernames are simple strings (alphanumeric, dashes, underscores) rather than formal identifiers. No authentication or password required in Phase I (console app trust model).

7. **Database Size Limits**: Database will not exceed 1GB or 1 million tasks in Phase I usage (reasonable limits for local SQLite file). Performance testing targets up to 10,000 tasks.

8. **No Concurrent Edits**: Multiple users won't simultaneously edit the same `todo.db` file in a way that creates conflicts (SQLite locking handles this, but UI doesn't need optimistic concurrency handling).

9. **Error Recovery**: If database becomes corrupted, users can delete `todo.db` and start fresh (no backup/restore in Phase I).

10. **Future Migration Path**: Users understand that Phase I is a stepping stone to Phase II web app, and data will be migrated (username strings → user IDs via migration script in Phase II).

---

## Out of Scope

The following features are **explicitly excluded** from Phase I and will be addressed in later phases:

1. **Web Interface**: No browser-based UI (console-only). Web UI comes in Phase II.

2. **User Authentication**: No passwords, login, or session management. Usernames are simple strings with no verification. Authentication comes in Phase II with Better Auth.

3. **Task Descriptions**: Tasks have titles only, no multi-line descriptions. Descriptions come in Phase II.

4. **Task Priority**: No high/medium/low priority levels. Priority comes in Phase V intermediate features.

5. **Task Tags**: No tagging or categorization system. Tags come in Phase V intermediate features.

6. **Due Dates**: No deadline tracking or overdue notifications. Due dates come in Phase V intermediate features.

7. **Task Recurrence**: No recurring tasks (daily, weekly, etc.). Recurrence comes in Phase V advanced features.

8. **Search/Filter**: No search by keyword or filter by completion status. Users view entire task list only. Search comes in Phase II.

9. **Task Sorting**: Tasks are displayed in ID order (creation order). No custom sorting options. Sorting comes in Phase II.

10. **Export/Import**: No data export to JSON/CSV or import from other apps. Export comes in Phase V with GDPR compliance.

11. **Undo/Redo**: No operation history or undo functionality. Changes are immediate and permanent.

12. **Rich Text Formatting**: Task titles are plain text only (no markdown, HTML, or formatting). Plain text only.

13. **Attachments**: No file attachments or links to external resources. Tasks are text-only.

14. **Collaboration**: No sharing tasks with other users or team features. Single-user context only (though multi-user capable via username isolation).

15. **Notifications/Reminders**: No proactive notifications about tasks. Users must open app to view tasks.

16. **Cloud Sync**: No synchronization across devices. Database is local file only. Cloud sync comes in Phase V.

17. **Mobile App**: No iOS/Android native apps. Console-only. Mobile is out of scope for all phases per master vision.

18. **Database Backup**: No automated backup system. Users responsible for backing up `todo.db` manually if needed. Automated backups come in Phase V.

19. **Performance Metrics**: No analytics, usage tracking, or telemetry. Basic application only.

20. **Multi-Language Support**: English-only error messages and help text. Internationalization out of scope.

---

## Dependencies

### External Libraries

**Required**:
- SQLite database (bundled with standard library, no separate installation)

**Optional**:
- Rich text terminal library (for enhanced console output formatting) - nice-to-have, not required

### Development Tools

**Required**:
- Python 3.13 or higher (constitutional requirement)
- pytest (for testing with ≥80% coverage requirement)
- pytest-cov (for coverage measurement)
- mypy (for type checking with --strict mode)
- black (for code formatting)
- flake8 (for linting)

### Related Specifications

- **Master Vision**: `specs/001-evolution-vision/spec.md` - Full 5-phase roadmap and constitutional alignment
- **Constitution**: `.specify/memory/constitution.md` - 28 constitutional principles governing all phases

### Phase II Migration Considerations

This specification is designed to facilitate migration to Phase II web app:

1. **Data Model Compatibility**: Task schema includes all Phase V fields (nullable) to avoid schema migrations
2. **User ID Migration Path**: Username strings in Phase I map to user.id integers in Phase II via migration script
3. **User Isolation Pattern**: Phase I enforces `WHERE user_id = ?` pattern that directly translates to Phase II `/api/{user_id}/tasks` REST API endpoints
4. **Stateless Architecture**: No in-memory state (database-backed only) aligns with Phase II stateless web app requirement

---

## Notes

- **This is a FOCUSED Phase I spec**: Covers console app only. See `specs/001-evolution-vision/spec.md` for full 5-phase vision.
- **Future-Proof Data Model**: All Phase V fields included from Phase I (nullable) per constitutional requirement to prevent schema migrations.
- **User Isolation from Day 1**: Enforces `WHERE user_id = ?` pattern in Phase I to prepare for Phase II multi-tenant web app.
- **Constitutional Compliance**: Spec adheres to Principles I (Spec-Driven), II (User Isolation), IV (Stateless), IX (Code Quality), X (Testing).
- **Success-Driven**: 16 measurable success criteria to validate delivery quality (10 user-facing outcomes + 6 quality gates).
- **Scope-Controlled**: 20 explicit "Out of Scope" items prevent feature creep and keep Phase I focused on console app basics.
- **Migration-Ready**: Designed for clean migration to Phase II web app (username → user_id, SQLite → PostgreSQL, console → REST API).
