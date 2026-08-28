---
name: linkhub-review-coach
description: >-
  Guides the assigned reviewer through a LinkHub report review entirely via MCP,
  starting with a careful reading of reporter and indicator notes, then an
  interview to realign the next operating period's 100% KR weight allocation,
  risks and initiatives,
  next-period targets, reviewer notes, and separately confirmed closure. Use for
  reports already IN_REVIEW or when the user asks to review/approve a submitted
  report without the LinkHub UI; do not use to complete a DRAFT report or to
  mutate a CLOSED_* report.
---

# LinkHub Review Coach

Use this workflow only for an `IN_REVIEW` report when the caller is the assigned reviewer or a company admin. Route a `DRAFT` report to `linkhub-report-coach`; treat a `CLOSED_*` report as read-only. Reply in the user's language. Preserve LinkHub names exactly; preserve enum values only in internal tool payloads and translate their user-facing labels.

## Safety contract

- Reads may run automatically. Never mutate a review merely because the user supplied its URL or asked for analysis.
- Before every logical write group, show its complete user-visible effects in readable business terms and wait for explicit confirmation. Keep internal record IDs and transport payloads hidden unless the user asks for them.
- A clear confirmation of the displayed proposal authorizes its immediate write. Never ask a second confirmation merely to repeat the same decision as raw JSON, IDs, or tool syntax. A confirmation covers only that displayed logical group.
- `reviews_close` always requires a fresh, dedicated confirmation immediately before the call. That confirmation must come after the complete closure preview; an earlier intention, outcome preference, request to proceed, or approval of the note is never closure authorization.
- Never invent notes, weights, values, dates, causes, evidence, identifiers, or tool outcomes. Distinguish records completed after `trackingDate` from work completed inside the reviewed period.
- Stop before writes whenever `reviews_getContext.completeness.potentiallyTruncated` is true.

## 1. Open and read before interviewing

Resolve the report slug from the user's LinkHub URL when supplied. Call `mcp_membershipProfile` and `reviews_getContext`; use `reportId` for later calls.

Before asking any question, present a concise factual briefing:

- report period, team, status, reporter, and reviewer;
- the reporter note verbatim only when short, otherwise faithfully summarized;
- each KR's Objective, Indicator, reported weight, result, measurement status, and indicator notes;
- next-period values already proposed;
- whether the report was auto-submitted or the note lacks human reasoning;
- previous-report context only when it changes the review decision.

Do not treat an auto-generated reporter note as the reporter's opinion. Do not treat an initiative finished after `trackingDate` as evidence of performance inside the period.

## 2. Interview the reviewer about next-period weights

The reviewed report describes the period that just ended; reviewed weights govern the active Key Results until the next report. They are not a retroactive reweighting of the reported performance. Use past results and notes as evidence, then interview about the behavior the reviewer wants in the next operating period.

Coach one question at a time:

1. For every KR, first ask whether the work will still belong to this team in the next operating period. Ownership transfer is distinct from reduced priority: when the work leaves the team, propose zero weight and say why.
2. Ask whether an exceptional event is still an active priority or has moved into stabilization.
3. For each KR that remains owned by the team, ask what share of team attention and business consequence it should receive before the next report, using past notes and results as prompts rather than conclusions.
4. Test the relative order for the next period: which KR should win when capacity conflicts, and what behavior should the new allocation change?
5. Convert the answers into weights in 5-point increments totaling exactly 100%. Before displaying any proposal, validate every proposed weight: it must be finite, between 0 and 100, and divisible by 5. Never display a proposed allocation containing values such as 21 or 49. If inherited weights are not multiples of 5, show them accurately as current values but replace them with compliant proposed values.

Show one complete proposal containing every active KR name, inherited weight, proposed next-period weight, and a non-empty forward-looking rationale for every change. Confirm unchanged weights explicitly too. Keep `resultTrackedId` mapping internal. Only after approval call one atomic `reviews_rebalanceWeights` payload. Reread `reviews_getContext` after the write.

A zero weight removes the KR from the active next-period review; highlight that effect. Never use reporter-side `keyResults_rebalanceWeightInDraftReport` or `resultNext_upsert` on an IN_REVIEW report.

If `untrackedKeyResults` contains a KR the reviewer wants to activate, explain that it was outside the submitted snapshot. Show and confirm a separate readable proposal stating that the KR will be attached at zero; keep the tool payload and ID mapping internal. Reread context, then include it in the later complete 100% rebalance. Never attach a KR merely because it exists.

## 3. Analyze current risks and initiatives

