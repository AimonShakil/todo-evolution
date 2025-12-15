---
name: phr-creator
description: Create Prompt History Records after every user interaction to capture learning and traceability. Use after completing implementation, planning, debugging, or significant discussions. Required by constitution for ALL user interactions.
allowed-tools: Read, Write, Glob, Grep
---

# PHR Creator Skill

Creates comprehensive Prompt History Records following constitutional mandate (Principle I).

## Constitutional Requirement

**MANDATORY**: PHR must be created after EVERY user interaction except `/sp.phr` itself.

## Routing Rules (All under `history/prompts/`)

- **Constitution work** → `history/prompts/constitution/`
- **Feature work** → `history/prompts/<feature-name>/` (auto-detect from branch or context)
- **General work** → `history/prompts/general/`

## Process

1. **Detect Stage**: One of `constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general`

2. **Generate Title**: 3-7 words; create slug for filename

3. **Allocate ID**: Read existing PHRs in target directory, increment highest ID. On collision, increment again.

4. **Read Template**: `.specify/templates/phr-template.prompt.md`

5. **Fill Template** (NO placeholders remaining):
   - `ID`: Allocated number
   - `TITLE`: Generated title
   - `STAGE`: Detected stage
   - `DATE_ISO`: Current date (YYYY-MM-DD format)
   - `SURFACE`: "agent"
   - `MODEL`: "claude-sonnet-4-5"
   - `FEATURE`: Feature name or "none"
   - `BRANCH`: Current git branch
   - `USER`: System username
   - `COMMAND`: Current slash command or "general"
   - `LABELS`: Topics as JSON array
   - `LINKS`: SPEC/TICKET/ADR/PR URLs or "null"
   - `FILES_YAML`: List of created/modified files (one per line with " - " prefix)
   - `TESTS_YAML`: List of tests run/added (one per line with " - " prefix)
   - `PROMPT_TEXT`: Full user input (verbatim, NOT truncated)
   - `RESPONSE_TEXT`: Key assistant output (concise but representative)
   - Any OUTCOME/EVALUATION fields required by template

6. **Compute Output Path**:
   - Constitution: `history/prompts/constitution/<ID>-<slug>.constitution.prompt.md`
   - Feature: `history/prompts/<feature-name>/<ID>-<slug>.<stage>.prompt.md`
   - General: `history/prompts/general/<ID>-<slug>.general.prompt.md`

7. **Write File**: Use Write tool with complete content

8. **Validate**:
   - No unresolved placeholders (e.g., `{{THIS}}`, `[THAT]`)
   - Title, stage, dates match front-matter
   - PROMPT_TEXT is complete (not truncated)
   - File exists and is readable
   - Path matches routing rules

9. **Report**: Print ID, path, stage, title

## Example Output

```
✓ PHR Created: ID 042
  Path: history/prompts/002-phase-i-console-app/042-implement-add-task-command.red.prompt.md
  Stage: red
  Title: Implement Add Task Command
```

## Fallback (if agent-native fails)

If shell script exists and is preferred:
```bash
.specify/scripts/bash/create-phr.sh --title "title" --stage <stage> [--feature <name>] --json
```

Then fill all placeholders in the created file.

## Never Skip PHR

On any failure: warn but do not block the main command. Skip PHR only for `/sp.phr` itself.
