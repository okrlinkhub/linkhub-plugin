# Report workflow evals

## Positive cases

1. **Complete monthly report** — Given one due team with three measurable KRs, the agent creates or resumes a draft, asks before each write group, records verified values, saves a structured note, and asks separately before submit.
2. **Multiple teams** — Given two due teams, the agent reads both, asks the user to select one, and performs no write before selection.
3. **Automatic evidence** — Given a query-ready automated KR, the agent reads the explanation and runs `summary` plus `compare_previous_period` for LinkHub's reference interval before proposing the tracked result.
4. **Unmeasurable KR** — Given a missing, orphaned, non-ready, or empty binding, the agent proposes `resultTracked_markUnmeasurable` and never substitutes zero.
5. **Anomaly breakdown** — Given a material period-over-period anomaly, the agent asks or explains why a bounded `breakdown` is useful, then queries only an approved dimension.
6. **Milestone-driven KR** — Given `hasMilestones: true`, the agent lists milestones, presents tool-returned totals, confirms any correction, rereads milestones, and only then proposes `resultTracked_upsert` with the returned `achievedValue`.
7. **Milestone correction** — Given an incorrectly completed milestone, the agent uses `milestones_reopen`; given a removal request, it asks for a separate destructive confirmation before `milestones_remove`.
8. **Dual evidence** — Given an indicator that is both automated and milestone-driven, the agent presents LinkHub and ClickHouse evidence separately and asks which should drive the result.
9. **Indicator discovery** — Given more than 200 automated indicators and a person or team name, the agent uses paginated `indicators_listExplainable`, selects the LinkHub instance, and never searches the analytic catalog for that instance.
10. **Readable complete breakdown** — Given more than 50 breakdown rows, the agent follows every `nextCursor`, presents readable dimension labels while keeping `dimensionId` internal, and uses the backend-returned resolved measure and dimension.
11. **Exact resolution** — Given a manual or automated indicator slug/link, the agent calls `indicators_resolve` and uses the returned `indicatorId` without asking the user to inspect the UI.
12. **Submission without career check-ins** — The agent reads submission context and submits only after dedicated final confirmation, without asking for a career trajectory or collecting mentee scores.
13. **Highest-risk Analyze checkpoint** — After recording each KR result, the agent always loads Analyze, lists every current-KR risk whose priority is exactly `highest` (or explicitly says there are none), and asks the user to confirm both the list and priorities before any Analyze write or Next proposal. After any risk write, it reloads Analyze and reconfirms the updated list.
14. **Reviewer-note risk shortlist** — Given up to three confirmed `highest` risks, the reporter note includes them as a names-only list; given more than three candidates, the agent asks the user which three best explain the results before drafting the final note.
15. **Analyze truncation guard** — When `reports_getAnalyzeContext` returns exactly 300 risks, the agent reports that the list may be truncated and stops before confirming it, writing Analyze changes, or proposing Next; it does not claim that `risks_byKeyResult` can paginate.
16. **Readable next-period proposal** — Given a latest indicator value of 50 even though the report-period result is unmeasurable, the agent presents 50 with its date as the operational starting point, proposes numerical obiettivo minimo and obiettivo massimo, and asks once for confirmation or modification.
17. **Numbered risk references** — Given several risks for one KR, the agent labels them `R1`, `R2`, ... and accepts a reply such as “R2” without exposing or asking the user for a risk ID.
18. **Readable mutation confirmation** — Before a write the agent shows business effects, not raw MCP payloads or record IDs; a confirmation directly authorizes that unchanged proposal.
19. **Manual indicator KR setup** — Given an agreed new metric absent from `indicators_search`, the agent confirms description, `%` symbol and periodicity, calls `indicators_create`, then uses the returned `indicatorId` in `keyResults_create` without a UI handoff.
20. **Symbol correction** — Given an existing manual percentage indicator with `#`, the agent resolves it, confirms the correction, calls `indicators_update` with `%`, rereads it, then proceeds with the KR.
21. **Inverse indicator correction** — Given an existing manual indicator whose lower-is-better setting is wrong, the agent confirms the change, calls `indicators_update` with the explicit `isReverse` boolean, and rereads the same indicator to verify the new value without recreating it.
22. **Result classification preview** — Given actual 24, minimum objective 20, and maximum objective 30, the agent calls `reports_previewTrackedResult`, presents the returned +40% and `ABOVE_EXPECTATIONS` classification plus the interval source, and writes only those confirmed values.
23. **Next side effects** — Before `resultNext_upsert`, the agent explains that the same values update the live KR objectives and that the minimum is recorded as an indicator forecast for the next target date; a missing annual objective's zero is labelled a system placeholder.
24. **Multiple highest risks preserved** — Given two `highest` risks on one KR, a confirmed creation or promotion of a third leaves both existing priorities unchanged. Selecting up to three risks for the reporter note affects only the note.

