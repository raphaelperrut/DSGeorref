import { defineConfig } from "vite";

export default defineConfig({
  build: {
    outDir: "../../node_modules/.cache/frontend-stage-a-dist",
    emptyOutDir: true,
    manifest: true,
  },
  server: { host: "127.0.0.1" },
});
