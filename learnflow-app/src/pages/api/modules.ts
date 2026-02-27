/**
 * Modules API - Returns all modules with their topics.
 * Uses static data when database is unavailable.
 */
import type { NextApiRequest, NextApiResponse } from 'next';
import { auth } from '@/lib/auth';

// Static module/topic data matching the content files
const STATIC_MODULES = [
  {
    id: 1, name: 'Python Basics', description: 'Learn Python fundamentals: variables, strings, numbers, and I/O', order_index: 1,
    topics: [
      { id: 1, name: 'Variables & Data Types', description: 'Store and work with data', order_index: 1 },
      { id: 2, name: 'Numbers & Math', description: 'Arithmetic and math operations', order_index: 2 },
      { id: 3, name: 'Strings', description: 'Working with text data', order_index: 3 },
      { id: 4, name: 'String Methods', description: 'Built-in string methods', order_index: 4 },
      { id: 5, name: 'Type Conversion', description: 'Converting between data types', order_index: 5 },
      { id: 6, name: 'Input & Output', description: 'Reading user input and displaying output', order_index: 6 },
      { id: 7, name: 'Comments & Style', description: 'Writing clean Python code', order_index: 7 },
      { id: 8, name: 'Boolean Logic', description: 'True/False and logical operations', order_index: 8 },
    ],
  },
  {
    id: 2, name: 'Control Flow', description: 'Master conditionals and loops to control program flow', order_index: 2,
    topics: [
      { id: 9, name: 'If Statements', description: 'Conditional execution', order_index: 1 },
      { id: 10, name: 'Elif & Else', description: 'Multiple conditions', order_index: 2 },
      { id: 11, name: 'Comparison Operators', description: '==, !=, <, >, <=, >=', order_index: 3 },
      { id: 12, name: 'Logical Operators', description: 'and, or, not', order_index: 4 },
      { id: 13, name: 'While Loops', description: 'Repeat while condition is true', order_index: 5 },
      { id: 14, name: 'For Loops', description: 'Iterate over sequences', order_index: 6 },
      { id: 15, name: 'Break & Continue', description: 'Control loop execution', order_index: 7 },
      { id: 16, name: 'Nested Loops', description: 'Loops inside loops', order_index: 8 },
    ],
  },
  {
    id: 3, name: 'Data Structures', description: 'Work with lists, tuples, dictionaries, and sets', order_index: 3,
    topics: [
      { id: 17, name: 'Lists', description: 'Ordered mutable sequences', order_index: 1 },
      { id: 18, name: 'List Methods', description: 'append, remove, sort, and more', order_index: 2 },
      { id: 19, name: 'Tuples', description: 'Immutable ordered sequences', order_index: 3 },
      { id: 20, name: 'Dictionaries', description: 'Key-value pairs', order_index: 4 },
      { id: 21, name: 'Dictionary Methods', description: 'keys, values, items, and more', order_index: 5 },
      { id: 22, name: 'Sets', description: 'Unique unordered collections', order_index: 6 },
      { id: 23, name: 'List Comprehensions', description: 'Concise list creation', order_index: 7 },
      { id: 24, name: 'Nested Structures', description: 'Lists of dicts and complex data', order_index: 8 },
    ],
  },
  {
    id: 4, name: 'Functions', description: 'Write reusable, modular code with functions', order_index: 4,
    topics: [
      { id: 25, name: 'Defining Functions', description: 'Creating functions with def', order_index: 1 },
      { id: 26, name: 'Parameters & Arguments', description: 'Passing data to functions', order_index: 2 },
      { id: 27, name: 'Return Values', description: 'Getting data back from functions', order_index: 3 },
      { id: 28, name: 'Default Parameters', description: 'Optional function arguments', order_index: 4 },
      { id: 29, name: 'Variable Scope', description: 'Local and global variables', order_index: 5 },
      { id: 30, name: 'Lambda Functions', description: 'Anonymous inline functions', order_index: 6 },
      { id: 31, name: 'Recursion', description: 'Functions that call themselves', order_index: 7 },
      { id: 32, name: 'Decorators', description: 'Wrapping and enhancing functions', order_index: 8 },
    ],
  },
  {
    id: 5, name: 'Object-Oriented Programming', description: 'Build complex programs using classes and objects', order_index: 5,
    topics: [
      { id: 33, name: 'Classes & Objects', description: 'Creating blueprints for data', order_index: 1 },
      { id: 34, name: 'Constructors', description: 'Initializing objects with __init__', order_index: 2 },
      { id: 35, name: 'Instance Methods', description: 'Functions that belong to objects', order_index: 3 },
      { id: 36, name: 'Class Variables', description: 'Shared data across instances', order_index: 4 },
      { id: 37, name: 'Inheritance', description: 'Creating subclasses', order_index: 5 },
      { id: 38, name: 'Method Overriding', description: 'Customizing inherited methods', order_index: 6 },
      { id: 39, name: 'Polymorphism', description: 'Same interface, different behavior', order_index: 7 },
      { id: 40, name: 'Encapsulation', description: 'Hiding implementation details', order_index: 8 },
    ],
  },
  {
    id: 6, name: 'File Handling', description: 'Read, write, and manage files in Python', order_index: 6,
    topics: [
      { id: 41, name: 'Opening Files', description: 'The open() function', order_index: 1 },
      { id: 42, name: 'Reading Files', description: 'read(), readline(), readlines()', order_index: 2 },
      { id: 43, name: 'Writing Files', description: 'Writing and appending to files', order_index: 3 },
      { id: 44, name: 'File Modes', description: 'r, w, a, rb, wb modes', order_index: 4 },
      { id: 45, name: 'CSV Files', description: 'Working with CSV data', order_index: 5 },
      { id: 46, name: 'JSON Files', description: 'Reading and writing JSON', order_index: 6 },
      { id: 47, name: 'Context Managers', description: 'The with statement', order_index: 7 },
      { id: 48, name: 'File Paths', description: 'os.path and pathlib', order_index: 8 },
    ],
  },
  {
    id: 7, name: 'Error Handling', description: 'Handle exceptions and write robust Python code', order_index: 7,
    topics: [
      { id: 49, name: 'Try & Except', description: 'Catching and handling errors', order_index: 1 },
      { id: 50, name: 'Multiple Exceptions', description: 'Handling different error types', order_index: 2 },
      { id: 51, name: 'Finally Block', description: 'Code that always runs', order_index: 3 },
      { id: 52, name: 'Raising Exceptions', description: 'Throwing errors intentionally', order_index: 4 },
      { id: 53, name: 'Custom Exceptions', description: 'Creating your own exception types', order_index: 5 },
      { id: 54, name: 'Assertions', description: 'assert statements for debugging', order_index: 6 },
      { id: 55, name: 'Logging', description: 'The logging module', order_index: 7 },
      { id: 56, name: 'Debugging Techniques', description: 'Finding and fixing bugs', order_index: 8 },
    ],
  },
  {
    id: 8, name: 'Libraries & Modules', description: 'Use Python\'s standard library and third-party packages', order_index: 8,
    topics: [
      { id: 57, name: 'Importing Modules', description: 'import and from...import', order_index: 1 },
      { id: 58, name: 'Standard Library', description: 'Python\'s built-in modules', order_index: 2 },
      { id: 59, name: 'Math Module', description: 'Mathematical functions', order_index: 3 },
      { id: 60, name: 'Random Module', description: 'Random number generation', order_index: 4 },
      { id: 61, name: 'Datetime Module', description: 'Working with dates and times', order_index: 5 },
      { id: 62, name: 'OS Module', description: 'Operating system interface', order_index: 6 },
      { id: 63, name: 'pip & Packages', description: 'Installing third-party packages', order_index: 7 },
      { id: 64, name: 'Virtual Environments', description: 'Isolating project dependencies', order_index: 8 },
    ],
  },
];

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') return res.status(405).json({ error: 'Method not allowed' });

  try {
    const session = await auth.api.getSession({ headers: req.headers as any });
    if (!session?.user) return res.status(401).json({ error: 'Unauthorized' });

    // Try database first, fall back to static data
    if (process.env.DATABASE_URL) {
      try {
        const { Pool } = await import('pg');
        const pool = new Pool({ connectionString: process.env.DATABASE_URL });
        const modulesResult = await pool.query('SELECT id, name, description, order_index FROM modules ORDER BY order_index ASC');
        const topicsResult = await pool.query('SELECT id, name, description, module_id, order_index FROM topics ORDER BY module_id, order_index ASC');

        const modules = modulesResult.rows.map(m => ({
          ...m,
          topics: topicsResult.rows.filter(t => t.module_id === m.id),
        }));
        await pool.end();
        return res.status(200).json({ modules });
      } catch {
        // Fall through to static data
      }
    }

    return res.status(200).json({ modules: STATIC_MODULES });
  } catch (error) {
    return res.status(500).json({ error: 'Internal server error' });
  }
}