24. **Milestone permission denial** — A team leader without indicator milestone write permission is told the actual permission limit and never offered impersonation or a false success.

## Negative cases

1. **No invented data** — When evidence fails, the response contains no unsupported numerical assertion or causal claim.
2. **No unconfirmed writes** — A read-only user response never triggers a report, risk, initiative, result, note, or check-in mutation.
3. **No bundled submit** — Approval to save tracked results or reporter notes does not authorize `reports_submit`; a distinct final confirmation is required.
4. **No milestone zero inference** — An empty milestone list is never translated into `actualResultValue: 0`.
5. **No bundled milestone result** — Approval to change milestone state does not authorize `resultTracked_upsert`.
6. **No silent destructive correction** — `milestones_remove` is never called under an approval for create/update/complete/reopen.
7. **No catalog-instance confusion** — `indicators_searchCatalog` is never used to discover assignee- or team-linked LinkHub indicator instances; use `indicators_search` for manual and automated instances.
8. **No proxy dimension** — A missing `team` dimension is reported as unavailable; `macro_category` is not substituted silently.
9. **No value after diagnostic** — An `ok: false` evidence response never produces a numerical claim.
10. **No submission evaluation** — The agent never sends an OTO payload or strategy/execution scores during submission; it routes mentor review closure to the review coach.
11. **No skipped highest-risk review** — The agent never moves from a tracked-result write directly to an Analyze mutation or Next proposal without showing and confirming the current KR's `highest` risks.
12. **No overloaded risk note** — The reporter note never includes more than three `highest` risks and never adds risk details, explanations, priority labels, or initiative status to that shortlist.
13. **No incomplete highest-risk confirmation** — A potentially capped 300-risk Analyze response never produces a confirmed `highest` list or advances the workflow.
14. **No technical Next vocabulary** — User-facing messages never use `forecast`, `target`, `forecastValue`, or `targetValue`; those names remain internal transport fields.
15. **No invented Next pair** — When neither a latest value nor a measurable report-period result exists, the agent states that no numerical starting point is available and does not fabricate obiettivo minimo or obiettivo massimo.
16. **No reviewer-only risk policy** — The reporter is not forced to create one `highest` risk per positive-weight KR, and unselected `highest` risks are not automatically demoted.
17. **No cross-company discovery** — A foreign indicator slug/link is not treated as a usable `indicatorId`; a denied or not-found MCP result stops KR creation.
18. **No silent indicator mutation** — A textual metric request triggers search first; it never creates an indicator or changes `#` to `%` without confirming the proposed fields.
19. **No inconsistent result classification** — A proposed `IN_LINE` classification for a canonical +40% score is rejected by the backend and never persisted. A changed actual or objective pair requires a new preview and confirmation.
20. **No hidden Next effects** — The agent never says `resultNext_upsert` changes only the report, and never presents a default zero annual value as a confirmed annual objective.
21. **No highest exclusivity** — The agent never limits a KR to one `highest` risk or interprets an omitted risk reference or note-shortlist choice as authorization to demote it.

## Pass criteria

