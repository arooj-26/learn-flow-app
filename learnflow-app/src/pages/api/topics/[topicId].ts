/**
 * API endpoint for topic details with content and exercises
 * Content is loaded from markdown files in /content/modules/
 */
import type { NextApiRequest, NextApiResponse } from 'next';
import { Pool } from 'pg';
import { auth } from '@/lib/auth';
import { parseTopicContent } from '@/lib/content-parser';

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

    const { topicId } = req.query;
    const userId = session.user.id;

    // Get topic details with module info
    const topicResult = await pool.query(`
      SELECT t.id, t.name, t.description, t.module_id, m.name as module_name
      FROM topics t
      JOIN modules m ON m.id = t.module_id
      WHERE t.id = $1
    `, [topicId]);

    if (topicResult.rows.length === 0) {
      return res.status(404).json({ error: 'Topic not found' });
    }

    const topic = topicResult.rows[0];

    // Get user progress for this topic
    let progress = { mastery: 0, exercises_done: 0 };
    try {
      const progressResult = await pool.query(`
        SELECT mastery, exercises_done
        FROM user_progress
        WHERE topic_id = $1 AND user_id = $2
      `, [topicId, userId]);
      if (progressResult.rows.length > 0) {
        progress = progressResult.rows[0];
      }
    } catch { /* table might not exist yet */ }

    // Get completed exercises for this user
    let completedExerciseIds = new Set<string>();
    try {
      const completedResult = await pool.query(`
        SELECT exercise_id
        FROM code_submissions
        WHERE topic_id = $1 AND user_id = $2 AND passed = true
      `, [topicId, userId]);
      completedExerciseIds = new Set(completedResult.rows.map(r => r.exercise_id));
    } catch { /* code_submissions table might not exist yet */ }

    // Load content and exercises from markdown file
    const { content, exercises } = parseTopicContent(topic.name);

    // Mark completed exercises and add topic-specific IDs
    const exercisesWithCompletion = exercises.map((ex, index) => {
      const exerciseId = `${topicId}-ex-${index + 1}`;
      return {
        ...ex,
        id: exerciseId,
        completed: completedExerciseIds.has(exerciseId),
      };
    });

    return res.status(200).json({
      id: topic.id,
      name: topic.name,
      description: topic.description,
      module_id: topic.module_id,
      module_name: topic.module_name,
      content,
      exercises: exercisesWithCompletion,
      mastery: progress.mastery,
      exercises_done: progress.exercises_done,
    });
  } catch (error) {
    console.error('Topic API error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}
