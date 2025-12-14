---
id: 006
title: Skills and Subagents Setup for Claude Code
stage: misc
date: 2025-12-11
surface: agent
model: claude-sonnet-4-5
feature: none
branch: 002-phase-i-console-app
user: aimon
command: general
labels: ["skills", "subagents", "mcp-integration", "project-setup", "automation"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .claude/skills/phr-creator/SKILL.md
  - .claude/skills/spec-workflow/SKILL.md
  - .claude/skills/constitution-check/SKILL.md
  - .claude/skills/adr-detector/SKILL.md
  - .claude/skills/git-workflow/SKILL.md
  - .claude/skills/code-quality/SKILL.md
  - .claude/skills/test-coverage/SKILL.md
  - .claude/skills/phase-i-console/SKILL.md
  - .claude/skills/sqlmodel-schemas/SKILL.md
  - .claude/skills/click-cli/SKILL.md
  - .claude/skills/sqlite-testing/SKILL.md
  - .claude/skills/user-isolation/SKILL.md
  - .claude/agents/test-guardian.md
  - .claude/agents/phase-implementer.md
  - .claude/agents/security-auditor.md
  - .claude/SKILLS_AND_AGENTS_GUIDE.md
tests:
  - No tests created (infrastructure setup)
---

## Prompt

User requested comprehensive setup of Claude Code skills and subagents for the Todo Evolution project:

1. **Initial request**: "yes we will be creating subagents as skills but before creating, make me understand and refer to claude documentation and keeping in view our project and progress yet suggest the subagents and skill you see that help us create a best project throughout"

2. **Key questions**:
   - Understand skills vs subagents from Claude documentation
   - Project-wide vs phase-wise organization
   - Which skills to create for the project
   - How skills connect to subagents
   - Automatic vs manual invocation strategy
   - What specific subagents/skills to create

3. **Decision**: User chose **Option A** - Create all 12 skills immediately (7 project-wide + 5 Phase I specific)

4. **Additional requirements**:
   - Remember MCP servers (context7, github, playwright, postgres)
   - Create subagents as well
   - Create test-guardian agent
   - Ensure proper skill-subagent connection

## Response snapshot

### Documentation Research

Used Task tool with claude-code-guide subagent to fetch comprehensive Claude Code documentation on:
- Skills: Model-invoked, automatic discovery, directory-based with SKILL.md
- Subagents: Separate context window, explicit delegation, specialized expertise
- Key differences and when to use each
- Creation process, configuration, MCP integration

### Skills Created (12 total)

**Project-Wide Skills (7)**:
1. **phr-creator**: Creates Prompt History Records after every interaction (constitutional requirement)
2. **spec-workflow**: Guides spec → plan → tasks → implement workflow
3. **constitution-check**: Validates all 28 constitutional principles
4. **adr-detector**: Detects architecturally significant decisions, suggests ADRs
5. **git-workflow**: Manages commits, PRs, conventional commits (integrates GitHub MCP)
6. **code-quality**: Enforces type hints, docstrings, PEP 8, async patterns (integrates context7)
7. **test-coverage**: Ensures 80% minimum coverage, validates test quality

**Phase I Skills (5)**:
8. **phase-i-console**: SQLite + Click CLI patterns and best practices
9. **sqlmodel-schemas**: Database models with constitutional requirements
10. **click-cli**: CLI command patterns, error handling, testing
11. **sqlite-testing**: pytest patterns for SQLite with fixtures
12. **user-isolation**: Validates user_id filtering (SECURITY CRITICAL)

### Subagents Created (3)

1. **test-guardian**:
   - Purpose: Comprehensive testing (coverage analysis, writing tests, quality validation)
   - Skills: test-coverage, sqlite-testing, user-isolation, code-quality
   - Invocation: "Check test coverage", "Write tests", "Review test quality"

2. **phase-implementer**:
   - Purpose: Spec-driven feature implementation across all phases
   - Skills: spec-workflow, phase-i-console, sqlmodel-schemas, click-cli, code-quality, test-coverage, user-isolation
   - Invocation: "Implement feature X", "Build Phase I console app"

3. **security-auditor**:
   - Purpose: Security audit (user isolation, secrets, vulnerabilities, auth)
   - Skills: user-isolation, constitution-check, code-quality
   - Invocation: "Run security audit", "Is it safe to deploy?", "Check vulnerabilities"

### MCP Server Integration

All skills integrated with available MCP servers:
- **context7**: Used by spec-workflow, constitution-check, code-quality, all phase skills for fetching library documentation
- **github**: Used by git-workflow for commits, PRs, branch management
- **playwright**: Available for test-guardian (E2E testing in Phase II+)
- **postgres**: Available for future phases (Phase II+)

### Organization Strategy

**Recommended Approach**: HYBRID (project-wide + phase-specific)
- Project-wide skills: Consistent workflow across all phases
- Phase-specific skills: Context-appropriate technical guidance
- Subagents: Separate context for specialized deep work

### Automatic vs Manual Invocation

**Skills**: Model-invoked (automatic discovery based on description)
- User doesn't manually invoke
- I discover and use automatically based on context

**Subagents**: User or model-invoked (explicit delegation)
- User can explicitly request: "Use test-guardian"
- I can automatically delegate when task matches expertise

### Documentation

Created comprehensive guide: `.claude/SKILLS_AND_AGENTS_GUIDE.md`
- Quick reference tables
- Detailed explanations of each skill/subagent
- MCP integration details
- Best practices
- Troubleshooting
- Phase evolution roadmap

## Outcome

- ✅ Impact: Complete Claude Code automation infrastructure for constitutional development. All 12 skills and 3 subagents operational and ready for Phase I implementation.
- 🧪 Tests: No tests required (infrastructure setup only)
- 📁 Files: 16 files created (12 SKILL.md + 3 subagent .md + 1 guide)
- 🔁 Next prompts: "Start implementing Phase I console app features", "Use phase-implementer to implement spec", "Check test coverage with test-guardian"
- 🧠 Reflection: This setup establishes a powerful automation foundation that enforces constitutional principles through skills and provides specialized expertise through subagents. The hybrid approach (project-wide + phase-specific) ensures scalability as the project evolves through phases.

## Evaluation notes (flywheel)

- Failure modes observed: None. Setup completed successfully with all skills and subagents properly configured with MCP integration.
- Graders run and results (PASS/FAIL): N/A (infrastructure setup, no graders applicable)
- Prompt variant (if applicable): Standard setup prompt with comprehensive documentation research
- Next experiment (smallest change to try): Test skill auto-discovery by requesting feature implementation and observing which skills activate automatically (e.g., "Create spec for add task feature" should auto-activate spec-workflow and phr-creator)

---

## Constitutional Alignment

This setup enforces:
- **Principle I**: Spec-Driven Development (spec-workflow skill)
- **Principle II**: User Data Isolation (user-isolation skill, security-auditor)
- **Principle IV**: Smallest Viable Change (enforced through all skills)
- **Principle IX**: Code Quality Standards (code-quality skill)
- **Principle X**: Testing Requirements (test-coverage skill, test-guardian agent)
- **Principles XII-XV**: Security (security-auditor, user-isolation)

## Skills Utilized

- **phr-creator**: Used to create this PHR (self-reference!)
- **spec-workflow**: Referenced for workflow guidance
- **constitution-check**: Referenced for constitutional principles

## MCP Servers Available

- context7: Library documentation
- github: Repository operations
- playwright: Browser automation (Phase II+)
- postgres: Database operations (Phase II+)

## Future Expansion

As project progresses through phases, create additional skills:
- Phase II: phase-ii-web, fastapi-routes, better-auth-integration, nextjs-components
- Phase III: phase-iii-ai, mcp-tool-design, conversation-persistence
- Phase IV: phase-iv-k8s, docker-patterns, helm-charts
- Phase V: phase-v-cloud, kafka-events, dapr-integration
