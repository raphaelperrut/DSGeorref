import { defineConfig } from "@playwright/test";
import { fileURLToPath } from "node:url";

const frontend = fileURLToPath(new URL("../../../../../", import.meta.url));
const dist = fileURLToPath(new URL("../../../../../../../node_modules/.cache/project-access-dist", import.meta.url));
export default defineConfig({
  testDir: ".", testMatch: "surface.browser.spec.ts", workers: 1,
  outputDir: fileURLToPath(new URL("../../../../../../../node_modules/.cache/project-access-browser", import.meta.url)),
  use: { browserName: "chromium", baseURL: "http://127.0.0.1:4189", trace: "off", video: "off" },
  webServer: {
    command: `pnpm exec vite preview src/contexts/identity_access/features/autorizacao-por-projeto-operacao-artefato-e-caminho --outDir "${dist}" --host 127.0.0.1 --port 4189 --strictPort`,
    cwd: frontend, url: "http://127.0.0.1:4189", reuseExistingServer: false,
  },
});
