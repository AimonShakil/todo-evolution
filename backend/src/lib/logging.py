"""
Structured JSON logging for observability.

Provides consistent logging format across all services with support for:
- JSON structured logging for machine parsing
- Request/response tracing
- Tool call logging
- Error tracking with context
"""

import json
import logging
import sys
from datetime import datetime
from typing import Any, Dict, Optional


class JSONFormatter(logging.Formatter):
    """
    Custom formatter that outputs JSON-structured logs.
    
    Each log entry includes:
    - timestamp: ISO 8601 format
    - level: Log level (INFO, ERROR, etc.)
    - message: Log message
    - extra: Additional context fields
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON string."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields from record
        # These come from logger.info("msg", extra={...})
        for key, value in record.__dict__.items():
            if key not in [
                "name", "msg", "args", "created", "filename", "funcName",
                "levelname", "levelno", "lineno", "module", "msecs",
                "message", "pathname", "process", "processName",
                "relativeCreated", "thread", "threadName", "exc_info",
                "exc_text", "stack_info", "taskName"
            ]:
                log_data[key] = value
        
        return json.dumps(log_data)


def setup_logging(
    logger_name: str = "todo-evolution",
    level: int = logging.INFO,
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Setup structured JSON logging for a service.
    
    Args:
        logger_name: Name of the logger (default: "todo-evolution")
        level: Logging level (default: INFO)
        log_file: Optional file path for log output (default: stdout only)
        
    Returns:
        Configured logger instance
        
    Example:
        >>> logger = setup_logging("agent-service")
        >>> logger.info("Agent invoked", extra={
        ...     "user_id": 123,
        ...     "conversation_id": 456,
        ...     "model": "gpt-4"
        ... })
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    
    # Remove existing handlers to avoid duplicates
    logger.handlers = []
    
    # Console handler with JSON formatting
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(JSONFormatter())
    logger.addHandler(console_handler)
    
    # Optional file handler
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(JSONFormatter())
        logger.addHandler(file_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger


def log_agent_request(
    logger: logging.Logger,
    user_id: int,
    conversation_id: int,
    message: str,
    model: str = "gpt-4"
) -> None:
    """
    Log an agent request with structured context.
    
    Args:
        logger: Logger instance
        user_id: User ID making the request
        conversation_id: Active conversation ID
        message: User's message
        model: AI model to use (default: gpt-4)
    """
    logger.info(
        "Agent request received",
        extra={
            "event_type": "agent_request",
            "user_id": user_id,
            "conversation_id": conversation_id,
            "message_length": len(message),
            "model": model,
        }
    )


def log_agent_response(
    logger: logging.Logger,
    user_id: int,
    conversation_id: int,
    response: str,
    model_used: str,
    tool_calls: Optional[list] = None,
    latency_ms: Optional[float] = None,
    tokens_used: Optional[int] = None,
) -> None:
    """
    Log an agent response with observability metrics.
    
    Args:
        logger: Logger instance
        user_id: User ID
        conversation_id: Conversation ID
        response: Assistant's response
        model_used: Actual model used (may differ from requested due to fallback)
        tool_calls: List of tool calls made (if any)
        latency_ms: Response latency in milliseconds
        tokens_used: Total tokens consumed
    """
    logger.info(
        "Agent response generated",
        extra={
            "event_type": "agent_response",
            "user_id": user_id,
            "conversation_id": conversation_id,
            "response_length": len(response),
            "model_used": model_used,
            "tool_count": len(tool_calls) if tool_calls else 0,
            "tool_calls": tool_calls if tool_calls else [],
            "latency_ms": latency_ms,
            "tokens_used": tokens_used,
        }
    )


def log_tool_call(
    logger: logging.Logger,
    user_id: int,
    conversation_id: int,
    tool_name: str,
    tool_args: Dict[str, Any],
    success: bool,
    error: Optional[str] = None,
) -> None:
    """
    Log a tool call execution.
    
    Args:
        logger: Logger instance
        user_id: User ID
        conversation_id: Conversation ID
        tool_name: Name of the tool called
        tool_args: Tool arguments
        success: Whether the tool call succeeded
        error: Error message if failed
    """
    logger.info(
        f"Tool call: {tool_name}",
        extra={
            "event_type": "tool_call",
            "user_id": user_id,
            "conversation_id": conversation_id,
            "tool_name": tool_name,
            "tool_args": tool_args,
            "success": success,
            "error": error,
        }
    )


def log_error(
    logger: logging.Logger,
    error_type: str,
    error_message: str,
    user_id: Optional[int] = None,
    conversation_id: Optional[int] = None,
    context: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Log an error with full context.
    
    Args:
        logger: Logger instance
        error_type: Type of error (e.g., "ValueError", "OpenAIError")
        error_message: Error message
        user_id: Optional user ID
        conversation_id: Optional conversation ID
        context: Additional error context
    """
    extra = {
        "event_type": "error",
        "error_type": error_type,
        "error_message": error_message,
    }
    
    if user_id:
        extra["user_id"] = user_id
    if conversation_id:
        extra["conversation_id"] = conversation_id
    if context:
        extra["context"] = context
    
    logger.error(f"Error: {error_type} - {error_message}", extra=extra)
