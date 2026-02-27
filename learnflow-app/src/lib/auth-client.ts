/**
 * Better Auth React client for LearnFlow.
 * Provides hooks and methods for authentication on the client side.
 */
import { createAuthClient } from 'better-auth/react';

// Dynamically get baseURL to support multiple ports (3000, 3001, etc.)
const getBaseURL = () => {
  if (typeof window !== 'undefined') {
    return window.location.origin;
  }
  return process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000';
};

export const authClient = createAuthClient({
  baseURL: getBaseURL(),
});

// Export commonly used hooks and methods
export const {
  signIn,
  signUp,
  signOut,
  useSession,
  getSession,
} = authClient;

// Helper to get bearer token for API calls
export function getAuthToken(): string | null {
  // Better Auth stores session in cookies, but we can also use localStorage for API tokens
  if (typeof window !== 'undefined') {
    return localStorage.getItem('learnflow_token');
  }
  return null;
}

// Helper to set auth token (used after login for API calls)
export function setAuthToken(token: string | null): void {
  if (typeof window !== 'undefined') {
    if (token) {
      localStorage.setItem('learnflow_token', token);
    } else {
      localStorage.removeItem('learnflow_token');
    }
  }
}

// Helper to validate teacher access code
export function validateTeacherCode(code: string): boolean {
  const teacherCode = process.env.NEXT_PUBLIC_TEACHER_ACCESS_CODE || 'learnflow-teacher-2026';
  return code === teacherCode;
}
