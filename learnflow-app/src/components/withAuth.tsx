/**
 * Higher-Order Component for protecting routes that require authentication.
 * Redirects to login page if user is not authenticated.
 */
import { useEffect, ComponentType } from 'react';
import { useRouter } from 'next/router';
import { Loader2 } from 'lucide-react';
import { useAuth, AuthUser } from '@/contexts/AuthContext';

interface WithAuthOptions {
  /** Required role to access the page. If not specified, any authenticated user can access. */
  requiredRole?: 'student' | 'teacher';
  /** Path to redirect to if not authenticated. Defaults to '/login'. */
  redirectTo?: string;
  /** Path to redirect to if user doesn't have required role. Defaults to '/dashboard'. */
  unauthorizedRedirect?: string;
}

interface WithAuthProps {
  user: AuthUser;
}

/**
 * HOC that wraps a component with authentication protection.
 *
 * @example
 * // Require any authenticated user
 * export default withAuth(DashboardPage);
 *
 * @example
 * // Require teacher role
 * export default withAuth(TeacherPage, { requiredRole: 'teacher' });
 */
export function withAuth<P extends WithAuthProps>(
  WrappedComponent: ComponentType<P>,
  options: WithAuthOptions = {}
) {
  const {
    requiredRole,
    redirectTo = '/login',
    unauthorizedRedirect = '/dashboard',
  } = options;

  function AuthenticatedComponent(props: Omit<P, keyof WithAuthProps>) {
    const router = useRouter();
    const { user, isLoading, isAuthenticated } = useAuth();

    useEffect(() => {
      // Wait for auth to load
      if (isLoading) return;

      // Redirect to login if not authenticated
      if (!isAuthenticated) {
        router.replace(redirectTo);
        return;
      }

      // Check role requirement
      if (requiredRole && user?.role !== requiredRole) {
        router.replace(unauthorizedRedirect);
        return;
      }
    }, [isLoading, isAuthenticated, user, router]);

    // Show loading state while checking auth
    if (isLoading) {
      return (
        <div className="min-h-screen bg-slate-900 flex items-center justify-center">
          <div className="text-center">
            <Loader2 className="animate-spin text-blue-400 mx-auto mb-4" size={32} />
            <p className="text-slate-400 text-sm">Loading...</p>
          </div>
        </div>
      );
    }

    // Don't render if not authenticated or missing required role
    if (!isAuthenticated || !user) {
      return null;
    }

    if (requiredRole && user.role !== requiredRole) {
      return null;
    }

    // Render the wrapped component with user prop
    return <WrappedComponent {...(props as P)} user={user} />;
  }

  // Set display name for debugging
  AuthenticatedComponent.displayName = `withAuth(${WrappedComponent.displayName || WrappedComponent.name || 'Component'})`;

  return AuthenticatedComponent;
}

/**
 * Hook-based alternative for protecting routes.
 * Returns auth state and handles redirects.
 *
 * @example
 * function ProtectedPage() {
 *   const { user, isReady } = useRequireAuth();
 *   if (!isReady) return <Loading />;
 *   return <div>Welcome {user.name}</div>;
 * }
 */
export function useRequireAuth(options: WithAuthOptions = {}) {
  const {
    requiredRole,
    redirectTo = '/login',
    unauthorizedRedirect = '/dashboard',
  } = options;

  const router = useRouter();
  const { user, isLoading, isAuthenticated } = useAuth();

  useEffect(() => {
    if (isLoading) return;

    if (!isAuthenticated) {
      router.replace(redirectTo);
      return;
    }

    if (requiredRole && user?.role !== requiredRole) {
      router.replace(unauthorizedRedirect);
    }
  }, [isLoading, isAuthenticated, user, router, requiredRole, redirectTo, unauthorizedRedirect]);

  const isReady = !isLoading && isAuthenticated && (!requiredRole || user?.role === requiredRole);

  return {
    user,
    isLoading,
    isAuthenticated,
    isReady,
  };
}

export default withAuth;
