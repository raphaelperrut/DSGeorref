import { defineConfig } from "@playwright/test";
import { fileURLToPath } from "node:url";

const frontend = fileURLToPath(new URL("../../../../../", import.meta.url));
const preview = process.env.IDENTITY_PREVIEW === "1";
const dist = fileURLToPath(new URL("../../../../../../../node_modules/.cache/identity-access-dist", import.meta.url));
export default defineConfig({
  testDir: ".", testMatch: "surface.browser.spec.ts", workers: 1,
  outputDir: fileURLToPath(new URL("../../../../../../../node_modules/.cache/identity-access-browser", import.meta.url)),
  use: { browserName: "chromium", baseURL: "http://127.0.0.1:4188", trace: "off", screenshot: "off", video: "off" },
  webServer: {
    command: preview
      ? `pnpm exec vite preview src/contexts/identity_access/features/contas-locais-bootstrap-unico-sessoes-tokens-e-adapter --outDir "${dist}" --host 127.0.0.1 --port 4188 --strictPort`
      : "pnpm exec vite --host 127.0.0.1 --port 4188 --strictPort",
    cwd: frontend, url: "http://127.0.0.1:4188", reuseExistingServer: false,
  },
});
