
export default defineConfig({
  server: {
    proxy: {
      "/api": {
        target: "https://ohmanda.com",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
});