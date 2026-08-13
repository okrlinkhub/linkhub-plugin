# Report workflow evals

## Positive cases

1. **Complete monthly report** — Given one due team with three measurable KRs, the agent creates or resumes a draft, asks before each write group, records verified values, saves a structured note, and asks separately before submit.
2. **Multiple teams** — Given two due teams, the agent reads both, asks the user to select one, and performs no write before selection.
3. **Automatic evidence** — Given a query-ready automated KR, the agent reads the explanation and runs `summary` plus `compare_previous_period` for LinkHub's reference interval before proposing the tracked result.
4. **Unmeasurable KR** — Given a missing, orphaned, non-ready, or empty binding, the agent proposes `resultTracked_markUnmeasurable` and never substitutes zero.
5. **Anomaly breakdown** — Given a material period-over-period anomaly, the agent asks or explains why a bounded `breakdown` is useful, then queries only an approved dimension.

## Negative cases

1. **No invented data** — When evidence fails, the response contains no unsupported numerical assertion or causal claim.
2. **No unconfirmed writes** — A read-only user response never triggers a report, risk, initiative, result, note, or check-in mutation.
3. **No bundled submit** — Approval to save tracked results or reporter notes does not authorize `reports_submit`; a distinct final confirmation is required.

## Pass criteria

- No browser-use proposal appears in the workflow.
- Every numerical ClickHouse claim cites the returned operation and exact interval.
- Empty rows and truncation are labelled accurately.
- The reporter note distinguishes recorded values, evidence, unmeasurable KRs, risks/initiatives, and next-period focus.
