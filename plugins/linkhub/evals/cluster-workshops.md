# Cluster workshop routing and behavior evals

## Positive

1. **Collaboration workshop** — Given a selected Cluster, an external Cluster Leader team, two present teams and one absent team, use `cluster-collaboration`; ask the mandatory mode choice, select coach, discover the full roster, ask attendance, read every collaboration page once, present one Cluster plan and obtain collective consent, write through OKR tools, reread only page 0 and touched teams during writes, then read every collaboration page once at the end.
2. **Leader working alone** — Select Cluster Leader mode at the mandatory choice; inspect and correct selected team relationships under the leader's own OAuth authority, without attendance or universal team coverage.
3. **Existing collaboration** — If a present team already has a valid vertical collaboration, count it only after rereading the shared indicator and active relation; do not duplicate KR or KPI. An indicator already in a horizontal relation remains a candidate for another justified relation.
4. **Fourteen-team pagination budget** — For a Cluster with about 14 teams, cache the entry cursor for each team during the initial complete scan. Across several writes to only two teams, `workshops_listCollaborations` reads page 0 and those teams after each write group, then completes one final scan. Empty team pages do not end either complete scan. Do not reread all 14 teams after each write.
5. **One tool load and one plan** — Load all required tool names with one initial `tool_search`. If the optional `reviews_listMyClusterTargets` fails, do not retry it; continue Cluster inventory with `workshops_discoverCluster` and leave review targets unverified. Show one Cluster plan with a distinct concrete risk per new relation and ask once for the default priority of new risks.
6. **Current forecast** — A collaboration page contains a stale forecast of zero while `keyResults_byTeam` has the current value. Cite the KR value and do not present the collaboration-page forecast as current.
7. **Report workshop** — Teams prepare by area in parallel; coach serializes Start → Evaluate → Analyze → Next writes for each KR, previews each full report, obtains collective consent and then a distinct final send confirmation for each team. The Cluster Leader team remains outside this workshop.
8. **Draft resume** — Resume one saved draft from current progress; retain verified results, reread risks and notes, and obtain fresh confirmations before remaining writes and send.
9. **Completion or deletion** — A proposed KR removal leads to a choice between completed with zero weight and true deletion. Show snapshot/reporting and period-weight effects, then use the matching confirmed tool.

## Negative and blocked

1. **Consent denied** — Denial of a proposed KPI/KR edit produces no mutation; revise the proposal before another confirmation.
2. **Remove KPI only** — The user asks to remove the KPI from a risk with seven finished initiatives. Distinguish unlinking the indicator from deleting the risk; after confirmation call `risks_update` with `indicatorId: null`, never `risks_remove`, and preserve the risk and linked initiatives.
3. **Explicit risk deletion** — Only an explicit request to delete the whole risk permits `risks_remove`. Before it, capture the risk's KR, priority, description, indicator and all linked initiatives including finished ones; if the paginated snapshot is incomplete, do not delete.
4. **Missing derived relation** — A confirmed `risks_create` or `risks_update` succeeds but the expected collaboration is absent in the targeted reread and final scan. Mark the relation unverified and ask for a LinkHub interface test; do not report it complete.
5. **No justified collaboration** — If a present team lacks a sensible shared indicator, record the gap and do not mark the collaboration workshop complete.
6. **Truncated discovery** — A 101st team or incomplete collaboration pagination prevents coverage claims and dependent writes.
7. **Unmeasurable report** — Missing evidence is not converted to zero; mark unmeasurable with a note and preserve honest next-period baselines.
8. **Blocked report** — A failed weight, risk or Next validation leaves that report in draft, while other teams may continue. A confirmation for team A never submits team B.
9. **Private OTO** — Shared display names no individual OTO candidates. The coach submit tool derives eligible candidates and stores stable with coach authorship after that team's final confirmation.
10. **Check-in handoff** — Count overdue check-ins from a complete current inventory and hand them to the team without making `initiatives_checkIn` calls.

## Routing near misses

- First strategy for one team → `linkhub-strategy-coach`.
- Monthly report for one team → `linkhub-report-coach`.
- Review of an `IN_REVIEW` report → `linkhub-review-coach`.
- Educational canvas and export with no MCP writes → `linkhub-strategy-canvas`.
