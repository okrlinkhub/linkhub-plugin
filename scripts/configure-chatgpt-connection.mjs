import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const rawId = process.argv[2];
if (!rawId || !/^(?:plugin_)?asdk_app_[a-f0-9]+$/i.test(rawId)) {
  throw new Error("Uso: node scripts/configure-chatgpt-connection.mjs <plugin_asdk_app... oppure asdk_app...>");
}

const appId = rawId.replace(/^plugin_/, "");
const repositoryRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const pluginRoot = join(repositoryRoot, "plugins", "linkhub");
const manifestPath = join(pluginRoot, ".codex-plugin", "plugin.json");

if (!existsSync(manifestPath)) {
  throw new Error("Esegui lo script dalla copia del repository linkhub-plugin");
}

const appManifest = {
  apps: {
    linkhub: {
      id: appId,
      required: true,
    },
  },
};
writeFileSync(join(pluginRoot, ".app.json"), `${JSON.stringify(appManifest, null, 2)}\n`);

const manifest = JSON.parse(readFileSync(manifestPath, "utf8"));
delete manifest.mcpServers;
manifest.apps = "./.app.json";
writeFileSync(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`);

console.log(`Connessione ChatGPT ${appId} configurata localmente per LinkHub`);
