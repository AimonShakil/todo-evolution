"use client";

/**
 * Landing Page - Phase III Premium UI
 *
 * Modern, animated landing page with dark mode support.
 * Features: gradient backgrounds, hover animations, view showcase, pricing.
 */

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Moon, Sun } from "lucide-react";

export default function Home() {
  const router = useRouter();
  const [theme, setTheme] = useState<"light" | "dark">("light");

  useEffect(() => {
    // Check system preference
    if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
      setTheme("dark");
      document.documentElement.classList.add("dark");
    }
  }, []);

  useEffect(() => {
    // Redirect to tasks if already signed in
    const token = localStorage.getItem("token");
    if (token) {
      router.push("/tasks");
    }
  }, [router]);

  const toggleTheme = () => {
    if (theme === "light") {
      setTheme("dark");
      document.documentElement.classList.add("dark");
    } else {
      setTheme("light");
      document.documentElement.classList.remove("dark");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100 dark:from-slate-950 dark:to-slate-900 transition-colors">
      {/* Header */}
      <header className="border-b bg-white/80 dark:bg-slate-950/80 backdrop-blur-sm sticky top-0 z-50 transition-colors">
        <div className="container mx-auto px-6 py-4 flex items-center justify-between">
          <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Todo Evolution
          </h1>
          <div className="flex gap-3 items-center">
            <button
              onClick={toggleTheme}
              className="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
              aria-label="Toggle theme"
            >
              {theme === "light" ? (
                <Moon className="w-5 h-5 text-slate-600" />
              ) : (
                <Sun className="w-5 h-5 text-slate-400" />
              )}
            </button>
            <Link href="/signin">
              <Button variant="ghost">Sign In</Button>
            </Link>
            <Link href="/signup">
              <Button className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 transition-all">
                Get Started
              </Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section with Gradient Background */}
      <section className="relative overflow-hidden">
        {/* Animated gradient background */}
        <div className="absolute inset-0 bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 dark:from-blue-950/30 dark:via-purple-950/30 dark:to-pink-950/30" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(147,51,234,0.1),transparent_50%)]" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_bottom_left,rgba(59,130,246,0.1),transparent_50%)]" />

        <div className="relative container mx-auto px-6 py-32 text-center">
          <div className="max-w-4xl mx-auto space-y-8">
            <div className="inline-block px-4 py-2 bg-blue-100 dark:bg-blue-900/30 rounded-full mb-4">
              <span className="text-sm font-semibold text-blue-600 dark:text-blue-400">
                ✨ Powered by GPT-4 • Context-Aware AI
              </span>
            </div>

            <h2 className="text-6xl md:text-7xl lg:text-8xl font-extrabold bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent leading-tight">
              Manage Tasks with AI
            </h2>

            <p className="text-xl md:text-2xl text-slate-600 dark:text-slate-300 max-w-3xl mx-auto">
              Stop clicking through menus. Just tell our AI what you need to do,
              and it handles the rest. Natural language task management that actually understands you.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
              <Link href="/signup">
                <Button
                  size="lg"
                  className="text-lg px-10 py-7 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 hover:scale-105 transition-all shadow-lg hover:shadow-xl"
                >
                  Start Free Trial
                </Button>
              </Link>
              <Link href="/signin">
                <Button
                  size="lg"
                  variant="outline"
                  className="text-lg px-10 py-7 border-2 hover:bg-slate-50 dark:hover:bg-slate-800 hover:scale-105 transition-all"
                >
                  Watch Demo
                </Button>
              </Link>
            </div>

            <p className="text-sm text-slate-500 dark:text-slate-400">
              No credit card required • 14-day free trial • Cancel anytime
            </p>
          </div>
        </div>
      </section>

      {/* Features Section with Hover Animations */}
      <section className="container mx-auto px-6 py-20">
        <h3 className="text-4xl font-bold text-center mb-4 dark:text-white">
          Why Todo Evolution?
        </h3>
        <p className="text-center text-slate-600 dark:text-slate-400 mb-12 max-w-2xl mx-auto">
          The only task manager that truly understands natural language and context
        </p>

        <div className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto">
          {/* Feature 1 */}
          <Card className="group hover:scale-105 hover:-translate-y-2 transition-all duration-300 hover:shadow-2xl border-2 hover:border-blue-400 dark:hover:border-blue-600">
            <CardHeader>
              <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-blue-100 to-blue-200 dark:from-blue-900/30 dark:to-blue-800/30 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                <svg className="w-7 h-7 text-blue-600 dark:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                </svg>
              </div>
              <CardTitle className="text-xl dark:text-white">Natural Language</CardTitle>
              <CardDescription className="dark:text-slate-400">
                Just type "Buy milk tomorrow" or "Remind me to call the dentist" - our AI understands and creates tasks instantly.
              </CardDescription>
            </CardHeader>
          </Card>

          {/* Feature 2 */}
          <Card className="group hover:scale-105 hover:-translate-y-2 transition-all duration-300 hover:shadow-2xl border-2 hover:border-purple-400 dark:hover:border-purple-600">
            <CardHeader>
              <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-purple-100 to-purple-200 dark:from-purple-900/30 dark:to-purple-800/30 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                <svg className="w-7 h-7 text-purple-600 dark:text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <CardTitle className="text-xl dark:text-white">Smart Management</CardTitle>
              <CardDescription className="dark:text-slate-400">
                "Complete the milk task" - no need to remember IDs or navigate menus. AI finds and updates tasks by name.
              </CardDescription>
            </CardHeader>
          </Card>

          {/* Feature 3 */}
          <Card className="group hover:scale-105 hover:-translate-y-2 transition-all duration-300 hover:shadow-2xl border-2 hover:border-green-400 dark:hover:border-green-600">
            <CardHeader>
              <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-green-100 to-green-200 dark:from-green-900/30 dark:to-green-800/30 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                <svg className="w-7 h-7 text-green-600 dark:text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <CardTitle className="text-xl dark:text-white">Context Aware</CardTitle>
              <CardDescription className="dark:text-slate-400">
                "Actually, make it oat milk" - AI remembers your conversation and updates the right task automatically.
              </CardDescription>
            </CardHeader>
          </Card>
        </div>
      </section>

      {/* Views Showcase Section */}
      <section className="bg-white dark:bg-slate-900 py-20 transition-colors">
        <div className="container mx-auto px-6">
          <div className="text-center mb-12">
            <h3 className="text-4xl font-bold mb-4 dark:text-white">
              Switch between different views to match your workflow
            </h3>
            <p className="text-xl text-slate-600 dark:text-slate-400">
              All your tasks, visualized beautifully
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto">
            {/* List View */}
            <Card className="group hover:scale-105 transition-all duration-300 hover:shadow-xl">
              <CardHeader>
                <div className="w-12 h-12 rounded-lg bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center mb-3 group-hover:rotate-12 transition-transform">
                  <svg className="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                  </svg>
                </div>
                <CardTitle className="text-lg dark:text-white">List View</CardTitle>
                <CardDescription className="dark:text-slate-400">
                  Classic checklist for quick scanning
                </CardDescription>
              </CardHeader>
            </Card>

            {/* Grid View */}
            <Card className="group hover:scale-105 transition-all duration-300 hover:shadow-xl">
              <CardHeader>
                <div className="w-12 h-12 rounded-lg bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center mb-3 group-hover:rotate-12 transition-transform">
                  <svg className="w-6 h-6 text-purple-600 dark:text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 5a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM14 5a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1V5zM4 15a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H5a1 1 0 01-1-1v-4zM14 15a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z" />
                  </svg>
                </div>
                <CardTitle className="text-lg dark:text-white">Grid View</CardTitle>
                <CardDescription className="dark:text-slate-400">
                  Card-based layout for visual organization
                </CardDescription>
              </CardHeader>
            </Card>

            {/* Kanban Board */}
            <Card className="group hover:scale-105 transition-all duration-300 hover:shadow-xl">
              <CardHeader>
                <div className="w-12 h-12 rounded-lg bg-green-100 dark:bg-green-900/30 flex items-center justify-center mb-3 group-hover:rotate-12 transition-transform">
                  <svg className="w-6 h-6 text-green-600 dark:text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7m0 10a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2" />
                  </svg>
                </div>
                <CardTitle className="text-lg dark:text-white">Kanban Board</CardTitle>
                <CardDescription className="dark:text-slate-400">
                  Drag-and-drop workflow management
                </CardDescription>
              </CardHeader>
            </Card>

            {/* Calendar */}
            <Card className="group hover:scale-105 transition-all duration-300 hover:shadow-xl">
              <CardHeader>
                <div className="w-12 h-12 rounded-lg bg-orange-100 dark:bg-orange-900/30 flex items-center justify-center mb-3 group-hover:rotate-12 transition-transform">
                  <svg className="w-6 h-6 text-orange-600 dark:text-orange-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
                <CardTitle className="text-lg dark:text-white">Calendar</CardTitle>
                <CardDescription className="dark:text-slate-400">
                  Time-based scheduling and planning
                </CardDescription>
              </CardHeader>
            </Card>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section className="container mx-auto px-6 py-20">
        <div className="text-center mb-12">
          <h3 className="text-4xl font-bold mb-4 dark:text-white">Simple, Transparent Pricing</h3>
          <p className="text-xl text-slate-600 dark:text-slate-400">
            Choose the plan that works for you
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {/* Free Plan */}
          <Card className="hover:scale-105 transition-all duration-300">
            <CardHeader>
              <CardTitle className="text-2xl dark:text-white">Free</CardTitle>
              <div className="mt-4">
                <span className="text-4xl font-bold dark:text-white">$0</span>
                <span className="text-slate-600 dark:text-slate-400">/month</span>
              </div>
            </CardHeader>
            <CardContent>
              <ul className="space-y-3 mb-6">
                <li className="flex items-start">
                  <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span className="dark:text-slate-300">Up to 50 tasks</span>
                </li>
                <li className="flex items-start">
                  <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span className="dark:text-slate-300">AI chat (10 messages/day)</span>
                </li>
                <li className="flex items-start">
                  <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span className="dark:text-slate-300">List view only</span>
                </li>
              </ul>
              <Link href="/signup">
                <Button className="w-full" variant="outline">Get Started</Button>
              </Link>
            </CardContent>
          </Card>

          {/* Pro Plan */}
          <Card className="hover:scale-105 transition-all duration-300 border-2 border-purple-500 relative">
            <div className="absolute -top-4 left-1/2 -translate-x-1/2 bg-gradient-to-r from-blue-600 to-purple-600 text-white px-4 py-1 rounded-full text-sm font-semibold">
              Most Popular
            </div>
            <CardHeader>
              <CardTitle className="text-2xl dark:text-white">Pro</CardTitle>
              <div className="mt-4">
                <span className="text-4xl font-bold dark:text-white">$12</span>
                <span className="text-slate-600 dark:text-slate-400">/month</span>
              </div>
            </CardHeader>
            <CardContent>
              <ul className="space-y-3 mb-6">
                <li className="flex items-start">
                  <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span className="dark:text-slate-300">Unlimited tasks</span>
                </li>
                <li className="flex items-start">
                  <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span className="dark:text-slate-300">Unlimited AI chat</span>
                </li>
                <li className="flex items-start">
                  <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span className="dark:text-slate-300">All views (List, Grid, Kanban, Calendar)</span>
                </li>
                <li className="flex items-start">
                  <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span className="dark:text-slate-300">Priority support</span>
                </li>
              </ul>
              <Link href="/signup">
                <Button className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700">
                  Start Free Trial
                </Button>
              </Link>
            </CardContent>
          </Card>

          {/* Team Plan */}
          <Card className="hover:scale-105 transition-all duration-300">
            <CardHeader>
              <CardTitle className="text-2xl dark:text-white">Team</CardTitle>
              <div className="mt-4">
                <span className="text-4xl font-bold dark:text-white">$29</span>
                <span className="text-slate-600 dark:text-slate-400">/month</span>
              </div>
            </CardHeader>
            <CardContent>
              <ul className="space-y-3 mb-6">
                <li className="flex items-start">
                  <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span className="dark:text-slate-300">Everything in Pro</span>
                </li>
                <li className="flex items-start">
                  <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span className="dark:text-slate-300">Up to 10 team members</span>
                </li>
                <li className="flex items-start">
                  <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span className="dark:text-slate-300">Shared workspaces</span>
                </li>
                <li className="flex items-start">
                  <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span className="dark:text-slate-300">Admin controls</span>
                </li>
              </ul>
              <Link href="/signup">
                <Button className="w-full" variant="outline">Get Started</Button>
              </Link>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="bg-slate-50 dark:bg-slate-800/50 py-20 transition-colors">
        <div className="container mx-auto px-6">
          <h3 className="text-4xl font-bold text-center mb-16 dark:text-white">
            How It Works
          </h3>
          <div className="max-w-4xl mx-auto grid md:grid-cols-3 gap-8 text-center">
            <div className="group">
              <div className="w-20 h-20 rounded-full bg-gradient-to-br from-blue-100 to-blue-200 dark:from-blue-900/30 dark:to-blue-800/30 text-blue-600 dark:text-blue-400 flex items-center justify-center text-3xl font-bold mx-auto mb-4 group-hover:scale-110 transition-transform">
                1
              </div>
              <h4 className="font-semibold text-xl mb-2 dark:text-white">Sign Up Free</h4>
              <p className="text-slate-600 dark:text-slate-400">Create your account in seconds - no credit card required</p>
            </div>
            <div className="group">
              <div className="w-20 h-20 rounded-full bg-gradient-to-br from-purple-100 to-purple-200 dark:from-purple-900/30 dark:to-purple-800/30 text-purple-600 dark:text-purple-400 flex items-center justify-center text-3xl font-bold mx-auto mb-4 group-hover:scale-110 transition-transform">
                2
              </div>
              <h4 className="font-semibold text-xl mb-2 dark:text-white">Chat with AI</h4>
              <p className="text-slate-600 dark:text-slate-400">Tell the AI what you need to do in plain English</p>
            </div>
            <div className="group">
              <div className="w-20 h-20 rounded-full bg-gradient-to-br from-green-100 to-green-200 dark:from-green-900/30 dark:to-green-800/30 text-green-600 dark:text-green-400 flex items-center justify-center text-3xl font-bold mx-auto mb-4 group-hover:scale-110 transition-transform">
                3
              </div>
              <h4 className="font-semibold text-xl mb-2 dark:text-white">Get Things Done</h4>
              <p className="text-slate-600 dark:text-slate-400">AI organizes, tracks, and manages your tasks effortlessly</p>
            </div>
          </div>
        </div>
      </section>

      {/* Final CTA Section */}
      <section className="container mx-auto px-6 py-24 text-center">
        <div className="max-w-3xl mx-auto space-y-8">
          <h3 className="text-5xl font-bold dark:text-white">Ready to evolve your productivity?</h3>
          <p className="text-2xl text-slate-600 dark:text-slate-400">
            Join thousands of users who manage their tasks with AI
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/signup">
              <Button
                size="lg"
                className="text-lg px-12 py-7 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 hover:scale-105 transition-all shadow-lg"
              >
                Get Started for Free
              </Button>
            </Link>
          </div>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            14-day free trial • No credit card required • Cancel anytime
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t bg-white dark:bg-slate-950 transition-colors">
        <div className="container mx-auto px-6 py-12">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            {/* Brand */}
            <div>
              <h3 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-4">
                Todo Evolution
              </h3>
              <p className="text-sm text-slate-600 dark:text-slate-400">
                AI-powered task management for the modern world.
              </p>
            </div>

            {/* Product */}
            <div>
              <h4 className="font-semibold mb-4 dark:text-white">Product</h4>
              <ul className="space-y-2 text-sm">
                <li><Link href="/signup" className="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200">Features</Link></li>
                <li><Link href="/signup" className="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200">Pricing</Link></li>
                <li><Link href="/signup" className="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200">FAQ</Link></li>
                <li><Link href="/signin" className="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200">Sign In</Link></li>
              </ul>
            </div>

            {/* Company */}
            <div>
              <h4 className="font-semibold mb-4 dark:text-white">Company</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200">About</a></li>
                <li><a href="#" className="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200">Blog</a></li>
                <li><a href="#" className="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200">Careers</a></li>
                <li><a href="#" className="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200">Contact</a></li>
              </ul>
            </div>

            {/* Download Apps */}
            <div>
              <h4 className="font-semibold mb-4 dark:text-white">Download Apps</h4>
              <div className="space-y-3">
                <a
                  href="#"
                  className="flex items-center gap-2 px-4 py-2 bg-black dark:bg-white text-white dark:text-black rounded-lg hover:scale-105 transition-transform text-sm"
                >
                  <svg className="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z"/>
                  </svg>
                  <div className="text-left">
                    <div className="text-[10px]">Download on the</div>
                    <div className="text-sm font-semibold -mt-1">App Store</div>
                  </div>
                </a>
                <a
                  href="#"
                  className="flex items-center gap-2 px-4 py-2 bg-black dark:bg-white text-white dark:text-black rounded-lg hover:scale-105 transition-transform text-sm"
                >
                  <svg className="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M3,20.5V3.5C3,2.91 3.34,2.39 3.84,2.15L13.69,12L3.84,21.85C3.34,21.6 3,21.09 3,20.5M16.81,15.12L6.05,21.34L14.54,12.85L16.81,15.12M20.16,10.81C20.5,11.08 20.75,11.5 20.75,12C20.75,12.5 20.5,12.92 20.16,13.19L17.89,14.5L15.39,12L17.89,9.5L20.16,10.81M6.05,2.66L16.81,8.88L14.54,11.15L6.05,2.66Z"/>
                  </svg>
                  <div className="text-left">
                    <div className="text-[10px]">GET IT ON</div>
                    <div className="text-sm font-semibold -mt-1">Google Play</div>
                  </div>
                </a>
              </div>
            </div>
          </div>

          {/* Bottom Bar */}
          <div className="pt-8 border-t border-slate-200 dark:border-slate-800 flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-sm text-slate-600 dark:text-slate-400">
              © 2025 Todo Evolution. Powered by GPT-4. All rights reserved.
            </p>
            <div className="flex gap-6 text-sm">
              <a href="#" className="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200">Privacy Policy</a>
              <a href="#" className="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200">Terms of Service</a>
              <a href="#" className="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200">Cookie Policy</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
