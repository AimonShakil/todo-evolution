# Tasks: Phase II - Full-Stack Web Application

**Input**: Design documents from `/specs/003-phase-ii-web-app/` and `/specs/001-evolution-vision/`
**Prerequisites**: plan.md (completed), spec.md (evolution-vision covers Phase II requirements)

**Tests**: Test tasks included as tests are mandatory per Constitutional Principle X (≥80% coverage)

**Organization**: Tasks are grouped by implementation step (STEP 0-6) aligning with the plan.md structure

## Format: `[ID] [P?] [Step] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Step]**: STEP 0-6 from plan.md (granular sub-steps for clarity)
- Include exact file paths in descriptions

## Path Conventions

- **Web app monorepo**: `backend/src/`, `frontend/src/`, `backend/tests/`, `frontend/tests/`
- Paths follow plan.md structure (frontend/ and backend/ directories)

---

## Phase 1: Setup (STEP 0 - Environment & Migration Planning)

**Purpose**: Environment setup, database configuration, and research

**Duration**: 4-6 hours

### STEP 0.1: Neon PostgreSQL Setup

- [ ] T001 Create Neon PostgreSQL project at https://console.neon.tech
- [ ] T002 Create production database in Neon project (name: `todo-evolution`)
- [ ] T003 Copy connection string from Neon dashboard

### STEP 0.2: Backend Environment Configuration

- [ ] T004 Create backend/.env file with DATABASE_URL (Neon connection string)
- [ ] T005 Create backend/.env.example with placeholder values for documentation

### STEP 0.3: Better Auth Credentials Setup

- [ ] T006 Generate BETTER_AUTH_SECRET using `openssl rand -base64 32`
- [ ] T007 Generate JWT_SECRET using `openssl rand -base64 32`
- [ ] T008 Add both secrets to backend/.env
- [ ] T009 Add secret placeholders to backend/.env.example

### STEP 0.4: Research FastAPI + Better Auth (Context7 MCP)

- [ ] T010 [P] Use Context7 MCP: "How to implement Better Auth with FastAPI in 2025?"
- [ ] T011 [P] Use Context7 MCP: "What's the latest FastAPI JWT middleware pattern 2025?"
- [ ] T012 [P] Use Context7 MCP: "FastAPI async route handlers with SQLModel best practices"

### STEP 0.5: Research Next.js 16 + Better Auth (Context7 MCP)

- [ ] T013 [P] Use Context7 MCP: "Next.js 16 App Router server components best practices 2025"
- [ ] T014 [P] Use Context7 MCP: "Next.js 16 authentication with Better Auth React hooks 2025"
- [ ] T015 [P] Use Context7 MCP: "How to configure CORS for Next.js 16+ frontend with FastAPI backend?"

### STEP 0.6: Database Migration Strategy

- [ ] T016 Document SQLite → PostgreSQL migration strategy in specs/003-phase-ii-web-app/data-model.md
- [ ] T017 Design user table schema (id, email, name, created_at, updated_at) in data-model.md
- [ ] T018 Design tasks table schema migration (user_id string → integer FK) in data-model.md
- [ ] T019 Document RI (Reusable Intelligence) components from Phase I in data-model.md

### STEP 0.7: Alembic Setup

- [ ] T020 Install Alembic in backend: `cd backend && uv add alembic`
- [ ] T021 Initialize Alembic: `cd backend && alembic init alembic`
- [ ] T022 Configure alembic.ini with Neon DATABASE_URL
- [ ] T023 Update alembic/env.py to import SQLModel metadata

**Checkpoint**: Environment configured, research complete, migration strategy documented

---

## Phase 2: Foundational (STEP 1 - Backend Foundation)

**Purpose**: Core backend infrastructure - BLOCKS all user stories until complete

**Duration**: 12-16 hours

**⚠️ CRITICAL**: No frontend or user story work can begin until this phase is complete

### STEP 1.1: Database Models (RI: Reuses Phase I Task Model)

- [ ] T024 [P] Create backend/src/models/__init__.py
- [ ] T025 [P] Migrate Task model from Phase I src/models/task.py to backend/src/models/task.py (adapt for PostgreSQL)
- [ ] T026 [P] Create User model in backend/src/models/user.py (id, email, name, created_at, updated_at) for Better Auth
- [ ] T027 Update Task model user_id field to Integer foreign key referencing users.id in backend/src/models/task.py
- [ ] T028 Verify SQLModel imports and table=True on both models

### STEP 1.2: Database Migrations

- [ ] T029 Create Alembic migration for users table: `alembic revision --autogenerate -m "create users table"`
- [ ] T030 Create Alembic migration for tasks table: `alembic revision --autogenerate -m "create tasks table with user_id FK"`
- [ ] T031 Review generated migration files in backend/alembic/versions/
- [ ] T032 Run migrations against Neon: `alembic upgrade head`
- [ ] T033 Verify schema in Neon using psql or PostgreSQL MCP: `\d users` and `\d tasks`

