/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*'
      }
    ]
  },
  env: {
    CUSTOM_KEY: 'finance-suite',
  },
  images: {
    domains: ['localhost'],
  }
}

module.exports = nextConfig 