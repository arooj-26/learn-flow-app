/**
 * Auth Context Provider for LearnFlow.
 * Provides authentication state throughout the application.
 */
import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { useRouter } from 'next/router';
import { authClient, setAuthToken } from '@/lib/auth-client';

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

interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const router = useRouter();
  const { data: session, isPending, refetch } = authClient.useSession();
  const [isSigningOut, setIsSigningOut] = useState(false);

  // Map session to auth user
  const user: AuthUser | null = session?.user
    ? {
        id: session.user.id,
        name: session.user.name,
        email: session.user.email,
        role: (session.user as { role?: string }).role === 'teacher' ? 'teacher' : 'student',
        image: session.user.image,
        emailVerified: session.user.emailVerified,
      }
    : null;

  const isLoading = isPending || isSigningOut;
  const isAuthenticated = !!user && !isLoading;

  // Update auth token when session changes
  useEffect(() => {
    if (session?.session?.token) {
      setAuthToken(session.session.token);
    }
  }, [session]);

  const handleSignOut = async () => {
    setIsSigningOut(true);
    try {
      await authClient.signOut();
      setAuthToken(null);
      router.push('/login');
    } finally {
      setIsSigningOut(false);
    }
  };

  const refreshSession = async () => {
    await refetch();
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        isAuthenticated,
        signOut: handleSignOut,
        refreshSession,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

// Helper hook for getting the current user ID (throws if not authenticated)
export function useUserId(): string {
  const { user, isAuthenticated } = useAuth();
  if (!isAuthenticated || !user) {
    throw new Error('User is not authenticated');
  }
  return user.id;
}
