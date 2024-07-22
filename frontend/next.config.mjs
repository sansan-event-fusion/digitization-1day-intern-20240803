/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    BACKEND_SERVICE_URL: "http://127.0.0.1:8000",
  },
  images: {
    domains: ["127.0.0.1"],
  },
  reactStrictMode: false,
};

export default nextConfig;
