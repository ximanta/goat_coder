/** @type {import('next').NextConfig} */
const nextConfig = {
  // output: "export",
  // webpack: (config) => {
  //   config.resolve.alias.canvas = false;
  //   return config;
  // },
  compiler: {
    styledComponents: true,
  },
  reactStrictMode: true,

  eslint: {
    ignoreDuringBuilds: true, // Disable ESLint during the build
  },

  typescript: {
    ignoreBuildErrors: true, // Disable TypeScript type checking during the build
  },
};

export default nextConfig;
