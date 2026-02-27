/**
 * Server-side auth for LearnFlow API routes.
 * Uses signed JWT cookies — no database required.
 */
export { getSessionFromRequest } from './server-auth';

// Compatibility shim so existing API routes still work:
// const session = await auth.api.getSession({ headers: req.headers });
import { getSessionFromRequest } from './server-auth';

export const auth = {
  api: {
    getSession: async ({ headers }: { headers: Record<string, string | string[] | undefined> }) => {
      const req = { headers: { cookie: Array.isArray(headers.cookie) ? headers.cookie[0] : (headers.cookie || '') } };
      const user = getSessionFromRequest(req);
      if (!user) return null;
      return { user };
    },
  },
};

export type Session = { user: { id: string; name: string; email: string; role: string } };
export type User = Session['user'];
