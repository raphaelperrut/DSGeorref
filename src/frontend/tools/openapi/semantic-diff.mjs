import { runOasdiffBreakingFromSpecs } from "@oasdiff-js/oasdiff-js";
import { parseLocalSource } from "./config.mjs";

export async function semanticDiff(baseBytes, revisionBytes) {
  const result = await runOasdiffBreakingFromSpecs(
    parseLocalSource(baseBytes), parseLocalSource(revisionBytes),
    { failOn: "WARN", format: "json" },
  );
  if (result.exitCode !== 0 || result.changes.length > 0) {
    throw new Error(`OpenAPI semantic diff failed: ${result.stderr}\n${result.stdout}`);
  }
  return result;
}
