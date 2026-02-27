/**
 * Quiz API - Get quizzes for a topic
 */
import type { NextApiRequest, NextApiResponse } from 'next';
import { Pool } from 'pg';
import { auth } from '@/lib/auth';
import { getQuizzesForTopic } from '@/lib/quizzes';

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

    const { topicId } = req.query;

    if (!topicId || typeof topicId !== 'string') {
      return res.status(400).json({ error: 'Topic ID is required' });
    }

    // Get topic name from database
    const topicResult = await pool.query(
      'SELECT name FROM topics WHERE id = $1',
      [topicId]
    );

    if (topicResult.rows.length === 0) {
      return res.status(404).json({ error: 'Topic not found' });
    }

    const topicName = topicResult.rows[0].name;

    // Get quizzes for this topic
    const quizzes = getQuizzesForTopic(topicName);

    return res.status(200).json({
      topicId,
      topicName,
      quizzes,
      totalQuizzes: quizzes.length,
    });
  } catch (error) {
    console.error('Quiz API error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}
