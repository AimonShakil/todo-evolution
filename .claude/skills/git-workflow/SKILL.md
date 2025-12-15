---
name: git-workflow
description: Execute Git workflows including commits and pull requests following constitutional standards. Use when creating commits, managing branches, creating PRs, or any Git operations. Integrates with GitHub MCP server.
allowed-tools: Bash
---

# Git Workflow Automation Skill

Manages Git operations following Constitutional Principle XXVIII (Git & Version Control).

## Constitutional Requirements

### Commit Message Format
```
<type>: <description>

[Optional body]

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Types**: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

### Commit Standards
- **Atomic Commits**: One logical change per commit
- **Conventional Format**: Type prefix required
- **Attribution**: Co-authored-by footer

### Required .gitignore Entries
- `.env` (secrets)
- `node_modules` (Node.js dependencies)
- `__pycache__` (Python cache)
- `.venv` (Python virtual environment)
- `dist` (build output)
- `*.db` (SQLite databases - Phase I only)

## Git Workflow Patterns

### Pattern 1: Create Commit

**When to use**: After completing implementation, tests pass, ready to commit changes

**Process**:

1. **Check Status**:
```bash
git status
```

2. **Review Changes**:
```bash
git diff
git diff --staged
```

3. **Stage Files**:
```bash
git add <files>
# or
git add .
```

4. **Create Commit** (using heredoc for proper formatting):
```bash
git commit -m "$(cat <<'EOF'
feat: add user task creation endpoint

Implements POST /api/{user_id}/tasks with Pydantic validation
and user isolation enforcement.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

5. **Verify Commit**:
```bash
git log -1 --format='[%h] %s'
```

### Pattern 2: Create Pull Request

**When to use**: After committing changes, ready to merge to main

**Process**:

1. **Ensure on feature branch**:
```bash
git branch --show-current
```

2. **Review all commits since divergence from main**:
```bash
git log main..HEAD --oneline
git diff main...HEAD
```

3. **Push to remote** (if not already pushed):
```bash
git push -u origin <branch-name>
```

4. **Create PR using GitHub MCP** (preferred):
```bash
# Use MCP tool instead of gh cli
# mcp__github__create_pull_request with:
# - owner: repo owner
# - repo: repo name
# - title: PR title
# - body: PR description (summary + test plan)
# - head: current branch
# - base: main (or target branch)
```

**Alternative: Use gh CLI**:
```bash
gh pr create --title "feat: Phase I console app implementation" --body "$(cat <<'EOF'
## Summary
- Implemented basic task CRUD operations
- Added user isolation via CLI arguments
- SQLite persistence with SQLModel ORM

## Test Plan
- [x] Unit tests pass (pytest)
- [x] Coverage ≥ 80%
- [x] User isolation tests pass
- [ ] Manual testing: add/view/complete/delete tasks

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

5. **Return PR URL** to user

### Pattern 3: Create Branch

**When to use**: Starting new feature work

**Process**:

1. **Ensure on main and up to date**:
```bash
git checkout main
git pull
```

2. **Create feature branch**:
```bash
git checkout -b <feature-branch-name>
```

**Branch naming convention**:
- `<number>-<feature-name>` (e.g., `002-phase-i-console-app`)
- Use hyphens, lowercase
- Include feature number if applicable

3. **Verify branch created**:
```bash
git branch --show-current
```

### Pattern 4: Amend Commit (Pre-commit Hook Changes)

**When to use**: Pre-commit hook modified files after commit

**Safety Checks** (MUST pass before amending):
1. Verify HEAD commit is yours:
```bash
git log -1 --format='[%h] (%an <%ae>) %s'
```

2. Verify not pushed:
```bash
git status | grep "Your branch is ahead"
```

3. If both checks pass:
```bash
git add <hook-modified-files>
git commit --amend --no-edit
```

**NEVER amend if**:
- Commit author is not Claude/current user
- Commit already pushed to remote
- Branch is not ahead of remote

## MCP Server Integration (GitHub)

### Available GitHub MCP Tools

When working with Git workflows, prefer MCP tools over shell commands:

1. **Create Pull Request**:
```
mcp__github__create_pull_request:
  owner: <repo-owner>
  repo: <repo-name>
  title: "feat: Phase I implementation"
  body: "## Summary\n...\n## Test Plan\n..."
  head: <feature-branch>
  base: main
```

2. **Create Branch** (via MCP):
```
mcp__github__create_branch:
  owner: <repo-owner>
  repo: <repo-name>
  branch: "003-new-feature"
  from_branch: main  # optional
```

3. **Push Files** (multiple files in one commit):
```
mcp__github__push_files:
  owner: <repo-owner>
  repo: <repo-name>
  branch: <feature-branch>
  files:
    - path: "backend/main.py"
      content: "..."
    - path: "backend/models.py"
      content: "..."
  message: "feat: add task endpoints"
```

4. **List Commits**:
```
mcp__github__list_commits:
  owner: <repo-owner>
  repo: <repo-name>
  sha: <branch-name>  # optional
```

5. **Get File Contents**:
```
mcp__github__get_file_contents:
  owner: <repo-owner>
  repo: <repo-name>
  path: "backend/main.py"
  branch: <branch-name>  # optional
```

### When to Use MCP vs Git CLI

| Operation | Prefer | Reason |
|-----------|--------|--------|
| Local commit | Git CLI | Direct git operations |
| Create PR | **GitHub MCP** | Structured API, better error handling |
| Push files | **GitHub MCP** | Atomic multi-file commits |
| Create branch | Either | Both work well |
| Review commits | Git CLI | Local, faster |
| Check file contents | **GitHub MCP** | Remote files without clone |

## Commit Type Guidelines

### `feat`: New Feature
```bash
git commit -m "$(cat <<'EOF'
feat: add task deletion endpoint

