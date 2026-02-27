/**
 * Better Auth server configuration for LearnFlow.
 * Uses PostgreSQL adapter with pg package.
 */
import { betterAuth } from 'better-auth';
import { Pool } from 'pg';

// Create PostgreSQL connection pool
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

export const auth = betterAuth({
  database: pool,

  // Email and password authentication
  emailAndPassword: {
    enabled: true,
    minPasswordLength: 8,
  },

  // Social login providers
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID || '',
      clientSecret: process.env.GOOGLE_CLIENT_SECRET || '',
    },
    github: {
      clientId: process.env.GITHUB_CLIENT_ID || '',
      clientSecret: process.env.GITHUB_CLIENT_SECRET || '',
    },
  },

  // User configuration
  user: {
    modelName: 'user',
  },

  // Session configuration
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24, // Update session every 24 hours
    cookieCache: {
      enabled: true,
      maxAge: 60 * 5, // 5 minutes
    },
  },

  // Base URL configuration
  baseURL: process.env.BETTER_AUTH_URL || 'http://localhost:3000',

  // Secret for signing tokens
  secret: process.env.BETTER_AUTH_SECRET,

  // Trust host header in production - support multiple ports
  trustedOrigins: [
    'http://localhost:3000',
    'http://localhost:3001',
    'http://localhost:3002',
    'http://localhost:3003',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:3001',
    'http://127.0.0.1:3002',
    'http://127.0.0.1:3003',
    process.env.NEXT_PUBLIC_APP_URL || '',
    process.env.NEXT_PUBLIC_APP_URL_ALT || '',
  ].filter(Boolean),
});

// Export type for session
export type Session = typeof auth.$Infer.Session;
export type User = Session['user'];
