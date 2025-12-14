# Skills and Subagents Guide

**Created**: 2025-12-11
**Version**: 1.0.0

This guide documents all Claude Code skills and subagents available for the Todo Evolution project.

## Quick Reference

### Skills Overview

**Total**: 12 skills (7 project-wide + 5 Phase I-specific)

| Skill | Type | Purpose | MCP Integration |
|-------|------|---------|-----------------|
| **phr-creator** | Project-wide | Create Prompt History Records | - |
| **spec-workflow** | Project-wide | Guide spec→plan→tasks workflow | context7 |
| **constitution-check** | Project-wide | Validate constitutional compliance | context7 |
| **adr-detector** | Project-wide | Detect significant architectural decisions | - |
| **git-workflow** | Project-wide | Git commits and PRs | github |
| **code-quality** | Project-wide | Enforce quality standards | context7 |
| **test-coverage** | Project-wide | Ensure 80% coverage | - |
| **phase-i-console** | Phase I | SQLite + Click CLI patterns | context7 |
| **sqlmodel-schemas** | Phase I | Database model patterns | context7 |
| **click-cli** | Phase I | CLI command patterns | context7 |
| **sqlite-testing** | Phase I | Test patterns for SQLite | - |
| **user-isolation** | Phase I | Validate user data isolation | - |

### Subagents Overview

**Total**: 3 specialized agents

| Subagent | Purpose | Skills Used | When to Invoke |
|----------|---------|-------------|----------------|
| **test-guardian** | Comprehensive testing | test-coverage, sqlite-testing, user-isolation, code-quality | "Check test coverage", "Write tests", "Validate test quality" |
| **phase-implementer** | Feature implementation | spec-workflow, phase-i-console, sqlmodel-schemas, click-cli, code-quality, test-coverage, user-isolation | "Implement feature", "Build Phase I app" |
| **security-auditor** | Security audit | user-isolation, constitution-check, code-quality | "Run security audit", "Check for vulnerabilities", "Is it safe to deploy?" |

## How Skills Work

### Automatic Discovery

Skills are **automatically discovered** by me based on:
1. Your request content (e.g., "create a spec" → spec-workflow activates)
2. The skill's `description` field (must be specific!)
3. Current conversation context

**You don't need to manually invoke skills** - I find and use them automatically.

### Example: Automatic Skill Usage

```
You: "Create a specification for the add task feature"
  ↓
Me: [Discovers spec-workflow skill automatically]
  ↓
spec-workflow skill: Provides guidance on spec.md structure
  ↓
Me: Creates spec.md following constitutional requirements
  ↓
Me: [Discovers phr-creator skill automatically]
  ↓
phr-creator skill: Creates PHR after completion
```

## How Subagents Work

### Manual or Model Invocation

Subagents can be invoked:
1. **By you explicitly**: "Use the test-guardian agent to check coverage"
2. **By me automatically**: When I detect the task matches the agent's expertise

### Example: Subagent Usage

```
You: "Implement Phase I console app"
  ↓
Me: [Delegates to phase-implementer agent]
  ↓
phase-implementer: Reads spec.md, plan.md, tasks.md
  ↓
phase-implementer: Implements incrementally with tests
  ↓
phase-implementer: Returns completed implementation
  ↓
Me: Reports to you: "✅ Phase I console app implemented. Coverage: 87%"
```

## MCP Server Integration

### Context7 (Library Documentation)

Used by these skills:
- **spec-workflow**: Fetch API patterns when planning
- **constitution-check**: Verify library usage against docs
- **code-quality**: Check official best practices
- **phase-i-console**: SQLModel, Click documentation
- **sqlmodel-schemas**: ORM patterns
- **click-cli**: CLI framework docs

**Example**:
```
Me: Planning FastAPI authentication
  ↓
spec-workflow skill: Uses context7 to fetch Better Auth docs
  ↓
mcp__context7__get-library-docs("/better-auth/better-auth", topic="jwt")
  ↓
Includes official patterns in plan.md
```

### GitHub (Repository Operations)

Used by:
- **git-workflow**: Commits, PRs, branch management

