# AGENTS.md

## Purpose

This project uses **Spec-Driven Development (SDD)** — a workflow where **no agent is allowed to write code until the specification is complete and approved**.

All AI agents (Claude, Copilot, Gemini, local LLMs, etc.) must follow the **Spec-Kit lifecycle**:

> **Specify → Plan → Tasks → Implement**

This prevents "vibe coding," ensures alignment across agents, and guarantees that every implementation step maps back to an explicit requirement.

---

## How Agents Must Work

Every agent in this project MUST obey these rules:

1. **Never generate code without a referenced Task ID.**
2. **Never modify architecture without updating the plan file (`specs/<feature>/plan.md`).**
3. **Never propose features without updating the specification (`specs/<feature>/spec.md`).**
4. **Never change approach without updating the constitution (`.specify/memory/constitution.md`).**
5. **Every code file must contain a comment linking it to the Task and Spec sections.**

If an agent cannot find the required spec, it must **stop and request it**, not improvise.

---

## Spec-Kit Workflow (Source of Truth)

### 1. Constitution (WHY — Principles & Constraints)

**File**: `.specify/memory/constitution.md`

Defines the project's non-negotiables:
- Architecture values
- Security rules
- Tech stack constraints
- Performance expectations
- Patterns allowed

Agents must check this before proposing solutions.

---

### 2. Specify (WHAT — Requirements, Journeys & Acceptance Criteria)

**File**: `specs/<feature>/spec.md`

Contains:
- User journeys
- Requirements
- Acceptance criteria
- Domain rules
- Business constraints

Agents must not infer missing requirements — they must request clarification or propose specification updates.

---

### 3. Plan (HOW — Architecture, Components, Interfaces)

**File**: `specs/<feature>/plan.md`

Includes:
- Component breakdown
- APIs & schema diagrams
- Service boundaries
- System responsibilities
- High-level sequencing

All architectural output MUST be generated from the Specify file.

---

### 4. Tasks (BREAKDOWN — Atomic, Testable Work Units)

**File**: `specs/<feature>/tasks.md`

Each Task must contain:
- Task ID (e.g., T001, T042)
- Clear description
- Preconditions
- Expected outputs
- Artifacts to modify
- Links back to Specify + Plan sections

Agents **implement only what these tasks define**.

---

### 5. Implement (CODE — Write Only What the Tasks Authorize)

Agents now write code, but must:
- Reference Task IDs in commits and comments
- Follow the Plan exactly
- Not invent new features or flows
- Stop and request clarification if anything is underspecified

> **The golden rule: No task = No code.**

---

## Agent Behavior in This Project

### When generating code:

Agents must reference:
```
[Task]: T-001
[From]: specs/feature-name/spec.md §2.1, specs/feature-name/plan.md §3.4
```

### When proposing architecture:

Agents must reference:
```
Update required in specs/feature-name/plan.md → add component X
```

### When proposing new behavior or a new feature:

Agents must reference:
```
Requires update in specs/feature-name/spec.md (WHAT)
```

### When changing principles:

Agents must reference:
```
Modify .specify/memory/constitution.md → Principle #X
```

---

## Agent Failure Modes (What Agents MUST Avoid)

Agents are NOT allowed to:
- Freestyle code or architecture
- Generate missing requirements
- Create tasks on their own
- Alter stack choices without justification
- Add endpoints, fields, or flows that aren't in the spec
- Ignore acceptance criteria
- Produce "creative" implementations that violate the plan

If a conflict arises between spec files, the **Constitution > Specify > Plan > Tasks** hierarchy applies.

---

## Developer–Agent Alignment

Humans and agents collaborate, but the **spec is the single source of truth**.

Before every session, agents should re-read:
1. `.specify/memory/constitution.md` (principles)
2. `specs/<current-feature>/spec.md` (requirements)
3. `specs/<current-feature>/plan.md` (architecture)
4. `specs/<current-feature>/tasks.md` (current work items)

This ensures predictable, deterministic development.

---

## Project-Specific Commands

This project uses **SpecKit Plus** commands accessible as skills in Claude Code:

### Specification Phase
- `/sp.specify` - Create or update feature specification from natural language
- `/sp.clarify` - Identify underspecified areas and ask targeted questions

### Planning Phase
- `/sp.plan` - Generate architectural plan from spec
- `/sp.adr` - Create Architecture Decision Record for significant decisions

### Task Breakdown Phase
- `/sp.tasks` - Generate actionable task list from plan
- `/sp.analyze` - Analyze consistency across spec/plan/tasks
- `/sp.checklist` - Generate custom checklist for current feature

