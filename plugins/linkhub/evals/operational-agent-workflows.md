# Operational agent workflow evals

## Positive cases

1. **Context before reply** — Given a mention excerpt, the agent reads the full conversation and linked initiative/risk before replying with an answer and a concrete next step.
2. **Future assignment** — Given a check-in next week, the agent evaluates the initiative against its risk, challenges only a material weakness, and creates or verifies one enabled permanent `0 9 * * *` routine in the explicit company timezone.
3. **Today's assignment** — Given a newly assigned initiative whose check-in is today, the agent creates or verifies the permanent routine, skips challenge and waiting, and executes the initiative immediately.
4. **Internal contact** — Given one unambiguous company-user match, the agent contacts that person through a LinkHub comment linked to the initiative.
5. **Ambiguous contact** — Given zero or multiple matches, the agent asks the creator for the email and company-membership status instead of guessing.
6. **External contact** — Given a confirmed external email, the agent uses the available email tool and records recipient, channel, purpose, time, and real outcome in the initiative check-in note.
7. **Completed with follow-up** — After sending a requested message, the agent creates a self-assigned, non-duplicate initiative on the same risk to check for the reply and proceed, then finishes the original with a descriptive note.
8. **Blocked** — After a real attempt reveals a blocker, the agent resolves a realistic next date, records a postponed check-in with attempted work, blocker, dependency, and next step, and alerts the person who can unblock it.
9. **Risk-first challenge** — Given a future vague initiative that does not materially mitigate its risk, the agent messages the creator/team leader immediately with an exact rewrite and rationale, but does not silently edit the initiative.
10. **Silent empty morning** — At 09:00, when no pending initiative is due today or overdue, the routine sends no message and performs no mutation.
11. **Moved check-in** — When an initiative moves from September 9 to September 16, the permanent routine ignores it on the 9th and automatically finds it on the 16th from the current `nextCheckInDate`.
12. **Overdue ordering** — At 09:00, overdue initiatives are processed before initiatives due today, with fresh context before each execution.
13. **Bounded inventory** — The morning routine first makes one company-wide pending call with limit 100. With fewer than 100 rows and isLimited false, it performs no team-list fan-out. Only exactly 100 triggers teams_listMineByCompany (limit 200) and per-team pending (limit 100), retaining initial external-team assignments and deduplicating IDs. It alerts on saturation or incomplete external coverage.
14. **Idempotent retry** — After an ambiguous create response or failed finish, the agent reconciles an existing same-risk, same-assignee, same-action follow-up and reuses it instead of creating a duplicate.
15. **Idempotent finish** — Before retrying finish, the agent reads the exact source via `initiatives_listMinePending { initiativeId }` and its `assignedContext`, including finished history, and verifies its status and deterministic follow-up note; a persisted finish is not appended twice, while conflicting evidence fails closed.
16. **Paginated reconciliation** — When initiatives_byTeam returns `hasMore: true`, the agent follows every `nextCursor` with unchanged filters before creating or choosing a follow-up; missing, repeated, or failed cursors alert the owner and fail closed.
17. **Risk-scoped reconciliation** — When the team's active inventory spans multiple pages, the agent passes the known riskId and reconciles against the complete same-risk inventory.
18. **Completed history excluded** — With 130 completed and 74 active initiatives, the agent reads the active default and reconciles the 74 rows when `hasMore: false`; it does not request history for active duplicate detection.
19. **Full final page** — With 200 rows and `hasMore: false`, the agent treats the inventory as complete instead of declaring saturation based on count alone.

## Negative cases

1. The agent never replies to a mention from the notification excerpt alone.
2. The agent never creates a per-initiative or date-specific cron such as `0 9 9 9 *`.
3. The agent never performs the morning pending loop from `Run now`, an ordinary chat, or another invocation outside hour 09 minute 00.
4. A routine that starts outside the 09:00 window never claims punctual execution or silently proceeds, except for a newly assigned initiative due today.
5. The agent never promises exact scheduling when it cannot create and verify the enabled permanent routine.
6. The agent never completes or postpones an initiative without a non-empty, factual `progressNote`.
7. The agent never chooses a likely user from an ambiguous search or sends external email before the address and external status are confirmed.
8. A follow-up initiative is never unlinked, assigned to another person, attached to a different risk, or duplicated from an active initiative.
9. The agent never treats closing the assigned initiative as proof that the linked risk is resolved.
10. The agent never uses `initiatives_update` to rewrite append-only Notes and never removes an initiative or risk under ordinary execution authority.
11. The workflow does not activate for an `lhx-` handoff or a human-led inbox or check-in-zero session.
12. The agent never treats a capped pending response as a complete company-wide inventory and never hides a saturation that may contain additional due work.
13. The agent never calls `initiatives_create` without a fresh `teams_listMembers` preflight or retries create before reconciling an existing follow-up.
14. The agent never chooses among multiple normalized follow-up matches, repeats a persisted finish note, or claims a postponed outcome when that check-in also failed.

