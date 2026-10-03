import { createClient } from "@hey-api/openapi-ts";
import { readFile, readdir, mkdtemp, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import { parseLocalSource, repositoryRoot } from "./config.mjs";

export async function generate(sourceBytes, output) {
  await createClient({
    input: parseLocalSource(sourceBytes),
    tsConfigPath: path.join(repositoryRoot, "src/frontend/tsconfig.json"),
    output: { path: output, format: false, lint: false },
    plugins: ["@hey-api/typescript", "@hey-api/sdk", { name: "@hey-api/client-fetch", bundle: false }],
    logs: { level: "silent" },
  });
}

export async function artifactFiles(directory, prefix = "") {
  const result = new Map();
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const relative = prefix + entry.name;
    if (entry.isSymbolicLink()) throw new Error("Generated artifact cannot contain symlinks");
    if (entry.isDirectory()) {
      for (const [key, bytes] of await artifactFiles(path.join(directory, entry.name), relative + "/")) {
        result.set(key, bytes);
      }
    } else {
      const bytes = await readFile(path.join(directory, entry.name));
      // Match Git text normalization on Windows checkouts; every other byte is compared.
      result.set(relative, Buffer.from(bytes.toString("utf8").replaceAll("\r\n", "\n")));
    }
  }
  return new Map([...result].sort(([a], [b]) => a.localeCompare(b, "en")));
}

export async function checkArtifact(sourceBytes, committedDirectory) {
  const temporary = await mkdtemp(path.join(tmpdir(), "dsgeorref-openapi-"));
  try {
    await generate(sourceBytes, path.join(temporary, "generated"));
    const expected = await artifactFiles(path.join(temporary, "generated"));
    const actual = await artifactFiles(committedDirectory);
    if (expected.size === 0 || expected.size !== actual.size ||
        [...expected].some(([name, bytes]) => !actual.get(name)?.equals(bytes))) {
      throw new Error("Generated artifact drift: run openapi:generate and commit all outputs");
    }
    return [...expected.keys()];
  } finally {
    await rm(temporary, { recursive: true, force: true });
  }
}
