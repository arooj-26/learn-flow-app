/**
 * API endpoint to set user role after signup.
 * POST: Validates teacher code and returns success.
 * Role update is done client-side via localStorage.
 */
import type { NextApiRequest, NextApiResponse } from 'next';
import { getSessionFromRequest } from '@/lib/server-auth';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const user = getSessionFromRequest(req);
  if (!user) return res.status(401).json({ error: 'Unauthorized' });

  const { teacherCode } = req.body;
  const validTeacherCode = process.env.TEACHER_ACCESS_CODE || 'learnflow-teacher-2026';

  if (teacherCode !== validTeacherCode) {
    return res.status(400).json({ error: 'Invalid teacher code' });
  }

  return res.status(200).json({ success: true, role: 'teacher' });
}
