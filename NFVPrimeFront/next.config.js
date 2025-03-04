/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: false,
  env: {
    API_URL: `${process.env.API_URL}`,
    APP_STAGE: `${process.env.APP_STAGE}`
  },
  output: "export",
  distDir: "build",
  // trailingSlash: true
};

module.exports = nextConfig;