### Implementation Phase
- `/sp.implement` - Execute tasks from tasks.md with TDD workflow

### Documentation Phase
- `/sp.phr` - Create Prompt History Record for traceability
- `/sp.constitution` - Create/update project constitution

### Git Workflow
- `/sp.git.commit_pr` - Intelligent git commit and PR creation

---

## Current Project Structure

```
.
├── .specify/
│   ├── memory/
│   │   └── constitution.md          # 28 principles (Principle I-XXVIII)
│   ├── templates/                   # Spec/plan/task templates
│   └── scripts/                     # Helper scripts
├── specs/
│   ├── 001-add-task/               # Phase I: Console App
│   ├── 002-phase-i-console-app/    # Phase I: Complete Console
│   ├── 003-phase-ii-web-app/       # Phase II: Web App
│   └── 004-phase-iii-ai-chatbot/   # Phase III: AI Chatbot (CURRENT)
│       ├── spec.md
│       ├── plan.md
│       ├── tasks.md
│       ├── data-model.md
│       └── contracts/              # MCP tool contracts
├── history/
│   ├── prompts/                    # Prompt History Records (PHRs)
│   └── adr/                        # Architecture Decision Records
├── backend/                        # FastAPI + Python 3.13
│   ├── src/
│   │   ├── models/                # SQLModel ORM models
│   │   ├── services/              # Business logic layer
│   │   ├── routes/                # FastAPI endpoints
│   │   └── mcp/                   # MCP tools for agent
│   └── tests/                     # pytest tests (80%+ coverage)
├── frontend/                       # Next.js 16 + React 19
│   ├── app/                       # Next.js app router
│   ├── components/                # React components
│   └── lib/                       # Utilities
├── AGENTS.md                       # This file (agent behavior guide)
├── CLAUDE.md                       # Claude Code configuration
└── PROGRESS.md                     # Current implementation status
```

---

## Current Development Phase: Phase III - Agentic AI Chatbot

**Branch**: `004-phase-iii-ai-chatbot`
**Progress**: 18/95 tasks complete (19%)

**Completed**:
- ✅ Phase 1: Setup (T001-T004)
- ✅ Phase 2: Database Foundation (T005-T009)
- ✅ Phase 2: Service Layer (T010-T011)
- ✅ Phase 2: MCP Tools (T012-T018)

**Next**: Agent Service Foundation (T019-T024)

**Active Spec Files**:
- `specs/004-phase-iii-ai-chatbot/spec.md` - Requirements & user stories
- `specs/004-phase-iii-ai-chatbot/plan.md` - Architecture & decisions
- `specs/004-phase-iii-ai-chatbot/tasks.md` - Task breakdown (95 tasks)
- `specs/004-phase-iii-ai-chatbot/data-model.md` - Database schemas
- `specs/004-phase-iii-ai-chatbot/contracts/*.json` - MCP tool contracts

---

## Key Technologies (Per Constitution)

**Backend**:
- Python 3.13+ (Principle III)
- FastAPI 0.115.0+ (async web framework)
- SQLModel 0.0.14+ (ORM with Pydantic validation)
- Neon PostgreSQL (managed database)
- OpenAI SDK 2.14.0+ (agent integration)
- UV 0.9.17+ (package manager - NEVER use pip)

**Frontend**:
- Next.js 16 (React 19)
- TypeScript 5.x
- Better Auth (authentication)
- @openai/chatkit-react 1.4.0 (chat UI)

**Agent Tools**:
- MCP (Model Context Protocol) for tool integration
- OpenAI Agents SDK (not raw API)

---

## Agent-Specific Reminders

1. **Always read PROGRESS.md** to understand current state
2. **UV, not pip**: Use `uv pip install`, never `pip install`
3. **Constitutional Principles**: 28 principles in `.specify/memory/constitution.md`
4. **User Data Isolation**: All queries must filter by `user_id` (Principle II)
5. **Testing**: Maintain 80%+ coverage (Principle X)
6. **PHR Creation**: Required after every user interaction (see CLAUDE.md)
7. **ADR Suggestions**: Suggest (don't auto-create) for significant decisions

---

## Summary

**Spec-Kit enforces discipline**. Agents work within constraints, not around them.

- No improvisation.
- No guessing.
- No "creative" implementations.
- Every line of code maps to a task.
- Every task maps to a plan.
- Every plan maps to a spec.
- Every spec aligns with the constitution.

**If in doubt, ask. Never assume.**
