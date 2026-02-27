/**
 * API endpoint to get current user's profile including role.
 * GET: Fetch user profile with role
 */
import type { NextApiRequest, NextApiResponse } from 'next';
import { Pool } from 'pg';
import { auth } from '@/lib/auth';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Get session from Better Auth
    const session = await auth.api.getSession({
      headers: req.headers as any,
    });

    if (!session?.user) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    const { email, name, id } = session.user;

    // Get role from user_roles table (or default to student)
    let role = 'student';
    try {
      const roleResult = await pool.query(
        'SELECT role FROM user_roles WHERE user_id = $1',
        [id]
      );
      if (roleResult.rows.length > 0) {
        role = roleResult.rows[0].role;
      }
    } catch {
      // user_roles table might not exist yet
    }

    // Also check the role column on the "user" table
    try {
      const userResult = await pool.query(
        'SELECT role FROM "user" WHERE id = $1',
        [id]
      );
      if (userResult.rows.length > 0 && userResult.rows[0].role) {
        role = userResult.rows[0].role;
      }
    } catch {
      // role column might not exist
    }

    return res.status(200).json({
      id,
      name,
      email,
      role,
    });
  } catch (error) {
    console.error('User me API error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}