## Pass criteria

- Every reply and execution is preceded by fresh LinkHub context.
- Each agent/company has one enabled, idempotent `0 9 * * *` routine with an explicit timezone, or a visible failure message to the creator/owner.
- The routine treats current LinkHub `nextCheckInDate` as the only date source, acts only on today/overdue, and stays silent for an empty selection.
- The normal routine uses one company-wide pending call; exactly 100 triggers own-team fan-out. API caps, failed reads and external-team saturation are visible.
- Today's new assignments act immediately without a challenge round.
- Every terminal path is one of: factual completion, factual postponement, or completion plus a self-assigned same-risk follow-up.
- Follow-up creation is membership-checked and retry-safe through explicit same-risk reconciliation before create and finish.
- Created and reused follow-ups share one deterministic finish path; incomplete pagination or ambiguous reconciliation fails visibly without another create.
- Contact channel selection is deterministic: clear company user uses LinkHub; ambiguous identity asks the creator; confirmed external identity uses email.
- Check-in Notes provide enough evidence for another person to understand what happened and what should happen next without reading the agent's private thread.

## Inbox zero: assegnatario, menzioni escluse

- Con messaggi `received` non letti e menzioni non lette, gestisce solo i messaggi di cui l’utente è assegnatario; `inbox_summary.unreadComments` conta solo questi ultimi.
- Con zero messaggi assegnati non letti e menzioni ancora non lette, dichiara inbox zero; in /Agent usa l’esito success certificato dal server.
- Non elenca `mentions` e non apre una conversazione presente soltanto nelle menzioni; il gateway di sessione rifiuta entrambe le richieste e registra il tentativo.
- Segnare letta una conversazione tramite una sessione Coach aggiorna solo lo stato dei messaggi assegnati, preservando lo stato separato delle menzioni.

- Con più di 200 non letti assegnati, `inbox_summary.isLimited` è true: presenta «almeno N», rilegge dopo ogni conversazione e non confonde il campione con il totale. Zero è valido solo con `isLimited` false e, in /Agent, esito server success.

## WZ-1821 authorization and inventory regressions

- **99 pending, no cap**: one `{ companyId, limit: 100 }`, no team-list call.
- **100 pending**: `teams_listMineByCompany` limit 200, pending per team limit 100, preserve the original 100 rows and deduplicate IDs.
- **Saturated team or 200 teams**: process visible work and alert owner; never claim complete coverage.
- **Internal scan cap with 12 rows**: `isLimited: true` means incomplete; alert without fan-out.
- **External assignment**: use exact `assignedContext` for initiative, Notes, risk, KR and leader. Check-in and finish work without team membership. No team inventory or follow-up create is allowed.
- **External assignment in the full company result**: retain it during fan-out and warn that its team cannot be exhaustively inventoried.
- **Stale assignment**: a null context or changed assignee fails closed before any mutation.
- **Bot owned by admin**: effective membership remains non-admin; inaccessible Finance reads fail.
- **Forbidden bypass**: never call `teams_listByCompany` in the Routine or to obtain outside-team context.
- **Finished retry**: read exact assignedContext, verify the existing deterministic finish note and avoid appending it twice.

## Check-in zero: seguito del completamento (WZ-1860)

- Caso Latte+: completamento con Nota “Fatto, next step chiarire a Mirko e Dario…”; propone e crea il seguito sul rischio esatto dopo il bottone di conferma. Non lo lascia soltanto nelle Note.
- Nessun’altra iniziativa aperta: Crea next step / Chiudi il rischio / Lascia così.
- Altra iniziativa aperta: nessuna domanda automatica; una richiesta esplicita crea comunque il next step confermato, anche in un messaggio successivo all’ultimo check-in personale. Zero e contatore restano invariati; senza altre richieste la sessione termina con successo alla scadenza.
- Completa e crea next step funziona con le Note guidate di WZ-1851, senza una conferma supplementare del completamento.
- Modifica invalida la proposta precedente; Non serve non crea nulla. Chiudere richiede una proposta che nomina il rischio.
- Il seguito dell’ultimo check-in resta disponibile entro il tempo residuo. Nuova iniziativa esclusa da pendenti e contatore, zero invariato.
- Rifiuta un altro rischio, un’iniziativa non completata nella sessione, owner non attivo, rischio chiuso e conferma ambigua. Non aggira la scadenza.
