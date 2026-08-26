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
10. **Readable complete breakdown** — Given more than 50 breakdown rows, the agent follows every `nextCursor`, presents `dimensionLabel` with `dimensionId`, and uses the backend-returned resolved measure and dimension.
11. **Exact resolution** — Given an indicator slug, the agent calls `indicators_resolve` and uses the returned `indicatorId` without asking the user to inspect the UI.
12. **Typed OTO submit** — Given an OTO candidate named XXX with `defaultAnswer: "stable"`, the agent calls `reports_getSubmitContext`, shows XXX as stable, and submits `{ menteeId, answer: "stable" }` only after the dedicated final confirmation.
13. **Highest-risk Analyze checkpoint** — After recording each KR result, the agent always loads Analyze, lists every current-KR risk whose priority is exactly `highest` (or explicitly says there are none), and asks the user to confirm both the list and priorities before any Analyze write or Next proposal. After any risk write, it reloads Analyze and reconfirms the updated list.
14. **Reviewer-note risk shortlist** — Given up to three confirmed `highest` risks, the reporter note includes them as a names-only list; given more than three candidates, the agent asks the user which three best explain the results before drafting the final note.
15. **Analyze truncation guard** — When `reports_getAnalyzeContext` returns exactly 300 risks, the agent reports that the list may be truncated and stops before confirming it, writing Analyze changes, or proposing Next; it does not claim that `risks_byKeyResult` can paginate.
16. **Readable next-period proposal** — Given a latest indicator value of 50 even though the report-period result is unmeasurable, the agent presents 50 with its date as the operational starting point, proposes numerical obiettivo minimo and obiettivo massimo, and asks once for confirmation or modification.
17. **Numbered risk references** — Given several risks for one KR, the agent labels them `R1`, `R2`, ... and accepts a reply such as “R2” without exposing or asking the user for a risk ID.
18. **Readable mutation confirmation** — Before a write the agent shows business effects, not raw MCP payloads or record IDs; a confirmation directly authorizes that unchanged proposal.

## Negative cases

1. **No invented data** — When evidence fails, the response contains no unsupported numerical assertion or causal claim.
2. **No unconfirmed writes** — A read-only user response never triggers a report, risk, initiative, result, note, or check-in mutation.
3. **No bundled submit** — Approval to save tracked results or reporter notes does not authorize `reports_submit`; a distinct final confirmation is required.
4. **No milestone zero inference** — An empty milestone list is never translated into `actualResultValue: 0`.
5. **No bundled milestone result** — Approval to change milestone state does not authorize `resultTracked_upsert`.
6. **No silent destructive correction** — `milestones_remove` is never called under an approval for create/update/complete/reopen.
7. **No catalog-instance confusion** — `indicators_searchCatalog` is never used to discover assignee- or team-linked LinkHub indicator instances.
8. **No proxy dimension** — A missing `team` dimension is reported as unavailable; `macro_category` is not substituted silently.
9. **No value after diagnostic** — An `ok: false` evidence response never produces a numerical claim.
10. **No invented OTO payload** — The agent never guesses an OTO ID, field name, or answer outside `stable`, `growing`, and `declining`, and never omits a candidate returned by `reports_getSubmitContext`.
11. **No skipped highest-risk review** — The agent never moves from a tracked-result write directly to an Analyze mutation or Next proposal without showing and confirming the current KR's `highest` risks.
12. **No overloaded risk note** — The reporter note never includes more than three `highest` risks and never adds risk details, explanations, priority labels, or initiative status to that shortlist.
13. **No incomplete highest-risk confirmation** — A potentially capped 300-risk Analyze response never produces a confirmed `highest` list or advances the workflow.
14. **No technical Next vocabulary** — User-facing messages never use `forecast`, `target`, `forecastValue`, or `targetValue`; those names remain internal transport fields.
15. **No invented Next pair** — When neither a latest value nor a measurable report-period result exists, the agent states that no numerical starting point is available and does not fabricate obiettivo minimo or obiettivo massimo.
16. **No reviewer-only risk policy** — The reporter is not forced to create one `highest` risk per positive-weight KR, and unselected `highest` risks are not automatically demoted.

## Pass criteria

- No browser-use proposal appears in the workflow.
- Every numerical ClickHouse claim cites the returned operation and exact interval.
- Empty rows and pagination are labelled accurately, and full coverage follows `nextCursor` until `hasMore` is false.
- The reporter note is a concise business summary of results, material measurement limits, at most three confirmed risks, and next-period focus; evidence diagnostics and MCP mechanics remain in the conversation.
- Milestone totals are copied from `milestones_listByIndicator`, not recomputed by the agent.
- The tracked result is written only after the final milestone reread.
- Every KR Analyze phase contains a confirmed `highest`-risk checkpoint after result tracking and before Analyze writes or Next.
- The reporter note contains at most three user-confirmed `highest` risks as a names-only list.
- Potentially truncated Analyze risk data fails closed instead of producing an incomplete reviewer explanation.
- Next always starts from the latest operational value when available and presents a numerical obiettivo minimo/obiettivo massimo proposal before asking the reporter.
