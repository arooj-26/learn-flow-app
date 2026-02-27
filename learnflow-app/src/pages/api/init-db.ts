/**
 * Database Initialization API
 * Creates all required tables for Better Auth + LearnFlow app
 * Run once: GET http://localhost:3000/api/init-db
 */
import type { NextApiRequest, NextApiResponse } from 'next';
import { Pool } from 'pg';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const results: string[] = [];

  try {
    // ============================================================
    // 0. Drop conflicting old tables with wrong schemas
    // ============================================================

    // Drop old Better Auth tables that might have wrong column names
    // (e.g. account with user_id instead of "userId")
    try {
      // Check if account table exists with wrong schema
      const accountCheck = await pool.query(`
        SELECT column_name FROM information_schema.columns
        WHERE table_name = 'account' AND column_name = 'user_id'
      `);
      if (accountCheck.rows.length > 0) {
        await pool.query('DROP TABLE IF EXISTS "account" CASCADE');
        results.push('Dropped old account table (had wrong column names)');
      }
    } catch { /* ignore */ }

    try {
      // Check if session table exists with wrong schema
      const sessionCheck = await pool.query(`
        SELECT column_name FROM information_schema.columns
        WHERE table_name = 'session' AND column_name = 'user_id'
      `);
      if (sessionCheck.rows.length > 0) {
        await pool.query('DROP TABLE IF EXISTS "session" CASCADE');
        results.push('Dropped old session table (had wrong column names)');
      }
    } catch { /* ignore */ }

    // ============================================================
    // 1. Better Auth Tables (required for authentication)
    // ============================================================

    // "user" table - Better Auth's user table
    await pool.query(`
      CREATE TABLE IF NOT EXISTS "user" (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        "emailVerified" BOOLEAN DEFAULT false,
        image TEXT,
        role TEXT DEFAULT 'student',
        "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        "updatedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);
    results.push('Created table: user');

    // "session" table
    await pool.query(`
      CREATE TABLE IF NOT EXISTS "session" (
        id TEXT PRIMARY KEY,
        "expiresAt" TIMESTAMP NOT NULL,
        token TEXT NOT NULL UNIQUE,
        "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        "updatedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        "ipAddress" TEXT,
        "userAgent" TEXT,
        "userId" TEXT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE
      )
    `);
    results.push('Created table: session');

    // "account" table
    await pool.query(`
      CREATE TABLE IF NOT EXISTS "account" (
        id TEXT PRIMARY KEY,
        "accountId" TEXT NOT NULL,
        "providerId" TEXT NOT NULL,
        "userId" TEXT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
        "accessToken" TEXT,
        "refreshToken" TEXT,
        "idToken" TEXT,
        "accessTokenExpiresAt" TIMESTAMP,
        "refreshTokenExpiresAt" TIMESTAMP,
        scope TEXT,
        password TEXT,
        "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        "updatedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);
    results.push('Created table: account');

    // "verification" table
    await pool.query(`
      CREATE TABLE IF NOT EXISTS "verification" (
        id TEXT PRIMARY KEY,
        identifier TEXT NOT NULL,
        value TEXT NOT NULL,
        "expiresAt" TIMESTAMP NOT NULL,
        "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        "updatedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);
    results.push('Created table: verification');

    // ============================================================
    // 2. LearnFlow App Tables
    // ============================================================

    // Modules table
    await pool.query(`
      CREATE TABLE IF NOT EXISTS modules (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        description TEXT,
        order_index INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);
    results.push('Created table: modules');

    // Topics table
    await pool.query(`
      CREATE TABLE IF NOT EXISTS topics (
        id SERIAL PRIMARY KEY,
        module_id INTEGER REFERENCES modules(id) ON DELETE CASCADE,
        name TEXT NOT NULL,
        slug TEXT,
        description TEXT,
        order_index INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);
    results.push('Created table: topics');

    // User progress table (references Better Auth's "user" table)
    await pool.query(`
      CREATE TABLE IF NOT EXISTS user_progress (
        id SERIAL PRIMARY KEY,
        user_id TEXT NOT NULL,
        topic_id INTEGER REFERENCES topics(id) ON DELETE CASCADE,
        mastery INTEGER DEFAULT 0,
        exercises_done INTEGER DEFAULT 0,
        quiz_score INTEGER DEFAULT 0,
        code_quality INTEGER DEFAULT 0,
        streak INTEGER DEFAULT 0,
        last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, topic_id)
      )
    `);
    results.push('Created table: user_progress');

    // Quiz results table
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
    results.push('Created table: quiz_results');

    // User roles table (for teacher/student mapping)
    await pool.query(`
      CREATE TABLE IF NOT EXISTS user_roles (
        id SERIAL PRIMARY KEY,
        user_id TEXT NOT NULL UNIQUE,
        role TEXT DEFAULT 'student' CHECK (role IN ('student', 'teacher', 'admin')),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);
    results.push('Created table: user_roles');

    // ============================================================
    // 3. Seed Modules and Topics (if empty)
    // ============================================================

    const moduleCount = await pool.query('SELECT COUNT(*) FROM modules');
    if (parseInt(moduleCount.rows[0].count) === 0) {
      // Insert modules
      const modulesData = [
        { name: 'Python Basics', description: 'Variables, data types, operators, and basic I/O', order: 1 },
        { name: 'Control Flow', description: 'If/else statements, loops, and program flow', order: 2 },
        { name: 'Data Structures', description: 'Lists, tuples, dictionaries, and sets', order: 3 },
        { name: 'Functions', description: 'Defining functions, parameters, and return values', order: 4 },
        { name: 'Object-Oriented Programming', description: 'Classes, objects, inheritance, and polymorphism', order: 5 },
        { name: 'File Handling', description: 'Reading, writing, and managing files', order: 6 },
        { name: 'Error Handling', description: 'Try/except, custom exceptions, and debugging', order: 7 },
        { name: 'Libraries & Modules', description: 'Standard library, pip, and popular packages', order: 8 },
      ];

      for (const mod of modulesData) {
        await pool.query(
          'INSERT INTO modules (name, description, order_index) VALUES ($1, $2, $3) ON CONFLICT (name) DO NOTHING',
          [mod.name, mod.description, mod.order]
        );
      }
      results.push('Seeded modules');

      // Insert topics per module
      const topicsData: Record<string, string[]> = {
        'Python Basics': [
          'Variables & Data Types', 'Numbers & Math', 'Strings', 'String Methods',
          'Type Conversion', 'Input & Output', 'Comments & Style', 'Boolean Logic'
        ],
        'Control Flow': [
          'If Statements', 'Elif & Else', 'Comparison Operators', 'Logical Operators',
          'While Loops', 'For Loops', 'Break & Continue', 'Nested Loops'
        ],
        'Data Structures': [
          'Lists', 'List Methods', 'Tuples', 'Dictionaries',
          'Dictionary Methods', 'Sets', 'List Comprehensions', 'Nested Structures'
        ],
        'Functions': [
          'Defining Functions', 'Parameters & Arguments', 'Return Values', 'Default Parameters',
          'Variable Scope', 'Lambda Functions', 'Recursion', 'Decorators'
        ],
        'Object-Oriented Programming': [
          'Classes & Objects', 'Constructors', 'Instance Methods', 'Class Variables',
          'Inheritance', 'Method Overriding', 'Polymorphism', 'Encapsulation'
        ],
        'File Handling': [
          'Opening Files', 'Reading Files', 'Writing Files', 'File Modes',
          'CSV Files', 'JSON Files', 'Context Managers', 'File Paths'
        ],
        'Error Handling': [
          'Try & Except', 'Multiple Exceptions', 'Finally Block', 'Raising Exceptions',
          'Custom Exceptions', 'Assertions', 'Logging', 'Debugging Techniques'
        ],
        'Libraries & Modules': [
          'Importing Modules', 'Standard Library', 'Math Module', 'Random Module',
          'Datetime Module', 'OS Module', 'pip & Packages', 'Virtual Environments'
        ],
      };

      const modulesResult = await pool.query('SELECT id, name FROM modules ORDER BY order_index');
      for (const mod of modulesResult.rows) {
        const topics = topicsData[mod.name] || [];
        for (let i = 0; i < topics.length; i++) {
          const slug = topics[i].toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
          await pool.query(
            'INSERT INTO topics (module_id, name, slug, order_index) VALUES ($1, $2, $3, $4) ON CONFLICT DO NOTHING',
            [mod.id, topics[i], slug, i + 1]
          );
        }
      }
      results.push('Seeded topics (64 total across 8 modules)');
    } else {
      results.push('Modules already exist, skipping seed');
    }

    // ============================================================
    // 4. Verify everything
    // ============================================================

    const tables = await pool.query(`
      SELECT table_name FROM information_schema.tables
      WHERE table_schema = 'public'
      ORDER BY table_name
    `);

    const tableList = tables.rows.map((r: any) => r.table_name);

    return res.status(200).json({
      success: true,
      message: 'Database initialized successfully!',
      results,
      tables: tableList,
    });
  } catch (error: any) {
    console.error('DB Init Error:', error);
    return res.status(500).json({
      success: false,
      error: error.message,
      results,
    });
  }
}
