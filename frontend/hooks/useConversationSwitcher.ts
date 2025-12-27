import { useState, useCallback } from "react";

/**
 * Hook for managing conversation switching logic.
 *
 * Handles:
 * - Switching between conversations
 * - Creating new conversations (archives current active one)
 * - Tracking active conversation ID
 */
export function useConversationSwitcher(initialConversationId: number | null = null) {
  const [activeConversationId, setActiveConversationId] = useState<number | null>(
    initialConversationId
  );

  /**
   * Switch to a different conversation.
   * The backend will automatically archive the current active conversation
   * when a new conversation is created.
   */
  const switchConversation = useCallback((conversationId: number) => {
    setActiveConversationId(conversationId);
  }, []);

  /**
   * Create a new conversation.
   * This will archive the current active conversation on the backend
   * when the first message is sent (the backend creates the conversation).
   */
  const createNewConversation = useCallback(() => {
    setActiveConversationId(null);
  }, []);

  /**
   * Set the active conversation ID after a new conversation is created
   * (typically called after the first message is sent and backend returns conversation_id).
   */
  const setConversationId = useCallback((conversationId: number) => {
    setActiveConversationId(conversationId);
  }, []);

  return {
    activeConversationId,
    switchConversation,
    createNewConversation,
    setConversationId,
  };
}
