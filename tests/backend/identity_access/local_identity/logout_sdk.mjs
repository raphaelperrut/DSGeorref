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
  const { deleteAuthSession } = await import(new URL("sdk.gen.ts", generated).href);
  const { baseUrl, headers } = JSON.parse(readFileSync(0, "utf8"));
  const rejected = await deleteAuthSession({
    baseUrl,
    headers: { ...headers, "X-CSRF-Token": "invalid" },
  });
  assert.equal(rejected.response.status, 401);
  assert.equal(rejected.error.code, "unauthorized");

  const accepted = await deleteAuthSession({ baseUrl, headers });
  assert.equal(accepted.response.status, 204);
  assert.match(accepted.response.headers.get("set-cookie"), /Max-Age=0/);
} finally {
  hooks.deregister();
}
