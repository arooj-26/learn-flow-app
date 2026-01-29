/**
 * Better Auth catch-all API route handler for Next.js Pages Router.
 * Handles all authentication endpoints:
 * - POST /api/auth/sign-up/email
 * - POST /api/auth/sign-in/email
 * - POST /api/auth/sign-in/social
 * - POST /api/auth/sign-out
 * - GET /api/auth/session
 * - GET /api/auth/callback/:provider
 */
import { auth } from '@/lib/auth';
import { toNodeHandler } from 'better-auth/node';

// Disable body parsing - Better Auth handles this
export const config = {
  api: {
    bodyParser: false,
  },
};

export default toNodeHandler(auth.handler);
