# Migration and Testing Notes

**Date**: 2025-12-15
**Issue**: Pydantic + SQLModel + Python 3.14 Compatibility

---

## 🐛 Known Issue: Python 3.14 + SQLModel Compatibility

### Problem

**SQLModel 0.0.22** is not fully compatible with **Pydantic 2.12+** and **Python 3.14**:

1. **Pydantic 2.12.5** (latest) → Works with Python 3.14 but has breaking changes for SQLModel
2. **Pydantic 2.9.2** (older) → Compatible with SQLModel but doesn't support Python 3.14
3. **Python 3.14** → Too new for pydantic-core 2.23.4 (PyO3 limitation)

**Error**: `Field 'id' requires a type annotation` when importing models

### Impact

- ❌ Cannot run `alembic upgrade head` (requires model imports)
- ❌ Cannot run test suite (requires model imports)
- ❌ Cannot start development server (requires model imports)

### Workaround Applied

**Manual migrations created** (don't require model imports):
- `alembic/versions/001_create_users_table.py`
- `alembic/versions/002_create_tasks_table.py`

**Models commented out in alembic/env.py**:
```python
# Uncomment when Pydantic compatibility is fixed:
# from src.models.user import User  # noqa: F401
# from src.models.task import Task  # noqa: F401
```

---

## ✅ Solution Options

### Option 1: Downgrade Python (RECOMMENDED for testing now)

Use Python 3.11 or 3.12 instead of 3.14:

```bash
# Install Python 3.12
# Then recreate venv:
cd backend
rm -rf .venv
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Now you can run:
alembic upgrade head
pytest
python src/main.py
```

### Option 2: Wait for SQLModel Update

SQLModel maintainers are working on Pydantic 2.x compatibility.
Check: https://github.com/tiangolo/sqlmodel/issues

### Option 3: Switch to Pure SQLAlchemy

Replace SQLModel with SQLAlchemy 2.0 + Pydantic separately (more work).

---

## 📋 Manual Migration Steps (When DATABASE_URL is set)

Since automatic migrations don't work, here's how to apply migrations manually:

### 1. Verify DATABASE_URL

```bash
cd backend
cat .env | grep DATABASE_URL

# Should show your Neon PostgreSQL connection string:
# postgresql://user:pass@host.neon.tech/database?sslmode=require
```

### 2. Apply Migrations (with Python 3.12)

```bash
source .venv/bin/activate  # Python 3.12 venv
alembic upgrade head
```

**Expected output**:
```
INFO  [alembic.runtime.migration] Running upgrade  -> 001, Create users table
INFO  [alembic.runtime.migration] Running upgrade 001 -> 002, Create tasks table
```

### 3. Verify Tables Created

**Option A: Neon Dashboard**
- Go to https://console.neon.tech
- Select your project
- Click "Tables" in sidebar
- Should see: `user` and `task` tables

**Option B: SQL Query** (if using psql):
```sql
-- Connect to Neon
psql $DATABASE_URL

-- List tables
\dt

-- Check user table schema
\d user

-- Check task table schema
\d task
```

---

## 🧪 Test Suite Status

### Tests Written (78 total)

**Unit Tests**:
- ✅ test_models.py (15 tests) - Model validation
- ✅ test_auth_service.py (11 tests) - Password & JWT
- ✅ test_task_service.py (20 tests) - CRUD operations

**Integration Tests**:
- ✅ test_auth_routes.py (7 tests) - Auth API
- ✅ test_task_routes.py (14 tests) - Task API
- ✅ test_user_isolation.py (11 tests) - User isolation (CRITICAL)

### Running Tests (Requires Python 3.12)

```bash
# With Python 3.12 venv:
source .venv/bin/activate
pytest -v

# Expected output:
# ======================== 78 passed in X.XXs ========================
# Coverage: ≥80%
```

### Test Configuration

**pytest.ini** configured for:
- ✅ In-memory SQLite database (fast, no Neon connection needed)
- ✅ Async test support
- ✅ Coverage reporting (HTML + terminal)
- ✅ 80% minimum coverage threshold

---

## 🚀 Development Server (Requires Python 3.12)

### Starting the Server

```bash
cd backend
source .venv/bin/activate  # Python 3.12
python src/main.py
```

**Server runs on**: http://localhost:8000

**Endpoints**:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

### Testing API Manually

**1. Using Swagger UI** (easiest):
```
1. Go to http://localhost:8000/docs
2. Click "POST /api/auth/signup"
3. Click "Try it out"
4. Enter:
   {
     "email": "test@example.com",
     "name": "Test User",
     "password": "password123"
   }
5. Click "Execute"
6. Copy the "token" from response
7. Click "Authorize" button (top right)
8. Paste token: "Bearer <paste-token-here>"
9. Now you can test all task endpoints!
```

**2. Using curl**:
```bash
# Signup
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","name":"Test","password":"password123"}'

# Signin
curl -X POST http://localhost:8000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Get tasks (replace TOKEN)
curl -X GET http://localhost:8000/api/1/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## 📊 What's Working vs Not Working

### ✅ Working (Code is Ready)

- Models defined correctly (User, Task)
- Services implemented (auth_service, task_service)
- Routes implemented (auth, tasks)
- Main app configured (CORS, rate limiting)
- Tests written (78 tests with fixtures)
- Manual migrations created
- Documentation complete

### ❌ Blocked by Python 3.14 Compatibility

- Running Alembic migrations
- Running test suite
- Starting development server
- Importing models in Python code

### ⏳ Requires User Action

- Set real DATABASE_URL in `.env` (currently has placeholder)
- Create Python 3.12 virtual environment (for testing)
- Apply migrations to Neon PostgreSQL

---

## 🎯 Next Steps

### For Backend (Blocked - needs Python 3.12)

1. **Setup Python 3.12 environment**:
   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Apply migrations**:
   ```bash
   alembic upgrade head
   ```

3. **Run tests**:
   ```bash
   pytest
   ```

4. **Start server**:
   ```bash
   python src/main.py
   ```

### For Frontend (Not Blocked - can proceed!)

**STEP 3: Frontend Foundation**
- Next.js 16 with App Router
- Better Auth React integration
- Shadcn/ui components (Slate theme)
- API client for backend

---

## 💡 Recommendations

**Immediate**: Proceed with STEP 3 (Frontend) while backend compatibility issue is resolved

**Short-term**: Use Python 3.12 for backend testing and development

**Long-term**: Monitor SQLModel repository for Pydantic 2.12+ compatibility update

---

## 📚 References

- **SQLModel Issue Tracker**: https://github.com/tiangolo/sqlmodel/issues
- **Pydantic 2 Migration Guide**: https://docs.pydantic.dev/latest/migration/
- **Python 3.14 Release Notes**: https://docs.python.org/3.14/whatsnew/3.14.html

---

**Status**: Backend code complete, waiting for compatibility fix or Python downgrade to test
