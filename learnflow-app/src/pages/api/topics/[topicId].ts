/**
 * API endpoint for topic details with content and exercises.
 * Content loaded from markdown files in /content/modules/.
 * Uses static metadata when database is unavailable.
 */
import type { NextApiRequest, NextApiResponse } from 'next';
import { auth } from '@/lib/auth';
import { parseTopicContent } from '@/lib/content-parser';

// Flat lookup: topicId → { name, description, module_id, module_name }
const STATIC_TOPICS: Record<number, { name: string; description: string; module_id: number; module_name: string }> = {
  1:  { name: 'Variables & Data Types',  description: 'Store and work with data', module_id: 1, module_name: 'Python Basics' },
  2:  { name: 'Numbers & Math',           description: 'Arithmetic and math operations', module_id: 1, module_name: 'Python Basics' },
  3:  { name: 'Strings',                  description: 'Working with text data', module_id: 1, module_name: 'Python Basics' },
  4:  { name: 'String Methods',           description: 'Built-in string methods', module_id: 1, module_name: 'Python Basics' },
  5:  { name: 'Type Conversion',          description: 'Converting between data types', module_id: 1, module_name: 'Python Basics' },
  6:  { name: 'Input & Output',           description: 'Reading user input and displaying output', module_id: 1, module_name: 'Python Basics' },
  7:  { name: 'Comments & Style',         description: 'Writing clean Python code', module_id: 1, module_name: 'Python Basics' },
  8:  { name: 'Boolean Logic',            description: 'True/False and logical operations', module_id: 1, module_name: 'Python Basics' },
  9:  { name: 'If Statements',            description: 'Conditional execution', module_id: 2, module_name: 'Control Flow' },
  10: { name: 'Elif & Else',              description: 'Multiple conditions', module_id: 2, module_name: 'Control Flow' },
  11: { name: 'Comparison Operators',     description: '==, !=, <, >, <=, >=', module_id: 2, module_name: 'Control Flow' },
  12: { name: 'Logical Operators',        description: 'and, or, not', module_id: 2, module_name: 'Control Flow' },
  13: { name: 'While Loops',              description: 'Repeat while condition is true', module_id: 2, module_name: 'Control Flow' },
  14: { name: 'For Loops',                description: 'Iterate over sequences', module_id: 2, module_name: 'Control Flow' },
  15: { name: 'Break & Continue',         description: 'Control loop execution', module_id: 2, module_name: 'Control Flow' },
  16: { name: 'Nested Loops',             description: 'Loops inside loops', module_id: 2, module_name: 'Control Flow' },
  17: { name: 'Lists',                    description: 'Ordered mutable sequences', module_id: 3, module_name: 'Data Structures' },
  18: { name: 'List Methods',             description: 'append, remove, sort, and more', module_id: 3, module_name: 'Data Structures' },
  19: { name: 'Tuples',                   description: 'Immutable ordered sequences', module_id: 3, module_name: 'Data Structures' },
  20: { name: 'Dictionaries',             description: 'Key-value pairs', module_id: 3, module_name: 'Data Structures' },
  21: { name: 'Dictionary Methods',       description: 'keys, values, items, and more', module_id: 3, module_name: 'Data Structures' },
  22: { name: 'Sets',                     description: 'Unique unordered collections', module_id: 3, module_name: 'Data Structures' },
  23: { name: 'List Comprehensions',      description: 'Concise list creation', module_id: 3, module_name: 'Data Structures' },
  24: { name: 'Nested Structures',        description: 'Lists of dicts and complex data', module_id: 3, module_name: 'Data Structures' },
  25: { name: 'Defining Functions',       description: 'Creating functions with def', module_id: 4, module_name: 'Functions' },
  26: { name: 'Parameters & Arguments',   description: 'Passing data to functions', module_id: 4, module_name: 'Functions' },
  27: { name: 'Return Values',            description: 'Getting data back from functions', module_id: 4, module_name: 'Functions' },
  28: { name: 'Default Parameters',       description: 'Optional function arguments', module_id: 4, module_name: 'Functions' },
  29: { name: 'Variable Scope',           description: 'Local and global variables', module_id: 4, module_name: 'Functions' },
  30: { name: 'Lambda Functions',         description: 'Anonymous inline functions', module_id: 4, module_name: 'Functions' },
  31: { name: 'Recursion',                description: 'Functions that call themselves', module_id: 4, module_name: 'Functions' },
  32: { name: 'Decorators',               description: 'Wrapping and enhancing functions', module_id: 4, module_name: 'Functions' },
  33: { name: 'Classes & Objects',        description: 'Creating blueprints for data', module_id: 5, module_name: 'Object-Oriented Programming' },
  34: { name: 'Constructors',             description: 'Initializing objects with __init__', module_id: 5, module_name: 'Object-Oriented Programming' },
  35: { name: 'Instance Methods',         description: 'Functions that belong to objects', module_id: 5, module_name: 'Object-Oriented Programming' },
  36: { name: 'Class Variables',          description: 'Shared data across instances', module_id: 5, module_name: 'Object-Oriented Programming' },
  37: { name: 'Inheritance',              description: 'Creating subclasses', module_id: 5, module_name: 'Object-Oriented Programming' },
  38: { name: 'Method Overriding',        description: 'Customizing inherited methods', module_id: 5, module_name: 'Object-Oriented Programming' },
  39: { name: 'Polymorphism',             description: 'Same interface, different behavior', module_id: 5, module_name: 'Object-Oriented Programming' },
  40: { name: 'Encapsulation',            description: 'Hiding implementation details', module_id: 5, module_name: 'Object-Oriented Programming' },
  41: { name: 'Opening Files',            description: 'The open() function', module_id: 6, module_name: 'File Handling' },
  42: { name: 'Reading Files',            description: 'read(), readline(), readlines()', module_id: 6, module_name: 'File Handling' },
  43: { name: 'Writing Files',            description: 'Writing and appending to files', module_id: 6, module_name: 'File Handling' },
  44: { name: 'File Modes',               description: 'r, w, a, rb, wb modes', module_id: 6, module_name: 'File Handling' },
  45: { name: 'CSV Files',                description: 'Working with CSV data', module_id: 6, module_name: 'File Handling' },
  46: { name: 'JSON Files',               description: 'Reading and writing JSON', module_id: 6, module_name: 'File Handling' },
  47: { name: 'Context Managers',         description: 'The with statement', module_id: 6, module_name: 'File Handling' },
  48: { name: 'File Paths',               description: 'os.path and pathlib', module_id: 6, module_name: 'File Handling' },
  49: { name: 'Try & Except',             description: 'Catching and handling errors', module_id: 7, module_name: 'Error Handling' },
  50: { name: 'Multiple Exceptions',      description: 'Handling different error types', module_id: 7, module_name: 'Error Handling' },
  51: { name: 'Finally Block',            description: 'Code that always runs', module_id: 7, module_name: 'Error Handling' },
  52: { name: 'Raising Exceptions',       description: 'Throwing errors intentionally', module_id: 7, module_name: 'Error Handling' },
  53: { name: 'Custom Exceptions',        description: 'Creating your own exception types', module_id: 7, module_name: 'Error Handling' },
  54: { name: 'Assertions',               description: 'assert statements for debugging', module_id: 7, module_name: 'Error Handling' },
  55: { name: 'Logging',                  description: 'The logging module', module_id: 7, module_name: 'Error Handling' },
  56: { name: 'Debugging Techniques',     description: 'Finding and fixing bugs', module_id: 7, module_name: 'Error Handling' },
  57: { name: 'Importing Modules',        description: 'import and from...import', module_id: 8, module_name: 'Libraries & Modules' },
  58: { name: 'Standard Library',         description: "Python's built-in modules", module_id: 8, module_name: 'Libraries & Modules' },
  59: { name: 'Math Module',              description: 'Mathematical functions', module_id: 8, module_name: 'Libraries & Modules' },
  60: { name: 'Random Module',            description: 'Random number generation', module_id: 8, module_name: 'Libraries & Modules' },
  61: { name: 'Datetime Module',          description: 'Working with dates and times', module_id: 8, module_name: 'Libraries & Modules' },
  62: { name: 'OS Module',                description: 'Operating system interface', module_id: 8, module_name: 'Libraries & Modules' },
  63: { name: 'pip & Packages',           description: 'Installing third-party packages', module_id: 8, module_name: 'Libraries & Modules' },
  64: { name: 'Virtual Environments',     description: 'Isolating project dependencies', module_id: 8, module_name: 'Libraries & Modules' },
};

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') return res.status(405).json({ error: 'Method not allowed' });

  try {
    const session = await auth.api.getSession({ headers: req.headers as any });
    if (!session?.user) return res.status(401).json({ error: 'Unauthorized' });

    const topicId = Number(req.query.topicId);
    const userId = session.user.id;

    // Try database first, fall back to static data
    if (process.env.DATABASE_URL) {
      try {
        const { Pool } = await import('pg');
        const pool = new Pool({ connectionString: process.env.DATABASE_URL });

        const topicResult = await pool.query(`
          SELECT t.id, t.name, t.description, t.module_id, m.name as module_name
          FROM topics t JOIN modules m ON m.id = t.module_id WHERE t.id = $1
        `, [topicId]);

        if (topicResult.rows.length > 0) {
          const topic = topicResult.rows[0];
          let progress = { mastery: 0, exercises_done: 0 };
          let completedExerciseIds = new Set<string>();

          try {
            const pr = await pool.query('SELECT mastery, exercises_done FROM user_progress WHERE topic_id=$1 AND user_id=$2', [topicId, userId]);
            if (pr.rows.length > 0) progress = pr.rows[0];
          } catch { /* ok */ }

          try {
            const cr = await pool.query('SELECT exercise_id FROM code_submissions WHERE topic_id=$1 AND user_id=$2 AND passed=true', [topicId, userId]);
            completedExerciseIds = new Set(cr.rows.map((r: { exercise_id: string }) => r.exercise_id));
          } catch { /* ok */ }

          await pool.end();
          const { content, exercises } = parseTopicContent(topic.name);
          return res.status(200).json({
            ...topic,
            content,
            exercises: exercises.map((ex, i) => ({ ...ex, id: `${topicId}-ex-${i + 1}`, completed: completedExerciseIds.has(`${topicId}-ex-${i + 1}`) })),
            mastery: progress.mastery,
            exercises_done: progress.exercises_done,
          });
        }
        await pool.end();
      } catch { /* Fall through to static */ }
    }

    // Static fallback
    const topic = STATIC_TOPICS[topicId];
    if (!topic) return res.status(404).json({ error: 'Topic not found' });

    const { content, exercises } = parseTopicContent(topic.name);

    return res.status(200).json({
      id: String(topicId),
      name: topic.name,
      description: topic.description,
      module_id: topic.module_id,
      module_name: topic.module_name,
      content,
      exercises: exercises.map((ex, i) => ({ ...ex, id: `${topicId}-ex-${i + 1}`, completed: false })),
      mastery: 0,
      exercises_done: 0,
    });
  } catch (error) {
    console.error('Topic API error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}
