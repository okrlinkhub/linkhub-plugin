---
name: linkhub-report-coach
description: >-
  Completes a LinkHub periodic team report end to end through MCP, including
  automatic approved indicator evidence, coached KR evaluation, risks,
  initiatives, next-period plans, reporter notes, and separately confirmed
  submission. Use for monthly reports, DRAFT completion, OKR review, or when the
  user asks to report a team without opening LinkHub in a browser.
---

# LinkHub Report Coach

Complete the report entirely through the LinkHub MCP connection. Never require browser use for the report. Reply in the user's language; preserve LinkHub names and enum values exactly.

## Safety contract

- Reads may run automatically.
- Before every logical group of writes, show the exact proposed payloads and wait for explicit confirmation.
- A confirmation covers only the displayed group. If its payload changes, ask again.
- `reports_submit` always requires a new, separate confirmation immediately before the call. Never include it in an earlier approval.
- Never invent a number, date, cause, SQL expression, measure, dimension, or catalog metric.
- A numerical ClickHouse claim is allowed only after a successful `indicators_queryEvidence` or `indicators_queryCatalogEvidence` response.

## 1. Open the report

Read `mcp_membershipProfile`, `companies_list`, and `reports_listDueForUser`. If several teams or reports match, present the choices and ask the user to select one. Create a missing draft with `reports_createDraft` only after showing that write payload and receiving confirmation.

Load `reports_getWorkflowProgress` and one team snapshot with `objectives_byTeam`, `keyResults_byTeam`, `initiatives_byTeam`, and `initiatives_listMinePending`. Do not fan out risk reads for every KR.

## 2. Work through each KR

Follow LinkHub's workflow in this order and do not bypass it:

1. `reports_getEvaluateContext`
2. evaluate result
3. `reports_getAnalyzeContext` when useful
4. analyze risks and initiatives
5. `resultNext_skipWithDefaults` or `resultNext_upsert`

### Automatic indicator evidence

For each KR, inspect the evaluate context. If its indicator is automated:

1. Call `indicators_getExplanation`.
2. Show the definition, inclusions, exclusions, caveats, binding state, and approved reference period.
3. When `queryReady` is true and a reference period exists, call `indicators_queryEvidence` with `summary`, then `compare_previous_period`, using that exact half-open interval.
4. Call `latest_available_period` only when LinkHub did not provide a reference period.
5. Use `breakdown` or `trend` only for a visible anomaly or an explicit user question.
6. Use `indicators_searchCatalog` and then `indicators_queryCatalogEvidence` only for a specific question involving a different catalog metric. Pass the exact returned `namespace` and `metricKey`.

Before proposing an evaluation write, present:

- LinkHub indicator and KR;
- ClickHouse value and exact interval;
- previous-period comparison;
- definition and applicable caveats;
- whether rows were empty or truncated.

If the explanation is missing, orphaned, not query-ready, or returns no rows, use only existing LinkHub values that are explicitly present in the report context. Otherwise propose `resultTracked_markUnmeasurable` with an honest note. Never translate an empty result into zero.

### Evaluation writes

Propose exactly one of:

- `resultTracked_upsert` for a verified value;
- `resultTracked_markUnmeasurable` when evidence is unavailable;
- `resultTracked_markCompleted` for a completed zero-weight objective.

Do not pass `weightReported` to `resultTracked_upsert`. Weight changes in a draft use only `keyResults_rebalanceWeightInDraftReport` and require their own confirmed write group.

### Analyze and next

Load risks and initiatives for the current KR only. Ask whether observed risks still explain the gap. Propose removals, new risks, initiative check-ins, or new initiatives as one clearly scoped write group. Before creating an initiative, call `teams_listMembers`; resolve calendar dates with `mcp_resolveIsoDate`. Never duplicate an existing initiative.

Use `resultNext_skipWithDefaults` unless the user wants a custom next forecast or target. Show and confirm the write payload. Recheck `reports_getWorkflowProgress` every one or two KRs.

## 3. Initiative hygiene

Before submission, process relevant pending check-ins. Every `initiatives_checkIn` or `initiatives_finish` needs a non-empty progress note. Show each proposed group and wait for confirmation.

## 4. Reporter note

Draft the note in the user's language and show it before writing. Keep these sections distinct:

- values recorded in the LinkHub report;
- ClickHouse evidence and its exact periods;
- unmeasurable KRs and reasons;
- risks and initiatives;
- focus for the next period.

Do not cite a ClickHouse number that was not returned successfully. Save with `reports_updateReporterNotes` only after confirmation.

## 5. Final check and submission

Read `reports_getWorkflowProgress`, `objectives_byTeam`, and `keyResults_byTeam`. Verify all KRs are complete, weights total 100%, no KR is orphaned, overdue initiatives are handled, and reporter notes are saved.

Then show the exact `reports_submit` payload and ask a dedicated final question. Call `reports_submit` only after that separate confirmation. Report the returned status and any remaining follow-up.

## References

- MCP report tools: [reference-mcp-tools.md](reference-mcp-tools.md)
- Indicator evidence protocol: [indicator-evidence.md](indicator-evidence.md)