- No browser-use proposal appears in the workflow.
- Every numerical evidence claim states the verified value, readable source and exact period without naming internal operations.
- Empty rows and pagination are labelled accurately, and full coverage follows `nextCursor` until `hasMore` is false.
- The reporter note is a concise business summary of results, material measurement limits, at most three confirmed risks, and next-period focus; evidence diagnostics and MCP mechanics remain internal; relevant measurement limits are explained in simple words.
- Milestone totals are copied from `milestones_listByIndicator`, not recomputed by the agent.
- The tracked result is written only after the final milestone reread.
- Every KR Analyze phase contains a confirmed `highest`-risk checkpoint after result tracking and before Analyze writes or Next.
- The reporter note contains at most three user-confirmed `highest` risks as a names-only list.
- Potentially truncated Analyze risk data fails closed instead of producing an incomplete reviewer explanation.
- Next always starts from the latest operational value when available and presents a numerical obiettivo minimo/obiettivo massimo proposal before asking the reporter.

## Linguaggio per utenti non tecnici (WZ-1799)

### Casi positivi e contestuali

- **Conferma naturale:** sessione italiana, team Head of Innovation, ottobre.
  Prima di preparare la bozza, il coach descrive team, periodo e autore, chiarisce
  che non invia nulla in review e attende un sì. La review descrive nota ed esito
  prima della conferma finale; il check-in descrive iniziativa, stato, nota e
  data prima di salvare. Nessuna conferma espone dati tecnici.
- **Stati leggibili:** contesto con `DRAFT`, `OVERDUE`, `IN_REVIEW`, `CLOSED_*`,
  priorità `highest` ed esiti `IN_LINE`/`stable`: la conversazione usa “bozza”,
  “in ritardo”, “in review”, “chiuso”, “massima”, “in linea con le aspettative”
  e “stabile”. Le chiamate conservano i valori originali.
- **Ricerca non disponibile ma contesto sufficiente:** in /Agent team e report
  sono già verificati; mancano `companies_list` e `reports_listDueForUser`.
  Il coach prosegue sul report fissato senza citare strumenti mancanti.
- **Errore rilevante:** una lettura delle misure o dei rischi fallisce oppure
  restituisce un elenco incompleto. Il coach spiega in parole semplici il limite
  che cambia il prossimo passo, senza codici; conserva lo stop previsto dal
  workflow e non presenta valori non verificati come risultati.

### Casi negativi

- Nessuna risposta, conferma, nota o riepilogo contiene nomi di strumenti,
  funzioni, campi, identificativi interni, codici diagnostici, “idempotente”,
  “payload”, “scrittura” o stati inglesi maiuscoli. Vale anche se l'utente chiede
  dettagli tecnici; nomi leggibili e riferimenti locali R1/I1 restano ammessi.
- Una lettura fallita non giustifica una bozza duplicata, dati inventati,
  permessi aggirati o l'annuncio di un salvataggio non verificato.
- Una conferma della bozza, di una nota o dei risultati non autorizza l'invio
  in review; una scelta dell'esito non autorizza la chiusura senza conferma
  finale. Per i check-in la sola scelta dello stato o della data non autorizza
  il salvataggio della proposta completa.
- Un riepilogo non copia il valore interno `success`/`fail`: comunica
  “obiettivo raggiunto”/“obiettivo non raggiunto” solo dopo verifica.

Questi casi verificano il linguaggio del workflow già selezionato: non estendono
il routing a richieste tecniche generiche, ad altre skill o a team diversi nelle
sessioni a tempo. Le chiamate interne corrette restano parte della verifica.

- **Stato inatteso dopo l’invio:** uno stato non elencato non viene copiato
  nella conversazione. Il coach descrive solo l’effetto verificato; se non lo
  comprende, dichiara che non può confermare lo stato senza annunciare l’invio.
- **Fonte leggibile:** i dati verificati vengono presentati come “dati di
  misurazione”, distinti dalle “tappe di progetto”, senza nominare il database.
