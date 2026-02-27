/**
 * Catch-all auth handler — delegates to specific auth endpoints.
 * Kept for backward compatibility only.
 */
import type { NextApiRequest, NextApiResponse } from 'next';
import { getSessionFromRequest, makeSessionCookie, clearSessionCookie } from '@/lib/server-auth';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  const { all } = req.query;
  const path = Array.isArray(all) ? all.join('/') : all || '';

  // GET /api/auth/get-session or /api/auth/session
  if (req.method === 'GET' && (path === 'get-session' || path === 'session')) {
    const user = getSessionFromRequest(req);
    return res.status(200).json(user ? { user, session: { token: 'cookie' } } : null);
  }

  // POST /api/auth/sign-out
  if (req.method === 'POST' && path === 'sign-out') {
    res.setHeader('Set-Cookie', clearSessionCookie());
    return res.status(200).json({ ok: true });
  }

  // POST /api/auth/create-session
  if (req.method === 'POST' && path === 'create-session') {
    const { id, name, email, role } = req.body || {};
    if (!id || !email) return res.status(400).json({ error: 'Missing user data' });
    res.setHeader('Set-Cookie', makeSessionCookie({ id, name: name || '', email, role: role || 'student' }));
    return res.status(200).json({ ok: true });
  }

  return res.status(404).json({ error: 'Auth endpoint not found' });
}
