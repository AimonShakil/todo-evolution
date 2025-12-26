"use client";

/**
 * Navigation Component - Phase III
 *
 * Task: T037 [US1] Update navigation (Tasks → Chat)
 * Spec: specs/004-phase-iii-ai-chatbot/spec.md
 *
 * Global navigation bar for authenticated pages.
 */

import { usePathname, useRouter } from "next/navigation";
import Link from "next/link";
import { Button } from "@/components/ui/button";

interface NavigationProps {
  userName?: string;
}

export default function Navigation({ userName }: NavigationProps) {
  const pathname = usePathname();
  const router = useRouter();

  const handleSignOut = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user_id");
    localStorage.removeItem("user_name");
    router.push("/signin");
  };

  const navLinks = [
    { href: "/tasks", label: "Tasks" },
    { href: "/chat", label: "Chat" },
  ];

  return (
    <nav className="border-b bg-background">
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-8">
            <Link href="/" className="text-xl font-bold">
              Todo Evolution
            </Link>
            <div className="flex space-x-4">
              {navLinks.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    pathname === link.href
                      ? "bg-primary text-primary-foreground"
                      : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
                  }`}
                >
                  {link.label}
                </Link>
              ))}
            </div>
          </div>
          <div className="flex items-center space-x-4">
            {userName && (
              <span className="text-sm text-muted-foreground">
                Welcome, {userName}
              </span>
            )}
            <Button variant="outline" size="sm" onClick={handleSignOut}>
              Sign Out
            </Button>
          </div>
        </div>
      </div>
    </nav>
  );
}