### STEP 1.3: Database Session Management (RI: Reuses Phase I db.py)

- [ ] T034 Create backend/src/services/__init__.py
- [ ] T035 Migrate db.py from Phase I src/services/db.py to backend/src/services/db.py
- [ ] T036 Update DATABASE_URL to load from environment in backend/src/services/db.py
- [ ] T037 Update engine creation for PostgreSQL (replace SQLite-specific config) in backend/src/services/db.py
- [ ] T038 Test database connection: create test script backend/test_db_connection.py

### STEP 1.4: FastAPI Application Setup

- [ ] T039 Create backend/src/main.py with FastAPI app initialization
- [ ] T040 Add CORS middleware in backend/src/main.py (allow http://localhost:3000 for Next.js dev)
- [ ] T041 Add rate limiting middleware using slowapi in backend/src/main.py (100 req/min per user)
- [ ] T042 Configure structured JSON logging in backend/src/main.py
- [ ] T043 Create health check endpoint GET /health in backend/src/main.py
- [ ] T044 Test FastAPI app starts: `uvicorn src.main:app --reload`

### STEP 1.5: Better Auth Integration (JWT Validation)

- [ ] T045 Install Better Auth Python SDK: `uv add better-auth-python python-jose passlib`
- [ ] T046 Create backend/src/config.py for environment variables (DATABASE_URL, BETTER_AUTH_SECRET, JWT_SECRET)
- [ ] T047 Create backend/src/services/auth_service.py with JWT decode function
- [ ] T048 Implement JWT validation middleware in backend/src/services/auth_service.py (extract user_id from token)
- [ ] T049 Add auth dependency function `get_current_user()` in backend/src/services/auth_service.py
- [ ] T050 Test JWT validation with mock token in backend/test_jwt_validation.py

### STEP 1.6: Authentication Routes

- [ ] T051 Create backend/src/routes/__init__.py
- [ ] T052 Create backend/src/routes/auth.py
- [ ] T053 Implement POST /api/auth/signup endpoint in backend/src/routes/auth.py (create user, hash password)
- [ ] T054 Implement POST /api/auth/signin endpoint in backend/src/routes/auth.py (verify password, return JWT)
- [ ] T055 Register auth routes in backend/src/main.py
- [ ] T056 Test signup/signin with curl or httpx

### STEP 1.7: Task Service (RI: Reuses Phase I TaskService, Made Async)

- [ ] T057 Migrate TaskService from Phase I src/services/task_service.py to backend/src/services/task_service.py
- [ ] T058 Convert all TaskService methods to async in backend/src/services/task_service.py
- [ ] T059 Update TaskService.create_task() signature for async session in backend/src/services/task_service.py
- [ ] T060 Update TaskService.get_tasks_for_user() for async session in backend/src/services/task_service.py
- [ ] T061 Add TaskService.get_task_by_id() method in backend/src/services/task_service.py
- [ ] T062 Add TaskService.update_task() method in backend/src/services/task_service.py
- [ ] T063 Add TaskService.delete_task() method in backend/src/services/task_service.py
- [ ] T064 Preserve SECURITY CRITICAL docstrings from Phase I in backend/src/services/task_service.py

### STEP 1.8: Validation Logic (RI: Reuses Phase I Validators)

- [ ] T065 Create backend/src/lib/__init__.py
- [ ] T066 Migrate validators.py from Phase I src/lib/validators.py to backend/src/lib/validators.py
- [ ] T067 Create Pydantic request models in backend/src/lib/schemas.py (CreateTaskRequest, UpdateTaskRequest)
- [ ] T068 Integrate validate_title() into CreateTaskRequest model in backend/src/lib/schemas.py
- [ ] T069 Integrate validate_user_id() into auth middleware in backend/src/services/auth_service.py

### STEP 1.9: Task API Endpoints

- [ ] T070 Create backend/src/routes/tasks.py
- [ ] T071 Implement POST /api/{user_id}/tasks endpoint in backend/src/routes/tasks.py (create task, verify JWT user matches path user_id)
- [ ] T072 Implement GET /api/{user_id}/tasks endpoint in backend/src/routes/tasks.py (list tasks with pagination ?page=1&limit=20)
- [ ] T073 Implement GET /api/{user_id}/tasks/{task_id} endpoint in backend/src/routes/tasks.py (get single task, verify ownership)
- [ ] T074 Implement PUT /api/{user_id}/tasks/{task_id} endpoint in backend/src/routes/tasks.py (full update, verify ownership)
- [ ] T075 Implement PATCH /api/{user_id}/tasks/{task_id}/complete endpoint in backend/src/routes/tasks.py (toggle completed status)
- [ ] T076 Implement DELETE /api/{user_id}/tasks/{task_id} endpoint in backend/src/routes/tasks.py (delete task, verify ownership)
- [ ] T077 Add user isolation check: verify JWT user_id matches URL {user_id} (401 if mismatch) in all endpoints
- [ ] T078 Add error handling and consistent error format `{error: string, details?: object}` in backend/src/routes/tasks.py
- [ ] T079 Register task routes in backend/src/main.py
- [ ] T080 Test all endpoints with curl or Postman

**Checkpoint**: Backend foundation complete - all API endpoints functional with JWT auth and user isolation

---

## Phase 3: Backend Testing (STEP 2 - Backend Testing)

**Purpose**: Achieve ≥80% backend test coverage

**Duration**: 8-10 hours

### STEP 2.1: Unit Tests (RI: Reuses Phase I Test Patterns)

- [ ] T081 Create backend/tests/unit/__init__.py
- [ ] T082 Create backend/tests/conftest.py with async test fixtures (async_session, test_db)
- [ ] T083 [P] Migrate test_task_service.py unit tests from Phase I to backend/tests/unit/test_task_service.py (convert to async)
- [ ] T084 [P] Create backend/tests/unit/test_auth_service.py for JWT validation tests
- [ ] T085 [P] Create backend/tests/unit/test_validators.py for Pydantic schema validation tests
- [ ] T086 [P] Create backend/tests/unit/test_models.py for SQLModel model tests
- [ ] T087 Run unit tests: `pytest backend/tests/unit/ -v`
- [ ] T088 Verify unit test coverage: `pytest backend/tests/unit/ --cov=backend/src --cov-report=term-missing`

### STEP 2.2: Integration Tests (RI: Reuses Phase I Isolation Tests)

- [ ] T089 Create backend/tests/integration/__init__.py
- [ ] T090 Create backend/tests/integration/test_auth_endpoints.py
- [ ] T091 Test POST /api/auth/signup (valid user creation) in backend/tests/integration/test_auth_endpoints.py
- [ ] T092 Test POST /api/auth/signin (valid login, JWT returned) in backend/tests/integration/test_auth_endpoints.py
- [ ] T093 Test POST /api/auth/signin (invalid credentials, 401) in backend/tests/integration/test_auth_endpoints.py
- [ ] T094 Create backend/tests/integration/test_task_endpoints.py
- [ ] T095 Test POST /api/{user_id}/tasks (create task, verify response) using httpx.AsyncClient
- [ ] T096 Test GET /api/{user_id}/tasks (list tasks, pagination) using httpx.AsyncClient
- [ ] T097 Test GET /api/{user_id}/tasks/{task_id} (get task detail) using httpx.AsyncClient
- [ ] T098 Test PUT /api/{user_id}/tasks/{task_id} (full update) using httpx.AsyncClient
- [ ] T099 Test PATCH /api/{user_id}/tasks/{task_id}/complete (mark complete) using httpx.AsyncClient
- [ ] T100 Test DELETE /api/{user_id}/tasks/{task_id} (delete task) using httpx.AsyncClient
- [ ] T101 Test user isolation: Alice cannot access /api/bob/tasks (expect 401) in backend/tests/integration/test_task_endpoints.py
- [ ] T102 Test user isolation: Bob cannot access Alice's task via /api/bob/tasks/{alice-task-id} (expect 404) in backend/tests/integration/test_task_endpoints.py
- [ ] T103 Test rate limiting: send 120 requests, verify 101st returns 429 in backend/tests/integration/test_rate_limiting.py
- [ ] T104 Test pagination: create 30 tasks, verify ?limit=20 returns 20 in backend/tests/integration/test_task_endpoints.py
- [ ] T105 Run integration tests: `pytest backend/tests/integration/ -v`

### STEP 2.3: Coverage Verification

- [ ] T106 Run full backend test suite: `pytest backend/tests/ -v`
- [ ] T107 Generate coverage report: `pytest backend/tests/ --cov=backend/src --cov-report=html --cov-fail-under=80`
- [ ] T108 Review coverage report in backend/htmlcov/index.html
- [ ] T109 Add missing tests if coverage <80%
- [ ] T110 Document test results in specs/003-phase-ii-web-app/test-results.md

**Checkpoint**: Backend tests passing with ≥80% coverage, user isolation verified

---

## Phase 4: Frontend Foundation (STEP 3 - Frontend Foundation)

**Purpose**: Build Next.js 16 frontend with Shadcn/ui (Slate theme)

**Duration**: 12-16 hours

### STEP 3.1: Next.js Project Initialization

- [ ] T111 Create frontend/ directory: `mkdir frontend && cd frontend`
- [ ] T112 Initialize Next.js 16 project: `npx create-next-app@latest . --typescript --tailwind --app --no-src-dir`
- [ ] T113 Configure TypeScript strict mode in frontend/tsconfig.json (`"strict": true`)
- [ ] T114 Verify Tailwind CSS 4.x configured in frontend/tailwind.config.ts
- [ ] T115 Test Next.js dev server: `npm run dev` (verify http://localhost:3000 works)

### STEP 3.2: Shadcn/ui Setup (Slate Theme)

- [ ] T116 Initialize Shadcn/ui: `npx shadcn@latest init` (choose Slate theme, TypeScript, App Router)
- [ ] T117 Add Button component: `npx shadcn@latest add button`
- [ ] T118 Add Card component: `npx shadcn@latest add card`
- [ ] T119 Add Form component: `npx shadcn@latest add form`
- [ ] T120 Add Input component: `npx shadcn@latest add input`
- [ ] T121 Add Label component: `npx shadcn@latest add label`
- [ ] T122 Add Checkbox component: `npx shadcn@latest add checkbox`
- [ ] T123 Add Dialog component: `npx shadcn@latest add dialog`
- [ ] T124 Add DropdownMenu component: `npx shadcn@latest add dropdown-menu`
- [ ] T125 Add Separator component: `npx shadcn@latest add separator`
- [ ] T126 Add Toast component: `npx shadcn@latest add toast`
- [ ] T127 Verify all components in frontend/components/ui/
- [ ] T128 Install Lucide React icons: `npm install lucide-react`

### STEP 3.3: Better Auth Client Configuration

- [ ] T129 Install Better Auth React: `npm install better-auth-react @better-auth/client`
- [ ] T130 Create frontend/lib/auth.ts with Better Auth client config (API URL: http://localhost:8000/api/auth)
- [ ] T131 Create frontend/lib/types.ts with TypeScript types (User, Task, CreateTaskRequest, etc.)
- [ ] T132 Configure shared BETTER_AUTH_SECRET in frontend/.env.local
- [ ] T133 Create frontend/.env.example with placeholder values

### STEP 3.4: API Client Abstraction

- [ ] T134 Create frontend/lib/api.ts with API client class
- [ ] T135 Implement API client methods in frontend/lib/api.ts: signup(), signin(), getTasks(), createTask(), updateTask(), completeTask(), deleteTask()
- [ ] T136 Add JWT token header injection in all API client methods
- [ ] T137 Add error handling (401 → redirect to signin) in API client
- [ ] T138 Test API client with backend running: create test in frontend/lib/__tests__/api.test.ts

### STEP 3.5: Root Layout & Theme

- [ ] T139 Update frontend/app/layout.tsx with Better Auth provider wrapper
- [ ] T140 Add ThemeProvider for dark mode support in frontend/app/layout.tsx
- [ ] T141 Create frontend/app/globals.css with Slate theme CSS variables
- [ ] T142 Add Toaster component to frontend/app/layout.tsx for toast notifications

### STEP 3.6: Landing Page

- [ ] T143 Create frontend/app/page.tsx (landing page with "Sign In" and "Sign Up" buttons)
- [ ] T144 Add hero section with project title and description
- [ ] T145 Add navigation links using Shadcn Button components

### STEP 3.7: Authentication Pages

- [ ] T146 Create frontend/app/auth/signup/page.tsx
- [ ] T147 Build signup form using Shadcn Card + Form + Input components in frontend/app/auth/signup/page.tsx
- [ ] T148 Add Zod validation schema for signup form (email, password validation)
- [ ] T149 Handle signup submission, call API client signup(), show toast on success/error
- [ ] T150 Redirect to /tasks on successful signup
- [ ] T151 Create frontend/app/auth/signin/page.tsx
- [ ] T152 Build signin form using Shadcn Card + Form + Input components in frontend/app/auth/signin/page.tsx
- [ ] T153 Add Zod validation schema for signin form
- [ ] T154 Handle signin submission, call API client signin(), store JWT in httpOnly cookie
- [ ] T155 Redirect to /tasks on successful signin
- [ ] T156 Test signup → signin flow manually

### STEP 3.8: Task List Page (Server Component)

- [ ] T157 Create frontend/app/tasks/page.tsx as React Server Component
- [ ] T158 Fetch tasks from API in server component (use cookies for JWT)
- [ ] T159 Render task list using Shadcn Card component
- [ ] T160 Add "Add Task" button that opens dialog
- [ ] T161 Add empty state message if no tasks

### STEP 3.9: Task Components

- [ ] T162 Create frontend/components/TaskList.tsx (display list of tasks in Card)
- [ ] T163 Create frontend/components/TaskItem.tsx (single task with Checkbox + DropdownMenu)
- [ ] T164 Add task complete toggle using Shadcn Checkbox in TaskItem component
- [ ] T165 Add task actions dropdown (Edit, Delete) using Shadcn DropdownMenu in TaskItem component
- [ ] T166 Handle task complete/uncomplete action (call API, refresh list)
- [ ] T167 Handle task delete action (call API, show confirmation toast, refresh list)

### STEP 3.10: Task Form Dialog (Add/Edit)

- [ ] T168 Create frontend/components/TaskForm.tsx with Shadcn Dialog + Form
- [ ] T169 Add Zod validation schema for task form (title 1-200 chars)
- [ ] T170 Handle task creation (call API client createTask(), close dialog, show toast, refresh list)
- [ ] T171 Handle task editing (pre-fill form, call API client updateTask(), close dialog, show toast, refresh list)
- [ ] T172 Add loading state with Shadcn Button disabled + Loader2 icon during submission

### STEP 3.11: Responsive Design & Polish

- [ ] T173 Test mobile layout (375px width) - verify all components responsive
- [ ] T174 Test tablet layout (768px width) - verify grid/flexbox adapts
- [ ] T175 Test desktop layout (1920px width) - verify max-width constraints
- [ ] T176 Add Tailwind responsive classes (sm:, md:, lg:) where needed
- [ ] T177 Verify keyboard navigation works (Tab, Enter, Escape) for all interactive elements
- [ ] T178 Test dark mode toggle (if implemented)

**Checkpoint**: Frontend complete with professional Shadcn/ui (Slate theme), fully responsive, accessible

---

## Phase 5: Frontend Testing & Accessibility (STEP 4)

**Purpose**: Achieve ≥80% frontend coverage, Lighthouse ≥90

**Duration**: 8-12 hours

### STEP 4.1: Component Tests

- [ ] T179 Install testing dependencies: `npm install --save-dev @testing-library/react @testing-library/jest-dom vitest`
- [ ] T180 Create frontend/vitest.config.ts
- [ ] T181 Create frontend/components/__tests__/TaskForm.test.tsx
- [ ] T182 Test TaskForm valid input submission in frontend/components/__tests__/TaskForm.test.tsx
- [ ] T183 Test TaskForm validation errors (empty title, too long title) in frontend/components/__tests__/TaskForm.test.tsx
- [ ] T184 Create frontend/components/__tests__/TaskList.test.tsx
- [ ] T185 Test TaskList empty state display in frontend/components/__tests__/TaskList.test.tsx
- [ ] T186 Test TaskList populated state with 3 tasks in frontend/components/__tests__/TaskList.test.tsx
- [ ] T187 Create frontend/components/__tests__/TaskItem.test.tsx
- [ ] T188 Test TaskItem complete toggle action in frontend/components/__tests__/TaskItem.test.tsx
- [ ] T189 Test TaskItem delete action with confirmation in frontend/components/__tests__/TaskItem.test.tsx
- [ ] T190 Install msw (Mock Service Worker): `npm install --save-dev msw`
- [ ] T191 Create frontend/mocks/handlers.ts with API mock handlers
- [ ] T192 Mock API calls in all component tests using msw
- [ ] T193 Run component tests: `npm run test`
- [ ] T194 Generate coverage report: `npm run test -- --coverage`

### STEP 4.2: E2E Tests with Playwright MCP

- [ ] T195 Install Playwright: `npm install --save-dev @playwright/test`
- [ ] T196 Initialize Playwright: `npx playwright install`
- [ ] T197 Create frontend/tests/e2e/auth.spec.ts
- [ ] T198 Test E2E: signup → verify redirect to /tasks in frontend/tests/e2e/auth.spec.ts
- [ ] T199 Test E2E: signin → verify redirect to /tasks in frontend/tests/e2e/auth.spec.ts
- [ ] T200 Create frontend/tests/e2e/tasks.spec.ts
- [ ] T201 Test E2E: signin → create task → verify in list in frontend/tests/e2e/tasks.spec.ts
- [ ] T202 Test E2E: create task → mark complete → verify status change in frontend/tests/e2e/tasks.spec.ts
- [ ] T203 Test E2E: create task → delete task → verify removal in frontend/tests/e2e/tasks.spec.ts
- [ ] T204 Test E2E cross-user isolation: Alice creates task → Bob signs in → verify Alice's task not visible in frontend/tests/e2e/tasks.spec.ts
- [ ] T205 Run Playwright tests: `npx playwright test`
- [ ] T206 Review Playwright test report: `npx playwright show-report`

### STEP 4.3: Accessibility Audit (Shadcn/ui Guarantees WCAG 2.1 AA)

- [ ] T207 Install Lighthouse CI: `npm install --save-dev @lhci/cli`
- [ ] T208 Create frontend/lighthouserc.json config
- [ ] T209 Run Lighthouse audit on /tasks page: `npx lhci autorun`
- [ ] T210 Verify Lighthouse performance score ≥90
- [ ] T211 Verify Lighthouse accessibility score ≥90
- [ ] T212 Verify Lighthouse best practices score ≥90
- [ ] T213 Install axe DevTools browser extension
- [ ] T214 Run axe scan on signup page, fix critical violations (if any)
- [ ] T215 Run axe scan on signin page, fix critical violations (if any)
- [ ] T216 Run axe scan on tasks page, fix critical violations (if any)
- [ ] T217 Test keyboard navigation: Tab through all forms and buttons
- [ ] T218 Verify focus indicators visible on all interactive elements
- [ ] T219 Test screen reader (NVDA/VoiceOver) on signup form
- [ ] T220 Verify color contrast 4.5:1 for normal text (Shadcn Slate theme auto-handles)
- [ ] T221 Test responsive design on mobile (iPhone SE 375px), tablet (iPad 768px), desktop (1920px)
- [ ] T222 Document accessibility test results in specs/003-phase-ii-web-app/accessibility-report.md

**Checkpoint**: Frontend tests passing with ≥80% coverage, Lighthouse ≥90, axe 0 critical violations

---

## Phase 6: Performance Optimization (STEP 5)

**Purpose**: Achieve p95 <500ms backend, FCP <1.5s frontend

**Duration**: 6-8 hours

### STEP 5.1: Backend Performance

- [ ] T223 Enable SQLAlchemy query logging in backend/src/services/db.py (echo=True for dev)
- [ ] T224 Review query logs for N+1 queries (task list endpoint)
- [ ] T225 Fix N+1 queries using joinedload() or selectinload() if found
- [ ] T226 Configure PostgreSQL connection pooling in backend/src/services/db.py (pool_size=10, max_overflow=20)
- [ ] T227 Add database indexes: CREATE INDEX idx_tasks_user_id ON tasks(user_id) in Alembic migration
- [ ] T228 Add database indexes: CREATE INDEX idx_tasks_completed ON tasks(completed) in Alembic migration
- [ ] T229 Run new migration: `alembic upgrade head`
- [ ] T230 Install Locust: `pip install locust`
- [ ] T231 Create backend/locustfile.py for load testing (100 users, 10 req/sec, 5 minutes)
- [ ] T232 Run load test: `locust -f backend/locustfile.py --users 100 --spawn-rate 10 --run-time 5m`
- [ ] T233 Analyze load test results (p95, p99 latency)
- [ ] T234 Verify p95 latency <500ms under 100 concurrent users
- [ ] T235 Document performance results in specs/003-phase-ii-web-app/performance-results.md

### STEP 5.2: Frontend Performance

- [ ] T236 Run Next.js production build: `npm run build`
- [ ] T237 Analyze bundle size in build output (main bundle target <200KB gzipped)
- [ ] T238 Optimize images: convert PNGs to WebP, use Next.js Image component
- [ ] T239 Verify code splitting: check .next/static/chunks/ for route-based splits
- [ ] T240 Run Lighthouse CI on production build: `npx lhci autorun --url=http://localhost:3000/tasks`
- [ ] T241 Verify FCP (First Contentful Paint) <1.5s
- [ ] T242 Verify LCP (Largest Contentful Paint) <2.5s
- [ ] T243 Verify TTI (Time to Interactive) <3.5s
- [ ] T244 Optimize Shadcn/ui component imports (tree-shaking already handled)
- [ ] T245 Document frontend performance results in specs/003-phase-ii-web-app/performance-results.md

**Checkpoint**: Performance targets met - p95 <500ms backend, Lighthouse performance ≥90 frontend

---

## Phase 7: Documentation & Deployment (STEP 6)

**Purpose**: Documentation, deployment preparation

**Duration**: 4-6 hours

### STEP 6.1: API Documentation

- [ ] T246 Verify FastAPI auto-generates OpenAPI docs at http://localhost:8000/docs
- [ ] T247 Add endpoint descriptions to all routes in backend/src/routes/tasks.py
- [ ] T248 Add request/response examples to POST /api/{user_id}/tasks
- [ ] T249 Add request/response examples to GET /api/{user_id}/tasks
- [ ] T250 Add request/response examples to PUT /api/{user_id}/tasks/{task_id}
- [ ] T251 Test OpenAPI docs in browser, verify all endpoints documented

### STEP 6.2: README Updates

- [ ] T252 Update root README.md with Phase II architecture diagram (use Mermaid or ASCII art)
- [ ] T253 Document environment setup (Neon, Better Auth, Shadcn/ui) in README.md
- [ ] T254 Add local development instructions in README.md (backend + frontend setup)
- [ ] T255 Add deployment instructions (Vercel frontend, Docker backend) in README.md
- [ ] T256 Create backend/README.md with backend-specific setup
- [ ] T257 Create frontend/README.md with frontend-specific setup

### STEP 6.3: Environment Configuration

- [ ] T258 Verify backend/.env.example has all required variables (DATABASE_URL, BETTER_AUTH_SECRET, JWT_SECRET)
- [ ] T259 Verify frontend/.env.example has all required variables (NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET)
- [ ] T260 Create setup guide for new developers in docs/SETUP.md

### STEP 6.4: Deployment Preparation

- [ ] T261 Create docker-compose.yml for local development (backend, frontend, postgres services)
- [ ] T262 Test docker-compose up: `docker-compose up -d`
- [ ] T263 Verify frontend deploys to Vercel: create vercel.json config
- [ ] T264 Create backend/Dockerfile for production deployment
- [ ] T265 Test backend Docker build: `docker build -t todo-backend ./backend`
- [ ] T266 Test backend runs in Docker: `docker run -p 8000:8000 todo-backend`

**Checkpoint**: Documentation complete, deployment ready

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final polish, code quality, integration validation

**Duration**: 4-6 hours

- [ ] T267 [P] Run black formatter on backend: `black backend/src backend/tests`
- [ ] T268 [P] Run mypy strict type checking on backend: `mypy backend/src --strict`
- [ ] T269 [P] Run flake8 linter on backend: `flake8 backend/src backend/tests`
- [ ] T270 [P] Run pydocstyle on backend: `pydocstyle backend/src`
- [ ] T271 [P] Run eslint on frontend: `npm run lint`
- [ ] T272 [P] Run prettier on frontend: `npm run format`
- [ ] T273 [P] Run TypeScript type checking on frontend: `tsc --noEmit`
- [ ] T274 Create backend/CLAUDE.md with backend-specific guidance
- [ ] T275 Create frontend/CLAUDE.md with frontend-specific guidance
- [ ] T276 Update root CLAUDE.md with Phase II completion notes
- [ ] T277 Run full backend test suite with coverage: `pytest backend/tests/ --cov=backend/src --cov-fail-under=80`
- [ ] T278 Run full frontend test suite with coverage: `npm run test -- --coverage`
- [ ] T279 Run full E2E test suite: `npx playwright test`
- [ ] T280 Create acceptance checklist in specs/003-phase-ii-web-app/acceptance-checklist.md (map all 7 success criteria)
- [ ] T281 Verify all 7 Phase II success criteria (SC-201 through SC-207) passing
- [ ] T282 Test full user journey manually: signup → signin → create task → view → edit → complete → delete
- [ ] T283 Commit all Phase II code with comprehensive commit message
- [ ] T284 Create PR with Phase II summary and link to spec

**Checkpoint**: Phase II complete - all quality gates passing, ready for deployment

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup - STEP 0)**: No dependencies - start immediately
- **Phase 2 (Foundational - STEP 1)**: Depends on Phase 1 completion - BLOCKS all frontend work
- **Phase 3 (Frontend - STEP 3)**: Depends on Phase 2 completion (backend must be running)
- **Phase 4 (Testing - STEP 2 + STEP 4)**: Can run in parallel once backend/frontend foundations complete
- **Phase 5 (Performance - STEP 5)**: Depends on Phase 2, 3, 4 completion
- **Phase 6 (Documentation - STEP 6)**: Depends on all previous phases
- **Phase 7 (Polish)**: Depends on all previous phases

### Task Dependencies Within Phases

**Phase 1 (Setup)**:
- STEP 0.1-0.3 can run in any order
- STEP 0.4-0.5 (Research with Context7 MCP) can run in parallel [P]
- STEP 0.6-0.7 depend on research completion

**Phase 2 (Foundational)**:
- Models (T024-T028) can run in parallel [P]
- Migrations (T029-T033) depend on models
- DB session (T034-T038) can run in parallel with models
- FastAPI setup (T039-T044) can run in parallel with migrations
- Better Auth (T045-T056) can start after FastAPI setup
- Task service (T057-T064) depends on models
- Validators (T065-T069) can run in parallel with task service
- Task routes (T070-T080) depend on task service, validators, Better Auth

**Phase 3 (Frontend)**:
- Next.js init (T111-T115) must complete first
- Shadcn setup (T116-T128) depends on Next.js init
- Better Auth client (T129-T133) and API client (T134-T138) can run in parallel [P]
- All page components (T139-T178) depend on Shadcn + API client

**Phase 4 (Testing)**:
- Unit tests (T081-T088) and integration tests (T089-T105) can run in parallel [P]
- Component tests (T179-T194) and E2E tests (T195-T206) can run in parallel [P]

**Phase 5 (Performance)**:
- Backend performance (T223-T235) and frontend performance (T236-T245) can run in parallel [P]

### Parallel Opportunities

**Within Phase 1 (Setup)**:
- All Context7 research tasks (T010-T015) can run concurrently

**Within Phase 2 (Foundational)**:
- Models creation (T024, T025, T026) can run concurrently [P]
- DB session migration (T034-T038) while models are being created [P]

**Within Phase 3 (Frontend)**:
- Shadcn component additions (T117-T126) can be batched
- Auth pages and task pages can be developed in parallel [P]

**Within Phase 4 (Testing)**:
- All unit tests within backend (T083-T086) can run in parallel [P]
- All component tests within frontend (T181-T189) can run in parallel [P]

**Within Phase 8 (Polish)**:
- All linters (T267-T273) can run concurrently [P]

### Critical Path

The critical path for Phase II (tasks that cannot be parallelized):

1. **STEP 0**: Research + Environment Setup (serial, 4-6 hours)
2. **STEP 1**: Backend Foundation (mostly serial due to dependencies, 12-16 hours)
3. **STEP 3**: Frontend Foundation (depends on backend, 12-16 hours)
4. **STEP 2 + STEP 4**: Testing (can overlap, 8-12 hours each, total ~12 hours if parallel)
5. **STEP 5**: Performance (6-8 hours)
6. **STEP 6**: Documentation (4-6 hours)
7. **STEP 8**: Polish (4-6 hours)

**Total Critical Path**: ~50-64 hours (aligns with plan.md estimate of 46.5 hours realistic)

---

## Parallel Example: Phase 2 (Foundational) Task Batching

```bash
# Batch 1: Models (can run in parallel)
Task: "Create backend/src/models/__init__.py"
Task: "Migrate Task model from Phase I to backend/src/models/task.py"
Task: "Create User model in backend/src/models/user.py"

# Batch 2: Database setup (can run in parallel after Batch 1)
Task: "Create Alembic migration for users table"
Task: "Create Alembic migration for tasks table"

# Batch 3: Services (can run in parallel after models)
Task: "Migrate db.py from Phase I to backend/src/services/db.py"
Task: "Migrate TaskService from Phase I to backend/src/services/task_service.py"
Task: "Migrate validators.py from Phase I to backend/src/lib/validators.py"
```

---

## Implementation Strategy

### MVP First (Minimal Viable Product)

**Goal**: Get basic task CRUD working end-to-end

1. Complete Phase 1 (Setup) - **~5 hours**
2. Complete Phase 2 (Foundational) - **~14 hours**
3. Complete Phase 3 (Frontend) - **~14 hours**
4. Skip comprehensive testing initially, do smoke tests only
5. **STOP and VALIDATE**: Manually test signup → signin → create/view/edit/delete tasks
6. **MVP Ready** (~33 hours) - Can demo basic functionality

### Full Implementation (Production Ready)

**Goal**: Meet all 7 Phase II success criteria (SC-201 through SC-207)

1. Complete MVP path (Phase 1-3) - **~33 hours**
2. Complete Phase 4 (Testing) - **~10 hours** (≥80% coverage)
3. Complete Phase 5 (Performance) - **~7 hours** (p95 <500ms, Lighthouse ≥90)
4. Complete Phase 6 (Documentation) - **~5 hours**
5. Complete Phase 8 (Polish) - **~5 hours**
6. **Production Ready** (~60 hours total, aligns with 46.5-52 hour estimate with RI savings)

### Incremental Delivery Checkpoints

**Checkpoint 1**: Setup Complete (T001-T023)
- Environment configured, research done, can start coding

**Checkpoint 2**: Backend Foundation Complete (T024-T080)
- All 6 API endpoints working with JWT auth
- Can test with curl/Postman

**Checkpoint 3**: Frontend Foundation Complete (T111-T178)
- Signup, signin, task CRUD UI fully functional
- Manual testing possible

**Checkpoint 4**: Testing Complete (T081-T222)
- ≥80% backend coverage, ≥80% frontend coverage
- E2E tests passing, Lighthouse ≥90

**Checkpoint 5**: Performance Validated (T223-T245)
- p95 <500ms backend, FCP <1.5s frontend
- Ready for production load

**Checkpoint 6**: Production Ready (T246-T284)
- Documentation complete, deployment tested
- All 7 success criteria verified

---

## Notes

- **[P]** = Parallelizable (different files, no blocking dependencies)
- **[RI]** = Reusable Intelligence from Phase I (8-12 hours savings)
- **[UI]** = Shadcn/ui component (6-10 hours savings vs custom CSS)
- All file paths are absolute from monorepo root
- Commit after each checkpoint or every 5-10 tasks
- Use Context7 MCP for research tasks (STEP 0.4, 0.5)
- Use Playwright MCP for E2E testing (STEP 4.2)
- Use GitHub MCP for final commit/PR (T283-T284)
- Shadcn/ui Slate theme chosen per user preference
- Backend tests use pytest-asyncio for async compatibility
- Frontend uses Vitest + React Testing Library + Playwright
- Total: **284 tasks** covering all 6 implementation steps
- Estimated completion: **46.5-52 hours** (6 days at 8 hours/day)
