"use client";

/**
 * Chat Page - Phase III AI Chat Interface
 *
 * Task: T036 [US1] Create chat page integrating ChatInterface component
 * Spec: specs/004-phase-iii-ai-chatbot/spec.md
 *
 * Natural language task management interface.
 * Constitutional Principle II: User Data Isolation enforced via JWT.
 */

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import ChatInterface from "@/components/ChatInterface";
import Navigation from "@/components/Navigation";

export default function ChatPage() {
  const router = useRouter();
  const [userId, setUserId] = useState<number | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [userName, setUserName] = useState<string>("");
  const [loading, setLoading] = useState(true);

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
      <div className="container mx-auto p-6">
        <div className="mb-4">
          <h1 className="text-3xl font-bold">AI Task Assistant</h1>
          <p className="text-muted-foreground mt-1">
            Manage your tasks using natural language
          </p>
        </div>
        <ChatInterface userId={userId} token={token} userName={userName} />
      </div>
    </>
  );
}
