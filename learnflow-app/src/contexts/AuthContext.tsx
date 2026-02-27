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

  const loadSession = () => {
    const session = getStoredSession();
    if (session) {
      setUser({
        id: session.id,
        name: session.name,
        email: session.email,
        role: session.role === 'teacher' ? 'teacher' : 'student',
      });
    } else {
      setUser(null);
    }
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
    loadSession();
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
