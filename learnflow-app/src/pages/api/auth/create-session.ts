/**
 * POST /api/auth/create-session
 * Creates a server-side session cookie from client-provided user data.
 * Called automatically after client-side sign-in/sign-up.
 */
import type { NextApiRequest, NextApiResponse } from 'next';
import { makeSessionCookie } from '@/lib/server-auth';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') return res.status(405).end();

  const { id, name, email, role } = req.body || {};
  if (!id || !email) return res.status(400).json({ error: 'Missing user data' });

  res.setHeader('Set-Cookie', makeSessionCookie({ id, name: name || '', email, role: role || 'student' }));
  res.status(200).json({ ok: true });
}
