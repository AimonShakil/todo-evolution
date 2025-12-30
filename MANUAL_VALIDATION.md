# Phase III Manual Validation Checklist

**Purpose**: Validate all 4 user stories work end-to-end
**Time**: ~15-20 minutes
**Prerequisites**: Backend and frontend running

---

## Setup

### 1. Start Backend
```bash
cd backend
source .venv/bin/activate
uvicorn src.main:app --reload --port 8000
```

**Expected**: Server starts on http://localhost:8000
**Verify**: Visit http://localhost:8000/docs (Swagger UI loads)

### 2. Start Frontend
```bash
cd frontend
npm run dev
```

**Expected**: App starts on http://localhost:3000
**Verify**: Visit http://localhost:3000 (landing page loads)

### 3. Create Test Account
1. Go to http://localhost:3000/signup
2. Fill in:
   - Email: `test@example.com`
   - Name: `Test User`
   - Password: `password123`
3. Click "Create Account"

**Expected**: Redirects to `/tasks` page
**Verify**: You see empty task list

---

## User Story 1: Task Creation via Chat

**Goal**: Create tasks using natural language in the chat interface

### Test Scenarios

#### Scenario 1.1: Simple Task Creation
1. Navigate to `/chat` page (use navigation or go to http://localhost:3000/chat)
2. Type: `Add task: Buy milk`
3. Press Send

**Expected Response**:
- ✅ AI responds: "Added task: Buy milk"
- ✅ Tool call shown (if enabled)
- ✅ Message appears in chat history

**Verification**:
- Go to `/tasks` page
- ✅ "Buy milk" task appears in list
- ✅ Task is marked as incomplete (unchecked)

#### Scenario 1.2: Task with Description
1. In chat, type: `Remember to call the dentist on Monday at 2pm`
2. Press Send

**Expected Response**:
- ✅ AI creates task with appropriate title
- ✅ Description may include time details

**Verification**:
- Go to `/tasks` page
- ✅ Dentist task appears

#### Scenario 1.3: Multiple Tasks in One Message
1. Type: `I need to finish the quarterly report and buy groceries`
2. Press Send

**Expected Response**:
- ✅ AI should handle this (may create one or two tasks depending on interpretation)

---

## User Story 2: Task Queries with Conversational Responses

**Goal**: Query tasks and receive formatted, conversational responses

### Test Scenarios

#### Scenario 2.1: List All Tasks
1. Type: `What tasks do I have?`
2. Press Send

**Expected Response**:
- ✅ AI lists all tasks (should include "Buy milk", "Call dentist", "Quarterly report", etc.)
- ✅ Response is conversational (not raw JSON)
- ✅ Shows task IDs and completion status
- ✅ Formatted with newlines/bullets

**Example Response**:
```
You have 3 pending tasks and 0 completed tasks:

Pending:
1. Buy milk (ID: 1)
2. Call the dentist on Monday at 2pm (ID: 2)
3. Finish the quarterly report (ID: 3)
```

#### Scenario 2.2: Filter Incomplete Tasks
1. Type: `Show me my incomplete tasks`
2. Press Send

**Expected Response**:
- ✅ Lists only pending tasks
- ✅ Excludes completed tasks

#### Scenario 2.3: Empty List Handling
1. Complete all tasks manually via `/tasks` page
2. Type: `What have I completed?`
3. Press Send

**Expected Response**:
- ✅ Shows completed tasks with friendly message
- OR if no completed tasks: "You haven't completed any tasks yet. Keep working!"

---

## User Story 3: Task Management without IDs

**Goal**: Manage tasks using natural language (no need to know task IDs)

### Test Scenarios

#### Scenario 3.1: Complete Task by Name (Single Match)
1. Type: `Complete the milk task`
2. Press Send

**Expected Response**:
- ✅ AI responds: "Completed task: Buy milk"
- ✅ No clarification needed (direct match)

**Verification**:
- Go to `/tasks` page
- ✅ "Buy milk" task is checked (completed)

#### Scenario 3.2: Delete Task by Name
1. Type: `Delete my dentist task`
2. Press Send

**Expected Response**:
- ✅ AI responds: "Deleted task: Call the dentist on Monday at 2pm"

**Verification**:
- Go to `/tasks` page
- ✅ Dentist task is gone

#### Scenario 3.3: Update Task by Name
1. Type: `Change the report task to 'Finish Q4 report by Friday'`
2. Press Send

**Expected Response**:
- ✅ AI responds: "Updated task: Finish Q4 report by Friday"

**Verification**:
- Go to `/tasks` page
- ✅ Task title updated

#### Scenario 3.4: Ambiguous Match Handling
1. Create multiple similar tasks:
   - Type: `Add task: Buy organic milk`
   - Type: `Add task: Buy whole milk`
2. Type: `Complete the milk task`
3. Press Send

**Expected Response**:
- ✅ AI lists 2+ matching tasks and asks for clarification
- ✅ Shows task IDs for disambiguation
- ✅ Message like: "I found 2 tasks matching 'milk': 1. Buy organic milk (ID: 4) 2. Buy whole milk (ID: 5). Please specify which one."

#### Scenario 3.5: No Match Handling
1. Type: `Complete the unicorn task`
2. Press Send

**Expected Response**:
- ✅ AI responds: "I couldn't find a pending task matching 'unicorn'. Would you like me to create one?"

---

## User Story 4: Context Awareness & Conversation History

**Goal**: Maintain context across multi-turn dialogues

### Test Scenarios

#### Scenario 4.1: Pronoun Resolution
1. Type: `Add task: Buy almond milk`
2. Press Send
3. **Immediately after**, type: `Actually, make it oat milk instead`
4. Press Send

**Expected Response**:
- ✅ AI understands "it" refers to the last-created task
- ✅ Updates "Buy almond milk" → "Buy oat milk"
- OR creates new task if context lost (acceptable)

**Verification**:
- Go to `/tasks` page
- ✅ Task should be "Buy oat milk" (updated) or both tasks exist

#### Scenario 4.2: Conversation History Sidebar
1. Look at left sidebar in `/chat` page
2. Verify:
   - ✅ Current conversation is highlighted (green "Active" badge)
   - ✅ Message count is displayed (should show ~10+ messages if you've been testing)
   - ✅ Timestamp shows (e.g., "Just now", "5m ago")

#### Scenario 4.3: New Conversation
1. Click "New Conversation" button in sidebar
2. Type: `What tasks do I have?`
3. Press Send

**Expected Result**:
- ✅ Chat clears (fresh conversation)
- ✅ AI still has access to your tasks (user data persists)
- ✅ Old conversation appears in sidebar with previous message count

#### Scenario 4.4: Switch Conversations
1. Click on old conversation in sidebar
2. Verify:
   - ✅ Chat clears (shows fresh welcome message)
   - ✅ Conversation is now marked as active
   - ✅ Backend tracks this as active conversation (new messages go here)

Note: Message history is maintained on backend but not re-displayed in UI (this is by design - fresh UI on switch).

#### Scenario 4.5: Multi-Turn Dialogue
1. Start new conversation
2. Type: `Add task: Water the plants`
3. Type: `When should I do it?`
4. Type: `How many tasks do I have now?`
5. Type: `Complete the plants task`

**Expected Results**:
- ✅ AI maintains context across all 4 messages
- ✅ References previous messages appropriately
- ✅ Understands "the plants task" refers to earlier task

---

## Auto-Archive Feature (500 Messages)

**Goal**: Verify conversations auto-archive at 500 messages

**Note**: This is time-consuming to test manually. Skip unless critical.

**Test**:
1. Create 500 messages in a conversation (scripted test recommended)
2. Verify conversation is archived (is_active = false)
3. Verify archived conversation still appears in sidebar

**Alternative**: Trust the implementation (auto-archive logic is simple and tested via unit test script).

---

## Validation Completion Checklist

After completing all scenarios above, verify:

- ✅ **User Story 1**: Tasks created via natural language (/chat works)
- ✅ **User Story 2**: Task queries return conversational responses
- ✅ **User Story 3**: Tasks managed without IDs (search-based)
- ✅ **User Story 4**: Context maintained across multi-turn dialogues
- ✅ **Conversation History**: Sidebar shows conversations, switching works
- ✅ **Navigation**: Tasks ↔ Chat navigation works
- ✅ **Sign Out**: Can sign out and sign back in
- ✅ **User Isolation**: Create second account, verify tasks are separate

---

## Bug Reporting

If any scenario fails, note:
1. Which scenario failed
2. What you typed
3. What happened (actual behavior)
4. What you expected (expected behavior)
5. Any error messages in browser console (F12 → Console tab)
6. Any error messages in backend terminal

---

**Status**: Ready for manual validation
**Estimated Time**: 15-20 minutes for full validation
**Priority Scenarios**: 1.1, 2.1, 3.1, 4.1, 4.2 (cover core functionality)
