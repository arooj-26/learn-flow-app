/**
 * Auth client for LearnFlow.
 * Uses localStorage for user storage and signed JWT cookies for API session.
 * No database or external service required.
 */
import { useState, useEffect } from 'react';
import { localSignUp, localSignIn, localSignOut, getStoredSession, updateLocalRole } from './auth-simple';

interface SessionUser {
  id: string;
  name: string;
  email: string;
  role: string;
}

interface SessionData {
  user: SessionUser;
  session: { token: string };
}

// Create a server session cookie so API routes can identify the user
async function syncServerSession(user: SessionUser | null): Promise<void> {
  try {
    if (user) {
      await fetch('/api/auth/create-session', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(user),
      });
    } else {
      await fetch('/api/auth/signout', { method: 'POST', credentials: 'include' });
    }
  } catch {
    // Non-critical - localStorage session still works
  }
}

function useSessionHook(): { data: SessionData | null; isPending: boolean; refetch: () => void } {
  const [data, setData] = useState<SessionData | null>(null);
  const [isPending, setIsPending] = useState(true);

  const loadSession = () => {
    const user = getStoredSession();
    setData(user ? { user, session: { token: 'local' } } : null);
    setIsPending(false);
  };

  useEffect(() => {
    loadSession();
  }, []);

  return { data, isPending, refetch: loadSession };
}

export const authClient = {
  signUp: {
    email: async ({ name, email, password }: { name: string; email: string; password: string }) => {
      const result = await localSignUp(name, email, password);
      if (result.error) return { error: { message: result.error }, data: null };
      await syncServerSession(result.user!);
      return { data: { user: result.user }, error: null };
    },
  },
  signIn: {
    email: async ({ email, password }: { email: string; password: string }) => {
      const result = await localSignIn(email, password);
      if (result.error) return { error: { message: result.error }, data: null };
      await syncServerSession(result.user!);
      return { data: { user: result.user }, error: null };
    },
    social: async ({ provider }: { provider: string; callbackURL?: string }) => {
      return { error: { message: `${provider} sign-in is not configured. Please use email and password.` }, data: null };
    },
  },
  signOut: async () => {
    localSignOut();
    await syncServerSession(null);
    return {};
  },
  useSession: useSessionHook,
};

// Named exports matching better-auth API surface
export const signIn = authClient.signIn.email;
export const signUp = authClient.signUp.email;
export const signOut = authClient.signOut;
export const useSession = useSessionHook;
export const getSession = async () => getStoredSession();

// Helper to get auth token for API calls
export function getAuthToken(): string | null {
  if (typeof window === 'undefined') return null;
  const session = getStoredSession();
  return session?.id || null;
}

// Helper to set auth token (legacy compat)
export function setAuthToken(_token: string | null): void {
  // No-op — session is managed by localStorage
}

// Helper to validate teacher access code
export function validateTeacherCode(code: string): boolean {
  const teacherCode = process.env.NEXT_PUBLIC_TEACHER_ACCESS_CODE || 'learnflow-teacher-2026';
  return code === teacherCode;
}

// Export updateLocalRole for use in signup page
export { updateLocalRole };
