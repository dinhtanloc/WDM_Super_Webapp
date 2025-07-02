/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,

  // 👇 Cho phép các IP LAN trong quá trình phát triển
  allowedDevOrigins: [
    'http://192.168.1.10', // hoặc IP máy bạn đang dùng
    'http://localhost:3000',
  ],
};

export default nextConfig;
