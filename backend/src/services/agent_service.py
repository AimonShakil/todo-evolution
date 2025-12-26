"""
Agent service for Phase III - Agentic AI Chatbot.

This module orchestrates OpenAI agent interactions, including context reconstruction,
tool registration, model fallback, and intent determination.

Constitutional Alignment:
- Principle II: User Data Isolation (all operations scoped to user_id)
- Principle III: Stateless Architecture (context reconstructed from DB each request)
- Principle IX: Code Quality Standards (type hints, docstrings, error handling)
- Principle XXVI: Agent Orchestration (OpenAI Agents SDK integration)

ADR References:
- ADR-006: Agent Context Reconstruction (last 50 messages)
- ADR-007: Model Fallback (GPT-4 → GPT-3.5-turbo on rate limits)
"""

import json
import os
from typing import Any, Optional

import openai
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from src.mcp.server import execute_tool, get_tool_schemas
from src.services.message_service import get_conversation_messages


class AgentService:
    """
    Orchestrates AI agent interactions with OpenAI SDK.

    Responsibilities:
    - Context reconstruction from message history (T020, ADR-006)
    - Agent invocation with tool registration (T021)
    - Model fallback logic (T022, ADR-007)
    - Ambiguous intent detection (T023)
    - Intent determination (T024)
    """

    def __init__(self):
        """
        Initialize AgentService with OpenAI client.

        Raises:
            ValueError: If OPENAI_API_KEY environment variable not set
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable not set. "
                "Get your API key from https://platform.openai.com/api-keys"
            )

        self.client = AsyncOpenAI(api_key=api_key)
        self.primary_model = "gpt-4"  # Primary model per ADR-007
        self.fallback_model = "gpt-3.5-turbo"  # Fallback per ADR-007

    async def get_conversation_context(
        self,
        session: AsyncSession,
        conversation_id: int,
        user_id: int,
        limit: int = 50,
    ) -> list[dict[str, str]]:
        """
        Reconstruct conversation context from database (T020, ADR-006).

        Fetches last N messages in chronological order for OpenAI API.

        Args:
            session: Async database session
            conversation_id: Conversation ID to fetch messages from
            user_id: User ID (owner filter, data isolation)
            limit: Maximum number of messages to fetch (default: 50 per ADR-006)

        Returns:
            List of message dicts in OpenAI format:
            [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]

        Example:
            >>> context = await agent_service.get_conversation_context(
            ...     session, conversation_id=1, user_id=1, limit=50
            ... )
            >>> len(context) <= 50
            True
            >>> context[0]["role"] in ["user", "assistant", "tool"]
            True
        """
        # Fetch last N messages using MessageService (ADR-006)
        messages = await get_conversation_messages(
            session=session,
            conversation_id=conversation_id,
            user_id=user_id,
            limit=limit,
        )

        # Convert to OpenAI message format
        context = [
            {
                "role": msg.role,  # "user", "assistant", or "tool"
                "content": msg.content,
            }
            for msg in messages
        ]

        return context

    async def invoke_agent(
        self,
        session: AsyncSession,
        user_id: int,
        user_message: str,
        conversation_context: list[dict[str, str]],
    ) -> dict[str, Any]:
        """
        Invoke OpenAI agent with tools and context (T021-T024).

        Handles:
        - Tool registration (T021)
        - Model fallback (T022, ADR-007)
        - Ambiguous intent detection (T023)
        - Intent determination (T024)

        Args:
            session: Async database session
            user_id: User ID for tool execution (data isolation)
            user_message: Current user input
            conversation_context: Previous messages from get_conversation_context()

        Returns:
            Dict with:
            - success: bool
            - response: str (agent's response text)
            - tool_calls: list[dict] (tools executed, for audit trail)
            - model_used: str (which model responded - for observability)

        Example:
            >>> result = await agent_service.invoke_agent(
            ...     session,
            ...     user_id=1,
            ...     user_message="Add task: Buy milk",
            ...     conversation_context=[]
            ... )
            >>> result["success"]
            True
            >>> "milk" in result["response"].lower()
            True
        """
        # Build messages array: context + new user message
        messages = conversation_context + [
            {"role": "user", "content": user_message}
        ]

        # Get tool schemas from MCP server (T021)
        tools = get_tool_schemas()

        # Try primary model (GPT-4) first per ADR-007
        model_used = self.primary_model
        try:
            response = await self._call_openai_agent(
                messages=messages,
                tools=tools,
                model=self.primary_model,
            )

        except openai.RateLimitError as e:
            # Fallback to GPT-3.5-turbo on rate limit (T022, ADR-007)
            model_used = self.fallback_model
            response = await self._call_openai_agent(
                messages=messages,
                tools=tools,
                model=self.fallback_model,
            )

        except openai.APIError as e:
            # Handle API errors gracefully (T022, ADR-007)
            return {
                "success": False,
                "response": "AI assistant temporarily unavailable. Please try again in a moment.",
                "tool_calls": [],
                "model_used": None,
                "error": str(e),
            }

        # Extract response and tool calls
        agent_message = response.choices[0].message
        response_text = agent_message.content or ""
        tool_calls_executed = []

        # Execute tool calls if agent requested them (T021)
        if agent_message.tool_calls:
            for tool_call in agent_message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)  # Parse JSON args (secure)

                # Execute tool via MCP server
                tool_result = await execute_tool(
                    tool_name=tool_name,
                    session=session,
                    user_id=user_id,
                    **tool_args,
                )

                tool_calls_executed.append(
                    {
                        "tool": tool_name,
                        "arguments": tool_args,
                        "result": tool_result,
                    }
                )

        # Detect ambiguous intent (T023, Edge Case 1)
        is_ambiguous = self._detect_ambiguous_intent(response_text)

        # Detect inability to determine intent (T024, Edge Case 2)
        intent_unclear = self._detect_unclear_intent(response_text)

        return {
            "success": True,
            "response": response_text,
            "tool_calls": tool_calls_executed,
            "model_used": model_used,
            "is_ambiguous": is_ambiguous,
            "intent_unclear": intent_unclear,
        }

    async def _call_openai_agent(
        self,
        messages: list[dict[str, str]],
        tools: list[dict[str, Any]],
        model: str,
    ) -> Any:
        """
        Call OpenAI Chat Completion API with tools.

        Args:
            messages: Conversation history + current message
            tools: Tool schemas from MCP server
            model: Model to use (gpt-4 or gpt-3.5-turbo)

        Returns:
            OpenAI ChatCompletion response object
        """
        response = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools if tools else None,
            tool_choice="auto",  # Let agent decide when to use tools
        )
        return response

    def _detect_ambiguous_intent(self, response_text: str) -> bool:
        """
        Detect if agent response indicates ambiguous user intent (T023).

        Edge Case 1: User types "milk" - unclear if task creation or search.

        Args:
            response_text: Agent's response text

        Returns:
            True if agent detected ambiguity and asked for clarification

        Example:
            >>> agent_service._detect_ambiguous_intent(
            ...     "I'm not sure if you want to create a task or search. Could you clarify?"
            ... )
            True
        """
        ambiguous_phrases = [
            "not sure",
            "unclear",
            "could you clarify",
            "do you mean",
            "did you want to",
            "which one",
            "can you be more specific",
        ]

        response_lower = response_text.lower()
        return any(phrase in response_lower for phrase in ambiguous_phrases)

    def _detect_unclear_intent(self, response_text: str) -> bool:
        """
        Detect if agent couldn't determine user intent at all (T024).

        Edge Case 2: User input completely unclear (e.g., "asdfgh", "??").

        Args:
            response_text: Agent's response text

        Returns:
            True if agent couldn't understand the request

        Example:
            >>> agent_service._detect_unclear_intent(
            ...     "I don't understand what you're asking for. Could you rephrase?"
            ... )
            True
        """
        unclear_phrases = [
            "don't understand",
            "didn't understand",
            "couldn't understand",
            "not clear",
            "doesn't make sense",
            "could you rephrase",
            "can you rephrase",
            "what do you mean",
        ]

        response_lower = response_text.lower()
        return any(phrase in response_lower for phrase in unclear_phrases)
