# Manual Validation Checklist - Phase III

**Date**: 2025-12-28
**Validator**: ___________________
**Environment**: ☐ Staging  ☐ Production

---

## Prerequisites

### Environment Setup
- [ ] Backend server running (`uvicorn src.main:app --reload`)
- [ ] Frontend server running (`npm run dev`)
- [ ] Database accessible (Neon PostgreSQL)
- [ ] `OPENAI_API_KEY` configured in `backend/.env`
- [ ] Valid test user created (email + password)

### Verification Commands
```bash
# Backend health check
curl http://localhost:8000/health

# Frontend accessible
curl http://localhost:3000

# Database connection
psql $DATABASE_URL -c "SELECT version();"

# OpenAI API key configured
grep OPENAI_API_KEY backend/.env
```

---

## User Story 1: Natural Language Task Creation (P1) 🎯

**Goal**: Create tasks via natural language conversation

### Test Scenarios

#### Scenario 1.1: Simple task creation
- [ ] **Given**: User is authenticated
- [ ] **When**: User types "Remember to buy milk tomorrow"
- [ ] **Then**: Agent creates task with title "Buy milk tomorrow"
- [ ] **Then**: Agent confirms: "Added task: Buy milk tomorrow" (or similar)
- [ ] **Verify**: Task appears in Phase II task list

**Expected Response**:
```
Agent: I've added a task for you: "Buy milk tomorrow"
```

#### Scenario 1.2: Task with description
- [ ] **Given**: User is authenticated
- [ ] **When**: User types "I need to call the dentist to schedule my annual checkup"
- [ ] **Then**: Agent creates task with appropriate title and description
- [ ] **Then**: Agent confirms creation

#### Scenario 1.3: Multiple task phrasings
- [ ] **When**: User types "Add task: finish quarterly report by Friday"
- [ ] **Then**: Agent creates task successfully
- [ ] **When**: User types "I need to finish the report"
- [ ] **Then**: Agent creates another task

#### Scenario 1.4: Error handling
- [ ] **When**: Simulate database error (disconnect database temporarily)
- [ ] **Then**: Agent returns user-friendly error message
- [ ] **Then**: Agent suggests retry (not technical error details)

**Pass Criteria**: ✅ All 4 scenarios pass

---

## User Story 2: Natural Language Task Queries (P2)

**Goal**: Query tasks via natural language with formatted responses

### Test Scenarios

#### Scenario 2.1: List all tasks
- [ ] **Given**: User has 3 pending tasks and 2 completed tasks
- [ ] **When**: User asks "What tasks do I have?"
- [ ] **Then**: Agent lists all 5 tasks in conversational format (not raw JSON)
- [ ] **Verify**: Response is readable and includes task titles

**Expected Response**:
```
Agent: You have 5 tasks:

Pending:
1. Buy milk tomorrow
2. Call dentist for checkup
3. Finish quarterly report by Friday

Completed:
4. Grocery shopping
5. Email report to manager
```

#### Scenario 2.2: Filter by status
- [ ] **When**: User asks "Show me my incomplete tasks"
- [ ] **Then**: Agent displays only 3 pending tasks
- [ ] **Then**: Response formatted conversationally

#### Scenario 2.3: Empty task list
- [ ] **Given**: User has no tasks
- [ ] **When**: User asks "What's on my list?"
- [ ] **Then**: Agent responds gracefully: "No tasks yet. Create your first task!"

#### Scenario 2.4: Long task list
- [ ] **Given**: User has 10+ tasks
- [ ] **When**: User asks "What tasks do I have?"
- [ ] **Then**: Agent presents tasks in readable format
- [ ] **Then**: UI scrolls properly (not truncated)

**Pass Criteria**: ✅ All 4 scenarios pass

---

## User Story 3: Natural Language Task Management (P3)

**Goal**: Complete/delete/update tasks via conversation with multi-step planning

### Test Scenarios

#### Scenario 3.1: Complete task by title
- [ ] **Given**: User has task "Buy groceries"
- [ ] **When**: User says "Mark the grocery task as done"
- [ ] **Then**: Agent finds matching task automatically
- [ ] **Then**: Agent marks task as completed
- [ ] **Then**: Agent confirms: "Completed task: Buy groceries"
- [ ] **Verify**: Task marked complete in database

