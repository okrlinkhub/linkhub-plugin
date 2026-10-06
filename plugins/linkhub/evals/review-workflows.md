# Review workflow evals

## Positive cases

1. **Cluster leader discovery** — The agent calls `mcp_membershipProfile` and `reviews_listMyClusterTargets`, identifies the returned `clusterLeaderTeam`, and offers only teams and people in that cluster, including a team where the reviewer has no ordinary membership.
2. **Non-cluster-leader fallback** — Given `status: not_cluster_leader`, the agent explicitly says that no own cluster can be resolved and does not substitute membership teams; it proceeds only if the user supplied an exact report that passes the direct authorization fallback.
3. **Notes before questions** — Given an IN_REVIEW report, the agent reads `reviews_getContext`, summarizes reporter and indicator notes, then asks one weight question.
4. **Auto-submitted report** — The agent labels the system-generated note as non-human and does not infer the reporter's opinion.
5. **Atomic next-period weight interview** — The agent treats reported weights as the starting allocation, asks what behavior and capacity priorities should change before the next report, then proposes all tracked results in one 100%, five-point allocation with forward-looking rationales.
6. **Post-period initiative** — An initiative finished after `trackingDate` is labelled follow-up, not evidence of in-period execution.
7. **Zero weight** — The agent explains removal from Next, includes the zero row in the complete allocation, and does not request Next validation for it.
8. **Next validation** — For every positive KR, the agent distinguishes the reviewed-period measurement from the latest available indicator value, uses that latest value as the operational baseline even when the period is unmeasured, then shows the reporter's and its own proposed `obiettivo minimo` and `obiettivo massimo` before asking for one confirmation; it preserves reported values and calls only `reviews_updateNextResult` with both reviewed values.
9. **Dedicated closure** — The agent rereads `reviews_getCloseContext`, shows recommendation, period evidence, both mandatory star scores and optional notes when the reviewer mentors the leader, and all user-visible effects, then asks separately for closure without exposing raw IDs.
10. **Empty report** — The agent permits only a separately acknowledged `BELOW_EXPECTATIONS` closure.
11. **Ownership before priority** — Before allocating the next period, the agent asks whether each KR still belongs to the team; transferred work is proposed at zero for that reason, not because the closed-period result was weak.
12. **Stable risk references** — The agent calls `reviews_getAnalyzeContext` once, shows `highest` risks as `R1`, `R2`, ... and correctly understands a reviewer reply such as “R2 non è più rilevante”.
13. **Minimum highest coverage per positive KR** — When an explicitly requested removal or demotion would leave a positive-weight KR uncovered, the agent blocks advancement and asks which existing risk to promote or what new highest risk to create for that KR. Merely naming other risks leaves omitted risks unchanged.
14. **Risk-linked initiative defaults** — A reviewer-created initiative is explicitly tied to one active numbered risk, explains the mitigation relationship, and is proposed for the returned team leader with a 7-day check-in; the agent asks only whether to include the exact standard assignment message before presenting the confirmed payload.
15. **Explicit priority changes only** — When the reviewer explicitly requests lowering R2 while keeping R1 at `highest`, the agent checks minimum coverage and shows only that requested change in the atomic proposal; one confirmation directly authorizes the call without a second raw-payload prompt.
16. **Automated indicator evidence** — Before proposing Next values for an automated positive-weight KR, the agent reads its approved explanation and runs the reference-period `summary` plus `compare_previous_period`; it reports formula, material exclusions, evidence status, and only then makes a numerical proposal.
17. **Sandbox evidence boundary** — A review running on an isolated deployment evaluates the indicator through that deployment and never reads a production-connected LinkHub MCP.
18. **Reporter-focused closing note** — The proposed reviewer note briefly covers period outcome, next-period changes, confirmed principal risks, and only useful reviewer-added initiatives; it omits assignment mechanics, check-in cadence, message-delivery choices, tool errors, and internal identifiers.
19. **Current values in Next proposal** — Each Next proposal places the reviewed-period measurement, dated current operational value, reporter proposal, and reviewer proposal together; when no current value exists, it says so explicitly before asking for approval.
20. **Analyze decision before Next** — After weights, the agent shows current risks and initiatives for every positive-weight KR and recommends concrete changes or no change; it resolves the reviewer's decision and approved writes before discussing future Next values.
21. **Localized outcome** — For an Italian review, the closure preview says `sopra le aspettative`, `in linea con le aspettative`, or `sotto le aspettative`; the corresponding enum remains internal to the tool payload.
22. **Post-preview closure approval** — A reviewer says “procediamo, sarà in linea e stabile”; the agent drafts the exact note and closure preview, asks a new dedicated confirmation, and waits for the next affirmative reply before calling `reviews_close`.
23. **Neutral interval** — Given a positive-weight increasing KR that is not yet measurable in the next period and a reporter proposal of `0 / 0`, the agent explains that equal goals have no success interval, proposes obiettivo minimo `0` and obiettivo massimo `10`, and waits for confirmation before writing.
24. **New risks on covered KRs** — Given R1 and R11 already at `highest` on Sviluppi Chiave and SLA, and two agreed new risks, the agent proposes both creations at `highest`, asks only for the creation confirmation, and calls `risks_create` with that priority. R1 and R11 remain unchanged.
25. **Several highest risks on one KR** — Given three active `highest` risks on a positive-weight KR, the agent lists all three and accepts complete coverage without selecting a single winner.
26. **Creation fills missing coverage** — Given a KR without any `highest` risk, the agent identifies the gap and proposes a new risk at `highest` without asking for priority; after confirmed creation it rereads Analyze and verifies coverage before Next.

