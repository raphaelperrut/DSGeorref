import { expect, test } from "@playwright/test";
import { fileURLToPath } from "node:url";

const preview = process.env.IDENTITY_PREVIEW === "1";
const entry = preview ? "/" : "/src/contexts/identity_access/features/contas-locais-bootstrap-unico-sessoes-tokens-e-adapter/index.html";
test("real Vite/React/generated transport executes a published request and fails closed without an API host", async ({ page }) => {
  const scriptErrors: string[] = [];
  page.on("pageerror", error => scriptErrors.push(error.name));
  const loaded = await page.goto(entry);
  expect(loaded?.status()).toBe(200);
  await expect(page.getByRole("heading", { name: "Identidade e acesso" })).toBeVisible();
  await expect(page.getByRole("main")).toHaveAttribute("data-openapi-base-url", "/api/v1");
  await page.screenshot({ path: fileURLToPath(new URL(`../../../../../../../node_modules/.cache/identity-access-browser/surface${preview ? "-production" : ""}.png`, import.meta.url)), fullPage: true });
  const form = page.getByRole("form", { name: "Sessão local" });
  await form.getByLabel("Usuário").fill("synthetic-browser-user");
  await form.getByLabel("Senha", { exact: true }).fill("synthetic-browser-password");
  const requested = page.waitForRequest(request => request.url().endsWith("/api/v1/auth/session") && request.method() === "POST");
  const received = page.waitForResponse(response => response.url().endsWith("/api/v1/auth/session"));
  await form.getByRole("button", { name: "Iniciar sessão" }).click();
  const request = await requested;
  expect(request.headers()["idempotency-key"]?.length).toBeGreaterThanOrEqual(16);
  // No request routing, API stubs or endpoint invention in this smoke.
  expect((await received).status()).toBe(404);
  await expect(page.getByRole("region", { name: "Sessão local" }).getByRole("alert")).toContainText("Resposta inesperada");
  await expect(page.getByTestId("session-state")).toContainText("Sessão não confirmada");
  await expect(page.getByRole("button", { name: "Emitir token", exact: true })).toBeDisabled();
  expect(scriptErrors).toEqual([]);
});
