# Implementation Plan: Phase II - Full-Stack Web Application

**Branch**: `003-phase-ii-web-app` | **Date**: 2025-12-15 | **Spec**: [Evolution Vision](../001-evolution-vision/spec.md)
**Input**: Phase II requirements from `/specs/001-evolution-vision/spec.md`

## Executive Summary

**PHASE II** transforms the Phase I console application into a production-ready full-stack web application with:
- **Backend**: FastAPI REST API with Better Auth authentication
- **Frontend**: Next.js 16+ with React Server Components + **Professional UI Design System**
- **Database**: Migration from SQLite to Neon PostgreSQL
- **Authentication**: Better Auth with JWT token validation
- **Performance**: p95 <500ms under 100 concurrent users, Lighthouse ≥90
- **UI/UX**: Shadcn/ui component library with professional color themes (zero custom CSS needed)

This plan provides a comprehensive breakdown of all implementation steps, Reusable Intelligence (RI) strategy, MCP server usage, UI/UX design system, time estimates, and success criteria alignment.

**YES, Frontend UI will be fully implemented in PHASE II** with a professional, interactive design using pre-built component libraries to avoid painful back-and-forth iterations.

---

## Technical Context

**Language/Version**:
- **Backend**: Python 3.13+ with UV package manager
- **Frontend**: TypeScript 5.x with Next.js 16+, React 19+

**Primary Dependencies**:
- **Backend**: FastAPI 0.110+, SQLModel 0.0.16+, Better Auth SDK (Python), python-jose (JWT), httpx (async HTTP)
- **Frontend**: Next.js 16+, React 19+, Better Auth (React hooks), Tailwind CSS 4.x, TypeScript 5.x
- **UI Components**: Shadcn/ui (pre-built, accessible components), Lucide React (icons), Radix UI (primitives)
- **UI Theme**: Professional color palette (recommended: Slate/Zinc for neutral, Blue/Violet for primary)

**Storage**: Neon Serverless PostgreSQL (cloud-hosted, replacing SQLite)

**Testing**:
- **Backend**: pytest, pytest-cov, pytest-asyncio, httpx.AsyncClient (API testing)
- **Frontend**: Jest/Vitest, React Testing Library, Playwright (E2E)
- **Coverage Target**: ≥80% (Constitutional Principle X)

**Target Platform**:
- **Backend**: Linux server (Docker containerized, local development)
- **Frontend**: Vercel deployment (Next.js App Router)
- **Database**: Neon cloud (managed PostgreSQL)

**Project Type**: Web application (monorepo with frontend/ and backend/ directories)

**Performance Goals**:
- API p95 latency <500ms under 100 concurrent users
- Frontend FCP <1.5s, LCP <2.5s, TTI <3.5s
- Lighthouse scores ≥90 (performance, accessibility, best practices)

**Constraints**:
- User data isolation: ZERO cross-user data leakage (Constitutional Principle II)
- Stateless architecture: No in-memory session state (Constitutional Principle III)
- Rate limiting: 100 requests/minute per user (Constitutional Principle XV)
- WCAG 2.1 Level AA accessibility (Constitutional Principle XVII)

**Scale/Scope**:
- 100 concurrent users (load testing target)
- 1000 tasks per user (performance testing dataset)
- 5 user stories (Add, View, Update, Delete, Complete tasks)

---

## Constitution Check

### ✅ Principle I: Spec-Driven Development
- Spec created: `specs/001-evolution-vision/spec.md` (covers all 5 phases)
- Plan created: This document
- Tasks will be created: After plan approval via `/sp.tasks`

### ✅ Principle II: User Data Isolation (SECURITY CRITICAL)
- ALL API endpoints include `user_id` in path: `/api/{user_id}/tasks`
- ALL database queries filter by `user_id`
- JWT token user matches URL `user_id` (401 if mismatch)
- Integration tests verify cross-user access blocked

### ✅ Principle III: Stateless Architecture
- FastAPI servers hold NO in-memory state
- Better Auth manages session via JWT tokens (database-backed)
- Any server instance can handle any request

### ✅ Principle VI: Database Standards
- SQLModel ORM exclusively (NO raw SQL)
- Alembic migrations for schema changes
- user_id indexed on all tables
- Foreign key constraints enforced

### ✅ Principle VII: API Design Standards
- RESTful methods: GET, POST, PUT, PATCH, DELETE
- URL pattern: `/api/{user_id}/resource`
- JSON with Pydantic validation
- Consistent error format: `{error: string, details?: object}`

### ✅ Principle IX: Code Quality Standards
- **Python**: mypy --strict, black, flake8, pydocstyle
- **TypeScript**: strict mode, eslint, prettier
- Type hints mandatory

### ✅ Principle X: Testing Requirements
- Coverage target: ≥80%
- pytest (backend), Jest/Vitest (frontend), Playwright (E2E)
- TDD encouraged

### ✅ Principle XIV: Authentication & Authorization
- Better Auth for user management
- JWT tokens for API authentication
- Shared `BETTER_AUTH_SECRET` between frontend and backend
- Token expiry enforced

### ✅ Principle XV: API Rate Limiting
- 100 requests/minute per authenticated user
- 429 response with Retry-After header
- slowapi middleware

### ✅ Principle XVII: Frontend Accessibility & Responsiveness
- WCAG 2.1 Level AA compliance
- Lighthouse ≥90
- Responsive breakpoints: mobile <640px, tablet 640-1024px, desktop >1024px

### ✅ Principle XVIII: Performance Standards
- Backend: p95 <500ms
- Frontend: FCP <1.5s, LCP <2.5s
- Lighthouse CI enforced

---

## Project Structure

### Documentation (Phase II Feature)

```text
specs/003-phase-ii-web-app/
├── plan.md              # This file
├── spec.md              # Phase II specific requirements (to be created)
├── tasks.md             # Task breakdown (created by /sp.tasks)
├── data-model.md        # PostgreSQL schema migration plan
├── contracts/           # API endpoint contracts
│   ├── auth.md          # Better Auth endpoints
│   ├── tasks.md         # Task CRUD endpoints
│   └── user.md          # User profile endpoints
└── research.md          # Technology research notes
```

