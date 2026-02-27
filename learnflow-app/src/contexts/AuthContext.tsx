/**
 * Auth Context Provider for LearnFlow.
 * Provides authentication state throughout the application.
 */
import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { useRouter } from 'next/router';
import { getStoredSession, clearSession } from '@/lib/auth-simple';

export interface AuthUser {
  id: string;
  name: string;
  email: string;
  role: 'student' | 'teacher';
  image?: string | null;
  emailVerified?: boolean;
}

interface AuthContextType {
  user: AuthUser | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  signOut: () => Promise<void>;
  refreshSession: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const router = useRouter();
  const [user, setUser] = useState<AuthUser | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const loadSession = async () => {
    // 1. Try localStorage first (fastest path)
    const localSession = getStoredSession();
    if (localSession) {
      setUser({
        id: localSession.id,
        name: localSession.name,
        email: localSession.email,
        role: localSession.role === 'teacher' ? 'teacher' : 'student',
      });
      setIsLoading(false);
      // Re-sync server cookie in case it was lost between browser sessions
      fetch('/api/auth/create-session', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(localSession),
      }).catch(() => {});
      return;
    }

    // 2. No localStorage — check if a valid server cookie still exists
    try {
      const res = await fetch('/api/auth/session', { credentials: 'include' });
      if (res.ok) {
        const data = await res.json();
        if (data?.user?.id) {
          const u = data.user;
          // Restore into localStorage so future loads are instant
          if (typeof window !== 'undefined') {
            localStorage.setItem('lf_session', JSON.stringify(u));
          }
          setUser({ id: u.id, name: u.name, email: u.email, role: u.role === 'teacher' ? 'teacher' : 'student' });
          setIsLoading(false);
          return;
        }
      }
    } catch { /* no server session */ }

    setUser(null);
    setIsLoading(false);
  };

  useEffect(() => {
    loadSession();
  }, []);

  const handleSignOut = async () => {
    clearSession();
    setUser(null);
    // Also clear server-side cookie
    try {
      await fetch('/api/auth/signout', { method: 'POST', credentials: 'include' });
    } catch { /* non-critical */ }
    router.push('/login');
  };

  const refreshSession = async () => {
    await loadSession();
  };

  return (
    <AuthContext.Provider value={{
      user,
      isLoading,
      isAuthenticated: !!user && !isLoading,
      signOut: handleSignOut,
      refreshSession,
    }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (context === undefined) throw new Error('useAuth must be used within an AuthProvider');
  return context;
}

export function useUserId(): string {
  const { user, isAuthenticated } = useAuth();
  if (!isAuthenticated || !user) throw new Error('User is not authenticated');
  return user.id;
}
