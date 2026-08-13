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
| `keyResults_byTeam` | teamId | slug, weight, forecast |
| `reports_getEvaluateContext` | reportId, keyResultId | indicator, tracked/next esistenti |
| `reports_getAnalyzeContext` | reportId, keyResultId | risks[], initiatives[] |
| `risks_byKeyResult` | keyResultId | solo se serve lista estesa |
| `initiatives_byTeam` | teamId, limit | hygiene batch |
| `initiatives_listMinePending` | companyId | check-in da fare |
| `teams_listMembers` | teamId | assignee validi |
| `users_searchForMentions` | query | menzioni commenti |
| `mcp_resolveIsoDate` | isoDate | timestamp + weekday |

## Read (indicator evidence)

| Tool | Args principali | Output utile |
|------|-----------------|--------------|
| `indicators_listExplainable` | companyId?, query?, limit? | indicatorId, periodicità, ownership e binding |
| `indicators_getExplanation` | indicatorId | definizione, caveat, chiavi approvate, lineage e periodo |
| `indicators_queryEvidence` | indicatorId, request | envelope con operazione, intervallo, righe, conteggio e truncation |
| `indicators_searchCatalog` | indicatorId, query?, limit? | metriche autorizzate con namespace e metricKey esatti |
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
| `resultNext_skipWithDefaults` | Next veloce (default) |
| `resultNext_upsert` | Next custom |
| `reports_updateReporterNotes` | Salva nota senza submit |
| `reports_submit` | DRAFT → IN_REVIEW |

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

## Campi copy-paste da evaluate context

Per upsert/markUnmeasurable servono sempre:
- `indicatorDescription`, `indicatorId`, `indicatorSymbol`
- `objectiveTitle`, `objectiveDescription`
- `intervallSource`, `resultType` (se upsert/unmeasurable)

Prendili da `reports_getEvaluateContext` + `objectives_byTeam`.
