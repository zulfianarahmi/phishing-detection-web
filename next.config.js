/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Pastikan file model bisa diakses
  webpack: (config) => {
    config.resolve.fallback = {
      ...config.resolve.fallback,
      fs: false,
    };
    return config;
  },
}

module.exports = nextConfig

