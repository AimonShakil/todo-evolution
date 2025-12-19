# Todo Evolution - Phase II Frontend

**Next.js 16 + React 19 + Shadcn/ui + Better Auth**

Modern web interface for task management with JWT authentication.

---

## Features

- ✅ **Next.js 16** with App Router
- ✅ **React 19** with Server Components
- ✅ **Tailwind CSS 4** for styling
- ✅ **Shadcn/ui** component library (Neutral theme)
- ✅ **Better Auth** for authentication
- ✅ **TypeScript** for type safety
- ✅ **JWT Authentication** with FastAPI backend

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
- Sign out button

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
├── app/                    # Next.js App Router pages
│   ├── page.tsx           # Home (landing page)
│   ├── signin/page.tsx    # Sign in page
│   ├── signup/page.tsx    # Sign up page
│   ├── tasks/page.tsx     # Task management page
│   └── globals.css        # Global styles (Shadcn/ui theme)
├── components/
│   └── ui/                # Shadcn/ui components
│       ├── button.tsx
│       ├── card.tsx
│       ├── input.tsx
│       ├── label.tsx
│       ├── checkbox.tsx
│       └── ...
├── lib/
│   ├── auth.ts            # Better Auth server config
│   ├── auth-client.ts     # Better Auth client (React hooks)
│   ├── api-client.ts      # API client for backend
│   └── utils.ts           # Utility functions
├── .env.local             # Environment variables (not committed)
├── components.json        # Shadcn/ui config
├── package.json
├── tailwind.config.ts
└── tsconfig.json
```

---

## Known Issues

### Backend Compatibility
- Backend requires Python 3.12 (not 3.14) due to Pydantic + SQLModel compatibility
- See `backend/MIGRATION_AND_TESTING_NOTES.md` for details

### Future Improvements (Phase V)
- Move JWT tokens to httpOnly cookies (more secure)
- Add email verification
- Add password reset
- Add task priority, tags, due dates
- Add task filtering and sorting

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

## Next Steps

- **STEP 4**: Frontend Testing (React Testing Library, E2E)
- **STEP 5**: Integration & Deployment
- **Phase V**: Advanced features (priorities, tags, recurrence, sharing)

---

**Status**: ✅ **STEP 3 COMPLETE** - Frontend foundation ready for integration testing