**Example**:
```
Me: Creating a pull request
  ↓
git-workflow skill: Uses GitHub MCP
  ↓
mcp__github__create_pull_request(...)
  ↓
Returns PR URL
```

### Playwright (E2E Testing - Phase II+)

Used by:
- **test-guardian**: E2E UI tests

**Example**:
```
test-guardian: Writing E2E test
  ↓
mcp__playwright__browser_navigate(url="http://localhost:3000")
  ↓
mcp__playwright__browser_click(element="add button", ref="...")
  ↓
Verifies UI behavior
```

## Project-Wide Skills Details

### 1. phr-creator

**When I use it**: After EVERY user interaction (constitutional requirement)

**What it does**:
- Detects stage (spec, plan, tasks, red, green, etc.)
- Routes to correct directory (constitution/, feature-name/, general/)
- Fills PHR template with complete context
- Validates no placeholders remain

### 2. spec-workflow

**When I use it**: Creating specs, plans, tasks, or implementing features

**What it does**:
- Guides spec → plan → tasks → code workflow
- Validates constitutional compliance
- Suggests ADRs for significant decisions
- Ensures all acceptance scenarios tested

### 3. constitution-check

**When I use it**: Reviewing code, validating implementations

**What it does**:
- Checks all 28 constitutional principles
- Validates user isolation (queries filter by user_id)
- Verifies code quality (type hints, docstrings)
- Ensures 80% test coverage
- Reports violations

### 4. adr-detector

**When I use it**: During planning (plan.md creation)

**What it does**:
- Tests decisions against 3-part significance criteria
- Suggests ADR creation (never auto-creates)
- Groups related decisions
- Waits for your consent before creating ADR

### 5. git-workflow

**When I use it**: Creating commits, branches, PRs

**What it does**:
- Follows conventional commit format
- Creates atomic commits
- Generates PR descriptions
- Integrates with GitHub MCP

### 6. code-quality

**When I use it**: Writing or reviewing code

**What it does**:
- Enforces type hints (mypy --strict)
- Validates docstrings (95% coverage)
- Checks PEP 8 (black, flake8)
- Ensures async I/O for all operations
- Runs automated quality gates

### 7. test-coverage

**When I use it**: Writing tests, reviewing coverage

**What it does**:
- Ensures 80% minimum coverage
- Validates test quality
- Checks required test categories
- Runs coverage reports
- Blocks deployment if coverage < 80%

## Phase I Skills Details

### 8. phase-i-console

**When I use it**: Implementing Phase I console app

**What it does**:
- Provides SQLite + Click patterns
- Shows user isolation patterns
- Demonstrates database setup
- Includes error handling patterns

### 9. sqlmodel-schemas

**When I use it**: Creating/modifying database models

**What it does**:
- Enforces constitutional fields (user_id, timestamps)
- Provides model templates
- Shows field validation patterns
- Includes relationship patterns

### 10. click-cli

**When I use it**: Building CLI commands

**What it does**:
- Shows Click command structure
- Demonstrates error handling
- Provides output formatting patterns
- Includes testing patterns

### 11. sqlite-testing

**When I use it**: Writing tests for Phase I

**What it does**:
- Provides test database fixtures
- Shows factory patterns
- Includes user isolation tests
- Demonstrates CRUD test patterns

### 12. user-isolation

**When I use it**: Reviewing code, validating security

**What it does**:
- Validates ALL queries filter by user_id
- Detects cross-user access violations
- Provides required isolation tests
- Reports violations as CRITICAL

## Subagent Details

### test-guardian

**Invoke with**: "Check test coverage", "Write tests for X", "Review test quality"

**What it does**:
1. Runs coverage reports
2. Identifies untested code
3. Writes missing tests
4. Validates test quality
5. Ensures user isolation tests exist
6. Enforces 80% coverage minimum

**Success criteria**:
- Coverage ≥ 80%
- All required test categories present
- Zero flaky tests
- User isolation verified

### phase-implementer

**Invoke with**: "Implement feature X", "Build Phase I console app"

