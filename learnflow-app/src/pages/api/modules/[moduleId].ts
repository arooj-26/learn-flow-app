/**
 * API endpoint for module details with topics
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
    const session = await auth.api.getSession({
      headers: req.headers as any,
    });

    if (!session?.user) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    const { moduleId } = req.query;
    const userId = session.user.id;

    // Get module details
    const moduleResult = await pool.query(
      'SELECT id, name, description FROM modules WHERE id = $1',
      [moduleId]
    );

    if (moduleResult.rows.length === 0) {
      return res.status(404).json({ error: 'Module not found' });
    }

    const module = moduleResult.rows[0];

    // Get topics with user progress
    const topicsResult = await pool.query(`
      SELECT
        t.id,
        t.name,
        t.description,
        t.order_index,
        COALESCE(p.mastery, 0) as mastery,
        COALESCE(p.exercises_done, 0) as exercises_done,
        6 as total_exercises
      FROM topics t
      LEFT JOIN user_progress p ON p.topic_id = t.id AND p.user_id = $1
      WHERE t.module_id = $2
      ORDER BY t.order_index
    `, [userId, moduleId]);

    return res.status(200).json({
      id: module.id,
      name: module.name,
      description: module.description,
      topics: topicsResult.rows,
    });
  } catch (error) {
    console.error('Module API error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}
