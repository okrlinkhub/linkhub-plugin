# Snippet LinkHub per CLAUDE.md

Con il connettore LinkHub collegato il server invia già queste istruzioni a
ogni chat (campo `instructions` di MCP), senza configurazione. Copia il blocco
qui sotto solo se il tuo client le ignora: per Claude Code in
`~/.claude/CLAUDE.md`, per Claude nelle preferenze personali, per ChatGPT nelle
istruzioni personalizzate. È lo stesso testo di «Copia per il tuo LLM» nella
Home di LinkHub.

```markdown
## LinkHub

Nelle conversazioni di lavoro (priorità, decisioni, impegni, pianificazione, risposte a colleghi o clienti), prima di rispondere chiama il tool LinkHub `me_whoami` e usa obiettivi, focus e iniziative per dare priorità e collegare gli impegni ai KR. Se nasce un impegno, proponi di tracciarlo come iniziativa o di metterlo in panchina come no (skill `filtro-impegni`); per il focus del giorno usa la skill `focus`. Senza plugin usa i tool LinkHub. Non serve nelle chat non di lavoro.
```

Se nel client c'è solo il connettore LinkHub, senza il plugin (per esempio in
ChatGPT), l'assistente applica le stesse regole direttamente con i tool del
connettore. Se il connettore non è disponibile nella chat, l'assistente lo dice
una volta e continua senza inventare il contesto. Prima di scrivere in LinkHub
chiede sempre conferma.