24. **Milestone replacement** — During Review, replace “Restore dei workflow impattati” with “Metriche LinkHub in catalogo” due 31 October of the confirmed year: read, show the replacement and preserved weight, confirm, call `milestones_update`, and reread before continuing Next.
25. **Milestone lifecycle** — Create, change description/deadline/weight, complete with an explicit date, and reopen using the corresponding MCP tools only after confirmation; removal of an ingestion milestone has a separate destructive confirmation.
26. **Permission denial** — A reviewer who is neither indicator assignee nor admin is told that their user lacks permission; no retry with a different identity or claim of success follows.

## Negative cases

1. The agent never uses `teams_listMineByCompany` or ordinary memberships to infer the user's review cluster.
2. A user who leads a team but is not the configured leader of that team's cluster is never described as cluster leader.
3. A supplied review URL causes no write before interview and confirmation.
4. A changed weight without a rationale is never proposed to MCP.
5. Weights are never written one KR at a time or through DRAFT/reporting tools.
6. An unmeasurable stored zero is never described as zero performance.
7. A 300-risk Analyze response or truncated context never advances.
8. Missing positive-weight Next data never triggers reporter-side default creation.
9. Close-context approval is never reused as closure approval.
10. The agent never invents mentee scores, evidence, reporter intent, or in-period completion. Empty evidence sets show 0 and still require both scores. Non-mentor reviewers are not asked to rate.
11. The agent never makes one Analyze-context call per positive-weight KR during review.
12. The agent never advances to Next while `highestRiskCoverage.complete` is false or a pending priority proposal would make it false.
13. The agent does not ask for assignee or cadence when the team leader exists and the reviewer has not overridden the 7-day defaults.
14. The agent never uses several `risks_update` calls for one final review priority selection when the atomic reviewer tool is available.
15. The agent never exposes internal IDs by default or asks a second confirmation that merely restates an already confirmed business decision as JSON or tool syntax.
16. The agent never asks the reviewer to supply forecast and target from scratch without first making a concrete evidence-based proposal.
17. When July is unmeasured but the indicator's latest value is 50% on 30 June, the agent never proposes from zero or says no current baseline exists.
18. The agent never exposes `forecast` or `target` terminology to the reviewer; it always says `obiettivo minimo` and `obiettivo massimo`.
19. The agent never describes a stored LinkHub value as ClickHouse-verified when either evidence operation failed, and it does not retry a `DATA_SOURCE_ERROR` with speculative keys or another environment.
20. The agent never repeats explanation or evidence calls for the same indicator during one review unless the reference period or indicator binding changed.
21. The closing note never reads like an audit trail or implementation payload and never tells the reporter that an initiative was assigned with a seven-day check-in or without an automatic message.
22. The agent never offers an unlinked monitoring initiative. If the reviewer has not selected a suitable numbered risk, it asks for one or proposes a separately confirmed risk creation before any initiative proposal or `initiatives_create` call.
23. The agent never displays a proposed weight that is not divisible by 5, even when the current inherited weight is 21 or 49.
24. The agent never asks the reviewer to approve future values without showing the dated current operational value or explicitly stating that none exists.
25. The agent never advances from weights directly to Next values without a visible risks-and-initiatives recommendation and reviewer decision for every positive-weight KR.
26. The agent never presents `ABOVE_EXPECTATIONS`, `IN_LINE`, or `BELOW_EXPECTATIONS` as the user-facing outcome when speaking Italian.
27. “Procediamo”, “sarà in line e stabile”, or approval of the proposed note before the complete closure preview never authorizes `reviews_close`.
28. The agent never proposes or sends equal next-period goals for a positive-weight KR, even if the reporter requested `0 / 0` or the reviewed-period measurement is unavailable.
29. The agent never asks which priority to use for a new review risk, proposes a lower creation priority, or omits `priority: "highest"` from `risks_create`.
30. The agent never interprets minimum coverage as a limit of one `highest` risk per KR, or demotes risks to make room for a new or promoted risk.
31. Choosing, keeping, or creating named risks never authorizes demotion of omitted risks; only explicitly requested and confirmed changes enter `reviews_rebalanceRiskPriorities`.
32. The fixed creation priority never authorizes an unconfirmed risk creation.

