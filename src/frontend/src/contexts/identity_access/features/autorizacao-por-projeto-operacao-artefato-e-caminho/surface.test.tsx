import { act } from "react";
import { afterEach, beforeEach, expect, test, vi } from "vitest";
import { fireEvent, within } from "@testing-library/dom";
import { api, client } from "../../../operator_experience/contracts/frontend-shell";
import { getAuthorizationCheck } from "../../../operator_experience/contracts/openapi/generated";
import { mountProjectAccess } from "./index";

Object.assign(globalThis, { IS_REACT_ACT_ENVIRONMENT: true });
const projectId = "00000000-0000-4000-8000-000000000001";
const userId = "00000000-0000-4000-8000-000000000002";
const csrf = "synthetic-csrf-for-frontend-contract-only";
const member = { projectId, userId, role: "viewer", revision: 1 };
const decision = { allowed: true, policyVersion: "1.1.0", reasonCode: "granted" };
const original = client.getConfig();
let container: HTMLDivElement;
let unmount: () => void;
let replies: Array<Response | Error>;
let requests: Request[];
const response = (status: number, data: unknown, type = "application/json") =>
  new Response(JSON.stringify(data), { status, headers: { "content-type": type } });
const problem = (status: number, code = "forbidden") => response(status,
  { type: "https://example.invalid/problems/" + code, title: code, code, status, detail: "Pedido recusado", instance: "/fixture/request" },
  "application/problem+json");
beforeEach(async () => {
  replies = []; requests = [];
  client.setConfig({ baseUrl: "/api/v1", fetch: async (input, init) => {
    requests.push(new Request(input, init));
    const reply = replies.shift();
    if (reply instanceof Error) throw reply;
    if (!reply) throw new Error("Unexpected request");
    return reply;
  } });
  container = document.createElement("div"); document.body.append(container);
  await act(async () => { unmount = mountProjectAccess(container); });
});
afterEach(async () => {
  await act(async () => unmount()); container.remove();
  client.setConfig({ ...original, fetch: original.fetch ?? globalThis.fetch }); vi.useRealTimers();
});
const region = (name: string) => within(within(container).getByRole("region", { name }));
async function edit(name: string, fields: Record<string, string>) {
  const form = region(name).getByRole("form");
  await act(async () => {
    for (const [field, content] of Object.entries(fields)) {
      fireEvent.input(form.querySelector(`[name="${field}"]`)!, { target: { value: content } });
    }
  });
}
async function submit(name: string, fields: Record<string, string> = {}) {
  await edit(name, fields);
  await act(async () => { fireEvent.submit(region(name).getByRole("form")); });
}
async function login() {
  replies.push(response(202, { data: { sessionId: projectId, userId, csrfToken: csrf,
    expiresAt: new Date(Date.now() + 60_000).toISOString() } }));
  await submit("Sessão local", { username: "fixture-user", password: "synthetic-password" });
}
const query = { action: "project_member:list", resourceType: "project", resourceId: projectId };
const add = { projectId, userId, role: "viewer" };
const output = () => region("Resultado");
const closed = () => expect(output().queryByText("Permissão confirmada nesta consulta.")).toBeNull();

test("test_epic_010_superficie", async () => {
  expect(api.getAuthorizationCheck).toBe(getAuthorizationCheck);
  await submit("Consultar autorização", query); expect(requests).toHaveLength(0);
  await login();
  replies.push(response(200, { data: decision }));
  await submit("Consultar autorização", query);
  expect(output().getByText("Permissão confirmada nesta consulta.")).toBeTruthy();
  const request = requests.at(-1)!;
  expect(request.method).toBe("GET");
  expect(Object.fromEntries(new URL(request.url).searchParams)).toEqual(query);
  expect(request.cache).toBe("no-store"); expect(request.credentials).toBe("same-origin");
  expect(request.headers.has("Idempotency-Key")).toBe(false);
  await edit("Consultar autorização", { resourceId: userId }); closed();
  replies.push(response(200, { data: { ...decision, allowed: false, reasonCode: "access_denied" } }));
  await submit("Consultar autorização");
  expect(output().getByText("Permissão negada pela API.")).toBeTruthy(); closed();
  replies.push(response(200, { items: [], page: { limit: 100 } }));
  await submit("Membros do projeto", { projectId });
  expect(output().getByText("Nenhum membro retornado pela API.")).toBeTruthy();
  replies.push(response(201, { data: member }));
  await submit("Vincular conta existente", add);
  expect(output().getByText(/Vínculo confirmado/)).toBeTruthy();
  expect(await requests.at(-1)!.json()).toEqual({ userId, role: "viewer" });
  expect(requests.at(-1)!.headers.get("X-CSRF-Token")).toBe(csrf);
});

test.each(["artifact", "logical_path", "physical_path"])("delegates %s denial without inventing path fields", async resourceType => {
  await login();
  replies.push(response(200, { data: { ...decision, allowed: false, reasonCode: "access_denied" } }));
  await submit("Consultar autorização", { ...query, resourceType });
  expect(Object.fromEntries(new URL(requests.at(-1)!.url).searchParams)).toEqual({ ...query, resourceType });
  expect(output().getByText("Permissão negada pela API.")).toBeTruthy(); closed();
});

test.each([401, 403, 404, 409, 412, 422, 429, 500])("preserves HTTP %s and Problem Details", async status => {
  await login(); replies.push(problem(status));
  await submit("Consultar autorização", query);
  for (const field of ["type", "title", "status", "code", "detail", "instance"]) expect(output().getByText(field)).toBeTruthy();
  expect(output().getByText(String(status))).toBeTruthy(); closed();
  if ([401, 403].includes(status)) {
    await submit("Membros do projeto", { projectId }); expect(requests).toHaveLength(2);
  }
});

