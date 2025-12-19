/**
 * Better Auth configuration for Todo Evolution Phase II
 *
 * Integrates with FastAPI backend authentication endpoints:
 * - POST /api/auth/signup
 * - POST /api/auth/signin
 */

import { betterAuth } from "better-auth";

export const auth = betterAuth({
  baseURL: process.env.BETTER_AUTH_URL || "http://localhost:3000",
  secret: process.env.BETTER_AUTH_SECRET || "",

  // Custom integration with FastAPI backend
  database: undefined, // We don't use Better Auth's database, backend handles it

  // Configure to work with our FastAPI backend
  endpoints: {
    signIn: {
      path: "/api/auth/signin",
    },
    signUp: {
      path: "/api/auth/signup",
    },
  },

  // Email/Password authentication (matches our backend)
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false, // Phase II doesn't have email verification yet
  },

  // Session configuration
  session: {
    cookieCache: {
      enabled: true,
      maxAge: 5 * 60, // Cache for 5 minutes
    },
  },
});
