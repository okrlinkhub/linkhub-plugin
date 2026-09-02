# LinkHub MCP — Reference report workflow

## Read (discovery)

| Tool | Args principali | Output utile |
|------|-----------------|--------------|
| `mcp_membershipProfile` | — | userId, company, permessi |
| `companies_list` | — | companyId |
| `reports_listDueForUser` | companyId? | report DRAFT / scaduti |
| `teams_listMineByCompany` | companyId | team dove sono leader |
| `reports_getWorkflowProgress` | reportId | KR status, next step, submit |
| `objectives_byTeam` | teamId | KR annidati + objective |
| `keyResults_byTeam` | teamId | slug, peso e valore tecnico usato internamente per l'obiettivo minimo |
| `reports_getEvaluateContext` | reportId, keyResultId | indicator, ultimo valore operativo con data, tracked/next esistenti |
| `reports_getAnalyzeContext` | reportId, keyResultId | risks[], initiatives[] |
| `risks_byKeyResult` | keyResultId | solo se serve lista estesa |
| `initiatives_byTeam` | teamId, riskId?, includeFinished?, cursor?, limit? | active hygiene page in `initiatives`, with `hasMore` and `nextCursor` |
| `initiatives_listMinePending` | companyId | check-in da fare |
| `teams_listMembers` | teamId | assignee validi |
| `users_searchForMentions` | query | menzioni commenti |
| `mcp_resolveIsoDate` | isoDate | timestamp + weekday |
| `milestones_listByIndicator` | indicatorId | milestone, stato, peso, date e totali verificati |

`initiatives_byTeam` excludes `FINISHED` by default and always excludes
soft-deleted records. Its envelope is
`{ initiatives, count, hasMore, nextCursor, truncated }`; `count` is the page
size, not a total, and `truncated` mirrors `hasMore`. The default limit is 100
(200 with `riskId`), maximum 200. Keep all filters unchanged when following
`nextCursor`; do not treat a failed or incomplete pagination as a complete
hygiene snapshot.

## Read (indicator evidence)

| Tool | Args principali | Output utile |
|------|-----------------|--------------|
| `indicators_listExplainable` | companyId?, query?, teamId?, usage?, assigneeId?, cursor?, limit? (max 50) | istanze LinkHub con slug, assignee, utilizzi team e paginazione |
| `indicators_resolve` | reference, companyId? | risoluzione esatta di slug o indicatorId |
| `indicators_getExplanation` | indicatorId | definizione, default, caveat, chiavi approvate, label, lineage e periodo |
| `indicators_queryEvidence` | indicatorId, request (`cursor?`, `limit?` max 50) | misura/dimensione risolte, righe tipizzate, diagnostica e paginazione |
| `indicators_searchCatalog` | indicatorId, query?, cursor?, limit? (max 50) | metriche analitiche autorizzate; non cerca istanze LinkHub |
| `indicators_queryCatalogEvidence` | indicatorId, metric, request | evidence envelope per la metrica catalogo verificata |

## Write (workflow)

| Tool | Quando |
|------|--------|
| `reports_createDraft` | Nessun DRAFT per periodo corrente (`report: null` in listDue) |
| `objectives_create` / `objectives_update` / `objectives_remove` | Setup strategico team (vedi `linkhub-strategy-coach`) |
| `keyResults_create` / `keyResults_update` / `keyResults_remove` | Setup strategico team (vedi `linkhub-strategy-coach`) |
| `keyResults_rebalanceWeightInDraftReport` | Cambio peso KR in DRAFT |
| `resultTracked_upsert` | Evaluate con valore |
| `resultTracked_markUnmeasurable` | Non so misurarlo |
| `resultTracked_markCompleted` | Objective completato (weight→0) |
| `risks_create` | Nuovo rischio in analyze / setup |
| `risks_update` | Modifica descrizione, priorità, KPI trigger |
| `risks_remove` | Rischio risolto (soft-delete) |
| `initiatives_create` | Nuova iniziativa |
| `initiatives_update` | Modifica descrizione, assignee, priorità, riskId, checkInDays, URL esterno |
| `initiatives_remove` | Soft-delete (errore / non più rilevante) |
| `initiatives_checkIn` | Check-in + prossima data + append note strutturato (`postponed`, `started`, `finish`); `progressNote` obbligatoria |
| `initiatives_finish` | Iniziativa completata + append note strutturato; `progressNote` obbligatoria |
| `resultNext_skipWithDefaults` | Conferma i default già mostrati come obiettivo minimo e obiettivo massimo |
| `resultNext_upsert` | Salva obiettivo minimo e obiettivo massimo personalizzati tramite i campi tecnici interni |
| `reports_updateReporterNotes` | Salva nota senza submit |
| `reports_getSubmitContext` | Elenca i candidati OTO leggibili e i valori ammessi prima del submit |
| `reports_submit` | DRAFT → IN_REVIEW; `otoCheckins?: [{ menteeId, answer: "stable" | "growing" | "declining" }]` |

## Write (milestone)

| Tool | Quando |
|------|--------|
| `milestones_create` | Crea una milestone con peso `%` e scadenza ISO opzionale |
| `milestones_update` | Modifica descrizione, peso o scadenza (`null` la rimuove) |
| `milestones_complete` | Completa con `achievedAtIso` esplicita |
| `milestones_reopen` | Corregge un completamento errato |
| `milestones_remove` | Soft-delete distruttivo, con conferma separata |

## Inbox (opzionale)

| Tool | Uso |
|------|-----|
| `inbox_summary` | Stato inbox |
| `inbox_listConversations` | Thread |
| `inbox_createComment` | Commento su entità |
| `inbox_reply` | Risposta thread |

## Validazioni submit (backend)

- Report status = DRAFT
- Nessun KR orfano
- Ogni tracked ha resultNext (`assertReportHasRequiredResultNext`)
- Pesi team = 100% (UI; verificare lato coach)
- Somma `value` delle milestone attive ≤ 100%
- Scrittura milestone consentita solo ad assignee indicatore o admin company
- `resultTracked_upsert` cattura lo snapshot milestone: eseguirlo dopo l'ultima rilettura

## Campi copy-paste da evaluate context

Per upsert/markUnmeasurable servono sempre:
- `indicatorDescription`, `indicatorId`, `indicatorSymbol`
- `objectiveTitle`, `objectiveDescription`
- `intervallSource`, `resultType` (se upsert/unmeasurable)

Prendili da `reports_getEvaluateContext` + `objectives_byTeam`.

## Linguaggio e conferme

- Verso l'utente usare sempre **obiettivo minimo** e **obiettivo massimo**;
  `forecast*` e `target*` sono esclusivamente nomi di trasporto interni.
- Mostrare valore operativo corrente, data e una proposta numerica prima di
  chiedere conferma del Next.
- Mostrare effetti leggibili delle mutation; non mostrare ID o payload MCP salvo
  richiesta esplicita.
- Numerare localmente i rischi di ogni KR come `R1`, `R2`, ... e mantenere la
  mappatura interna fino alla fine di quel KR.
