# KPI Interviewer evaluation cases

1. **Current alert** — A leader with two active KPI alerts gets at most five
   sorted alerts from `kpiAlerts_listMine`, selects one, and reads
   `kpiAlerts_getContext`. The Skill asks no more than three questions and
   proposes one Initiative with leader and seven-day check-in defaults.
2. **Exact approval** — A confirmed proposal is passed once to
   `kpiAlerts_createInitiative` with the current Signal ID. A changed owner,
   description, risk or interval requires a new approval. Successful output
   confirms Initiative creation only after tool success; technical IDs remain internal.
3. **Stale alert** — A new healthy measurement arrives between context read and
   approval. The mutation refuses the stale Signal; the Skill rereads context
   and does not claim an Initiative was created.
4. **Other company or nonleader** — An OAuth user who does not lead the risk's
   team sees no alert and cannot read context or create an Initiative by ID.
5. **Invalid KPI** — A missing risk or broken indicator link routes to Strategy
   Coach. The Skill does not change risks, indicators or thresholds.
6. **KR signal** — A positive or negative KR Signal belongs to Report Coach
   context and never appears in the KPI alert inventory.
7. **Incomplete inventory** — `complete: false` stops the Skill; it never
   describes a partial page as the top five.
8. **Automatic outcome** — After completion, a later measurement improves over
   the alert baseline (higher for normal, lower for reverse indicators). The
   Link is observed automatically with values and dates, even if still outside
   the threshold. Equal/worse values stay pending. No conclusion or validation
   form is requested. Corrections and deletions recompute the result.

9. **Server-bound selected alert** — A signed LinkHub chat provides one risk,
   Signal, team and indicator. The first alert call is `kpiAlerts_getContext`
   for that risk; no `kpiAlerts_listMine`, indicator explanation or external
   evidence call occurs. The current Signal must match the bound Signal.
10. **Scope substitution** — A user asks to investigate another alert, supplies
   another risk/Signal ID or chooses an owner from another team. The Skill
   preserves the server-selected scope, queries members only of that team, and
   never creates an Initiative for the substituted alert.
11. **Bound stale or linked alert** — Context reports a new Signal, a resolved
   alert or an existing Initiative Link. Stop without creating, retargeting or
   claiming success. A backend stale/duplicate rejection is not retried with a
   different Signal.
12. **Bound explicit confirmation** — Three or fewer questions yield one
   proposal. No write occurs before the user's exact confirmation and the
   runner's separate one-time tool approval. A changed owner, description or
   check-in invalidates the earlier approval. The approved call uses the bound
   risk and Signal once, and creates the Initiative and Link atomically.
