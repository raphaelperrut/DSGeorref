import { act } from "react";
import { afterEach, beforeEach, expect, test, vi } from "vitest";
import { fireEvent, within } from "@testing-library/dom";
import { client, api } from "../../../operator_experience/contracts/frontend-shell";
import { postAuthSession } from "../../../operator_experience/contracts/openapi/generated";
import { client as generatedClient } from "../../../operator_experience/contracts/openapi/generated/client.gen";
import type { Problem, Session, ProjectMember, PersonalAccessTokenWritable } from "../../../operator_experience/contracts/openapi/generated";
import { mountIdentitySurface } from "./index";

Object.assign(globalThis, { IS_REACT_ACT_ENVIRONMENT: true });
const userId = "00000000-0000-4000-8000-000000000001";
const projectId = "00000000-0000-4000-8000-000000000002";
const sessionId = "00000000-0000-4000-8000-000000000003";
const password = "synthetic-test-password";
const tokenValue = "synthetic-test-token-not-an-operational-credential";
const session = (): Session => ({ sessionId, userId, expiresAt: new Date(Date.now() + 60_000).toISOString(), csrfToken: "synthetic-csrf-value-for-contract-test-only" });
const member: ProjectMember = { projectId, userId, role: "viewer", revision: 1 };
const pat: PersonalAccessTokenWritable = { tokenId: sessionId, token: tokenValue, prefix: "synthetic", scopes: ["fixture-action"] };
const originalConfig = client.getConfig();
let container: HTMLDivElement;
let unmount: () => void;
let requests: Request[];
let replies: Array<Response | Error>;
const response = (status: number, data: unknown, extra: Record<string, string> = {}) =>
  new Response(status === 204 ? null : JSON.stringify(data), { status, headers: { "content-type": "application/json", ...extra } });
function problem(status: number, code: string, detail = "Pedido recusado") {
  const value: Problem = { type: `https://example.invalid/problems/${code}`, title: code, status, detail, instance: "/request/fixture", code };
  return response(status, value, { "content-type": "application/problem+json" });
}
beforeEach(async () => {
  requests = []; replies = [];
  client.setConfig({ baseUrl: "/api/v1", fetch: async request => {
    requests.push(request);
    const next = replies.shift();
    if (next instanceof Error) throw next;
    if (!next) throw new Error("Unexpected request in test");
    return next;
  } });
  container = document.createElement("div"); document.body.append(container);
  await act(async () => { unmount = mountIdentitySurface(container); });
});
afterEach(async () => {
  await act(async () => unmount()); container.remove();
  client.setConfig({ ...originalConfig, fetch: originalConfig.fetch ?? globalThis.fetch }); vi.restoreAllMocks(); vi.useRealTimers();
});
const region = (name: string) => within(within(container).getByRole("region", { name }));
async function submit(name: string, fields: Record<string, string> = {}) {
  const form = region(name).getByRole("form", { name });
  await act(async () => {
    for (const [field, content] of Object.entries(fields)) {
      const input = form.querySelector(`[name="${field}"]`);
      if (!input) throw new Error(`Missing field ${field}`);
      fireEvent.input(input, { target: { value: content } });
    }
  });
  await act(async () => { fireEvent.submit(form); });
}
async function login() {
  replies.push(response(202, { data: session() }, { etag: '"fixture-revision"' }));
  await submit("Sessão local", { username: "fixture-user", password });
}
const authenticated = () => within(container).getByTestId("session-state").textContent?.includes("Sessão válida recebida");
const expectClosed = () => {
  expect(authenticated()).toBe(false);
  expect((region("Emitir token pessoal").getByRole("button", { name: "Emitir token" }) as HTMLButtonElement).disabled
    || region("Emitir token pessoal").getByRole("button", { name: "Emitir token" }).closest("fieldset")?.disabled).toBe(true);
};