#### Scenario 3.2: Delete task by title
- [ ] **Given**: User has task "Call dentist"
- [ ] **When**: User says "Delete my dentist task"
- [ ] **Then**: Agent finds and deletes task
- [ ] **Then**: Agent confirms: "Deleted task: Call dentist"
- [ ] **Verify**: Task removed from database

#### Scenario 3.3: Update task title
- [ ] **Given**: User has task "Finish report"
- [ ] **When**: User says "Update my report task to 'Finish Q4 report by Friday'"
- [ ] **Then**: Agent finds and updates task
- [ ] **Then**: Agent confirms with new title

#### Scenario 3.4: No matching task
- [ ] **When**: User says "Complete the shopping task" (task doesn't exist)
- [ ] **Then**: Agent responds: "No matching task found. Would you like to create one?"
- [ ] **Then**: Agent offers to create the task

#### Scenario 3.5: Multiple matching tasks
- [ ] **Given**: User has 3 tasks with "report" in title
- [ ] **When**: User says "Complete the report task"
- [ ] **Then**: Agent lists matching tasks
- [ ] **Then**: Agent asks user to clarify which one

**Pass Criteria**: ✅ All 5 scenarios pass

---

## User Story 4: Conversation Context Awareness (P4)

**Goal**: Reference previous messages using pronouns and context

### Test Scenarios

#### Scenario 4.1: Pronoun resolution
- [ ] **Given**: Agent just created task "Buy milk"
- [ ] **When**: User says "Actually, make it almond milk"
- [ ] **Then**: Agent understands "it" refers to last-created task
- [ ] **Then**: Agent updates task to "Buy almond milk"
- [ ] **Verify**: Task title updated in database

#### Scenario 4.2: Reference previous list
- [ ] **Given**: Agent just listed tasks
- [ ] **When**: User says "Mark the first one as done"
- [ ] **Then**: Agent completes the first task from previous list

#### Scenario 4.3: Context persistence (10+ messages)
- [ ] **When**: Have 10+ message conversation
- [ ] **Then**: Agent maintains context throughout
- [ ] **Then**: Agent can still reference earlier messages

#### Scenario 4.4: New conversation
- [ ] **When**: User clicks "New Conversation" button
- [ ] **Then**: Previous conversation archived
- [ ] **Then**: New conversation starts fresh
- [ ] **Verify**: Previous conversation accessible in history sidebar

#### Scenario 4.5: Conversation history UI
- [ ] **Given**: User has 3 conversations
- [ ] **When**: User views conversation list sidebar
- [ ] **Then**: All 3 conversations displayed with message counts
- [ ] **Then**: Active conversation highlighted
- [ ] **When**: User clicks old conversation
- [ ] **Then**: Conversation switches (UI clears for now)

**Pass Criteria**: ✅ All 5 scenarios pass

---

## Cross-Cutting Concerns

### Authentication & Security
- [ ] Chat requires valid JWT token
- [ ] Invalid token returns 401 Unauthorized
- [ ] User can only access own conversations
- [ ] User can only manage own tasks

### Error Handling
- [ ] OpenAI API error → User-friendly message
- [ ] Database error → Graceful degradation
- [ ] Network timeout → Retry suggestion
- [ ] Invalid input → Clear validation message

### Performance
- [ ] Chat responses < 2 seconds (p95)
- [ ] UI responsive during agent processing
- [ ] No memory leaks after 50+ messages
- [ ] Concurrent users don't block each other

### UI/UX
- [ ] Loading indicator while agent processes
- [ ] Auto-scroll to bottom on new messages
- [ ] Message timestamps displayed
- [ ] Clear visual distinction: user vs assistant messages
- [ ] Navigation between Tasks and Chat pages works
- [ ] Sign out functionality works

### Data Persistence
- [ ] Conversations persist across sessions
- [ ] Messages persist in database
- [ ] Conversation history accessible after logout/login
- [ ] Active conversation resumes on page refresh

---

## Edge Cases

### Auto-Archive (500 messages)
- [ ] **Given**: Conversation has 499 messages
- [ ] **When**: User sends 500th message
- [ ] **Then**: Conversation auto-archives
- [ ] **Then**: New conversation created
- [ ] **Then**: User notified: "Previous conversation archived. Starting fresh."

### Message Length Limit (4000 chars)
- [ ] **When**: User sends message >4000 characters
- [ ] **Then**: System rejects with error
- [ ] **Then**: Error message: "Message too long. Please keep under 4000 characters."

### Model Fallback
- [ ] **When**: Simulate GPT-4 rate limit (use large volume of requests)
- [ ] **Then**: Agent falls back to GPT-3.5-turbo
- [ ] **Then**: Response still functional

### Ambiguous Intent
- [ ] **When**: User types "Add milk"
- [ ] **Then**: Agent interprets as task creation
- [ ] **Or**: Agent asks clarification: "Create task or search?"

### Tool Failure
- [ ] **When**: Simulate task service failure
- [ ] **Then**: Agent handles gracefully
- [ ] **Then**: User-friendly error message
- [ ] **Then**: Conversation continues (no crash)

---

## Test Coverage Summary

| User Story | Total Scenarios | Passed | Failed | Notes |
|------------|----------------|--------|--------|-------|
| US1: Task Creation | 4 | ___ | ___ | |
| US2: Task Queries | 4 | ___ | ___ | |
| US3: Task Management | 5 | ___ | ___ | |
| US4: Context Awareness | 5 | ___ | ___ | |
| Cross-Cutting | 19 | ___ | ___ | |
| Edge Cases | 5 | ___ | ___ | |
| **Total** | **42** | ___ | ___ | |

---

## Sign-Off

### Validator Information
- **Name**: ___________________
- **Date**: ___________________
- **Environment**: ___________________

### Overall Assessment
- [ ] **PASS**: All critical scenarios pass (US1-US4)
- [ ] **PASS WITH ISSUES**: Minor issues documented below
- [ ] **FAIL**: Critical issues prevent deployment

### Issues Found
| # | Severity | Issue | Status |
|---|----------|-------|--------|
| 1 | | | |
| 2 | | | |
| 3 | | | |

### Deployment Recommendation
- [ ] **APPROVED**: Ready for production deployment
- [ ] **APPROVED WITH CONDITIONS**: Deploy with monitoring
- [ ] **REJECTED**: Fix issues before deployment

### Notes
___________________________________________________________________
___________________________________________________________________
___________________________________________________________________

---

## Quick Test Script

For rapid validation, run this sequence:

```bash
# 1. Create task
"Remember to buy milk"
Expected: Task created, confirmation shown

# 2. List tasks
"What tasks do I have?"
Expected: Milk task listed

# 3. Update task
"Actually, make it almond milk"
Expected: Task updated to "almond milk"

# 4. Complete task
"Mark the milk task as done"
Expected: Task marked complete

# 5. Verify completion
"Show me completed tasks"
Expected: Almond milk task shown as complete

# 6. Delete task
"Delete the milk task"
Expected: Task deleted, confirmation shown

# 7. Verify deletion
"What tasks do I have?"
Expected: Empty list or other tasks (no milk task)
```

**Time**: ~5 minutes for quick smoke test, ~30 minutes for full validation

---

## Success Criteria Met

- [ ] **SC-001**: p95 latency <2s ✅ (Monitor in production)
- [ ] **SC-002**: ≥90% intent accuracy ✅ (Monitor in production)
- [ ] **SC-003**: Multi-step chaining works ✅
- [ ] **SC-004**: 10+ message context ✅
- [ ] **SC-005**: 100 concurrent users ✅ (Load test separately)
- [ ] **SC-006**: 100% Phase II reuse ✅
- [ ] **SC-007**: 100% error recovery ✅
- [ ] **SC-008**: Cross-device access ✅
- [ ] **SC-009**: <$0.10/conversation ✅
- [ ] **SC-010**: 100% confirmations ✅

**Overall**: ☐ All success criteria validated
