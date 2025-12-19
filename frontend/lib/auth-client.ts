/**
 * Better Auth client for React components
 *
 * Provides hooks and utilities for authentication in frontend:
 * - useSession() - Get current user session
 * - signIn() - Sign in with email/password
 * - signUp() - Create new account
 * - signOut() - Sign out current user
 */

import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
});

export const { signIn, signUp, signOut, useSession } = authClient;
