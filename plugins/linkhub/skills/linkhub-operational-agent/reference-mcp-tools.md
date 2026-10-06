# LinkHub MCP reference for operational agents

Leggi questa pagina quando devi costruire una chiamata. I nomi sotto sono
quelli pubblicati dal server MCP LinkHub; non inventare tool alternativi.

## Letture

| Tool | Uso |
| --- | --- |
| `mcp_membershipProfile` | Identità corrente, `userId`, `companyId` e membership |
| `mcp_resolveIsoDate` | Verifica `YYYY-MM-DD`, timestamp e giorno della settimana |
| `initiatives_listMinePending` | Inventario assegnato e, con `initiativeId`, `assignedContext` completo e limitato a quella iniziativa |
| `initiatives_byTeam` | Controlla iniziativa, duplicati e altre azioni sul team |
| `teams_listMineByCompany` | Richiede `companyId`; restituisce `{ teams, count }` dei tuoi team con `teamLeaderId`, fino a 200 |
| `keyResults_byTeam` | Legge KR soltanto nei team accessibili |
| `risks_byKeyResult` | Legge rischio e contesto del Key Result quando il KR è noto |
| `teams_listMembers` | Verifica che il bot sia un assignee valido nel team |
| `inbox_getConversation` | Legge l'intera conversazione prima di rispondere |
| `users_searchForMentions` | Cerca utenti company per nome o email senza indovinare |

`initiatives_listMinePending` accetta `companyId?`, `initiativeId?`, `teamId?`,
`overdueOnly?` e `limit?`; il default è 50 e il massimo è 100, senza cursore o
offset. Restituisce `{ initiatives, count, isLimited, hasOutsideTeamAssignments, assignedContext }`.
Con `initiativeId`, `assignedContext` include l'iniziativa completa (anche
FINISHED), il suo rischio, KR e teamLeaderId soltanto se ancora assegnata a te.
Non autorizza elenchi o modifiche generali sul team esterno.

Alle 09:00 usa una sola `{ companyId, limit: 100 }`. Meno di 100 righe con
`isLimited: false` significa inventario completo. Solo con esattamente 100,
usa `teams_listMineByCompany { companyId, limit: 200 }` e pending per ogni
team con `limit: 100`. Conserva le righe iniziali e deduplica per ID.
Mai `teams_listByCompany` nella Routine. Sono saturi: 200 team, 100 iniziative
per team, qualsiasi `isLimited: true`, una lettura fallita, oppure una
risposta company-wide piena con `hasOutsideTeamAssignments: true`, anche
se le assegnazioni esterne non compaiono nelle prime 100 righe. Processa il visibile e avvisa l'owner; non promettere copertura
completa. Se `isLimited: true` ma count è minore di 100, avvisa senza fan-out.

`initiatives_byTeam` richiede `teamId`; accetta `riskId?`, `includeFinished?`,
`cursor?` e `limit?` fino a 200. Restituisce
`{ initiatives, count, hasMore, nextCursor, truncated }`, con record completi
inclusi `createdBy` e `notes`. Il default esclude `FINISHED` e include sempre
solo record non soft-deleted; usa `includeFinished: true` esclusivamente quando
serve lo storico, per esempio per verificare un retry già concluso. Quando
passi `riskId`, la lettura usa 200 come limite predefinito e massimo; passalo
comunque insieme a `limit: 200` per rendere esplicita la richiesta. Il filtro
per rischio viene applicato prima della paginazione, così lo storico non
correlato del team non rende incompleto il contesto. Non usarlo come fonte della
data di check-in.

Quando `hasMore` è vero, ripeti la chiamata con gli stessi filtri e
`nextCursor`, accumulando `initiatives` fino a `hasMore: false`. `truncated`
riflette `hasMore`; `count` è il numero di righe della singola pagina, non il
totale. Se `nextCursor` manca, si ripete o una pagina fallisce, considera
l'inventario incompleto e non creare né scegliere follow-up.

Per il rischio e KR dell'iniziativa usa `assignedContext` con il suo
`initiativeId`. Fuori dai tuoi team non chiamare `keyResults_byTeam`,
`risks_byKeyResult` o `initiatives_byTeam`; puoi fare check-in/finish della
propria iniziativa, ma un follow-up richiede membership valida al team.

