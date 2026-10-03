// @vitest-environment node
import { afterEach, expect, test, vi } from "vitest";
import { cp, mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import { execFileSync, spawnSync } from "node:child_process";
import { pathToFileURL } from "node:url";
import { configPath, loadConfig, parseLocalSource, readSource, repositoryRoot } from "../../tools/openapi/config.mjs";
import { artifactFiles, checkArtifact, generate } from "../../tools/openapi/generation.mjs";
import { semanticDiff } from "../../tools/openapi/semantic-diff.mjs";

const source = execFileSync("git", ["show", "HEAD:contracts/http/openapi.yaml"], {
  cwd: repositoryRoot, maxBuffer: 20 * 1024 * 1024,
});
const output = path.join(repositoryRoot, (await loadConfig()).output);
const temporaryDirectories = [];
async function temporary() {
  const directory = await mkdtemp(path.join(tmpdir(), "dsgeorref-foundation-"));
  temporaryDirectories.push(directory);
  return directory;
}
afterEach(async () => {
  vi.unstubAllGlobals();
  for (const directory of temporaryDirectories.splice(0)) {
    // All directories originate from mkdtemp under the OS temporary root.
    await rm(directory, { recursive: true, force: true });
  }
});

test("generation is offline and byte-identical in two isolated directories", async () => {
  const network = vi.fn(() => { throw new Error("Network prohibited during generation"); });
  vi.stubGlobal("fetch", network);
  const directory = await temporary();
  await generate(source, path.join(directory, "one"));
  await generate(source, path.join(directory, "two"));
  expect(await artifactFiles(path.join(directory, "one"))).toEqual(await artifactFiles(path.join(directory, "two")));
  expect(network).not.toHaveBeenCalled();
  await expect(checkArtifact(source, output)).resolves.toContain("types.gen.ts");
}, 30_000);

test("source absent fails and external references fail closed", async () => {
  const directory = await temporary();
  await expect(readSource(path.join(directory, "missing.yaml")).then(bytes => generate(bytes, directory)))
    .rejects.toMatchObject({ code: "ENOENT" });
  const document = parseLocalSource(source);
  document.components.schemas.Problem = { $ref: "https://example.invalid/schema.json" };
  await expect(generate(Buffer.from(JSON.stringify(document)), path.join(directory, "generated")))
    .rejects.toThrow("External OpenAPI references");
});

test.each(["malformed", "source", "generator", "output"])("invalid configuration %s fails", async (field) => {
  const filename = path.join(await temporary(), "config.json");
  const config = JSON.parse(await readFile(configPath, "utf8"));
  if (field !== "malformed") config[field] = "invalid";
  await writeFile(filename, field === "malformed" ? "{" : JSON.stringify(config));
  await expect(loadConfig(filename)).rejects.toThrow();
});

test.each(["edited", "missing", "extra"])("openapi:check rejects %s artifact with nonzero exit", async (mode) => {
  const directory = path.join(await temporary(), "generated");
  await cp(output, directory, { recursive: true });
  if (mode === "edited") await writeFile(path.join(directory, "types.gen.ts"), "// drift\n");
  if (mode === "missing") await rm(path.join(directory, "types.gen.ts"));
  if (mode === "extra") await writeFile(path.join(directory, "extra.ts"), "// extra\n");
  // Execute the exact check used by openapi:check, against a copy rather than production outputs.
  const moduleUrl = pathToFileURL(path.join(repositoryRoot, "src/frontend/tools/openapi/generation.mjs")).href;
  const result = spawnSync(process.execPath, ["--input-type=module", "-e",
    `import { readFile } from 'node:fs/promises'; import { checkArtifact } from ${JSON.stringify(moduleUrl)}; await checkArtifact(await readFile(process.argv[1]), process.argv[2]);`,
    path.join(repositoryRoot, "contracts/http/openapi.yaml"), directory], { encoding: "utf8" });
  expect(result.status).toBe(1);
  expect(result.stderr).toContain("Generated artifact drift");
}, 30_000);

test("semantic gate accepts identical source and a documentation addition", async () => {
  await expect(semanticDiff(source, source)).resolves.toMatchObject({ exitCode: 0, changes: [] });
  const document = parseLocalSource(source);
  document.info.description += " Documentation-only clarification.";
  await expect(semanticDiff(source, Buffer.from(JSON.stringify(document))))
    .resolves.toMatchObject({ exitCode: 0, changes: [] });
}, 30_000);

test("semantic gate rejects a removed operation in a copy of the real OpenAPI", async () => {
  const document = parseLocalSource(source);
  delete document.paths["/admin/health"];
  await expect(semanticDiff(source, Buffer.from(JSON.stringify(document))))
    .rejects.toThrow("api-path-removed-without-deprecation");
}, 30_000);

test("semantic gate rejects a newly required request field in a copy", async () => {
  const document = parseLocalSource(source);
  const request = document.components.schemas.PostProjectsRequest;
  request.required = [...request.required, "description"];
  await expect(semanticDiff(source, Buffer.from(JSON.stringify(document))))
    .rejects.toThrow("request-property-became-required");
}, 30_000);

test("semantic gate rejects removing a published response property", async () => {
  const document = parseLocalSource(source);
  delete document.components.schemas.HealthStatus.properties.version;
  document.components.schemas.HealthStatus.required = ["status"];
  await expect(semanticDiff(source, Buffer.from(JSON.stringify(document))))
    .rejects.toThrow("response-required-property-removed");
}, 30_000);

test("semantic gate rejects expanding a response enum consumed by the client", async () => {
  const document = parseLocalSource(source);
  document.components.schemas.HealthStatus.properties.status.enum.push("fixture-only-status");
  await expect(semanticDiff(source, Buffer.from(JSON.stringify(document))))
    .rejects.toThrow("response-property-enum-value-added");
}, 30_000);
