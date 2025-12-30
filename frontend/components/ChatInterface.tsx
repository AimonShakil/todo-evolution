"use client";

/**
 * ChatInterface Component - Phase III AI Chat
 *
 * Task: T035 [US1] Create ChatInterface component wrapping chat functionality
 * Spec: specs/004-phase-iii-ai-chatbot/spec.md
 *
 * Main chat interface for natural language task management.
 * Constitutional Principle II: User Data Isolation enforced via JWT.
 */

import { useEffect, useState, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { chatApi } from "@/lib/api-client";
import {
  CHAT_CONFIG,
  validateMessageLength,
  formatToolCalls,
  extractErrorMessage,
  type ChatMessage,
} from "@/lib/chatkit-config";

interface ChatInterfaceProps {
  userId: number;
  token: string;
  userName?: string;
  activeConversationId?: number | null;
  onConversationChange?: (conversationId: number) => void;
}

export default function ChatInterface({
  userId,
  token,
  userName = "User",
  activeConversationId = null,
  onConversationChange,
}: ChatInterfaceProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [conversationId, setConversationId] = useState<number | null>(activeConversationId);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Add welcome message on mount or when conversation changes
  useEffect(() => {
    setMessages([
      {
        role: "assistant",
        content: CHAT_CONFIG.WELCOME_MESSAGE,
        created_at: new Date().toISOString(),
      },
    ]);
  }, [activeConversationId]);

  // Update local conversation ID when prop changes (conversation switch)
  useEffect(() => {
    setConversationId(activeConversationId);
  }, [activeConversationId]);

  const handleSendMessage = async () => {
    if (loading) return;

    // Validate message
    const validation = validateMessageLength(inputMessage);
    if (!validation.valid) {
      setError(validation.error || "Invalid message");
      return;
    }

    const userMessage: ChatMessage = {
      role: "user",
      content: inputMessage.trim(),
      created_at: new Date().toISOString(),
    };

    // Add user message to UI immediately
    setMessages((prev) => [...prev, userMessage]);
    setInputMessage("");
    setError("");
    setLoading(true);

    try {
      // Send message to backend
      const response = await chatApi.sendMessage(
        userId,
        { message: userMessage.content },
        token
      );

      // Update conversation ID if first message
      if (!conversationId && response.conversation_id) {
        setConversationId(response.conversation_id);
        onConversationChange?.(response.conversation_id);
      }

      // Format assistant response
      let assistantContent = response.response;

      // Append tool call results if any
      if (response.tool_calls && response.tool_calls.length > 0) {
        const toolResults = formatToolCalls(response.tool_calls);
        if (toolResults) {
          assistantContent = `${assistantContent}\n\n${toolResults}`;
        }
      }

      const assistantMessage: ChatMessage = {
        role: "assistant",
        content: assistantContent,
        created_at: new Date().toISOString(),
        tool_calls: response.tool_calls,
      };

      setMessages((prev) => [...prev, assistantMessage]);

      // Show warning if intent unclear or ambiguous
      if (response.is_ambiguous || response.intent_unclear) {
        setError(
          "⚠️ I might have misunderstood your request. Please clarify if needed."
        );
      }
    } catch (err: any) {
      const errorMessage = extractErrorMessage(err);
      setError(errorMessage);

      // Add error message to chat for context
      const errorChatMessage: ChatMessage = {
        role: "assistant",
        content: `${CHAT_CONFIG.RESPONSE_TYPES.ERROR} ${errorMessage}`,
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorChatMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <Card className="flex flex-col h-[calc(100vh-12rem)] max-w-4xl mx-auto">
      <CardHeader className="border-b shrink-0">
        <CardTitle className="flex items-center justify-between">
          <span>AI Task Assistant</span>
          <span className="text-sm font-normal text-muted-foreground">
            {userName}
          </span>
        </CardTitle>
      </CardHeader>

      <CardContent className="flex-1 flex flex-col p-0">
        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${
                message.role === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`max-w-[80%] rounded-lg px-4 py-2 ${
                  message.role === "user"
                    ? "bg-primary text-primary-foreground"
                    : message.role === "assistant"
                    ? "bg-muted"
                    : "bg-accent/50 text-accent-foreground"
                }`}
              >
                <div className="whitespace-pre-wrap leading-relaxed max-h-96 overflow-y-auto">
                  {message.content}
                </div>
                {message.created_at && (
                  <div
                    className={`text-xs mt-1 ${
                      message.role === "user"
                        ? "text-primary-foreground/70"
                        : "text-muted-foreground"
                    }`}
                  >
                    {new Date(message.created_at).toLocaleTimeString()}
                  </div>
                )}
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex justify-start">
              <div className="bg-muted rounded-lg px-4 py-2">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 bg-foreground/40 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-foreground/40 rounded-full animate-bounce delay-100"></div>
                  <div className="w-2 h-2 bg-foreground/40 rounded-full animate-bounce delay-200"></div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Error Message */}
        {error && (
          <div className="px-4 py-2 bg-destructive/10 text-destructive text-sm border-t border-destructive/20">
            {error}
          </div>
        )}

        {/* Input Area */}
        <div className="border-t p-4 shrink-0">
          <div className="flex gap-2">
            <Input
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={CHAT_CONFIG.INPUT_PLACEHOLDER}
              disabled={loading}
              maxLength={CHAT_CONFIG.MAX_MESSAGE_LENGTH}
              className="flex-1"
            />
            <Button onClick={handleSendMessage} disabled={loading || !inputMessage.trim()}>
              {loading ? "Sending..." : "Send"}
            </Button>
          </div>
          <div className="text-xs text-muted-foreground mt-1">
            {inputMessage.length}/{CHAT_CONFIG.MAX_MESSAGE_LENGTH} characters
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
