import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { registerHooks } from "node:module";

const generated = new URL(
  "../../../../src/frontend/src/contexts/operator_experience/contracts/openapi/generated/",
  import.meta.url,
);

// The generated SDK uses bundler-style imports. Load the committed TypeScript
// with Node's type stripping and resolve only imports internal to that SDK.
const hooks = registerHooks({
  resolve(specifier, context, nextResolve) {
    if (context.parentURL?.startsWith(generated.href) && specifier.startsWith(".")) {
      const suffix = specifier.endsWith("/client") ? "/index.ts" : ".ts";
      return nextResolve(specifier + suffix, context);
    }
    return nextResolve(specifier, context);
  },
});

try {
  const sdk = await import(new URL("sdk.gen.ts", generated).href);
  const input = JSON.parse(readFileSync(0, "utf8"));
  if (input.development) await verifySurface(sdk, input);
  else await verifyLogout(sdk, input);
} finally {
  hooks.deregister();
}

async function verifyLogout({ deleteAuthSession }, { baseUrl, headers }) {
  const rejected = await deleteAuthSession({
    baseUrl,
    headers: { ...headers, "X-CSRF-Token": "invalid" },
  });
  assert.equal(rejected.response.status, 401);
  assert.equal(rejected.error.code, "unauthorized");

  const accepted = await deleteAuthSession({ baseUrl, headers });
  assert.equal(accepted.response.status, 204);
  assert.match(accepted.response.headers.get("set-cookie"), /Max-Age=0/);
}

async function verifySurface(sdk, { baseUrl, headers, password, projectId, targetId }) {
  const body = { username: "admin", password };
  const loginOptions = { baseUrl, headers, body };
  const accepted = await sdk.postAuthSession(loginOptions);
  assert.equal(accepted.response.status, 202);
  const cookie = accepted.response.headers.get("set-cookie");
  assert.match(cookie, /; Secure; HttpOnly; SameSite=Strict$/);
  assert.ok(accepted.data.data.csrfToken.length >= 32);

  const replay = await sdk.postAuthSession(loginOptions);
  assert.equal(replay.response.status, 401);
  assert.equal(replay.response.headers.get("set-cookie"), null);
  const authenticated = {
    baseUrl, headers: { ...headers, Cookie: cookie.split(";")[0] },
  };
  const query = { resourceType: "project", resourceId: projectId, action: "project_member:list" };
  const decision = await sdk.getAuthorizationCheck({ ...authenticated, query });
  assert.equal(decision.response.status, 200);
  assert.equal(decision.data.data.allowed, true);
  const denied = await sdk.getAuthorizationCheck({
    ...authenticated, query: { action: "instance:bootstrap", resourceType: "instance" },
  });
  assert.equal(denied.data.data.allowed, false);

  const path = { projectId };
  const request = { ...authenticated, path, body: { userId: targetId, role: "viewer" } };
  const csrfMissing = await sdk.postProjectsProjectidMembers(request);
  assert.equal(csrfMissing.response.status, 403);
  assert.equal(csrfMissing.error.code, "forbidden");
  const mutation = {
    ...request, headers: { ...authenticated.headers, "X-CSRF-Token": accepted.data.data.csrfToken },
  };
  const added = await sdk.postProjectsProjectidMembers(mutation);
  assert.equal(added.response.status, 201);
  assert.equal(added.data.data.userId, targetId);
  const repeated = await sdk.postProjectsProjectidMembers(mutation);
  assert.deepEqual(repeated.data, added.data);
  const members = await sdk.getProjectsProjectidMembers({ ...authenticated, path });
  assert.equal(members.response.status, 200);
  assert.ok(members.data.items.some((member) => member.userId === targetId));

  const issued = await sdk.postAuthTokens({
    ...authenticated, headers: mutation.headers,
    body: { name: "dev-validation", scopes: ["authorization:check"] },
  });
  assert.equal(issued.response.status, 201);
  assert.match(issued.data.data.token, /^pat_/);
  await verifyLogout(sdk, {
    baseUrl, headers: { ...mutation.headers, "If-Match": accepted.response.headers.get("etag") },
  });
  const expired = await sdk.getProjectsProjectidMembers({ ...authenticated, path });
  assert.equal(expired.response.status, 401);
}
