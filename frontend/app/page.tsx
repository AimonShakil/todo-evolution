"use client";

/**
 * Landing Page - Phase III Professional UI
 *
 * Modern landing page showcasing AI-powered task management.
 * Inspired by professional SaaS landing pages.
 */

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    // Redirect to tasks if already signed in
    const token = localStorage.getItem("token");
    if (token) {
      router.push("/tasks");
    }
  }, [router]);

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-10">
        <div className="container mx-auto px-6 py-4 flex items-center justify-between">
          <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Todo Evolution
          </h1>
          <div className="flex gap-3">
            <Link href="/signin">
              <Button variant="ghost">Sign In</Button>
            </Link>
            <Link href="/signup">
              <Button>Get Started</Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-6 py-20 text-center">
        <div className="max-w-3xl mx-auto space-y-6">
          <h2 className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Manage Tasks with AI
          </h2>
          <p className="text-xl text-muted-foreground">
            Stop clicking through menus. Just tell our AI what you need to do,
            and it handles the rest. Natural language task management powered by GPT-4.
          </p>
          <div className="flex gap-4 justify-center pt-4">
            <Link href="/signup">
              <Button size="lg" className="text-lg px-8">
                Start Free
              </Button>
            </Link>
            <Link href="/signin">
              <Button size="lg" variant="outline" className="text-lg px-8">
                Sign In
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-6 py-16">
        <h3 className="text-3xl font-bold text-center mb-12">
          Why Todo Evolution?
        </h3>
        <div className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto">
          {/* Feature 1 */}
          <Card>
            <CardHeader>
              <div className="w-12 h-12 rounded-lg bg-blue-100 flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                </svg>
              </div>
              <CardTitle>Natural Language</CardTitle>
              <CardDescription>
                Just type "Buy milk tomorrow" or "Remind me to call the dentist" - our AI understands and creates tasks instantly.
              </CardDescription>
            </CardHeader>
          </Card>

          {/* Feature 2 */}
          <Card>
            <CardHeader>
              <div className="w-12 h-12 rounded-lg bg-purple-100 flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <CardTitle>Smart Management</CardTitle>
              <CardDescription>
                "Complete the milk task" - no need to remember IDs or navigate menus. AI finds and updates tasks by name.
              </CardDescription>
            </CardHeader>
          </Card>

          {/* Feature 3 */}
          <Card>
            <CardHeader>
              <div className="w-12 h-12 rounded-lg bg-green-100 flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <CardTitle>Context Aware</CardTitle>
              <CardDescription>
                "Actually, make it oat milk" - AI remembers your conversation and updates the right task automatically.
              </CardDescription>
            </CardHeader>
          </Card>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="container mx-auto px-6 py-16 bg-white rounded-lg my-16">
        <h3 className="text-3xl font-bold text-center mb-12">
          How It Works
        </h3>
        <div className="max-w-4xl mx-auto grid md:grid-cols-3 gap-8 text-center">
          <div>
            <div className="w-16 h-16 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center text-2xl font-bold mx-auto mb-4">
              1
            </div>
            <h4 className="font-semibold text-lg mb-2">Sign Up</h4>
            <p className="text-muted-foreground">Create your free account in seconds</p>
          </div>
          <div>
            <div className="w-16 h-16 rounded-full bg-purple-100 text-purple-600 flex items-center justify-center text-2xl font-bold mx-auto mb-4">
              2
            </div>
            <h4 className="font-semibold text-lg mb-2">Chat with AI</h4>
            <p className="text-muted-foreground">Tell the AI what you need to do in plain English</p>
          </div>
          <div>
            <div className="w-16 h-16 rounded-full bg-green-100 text-green-600 flex items-center justify-center text-2xl font-bold mx-auto mb-4">
              3
            </div>
            <h4 className="font-semibold text-lg mb-2">Get Things Done</h4>
            <p className="text-muted-foreground">AI organizes, tracks, and manages your tasks</p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto px-6 py-20 text-center">
        <div className="max-w-2xl mx-auto space-y-6">
          <h3 className="text-4xl font-bold">Ready to evolve your task management?</h3>
          <p className="text-xl text-muted-foreground">
            Join hundreds of users who manage their tasks with AI
          </p>
          <Link href="/signup">
            <Button size="lg" className="text-lg px-12 py-6">
              Get Started for Free
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t bg-white/80 backdrop-blur-sm mt-16">
        <div className="container mx-auto px-6 py-8">
          <div className="flex justify-between items-center">
            <p className="text-sm text-muted-foreground">
              © 2025 Todo Evolution. Powered by GPT-4.
            </p>
            <div className="flex gap-6 text-sm text-muted-foreground">
              <Link href="/signin" className="hover:text-foreground">Sign In</Link>
              <Link href="/signup" className="hover:text-foreground">Sign Up</Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
