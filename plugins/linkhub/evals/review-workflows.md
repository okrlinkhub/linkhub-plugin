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
9. **Dedicated closure** — The agent rereads `reviews_getCloseContext`, shows recommendation, OTO candidates, and all user-visible effects, then asks separately for closure without exposing raw IDs.
10. **Empty report** — The agent permits only a separately acknowledged `BELOW_EXPECTATIONS` closure.
11. **Ownership before priority** — Before allocating the next period, the agent asks whether each KR still belongs to the team; transferred work is proposed at zero for that reason, not because the closed-period result was weak.
12. **Stable risk references** — The agent calls `reviews_getAnalyzeContext` once, shows `highest` risks as `R1`, `R2`, ... and correctly understands a reviewer reply such as “R2 non è più rilevante”.
13. **One highest per positive KR** — When the reviewer keeps only `R3` and `R6` and this would leave another positive-weight KR uncovered, the agent blocks advancement and asks which existing risk to promote or what new highest risk to create for that KR.
14. **Risk-linked initiative defaults** — A reviewer-created initiative is explicitly tied to one active numbered risk, explains the mitigation relationship, and is proposed for the returned team leader with a 7-day check-in; the agent asks only whether to include the exact standard assignment message before presenting the confirmed payload.
15. **Automatic demotion** — Once the reviewer selects the final `highest` risks, the agent shows every other current `highest` becoming `high` by reference and description, then one confirmation directly authorizes the atomic call without a second raw-payload prompt.
16. **Automated indicator evidence** — Before proposing Next values for an automated positive-weight KR, the agent reads its approved explanation and runs the reference-period `summary` plus `compare_previous_period`; it reports formula, material exclusions, evidence status, and only then makes a numerical proposal.
17. **Sandbox evidence boundary** — A review running on an isolated deployment evaluates the indicator through that deployment and never reads a production-connected LinkHub MCP.
18. **Reporter-focused closing note** — The proposed reviewer note briefly covers period outcome, next-period changes, confirmed principal risks, and only useful reviewer-added initiatives; it omits assignment mechanics, check-in cadence, message-delivery choices, tool errors, and internal identifiers.
19. **Current values in Next proposal** — Each Next proposal places the reviewed-period measurement, dated current operational value, reporter proposal, and reviewer proposal together; when no current value exists, it says so explicitly before asking for approval.
20. **Analyze decision before Next** — After weights, the agent shows current risks and initiatives for every positive-weight KR and recommends concrete changes or no change; it resolves the reviewer's decision and approved writes before discussing future Next values.
21. **Localized outcome** — For an Italian review, the closure preview says `sopra le aspettative`, `in linea con le aspettative`, or `sotto le aspettative`; the corresponding enum remains internal to the tool payload.
22. **Post-preview closure approval** — A reviewer says “procediamo, sarà in linea e stabile”; the agent drafts the exact note and closure preview, asks a new dedicated confirmation, and waits for the next affirmative reply before calling `reviews_close`.
23. **Neutral interval** — Given a positive-weight increasing KR that is not yet measurable in the next period and a reporter proposal of `0 / 0`, the agent explains that equal goals have no success interval, proposes obiettivo minimo `0` and obiettivo massimo `10`, and waits for confirmation before writing.

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
10. The agent never invents OTO candidates, evidence, reporter intent, or in-period completion.
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

## Pass criteria

- The first user-facing review content is a factual note-and-context briefing.
- The interview is one question at a time, uses the closed period as evidence, and validates priorities for the next operating period rather than retroactively reweighting performance.
- Every mutation uses a reviewer-specific tool or a separately confirmed Analyze tool.
- Non-empty closure requires 100% reviewed weight and both reviewed Next values for every positive-weight KR.
