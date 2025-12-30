# Todo Evolution - Phase III Frontend

**Next.js 16 + React 19 + AI-Powered Chat Interface**

Modern web interface for task management with natural language AI assistant.

---

## Features

- ✅ **Next.js 16** with App Router (Turbopack)
- ✅ **React 19** with Server Components
- ✅ **Tailwind CSS 4** for styling
- ✅ **Shadcn/ui** component library (Neutral theme)
- ✅ **TypeScript** for type safety
- ✅ **JWT Authentication** with FastAPI backend
- ✅ **AI Chat Interface** (Phase III) - Natural language task management
- ✅ **Conversation History** (Phase III) - Multi-turn dialogue support

---

## Pages

### `/` - Home
- Landing page with sign in/sign up buttons
- Auto-redirects to `/tasks` if already authenticated

### `/signin` - Sign In
- Email/password authentication
- Integrates with FastAPI `POST /api/auth/signin`
- Stores JWT token in localStorage

### `/signup` - Sign Up
- Create new user account
- Integrates with FastAPI `POST /api/auth/signup`
- Auto-signs in after successful registration

### `/tasks` - Task Management
- View all tasks for authenticated user
- Create new tasks (title + optional description)
- Toggle task completion
- Delete tasks
- Navigation to Chat interface
- Sign out button

### `/chat` - AI Assistant (Phase III)
- **Natural language task management** via conversational interface
- **Conversation history sidebar** showing all past conversations
- **Context-aware responses** across multi-turn dialogues
- **Auto-archive** at 500 messages per conversation
- Switch between conversations or start new ones
- Powered by OpenAI GPT-4 with function calling

**Example interactions**:
- "Add task: Buy milk"
- "What tasks do I have?"
- "Complete the milk task"
- "Change it to almond milk" (context-aware)

---

## Getting Started

### Prerequisites

- Node.js 20+
- Backend API running on `http://localhost:8000`

### Installation

```bash
cd frontend
npm install
```

### Environment Variables

Create `.env.local` file:

```bash
# Better Auth Configuration
BETTER_AUTH_SECRET=your-secret-here
BETTER_AUTH_URL=http://localhost:3000

# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Important**: Replace `BETTER_AUTH_SECRET` with the same secret used in backend's `.env`.

### Development

```bash
npm run dev
```

Visit: http://localhost:3000

### Build for Production

```bash
npm run build
npm start
```

---

## API Integration

All API requests go through `/lib/api-client.ts`:

### Authentication API (`authApi`)
- `authApi.signup({ email, name, password })` → Returns `{ user_id, email, name, token }`
- `authApi.signin({ email, password })` → Returns `{ user_id, email, name, token }`

### Task API (`taskApi`)
All task endpoints require JWT token:
- `taskApi.getAll(userId, token)` → Get all tasks
- `taskApi.create(userId, { title, description }, token)` → Create task
- `taskApi.toggle(userId, taskId, token)` → Toggle completion
- `taskApi.delete(userId, taskId, token)` → Delete task

### Chat API (`chatApi`) - Phase III
All chat endpoints require JWT token:
- `chatApi.sendMessage(userId, { message }, token)` → Send message to AI assistant
  - Returns: `{ success, response, conversation_id, tool_calls, model_used }`
- `chatApi.getConversations(userId, token)` → Get conversation history
  - Returns: Array of `{ id, created_at, updated_at, is_active, message_count }`

---

## Constitutional Compliance

### Principle II: User Data Isolation
- JWT token contains `user_id`
- All API requests include JWT in `Authorization: Bearer {token}` header
- Backend validates JWT user matches URL `{user_id}` parameter
- Returns `403 Forbidden` if user tries to access another user's data

### Principle IX: Code Quality
- TypeScript for type safety
- Component-based architecture
- Reusable UI components from Shadcn/ui
- Proper error handling and loading states

### Principle XII: Security
- JWT tokens stored in localStorage (Phase II - will use httpOnly cookies in Phase V)
- Password minimum 8 characters
- HTTPS required for production
- CORS configured in backend

---

## Project Structure

```
frontend/
├── app/                         # Next.js App Router pages
│   ├── page.tsx                # Home (landing page)
│   ├── signin/page.tsx         # Sign in page
│   ├── signup/page.tsx         # Sign up page
│   ├── tasks/page.tsx          # Task management page
│   ├── chat/page.tsx           # AI chat page (Phase III)
│   ├── layout.tsx              # Root layout with metadata
│   └── globals.css             # Global styles (Shadcn/ui theme)
├── components/
│   ├── ui/                     # Shadcn/ui components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── input.tsx
│   │   ├── label.tsx
│   │   ├── checkbox.tsx
│   │   └── ...
│   ├── ChatInterface.tsx       # Phase III - Main chat UI
│   ├── ConversationList.tsx    # Phase III - Conversation sidebar
│   └── Navigation.tsx          # Global navigation (Tasks ↔ Chat)
├── hooks/
│   └── useConversationSwitcher.ts  # Phase III - Conversation state management
├── lib/
│   ├── auth.ts                 # Better Auth server config
│   ├── auth-client.ts          # Better Auth client (React hooks)
│   ├── api-client.ts           # API client for backend (includes chatApi)
│   ├── chatkit-config.ts       # Phase III - Chat configuration & validation
│   └── utils.ts                # Utility functions
├── .env.local                  # Environment variables (not committed)
├── components.json             # Shadcn/ui config
├── package.json
├── tailwind.config.ts
└── tsconfig.json
```

---

## Known Issues

### Backend Compatibility
- Backend requires Python 3.12 (not 3.14) due to Pydantic + SQLModel compatibility
- See `backend/MIGRATION_AND_TESTING_NOTES.md` for details

### Future Improvements
- **Phase IV**: Observability & Production (logging, metrics, cleanup scripts)
- **Phase V**: Advanced task features (priority, tags, due dates, filtering)
- **Phase VI**: Security enhancements (httpOnly cookies, email verification, password reset)
- **Phase VII**: Collaboration features (task sharing, teams, real-time updates)

---

## Development Notes

### Adding New Shadcn/ui Components

```bash
npx shadcn@latest add <component-name>
```

Example:
```bash
npx shadcn@latest add dialog
npx shadcn@latest add dropdown-menu
```

---

## Testing

**Manual Testing** (requires backend running):

1. Start backend: `cd backend && python src/main.py`
2. Start frontend: `cd frontend && npm run dev`
3. Open http://localhost:3000
4. Click "Create Account"
5. Fill form and submit
6. Should redirect to `/tasks` with empty task list
7. Create a task
8. Toggle completion
9. Delete task
10. Sign out
11. Sign in with same credentials

**Automated Testing** (STEP 4):
- Not yet implemented
- Will use React Testing Library
- Will add E2E tests with Playwright

---

## Development Status

- ✅ **Phase I Complete**: Console-based task management
- ✅ **Phase II Complete**: Web API with JWT authentication
- ✅ **Phase III Complete**: AI chatbot with natural language interface
  - ✅ User Story 1: Task creation via chat
  - ✅ User Story 2: Task queries with conversational responses
  - ✅ User Story 3: Task management without IDs (search-based)
  - ✅ User Story 4: Context awareness & conversation history
  - ✅ Auto-archive at 500 messages

---

**Next Steps**: Phase IV (Observability), Phase V (Advanced Features)

---

**Status**: ✅ **Phase III Complete** - AI-powered task management ready for production