test.each([
  { data: { ...decision, allowed: "true" } }, { data: { allowed: true } },
  { data: { ...decision, extraGrant: true } }, { data: null }, {}, { data: { ...decision, policyVersion: "" } },
])("rejects malformed successful decision %#", async data => {
  await login(); replies.push(response(200, { data: decision })); await submit("Consultar autorização", query);
  replies.push(response(200, data)); await submit("Consultar autorização");
  expect(output().getByRole("alert")).toBeTruthy(); expect(output().getByText(/HTTP 200/)).toBeTruthy(); closed();
});

test.each([200, 403, 500])("malformed JSON retains HTTP %s", async status => {
  await login(); replies.push(new Response("{broken", { status, headers: { "content-type": "application/json" } }));
  await submit("Consultar autorização", query);
  expect(output().getByText(new RegExp(`HTTP ${status}`))).toBeTruthy(); closed();
});

test("wrong status, media type, network failure and mismatching membership never succeed", async () => {
  await login();
  for (const reply of [response(201, { data: decision }), response(200, { data: decision }, "text/html"), new Error("offline")]) {
    replies.push(reply); await submit("Consultar autorização", query); expect(output().getByRole("alert")).toBeTruthy(); closed();
  }
  replies.push(response(201, { data: { ...member, userId: projectId } }));
  await submit("Vincular conta existente", add); expect(output().getByRole("alert")).toBeTruthy();
  expect(output().queryByText(/Vínculo confirmado/)).toBeNull();
});

test("unchanged retries preserve idempotency; edits and confirmed success renew it", async () => {
  await login(); replies.push(problem(409, "conflict")); await submit("Vincular conta existente", add);
  const first = requests.at(-1)!.headers.get("Idempotency-Key"); expect(first).toBeTruthy();
  replies.push(new Error("lost response")); await submit("Vincular conta existente");
  expect(requests.at(-1)!.headers.get("Idempotency-Key")).toBe(first);
  replies.push(response(201, { data: member })); await submit("Vincular conta existente");
  expect(requests.at(-1)!.headers.get("Idempotency-Key")).toBe(first);
  replies.push(problem(409, "conflict")); await submit("Vincular conta existente");
  const afterSuccess = requests.at(-1)!.headers.get("Idempotency-Key"); expect(afterSuccess).not.toBe(first);
  replies.push(problem(409, "conflict")); await submit("Vincular conta existente", { role: "editor" });
  expect(requests.at(-1)!.headers.get("Idempotency-Key")).not.toBe(afterSuccess);
});

test("session expiry clears decision and prevents protected requests", async () => {
  vi.useFakeTimers(); await login(); replies.push(response(200, { data: decision })); await submit("Consultar autorização", query);
  await act(async () => { await vi.advanceTimersByTimeAsync(60_001); });
  closed(); expect(output().getByText(/Sessão expirada/)).toBeTruthy();
  await submit("Consultar autorização"); expect(requests).toHaveLength(2);
});

test("partial member page is explicit; cross-project and malformed lists fail closed", async () => {
  await login(); replies.push(response(200, { items: [member], page: { limit: 1, nextCursor: "cursor" } }));
  await submit("Membros do projeto", { projectId }); expect(output().getByText(/lista é parcial/)).toBeTruthy();
  for (const items of [[{ ...member, projectId: userId }], [{ ...member, revision: 0 }]]) {
    replies.push(response(200, { items, page: { limit: 1 } })); await submit("Membros do projeto");
    expect(output().getByRole("alert")).toBeTruthy();
  }
});

test("invalid Problem Details never masks HTTP denial or confirms success", async () => {
  await login();
  replies.push(response(403, { type: "invalid", title: "forbidden", code: "forbidden", status: 200 }, "application/problem+json"));
  await submit("Consultar autorização", query);
  expect(output().getByRole("alert")).toHaveProperty("textContent", expect.stringContaining("HTTP 403")); closed();
  await submit("Membros do projeto", { projectId }); expect(requests).toHaveLength(2);
});

test("duplicate submission is locked while pending; expiry rejects a late allow", async () => {
  vi.useFakeTimers(); await login();
  let complete!: (reply: Response) => void;
  client.setConfig({ fetch: async input => {
    requests.push(new Request(input)); return new Promise<Response>(resolve => { complete = resolve; });
  } });
  await edit("Consultar autorização", query);
  const form = region("Consultar autorização").getByRole("form");
  await act(async () => { fireEvent.submit(form); fireEvent.submit(form); });
  expect(requests).toHaveLength(2); expect(output().getByText("Aguardando a API…")).toBeTruthy();
  await act(async () => { await vi.advanceTimersByTimeAsync(60_001); });
  await act(async () => complete(response(200, { data: decision })));
  closed(); expect(output().getByText(/Sessão expirada/)).toBeTruthy();
});

test("invalid authentication stays closed and does not disclose submitted password", async () => {
  const password = "synthetic-secret-login-fixture";
  replies.push(response(401, { type: "https://example.invalid/problems/invalid_credentials", title: "invalid_credentials", code: "invalid_credentials", status: 401,
    detail: `refused ${password}` }, "application/problem+json"));
  await submit("Sessão local", { username: "fixture-user", password });
  expect(output().getByText(/\[redigido\]/)).toBeTruthy();
  expect(output().getByRole("alert").textContent).not.toContain(password);
  replies.push(response(202, { data: { userId } }));
  await submit("Sessão local"); expect(output().getByText(/resposta inválida/)).toBeTruthy();
  await submit("Consultar autorização", query); expect(requests).toHaveLength(2); closed();
});
