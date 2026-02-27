/**
 * GET /api/auth/session
 * Returns the current user from the signed session cookie.
 */
import type { NextApiRequest, NextApiResponse } from 'next';
import { getSessionFromRequest } from '@/lib/server-auth';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') return res.status(405).end();
  const user = getSessionFromRequest(req);
  if (!user) return res.status(200).json(null);
  return res.status(200).json({ user, session: { token: 'cookie' } });
}
