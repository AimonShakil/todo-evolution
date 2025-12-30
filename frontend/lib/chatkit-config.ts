/**
 * ChatKit configuration for Phase III AI Chat Interface
 *
 * Task: T033 [US1] Create ChatKit configuration
 * Spec: specs/004-phase-iii-ai-chatbot/spec.md
 *
 * This module provides configuration constants and helper functions for the chat interface.
 */

/**
 * Chat configuration constants
 */
export const CHAT_CONFIG = {
  /**
   * Maximum message length (matches backend validation)
   * Backend constraint: 1-4000 characters (Pydantic Field validation)
   */
  MAX_MESSAGE_LENGTH: 4000,

  /**
   * Minimum message length
   */
  MIN_MESSAGE_LENGTH: 1,

  /**
   * Placeholder text for chat input
   */
  INPUT_PLACEHOLDER: "Ask me to create tasks, list todos, or manage your tasks...",

  /**
   * Welcome message shown on new conversations
   */
  WELCOME_MESSAGE:
    "Hello! I'm your AI task assistant. You can ask me to create tasks, list your todos, mark tasks as complete, or manage your tasks using natural language. Try saying something like 'Create a task to buy groceries tomorrow' or 'Show me my incomplete tasks'.",

  /**
   * Error messages
   */
  ERRORS: {
    MESSAGE_TOO_LONG: `Message must be less than 4000 characters`,
    MESSAGE_TOO_SHORT: "Message cannot be empty",
    NETWORK_ERROR: "Failed to send message. Please check your connection and try again.",
    AUTH_ERROR: "Your session has expired. Please sign in again.",
  },

  /**
   * System message prefixes for different response types
   */
  RESPONSE_TYPES: {
    TASK_CREATED: "✅ Task created:",
    TASK_UPDATED: "📝 Task updated:",
    TASK_COMPLETED: "✓ Task completed:",
    TASK_DELETED: "🗑️ Task deleted:",
    TASK_LIST: "📋 Your tasks:",
    ERROR: "❌ Error:",
    INFO: "ℹ️",
  },
} as const;

/**
 * Format a chat message for display
 */
export interface ChatMessage {
  id?: number;
  role: "user" | "assistant" | "system";
  content: string;
  created_at?: string;
  tool_calls?: Array<{
    tool: string;
    arguments: Record<string, any>;
    result: Record<string, any>;
  }>;
}

/**
 * Validate message length
 */
export function validateMessageLength(message: string): {
  valid: boolean;
  error?: string;
} {
  const trimmed = message.trim();

  if (trimmed.length < CHAT_CONFIG.MIN_MESSAGE_LENGTH) {
    return {
      valid: false,
      error: CHAT_CONFIG.ERRORS.MESSAGE_TOO_SHORT,
    };
  }

  if (trimmed.length > CHAT_CONFIG.MAX_MESSAGE_LENGTH) {
    return {
      valid: false,
      error: CHAT_CONFIG.ERRORS.MESSAGE_TOO_LONG,
    };
  }

  return { valid: true };
}

/**
 * Format tool calls for display
 */
export function formatToolCalls(
  toolCalls: Array<{
    tool: string;
    arguments: Record<string, any>;
    result: Record<string, any>;
  }>
): string {
  if (toolCalls.length === 0) return "";

  const formatted = toolCalls
    .map((call) => {
      const { tool, result } = call;
      if (result.success && result.message) {
        return result.message;
      }
      return `Executed: ${tool}`;
    })
    .join("\n");

  return formatted;
}

/**
 * Extract error message from API response
 */
export function extractErrorMessage(error: any): string {
  if (typeof error === "string") return error;
  if (error?.detail) return error.detail;
  if (error?.message) return error.message;
  return CHAT_CONFIG.ERRORS.NETWORK_ERROR;
}
