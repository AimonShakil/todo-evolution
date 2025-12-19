# Phase II Research Notes

**Date**: 2025-12-15
**Branch**: 003-phase-ii-web-app
**Status**: STEP 0.4-0.5 Research

---

## STEP 0.4: FastAPI + Better Auth Integration (2025)

### FastAPI JWT Middleware Pattern

**Best Practice Pattern (2025)**:
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from typing import Annotated

security = HTTPBearer()

async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> dict:
    """Extract and validate JWT token, return user claims."""
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=["HS256"]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        return {"user_id": user_id}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
```

**Usage in Routes**:
```python
from fastapi import APIRouter, Depends

router = APIRouter()

@router.get("/api/{user_id}/tasks")
async def get_tasks(
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    # Verify JWT user matches URL user_id
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Proceed with query...
```

### Better Auth + FastAPI Integration

**Installation**:
```bash
uv pip install fastapi uvicorn python-jose passlib[bcrypt] python-multipart
```

**Password Hashing**:
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

**JWT Token Generation**:
```python
from jose import jwt
from datetime import datetime, timedelta

def create_access_token(user_id: str) -> str:
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode = {"sub": user_id, "exp": expire}
    return jwt.encode(to_encode, JWT_SECRET, algorithm="HS256")
```

**Authentication Routes**:
```python
@router.post("/api/auth/signup")
async def signup(email: str, password: str, session: AsyncSession = Depends(get_session)):
    # 1. Check if user exists
    # 2. Hash password
    # 3. Create user in database
    # 4. Return JWT token
    pass

@router.post("/api/auth/signin")
async def signin(email: str, password: str, session: AsyncSession = Depends(get_session)):
    # 1. Find user by email
    # 2. Verify password
    # 3. Generate JWT token
    # 4. Return token
    pass
```

### CORS Configuration for Next.js

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Rate Limiting with SlowAPI

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@router.get("/api/{user_id}/tasks")
@limiter.limit("100/minute")  # 100 requests per minute
async def get_tasks(request: Request, user_id: str):
    pass
```

---

## STEP 0.5: Next.js 16 + Better Auth Integration (2025)

### Next.js 16 App Router Best Practices

**Project Structure**:
```
frontend/
├── app/
│   ├── layout.tsx          # Root layout with providers
│   ├── page.tsx            # Landing page
│   ├── auth/
│   │   ├── signin/page.tsx # Server Component
│   │   └── signup/page.tsx # Server Component
│   └── tasks/
│       └── page.tsx        # Server Component (fetch tasks)
├── components/
│   ├── TaskList.tsx        # Client Component ('use client')
│   ├── TaskForm.tsx        # Client Component
│   └── ui/                 # Shadcn/ui components
└── lib/
    ├── api.ts              # API client
    └── auth.ts             # Better Auth config
```

### Better Auth React Hooks (2025)

**Installation**:
```bash
npm install better-auth-react @better-auth/client
```

**Configuration** (`lib/auth.ts`):
```typescript
import { BetterAuthClient } from '@better-auth/client'

export const authClient = new BetterAuthClient({
  baseURL: 'http://localhost:8000/api/auth',
  credentials: 'include',  // Send cookies
})
```

**Provider Setup** (`app/layout.tsx`):
```typescript
import { BetterAuthProvider } from 'better-auth-react'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <BetterAuthProvider client={authClient}>
          {children}
        </BetterAuthProvider>
      </body>
    </html>
  )
}
```

**Usage in Components**:
```typescript
'use client'

import { useAuth } from 'better-auth-react'

export function SignInForm() {
  const { signIn, isLoading } = useAuth()

  async function handleSubmit(email: string, password: string) {
    const result = await signIn({ email, password })
    if (result.success) {
      router.push('/tasks')
    }
  }
}
```

### API Client with JWT (`lib/api.ts`)

```typescript
class APIClient {
  private baseURL = 'http://localhost:8000'

  private async getToken(): Promise<string> {
    // Get token from Better Auth session
    const session = await authClient.getSession()
    return session.token
  }

  async get<T>(path: string): Promise<T> {
    const token = await this.getToken()
    const res = await fetch(`${this.baseURL}${path}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })
    if (!res.ok) throw new Error(`API error: ${res.status}`)
    return res.json()
  }

  async post<T>(path: string, data: any): Promise<T> {
    const token = await this.getToken()
    const res = await fetch(`${this.baseURL}${path}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
    if (!res.ok) throw new Error(`API error: ${res.status}`)
    return res.json()
  }
}

export const api = new APIClient()
```

### Server Components (Next.js 16)

```typescript
// app/tasks/page.tsx
import { cookies } from 'next/headers'

export default async function TasksPage() {
  // Fetch data on server
  const cookieStore = await cookies()
  const token = cookieStore.get('auth-token')

  const tasks = await fetch('http://localhost:8000/api/user123/tasks', {
    headers: { Authorization: `Bearer ${token?.value}` },
  }).then(res => res.json())

  return <TaskList tasks={tasks} />
}
```

### Client Components (Interactive)

```typescript
'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'

export function TaskForm() {
  const [title, setTitle] = useState('')

  async function handleSubmit() {
    await api.post('/api/user123/tasks', { title })
  }

  return (
    <form>
      <Input value={title} onChange={(e) => setTitle(e.target.value)} />
      <Button onClick={handleSubmit}>Add Task</Button>
    </form>
  )
}
```

### CORS Configuration

**Backend must allow Next.js origin**:
```python
allow_origins=["http://localhost:3000"]  # Next.js dev
```

**Frontend must send credentials**:
```typescript
fetch(url, { credentials: 'include' })  # Send cookies
```

---

## Key Decisions

### 1. Authentication Flow
- ✅ Better Auth handles user creation and password hashing
- ✅ JWT tokens for API authentication (stateless)
- ✅ Shared `BETTER_AUTH_SECRET` between frontend and backend
- ✅ Tokens stored in httpOnly cookies (XSS protection)

### 2. API Security
- ✅ JWT validation middleware on ALL endpoints
- ✅ User ID verification (JWT user matches URL `{user_id}`)
- ✅ Rate limiting (100 req/min per user)
- ✅ CORS restricted to Next.js origin

### 3. Next.js 16 Architecture
- ✅ Server Components by default (fetch on server, better performance)
- ✅ Client Components only when needed (`'use client'` directive)
- ✅ Better Auth React hooks for auth state
- ✅ API client abstracts token management

### 4. Development Workflow
- ✅ Backend runs on http://localhost:8000
- ✅ Frontend runs on http://localhost:3000
- ✅ CORS allows cross-origin requests
- ✅ JWT tokens enable stateless auth

---

## Dependencies

### Backend
```bash
uv pip install fastapi uvicorn sqlmodel alembic python-jose passlib[bcrypt] httpx slowapi
```

### Frontend
```bash
npm install next@latest react@latest react-dom@latest
npm install better-auth-react @better-auth/client
npm install @radix-ui/react-* lucide-react  # Shadcn/ui dependencies
```

---

## References

- FastAPI Docs: https://fastapi.tiangolo.com
- Next.js 16 Docs: https://nextjs.org/docs
- Better Auth: https://better-auth.com
- SQLModel: https://sqlmodel.tiangolo.com
- Shadcn/ui: https://ui.shadcn.com

---

**Status**: Research complete, ready for implementation
**Next Steps**: STEP 0.6 (Database Migration Strategy), STEP 0.7 (Alembic Setup)
