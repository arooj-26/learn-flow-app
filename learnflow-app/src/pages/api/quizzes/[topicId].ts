/**
 * Quiz API - Get quizzes for a topic.
 * Uses static topic map when database is unavailable.
 */
import type { NextApiRequest, NextApiResponse } from 'next';
import { auth } from '@/lib/auth';
import { getQuizzesForTopic } from '@/lib/quizzes';

// Static topic ID → name (matches TOPIC_QUIZZES keys where possible)
const STATIC_TOPIC_NAMES: Record<number, string> = {
  // Python Basics
  1:  'Variables & Types',
  2:  'Operators',
  3:  'Strings',
  4:  'Strings',
  5:  'Variables & Types',
  6:  'Input/Output',
  7:  'Variables & Types',
  8:  'Variables & Types',
  // Control Flow
  9:  'If Statements',
  10: 'If Statements',
  11: 'Operators',
  12: 'Operators',
  13: 'While Loops',
  14: 'For Loops',
  15: 'Break & Continue',
  16: 'For Loops',
  // Data Structures
  17: 'Lists',
  18: 'Lists',
  19: 'Tuples',
  20: 'Dictionaries',
  21: 'Dictionaries',
  22: 'Sets',
  23: 'List Comprehensions',
  24: 'Lists',
  // Functions
  25: 'Defining Functions',
  26: 'Arguments',
  27: 'Return Values',
  28: 'Arguments',
  29: 'Scope',
  30: 'Lambda Functions',
  31: 'Defining Functions',
  32: 'Defining Functions',
  // OOP
  33: 'Classes',
  34: 'Objects',
  35: 'Methods',
  36: 'Classes',
  37: 'Inheritance',
  38: 'Methods',
  39: 'Polymorphism',
  40: 'Classes',
  // File Handling
  41: 'Reading Files',
  42: 'Reading Files',
  43: 'Writing Files',
  44: 'File Context',
  45: 'JSON & CSV',
  46: 'JSON & CSV',
  47: 'File Context',
  48: 'Reading Files',
  // Error Handling
  49: 'Try/Except',
  50: 'Exception Types',
  51: 'Try/Except',
  52: 'Raising Exceptions',
  53: 'Custom Exceptions',
  54: 'Try/Except',
  55: 'Standard Library',
  56: 'Try/Except',
  // Libraries & Modules
  57: 'Import Statements',
  58: 'Standard Library',
  59: 'Standard Library',
  60: 'Standard Library',
  61: 'Standard Library',
  62: 'Standard Library',
  63: 'pip & packages',
  64: 'Virtual Environments',
};

// Human-readable names for display (matches the static topic names)
const DISPLAY_NAMES: Record<number, string> = {
  1: 'Variables & Data Types', 2: 'Numbers & Math', 3: 'Strings', 4: 'String Methods',
  5: 'Type Conversion', 6: 'Input & Output', 7: 'Comments & Style', 8: 'Boolean Logic',
  9: 'If Statements', 10: 'Elif & Else', 11: 'Comparison Operators', 12: 'Logical Operators',
  13: 'While Loops', 14: 'For Loops', 15: 'Break & Continue', 16: 'Nested Loops',
  17: 'Lists', 18: 'List Methods', 19: 'Tuples', 20: 'Dictionaries',
  21: 'Dictionary Methods', 22: 'Sets', 23: 'List Comprehensions', 24: 'Nested Structures',
  25: 'Defining Functions', 26: 'Parameters & Arguments', 27: 'Return Values', 28: 'Default Parameters',
  29: 'Variable Scope', 30: 'Lambda Functions', 31: 'Recursion', 32: 'Decorators',
  33: 'Classes & Objects', 34: 'Constructors', 35: 'Instance Methods', 36: 'Class Variables',
  37: 'Inheritance', 38: 'Method Overriding', 39: 'Polymorphism', 40: 'Encapsulation',
  41: 'Opening Files', 42: 'Reading Files', 43: 'Writing Files', 44: 'File Modes',
  45: 'CSV Files', 46: 'JSON Files', 47: 'Context Managers', 48: 'File Paths',
  49: 'Try & Except', 50: 'Multiple Exceptions', 51: 'Finally Block', 52: 'Raising Exceptions',
  53: 'Custom Exceptions', 54: 'Assertions', 55: 'Logging', 56: 'Debugging Techniques',
  57: 'Importing Modules', 58: 'Standard Library', 59: 'Math Module', 60: 'Random Module',
  61: 'Datetime Module', 62: 'OS Module', 63: 'pip & Packages', 64: 'Virtual Environments',
};

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') return res.status(405).json({ error: 'Method not allowed' });

  try {
    const session = await auth.api.getSession({ headers: req.headers as any });
    if (!session?.user) return res.status(401).json({ error: 'Unauthorized' });

    const topicId = Number(req.query.topicId);

    // Try database first
    if (process.env.DATABASE_URL) {
      try {
        const { Pool } = await import('pg');
        const pool = new Pool({ connectionString: process.env.DATABASE_URL });
        const topicResult = await pool.query('SELECT name FROM topics WHERE id = $1', [topicId]);
        await pool.end();
        if (topicResult.rows.length > 0) {
          const topicName = topicResult.rows[0].name;
          const quizzes = getQuizzesForTopic(topicName);
          return res.status(200).json({ topicId, topicName, quizzes, totalQuizzes: quizzes.length });
        }
      } catch { /* Fall through */ }
    }

    // Static fallback — map topic ID to quiz key
    const quizKey = STATIC_TOPIC_NAMES[topicId];
    const displayName = DISPLAY_NAMES[topicId];
    if (!quizKey || !displayName) return res.status(404).json({ error: 'Topic not found' });

    const quizzes = getQuizzesForTopic(quizKey);
    return res.status(200).json({ topicId, topicName: displayName, quizzes, totalQuizzes: quizzes.length });
  } catch (error) {
    console.error('Quiz API error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}
