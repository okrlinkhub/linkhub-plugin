# LinkHub MCP — Reference strategy setup workflow

Workflow per **definizione strategica iniziale** (Objectives, Key Results, Rischi, Iniziative).
Per il reporting periodico usa `linkhub-report-coach`.

## Read (discovery)

| Tool | Args principali | Output utile |
|------|-----------------|--------------|
| `mcp_membershipProfile` | — | userId, company, permessi |
| `companies_list` | — | companyId |
| `teams_listMineByCompany` | companyId | team gestibili |
| `teams_listMembers` | teamId | assignee validi per iniziative |
| `objectives_byTeam` | teamId | objectives + KR annidati |
| `keyResults_byTeam` | teamId | slug, weight, indicatorDescription, indicatorId |
| `risks_byKeyResult` | keyResultId | rischi attivi sul KR corrente |
| `initiatives_byTeam` | teamId, limit | hygiene / anti-duplicati |
| `users_searchForMentions` | query | menzioni commenti assegnazione |
| `mcp_resolveIsoDate` | isoDate | timestamp + weekday per scadenze |

## Write (setup strategico)

| Tool | Quando |
|------|--------|
| `objectives_create` | Nuovo Objective qualitativo |
| `objectives_update` | Affina title/description |
| `objectives_remove` | Soft-delete (KR → orfani con snapshot) — **conferma utente** |
| `keyResults_create` | Nuovo KR sotto objective esistente |
| `keyResults_update` | Peso, indicatore, forecast/target, spostamento objective |
| `keyResults_remove` | Soft-delete KR — **conferma utente** |
| `risks_create` | 1–3 rischi per KR (`reportId` opzionale, omit in setup) |
| `risks_remove` | Rischio risolto/obsoleto — **conferma utente** |
| `initiatives_create` | Mitigazione rischio, scope ≤ ~30 giorni |
| `initiatives_update` | Modifica descrizione, assignee, priorità, riskId, checkInDays, URL esterno — **non** le Note |
| `initiatives_checkIn` | Check-in + prossima data + append note strutturato (`postponed`, `started`, `finish`); `progressNote` obbligatoria |
| `initiatives_finish` | Iniziativa completata + append note strutturato; `progressNote` obbligatoria |

## Write (solo se esiste già un report DRAFT)

| Tool | Nota |
|------|------|
| `keyResults_rebalanceWeightInDraftReport` | Solo con `reportId` DRAFT aperto |
| `reports_*`, `resultTracked_*`, `resultNext_*` | Usa `linkhub-report-coach` |

## Gap MCP — Indicatori

**Non esistono** tool `indicators_list` / `indicators_create` via MCP.

Per `keyResults_create` serve sempre `indicatorId`:
1. L'utente crea/seleziona l'indicatore in **LinkHub UI** (company scope).
2. Oppure riusa `indicatorId` da `keyResults_byTeam` (stesso team o altro team stessa company).

Formato indicatore atteso: descrizione = nome metrica + unità tra parentesi, coerente con regole AI Coach.

## Validazioni backend rilevanti

| Regola | Effetto |
|--------|---------|
| `validateTitle` / `validateDescription` | Objectives, rischi, iniziative |
| `validateWeight` | Peso KR 0–100 |
| `assertIndicatorAvailableForPositiveWeightKeyResult` | Stesso indicatore non duplicato con peso > 0 |
| `requirePrincipalTeamManageAccess` | Solo team gestibili dall'API key |
| `keyResults_update` cross-team | **Bloccato** — KR non cambia team |
| Soft-delete objective | KR orfani con `deletedObjectiveTitle` |
| Soft-delete KR | Rischi orfani con snapshot |

## Campi tipici copy-paste

### objectives_create
```json
{
  "teamId": "...",
  "title": "Eccellenza operativa nel customer care",
  "description": "..."
}
```

### keyResults_create
```json
{
  "objectiveId": "...",
  "indicatorId": "...",
  "weight": 40,
  "forecastValue": 90,
  "targetValue": 100
}
```

### risks_create (setup strategico, senza report)
```json
{
  "keyResultId": "...",
  "description": "Assenza di fonte dati consolidata per lo SLA ticket",
  "priority": "high"
}
```

### initiatives_create (orizzonte mensile)
```json
{
  "teamId": "...",
  "riskId": "...",
  "description": "Configurare export giornaliero SLA da Zendesk verso foglio condiviso",
  "assigneeId": "...",
  "checkInDays": 30,
  "priority": "high"
}
```

## Check-in e Note (iniziative esistenti)

In setup strategico **crei** iniziative; i check-in ricorrenti appartengono a `lh-check-in-zero` o al report coach.
Se l'utente completa o aggiorna un'iniziativa **durante** la sessione strategica:

| Tool | Quando |
|------|--------|
| `initiatives_checkIn` | Rimando (`postponed`), avvio (`started`) o chiusura (`finish`) con nota obbligatoria |
| `initiatives_finish` | Solo chiusura; equivalente a `checkInOutcome: "finish"` |

**Campi obbligatori:** `progressNote` non vuota; per `postponed`/`started` anche `customNextCheckInDateIso` (+ `mcp_resolveIsoDate`).

**Formato note append-only** (non usare `initiatives_update` sulle Note):

```
[GG/MM/YYYY] Spostato al GG/MM/YYYY
Rimandata per testo utente
```

```
[GG/MM/YYYY] Spostato al GG/MM/YYYY
Iniziato a testo utente
```

```
[GG/MM/YYYY] Completato con
testo utente
```

La riga `Spostato al ...` non compare con `finish`.

## Checklist pesi

Dopo ogni modifica pesi:
1. `keyResults_byTeam` → somma `weight` attivi = **100**
2. Se DRAFT report aperto e serve allineamento report → `keyResults_rebalanceWeightInDraftReport`