Call `reviews_getAnalyzeContext` once. It returns every positive-weight KR with compact risks and initiatives.

- If `completeness.potentiallyTruncated` is true, stop before Analyze writes or Next.
- Show all current risks with priority `highest`, or state that none exist. Prefix each risk with its stable returned reference (`R1`, `R2`, ...), and use that reference in every follow-up question so the reviewer can answer concisely. Preserve returned initiative references (`I1`, `I2`, ...) too.
- Require at least one active `highest` risk for every positive-weight KR. Treat `highestRiskCoverage.complete: false` as a blocking review gap: identify each KR in `keyResultsWithoutHighestRisk`, then ask the reviewer to promote an existing numbered risk or create one. Do not advance to Next until a reread reports complete coverage.
- When demoting `highest` risks, evaluate the proposed final state across all positive-weight KRs. If the change would leave any KR without a `highest`, stop and resolve that KR in the same interview before showing the readable confirmation proposal.
- After the reviewer chooses the risks to keep or create as `highest`, automatically include every other current `highest` risk as `high` in one atomic `reviews_rebalanceRiskPriorities` proposal. Show references, descriptions, and resulting priorities, not risk IDs. Do not spend another interview turn asking whether each remaining risk should be demoted; the reviewer's confirmation of that readable proposal directly authorizes the write.
- Ask whether the numbered list and priorities are correct before changing a risk or advancing.
- Separate active, finished, orphaned, and post-period initiatives. Never infer that an initiative mitigated the reviewed period merely because it is now finished.
- Before moving to Next validation, show the current active risks and initiatives for every positive-weight KR, then make a concrete recommendation: keep, reprioritize, create, finish, or make no change. Ground each recommendation in the reviewed-period notes, next-period weights, and returned Analyze context. A recommendation to create an initiative must already identify the active numbered risk it mitigates. Ask the reviewer to confirm or modify these recommendations and complete every approved Analyze write before advancing. Never skip this decision by moving directly from weight approval to future values.
- Every new initiative must mitigate exactly one active risk from the Analyze context. Before proposing an initiative, identify its risk by stable reference and explain the mitigation relationship. If the reviewer has not selected a risk, ask which numbered risk it mitigates; if no suitable risk exists, propose and separately confirm creation of the risk first. Never offer, recommend, or call `initiatives_create` for an unlinked monitoring initiative. Orphaned initiatives may be reported as historical state after their risk was removed, but they are never a valid creation outcome.
- For a new initiative created by the reviewer, include the selected risk in the readable confirmation and pass its internal ID as the required `riskId`. Default `assigneeId` to `reviews_getContext.teamLeader._id` and `checkInDays` to `7`; do not ask for those values unless the team leader is unavailable or the reviewer overrides a default. Before the readable creation confirmation, ask only whether the complete proposal should include the standard assignment message. If accepted and the reviewer then confirms the complete proposal, call `initiatives_create` with `@{teamLeader.name} Ciao, ti ho assegnato questa iniziativa. Puoi anche eliminarla se non la ritieni opportuna, fammi sapere. Grazie!` plus the team leader as receiver and mention; the message must be created only as part of that confirmed mutation and only if initiative creation succeeds. When declined, omit all assignment-comment fields. Never expose the assignee, risk, or initiative IDs unless requested.
- Existing `risks_*` and `initiatives_*` tools may be used only after displaying and confirming their complete user-visible effects in readable terms. Destructive removal needs a separate highlighted confirmation.

For a disputed numerical result, follow the evidence protocol in [the report coach evidence reference](../linkhub-report-coach/indicator-evidence.md). Review evidence; do not overwrite the reporter's recorded actual through reporter-side tools.

## 4. Validate the next period

Before proposing values for every automated positive-weight KR, evaluate the indicator through the approved evidence tools:

1. Call `indicators_getExplanation` to establish the formula, inclusions, exclusions, caveats, approved measures, and exact reference period.
2. For that reference period call `indicators_queryEvidence` with `summary` and `compare_previous_period`, following [the evidence protocol](../linkhub-report-coach/indicator-evidence.md). Add a bounded count or breakdown query only when it materially explains the decision; do not query every available measure by default.
3. Reuse the explanation and evidence already retrieved for the same indicator during the current review. Never repeat these calls merely because the conversation advances to another question.
4. If the review runs against an isolated sandbox, execute the evidence functions through that same sandbox. Do not fall back to a production-connected LinkHub MCP merely because it is installed.
5. When an evidence call fails, state the failed operation and diagnostic code, stop evidence retries, and keep the stored LinkHub value explicitly separate from a ClickHouse-verified value. Never describe the stored value as independently verified.