test("test_epic_008_superficie", async () => {
  expect(client).toBe(generatedClient); expect(api.postAuthSession).toBe(postAuthSession);
  for (const name of ["Bootstrap único", "Sessão local", "Encerrar sessão", "Emitir token pessoal", "Membros locais do projeto", "Vincular conta local existente", "Callback OIDC", "Consultar autorização"]) {
    expect(region(name).getByRole("form", { name })).toBeDefined();
  }
  expect(requests).toHaveLength(0); expectClosed();
  expect((region("Vincular conta local existente").getByLabelText("Papel") as HTMLSelectElement).value).toBe("");
  expect(within(container).queryByRole("button", { name: /revogar token/i })).toBeNull();
});
test("bootstrap success is observable without implicitly authenticating", async () => {
  replies.push(response(202, { data: { administratorId: userId, sessionId, createdAt: new Date().toISOString() } }));
  await submit("Bootstrap único", { username: "fixture-user", password, displayName: "Fixture" });
  expect(region("Bootstrap único").getByRole("status").textContent).toContain("Bootstrap confirmado"); expectClosed();
  expect(requests[0]!.url).toBe("http://localhost:3000/api/v1/auth/bootstrap");
  expect(requests[0]!.headers.get("Idempotency-Key")!.length).toBeGreaterThanOrEqual(16);
});
test("repeated bootstrap remains rejected and preserves Problem Details", async () => {
  replies.push(response(202, { data: { administratorId: userId, sessionId, createdAt: new Date().toISOString() } }));
  const fields = { username: "fixture-user", password, displayName: "Fixture" };
  await submit("Bootstrap único", fields);
  replies.push(problem(409, "bootstrap_already_completed")); await submit("Bootstrap único", fields);
  const alert = region("Bootstrap único").getByRole("alert");
  expect(alert.textContent).toContain("nova execução rejeitada"); expect(alert.textContent).toContain("409");
  expect(region("Bootstrap único").queryByRole("status")).toBeNull(); expectClosed();
  expect(requests[0]!.headers.get("Idempotency-Key")).not.toBe(requests[1]!.headers.get("Idempotency-Key"));
});
test.each([422, 401, 403])("bootstrap rejection %s fails closed and redacts a reflected password", async status => {
  replies.push(problem(status, status === 422 ? "password_policy_failed" : status === 401 ? "unauthorized" : "forbidden", `Rejected ${password}`));
  await submit("Bootstrap único", { username: "fixture-user", password, displayName: "Fixture" });
  const alert = region("Bootstrap único").getByRole("alert").textContent!;
  for (const field of ["type", "title", "status", "detail", "instance"]) expect(alert).toContain(field);
  expect(alert).toContain("[redigido]"); expect(alert.includes(password)).toBe(false); expectClosed();
});
test("valid login derives session state and retains the authoritative ETag", async () => {
  await login(); expect(authenticated()).toBe(true);
  expect((region("Encerrar sessão").getByLabelText("If-Match da sessão") as HTMLInputElement).value).toBe('"fixture-revision"');
  expect(requests[0]!.credentials).toBe("same-origin"); expect(requests[0]!.cache).toBe("no-store");
});
test("invalid login cannot retain a previous session", async () => {
  await login(); replies.push(problem(401, "invalid_credentials"));
  await submit("Sessão local", { username: "fixture-user", password });
  expect(region("Sessão local").getByRole("alert").textContent).toContain("Autenticação recusada"); expectClosed();
});
test.each([204, 500])("logout result %s never preserves privileged UI state", async status => {
  await login(); replies.push(status === 204 ? response(204, null) : problem(500, "internal_error"));
  await submit("Encerrar sessão"); expectClosed();
  expect(requests[1]!.method).toBe("DELETE"); expect(requests[1]!.headers.get("If-Match")).toBe('"fixture-revision"');
  expect(region("Encerrar sessão").queryByRole(status === 204 ? "status" : "alert")).not.toBeNull();
});
test("token issuance exposes only ephemeral secret; no logging or storage", async () => {
  const log = vi.spyOn(console, "log"); const warn = vi.spyOn(console, "warn"); const error = vi.spyOn(console, "error");
  const storage = vi.spyOn(Storage.prototype, "setItem");
  await login(); replies.push(response(201, { data: pat }));
  await submit("Emitir token pessoal", { name: "Fixture", scopes: "fixture-action" });
  const input = region("Emitir token pessoal").getByLabelText("Token emitido") as HTMLInputElement;
  expect(input.value === tokenValue).toBe(true); expect(input.type).toBe("password");
  await act(async () => { fireEvent.click(region("Emitir token pessoal").getByRole("button", { name: "Descartar valor exibido" })); });
  expect(region("Emitir token pessoal").queryByLabelText("Token emitido")).toBeNull();
  expect(log).not.toHaveBeenCalled(); expect(warn).not.toHaveBeenCalled(); expect(error).not.toHaveBeenCalled(); expect(storage).not.toHaveBeenCalled();
  expect(container.textContent?.includes(tokenValue)).toBe(false);
});
test.each([401, 403, 422])("token creation rejection %s shows error and no token", async status => {
  await login(); replies.push(problem(status, status === 422 ? "validation_failed" : status === 401 ? "unauthorized" : "forbidden"));
  await submit("Emitir token pessoal", { name: "Fixture", scopes: "fixture-action" });
  expect(region("Emitir token pessoal").getByRole("alert")).toBeDefined();
  expect(region("Emitir token pessoal").queryByLabelText("Token emitido")).toBeNull();
  if (status !== 422) expectClosed();
});
test("members listing and linking use published boundaries without account CRUD", async () => {
  await login(); replies.push(response(200, { items: [member], page: { limit: 20 } }));
  await submit("Membros locais do projeto", { projectId });
  expect(region("Membros locais do projeto").getByRole("status").textContent).toContain(userId);
  replies.push(response(201, { data: member }));
  await submit("Vincular conta local existente", { projectId, userId, role: "viewer" });
  expect(region("Vincular conta local existente").getByRole("status").textContent).toContain("Vínculo confirmado");
  expect(requests[1]!.method).toBe("GET"); expect(requests[2]!.method).toBe("POST");
  expect(requests[2]!.url).toContain(`/projects/${projectId}/members`);
});
test.each([401, 403])("member listing rejection %s clears session and previous protected results", async status => {
  await login(); replies.push(problem(status, status === 401 ? "unauthorized" : "forbidden"));
  await submit("Membros locais do projeto", { projectId }); expectClosed();
  expect(region("Membros locais do projeto").getByRole("alert").textContent).toContain(String(status));
});
test("UUID casing does not reject the same authoritative project/member identity", async () => {
  const canonicalProject = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa";
  const canonicalUser = "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb";
  const canonicalMember: ProjectMember = { ...member, projectId: canonicalProject, userId: canonicalUser };
  await login(); replies.push(response(200, { items: [canonicalMember], page: { limit: 20 } }));
  await submit("Membros locais do projeto", { projectId: canonicalProject.toUpperCase() });
  expect(region("Membros locais do projeto").getByRole("status").textContent).toContain(canonicalUser);
  replies.push(response(201, { data: canonicalMember }));
  await submit("Vincular conta local existente", { projectId: canonicalProject.toUpperCase(), userId: canonicalUser.toUpperCase(), role: "viewer" });
  expect(region("Vincular conta local existente").getByRole("status").textContent).toContain("Vínculo confirmado");
});
test.each([401, 403])("member linking rejection %s fails closed", async status => {
  await login(); replies.push(problem(status, status === 401 ? "unauthorized" : "forbidden"));
  await submit("Vincular conta local existente", { projectId, userId, role: "viewer" }); expectClosed();
  expect(region("Vincular conta local existente").queryByRole("status")).toBeNull();
});
test("OIDC callback validates a session without a provider or local fallback", async () => {
  replies.push(response(200, { data: { session: session(), linked: false } }));
  await submit("Callback OIDC", { code: "synthetic-code", state: "synthetic-state" });
  expect(authenticated()).toBe(true); expect(requests[0]!.url).toContain("/auth/oidc/callback?code=synthetic-code&state=synthetic-state");
  expect((region("Callback OIDC").getByLabelText("Code OIDC") as HTMLInputElement).value).toBe("");
});
test.each([[400, "oidc_state_invalid"], [502, "oidc_exchange_failed"], [409, "identity_link_conflict"], [500, "internal_error"]] as const)("OIDC %s/%s rejects authentication", async (status, code) => {
  await login(); replies.push(problem(status, code));
  await submit("Callback OIDC", { code: "synthetic-code", state: "synthetic-state" }); expectClosed();
  expect(region("Callback OIDC").getByRole("alert").textContent).toContain(code);
});
test("authorization denied remains a negative server decision", async () => {
  await login(); replies.push(response(200, { data: { allowed: false, policyVersion: "fixture-policy", reasonCode: "denied" } }));
  await submit("Consultar autorização", { action: "fixture-action", resourceType: "fixture-resource" });
  const content = region("Consultar autorização").getByRole("status").textContent!;
  expect(content).toContain("Permissão negada"); expect(content).not.toContain("Permissão confirmada");
});
test.each([null, {}, { data: {} }, { data: { ...session(), csrfToken: "short" } },
  { data: { ...session(), expiresAt: "2000-01-01T00:00:00Z" } }, { data: { ...session(), sessionId: "invalid" } },
  { data: { ...session(), administrator: true } }])("malformed/expired session fails closed", async body => {
  replies.push(response(202, body)); await submit("Sessão local", { username: "fixture-user", password });
  expectClosed(); expect(region("Sessão local").getByRole("alert").textContent).toContain("resposta inválida");
});
test("unexpected successful HTTP status cannot authenticate", async () => {
  replies.push(response(200, { data: session() })); await submit("Sessão local", { username: "fixture-user", password }); expectClosed();
});
test("malformed Problem Details is not rendered as trusted structured data", async () => {
  replies.push(response(401, { title: "untrusted", status: 200 }, { "content-type": "application/problem+json" }));
  await submit("Sessão local", { username: "fixture-user", password }); expectClosed();
  expect(region("Sessão local").getByRole("alert").textContent).not.toContain("untrusted");
});
test("authorization must be a boolean; malformed result clears session", async () => {
  await login(); replies.push(response(200, { data: { allowed: "true", policyVersion: "fixture", reasonCode: "fixture" } }));
  await submit("Consultar autorização", { action: "fixture-action", resourceType: "fixture-resource" }); expectClosed();
});
test("unchanged retry preserves idempotency; changed input starts a new intention", async () => {
  replies.push(new Error("network error with sensitive information"));
  await submit("Sessão local", { username: "fixture-user", password });
  replies.push(problem(401, "invalid_credentials")); await submit("Sessão local");
  expect(requests[0]!.headers.get("Idempotency-Key")).toBe(requests[1]!.headers.get("Idempotency-Key"));
  replies.push(problem(401, "invalid_credentials")); await submit("Sessão local", { username: "changed-user" });
  expect(requests[1]!.headers.get("Idempotency-Key")).not.toBe(requests[2]!.headers.get("Idempotency-Key"));
  expect(container.textContent).not.toContain("sensitive information");
});
test("expiration removes session and prevents subsequent protected calls", async () => {
  vi.useFakeTimers(); await login();
  await act(async () => { await vi.advanceTimersByTimeAsync(60_001); });
  expectClosed(); expect(within(container).getByText("Sessão expirada; autentique novamente.")).toBeDefined();
  await submit("Membros locais do projeto", { projectId }); expect(requests).toHaveLength(1);
});
test("token secret is discarded when page becomes hidden", async () => {
  await login(); replies.push(response(201, { data: pat }));
  await submit("Emitir token pessoal", { name: "Fixture", scopes: "fixture-action" });
  vi.spyOn(document, "hidden", "get").mockReturnValue(true);
  await act(async () => { document.dispatchEvent(new Event("visibilitychange")); });
  expect(region("Emitir token pessoal").queryByLabelText("Token emitido")).toBeNull();
});
test("malformed token and foreign-project member responses fail closed", async () => {
  await login(); replies.push(response(201, { data: { ...pat, token: 123 } }));
  await submit("Emitir token pessoal", { name: "Fixture", scopes: "fixture-action" }); expectClosed();
  await login(); replies.push(response(200, { items: [{ ...member, projectId: userId }], page: { limit: 20 } }));
  await submit("Membros locais do projeto", { projectId }); expectClosed();
});
test("malformed OIDC callback cannot authenticate", async () => {
  replies.push(response(200, { data: { session: session(), linked: "true" } }));
  await submit("Callback OIDC", { code: "synthetic-code", state: "synthetic-state" }); expectClosed();
});
test("pending operation shows loading and prevents duplicate submissions", async () => {
  let release: ((reply: Response) => void) | undefined;
  client.setConfig({ fetch: async request => { requests.push(request); return new Promise(resolve => { release = resolve; }); } });
  await submit("Sessão local", { username: "fixture-user", password });
  expect(region("Sessão local").getByRole("status").textContent).toContain("Enviando");
  await submit("Sessão local"); expect(requests).toHaveLength(1);
  await act(async () => { release!(response(202, { data: session() })); }); expect(authenticated()).toBe(true);
});