**What it does**:
1. Reads spec.md, plan.md, tasks.md
2. Implements tasks incrementally
3. Writes tests for each task (TDD)
4. Validates against acceptance criteria
5. Ensures constitutional compliance
6. Reports completion with coverage metrics

**Success criteria**:
- All tasks completed
- All acceptance scenarios validated
- Coverage ≥ 80%
- Zero user isolation violations

### security-auditor

**Invoke with**: "Run security audit", "Is it safe to deploy?", "Check for vulnerabilities"

**What it does**:
1. Audits user isolation (CRITICAL)
2. Scans for hardcoded secrets
3. Validates input validation
4. Checks authentication (Phase II+)
5. Runs dependency vulnerability scans
6. Generates security report

**Success criteria**:
- Zero critical violations
- All secrets in environment variables
- User isolation 100% enforced
- No high/critical CVEs
- All security tests pass

## Best Practices

### For You (User)

1. **Don't manually invoke skills** - I discover them automatically
2. **Explicitly invoke subagents when needed** - "Use test-guardian to check coverage"
3. **Trust the process** - Skills enforce constitutional requirements
4. **Review generated artifacts** - Specs, plans, tasks, PHRs, ADRs

### For Me (Claude)

1. **Always use phr-creator** after EVERY interaction
2. **Use spec-workflow** for all feature work
3. **Use constitution-check** before approving code
4. **Use user-isolation** for ALL security-sensitive code
5. **Delegate to subagents** for specialized tasks

## Phase Evolution

### Current: Phase I

**Active Skills**:
- All 7 project-wide skills
- All 5 Phase I skills

**Active Subagents**:
- test-guardian (testing)
- phase-implementer (implementation)
- security-auditor (security)

### Future: Phase II

**New Skills to Create**:
- phase-ii-web (FastAPI + Next.js patterns)
- fastapi-routes (API endpoint patterns)
- better-auth-integration (JWT authentication)
- nextjs-components (React patterns)
- neon-database (PostgreSQL patterns)

### Future: Phase III

**New Skills to Create**:
- phase-iii-ai (MCP + OpenAI Agents)
- mcp-tool-design (Stateless tool patterns)
- conversation-persistence (DB-backed chat)
- openai-agents (Agent SDK patterns)

### Future: Phase IV

**New Skills to Create**:
- phase-iv-k8s (Kubernetes + Helm)
- docker-patterns (Multi-stage builds)
- helm-charts (K8s deployment)
- health-checks (Liveness/readiness probes)

### Future: Phase V

**New Skills to Create**:
- phase-v-cloud (Kafka + Dapr)
- kafka-events (Event streaming)
- dapr-integration (Distributed runtime)
- cloud-deployment (DOKS/GKE/AKS)

## Troubleshooting

### Skill Not Being Used Automatically

**Problem**: Skill exists but I'm not using it

**Possible causes**:
1. Description is too vague
2. YAML syntax error in SKILL.md
3. File not in `.claude/skills/*/SKILL.md`

**Fix**:
```bash
# Check skill file exists
ls .claude/skills/my-skill/SKILL.md

# Check YAML frontmatter
head -n 10 .claude/skills/my-skill/SKILL.md

# Make description more specific
description: "Exact use case with keywords that match common requests"
```

### Subagent Not Available

**Problem**: Can't invoke subagent

**Fix**:
```bash
# Check agent file exists
ls .claude/agents/my-agent.md

# Verify frontmatter has name
grep "^name:" .claude/agents/my-agent.md
```

## Summary

**✅ Setup Complete**:
- 12 skills created (7 project-wide + 5 Phase I)
- 3 subagents created (test-guardian, phase-implementer, security-auditor)
- MCP integration (context7, github, playwright)
- Constitutional compliance enforced
- Ready for Phase I implementation

**Next Steps**:
1. Start implementing Phase I features
2. Skills will activate automatically
3. Invoke subagents as needed
4. Expand skills for Phase II when ready

---

**Constitutional Authority**: This setup enforces all 28 constitutional principles through automated skills and specialized agents. Zero tolerance for violations.
