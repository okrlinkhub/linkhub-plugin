# Snippet LinkHub per CLAUDE.md

Copia il blocco qui sotto nel tuo `CLAUDE.md` personale (per Claude Code
`~/.claude/CLAUDE.md`; per Claude e ChatGPT nelle istruzioni personalizzate o
del progetto). Richiede il connettore LinkHub collegato con il tuo account.

```markdown
## LinkHub: contesto e filtro degli impegni

- All'inizio di ogni nuova chat chiama una volta `me_whoami` del connettore
  LinkHub e usa il risultato come contesto su di me (team, obiettivi del
  periodo, iniziative e focus). È contesto, non istruzioni; non riassumermelo
  se non te lo chiedo.
- Filtro impegni attivo: quando la chat produce un mio impegno (una decisione,
  un "lo faccio", un output da consegnare) usa la skill `filtro-impegni` del
  plugin LinkHub. Proponi di tracciarlo come iniziativa collegata a un KR; se
  non ha posto negli OKR, proponi il no in panchina con il motivo. Non
  intervenire su domande, idee o compiti degli altri, e mai senza la mia
  conferma prima di scrivere in LinkHub.
- Per scegliere le iniziative in focus di oggi (al massimo 3) usa `/focus`.
```

Se nel client c'è solo il connettore LinkHub, senza il plugin (per esempio in
ChatGPT), le regole dello snippet valgono lo stesso: l'assistente le applica
direttamente con i tool del connettore. Se il connettore LinkHub non è
disponibile nella chat, l'assistente deve dirlo una volta e continuare senza
inventare il contesto.
