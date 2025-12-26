# Quick Resume Guide

## 📋 Where We Left Off

**Completed**: T001-T009 (Setup + Database Foundation)
**Next**: T010-T024 (Service Layer + MCP Tools + Agent Service)
**Progress**: 9/95 tasks (9.5%)

## 🚀 How to Resume Tomorrow

### Option 1: Simple Resume (Recommended)
Open terminal and say:
```
Continue from PROGRESS.md - implement Phase 2 Service Layer (T010-T024)
```

### Option 2: Detailed Resume
```
I'm resuming Phase III implementation. Read PROGRESS.md for full context.
We completed T001-T009 (Setup + Database). Continue with T010 (ConversationService).
```

### Option 3: Just Show Me What's Next
```
Read PROGRESS.md and show me the next 3 tasks to implement
```

## 📂 Key Files to Reference

1. **PROGRESS.md** - Full session summary (read this first!)
2. **specs/004-phase-iii-ai-chatbot/tasks.md** - Master task list
3. **specs/004-phase-iii-ai-chatbot/data-model.md** - Service implementation patterns
4. **CLAUDE.md** - Project rules (UV, not pip!)

## ⚠️ Important Reminders

- **Use UV**: `uv pip install` (NEVER `pip install`)
- **Database**: Migration 003 ready but not applied (connection timeout issue)
- **Branch**: `004-phase-iii-ai-chatbot`
- **Uncommitted**: 9 files changed (consider committing before continuing)

## 🎯 Next 3 Tasks

1. **T010a**: Implement ConversationService.create_conversation()
2. **T010b**: Implement ConversationService.get_active_conversation()
3. **T010c**: Implement ConversationService.list_user_conversations()

## 📞 Quick Commands

```bash
# Verify environment
cat PROGRESS.md

# Check git status
git status

# View next tasks
cat specs/004-phase-iii-ai-chatbot/tasks.md | grep -A 20 "T010"

# Test database connection
/mnt/g/AI_Eng/Q6/project/venv/bin/alembic current
```

---

**Pro Tip**: Claude Code reconstructs context from your codebase. The cleaner your progress tracking (PROGRESS.md, tasks.md, git commits), the easier it is to resume!
