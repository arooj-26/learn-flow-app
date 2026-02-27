/**
 * GET /api/user/me
 * Returns current user profile from session cookie.
 */
import type { NextApiRequest, NextApiResponse } from 'next';
import { getSessionFromRequest } from '@/lib/server-auth';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') return res.status(405).json({ error: 'Method not allowed' });

  const user = getSessionFromRequest(req);
  if (!user) return res.status(401).json({ error: 'Unauthorized' });

  return res.status(200).json({
    id: user.id,
    name: user.name,
    email: user.email,
    role: user.role,
  });
}
