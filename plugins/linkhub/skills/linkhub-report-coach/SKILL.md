---
name: linkhub-report-coach
description: >-
  Completes a LinkHub periodic team report end to end through MCP, including
  automatic approved indicator evidence, coached KR evaluation, risks,
  initiatives, next-period plans, reporter notes, and separately confirmed
  submission. Use for monthly reports, DRAFT completion, OKR review, or when the
  user asks to report a team without opening LinkHub in a browser. Do not use
  for reviewer approval after the report is IN_REVIEW; use
  `linkhub-review-coach` for that workflow.
---

# LinkHub Report Coach

Complete the report entirely through the LinkHub MCP connection. Never require browser use for the report. Reply in the user's language; preserve LinkHub names and enum values exactly.

If the selected report is already `IN_REVIEW`, stop this workflow and route to `linkhub-review-coach`; reporter tools must not be used to simulate reviewer decisions.

## Safety contract

- Reads may run automatically.
- Before every logical group of writes, show its complete user-visible effects in readable business terms and wait for explicit confirmation. Keep record IDs, transport fields, and raw MCP payloads hidden unless the user asks for them.
- A clear confirmation of the displayed proposal authorizes its immediate write. Never ask a second confirmation merely to repeat the same decision as JSON, IDs, or tool syntax. A confirmation covers only the displayed group; if its user-visible effects change, ask again.
- `reports_submit` always requires a new, separate confirmation immediately before the call. Never include it in an earlier approval.
- Never invent a number, date, cause, SQL expression, measure, dimension, or catalog metric.
- A numerical ClickHouse claim is allowed only after a successful `indicators_queryEvidence` or `indicators_queryCatalogEvidence` response.

## 1. Open the report

Read `mcp_membershipProfile`, `companies_list`, and `reports_listDueForUser`. If several teams or reports match, present the choices and ask the user to select one. Create a missing draft with `reports_createDraft` only after describing the team, reporting period, and resulting draft in readable terms and receiving confirmation.

Load `reports_getWorkflowProgress` and one team snapshot with `objectives_byTeam`, `keyResults_byTeam`, `initiatives_byTeam`, and `initiatives_listMinePending`. Do not fan out risk reads for every KR.

## 2. Work through each KR

Follow LinkHub's workflow in this order and do not bypass it:

1. `reports_getEvaluateContext`
2. evaluate result
3. `reports_getAnalyzeContext`
4. analyze risks and initiatives
5. `resultNext_skipWithDefaults` or `resultNext_upsert`

### Milestone-driven indicators

When the evaluate context says `hasMilestones: true`, always call
`milestones_listByIndicator` before proposing the evaluation result.

1. Show every milestone's description, percentage `value`, status, planned
   date, and achieved date, followed by `totalValue`, `achievedValue`, and
   `pendingValue` from the tool response.
2. Ask whether the milestone state is correct. Never calculate or silently
   repair the totals yourself, and never interpret an empty milestone list as
   zero progress.
3. For changes, resolve each calendar date with `mcp_resolveIsoDate`, show the
   readable milestone changes, and wait for confirmation before calling
   `milestones_create`, `milestones_update`, `milestones_complete`, or
   `milestones_reopen`. A planned date is removed internally only with an explicit
   `forecastDateIso: null`.
4. Treat `milestones_remove` as a destructive correction: identify the
   milestone and explain that it will be removed, then obtain a separate,
   explicitly highlighted confirmation. Keep IDs and the raw payload hidden
   unless requested. Do not substitute a removal when the user only needs
   `milestones_reopen`.
5. After any milestone write, call `milestones_listByIndicator` again. Use only
   the returned `summary.achievedValue` as the verified LinkHub milestone value.
6. Perform `resultTracked_upsert` only after the final milestone reread so the
   report snapshot captures the confirmed state.

If an indicator is both milestone-driven and automated, collect both LinkHub
milestone evidence and the approved ClickHouse evidence below, present them
separately, and ask the user which source should drive `actualResultValue`.
Never choose a precedence silently.

### Automatic indicator evidence

For each KR, inspect the evaluate context. If its indicator is automated:

1. Call `indicators_getExplanation`.
2. Show the definition, inclusions, exclusions, caveats, binding state, default measure/dimension keys, and approved reference period.
3. When `queryReady` is true and a reference period exists, call `indicators_queryEvidence` with `summary`, then `compare_previous_period`, using that exact half-open interval and the returned `resolvedMeasureKey`.
4. Call `latest_available_period` only when LinkHub did not provide a reference period.
5. Use `breakdown` or `trend` only for a visible anomaly or an explicit user question. Follow `nextCursor` while `hasMore` when complete coverage is required; show `dimensionLabel` and retain `dimensionId`.
6. Use `indicators_listExplainable` or `indicators_resolve` to discover LinkHub indicator instances. Use `indicators_searchCatalog` and then `indicators_queryCatalogEvidence` only for a specific question involving a different analytic metric. Pass the exact returned `namespace` and `metricKey`.
7. Never substitute a missing dimension with `macro_category` or another proxy that the explanation did not approve. Treat `ok: false` as unavailable evidence and show the diagnostic code.

Before proposing an evaluation write, present:

- LinkHub indicator and KR;
- ClickHouse value and exact interval;
- previous-period comparison;
- definition and applicable caveats;
- whether rows were empty or truncated.

For a milestone-driven indicator, also present the final LinkHub milestone
summary and identify it as LinkHub evidence rather than ClickHouse evidence.

If the explanation is missing, orphaned, not query-ready, or returns no rows, use only existing LinkHub values that are explicitly present in the report context. Otherwise propose `resultTracked_markUnmeasurable` with an honest note. Never translate an empty result into zero.

