/**
 * Server-side auth utilities using signed JWT cookies.
 * No database required.
 */
import crypto from 'crypto';

export interface SessionUser {
  id: string;
  name: string;
  email: string;
  role: string;
}

function getSecret(): string {
  return process.env.BETTER_AUTH_SECRET || process.env.JWT_SECRET || 'learnflow-demo-secret-change-in-prod';
}

export function signJWT(payload: object, expiresInSeconds = 60 * 60 * 24 * 30): string {
  const header = Buffer.from(JSON.stringify({ alg: 'HS256', typ: 'JWT' })).toString('base64url');
  const body = Buffer.from(JSON.stringify({
    ...payload,
    iat: Math.floor(Date.now() / 1000),
    exp: Math.floor(Date.now() / 1000) + expiresInSeconds,
  })).toString('base64url');
  const sig = crypto.createHmac('sha256', getSecret()).update(`${header}.${body}`).digest('base64url');
  return `${header}.${body}.${sig}`;
}

export function verifyJWT<T = Record<string, unknown>>(token: string): T | null {
  try {
    const parts = token.split('.');
    if (parts.length !== 3) return null;
    const [header, body, sig] = parts;
    const expectedSig = crypto.createHmac('sha256', getSecret()).update(`${header}.${body}`).digest('base64url');
    if (sig !== expectedSig) return null;
    const payload = JSON.parse(Buffer.from(body, 'base64url').toString()) as T & { exp?: number };
    if (payload.exp && payload.exp < Math.floor(Date.now() / 1000)) return null;
    return payload;
  } catch {
    return null;
  }
}

function parseCookies(cookieHeader: string): Record<string, string> {
  return Object.fromEntries(
    cookieHeader.split(';')
      .map(c => c.trim().split('='))
      .filter(([k]) => k)
      .map(([k, ...v]) => [k.trim(), decodeURIComponent(v.join('='))])
  );
}

export function getSessionFromRequest(req: { headers: { cookie?: string } }): SessionUser | null {
  const cookies = parseCookies(req.headers.cookie || '');
  const token = cookies['lf_session'];
  if (!token) return null;
  const payload = verifyJWT<SessionUser & { exp: number }>(token);
  if (!payload?.id) return null;
  return { id: payload.id, name: payload.name, email: payload.email, role: payload.role };
}

export function makeSessionCookie(user: SessionUser): string {
  const token = signJWT({ id: user.id, name: user.name, email: user.email, role: user.role });
  const secure = process.env.NODE_ENV === 'production' ? '; Secure' : '';
  return `lf_session=${token}; HttpOnly; Path=/; SameSite=Lax; Max-Age=2592000${secure}`;
}

export function clearSessionCookie(): string {
  return 'lf_session=; HttpOnly; Path=/; SameSite=Lax; Max-Age=0';
}