Implements DELETE /api/{user_id}/tasks/{task_id} with
user isolation enforcement.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

### `fix`: Bug Fix
```bash
git commit -m "$(cat <<'EOF'
fix: enforce user isolation in task queries

Added user_id filter to prevent cross-user data access.
Fixes security vulnerability.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

### `docs`: Documentation
```bash
git commit -m "$(cat <<'EOF'
docs: add API documentation to README

Documented all endpoints with examples and responses.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

### `refactor`: Code Refactoring
```bash
git commit -m "$(cat <<'EOF'
refactor: extract task validation logic

Moved validation to separate function for reusability.
No behavior changes.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

### `test`: Add Tests
```bash
git commit -m "$(cat <<'EOF'
test: add user isolation integration tests

Validates cross-user access is blocked for all endpoints.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

### `chore`: Maintenance
```bash
git commit -m "$(cat <<'EOF'
chore: update dependencies to latest versions

Updated FastAPI, SQLModel, pytest to resolve security CVEs.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

## Pull Request Template

```markdown
## Summary
- [Bullet points of what changed]
- [Why these changes were made]
- [Link to spec.md if applicable]

## Test Plan
- [x] Unit tests pass
- [x] Integration tests pass
- [x] Coverage ≥ 80%
- [ ] Manual testing completed: [describe steps]

## Constitutional Compliance
- [x] Spec-driven: spec.md → plan.md → tasks.md exists
- [x] User isolation: All queries filter by user_id
- [x] Code quality: Type hints, docstrings, PEP 8
- [x] Testing: 80%+ coverage
- [x] Security: No secrets in code

## ADRs Created
- [Link to ADR if significant architectural decisions made]
- [Or "No ADRs needed for this change"]

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

## Git Safety Protocol

Per Constitution (CLAUDE.md):

### MUST NEVER
- ❌ Update git config
- ❌ Force push to main/master
- ❌ Run destructive commands (hard reset) without user consent
- ❌ Skip hooks (--no-verify) without user request
- ❌ Amend commits by other developers

### MUST ALWAYS
- ✅ Check authorship before amending
- ✅ Verify commit not pushed before amending
- ✅ Use heredoc for multi-line commit messages
- ✅ Include attribution footer
- ✅ Follow conventional commit format

### Before Force Operations
```bash
# If user requests force push, confirm:
echo "⚠️ WARNING: Force push requested to main/master"
echo "This is destructive. Are you sure? (Ctrl+C to cancel)"
read -p "Type 'yes' to continue: " confirmation
```

## .gitignore Validation

Before first commit, verify .gitignore includes:

```bash
# Check .gitignore
cat .gitignore | grep -E "^\.env$|^node_modules$|^__pycache__$|^\.venv$|^dist$"
```

If missing, add:
```
.env
node_modules
__pycache__
.venv
dist
*.db
.DS_Store
*.pyc
.pytest_cache
.mypy_cache
```

## Common Git Workflows

### New Feature Workflow
```bash
# 1. Create branch
git checkout -b 002-new-feature

# 2. Make changes, run tests
pytest --cov

# 3. Stage and commit
git add .
git commit -m "$(cat <<'EOF'
feat: implement new feature

Description of changes.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"

# 4. Push and create PR
git push -u origin 002-new-feature
gh pr create --title "feat: New Feature" --body "..."
```

### Bug Fix Workflow
```bash
# 1. Create branch from main
git checkout -b fix-user-isolation-bug

# 2. Write test exposing bug (RED)
pytest tests/test_isolation.py

# 3. Fix bug (GREEN)
# ... make changes ...

# 4. Verify test passes
pytest tests/test_isolation.py

# 5. Commit
git add .
git commit -m "$(cat <<'EOF'
fix: enforce user isolation in delete endpoint

Added missing user_id filter to prevent cross-user deletion.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"

# 6. Push and create PR
git push -u origin fix-user-isolation-bug
```

### Hotfix Workflow (Emergency)
```bash
# 1. Branch from main
git checkout main
git pull
git checkout -b hotfix-security-vulnerability

# 2. Apply minimal fix
# ... make changes ...

# 3. Test thoroughly
pytest

# 4. Commit with urgency note
git commit -m "$(cat <<'EOF'
fix: patch critical security vulnerability

URGENT: Fixes CVE-2024-XXXXX in dependency.
Requires immediate deployment.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"

# 5. Create PR with priority label
gh pr create --title "URGENT: Security patch" --label "priority:critical" --body "..."
```

## Troubleshooting

### Merge Conflicts
```bash
# 1. Fetch latest main
git fetch origin main

# 2. Rebase on main
git rebase origin/main

# 3. Resolve conflicts manually
# Edit files, then:
git add <resolved-files>
git rebase --continue

# 4. Force push (branch only, not main)
git push --force-with-lease
```

### Undo Last Commit (Not Pushed)
```bash
# Keep changes
git reset --soft HEAD~1

# Discard changes (⚠️ destructive)
git reset --hard HEAD~1
```

### Undo Last Commit (Already Pushed)
```bash
# Create revert commit
git revert HEAD
git push
```

## MCP GitHub Integration Examples

### Check PR Status
```
mcp__github__get_pull_request:
  owner: <owner>
  repo: <repo>
  pull_number: 42
```

### List Open PRs
```
mcp__github__list_pull_requests:
  owner: <owner>
  repo: <repo>
  state: open
```

### Merge PR
```
mcp__github__merge_pull_request:
  owner: <owner>
  repo: <repo>
  pull_number: 42
  merge_method: squash
```

## Constitutional Compliance

All Git operations must follow Constitutional Principle XXVIII:
- Conventional commit format
- Atomic commits
- Proper .gitignore
- Semantic versioning for releases