### Evaluation writes

Propose exactly one of:

- `resultTracked_upsert` for a verified value;
- `resultTracked_markUnmeasurable` when evidence is unavailable;
- `resultTracked_markCompleted` for a completed zero-weight objective.

Do not pass `weightReported` to `resultTracked_upsert`. Weight changes in a draft use only `keyResults_rebalanceWeightInDraftReport` and require their own confirmed write group.

Milestone corrections and the evaluation result are separate write groups. An
approval for milestone changes never authorizes `resultTracked_upsert`.

### Analyze and next

After the tracked-result write, always load risks and initiatives for the current
KR with `reports_getAnalyzeContext`; do not skip Analyze. Before any Analyze
write or Next proposal:

1. Verify that the risk list is complete before filtering it. The current
   `reports_getAnalyzeContext` contract returns at most 300 active risks and has
   no cursor. When it returns exactly 300 risks, treat the result as potentially
   truncated: explain that MCP cannot guarantee a complete list and stop before
   confirmation, Analyze writes, or Next. Do not use `risks_byKeyResult` as a
   pagination substitute; it also has no cursor and returns at most 200 risks.
2. Show a concise list of every current-KR risk whose priority is exactly
   `highest`. Prefix the complete current-KR risk list with stable local references
   (`R1`, `R2`, ...) and reuse those references throughout that KR interview. If
   there are no `highest` risks, state that explicitly.
3. Ask the user to confirm both that these are the relevant highest-priority
   risks and that their priorities are correct. These confirmed risks are the
   primary explanations available to the reviewer for the reported result.
4. If the user changes a priority, show the referenced risk, description, and
   resulting priority in business terms and obtain confirmation before calling
   `risks_update`.
5. After any risk write, reload the current-KR Analyze context, repeat the
   completeness check, show the updated `highest` list, and confirm it again.
   Retain only the latest confirmed,
   still-current `highest` risks as candidates for the reporter note.

Then ask whether observed risks still explain the gap. Propose removals, new
risks, initiative check-ins, or new initiatives as one clearly scoped write
group. Before creating an initiative, call `teams_listMembers`; resolve calendar
dates with `mcp_resolveIsoDate`. Never duplicate an existing initiative.

### Plan the next period

For every non-zero-weight KR, present a concrete next-period proposal instead of
asking the reporter to invent two numbers:

- show the latest available indicator value and its date as the operational
  starting point, even when the report-period result is unmeasurable;
- if no latest value exists, fall back to a measurable report-period result;
  otherwise state that no numerical starting point is available rather than
  treating a stored zero as evidence;
- label the two user-facing values only as **obiettivo minimo** and **obiettivo
  massimo**;
- ground both proposed values in the starting point, verified indicator
  evidence when available, confirmed risks, active initiatives, annual
  objectives, and the KR weight;
- ask once whether the reporter confirms or wants to modify the proposal.

Never expose `forecast`, `target`, `forecastValue`, `targetValue`, or related MCP
field names in user-facing messages; use them only to construct the internal
call. Reuse explanation and evidence already retrieved for the same indicator
during the report, and do not repeat calls just because the conversation moved
to Next.

Use `resultNext_skipWithDefaults` only after presenting its resolved default
values as obiettivo minimo and obiettivo massimo and receiving confirmation.
Otherwise use `resultNext_upsert` with the confirmed internal mapping. Recheck
`reports_getWorkflowProgress` every one or two KRs.

## 3. Initiative hygiene

Before submission, process relevant pending check-ins. Every `initiatives_checkIn` or `initiatives_finish` needs a non-empty progress note. Show each proposed group and wait for confirmation.

## 4. Reporter note

Draft a short business note in the user's language and show it before writing.
Include only:

- a brief summary of how the period went, mentioning measurement limitations
  only when they materially change the interpretation;
- the most important recorded results;
- up to three user-confirmed `highest` risks, using only their readable names or
  descriptions;
- the focus, obiettivo minimo and obiettivo massimo changes that should guide
  the next period;
- when useful, initiatives added or changed and the outcome they should produce.

Keep ClickHouse intervals, evidence diagnostics, MCP mechanics, internal IDs,
payload fields, check-in mechanics, and tool outcomes in the conversation, not
in the reporter note. Do not cite a ClickHouse number that was not returned
successfully. If more than three `highest` risks qualify, show the numbered
candidates and ask which three best explain the results; never choose silently.
Save with `reports_updateReporterNotes` only after confirmation.

## 5. Final check and submission

Read `reports_getWorkflowProgress`, `objectives_byTeam`, and `keyResults_byTeam`. Verify all KRs are complete, weights total 100%, no KR is orphaned, overdue initiatives are handled, and reporter notes are saved.

Call `reports_getSubmitContext` immediately before proposing the submit payload.
For every returned OTO candidate, show the readable `userName` and encode exactly
one item as `{ menteeId, answer }`. The only allowed answers are:

- `stable`: stable career/role trajectory;
- `growing`: growing career/role trajectory;
- `declining`: declining career/role trajectory.

Use the returned `defaultAnswer` only when the user has not stated a different
trend. Include every candidate returned by the context, exactly as the LinkHub UI
does. If there are no candidates, omit `otoCheckins` rather than inventing one.

Then show every user-visible submission effect in readable terms and ask a
dedicated final question without exposing IDs or tool syntax. Call
`reports_submit` only after that separate confirmation. Report the returned
status and any remaining follow-up.

## References

- MCP report tools: [reference-mcp-tools.md](reference-mcp-tools.md)
- Indicator evidence protocol: [indicator-evidence.md](indicator-evidence.md)
