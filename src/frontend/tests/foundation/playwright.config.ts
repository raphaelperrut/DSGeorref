import { defineConfig } from "@playwright/test";
import { fileURLToPath } from "node:url";

export default defineConfig({
  testDir: ".",
  testMatch: "shell.browser.spec.ts",
  workers: 1,
  use: { browserName: "chromium", baseURL: "http://127.0.0.1:4178" },
  webServer: {
    command: "pnpm exec vite preview --host 127.0.0.1 --port 4178 --strictPort",
    cwd: fileURLToPath(new URL("../../", import.meta.url)),
    url: "http://127.0.0.1:4178",
    reuseExistingServer: false,
  },
});
