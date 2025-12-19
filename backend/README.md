# Backend - Todo Evolution Phase II

## Setup

1. Install UV package manager (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Create virtual environment:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   uv pip install fastapi uvicorn sqlmodel alembic python-jose passlib httpx pytest pytest-cov pytest-asyncio
   ```

4. Copy .env.example to .env and fill in values:
   ```bash
   cp .env.example .env
   ```

5. Run database migrations:
   ```bash
   alembic upgrade head
   ```

6. Start development server:
   ```bash
   uvicorn src.main:app --reload
   ```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

