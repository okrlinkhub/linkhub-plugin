import { cp, mkdir, mkdtemp, readdir, rm, stat } from "node:fs/promises";
import { dirname, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";
import { tmpdir } from "node:os";
import { createDeterministicZip } from "../../../scripts/lib/deterministic-zip.mjs";

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

// A scoped refresh also regenerates the legacy ZIP with its original skill folder.
const args = process.argv.slice(2);
if (args.length && (args.length !== 2 || args[0] !== "--skill" || !skillNames.includes(args[1]))) {
  throw new Error("Uso: node sync-legacy-skills.mjs [--skill <nome canonico>]");
}
const selectedSkills = args.length ? [args[1]] : skillNames;

await mkdir(legacyRoot, { recursive: true });
for (const skillName of selectedSkills) {
  const source = resolve(skillsRoot, skillName);
  const destination = resolve(legacyRoot, skillName);
  await rm(destination, { recursive: true, force: true });
  await cp(source, destination, {
    recursive: true,
    filter: (path) =>
      !path.split(sep).some((part) => part === "__pycache__" || part.endsWith(".pyc")),
  });
  if (args.length) {
    const archiveRoot = await mkdtemp(resolve(tmpdir(), "linkhub-legacy-skill-"));
    try {
      await cp(destination, resolve(archiveRoot, skillName), { recursive: true });
      createDeterministicZip(archiveRoot, resolve(legacyRoot, `${skillName}.zip`));
    } finally {
      await rm(archiveRoot, { recursive: true, force: true });
    }
  }
}

console.log(`Synchronized ${selectedSkills.length} generated legacy skill copies.`);
