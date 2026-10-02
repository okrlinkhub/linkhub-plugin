# KPI Interviewer evaluation cases

1. **Current alert** — A leader with two active KPI alerts gets at most five
   sorted alerts from `kpiAlerts_listMine`, selects one, and reads
   `kpiAlerts_getContext`. The Skill asks no more than three questions and
   proposes one Initiative with leader and seven-day check-in defaults.
2. **Exact approval** — A confirmed proposal is passed once to
   `kpiAlerts_createInitiative` with the current Signal ID. A changed owner,
   description, risk or interval requires a new approval. Successful output
   includes Initiative and Link IDs.
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