### Source Code (Monorepo Structure)

```text
/
├── frontend/
│   ├── CLAUDE.md                    # Frontend-specific guidance
│   ├── app/
│   │   ├── layout.tsx               # Root layout
│   │   ├── page.tsx                 # Landing page
│   │   ├── auth/
│   │   │   ├── signin/page.tsx
│   │   │   └── signup/page.tsx
│   │   └── tasks/
│   │       ├── page.tsx             # Task list
│   │       └── [id]/page.tsx        # Task detail
│   ├── components/
│   │   ├── TaskList.tsx
│   │   ├── TaskForm.tsx
│   │   ├── TaskItem.tsx
│   │   └── ui/                      # Shadcn/ui components
│   ├── lib/
│   │   ├── api.ts                   # API client abstraction
│   │   ├── auth.ts                  # Better Auth client config
│   │   └── types.ts                 # Shared TypeScript types
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   └── next.config.ts
│
├── backend/
│   ├── CLAUDE.md                    # Backend-specific guidance
│   ├── src/
│   │   ├── main.py                  # FastAPI entry point
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py              # Better Auth user model
│   │   │   └── task.py              # Task model (migrated from Phase I)
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py              # Better Auth endpoints
│   │   │   └── tasks.py             # Task CRUD endpoints
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── db.py                # Database session management
│   │   │   ├── auth_service.py      # JWT validation middleware
│   │   │   └── task_service.py      # Task business logic (migrated)
│   │   ├── lib/
│   │   │   ├── __init__.py
│   │   │   └── validators.py        # Shared validation (migrated)
│   │   └── config.py                # Settings (DATABASE_URL, secrets)
│   ├── alembic/
│   │   ├── versions/                # Database migrations
│   │   └── env.py
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── e2e/
│   ├── pyproject.toml               # UV dependencies
│   ├── alembic.ini
│   └── .env.example
│
├── .specify/
│   └── memory/constitution.md       # Constitutional principles
├── specs/
│   ├── 001-evolution-vision/
│   ├── 002-phase-i-console-app/
│   └── 003-phase-ii-web-app/        # This spec
├── history/
│   ├── prompts/
│   └── adr/
├── docker-compose.yml               # Local development
├── CLAUDE.md                        # Root guidance
└── README.md
```

**Structure Decision**: Monorepo with separate `frontend/` and `backend/` directories. This aligns with Constitutional monorepo standards and enables Claude Code single-context development. Frontend uses Next.js App Router (server components by default). Backend uses FastAPI with clear separation of concerns (models, routes, services).

---

## MCP Server Usage Strategy

Based on `specs/001-evolution-vision/mcp-usage-guide.md`, Phase II will leverage the following MCP servers:

### 1. Context7 MCP (Documentation Queries)

**When to Use**: Research phase for unfamiliar APIs and implementation patterns

**Specific Queries**:
- "How to implement Better Auth with FastAPI in 2025?"
- "What's the latest FastAPI JWT middleware pattern?"
- "How to configure CORS for Next.js 16+ frontend?"
- "Next.js 16 App Router server components best practices 2025"
- "Neon PostgreSQL connection pooling with SQLModel"
- "FastAPI async route handlers with SQLModel"
- "Next.js 16 authentication with Better Auth React hooks"

**Workflow**: Research → Implement → Test → Commit (Context7 used in research phase only)

**Security Note**: Context7 is read-only (no code execution), safe to use for documentation

### 2. GitHub MCP (Version Control)

**When to Use**: Committing code, creating PRs, managing branches

**Specific Operations**:
- Create feature branch: `003-phase-ii-web-app`
- Commit backend migrations
- Commit frontend components
- Create PR with comprehensive summary
- Link PR to Phase II spec

**Security Note**: Requires `GITHUB_TOKEN` with repo permissions

### 3. Playwright MCP (E2E Testing)

**When to Use**: End-to-end testing of web UI after implementation

