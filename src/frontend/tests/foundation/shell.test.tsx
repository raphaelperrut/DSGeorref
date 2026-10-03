import { act } from "react";
import { expect, test } from "vitest";
import { getByRole } from "@testing-library/dom";
import { mountFrontendShell, client, api } from "../../src/contexts/operator_experience/contracts/frontend-shell";
import { client as generatedClient } from "../../src/contexts/operator_experience/contracts/openapi/generated/client.gen";
import { getAdminHealth } from "../../src/contexts/operator_experience/contracts/openapi/generated/sdk.gen";
import type { GetAdminHealthResponses } from "../../src/contexts/operator_experience/contracts/openapi/generated/types.gen";

Object.assign(globalThis, { IS_REACT_ACT_ENVIRONMENT: true });

test("public composition and contract tests consume the same generated SDK/client", async () => {
  expect(client).toBe(generatedClient);
  expect(api.getAdminHealth).toBe(getAdminHealth);
  const container = document.createElement("div");
  document.body.append(container);
  let unmount: () => void = () => {};
  await act(async () => {
    unmount = mountFrontendShell(container, { children: <p>Composition content</p> });
  });
  expect(getByRole(container, "heading", { name: "DSGeorref" })).toBeDefined();
  expect(container.querySelector("main")?.dataset.openapiBaseUrl).toBe(client.getConfig().baseUrl);
  expect(container.textContent).toContain("Composition content");
  await act(async () => unmount());
  expect(container.childElementCount).toBe(0);
  container.remove();
});

test("generated SDK resolves a real published operation using an isolated Fetch stub", async () => {
  let requestedUrl = "";
  // Response is derived from the generated type; no second DTO declaration.
  const response: GetAdminHealthResponses[200] = { data: { status: "ok", version: "2.6.0" } };
  const result = await getAdminHealth({
    baseUrl: "https://example.invalid/api/v1",
    fetch: async (request) => {
      requestedUrl = (request as Request).url;
      return new Response(JSON.stringify(response), { headers: { "content-type": "application/json" } });
    },
  });
  expect(requestedUrl).toBe("https://example.invalid/api/v1/admin/health");
  expect(result.data).toEqual(response);
});
