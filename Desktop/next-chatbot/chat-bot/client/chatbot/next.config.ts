import type { NextConfig } from 'next';
import type { Configuration as WebpackConfig } from 'webpack';

const nextConfig: NextConfig = {
  experimental: {
    serverActions: {}
  },
  webpack: (config: WebpackConfig): WebpackConfig => {
    if (config.module) {
      config.module.exprContextCritical = false;
    }
    return config;
  }
};

export default nextConfig;