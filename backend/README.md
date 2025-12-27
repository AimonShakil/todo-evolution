# Backend - Todo Evolution Phase III

Full-stack task management application with AI-powered natural language interface.

## Features

- **Phase I**: Console-based task management (SQLite)
- **Phase II**: Web API with JWT authentication (FastAPI + PostgreSQL)
- **Phase III**: AI chatbot for natural language task management (OpenAI GPT-4)

## Setup

### 1. Install UV Package Manager

UV is a fast Python package installer (required for this project):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Create Virtual Environment

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

**Phase III includes OpenAI integration** - all dependencies installed via UV:

```bash
uv pip install -r requirements.txt
```

This installs:
- **Web Framework**: FastAPI, Uvicorn
- **Database**: SQLModel, Alembic, AsyncPG (PostgreSQL driver)
- **Authentication**: python-jose, passlib
- **AI Integration**: openai>=1.0.0 (Phase III)
- **Testing**: pytest, pytest-cov, pytest-asyncio

### 4. Configure Environment Variables

Copy the example environment file and configure:

```bash
cp .env.example .env
```

**Required variables**:
- `DATABASE_URL`: PostgreSQL connection string (Neon or local)
- `JWT_SECRET_KEY`: Secret key for JWT token signing
- **`OPENAI_API_KEY`** (Phase III): Your OpenAI API key from https://platform.openai.com/api-keys

Example `.env`:
```bash
DATABASE_URL=postgresql+asyncpg://user:password@host/database
JWT_SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=sk-proj-...  # Get from OpenAI dashboard
```

**Important**: Never commit `.env` to git. The `.gitignore` already excludes it.

### 5. Run Database Migrations

Apply all database schema migrations:

```bash
alembic upgrade head
```

This creates:
- **Phase II**: `user` and `task` tables
- **Phase III**: `conversation` and `message` tables

### 6. Start Development Server

```bash
uvicorn src.main:app --reload --port 8000
```

Server will start at http://localhost:8000

## Testing

The backend is running correctly if you see:

```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs (interactive API testing)
- **ReDoc**: http://localhost:8000/redoc (API reference documentation)

### Key Endpoints

**Authentication** (`/api/auth`):
- `POST /api/auth/signup` - Create new user account
- `POST /api/auth/signin` - Sign in and get JWT token

**Tasks** (`/api/{user_id}/tasks`):
- `GET /api/{user_id}/tasks` - List all tasks
- `POST /api/{user_id}/tasks` - Create new task
- `PATCH /api/{user_id}/tasks/{task_id}` - Update task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete task
- `POST /api/{user_id}/tasks/{task_id}/toggle` - Toggle completion status

**Chat** (`/api/{user_id}/chat`) - **Phase III**:
- `POST /api/{user_id}/chat` - Send message to AI assistant
- `GET /api/{user_id}/conversations` - List conversation history

All protected endpoints require `Authorization: Bearer {token}` header.

## Phase III Features

### Natural Language Task Management

The AI chatbot understands natural language commands:

**Create tasks**:
- "Add task: Buy milk"
- "Remember to call the dentist"
- "I need to finish the quarterly report by Friday"

**Query tasks**:
- "What tasks do I have?"
- "Show me my incomplete tasks"
- "What have I completed?"

**Manage tasks**:
- "Complete the milk task"
- "Delete my dentist appointment"
- "Change the report task to 'Finish Q4 report'"

### Conversation History

- Conversations auto-archived at 500 messages
- Sidebar shows conversation history with message counts
- Context awareness across multi-turn dialogues
- Switch between conversations seamlessly

## Architecture

**Technology Stack**:
- **Backend**: FastAPI (async Python web framework)
- **Database**: PostgreSQL (Neon serverless or local)
- **ORM**: SQLModel (Pydantic + SQLAlchemy)
- **Migrations**: Alembic
- **Authentication**: JWT tokens (python-jose + passlib)
- **AI Integration**: OpenAI GPT-4 with function calling
- **Testing**: pytest with async support

**Constitutional Principles**:
- **Principle II**: User Data Isolation (all queries filter by user_id)
- **Principle IX**: Code Quality Standards (type hints, docstrings, async/await)
- **Principle XIV**: Authentication & Authorization (JWT tokens required)
- **Principle XXVI**: Agent Orchestration (MCP tools + OpenAI integration)

## Troubleshooting

**Database connection errors**:
- Verify `DATABASE_URL` in `.env` is correct
- Check Neon database is accessible
- Run `alembic upgrade head` to apply migrations

**OpenAI API errors** (Phase III):
- Verify `OPENAI_API_KEY` in `.env` is valid
- Check API key has credits at https://platform.openai.com/usage
- GPT-4 automatically falls back to GPT-3.5-turbo on rate limits

**Import errors**:
- Ensure virtual environment is activated
- Reinstall dependencies: `uv pip install -r requirements.txt`
- Use UV package manager (NOT pip) for this project

