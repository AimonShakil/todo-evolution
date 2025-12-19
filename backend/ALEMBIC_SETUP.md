# Alembic Setup Guide

**Status**: STEP 0.7 Complete
**Date**: 2025-12-15
**Branch**: 003-phase-ii-web-app

---

## Overview

Alembic is configured for **async PostgreSQL migrations** using **asyncpg** driver and **SQLModel** metadata.

---

## Configuration Summary

### 1. Dependencies Installed

```bash
# Core dependencies installed via requirements.txt
alembic==1.14.0
asyncpg==0.30.0  # Async PostgreSQL driver
sqlmodel==0.0.22
python-dotenv==1.2.1  # Load .env file
```

### 2. Alembic Initialization

```bash
# Initialized with:
alembic init alembic

# Created files:
# - alembic.ini (configuration file)
# - alembic/env.py (migration environment)
# - alembic/versions/ (migration files directory)
```

### 3. alembic.ini Configuration

**Key changes**:
- **DATABASE_URL**: Read from environment variable (.env file) instead of hardcoded
- **Comment out** default `sqlalchemy.url` line

```ini
# sqlalchemy.url = driver://user:pass@localhost/dbname
# DATABASE_URL is read from environment variable (.env file) in alembic/env.py
```

### 4. alembic/env.py Configuration

**Key features**:
- ✅ **Async PostgreSQL support** (asyncpg driver)
- ✅ **Environment variable loading** (python-dotenv)
- ✅ **SQLModel metadata import** (for autogenerate)
- ✅ **URL conversion**: `postgresql://` → `postgresql+asyncpg://`
- ✅ **SSL parameter conversion**: `sslmode=require` → `ssl=true` (asyncpg format)

**Code highlights**:
```python
# Load .env file
from dotenv import load_dotenv
load_dotenv()

# Read DATABASE_URL from environment
database_url = os.getenv("DATABASE_URL")

# Convert to asyncpg format
if database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)

# Convert SSL parameter for asyncpg
if "sslmode=require" in database_url:
    database_url = database_url.replace("sslmode=require", "ssl=true")

# Import SQLModel metadata
from sqlmodel import SQLModel
target_metadata = SQLModel.metadata
```

---

## Common Alembic Commands

### 1. Check Current Revision

```bash
source .venv/bin/activate
alembic current
```

**Expected output** (before first migration):
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
```

### 2. Create a New Migration

**Auto-generate migration** (compares SQLModel models to database):
```bash
alembic revision --autogenerate -m "Create users and tasks tables"
```

**Manual migration** (empty template):
```bash
alembic revision -m "Migration description"
```

**Output**: Creates file like `alembic/versions/abc123_create_users_and_tasks_tables.py`

### 3. Apply Migrations (Upgrade)

```bash
# Apply all pending migrations
alembic upgrade head

# Apply specific revision
alembic upgrade abc123

# Apply next N migrations
alembic upgrade +2
```

### 4. Rollback Migrations (Downgrade)

```bash
# Rollback all migrations
alembic downgrade base

# Rollback to specific revision
alembic downgrade abc123

# Rollback by N revisions
alembic downgrade -1
```

### 5. View Migration History

```bash
# Show current revision
alembic current

# Show all revisions
alembic history

# Show detailed history with file paths
alembic history --verbose
```

---

## Migration Workflow Example

### Step 1: Create SQLModel Models

```bash
# Create models in src/models/
backend/src/models/
├── user.py    # User entity
└── task.py    # Task entity
```

### Step 2: Import Models in env.py

```python
# Uncomment these lines in alembic/env.py after creating models
from src.models.user import User
from src.models.task import Task
```

### Step 3: Generate Migration

```bash
source .venv/bin/activate
alembic revision --autogenerate -m "Create users and tasks tables"
```

### Step 4: Review Migration File

```bash
# Open generated file
cat alembic/versions/001_create_users_and_tasks_tables.py

