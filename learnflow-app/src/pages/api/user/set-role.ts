/**
 * API endpoint to set user role after signup.
 * POST: Set role to 'teacher' if valid teacher code is provided
 */
import type { NextApiRequest, NextApiResponse } from 'next';
import { Pool } from 'pg';
import { auth } from '@/lib/auth';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
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

    const { teacherCode } = req.body;
    const validTeacherCode = process.env.TEACHER_ACCESS_CODE || 'learnflow-teacher-2026';

    // Validate teacher code
    if (teacherCode !== validTeacherCode) {
      return res.status(400).json({ error: 'Invalid teacher code' });
    }

    const userId = session.user.id;

    // Update role in Better Auth's user table
    try {
      await pool.query(
        'UPDATE "user" SET role = $1 WHERE id = $2',
        ['teacher', userId]
      );
    } catch {
      // role column might not exist
    }

    // Also save in user_roles table
    await pool.query(`
      INSERT INTO user_roles (user_id, role)
      VALUES ($1, 'teacher')
      ON CONFLICT (user_id) DO UPDATE SET role = 'teacher'
    `, [userId]);

    return res.status(200).json({ success: true, role: 'teacher' });
  } catch (error) {
    console.error('Set role API error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}
