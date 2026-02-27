/**
 * Modules API - Get all modules with their topics
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
    // Verify authentication
    const session = await auth.api.getSession({
      headers: req.headers as any,
    });

    if (!session?.user) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    // Fetch all modules with their topics
    const modulesResult = await pool.query(`
      SELECT
        m.id,
        m.name,
        m.description,
        m.order_index
      FROM modules m
      ORDER BY m.order_index ASC
    `);

    const topicsResult = await pool.query(`
      SELECT
        t.id,
        t.name,
        t.module_id,
        t.order_index
      FROM topics t
      ORDER BY t.order_index ASC
    `);

    // Group topics by module
    const topicsByModule: Record<string, Array<{ id: string; name: string }>> = {};
    for (const topic of topicsResult.rows) {
      if (!topicsByModule[topic.module_id]) {
        topicsByModule[topic.module_id] = [];
      }
      topicsByModule[topic.module_id].push({
        id: topic.id,
        name: topic.name,
      });
    }

    // Build response
    const modules = modulesResult.rows.map((module) => ({
      id: module.id,
      name: module.name,
      description: module.description,
      topics: topicsByModule[module.id] || [],
    }));

    return res.status(200).json({ modules });
  } catch (error) {
    console.error('Modules API error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}
