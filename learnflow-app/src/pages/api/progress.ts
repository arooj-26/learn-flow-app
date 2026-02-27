/**
 * API endpoint for user-specific progress data.
 * GET: Fetch user's progress across all modules and topics
 * POST: Update progress for a specific topic
 */
import type { NextApiRequest, NextApiResponse } from 'next';
import { Pool } from 'pg';
import { auth } from '@/lib/auth';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

// Module icons mapping
const MODULE_ICONS: Record<string, string> = {
  'Python Basics': '🔤',
  'Control Flow': '🔀',
  'Data Structures': '📦',
  'Functions': '⚙️',
  'Object-Oriented Programming': '🏗️',
  'File Handling': '📁',
  'Error Handling': '🐛',
  'Libraries & Modules': '📚',
};

// Static fallback when no database is available
function getStaticProgress() {
  const moduleNames = [
    { id: 1, name: 'Python Basics', description: 'Learn Python fundamentals: variables, strings, numbers, and I/O' },
    { id: 2, name: 'Control Flow', description: 'Master conditionals and loops to control program flow' },
    { id: 3, name: 'Data Structures', description: 'Work with lists, tuples, dictionaries, and sets' },
    { id: 4, name: 'Functions', description: 'Write reusable, modular code with functions' },
    { id: 5, name: 'Object-Oriented Programming', description: 'Build complex programs using classes and objects' },
    { id: 6, name: 'File Handling', description: 'Read, write, and manage files in Python' },
    { id: 7, name: 'Error Handling', description: 'Handle exceptions and write robust Python code' },
    { id: 8, name: 'Libraries & Modules', description: "Use Python's standard library and third-party packages" },
  ];

  const modules = moduleNames.map(m => ({
    id: String(m.id),
    name: m.name,
    description: m.description,
    icon: MODULE_ICONS[m.name] || '📚',
    mastery: 0,
    topicsCount: 8,
    exercisesDone: 0,
    quizzesDone: 0,
    quizzesTotal: 8,
    bestQuizScore: 0,
  }));

  return {
    modules,
    recentTopics: [],
    stats: {
      overallMastery: 0,
      totalExercises: 0,
      currentStreak: 0,
      modulesStarted: 0,
      totalModules: 8,
    },
  };
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    const session = await auth.api.getSession({ headers: req.headers as any });
    if (!session?.user) return res.status(401).json({ error: 'Unauthorized' });

    const userId = session.user.id;

    if (req.method === 'GET') {
      if (!process.env.DATABASE_URL) {
        return res.status(200).json(getStaticProgress());
      }
      return await getProgress(userId, res);
    } else if (req.method === 'POST') {
      if (!process.env.DATABASE_URL) return res.status(200).json({ success: true });
      return await updateProgress(userId, req.body, res);
    } else {
      return res.status(405).json({ error: 'Method not allowed' });
    }
  } catch (error) {
    console.error('Progress API error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}

async function getProgress(userId: string, res: NextApiResponse) {
  // Get all modules with their topics
  const modulesResult = await pool.query(`
    SELECT m.id, m.name, m.description, m.order_index,
           COUNT(t.id) as topics_count
    FROM modules m
    LEFT JOIN topics t ON t.module_id = m.id
    GROUP BY m.id
    ORDER BY m.order_index
  `);

  // Get user's progress for all topics using user_progress table directly
  const progressResult = await pool.query(`
    SELECT t.id as topic_id, t.name as topic_name, t.module_id,
           COALESCE(p.mastery, 0) as mastery,
           COALESCE(p.exercises_done, 0) as exercises_done,
           COALESCE(p.quiz_score, 0) as quiz_score,
           COALESCE(p.code_quality, 0) as code_quality,
           COALESCE(p.streak, 0) as streak,
           p.last_activity
    FROM topics t
    LEFT JOIN user_progress p ON p.topic_id = t.id AND p.user_id = $1
    ORDER BY t.module_id, t.order_index
  `, [userId]);

  // Get quiz results for this user
  let quizResults: any[] = [];
  try {
    const quizResultsQuery = await pool.query(`
      SELECT qr.topic_id, qr.percentage as best_score, t.module_id
      FROM quiz_results qr
      JOIN topics t ON t.id::text = qr.topic_id
      WHERE qr.user_id = $1
    `, [userId]);
    quizResults = quizResultsQuery.rows;
  } catch (error) {
    // quiz_results table might not exist yet, ignore
    console.log('Quiz results query error (non-fatal):', error);
  }

  // Calculate module-level progress
  const modules = modulesResult.rows.map(mod => {
    const moduleTopics = progressResult.rows.filter(p => p.module_id === mod.id);
    const totalMastery = moduleTopics.reduce((sum, t) => sum + parseInt(t.mastery), 0);
    const avgMastery = moduleTopics.length > 0 ? Math.round(totalMastery / moduleTopics.length) : 0;
    const exercisesDone = moduleTopics.reduce((sum, t) => sum + parseInt(t.exercises_done), 0);

    // Calculate quiz stats for this module
    const moduleTopicIds = moduleTopics.map(t => String(t.topic_id));
    const moduleQuizResults = quizResults.filter(qr => moduleTopicIds.includes(String(qr.topic_id)));
    const quizzesDone = moduleQuizResults.length;
    const quizzesTotal = moduleTopics.length;
    const bestQuizScore = moduleQuizResults.length > 0
      ? Math.max(...moduleQuizResults.map(qr => parseInt(qr.best_score)))
      : 0;

    return {
      id: mod.id,
      name: mod.name,
      description: mod.description,
      icon: MODULE_ICONS[mod.name] || '📚',
      mastery: avgMastery,
      topicsCount: parseInt(mod.topics_count),
      exercisesDone,
      quizzesDone,
      quizzesTotal,
      bestQuizScore,
    };
  });

  // Get recent topics with activity
  const recentTopics = progressResult.rows
    .filter(t => t.last_activity !== null)
    .sort((a, b) => new Date(b.last_activity).getTime() - new Date(a.last_activity).getTime())
    .slice(0, 4)
    .map(t => ({
      topic_id: t.topic_id,
      topic_name: t.topic_name,
      mastery: parseInt(t.mastery),
      level: getMasteryLevel(parseInt(t.mastery)),
      exercises_done: parseInt(t.exercises_done),
      quiz_score: parseInt(t.quiz_score),
      code_quality: parseInt(t.code_quality),
      streak: parseInt(t.streak),
    }));

  // Calculate overall stats
  const overallMastery = modules.length > 0
    ? Math.round(modules.reduce((sum, m) => sum + m.mastery, 0) / modules.length)
    : 0;
  const totalExercises = modules.reduce((sum, m) => sum + m.exercisesDone, 0);
  const modulesStarted = modules.filter(m => m.mastery > 0).length;
  const maxStreak = Math.max(0, ...progressResult.rows.map(t => parseInt(t.streak)));

  return res.status(200).json({
    modules,
    recentTopics,
    stats: {
      overallMastery,
      totalExercises,
      currentStreak: maxStreak,
      modulesStarted,
      totalModules: modules.length,
    },
  });
}

async function updateProgress(userId: string, body: any, res: NextApiResponse) {
  const { topicId, mastery, exercisesDone, quizScore, codeQuality, streak } = body;

  if (!topicId) {
    return res.status(400).json({ error: 'topicId is required' });
  }

  // Upsert progress directly using Better Auth user ID
  await pool.query(`
    INSERT INTO user_progress (user_id, topic_id, mastery, exercises_done, quiz_score, code_quality, streak, last_activity)
    VALUES ($1, $2, $3, $4, $5, $6, $7, NOW())
    ON CONFLICT (user_id, topic_id)
    DO UPDATE SET
      mastery = COALESCE($3, user_progress.mastery),
      exercises_done = COALESCE($4, user_progress.exercises_done),
      quiz_score = COALESCE($5, user_progress.quiz_score),
      code_quality = COALESCE($6, user_progress.code_quality),
      streak = COALESCE($7, user_progress.streak),
      last_activity = NOW()
  `, [userId, topicId, mastery || 0, exercisesDone || 0, quizScore || 0, codeQuality || 0, streak || 0]);

  return res.status(200).json({ success: true });
}

function getMasteryLevel(mastery: number): 'beginner' | 'learning' | 'proficient' | 'mastered' {
  if (mastery >= 91) return 'mastered';
  if (mastery >= 71) return 'proficient';
  if (mastery >= 41) return 'learning';
  return 'beginner';
}