# Verify:
# - Creates 'users' table with correct columns
# - Creates 'tasks' table with foreign key to users
# - Creates indexes (idx_users_email, idx_tasks_user_id)
```

### Step 5: Apply Migration

```bash
alembic upgrade head
```

**Expected output**:
```
INFO  [alembic.runtime.migration] Running upgrade  -> 001, Create users and tasks tables
```

### Step 6: Verify in Database

```sql
-- Connect to Neon PostgreSQL
psql $DATABASE_URL

-- Check tables
\dt

-- Check users table schema
\d users

-- Check tasks table schema
\d tasks

-- Verify foreign key constraint
SELECT conname, conrelid::regclass, confrelid::regclass
FROM pg_constraint
WHERE contype = 'f';
```

---

## Troubleshooting

### Issue: `TypeError: connect() got an unexpected keyword argument 'sslmode'`

**Cause**: Asyncpg doesn't support `sslmode` parameter (psycopg2 syntax)

**Solution**: Alembic env.py auto-converts `sslmode=require` → `ssl=true` ✅

### Issue: `ModuleNotFoundError: No module named 'src'`

**Cause**: Alembic can't find src modules

**Solution**: env.py adds parent directory to sys.path ✅

```python
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
```

### Issue: `alembic: command not found`

**Cause**: Virtual environment not activated

**Solution**:
```bash
source .venv/bin/activate
```

### Issue: Migration fails with "relation already exists"

**Cause**: Manual schema changes or duplicate migrations

**Solution**:
```bash
# Drop all tables (CAUTION: loses data)
alembic downgrade base

# Re-apply migrations
alembic upgrade head
```

### Issue: DATABASE_URL not found

**Cause**: .env file not loaded or DATABASE_URL not set

**Solution**:
```bash
# Verify .env file exists
cat backend/.env | grep DATABASE_URL

# Should show:
# DATABASE_URL=postgresql://user:pass@host/database?sslmode=require
```

---

## Phase II Migration Files (STEP 1)

When models are created in STEP 1, generate two migrations:

### Migration 001: Create Users Table

```python
# alembic/versions/001_create_users_table.py
def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('NOW()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index('idx_users_email', 'users', ['email'], unique=True)
```

### Migration 002: Create Tasks Table

```python
# alembic/versions/002_create_tasks_table.py
def upgrade() -> None:
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('completed', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('NOW()'), nullable=False),
        # Phase V fields (nullable)
        sa.Column('priority', sa.String(length=10), nullable=True),
        sa.Column('tags', sa.Text(), nullable=True),
        sa.Column('due_date', sa.DateTime(), nullable=True),
        sa.Column('recurrence_pattern', sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )
    op.create_index('idx_tasks_user_id', 'tasks', ['user_id'])
```

---

## Best Practices

1. **Always review auto-generated migrations** before applying
   - Check column types match models
   - Verify foreign keys and indexes
   - Review upgrade AND downgrade functions

2. **Test migrations in development first**
   ```bash
   # Upgrade
   alembic upgrade head

   # Verify tables exist
   psql $DATABASE_URL -c '\dt'

   # Rollback to test downgrade
   alembic downgrade -1

   # Re-apply
   alembic upgrade head
   ```

3. **Never edit applied migrations**
   - Create a new migration to fix issues
   - Use `alembic revision -m "Fix issue"` instead

4. **Commit migration files to git**
   ```bash
   git add alembic/versions/*.py
   git commit -m "feat: add users and tasks migrations"
   ```

---

## Next Steps

After STEP 0.7 (Alembic Setup):
1. **STEP 1**: Backend Foundation (create models, generate migrations, apply to Neon)
2. **STEP 2**: Backend Testing (verify migrations work, test user isolation)
3. **STEP 3**: Frontend Foundation (Next.js 16 setup)

---

**Alembic Setup Complete** ✅
