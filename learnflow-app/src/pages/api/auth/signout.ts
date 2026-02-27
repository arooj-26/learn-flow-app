/**
 * POST /api/auth/signout
 * Clears the session cookie.
 */
import type { NextApiRequest, NextApiResponse } from 'next';
import { clearSessionCookie } from '@/lib/server-auth';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') return res.status(405).end();
  res.setHeader('Set-Cookie', clearSessionCookie());
  res.status(200).json({ ok: true });
}
