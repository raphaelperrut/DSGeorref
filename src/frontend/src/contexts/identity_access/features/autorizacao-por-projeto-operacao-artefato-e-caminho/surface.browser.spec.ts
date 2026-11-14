import { expect, test } from "@playwright/test";

const projectId = "00000000-0000-4000-8000-000000000001";
const userId = "00000000-0000-4000-8000-000000000002";
test("built surface uses generated HTTP and remains usable on mobile", async ({ page }, testInfo) => {
  let decisionCalls = 0;
  const keys: string[] = [];
  await page.route("**/api/v1/**", async route => {
    const request = route.request();
    const url = new URL(request.url());
    if (url.pathname.endsWith("/auth/session")) {
      await route.fulfill({ status: 202, json: { data: { sessionId: projectId, userId,
        csrfToken: "synthetic-browser-csrf-not-a-real-credential", expiresAt: new Date(Date.now() + 60_000).toISOString() } } });
    } else if (url.pathname.endsWith("/authorization/check")) {
      expect(Object.fromEntries(url.searchParams)).toEqual({ action: "project_member:list", resourceType: "project", resourceId: projectId });
      decisionCalls++;
      await route.fulfill({ status: 200, json: { data: { allowed: decisionCalls === 1, policyVersion: "1.1.0", reasonCode: decisionCalls === 1 ? "granted" : "access_denied" } } });
    } else if (request.method() === "POST" && url.pathname === `/api/v1/projects/${projectId}/members`) {
      expect(request.headers()["x-csrf-token"]).toBe("synthetic-browser-csrf-not-a-real-credential");
      expect(request.postDataJSON()).toEqual({ userId, role: "viewer" });
      keys.push(request.headers()["idempotency-key"]!);
      await route.fulfill({ status: 409, contentType: "application/problem+json", body: JSON.stringify({
        type: "https://example.invalid/problems/conflict", title: "conflict", code: "conflict", status: 409,
      }) });
    } else throw new Error(`Unexpected request: ${request.method()} ${url.pathname}`);
  });
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "Autorização e membros do projeto" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Verificar autorização" })).toBeDisabled();
  const login = page.getByRole("form", { name: "Sessão local" });
  await login.getByLabel("Usuário").fill("fixture-user");
  await login.getByLabel("Senha").fill("synthetic-password");
  await login.getByRole("button").click();
  await expect(page.getByText("Sessão confirmada pela API.", { exact: true })).toBeVisible();
  const check = page.getByRole("form", { name: "Consultar autorização" });
  await check.getByLabel("Ação", { exact: true }).fill("project_member:list");
  await check.getByLabel("Tipo de recurso").fill("project");
  await check.getByLabel("ID do recurso (opcional)").fill(projectId);
  await check.getByRole("button").click();
  await expect(page.getByText("Permissão confirmada nesta consulta.")).toBeVisible();
  await check.getByRole("button").click();
  await expect(page.getByText("Permissão negada pela API.")).toBeVisible();
  await expect(page.getByText("Permissão confirmada nesta consulta.")).toHaveCount(0);
  const add = page.getByRole("form", { name: "Vincular conta existente" });
  await add.getByLabel("ID do projeto", { exact: true }).fill(projectId);
  await add.getByLabel("ID da conta", { exact: true }).fill(userId);
  await add.getByLabel("Papel").selectOption("viewer");
  await add.getByRole("button").click();
  await expect(page.getByRole("alert")).toContainText("HTTP 409");
  await add.getByRole("button").click();
  await expect.poll(() => keys.length).toBe(2); expect(keys[0]).toBeTruthy(); expect(keys[1]).toBe(keys[0]);
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
  await page.screenshot({ path: testInfo.outputPath("mobile.png"), fullPage: true });
});
