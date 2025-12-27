"use client";

/**
 * Chat Page - Phase III AI Chat Interface
 *
 * Task: T036 [US1] Create chat page integrating ChatInterface component
 * Task: T062 [US4] Integrate conversation UI with sidebar
 * Spec: specs/004-phase-iii-ai-chatbot/spec.md
 *
 * Natural language task management interface with conversation history.
 * Constitutional Principle II: User Data Isolation enforced via JWT.
 */

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import ChatInterface from "@/components/ChatInterface";
import ConversationList from "@/components/ConversationList";
import Navigation from "@/components/Navigation";
import { useConversationSwitcher } from "@/hooks/useConversationSwitcher";

export default function ChatPage() {
  const router = useRouter();
  const [userId, setUserId] = useState<number | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [userName, setUserName] = useState<string>("");
  const [loading, setLoading] = useState(true);

  // Conversation management (T061)
  const {
    activeConversationId,
    switchConversation,
    createNewConversation,
    setConversationId,
  } = useConversationSwitcher();

  useEffect(() => {
    // Check authentication
    const storedToken = localStorage.getItem("token");
    const storedUserId = localStorage.getItem("user_id");
    const storedUserName = localStorage.getItem("user_name");

    if (!storedToken || !storedUserId) {
      router.push("/signin");
      return;
    }

    setToken(storedToken);
    setUserId(parseInt(storedUserId));
    setUserName(storedUserName || "User");
    setLoading(false);
  }, [router]);

  if (loading) {
    return (
      <div className="container mx-auto p-6">
        <div className="flex items-center justify-center h-[calc(100vh-12rem)]">
          <div className="text-muted-foreground">Loading...</div>
        </div>
      </div>
    );
  }

  if (!userId || !token) {
    return null; // Will redirect to signin
  }

  return (
    <>
      <Navigation userName={userName} />
      {/* T062: Conversation sidebar layout */}
      <div className="flex h-[calc(100vh-4rem)]">
        {/* Conversation List Sidebar (T060) */}
        <ConversationList
          userId={userId}
          token={token}
          activeConversationId={activeConversationId}
          onConversationSelect={switchConversation}
          onNewConversation={createNewConversation}
        />

        {/* Main Chat Area */}
        <div className="flex-1 flex flex-col">
          <div className="p-6 border-b">
            <h1 className="text-2xl font-bold">AI Task Assistant</h1>
            <p className="text-muted-foreground text-sm mt-1">
              Manage your tasks using natural language
            </p>
          </div>
          <div className="flex-1 p-6 overflow-hidden">
            <ChatInterface
              userId={userId}
              token={token}
              userName={userName}
              activeConversationId={activeConversationId}
              onConversationChange={setConversationId}
            />
          </div>
        </div>
      </div>
    </>
  );
}