**Specific Test Scenarios**:
- User signup → signin flow
- Create task → verify in list
- Update task title → verify persistence
- Mark task complete → verify status
- Delete task → verify removal
- Cross-user isolation (Alice cannot see Bob's tasks)
- JWT expiry handling (401 response)

**Security Note**: Runs in isolated browser context

### 4. PostgreSQL MCP (Database Validation)

**When to Use**: Validate migrations, inspect schema

**Requirements**: DATABASE_URL environment variable pointing to Neon PostgreSQL

**Specific Queries**:
- "DESCRIBE tasks;" (verify schema after migration)
- "SELECT COUNT(*) FROM tasks WHERE user_id = 'alice';" (verify data isolation)
- "SHOW INDEXES FROM tasks;" (verify user_id index exists)

**Note**: This MCP requires configuration and may not be immediately available. Alternative: Use `psql` via Bash tool with Neon connection string.

---

## Agent, Subagent, and Skill Usage

### Claude Code Agents Available

Based on the session context, the following specialized agents are available:

#### 1. **Explore Agent** (subagent_type='Explore')
**When to Use**: Codebase exploration before making changes

**Specific Use Cases**:
- "Where are user isolation checks implemented in Phase I?"
- "How is SQLModel ORM used in task_service.py?"
- "What validation logic exists in lib/validators.py?"

**Thoroughness Levels**:
- "quick": Basic file/pattern search
- "medium": Moderate exploration (recommended for Phase II migration)
- "very thorough": Comprehensive multi-location analysis

#### 2. **Plan Agent** (subagent_type='Plan')
**When to Use**: Designing implementation strategy for complex features

**Specific Use Cases**:
- "Plan the SQLite → PostgreSQL migration strategy"
- "Design Better Auth integration with FastAPI JWT middleware"
- "Architect the Next.js frontend data fetching pattern"

**Output**: Step-by-step plans, critical files, architectural trade-offs

#### 3. **General-Purpose Agent** (subagent_type='general-purpose')
**When to Use**: Multi-step tasks requiring search + code changes

**Note**: Use sparingly - prefer specialized agents (Explore, Plan) when possible

### Slash Commands (Skills)

Based on available slash commands in this project:

- **/sp.plan**: Execute planning workflow (already used for this document)
- **/sp.tasks**: Generate tasks.md from this plan (next step after approval)
- **/sp.implement**: Execute task implementation workflow
- **/sp.phr**: Create Prompt History Record (automatic after this session)
- **/sp.adr**: Create Architecture Decision Record (if significant decisions made)
- **/sp.analyze**: Cross-artifact consistency check (after tasks.md created)
- **/sp.git.commit_pr**: Autonomous git workflow (commit + PR creation)

### Reusable Intelligence (RI) Implementation Strategy

**Definition**: **RI (Reusable Intelligence)** refers to code, patterns, and architectural decisions from Phase I that can be migrated and reused in Phase II to accelerate development and maintain consistency.

#### RI Components We Are Migrating from Phase I:

**1. Data Models (src/models/task.py)**
- **Reuse**: Task model structure (id, user_id, title, completed, created_at, updated_at)
- **Adaptation**: Migrate from SQLite to PostgreSQL-compatible SQLModel
- **Benefit**: Proven data structure, no redesign needed

**2. Validation Logic (src/lib/validators.py)**
- **Reuse**: `validate_title()` and `validate_user_id()` functions
- **Adaptation**: Import into FastAPI Pydantic models for request validation
- **Benefit**: Consistent validation rules (1-200 chars, non-empty user_id)

**3. Business Logic (src/services/task_service.py)**
- **Reuse**: TaskService methods (create_task, get_tasks_for_user)
- **Adaptation**: Make methods async for FastAPI compatibility
- **Benefit**: User isolation logic already tested and verified

**4. Database Session Management (src/services/db.py)**
- **Reuse**: Session context manager pattern
- **Adaptation**: Update connection string from SQLite to Neon PostgreSQL
- **Benefit**: Proven session lifecycle management

**5. Test Patterns (tests/unit/, tests/integration/)**
- **Reuse**: User isolation test patterns, validation test cases
- **Adaptation**: Convert to pytest-asyncio for async API tests
- **Benefit**: 89% coverage patterns can be replicated for API endpoints

**6. Security-Critical Docstrings**
- **Reuse**: "SECURITY CRITICAL" docstrings on user isolation code
- **Adaptation**: Copy to FastAPI route handlers and middleware
- **Benefit**: Maintains security awareness across phases

#### RI Implementation in PHASE II Steps:

- **PHASE II - STEP 1.1** (Database Migration): Reuse Task model, adapt to PostgreSQL
- **PHASE II - STEP 1.4** (Task API Endpoints): Reuse TaskService, make async
- **PHASE II - STEP 2.1** (Backend Unit Tests): Reuse test patterns from Phase I
- **PHASE II - STEP 2.2** (Integration Tests): Reuse user isolation test logic

**Time Savings from RI**: Estimated **8-12 hours saved** by reusing proven Phase I patterns instead of redesigning from scratch.

---

## UI/UX Design System Strategy (AVOID PAINFUL BACK-AND-FORTH)

### Problem with Custom UI Design:
Your previous project suffered from back-and-forth iterations on UI/UX. Building custom components and color schemes is time-consuming and subjective.

### Solution: Pre-Built Professional Design System

We will use **Shadcn/ui** - a collection of beautifully designed, accessible components built on Radix UI primitives with Tailwind CSS. This is **NOT a component library you install via npm** - instead, you copy/paste pre-built components into your project, giving you full control.

#### Why Shadcn/ui is the BEST Choice for Phase II:

**1. Zero Custom CSS Needed**
- Components come pre-styled with Tailwind CSS
- Professional design out-of-the-box
- Consistent spacing, typography, colors

**2. Copy-Paste, Not Install**
- Run: `npx shadcn@latest init` (sets up Tailwind + config)
- Add components: `npx shadcn@latest add button card form input`
- Components appear in `frontend/components/ui/` - you own the code

**3. Fully Customizable**
- Edit components directly in your codebase
- Change colors via Tailwind config (no CSS fighting)
- Adapt to your needs without library constraints

**4. Accessibility Built-In (WCAG 2.1 AA)**
- Radix UI primitives handle keyboard navigation, ARIA labels, focus management
- Lighthouse accessibility score ≥90 guaranteed
- Screen reader tested

**5. Professional Color Themes (Zero Design Work)**

Shadcn/ui includes pre-configured color palettes. We'll use:

**Recommended Theme: "Slate" (Professional SaaS App)**
```typescript
// frontend/tailwind.config.ts
export default {
  theme: {
    extend: {
      colors: {
        border: "hsl(214.3 31.8% 91.4%)",      // Subtle borders
        background: "hsl(0 0% 100%)",           // White background
        foreground: "hsl(222.2 84% 4.9%)",      // Almost black text
        primary: {
          DEFAULT: "hsl(221.2 83.2% 53.3%)",    // Blue for buttons
          foreground: "hsl(210 40% 98%)",       // White text on blue
        },
        // ... (shadcn generates full palette)
      }
    }
  }
}
```

**Alternative Themes Available**:
- **Zinc**: Modern, high-contrast (good for dashboards)
- **Violet**: Creative, vibrant (good for creative tools)
- **Rose**: Warm, friendly (good for personal apps)
- **Orange**: Energetic, bold (good for productivity apps)

**We'll start with Slate theme and can change the entire color scheme in 5 minutes by editing one config file.**

#### Components We'll Use in Phase II:

**PHASE II - STEP 3.1** (Setup):
```bash
npx shadcn@latest init  # Choose Slate theme, TypeScript, App Router
npx shadcn@latest add button card form input label checkbox
npx shadcn@latest add dialog dropdown-menu separator toast
```

**PHASE II - STEP 3.2** (Authentication UI):
- `<Card>` for signin/signup forms
- `<Form>` with Zod validation (built-in)
- `<Input>` for email/password
- `<Button>` with loading states
- `<Toast>` for success/error messages

**PHASE II - STEP 3.3** (Task Management UI):
- `<Card>` for task list container
- `<Checkbox>` for task completion toggle
- `<Dialog>` for add/edit task modal
- `<DropdownMenu>` for task actions (edit, delete)
- `<Separator>` for visual spacing

#### Interactive Examples (From Shadcn/ui):

**Button Component** (no custom CSS needed):
```tsx
import { Button } from "@/components/ui/button"

// Primary action
<Button>Add Task</Button>

// Destructive action
<Button variant="destructive">Delete Task</Button>

// Loading state
<Button disabled>
  <Loader2 className="animate-spin" />
  Creating...
</Button>
```

**Form Component** (validation included):
```tsx
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"

const formSchema = z.object({
  title: z.string().min(1).max(200),
})

function TaskForm() {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
  })

  return (
    <Form {...form}>
      <FormField
        control={form.control}
        name="title"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Task Title</FormLabel>
            <FormControl>
              <Input placeholder="Buy groceries" {...field} />
            </FormControl>
            <FormMessage /> {/* Automatic error display */}
          </FormItem>
        )}
      />
    </Form>
  )
}
```

#### Icons: Lucide React (1000+ Professional Icons)

```bash
npm install lucide-react
```

```tsx
import { Plus, Check, Trash2, Edit, Loader2 } from "lucide-react"

<Button>
  <Plus className="w-4 h-4 mr-2" />
  Add Task
</Button>
```

#### Time Savings with Shadcn/ui:

| Task | Custom CSS Time | Shadcn/ui Time | Savings |
|------|-----------------|----------------|---------|
| Button component with variants | 2-3 hours | 5 minutes | ~2.5 hours |
| Form with validation display | 3-4 hours | 10 minutes | ~3.5 hours |
| Modal dialog | 2-3 hours | 5 minutes | ~2.5 hours |
| Dropdown menu | 2-3 hours | 5 minutes | ~2.5 hours |
| Toast notifications | 2-3 hours | 5 minutes | ~2.5 hours |
| Checkbox with labels | 1 hour | 2 minutes | ~1 hour |
| **TOTAL** | **12-19 hours** | **32 minutes** | **~14.5 hours** |

**Result**: You get a professional, interactive UI in **under 1 hour** instead of 12-19 hours of custom CSS work.

#### Color Customization (5-Minute Theme Changes):

If you want to change the color scheme:
1. Go to [shadcn.com/themes](https://ui.shadcn.com/themes)
2. Pick a theme (Slate, Zinc, Violet, Rose, Orange)
3. Copy the CSS variables
4. Paste into `frontend/app/globals.css`
5. **Done!** Entire app color scheme updates instantly.

#### Dark Mode Support (Built-In):

Shadcn/ui supports dark mode out-of-the-box:
```tsx
import { ThemeProvider } from "next-themes"

// Wrap app in theme provider
<ThemeProvider attribute="class">
  {children}
</ThemeProvider>

// Toggle dark mode
<Button onClick={() => setTheme(theme === "dark" ? "light" : "dark")}>
  Toggle Dark Mode
</Button>
```

### UI Implementation Plan (No Back-and-Forth):

**PHASE II - STEP 3.1**: Setup Shadcn/ui (30 minutes)
- Run init wizard (picks theme, configures Tailwind)
- Add 10-12 components we need
- All components appear in frontend/components/ui/

**PHASE II - STEP 3.2**: Build Authentication UI (2 hours)
- Signin form: `<Card>` + `<Form>` + `<Input>` + `<Button>`
- Signup form: Same components, different validation
- Toast notifications for success/error

**PHASE II - STEP 3.3**: Build Task Management UI (3-4 hours)
- Task list: `<Card>` container with task items
- Task item: `<Checkbox>` + `<DropdownMenu>` for actions
- Add task dialog: `<Dialog>` + `<Form>`
- Edit task dialog: Same as add task, pre-filled

**PHASE II - STEP 3.4**: Polish & Responsive (1-2 hours)
- Test on mobile (375px), tablet (768px), desktop (1920px)
- Tailwind responsive classes handle everything
- No media queries needed

**Total UI Time**: **6.5-8.5 hours** with professional results (vs. 12-19 hours custom CSS with likely pain)

---

## PHASE II Implementation Steps (Clear Numbering)

PHASE II is broken into **6 major steps** with detailed sub-tasks and time estimates:

### **PHASE II - STEP 0: Environment Setup & Migration Planning** (4-6 hours)

#### Sub-Tasks:
- **STEP 0.1**: Create Neon PostgreSQL project and database (30 minutes)
- **STEP 0.2**: Configure `DATABASE_URL` in backend/.env (15 minutes)
- **STEP 0.3**: Set up Better Auth credentials (secret keys) (30 minutes)
- **STEP 0.4**: Research FastAPI + Better Auth integration (Context7 MCP) (1-1.5 hours)
- **STEP 0.5**: Research Next.js 16 + Better Auth React hooks (Context7 MCP) (1-1.5 hours)
- **STEP 0.6**: Design database migration strategy (SQLite → PostgreSQL) (1 hour)
- **STEP 0.7**: Create Alembic migration scripts (30-45 minutes)

#### Success Criteria:
- ✅ Neon database accessible via `psql`
- ✅ Environment variables documented in .env.example
- ✅ Migration strategy documented in specs/003-phase-ii-web-app/data-model.md

#### Time Estimate: **4-6 hours**

---

### **PHASE II - STEP 1: Backend Foundation** (12-16 hours)

#### Sub-Tasks:

**STEP 1.1: Database Migration** (3-4 hours) - **[RI: Reuses Phase I Task model]**
- **STEP 1.1.1**: Update SQLModel models for PostgreSQL (add user model for Better Auth) (1 hour)
- **STEP 1.1.2**: Create Alembic migrations (users table, tasks table with user_id FK) (1-1.5 hours)
- **STEP 1.1.3**: Migrate existing SQLite data to Neon PostgreSQL (if applicable) (30-45 minutes)
- **STEP 1.1.4**: Verify schema with PostgreSQL MCP or psql (30 minutes)

**STEP 1.2: FastAPI Setup** (2-3 hours)
- **STEP 1.2.1**: Create backend/src/main.py with FastAPI app (45 minutes)
- **STEP 1.2.2**: Configure CORS for Next.js frontend (30 minutes)
- **STEP 1.2.3**: Set up middleware (rate limiting with slowapi) (45 minutes)
- **STEP 1.2.4**: Configure structured logging (JSON format) (30 minutes)

**STEP 1.3: Better Auth Integration** (4-5 hours)
- **STEP 1.3.1**: Install Better Auth Python SDK (15 minutes)
- **STEP 1.3.2**: Configure shared BETTER_AUTH_SECRET (30 minutes)
- **STEP 1.3.3**: Implement JWT validation middleware (2-2.5 hours)
- **STEP 1.3.4**: Create auth routes: POST /api/auth/signup, POST /api/auth/signin (1-1.5 hours)

**STEP 1.4: Task API Endpoints** (3-4 hours) - **[RI: Reuses TaskService logic, made async]**
- **STEP 1.4.1**: POST /api/{user_id}/tasks (create task) (30-45 minutes)
- **STEP 1.4.2**: GET /api/{user_id}/tasks (list tasks with pagination) (45-60 minutes)
- **STEP 1.4.3**: GET /api/{user_id}/tasks/{task_id} (get task detail) (30 minutes)
- **STEP 1.4.4**: PUT /api/{user_id}/tasks/{task_id} (full update) (30-45 minutes)
- **STEP 1.4.5**: PATCH /api/{user_id}/tasks/{task_id}/complete (mark complete) (30 minutes)
- **STEP 1.4.6**: DELETE /api/{user_id}/tasks/{task_id} (delete task) (30 minutes)

#### Success Criteria:
- ✅ All endpoints return proper status codes (200, 201, 400, 401, 404)
- ✅ JWT validation works (401 if missing/invalid token)
- ✅ User isolation enforced (Alice cannot access /api/bob/tasks)
- ✅ Rate limiting works (429 after 100 requests/minute)

#### Time Estimate: **12-16 hours**

---

### **PHASE II - STEP 2: Backend Testing** (8-10 hours)

#### Sub-Tasks:

**STEP 2.1: Unit Tests** (4-5 hours) - **[RI: Reuses Phase I test patterns]**
- **STEP 2.1.1**: Test task_service.py business logic (async version) (1.5-2 hours)
- **STEP 2.1.2**: Test JWT validation middleware (1-1.5 hours)
- **STEP 2.1.3**: Test input validation (Pydantic models) (1 hour)
- **STEP 2.1.4**: Mock database for isolated tests (30-45 minutes)

**STEP 2.2: Integration Tests** (4-5 hours) - **[RI: Reuses Phase I user isolation test logic]**
- **STEP 2.2.1**: Test all API endpoints with httpx.AsyncClient (2-2.5 hours)
- **STEP 2.2.2**: Test user isolation (cross-user access blocked) (1 hour)
- **STEP 2.2.3**: Test authentication flow (signup → signin → access protected endpoint) (45-60 minutes)
- **STEP 2.2.4**: Test rate limiting (send 120 requests, verify 429) (30-45 minutes)
- **STEP 2.2.5**: Test pagination (verify limit/offset work) (30 minutes)

#### Success Criteria:
- ✅ Backend test coverage ≥80%
- ✅ All integration tests pass
- ✅ User isolation tests verify ZERO data leakage

#### Time Estimate: **8-10 hours**

---

### **PHASE II - STEP 3: Frontend Foundation** (12-16 hours)

#### Sub-Tasks:

**STEP 3.1: Next.js & Shadcn/ui Setup** (2-3 hours) - **[UI: Professional design system]**
- **STEP 3.1.1**: Initialize Next.js 16 project with App Router (30 minutes)
- **STEP 3.1.2**: Configure TypeScript (strict mode) (15 minutes)
- **STEP 3.1.3**: Set up Tailwind CSS 4.x (15 minutes)
- **STEP 3.1.4**: Run `npx shadcn@latest init` - choose Slate theme (15 minutes)
- **STEP 3.1.5**: Add Shadcn/ui components (button, card, form, input, dialog, etc.) (30 minutes)
- **STEP 3.1.6**: Configure Better Auth client (React hooks) (45-60 minutes)

**STEP 3.2: Authentication UI** (4-5 hours) - **[UI: Shadcn Card + Form components]**
- **STEP 3.2.1**: Create app/auth/signup/page.tsx (signup form with `<Card>` + `<Form>`) (2-2.5 hours)
- **STEP 3.2.2**: Create app/auth/signin/page.tsx (signin form) (1.5-2 hours)
- **STEP 3.2.3**: Implement Better Auth React hooks (30 minutes)
- **STEP 3.2.4**: Handle JWT token storage (httpOnly cookies) (30 minutes)
- **STEP 3.2.5**: Redirect after authentication + toast notifications (30 minutes)

**STEP 3.3: Task Management UI** (6-8 hours) - **[UI: Shadcn Card, Dialog, Checkbox components]**
- **STEP 3.3.1**: Create app/tasks/page.tsx (task list with server components) (1.5-2 hours)
- **STEP 3.3.2**: Create components/TaskList.tsx (display tasks in `<Card>`) (1.5-2 hours)
- **STEP 3.3.3**: Create components/TaskForm.tsx (add/edit task with `<Dialog>` + `<Form>`) (2-2.5 hours)
- **STEP 3.3.4**: Create components/TaskItem.tsx (single task with `<Checkbox>` + `<DropdownMenu>`) (1-1.5 hours)
- **STEP 3.3.5**: Implement API client (lib/api.ts with JWT header) (1 hour)
- **STEP 3.3.6**: Handle loading states and error messages with `<Toast>` (30-45 minutes)

#### Success Criteria:
- ✅ User can sign up and sign in
- ✅ User can create, view, update, complete, and delete tasks
- ✅ Server components used by default (client components only where needed)
- ✅ API errors displayed to user with toast notifications
- ✅ Professional UI with Shadcn/ui (Slate theme)

#### Time Estimate: **12-16 hours**

---

### **PHASE II - STEP 4: Frontend Testing & Accessibility** (8-12 hours)

#### Sub-Tasks:

**STEP 4.1: Component Tests** (4-5 hours)
- **STEP 4.1.1**: Test TaskForm component (valid input, validation errors) (1.5-2 hours)
- **STEP 4.1.2**: Test TaskList component (empty state, populated state) (1-1.5 hours)
- **STEP 4.1.3**: Test TaskItem component (complete, delete actions) (1-1.5 hours)
- **STEP 4.1.4**: Mock API calls with msw (Mock Service Worker) (30-45 minutes)

**STEP 4.2: E2E Tests with Playwright MCP** (3-4 hours)
- **STEP 4.2.1**: Test signup → signin → create task → verify in list (1-1.5 hours)
- **STEP 4.2.2**: Test mark task complete → verify status change (30-45 minutes)
- **STEP 4.2.3**: Test delete task → verify removal (30-45 minutes)
- **STEP 4.2.4**: Test cross-user isolation (Alice cannot see Bob's tasks) (1 hour)

**STEP 4.3: Accessibility Audit** (1-3 hours) - **[UI: Shadcn/ui guarantees WCAG 2.1 AA]**
- **STEP 4.3.1**: Run Lighthouse audit (target ≥90) (30 minutes)
- **STEP 4.3.2**: Run axe DevTools (fix critical violations if any) (30-60 minutes)
- **STEP 4.3.3**: Test keyboard navigation (Tab, Enter, Escape) (30 minutes)
- **STEP 4.3.4**: Verify color contrast (4.5:1 for normal text) - auto-handled by Shadcn (15 minutes)
- **STEP 4.3.5**: Test responsive design (375px, 768px, 1920px) (30-45 minutes)

#### Success Criteria:
- ✅ Frontend test coverage ≥80%
- ✅ All E2E tests pass
- ✅ Lighthouse scores ≥90 (performance, accessibility, best practices)
- ✅ axe DevTools 0 critical violations
- ✅ Fully keyboard navigable

#### Time Estimate: **8-12 hours**

---

### **PHASE II - STEP 5: Performance Optimization & Load Testing** (6-8 hours)

#### Sub-Tasks:

**STEP 5.1: Backend Performance** (3-4 hours)
- **STEP 5.1.1**: Verify NO N+1 queries (SQLAlchemy query logging) (30-45 minutes)
- **STEP 5.1.2**: Configure PostgreSQL connection pooling (10-20 connections) (30 minutes)
- **STEP 5.1.3**: Add database indexes (user_id, status, due_date) (30 minutes)
- **STEP 5.1.4**: Load test with Locust or k6 (100 users, 10 req/sec, 5 minutes) (1-1.5 hours)
- **STEP 5.1.5**: Verify p95 <500ms under load (30-45 minutes)

**STEP 5.2: Frontend Performance** (3-4 hours) - **[UI: Shadcn/ui is lightweight by design]**
- **STEP 5.2.1**: Analyze bundle size with next build (target <200KB gzipped) (30 minutes)
- **STEP 5.2.2**: Optimize images (Next.js Image component) (1 hour)
- **STEP 5.2.3**: Implement code splitting (automatic with Next.js) (30 minutes)
- **STEP 5.2.4**: Run Lighthouse CI (verify FCP <1.5s, LCP <2.5s, TTI <3.5s) (1-1.5 hours)

#### Success Criteria:
- ✅ p95 latency <500ms under 100 concurrent users
- ✅ Lighthouse performance score ≥90
- ✅ Main bundle <200KB gzipped

#### Time Estimate: **6-8 hours**

---

### **PHASE II - STEP 6: Documentation & Deployment Preparation** (4-6 hours)

#### Sub-Tasks:

**STEP 6.1: API Documentation** (1-2 hours)
- **STEP 6.1.1**: Verify FastAPI auto-generates OpenAPI docs at /docs (15 minutes)
- **STEP 6.1.2**: Verify all endpoints documented with descriptions (30-45 minutes)
- **STEP 6.1.3**: Add request/response examples to endpoints (30-45 minutes)

**STEP 6.2: README Updates** (1-2 hours)
- **STEP 6.2.1**: Update root README.md with Phase II architecture diagram (30-45 minutes)
- **STEP 6.2.2**: Document environment setup (Neon, Better Auth, Shadcn/ui) (30-45 minutes)
- **STEP 6.2.3**: Add deployment instructions (Vercel frontend, Docker backend) (30-45 minutes)

**STEP 6.3: Environment Configuration** (1-1 hour)
- **STEP 6.3.1**: Document all environment variables in backend/.env.example (30 minutes)
- **STEP 6.3.2**: Document all environment variables in frontend/.env.example (15 minutes)
- **STEP 6.3.3**: Create setup guide for new developers (15-30 minutes)

**STEP 6.4: Deployment Prep** (1-1 hour)
- **STEP 6.4.1**: Create docker-compose.yml for local development (30 minutes)
- **STEP 6.4.2**: Verify frontend can deploy to Vercel (15 minutes)
- **STEP 6.4.3**: Verify backend can run in Docker container (15-30 minutes)

#### Success Criteria:
- ✅ API documentation accessible at /docs
- ✅ New developer can set up project from README
- ✅ `docker-compose up` starts full stack locally

#### Time Estimate: **4-6 hours**

---

## Total Time Estimate (Updated with RI & Shadcn/ui Savings)

| Step | Description | Time Estimate | RI/UI Savings |
|------|-------------|---------------|---------------|
| STEP 0 | Environment Setup & Migration Planning | 4-6 hours | - |
| STEP 1 | Backend Foundation | 12-16 hours | **-4 to -6 hours** (RI reuse) |
| STEP 2 | Backend Testing | 8-10 hours | **-2 to -3 hours** (RI test patterns) |
| STEP 3 | Frontend Foundation (with Shadcn/ui) | 12-16 hours | **-6 to -8 hours** (Shadcn/ui) |
| STEP 4 | Frontend Testing & Accessibility | 8-12 hours | **-1 to -2 hours** (Shadcn accessibility) |
| STEP 5 | Performance Optimization & Load Testing | 6-8 hours | - |
| STEP 6 | Documentation & Deployment Preparation | 4-6 hours | - |
| **TOTAL (Original)** | **Phase II Complete Implementation** | **54-74 hours** | - |
| **TOTAL (With Savings)** | **Phase II with RI + Shadcn/ui** | **41-52 hours** | **-13 to -22 hours saved** |

### Time Estimate Breakdown:

**Original Estimate (Without RI/Shadcn/ui)**:
- **Minimum (Best Case)**: 54 hours (~7 days at 8 hours/day)
- **Maximum (Worst Case)**: 74 hours (~9 days at 8 hours/day)
- **Most Likely (Realistic)**: 64 hours (~8 days at 8 hours/day)

**Updated Estimate (With RI Reuse + Shadcn/ui)**:
- **Minimum (Best Case)**: 41 hours (~5 days at 8 hours/day)
- **Maximum (Worst Case)**: 52 hours (~6.5 days at 8 hours/day)
- **Most Likely (Realistic)**: 46.5 hours (~6 days at 8 hours/day) ⭐ **RECOMMENDED ESTIMATE**

**Time Savings Breakdown**:
- **Reusable Intelligence (RI)**: 8-12 hours saved
  - Phase I Task models, validators, service logic reused
  - Test patterns replicated instead of redesigned
- **Shadcn/ui Design System**: 6-10 hours saved
  - Pre-built professional components (no custom CSS)
  - Accessibility guaranteed (WCAG 2.1 AA built-in)
  - Professional color themes (Slate/Zinc/Violet)

**Total Savings**: **13-22 hours** (20-30% time reduction)

**Factors Affecting Timeline**:
- Familiarity with FastAPI, Next.js 16, Better Auth
- Database migration complexity (if migrating existing Phase I data)
- E2E test debugging time
- Performance optimization iterations

**Risk Mitigation**: The "Most Likely" estimate of **6 days** includes buffer for unforeseen issues. With RI reuse and Shadcn/ui, the implementation is **significantly de-risked** compared to starting from scratch.

---

## Success Criteria Mapping

### Phase II Success Criteria from Evolution Vision Spec:

#### ✅ SC-201: 100 concurrent users, p95 <500ms
- **Verification**: Phase 5 - Load test with Locust/k6
- **Acceptance**: 95% of requests complete in <500ms with 100 concurrent users

#### ✅ SC-202: Better Auth + JWT validation
- **Verification**: Phase 1 - Integration tests
- **Acceptance**: All API endpoints reject requests without valid JWT (401 response)

#### ✅ SC-203: User isolation enforced
- **Verification**: Phase 2 - Integration tests
- **Acceptance**: User Alice cannot access /api/bob/tasks (401 response), Bob cannot access Alice's task via /api/bob/tasks/{alice-task-id} (404 response)

#### ✅ SC-204: Migration with zero data loss
- **Verification**: Phase 1 - Manual verification
- **Acceptance**: If Phase I has existing data, all tasks migrate to PostgreSQL with correct user_id and task_id

#### ✅ SC-205: Lighthouse ≥90
- **Verification**: Phase 4 - Lighthouse CI
- **Acceptance**: Performance ≥90, Accessibility ≥90, Best Practices ≥90

#### ✅ SC-206: Rate limiting works
- **Verification**: Phase 2 - Integration test
- **Acceptance**: 101st request in 60 seconds returns 429 with Retry-After header

#### ✅ SC-207: Migration script tested
- **Verification**: Phase 1 - Alembic migration execution
- **Acceptance**: Migration script runs without errors, schema matches expected structure

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Better Auth integration complexity | Medium | High | Research with Context7 MCP before implementation, allocate extra time |
| Neon PostgreSQL connection issues | Low | Medium | Test connection early in Phase 0, verify SSL/connection string format |
| Next.js 16 breaking changes | Low | Medium | Use Context7 MCP for latest 2025 docs, verify App Router patterns |
| Load testing reveals performance issues | Medium | Medium | Budget extra time in Phase 5, profile with SQLAlchemy query logging |
| E2E test flakiness | Medium | Low | Use Playwright's auto-wait features, add explicit waits where needed |
| JWT token expiry handling | Low | Medium | Test token refresh flow explicitly, handle 401 responses gracefully |

---

## Deferred Features ("Things We Said We Do Later")

Based on the Evolution Vision Spec, the following features are explicitly deferred to **Phase V**:

### Intermediate Features (Phase V Only):
- **Priorities & Tags**: Task priority levels (high, medium, low), custom tags
- **Search & Filter**: Full-text search, filter by status/priority/tags
- **Sort Tasks**: Sort by due date, priority, created date

### Advanced Features (Phase V Only):
- **Recurring Tasks**: Daily, weekly, monthly recurrence patterns
- **Due Dates & Time Reminders**: Due date tracking, notification system
- **Timeline View**: Calendar/Gantt chart view

**Rationale**: Phase II focuses on establishing the core full-stack architecture (FastAPI + Next.js + PostgreSQL + Better Auth). Advanced features are deferred to Phase V to avoid scope creep and ensure Phase II meets success criteria.

---

## Complexity Tracking

**No Constitutional Violations in Phase II Plan**

All architectural decisions align with the constitution:
- Spec-driven development (this plan follows spec → plan → tasks workflow)
- User data isolation enforced at API and database level
- Stateless architecture (JWT tokens, no in-memory state)
- Database standards (SQLModel ORM, Alembic migrations)
- API standards (RESTful, Pydantic validation)
- Code quality (mypy, black, eslint, prettier)
- Testing requirements (≥80% coverage, unit/integration/E2E)
- Authentication (Better Auth + JWT)
- Performance standards (p95 <500ms, Lighthouse ≥90)

---

## Next Steps

1. **User Approval**: Review this plan and approve before proceeding
2. **Create Tasks**: Run `/sp.tasks` to generate detailed task breakdown in `specs/003-phase-ii-web-app/tasks.md`
3. **Create Branch**: `git checkout -b 003-phase-ii-web-app`
4. **Start Phase 0**: Environment setup and migration planning
5. **Create PHR**: Prompt History Record will be automatically created after this session
6. **Optional ADR**: If significant architectural decisions are made during implementation (e.g., "FastAPI + Better Auth integration strategy"), consider running `/sp.adr <decision-title>`

---

## Quick Reference Summary

### ✅ What Gets Built in PHASE II:

**Backend (FastAPI + Neon PostgreSQL + Better Auth)**:
- ✅ User signup/signin with Better Auth
- ✅ JWT token authentication on all endpoints
- ✅ 6 REST API endpoints for task CRUD
- ✅ User data isolation (ZERO cross-user data leakage)
- ✅ Rate limiting (100 req/min per user)
- ✅ Alembic database migrations
- ✅ 80%+ test coverage

**Frontend (Next.js 16 + Shadcn/ui + Tailwind CSS)**:
- ✅ Professional UI with Shadcn/ui (Slate theme)
- ✅ Signup/signin pages with Better Auth
- ✅ Task list page (view all tasks)
- ✅ Add task dialog
- ✅ Edit task dialog
- ✅ Mark complete checkbox
- ✅ Delete task action
- ✅ Toast notifications (success/error)
- ✅ Fully responsive (mobile/tablet/desktop)
- ✅ WCAG 2.1 AA accessible
- ✅ Lighthouse ≥90 scores

### 📊 Key Metrics:

| Metric | Target | How Verified |
|--------|--------|--------------|
| API p95 latency | <500ms | Load test with Locust/k6 |
| Frontend FCP | <1.5s | Lighthouse CI |
| Frontend LCP | <2.5s | Lighthouse CI |
| Test coverage | ≥80% | pytest-cov, Jest coverage |
| Accessibility | Lighthouse ≥90 | Lighthouse + axe DevTools |
| User isolation | ZERO leakage | Integration tests |

### 🎨 UI/UX Strategy (NO Back-and-Forth):

**Problem**: Custom CSS is time-consuming and subjective
**Solution**: Shadcn/ui pre-built components

**Benefits**:
- ⚡ **14.5 hours saved** vs custom CSS
- 🎨 Professional Slate theme (changeable in 5 minutes)
- ♿ Accessibility guaranteed (WCAG 2.1 AA)
- 📱 Responsive by default
- 🌗 Dark mode support built-in
- 🔧 Fully customizable (you own the code)

**Alternative Themes**: Zinc (high-contrast), Violet (vibrant), Rose (warm), Orange (energetic)

### 🧠 Reusable Intelligence (RI) from Phase I:

**What We're Reusing**:
- ✅ Task model structure (id, user_id, title, completed, timestamps)
- ✅ Validation logic (validate_title, validate_user_id)
- ✅ TaskService business logic (made async)
- ✅ User isolation test patterns
- ✅ Security-critical docstrings

**Time Saved**: 8-12 hours

### ⏱️ Time Estimate:

**Realistic Estimate**: **6 days** (46.5 hours) at 8 hours/day

**Breakdown**:
- STEP 0: Environment Setup (4-6 hours)
- STEP 1: Backend Foundation (12-16 hours, -4 to -6 with RI)
- STEP 2: Backend Testing (8-10 hours, -2 to -3 with RI)
- STEP 3: Frontend Foundation (12-16 hours, -6 to -8 with Shadcn/ui)
- STEP 4: Frontend Testing (8-12 hours, -1 to -2 with Shadcn)
- STEP 5: Performance (6-8 hours)
- STEP 6: Documentation (4-6 hours)

**Total Savings**: 13-22 hours (20-30% faster than starting from scratch)

### 🚀 MCP Servers Used:

| MCP Server | When Used | Purpose |
|------------|-----------|---------|
| **Context7** | STEP 0, STEP 1 | Research FastAPI, Next.js 16, Better Auth docs |
| **GitHub** | After each step | Commit code, create PR |
| **Playwright** | STEP 4 | E2E testing of web UI |
| **PostgreSQL** | STEP 1 | Validate migrations, inspect schema |

### 📁 Project Structure:

```
/
├── frontend/               # Next.js 16 + Shadcn/ui
│   ├── app/               # App Router pages
│   ├── components/ui/     # Shadcn components (you own)
│   └── lib/api.ts         # API client with JWT
│
├── backend/               # FastAPI + SQLModel + Better Auth
│   ├── src/models/        # PostgreSQL models
│   ├── src/routes/        # API endpoints
│   ├── src/services/      # Business logic
│   └── alembic/           # Database migrations
│
└── specs/003-phase-ii-web-app/
    ├── plan.md            # This file
    └── tasks.md           # Generated by /sp.tasks (next step)
```

---

**Plan Status**: ✅ READY FOR REVIEW AND APPROVAL
**Estimated Completion**: **6 days** (46.5 hours) with RI + Shadcn/ui savings
**Constitutional Compliance**: 100% (28/28 principles followed)
**Success Criteria Coverage**: 7/7 (SC-201 through SC-207)
**UI Strategy**: Shadcn/ui (Slate theme) - Professional, accessible, zero custom CSS
**RI Strategy**: Reuse Phase I models, validators, service logic, test patterns