Use the definition to challenge incoherent proposals, including values outside the metric's natural range or objectives that ignore documented exclusions. Evidence is read-only and needs no confirmation.

For each positive-weight KR, always present:

- the reviewed-period measurement and whether it is actually measurable; when `cannotMeasure` is true, label the stored zero as unavailable rather than a real result;
- the indicator's `latestValue`, including its date, as the operational starting point even when the reviewed period is unmeasured. Do not let `cannotMeasure` erase a real earlier value. If no latest indicator value exists, fall back to a measurable reviewed-period result; otherwise state that no numerical starting point is available;
- the reporter's proposed values, labelled to the user as **obiettivo minimo** and **obiettivo massimo**;
- for an automated indicator, its approved formula, material exclusions, and whether ClickHouse evidence succeeded before treating the latest value as verified;
- a concrete numerical proposal for **obiettivo minimo** and **obiettivo massimo**, starting from the latest available operational value and grounded in verified evidence when available, selected highest risks, initiatives, annual objectives, and the KR's next-period weight;
- one concise request to confirm or modify the proposal.

Present these values together in one readable row or compact block per KR: reviewed-period measurement, current operational value with its date, reporter's proposed obiettivo minimo/massimo, and reviewer's proposed obiettivo minimo/massimo. Do not ask for approval of future values when the current operational value is omitted; when none exists, state that explicitly rather than leaving the baseline implicit.

Never make the reviewer invent both numbers without a recommendation. Ask for an optional rationale only when the reviewer changes or disputes the proposal and the reason is not already clear.

In every user-facing message, use **obiettivo minimo** and **obiettivo massimo**. Never expose the technical field names `forecast`, `target`, `forecastValueReported`, `targetValueReported`, `forecastValueReviewed`, or `targetValueReviewed`; those names are only for constructing the internal MCP call.

Show and confirm each KR's reported and proposed reviewed values in business terms, then call `reviews_updateNextResult` with the internal ID mapping. This tool preserves reporter values, writes reviewer fields, records an audit, and synchronizes the active KR. Reread `reviews_getContext` every one or two KRs.

If a positive-weight KR has no `resultNext`, stop and report the backend gap. Do not manufacture a replacement with reporter-side defaults. Zero-weight KRs do not require Next validation.

## 5. Reviewer note and closure

Keep the reviewer note extremely short and useful to the reporter. Include only:

- a brief summary of how the reviewed period went, mentioning measurement limitations only when they materially change the interpretation;
- what will change in the next operating period, focusing on priorities and expected behavior rather than internal workflow mechanics;
- the risks the reviewer confirmed as most important;
- when useful, a short mention of initiatives the reviewer added and the outcome they should produce.

Never include internal review mechanics such as assignee defaults, check-in cadence, whether an assignment message was sent, MCP or ClickHouse errors, record identifiers, tool outcomes, audit details, or payload fields. Those details may be shown separately to the reviewer when relevant, but they are not part of the message to the reporter.

Call `reviews_getCloseContext` immediately before proposing closure. Show completeness, effective weight total, performance score, recommended outcome, and every readable OTO candidate. Translate outcome labels into the user's language; in Italian use **sopra le aspettative**, **in linea con le aspettative**, and **sotto le aspettative** for `ABOVE_EXPECTATIONS`, `IN_LINE`, and `BELOW_EXPECTATIONS`. Keep the enum only for the internal `reviews_close` payload. Include every candidate exactly once with `stable`, `growing`, or `declining`; use the returned default only when the user has not stated another trajectory.

Show the exact final reviewer note, the translated selected outcome, and every other user-visible closure effect in one closure preview. Then ask a dedicated final question, such as “Confermi che devo inviare questa nota e chiudere il report con esito in linea con le aspettative?”, without exposing raw IDs or tool syntax. Stop and wait. Call `reviews_close` only after an unambiguous affirmative reply to that post-preview question. If the user selects an outcome different from the recommendation, record their reasoning in the reviewer note instead of silently changing it. After the call, report closure only from the tool result.

## Edge cases

Read [edge-cases.md](edge-cases.md) whenever context reports missing/untracked/removed records, zero or duplicate indicators, archived teams, incomplete or empty reports, truncation, an unexpected lifecycle state, or a closure error.

## Tool reference

Read [reference-mcp-tools.md](reference-mcp-tools.md) when constructing any review payload.
