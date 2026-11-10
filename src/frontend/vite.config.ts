import { readFileSync } from "node:fs";
import { defineConfig } from "vite";

export default defineConfig(({ command }) => {
  const backend = command === "serve" ? process.env.DSGEOREF_IDENTITY_DEV_BACKEND : undefined;
  const server = backend ? identityServer(backend) : { host: "127.0.0.1" };
  return {
    build: {
      outDir: "../../node_modules/.cache/frontend-stage-a-dist",
      emptyOutDir: true,
      manifest: true,
    },
    define: { "import.meta.env.VITE_IDENTITY_DEV": JSON.stringify(Boolean(backend)) },
    server,
  };
});

function identityServer(backend: string) {
  const target = new URL(backend);
  const key = process.env.DSGEOREF_IDENTITY_DEV_TLS_KEY;
  const cert = process.env.DSGEOREF_IDENTITY_DEV_TLS_CERT;
  if (target.protocol !== "http:" || target.hostname !== "127.0.0.1" || target.origin !== backend || !key || !cert) {
    throw new Error("Identity development requires a loopback HTTP backend and local TLS files");
  }
  return {
    host: "127.0.0.1",
    strictPort: true,
    https: { key: readFileSync(key), cert: readFileSync(cert) },
    proxy: { "/api/v1": backend },
  };
}
