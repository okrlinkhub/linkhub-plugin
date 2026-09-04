# LinkHub MCP review tools

## Primary review tools

| Tool | Purpose |
| --- | --- |
| `reviews_getContext { reportId? \| reportSlug? }` | Complete reviewer snapshot, team leader, notes, KR/indicator details including each indicator's latest value and date, previous reports, untracked KRs, and readiness |
| `reviews_getAnalyzeContext { reportId }` | All positive-weight review KRs, with compact stable risk references `R1...`, initiative references `I1...`, period relation, and per-KR `highest` coverage in one call |
| `reviews_rebalanceRiskPriorities { reportId, changes[] }` | Atomic priority update for a confirmed risk group; rejects a final state that leaves any positive-weight KR without a `highest` risk |
| `reviews_rebalanceWeights { reportId, allocations[] }` | Atomic complete 100% weight confirmation/rebalance; changed rows require reviewer notes |
| `reviews_attachKeyResult { reportId, keyResultId, reviewerNotes }` | Attach an existing untracked active KR at zero, before a separately confirmed complete rebalance |
| `reviews_updateNextResult { resultNextId, forecastValueReviewed, targetValueReviewed, notes? }` | Reviewer-only Next validation with audit; preserves reported values |
| `reviews_getCloseContext { reportId }` | Final completeness, recommendation, and exact OTO candidates |
| `reviews_close { reportId, resultType, reviewerNotes?, videoReviewUrl?, otoCheckins? }` | IN_REVIEW → CLOSED_* after dedicated confirmation |

`allocations[]` items are `{ resultTrackedId, weightReviewed, reviewerNotes? }`. Include every active tracked result exactly once. Changed weights require `reviewerNotes`; unchanged weights may preserve existing reviewer notes by omitting the field. `trackedResults[].reporterNotes` and `trackedResults[].reviewerNotes` have distinct authors and must never be merged or copied into each other.

The Next tool keeps technical field names for transport, but the interview must always present them as `obiettivo minimo` and `obiettivo massimo`. Base the proposal on `keyResults[].indicator.latestValue` when present, even if the reviewed-period result is marked unmeasurable.

## Reused read tools

| Tool | Purpose |
| --- | --- |
| `mcp_membershipProfile` | Current MCP identity and company |
| `indicators_getExplanation` / `indicators_queryEvidence` | Mandatory definition plus bounded ClickHouse evidence before proposing Next values for every automated positive-weight KR; reuse results within the review |
| `milestones_listByIndicator` | Tool-returned milestone values and totals |

## Reused writes during Analyze

Use `risks_create`, `risks_update`, `risks_remove`, `initiatives_create`, `initiatives_update`, `initiatives_checkIn`, `initiatives_finish`, or `initiatives_remove` only after their complete user-visible effects have been shown in readable terms and confirmed. Prefer `reviews_rebalanceRiskPriorities` over several `risks_update` calls when applying the reviewer's final `highest` selection.

`initiatives_create` requires one active `riskId`. A reviewer-created initiative must name the selected stable risk reference in the readable proposal and explain how it mitigates that risk; never offer an unlinked initiative. If no suitable risk exists, create and confirm the risk first. Reviewer-created initiatives default to the `reviews_getContext.teamLeader` assignee and a 7-day check-in. Ask whether to include the standard assignment message; do not spend separate interview turns reconfirming those defaults.

When reviewing in an isolated sandbox, invoke the indicator evidence functions through that sandbox as well. Never switch to a production-connected MCP. A failed evidence operation is not retried with speculative parameters or a different environment.

`reviewerNotes` is a short business message to the reporter, not an audit log. Exclude assignee defaults, check-in dates, assignment-message status, internal IDs, payload details, and evidence-tool diagnostics.

## Do not use during review

- `reports_getAnalyzeContext`: reporter-oriented, one-KR-at-a-time Analyze context; use the aggregated reviewer tool instead.
- `keyResults_rebalanceWeightInDraftReport`: reporter DRAFT semantics.
- `resultTracked_upsert`, `resultTracked_markUnmeasurable`, `resultTracked_markCompleted`: reporter evaluation semantics.
- `resultNext_upsert`, `resultNext_skipWithDefaults`: overwrite or create reporter-side Next data.
- `reports_submit`: DRAFT submission, not review closure.
