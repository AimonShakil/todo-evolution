"""
Main FastAPI application for Phase II Web App.

This module initializes the FastAPI app with middleware, routes, and lifecycle events.

Constitutional Alignment:
- Principle III: Authentication & Authorization (JWT-protected endpoints)
- Principle XV: API Rate Limiting (100 requests/minute per user)
- Principle XVI: Error Handling (user-friendly error messages)
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from src.lib.database import init_db, close_db
from src.routes import auth, tasks
from src.routes.tasks import router as task_router
from src.routes.tasks import router as tasks_router
# Create FastAPI app
app = FastAPI(
    title="Todo Evolution - Phase II API",
    description="Task management API with JWT authentication and user isolation",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware (allow Next.js frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev server
	"http://localhost:3002",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting (Constitutional Principle XV)
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Register routers
app.include_router(auth.router)
app.include_router(tasks_router, prefix="/api")


# Startup event
@app.on_event("startup")
async def on_startup():
    """
    Initialize database on application startup.

    Note: In production, use Alembic migrations instead of init_db().
    """
    # Uncomment for development to auto-create tables
    # await init_db()
    pass


# Shutdown event
@app.on_event("shutdown")
async def on_shutdown():
    """Close database connections on application shutdown."""
    await close_db()


# Health check endpoint
@app.get("/health", tags=["Health"])
@limiter.exempt  # No rate limit on health check
async def health_check() -> dict:
    """
    Health check endpoint.

    Returns:
        Status message

    Example:
        GET /health

        Response 200:
        {
            "status": "healthy",
            "version": "2.0.0"
        }
    """
    return {"status": "healthy", "version": "2.0.0"}


# Root endpoint
@app.get("/", tags=["Root"])
async def root() -> dict:
    """
    API root endpoint.

    Returns:
        Welcome message with links

    Example:
        GET /

        Response 200:
        {
            "message": "Todo Evolution API - Phase II",
            "docs": "/docs",
            "health": "/health"
        }
    """
    return {
        "message": "Todo Evolution API - Phase II",
        "docs": "/docs",
        "health": "/health",
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Handle unexpected errors gracefully.

    Constitutional Principle XVI: User-friendly error messages.

    Args:
        request: HTTP request
        exc: Exception that occurred

    Returns:
        JSON error response
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An unexpected error occurred. Please try again later.",
            "type": "internal_server_error",
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes (development only)
    )
