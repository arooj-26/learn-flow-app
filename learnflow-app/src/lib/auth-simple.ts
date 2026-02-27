/**
 * Simple client-side auth using localStorage.
 * No database required - works on Vercel and any hosting.
 */

interface StoredUser {
  id: string;
  name: string;
  email: string;
  passwordHash: string;
  role: string;
  createdAt: string;
}

interface SessionUser {
  id: string;
  name: string;
  email: string;
  role: string;
}

async function sha256(str: string): Promise<string> {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(str));
  return Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, '0')).join('');
}

function generateId(): string {
  return Date.now().toString(36) + Math.random().toString(36).slice(2);
}

function getUsers(): StoredUser[] {
  if (typeof window === 'undefined') return [];
  try { return JSON.parse(localStorage.getItem('lf_users') || '[]'); } catch { return []; }
}

function saveUsers(users: StoredUser[]): void {
  localStorage.setItem('lf_users', JSON.stringify(users));
}

export function getStoredSession(): SessionUser | null {
  if (typeof window === 'undefined') return null;
  try {
    const s = localStorage.getItem('lf_session');
    return s ? JSON.parse(s) : null;
  } catch { return null; }
}

function saveSession(user: SessionUser): void {
  localStorage.setItem('lf_session', JSON.stringify(user));
}

export function clearSession(): void {
  if (typeof window !== 'undefined') localStorage.removeItem('lf_session');
}

export async function localSignUp(name: string, email: string, password: string): Promise<{ user?: SessionUser; error?: string }> {
  const users = getUsers();
  const emailLower = email.toLowerCase().trim();

  if (users.find(u => u.email === emailLower)) {
    return { error: 'An account with this email already exists' };
  }

  const passwordHash = await sha256(password + emailLower);
  const user: StoredUser = {
    id: generateId(),
    name: name.trim(),
    email: emailLower,
    passwordHash,
    role: 'student',
    createdAt: new Date().toISOString(),
  };

  users.push(user);
  saveUsers(users);

  const sessionUser: SessionUser = { id: user.id, name: user.name, email: user.email, role: user.role };
  saveSession(sessionUser);
  return { user: sessionUser };
}

export async function localSignIn(email: string, password: string): Promise<{ user?: SessionUser; error?: string }> {
  const users = getUsers();
  const emailLower = email.toLowerCase().trim();
  const user = users.find(u => u.email === emailLower);

  if (!user) return { error: 'Invalid email or password' };

  const passwordHash = await sha256(password + emailLower);
  if (user.passwordHash !== passwordHash) return { error: 'Invalid email or password' };

  const sessionUser: SessionUser = { id: user.id, name: user.name, email: user.email, role: user.role };
  saveSession(sessionUser);
  return { user: sessionUser };
}

export function localSignOut(): void {
  clearSession();
}

export function updateLocalRole(userId: string, role: string): void {
  const users = getUsers();
  const idx = users.findIndex(u => u.id === userId);
  if (idx !== -1) {
    users[idx].role = role;
    saveUsers(users);
    const session = getStoredSession();
    if (session?.id === userId) saveSession({ ...session, role });
  }
}