## Messaggi

`inbox_reply` richiede `companyId`, `conversationId` e `mentionIds`; accetta
`text` e fino a 5 `attachments` HTTPS da massimo 10 MB ciascuno. Specifica
almeno il testo o un allegato.

`inbox_createComment` richiede:

```json
{
  "receiverId": "user-id",
  "text": "messaggio",
  "initiativeId": "initiative-id",
  "mentionIds": ["user-id"],
  "attachments": []
}
```

Prima di popolare `attachments`, chiedi all'utente un URL HTTPS pubblico reale
e il relativo nome file; non inventare URL o identificativi di esempio.

Può collegare in alternativa `indicatorId`, `teamId`, `riskId` o
`personalInitiativeId`. Usa una sola entità coerente con la conversazione.
Gli URL firmati sono accettati solo se HTTPS e pubblici; l'intera operazione
fallisce se anche un solo allegato non supera la validazione.

`inbox_markConversationAsRead` richiede `companyId` e `conversationId`.

## Check-in append-only

Completamento:

```json
{
  "initiativeId": "initiative-id",
  "checkInOutcome": "finish",
  "progressNote": "Cosa è stato completato e con quale esito osservato."
}
```

Blocco/rimando:

```json
{
  "initiativeId": "initiative-id",
  "customNextCheckInDateIso": "YYYY-MM-DD",
  "checkInOutcome": "postponed",
  "progressNote": "Tentativo, blocco, dipendenza e prossimo passo."
}
```

Non usare `initiatives_update` per le Note. `initiatives_finish` è disponibile
come alternativa al check-in `finish`, ma richiede comunque `progressNote`.

## Follow-up sullo stesso rischio

Rileggi prima `initiatives_byTeam` con `teamId`, lo stesso `riskId` e
`limit: 200`, usando il default attivo, e completa tutte le pagine. Normalizza la descrizione
solo per case e spazi. Con zero corrispondenze puoi proseguire; con una riusa
quell'ID; con due o più non riusare e non creare, segnala l'ambiguità e passa al
percorso bloccato. Se la paginazione non si completa, interrompi la
riconciliazione. Subito
prima di una nuova creazione chiama `teams_listMembers` e verifica che
l'identità corrente sia ancora assegnabile. Poi usa `initiatives_create` con:

```json
{
  "description": "Azione successiva autosufficiente e verificabile",
  "teamId": "team-id",
  "riskId": "lo-stesso-risk-id",
  "assigneeId": "mcp-membership-profile-user-id",
  "checkInDays": 3,
  "priority": "high"
}
```

`riskId` è obbligatorio. `checkInDays` deve riflettere il prossimo evento
osservabile; non usare automaticamente 3 giorni. `priority` può essere
`lowest`, `low`, `medium`, `high` o `highest` e va omessa se non è supportata
dal contesto.

Dopo create rileggi tutte le pagine attive di `initiatives_byTeam` con lo stesso
`teamId` e `riskId` e conserva l'ID riconciliato. Per un
follow-up creato o riusato, chiudi la sorgente con `initiatives_checkIn` e una
nota deterministica che includa quell'ID. Prima di ogni retry rileggi stato e
`notes` in `assignedContext` tramite `initiatives_listMinePending { initiativeId }`: se la sorgente è già `FINISHED` con lo
stesso ID e la stessa nota, non
ripetere il check-in; se l'evidenza è diversa, fermati e segnala l'ambiguità.
Non ripetere create dopo una risposta ambigua senza avere prima riconciliato.
Se finish continua a fallire, risolvi una nuova data con `mcp_resolveIsoDate` e
tenta il check-in `postponed` completo mostrato sopra; se anche questo fallisce,
avvisa il creatore e non dichiarare un esito non persistito.

## Mutazioni che richiedono autorità distinta

Non usare `initiatives_update`, `initiatives_remove`, `risks_update` o
`risks_remove` soltanto perché il bot sta eseguendo l'iniziativa. Un cambio di
testo concordato può usare `initiatives_update`; rimozioni o risoluzione del
rischio richiedono una conferma esplicita e separata.