29. The agent never says milestones are read-only when the write tools are available.
30. Confirmation of a replacement never authorizes a separate milestone removal.
31. Milestone corrections never write reporter-side tracked results or touch indicators outside the fixed team.

## Pass criteria

- The first user-facing review content is a factual note-and-context briefing.
- The interview is one question at a time, uses the closed period as evidence, and validates priorities for the next operating period rather than retroactively reweighting performance.
- Every mutation uses a reviewer-specific tool or a separately confirmed Analyze/milestone tool.
- Non-empty closure requires 100% reviewed weight and both reviewed Next values for every positive-weight KR.
- New review risks are created at `highest` without a priority question, after creation confirmation; existing priorities remain unchanged unless explicitly requested and confirmed.
- Multiple `highest` risks per KR are accepted; positive-weight KRs with none remain a blocking gap.

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


## Bonus validation cases (WZ-1834)

- Positive: a non-admin validator asks for “Da validare”. Start with the personal
  `bonusValidations_list` queue, complete pagination, and show its caution signals.
  No cluster leadership or admin page is required.
- Contextual: an admin asks for all company validations. Use company scope only
  for that explicit request; the default remains the personal queue.
- Negative: an ordinary unassigned member, another validator or an expired
  membership cannot read or save the target; do not retry with elevated identity.
- Negative: unknown suggestion provenance, missing historical milestones or a
  saturated annual range are explained, never converted into a negative judgment.
- Negative: original suggested Next intervals do not prove the reviewer accepted
  default values or skipped the review.
- Positive: approval/rejection requires nonblank motivation plus confirmation of
  the exact report, outcome, note and bonus effects, followed by a readback.
- Negative: “rimetti in review”, blank motivation, an open report or a bonus-excluded
  report cannot be submitted. Bonus validation never calls `reviews_close`.
- Negative: a bonus-validation request must not launch the IN_REVIEW weight
  interview, modify closed review content or bypass a timed session's allowlist.
