"use client";

import { useEffect, useState } from "react";
import { Conversation, chatApi } from "@/lib/api-client";

interface ConversationListProps {
  userId: number;
  token: string;
  activeConversationId: number | null;
  onConversationSelect: (conversationId: number) => void;
  onNewConversation: () => void;
}

export default function ConversationList({
  userId,
  token,
  activeConversationId,
  onConversationSelect,
  onNewConversation,
}: ConversationListProps) {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch conversations on mount and when activeConversationId changes
  useEffect(() => {
    async function fetchConversations() {
      try {
        setLoading(true);
        const data = await chatApi.getConversations(userId, token);
        setConversations(data);
        setError(null);
      } catch (err) {
        console.error("Failed to fetch conversations:", err);
        setError("Failed to load conversations");
      } finally {
        setLoading(false);
      }
    }

    fetchConversations();
  }, [userId, token, activeConversationId]);

  // Format date for display
  function formatDate(dateString: string): string {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return "Just now";
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    return date.toLocaleDateString();
  }

  return (
    <div className="w-64 bg-muted/30 border-r h-full flex flex-col">
      {/* Header */}
      <div className="p-4 border-b">
        <h2 className="text-lg font-semibold mb-3">Conversations</h2>
        <button
          onClick={onNewConversation}
          className="w-full px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors text-sm font-medium"
        >
          + New Conversation
        </button>
      </div>

      {/* Conversation List */}
      <div className="flex-1 overflow-y-auto">
        {loading && (
          <div className="p-4 text-center text-sm text-muted-foreground">
            Loading conversations...
          </div>
        )}

        {error && (
          <div className="p-4 text-center text-sm text-destructive">
            {error}
          </div>
        )}

        {!loading && !error && conversations.length === 0 && (
          <div className="p-4 text-center text-sm text-muted-foreground">
            No conversations yet.
            <br />
            Start a new one!
          </div>
        )}

        {!loading && !error && conversations.length > 0 && (
          <div className="divide-y">
            {conversations.map((conversation) => (
              <button
                key={conversation.id}
                onClick={() => onConversationSelect(conversation.id)}
                className={`w-full px-4 py-3 text-left hover:bg-accent transition-colors ${
                  conversation.id === activeConversationId
                    ? "bg-accent border-l-4 border-primary"
                    : ""
                }`}
              >
                <div className="flex items-start justify-between mb-1">
                  <span className="text-sm font-medium">
                    Conversation #{conversation.id}
                  </span>
                  {conversation.is_active && (
                    <span className="ml-2 px-2 py-0.5 bg-green-100 text-green-700 text-xs rounded-full">
                      Active
                    </span>
                  )}
                </div>
                <div className="flex items-center justify-between text-xs text-muted-foreground">
                  <span>{conversation.message_count} messages</span>
                  <span>{formatDate(conversation.updated_at)}</span>
                </div>
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
