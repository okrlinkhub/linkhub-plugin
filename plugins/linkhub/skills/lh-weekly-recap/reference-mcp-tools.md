# Strumenti MCP del weeklyRecap

Nomi tecnici solo per le chiamate interne: non mostrarli all'utente. Tutti gli
strumenti valgono per la company del collegamento e solo con l'accesso
personale dell'utente: gli agenti operativi vengono rifiutati.

## Letture

- `mcp_membershipProfile` — nome dell'utente e company del collegamento.
- `me_weeklyRecap { weekOfIso?: "YYYY-MM-DD", locale?: "it" | "en" }` — recap
  privato della settimana (lunedì–domenica nel fuso dell'utente, pronta il
  venerdì mattina; ultime 26 settimane). Restituisce `week { startIso, endIso,
  previousStartIso, nextStartIso }`, `closedInitiatives` (iniziative chiuse
  con team e KR), `keyResultEffects` (iniziative chiuse per KR, valore attuale
  e obiettivo), `declined` e `declinedCount` (i no della settimana con il
  motivo), `benchCleanup { promote, remove, foundPlace }`, `shareText` (testo da
  inoltrare, solo il numero dei no) e `partial` (elenchi forse incompleti).
  Non invia nulla.
- `bench_list { statuses?, dateIso?, limit? }` — panchina privata, aperti e no
  per impostazione predefinita; ogni elemento ha KR, team, no e iniziativa
  promossa. Serve per i dati completi prima di promuovere o aggiornare.
- `risks_byKeyResult { keyResultId }` — rischi attivi del KR e il suo team
  (`keyResult.teamId`): il rischio di una promozione deve essere dello stesso team.
- `teams_listMineByCompany`, `keyResults_byTeam` — team e KR per collegare un
  elemento o scegliere un KR in un altro team.

## Modifiche (sempre dopo un sì sulla proposta esatta)

- `bench_promote { benchItemId, keyResultId, riskId?, riskDescription?,
  checkInDays, teamId?, description?, assigneeId?, priority?, externalUrl? }` —
  KR obbligatorio, team del KR. Senza `riskId` crea un rischio nuovo sul KR:
  passa in `riskDescription` il testo esatto confermato (senza, usa titolo e
  nota dell'elemento); mai entrambi. Crea
  l'iniziativa come `initiatives_create`, segna l'elemento come promosso e
  restituisce `riskCreated`.
- `bench_update { benchItemId, title?, note?, dateIso?, keyResultId?, teamId?,
  status?, declinedReason?, declinedOnIso? }` — aggiorna un elemento aperto o un
  no; `status: "OPEN"` riapre un no, `status: "DECLINED"` richiede il motivo.
  Gli elementi promossi non si modificano.
- `bench_remove { benchItemId }` — elimina un elemento; un'iniziativa già
  promossa non cambia.
