/**
 * API client for FastAPI backend communication
 *
 * Handles all HTTP requests to backend with JWT authentication.
 * Constitutional Principle II: User Data Isolation enforced via JWT tokens.
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface Task {
  id: number;
  user_id: number;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface CreateTaskRequest {
  title: string;
  description?: string;
}

export interface UpdateTaskRequest {
  title?: string;
  description?: string;
  completed?: boolean;
}

export interface AuthResponse {
  user_id: number;
  email: string;
  name: string;
  token: string;
}

export interface SignupRequest {
  email: string;
  name: string;
  password: string;
}

export interface SigninRequest {
  email: string;
  password: string;
}

/**
 * Base API request with JWT authentication
 */
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {},
  token?: string
): Promise<T> {
  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  });

  // Handle 204 No Content responses (e.g., DELETE success)
  if (response.status === 204) {
    return undefined as T;
  }

  // Handle error responses
  if (!response.ok) {
    // Check if response has JSON content
    const contentType = response.headers.get("content-type");
    if (contentType && contentType.includes("application/json")) {
      try {
        const error = await response.json();
        throw new Error(error.detail || `HTTP ${response.status}`);
      } catch (e) {
        // If JSON parsing fails, throw generic error
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
    } else {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
  }

  // Handle success responses with JSON body
  const contentType = response.headers.get("content-type");
  if (contentType && contentType.includes("application/json")) {
    return response.json();
  }

  // If no JSON content, return undefined
  return undefined as T;
}

/**
 * Authentication API
 */
export const authApi = {
  signup: (data: SignupRequest): Promise<AuthResponse> =>
    apiRequest("/api/auth/signup", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  signin: (data: SigninRequest): Promise<AuthResponse> =>
    apiRequest("/api/auth/signin", {
      method: "POST",
      body: JSON.stringify(data),
    }),
};

/**
 * Task API (requires JWT authentication)
 */
export const taskApi = {
  getAll: (userId: number, token: string): Promise<Task[]> =>
    apiRequest(`/api/${userId}/tasks`, {}, token),

  getOne: (userId: number, taskId: number, token: string): Promise<Task> =>
    apiRequest(`/api/${userId}/tasks/${taskId}`, {}, token),

  create: (userId: number, data: CreateTaskRequest, token: string): Promise<Task> =>
    apiRequest(`/api/${userId}/tasks`, {
      method: "POST",
      body: JSON.stringify(data),
    }, token),

  update: (userId: number, taskId: number, data: UpdateTaskRequest, token: string): Promise<Task> =>
    apiRequest(`/api/${userId}/tasks/${taskId}`, {
      method: "PATCH",
      body: JSON.stringify(data),
    }, token),

  toggle: (userId: number, taskId: number, token: string): Promise<Task> =>
    apiRequest(`/api/${userId}/tasks/${taskId}/toggle`, {
      method: "POST",
    }, token),

  delete: (userId: number, taskId: number, token: string): Promise<void> =>
    apiRequest(`/api/${userId}/tasks/${taskId}`, {
      method: "DELETE",
    }, token),
};
