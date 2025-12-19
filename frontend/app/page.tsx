"use client";

/**
 * Home Page - Phase II Web App
 *
 * Landing page with sign in/sign up options.
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
    <div className="flex min-h-screen items-center justify-center bg-slate-50 px-4">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <CardTitle className="text-3xl font-bold">Todo Evolution</CardTitle>
          <CardDescription className="text-lg">
            Phase II: Web Application
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-center text-muted-foreground">
            Manage your tasks with a modern web interface
          </p>
          <div className="flex flex-col gap-3">
            <Link href="/signin" className="w-full">
              <Button className="w-full" size="lg">
                Sign In
              </Button>
            </Link>
            <Link href="/signup" className="w-full">
              <Button variant="outline" className="w-full" size="lg">
                Create Account
              </Button>
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
