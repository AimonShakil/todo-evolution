"""
Chat routes for Phase III - Agentic AI Chatbot.

This module provides the chat endpoint for natural language task management.

Constitutional Alignment:
- Principle II: User Data Isolation (all endpoints verify JWT user matches {user_id})
- Principle III: Stateless Architecture (conversation state from DB)
- Principle XIV: Authentication & Authorization (JWT token required)
- Principle XVI: Error Handling (graceful degradation, user-friendly messages)
- Principle XXVI: Agent Orchestration (OpenAI integration)
"""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.lib.database import get_session
from src.services.agent_service import AgentService
from src.services.auth_service import get_user_id_from_token
from src.services.conversation_service import (
    create_conversation,
    get_active_conversation,
)
from src.services.message_service import create_message, get_conversation_messages

router = APIRouter(prefix="", tags=["Chat"])
security = HTTPBearer()


# Request/Response models (T027)
class ChatRequest(BaseModel):
    """Chat message request."""

    message: str = Field(
        ...,
        min_length=1,
        max_length=4000,
        description="User's message (1-4000 characters)",
    )


class ChatResponse(BaseModel):
    """Chat message response."""

    success: bool
    response: str
    conversation_id: int
    tool_calls: list[dict[str, Any]] = Field(default_factory=list)
    model_used: str | None = None
    is_ambiguous: bool = False
    intent_unclear: bool = False


# Dependency: Get current user from JWT token (T026)
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> int:
    """
    Extract and validate JWT token, return user_id.

    Constitutional Principle XIV: Authentication required for chat endpoint.

    Args:
        credentials: HTTP Bearer token from Authorization header

    Returns:
        User ID from JWT token

    Raises:
        HTTPException 401: Invalid or missing token
    """
    token = credentials.credentials
    user_id = get_user_id_from_token(token)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    return user_id


# Dependency: Verify JWT user matches URL user_id (T026)
async def verify_user_access(
    user_id: int, current_user: int = Depends(get_current_user)
) -> int:
    """
    Verify that JWT user matches URL {user_id} parameter.

    Constitutional Principle II: User Data Isolation enforcement.

    Args:
        user_id: User ID from URL path parameter
        current_user: User ID from JWT token

    Returns:
        User ID if authorized

    Raises:
        HTTPException 403: User ID mismatch (trying to access another user's data)
    """
    if current_user != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access another user's chat",
        )
    return current_user


# Chat endpoint (T025, T028-T031)
@router.post("/{user_id}/chat", response_model=ChatResponse)
async def send_chat_message(
    user_id: int,
    request: ChatRequest,
    verified_user: int = Depends(verify_user_access),
    session: AsyncSession = Depends(get_session),
) -> ChatResponse:
    """
    Send a chat message and receive AI response with tool execution.

    This endpoint orchestrates the full conversation flow:
    1. Find or create active conversation (T028)
    2. Persist user message (T030)
    3. Reconstruct context and invoke agent (T029)
    4. Persist assistant response (T030)
    5. Handle errors gracefully (T031)

    Constitutional Principles:
    - Principle II: User isolation (user_id verified)
    - Principle III: Stateless (conversation from DB)
    - Principle XXVI: Agent orchestration

    Args:
        user_id: User ID from URL (verified against JWT)
        request: Chat message request with user's input
        verified_user: User ID after JWT verification
        session: Database session

    Returns:
        ChatResponse with agent's reply and metadata

    Raises:
        HTTPException 400: Invalid request (message too long)
        HTTPException 500: Agent service error
    """
    try:
        # T028: Conversation lifecycle - find or create active conversation
        conversation = await get_active_conversation(
            session=session, user_id=user_id
        )

        if not conversation:
            # Create new conversation if none exists
            conversation = await create_conversation(session=session, user_id=user_id)

        # T030: Message persistence - save user message
        user_message = await create_message(
            session=session,
            conversation_id=conversation.id,
            user_id=user_id,
            role="user",
            content=request.message,
        )

        # T029: Agent invocation - initialize agent service
        agent_service = AgentService()

        # Reconstruct conversation context (last 50 messages per ADR-006)
        conversation_context = await agent_service.get_conversation_context(
            session=session,
            conversation_id=conversation.id,
            user_id=user_id,
            limit=50,
        )

        # Invoke agent with context and tools
        agent_result = await agent_service.invoke_agent(
            session=session,
            user_id=user_id,
            user_message=request.message,
            conversation_context=conversation_context,
        )

        # T031: Error handling - check if agent invocation succeeded
        if not agent_result["success"]:
            # Agent failed (API error, etc.)
            error_response = agent_result.get(
                "response",
                "I'm having trouble connecting to the AI service. Please try again.",
            )

            # Still save the error as an assistant message for audit trail
            await create_message(
                session=session,
                conversation_id=conversation.id,
                user_id=user_id,
                role="assistant",
                content=error_response,
            )

            return ChatResponse(
                success=False,
                response=error_response,
                conversation_id=conversation.id,
                tool_calls=[],
                model_used=None,
            )

        # T030: Message persistence - save assistant response
        assistant_message = await create_message(
            session=session,
            conversation_id=conversation.id,
            user_id=user_id,
            role="assistant",
            content=agent_result["response"],
        )

        # Return successful response with agent output
        return ChatResponse(
            success=True,
            response=agent_result["response"],
            conversation_id=conversation.id,
            tool_calls=agent_result.get("tool_calls", []),
            model_used=agent_result.get("model_used"),
            is_ambiguous=agent_result.get("is_ambiguous", False),
            intent_unclear=agent_result.get("intent_unclear", False),
        )

    except ValueError as e:
        # T031: Handle validation errors (from Pydantic or service layer)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    except Exception as e:
        # T031: Handle unexpected errors gracefully
        # Log error for debugging but return user-friendly message
        error_message = (
            "An unexpected error occurred. Please try again in a moment."
        )

        # Try to save error message to conversation for audit
        try:
            if conversation:
                await create_message(
                    session=session,
                    conversation_id=conversation.id,
                    user_id=user_id,
                    role="assistant",
                    content=error_message,
                )
        except:
            pass  # Don't fail on error logging

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_message,
        )
