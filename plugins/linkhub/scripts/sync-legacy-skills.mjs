import { cp, mkdir, readdir, rm, stat } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const pluginRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const repositoryRoot = resolve(pluginRoot, "../..");
const legacyRoot = resolve(repositoryRoot, ".claude/skills");
const skillsRoot = resolve(pluginRoot, "skills");
const skillNames = [];
for (const entry of await readdir(skillsRoot, { withFileTypes: true })) {
  if (!entry.isDirectory()) continue;
  try {
    if ((await stat(resolve(skillsRoot, entry.name, "SKILL.md"))).isFile()) {
      skillNames.push(entry.name);
    }
  } catch {
    // A directory without SKILL.md is not an installable skill.
  }
}
skillNames.sort();

await mkdir(legacyRoot, { recursive: true });
for (const skillName of skillNames) {
  const source = resolve(skillsRoot, skillName);
  const destination = resolve(legacyRoot, skillName);
  await rm(destination, { recursive: true, force: true });
  await cp(source, destination, { recursive: true });
}

console.log(`Synchronized ${skillNames.length} generated legacy skill copies.`);
