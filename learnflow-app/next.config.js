/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone',
  env: {
    API_BASE_URL: process.env.API_BASE_URL || 'http://localhost:8000',
    SANDBOX_URL: process.env.SANDBOX_URL || 'http://localhost:8010',
  },
};

module.exports = nextConfig;
