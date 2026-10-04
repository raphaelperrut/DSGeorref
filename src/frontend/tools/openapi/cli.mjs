import { execFileSync } from "node:child_process";
import { rm } from "node:fs/promises";
import path from "node:path";
import { configPath, loadConfig, readSource, repositoryRoot } from "./config.mjs";
import { checkArtifact, generate } from "./generation.mjs";
import { semanticDiff } from "./semantic-diff.mjs";

try {
  const [command, ...args] = process.argv.slice(2);
  const config = await loadConfig(configPath);
  const workingSource = await readSource(path.join(repositoryRoot, config.source));
  const gitSource = (ref) => execFileSync("git", ["show", `${ref}:${config.source}`], {
    cwd: repositoryRoot, maxBuffer: 20 * 1024 * 1024,
  });
  // A local uncommitted specification is never a generation authority.
  const source = gitSource("HEAD");
  const normalize = (bytes) => bytes.toString("utf8").replaceAll("\r\n", "\n");
  if (normalize(workingSource) !== normalize(source)) throw new Error("OpenAPI source differs from committed HEAD");
  const output = path.join(repositoryRoot, config.output);
  if (command === "generate" && args.length === 0) {
    // output is fixed/validated above, never a caller-supplied directory.
    await rm(output, { recursive: true, force: true });
    await generate(source, output);
  } else if (command === "check" && args.length === 0) {
    await checkArtifact(source, output);
  } else if (command === "diff" && args.length <= 1) {
    const baseline = args[0] ?? config.semanticDiff.baseline;
    const sha = execFileSync("git", ["rev-parse", "--verify", "--end-of-options", `${baseline}^{commit}`], {
      cwd: repositoryRoot, encoding: "utf8",
    }).trim();
    await semanticDiff(gitSource(sha), source);
  } else {
    throw new Error("Usage: cli.mjs generate|check|diff [baseline-ref]");
  }
  console.log(`OpenAPI ${command}: PASS`);
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
}
