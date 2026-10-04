import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import path from "node:path";
import { isDeepStrictEqual } from "node:util";
import { parse } from "yaml";

export const repositoryRoot = fileURLToPath(new URL("../../../../", import.meta.url));
export const configPath = path.join(repositoryRoot, "src/frontend/openapi-client.config.json");

export async function readSource(filename) {
  const bytes = await readFile(filename);
  parseLocalSource(bytes);
  return bytes;
}

export async function loadConfig(filename = configPath) {
  const config = JSON.parse(await readFile(filename, "utf8"));
  const expected = {
    schemaVersion: 1,
    source: "contracts/http/openapi.yaml",
    output: "src/frontend/src/contexts/operator_experience/contracts/openapi/generated",
    generator: { name: "@hey-api/openapi-ts", version: "0.87.5" },
    transport: { name: "@hey-api/client-fetch", version: "0.13.1", bundle: false },
    semanticDiff: { name: "@oasdiff-js/oasdiff-js", version: "1.0.0", engineVersion: "1.15.0", baseline: "origin/main" },
  };
  for (const [key, value] of Object.entries(expected)) {
    if (!isDeepStrictEqual(config[key], value)) {
      throw new Error(`Invalid OpenAPI configuration: ${key}`);
    }
  }
  return config;
}

/** Deny external references before either tool sees the document: generation is offline. */
export function parseLocalSource(bytes) {
  const document = parse(bytes.toString());
  if (document?.openapi !== "3.1.0" || !document.paths || !document.components) {
    throw new Error("Invalid OpenAPI 3.1 source");
  }
  function visit(value) {
    if (!value || typeof value !== "object") return;
    if (typeof value.$ref === "string" && !value.$ref.startsWith("#/")) {
      throw new Error("External OpenAPI references are prohibited");
    }
    for (const child of Object.values(value)) visit(child);
  }
  visit(document);
  return document;
}
