/**
 * API endpoint for teachers to view all students and their progress.
 * GET: Fetch all students with their progress data
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

    // Check if user is a teacher (check user_roles table and "user" table)
    let isTeacher = false;
    try {
      const roleCheck = await pool.query(
        'SELECT role FROM user_roles WHERE user_id = $1',
        [session.user.id]
      );
      if (roleCheck.rows.length > 0 && roleCheck.rows[0].role === 'teacher') {
        isTeacher = true;
      }
    } catch { /* table might not exist */ }

    if (!isTeacher) {
      try {
        const userCheck = await pool.query(
          'SELECT role FROM "user" WHERE id = $1',
          [session.user.id]
        );
        if (userCheck.rows.length > 0 && userCheck.rows[0].role === 'teacher') {
          isTeacher = true;
        }
      } catch { /* role column might not exist */ }
    }

    if (!isTeacher) {
      return res.status(403).json({ error: 'Access denied. Teachers only.' });
    }

    // Get all students from Better Auth's "user" table with their progress
    const studentsResult = await pool.query(`
      SELECT
        u.id,
        u.name,
        u.email,
        u."createdAt" as created_at,
        COALESCE(AVG(p.mastery), 0)::integer as overall_mastery,
        COALESCE(SUM(p.exercises_done), 0)::integer as total_exercises,
        COUNT(DISTINCT p.topic_id)::integer as topics_started,
        MAX(p.last_activity) as last_activity
      FROM "user" u
      LEFT JOIN user_progress p ON p.user_id = u.id
      LEFT JOIN user_roles ur ON ur.user_id = u.id
      WHERE ur.role IS NULL OR ur.role = 'student'
      GROUP BY u.id, u.name, u.email, u."createdAt"
      ORDER BY u."createdAt" DESC
    `);

    // Get module-level progress for each student
    const students = await Promise.all(studentsResult.rows.map(async (student) => {
      const moduleProgress = await pool.query(`
        SELECT
          m.name as module_name,
          COALESCE(AVG(p.mastery), 0)::integer as mastery,
          COUNT(DISTINCT p.topic_id)::integer as topics_completed
        FROM modules m
        LEFT JOIN topics t ON t.module_id = m.id
        LEFT JOIN user_progress p ON p.topic_id = t.id AND p.user_id = $1
        GROUP BY m.id, m.name, m.order_index
        ORDER BY m.order_index
      `, [student.id]);

      return {
        id: student.id,
        name: student.name,
        email: student.email,
        joinedAt: student.created_at,
        overallMastery: student.overall_mastery,
        totalExercises: student.total_exercises,
        topicsStarted: student.topics_started,
        lastActivity: student.last_activity,
        moduleProgress: moduleProgress.rows,
      };
    }));

    // Get class statistics
    const totalStudents = students.length;
    const avgMastery = totalStudents > 0
      ? Math.round(students.reduce((sum, s) => sum + s.overallMastery, 0) / totalStudents)
      : 0;
    const activeToday = students.filter(s => {
      if (!s.lastActivity) return false;
      const today = new Date();
      const lastActive = new Date(s.lastActivity);
      return lastActive.toDateString() === today.toDateString();
    }).length;

    return res.status(200).json({
      students,
      stats: {
        totalStudents,
        avgMastery,
        activeToday,
      },
    });
  } catch (error) {
    console.error('Teacher students API error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}
