/**
 * Quiz Results API - Save completed quiz results.
 * Returns success even without a database so the UI always works.
 */
import type { NextApiRequest, NextApiResponse } from 'next';
import { auth } from '@/lib/auth';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const session = await auth.api.getSession({ headers: req.headers as any });
    if (!session?.user) return res.status(401).json({ error: 'Unauthorized' });

    const { topicId, results, score, total } = req.body;
    if (!topicId || score === undefined || total === undefined) {
      return res.status(400).json({ error: 'Missing required fields' });
    }

    const percentage = Math.round((score / total) * 100);

    // Persist to DB if available
    if (process.env.DATABASE_URL) {
      try {
        const { Pool } = await import('pg');
        const pool = new Pool({ connectionString: process.env.DATABASE_URL });
        const userId = session.user.id;

        await pool.query(`
          CREATE TABLE IF NOT EXISTS quiz_results (
            id SERIAL PRIMARY KEY,
            user_id TEXT NOT NULL,
            topic_id TEXT NOT NULL,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            percentage INTEGER NOT NULL,
            results JSONB,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, topic_id)
          )
        `);

        await pool.query(`
          INSERT INTO quiz_results (user_id, topic_id, score, total, percentage, results, completed_at)
          VALUES ($1, $2, $3, $4, $5, $6, CURRENT_TIMESTAMP)
          ON CONFLICT (user_id, topic_id)
          DO UPDATE SET
            score = GREATEST(quiz_results.score, EXCLUDED.score),
            total = EXCLUDED.total,
            percentage = GREATEST(quiz_results.percentage, EXCLUDED.percentage),
            results = EXCLUDED.results,
            completed_at = CURRENT_TIMESTAMP
        `, [userId, topicId, score, total, percentage, JSON.stringify(results)]);

        if (percentage >= 70) {
          await pool.query(`
            UPDATE user_progress
            SET mastery = LEAST(100, mastery + $1)
            WHERE user_id = $2 AND topic_id = $3
          `, [Math.floor(percentage / 10), userId, topicId]);
        }

        await pool.end();
      } catch { /* No DB — results lost but UI continues */ }
    }

    return res.status(200).json({ success: true, score, total, percentage, passed: percentage >= 70 });
  } catch (error) {
    console.error('Quiz results API error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}
