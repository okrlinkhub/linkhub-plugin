import { cp, mkdir, rm } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const pluginRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const repositoryRoot = resolve(pluginRoot, "../..");
const legacyRoot = resolve(repositoryRoot, ".claude/skills");
const skillNames = [
  "linkhub-report-coach",
  "linkhub-indicator-analyst",
  "lh-check-in-zero",
  "lh-inbox-zero",
  "lh-execution",
  "linkhub-strategy-coach",
];

await mkdir(legacyRoot, { recursive: true });
for (const skillName of skillNames) {
  const source = resolve(pluginRoot, "skills", skillName);
  const destination = resolve(legacyRoot, skillName);
  await rm(destination, { recursive: true, force: true });
  await cp(source, destination, { recursive: true });
}

console.log(`Synchronized ${skillNames.length} generated legacy skill copies.`);
