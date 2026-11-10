import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import { fileURLToPath, pathToFileURL } from "node:url";

const frontend = new URL("../../../../src/frontend/", import.meta.url);
const requireFrontend = createRequire(new URL("package.json", frontend));
const { chromium } = requireFrontend("@playwright/test");
const { createServer } = await import(pathToFileURL(requireFrontend.resolve("vite")).href);
const { backend, origin, key, cert, password, projectId } = JSON.parse(readFileSync(0, "utf8"));

process.env.DSGEOREF_IDENTITY_DEV_BACKEND = backend;
process.env.DSGEOREF_IDENTITY_DEV_TLS_KEY = key;
process.env.DSGEOREF_IDENTITY_DEV_TLS_CERT = cert;
const vite = await createServer({
  root: fileURLToPath(frontend),
  server: { port: Number(new URL(origin).port) },
});
try {
  await vite.listen();
  const browser = await chromium.launch();
  try {
    const context = await browser.newContext({ ignoreHTTPSErrors: true });
    const page = await context.newPage();
    await page.goto(origin);
    const login = page.getByRole("form", { name: "Sessão local" });
    await login.getByLabel("Usuário").fill("admin");
    await login.getByLabel("Senha").fill(password);
    await login.getByRole("button", { name: "Iniciar sessão" }).click();
    await page.getByText("Sessão confirmada pela API.").waitFor();
    const cookie = (await context.cookies()).find(({ name }) => name === "dsgeorref_session");
    assert.equal(cookie?.httpOnly, true);
    assert.equal(cookie?.secure, true);

    const members = page.getByRole("form", { name: "Membros locais do projeto" });
    await members.getByLabel("ID do projeto").fill(projectId);
    await members.getByRole("button", { name: "Consultar membros" }).click();
    await page.getByText(/Consulta confirmada/).waitFor();

    const authorization = page.getByRole("form", { name: "Consultar autorização" });
    await authorization.getByLabel("Ação").fill("instance:bootstrap");
    await authorization.getByLabel("Tipo de recurso").fill("instance");
    await authorization.getByRole("button", { name: "Verificar autorização" }).click();
    await page.getByText("Permissão negada pela API.").waitFor();

    const logout = page.getByRole("form", { name: "Encerrar sessão" });
    await logout.getByRole("button", { name: "Encerrar sessão" }).click();
    await page.getByText("Sessão encerrada pela API.").waitFor();
    assert.ok(!(await context.cookies()).some(({ name }) => name === "dsgeorref_session"));
  } finally {
    await browser.close();
  }
} finally {
  await vite.close();
}
