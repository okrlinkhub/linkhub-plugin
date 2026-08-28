# Review edge cases

## Lifecycle and authorization

- `DRAFT`: stop and route report completion to `linkhub-report-coach`.
- `IN_REVIEW`: normal review workflow.
- `CLOSED_*`: read-only explanation unless the user separately asks an authorized admin to reopen it; this skill does not reopen reports.
- Caller is neither assigned reviewer nor company admin: stop. Never substitute another user ID.
- Archived team: historical reads remain valid. Weight and Next writes must not mutate active KR state; adding a new KR is not allowed.

## Snapshot completeness

- Any `potentiallyTruncated: true`: fail closed. Do not confirm weights, risks, or closure from an incomplete set.
- Missing `resultNext` for a positive-weight tracked result: report the exact KR and stop before closure.
- Untracked active KR: explain that it is outside the submitted report snapshot. If the reviewer wants it to govern the next period, show and confirm `reviews_attachKeyResult` first; it enters at zero, then requires a separately confirmed complete rebalance. Do not use reporter-side result creation.
- Removed or missing KR with positive proposed weight: stop. A historical snapshot may be set to zero, but an active replacement requires a deliberate product decision.

## Weights

- Verify next-period team ownership before discussing relative priority. Work transferred outside the team should normally receive zero, with a forward-looking ownership rationale; do not mislabel it as poor performance or mere stabilization.
- Send every active tracked result once in `reviews_rebalanceWeights`, including unchanged rows.
- Weights must be finite, between 0 and 100, multiples of 5, and total exactly 100.
- Validate those constraints before showing the proposal, not only before the write. Report an inherited non-multiple accurately as current state, but never repeat it as a proposed value.
- Every changed weight needs a non-empty, forward-looking rationale tied to priority before the next report, not merely to the observed result in the closed period.
- Duplicate positive-weight indicators are invalid. Do not work around the backend by splitting calls.
- A zero weight automatically marks its Next result as removed. Highlight this before confirmation.

## Evidence and dates

- `cannotMeasureAt` means the report did not establish a measurable actual; zero-valued storage fields are not evidence of zero performance.
- Auto-submitted notes describe system behavior, not the reporter's judgment.
- Compare `finishedAt` and note dates with `trackingDate`. Label later work as post-period follow-up.
- Past results and risks inform the interview, but `weightReviewed` governs the active KR allocation for the next operating period; never describe it as rewriting the closed period.
- An empty evidence response is unavailable evidence, never zero.

## Highest-risk coverage

- Every positive-weight KR must retain at least one active `highest` risk before Next validation.
- A proposal that demotes the last `highest` risk of a KR is incomplete until another existing risk is promoted or a new `highest` risk is explicitly confirmed for that KR.
- Zero-weight KRs are excluded from this coverage requirement because they are outside the active next-period allocation.

## Empty and incomplete reports

- A genuinely empty report may close only as `BELOW_EXPECTATIONS`, after the user explicitly acknowledges that no KR was reviewed.
- Any non-empty review with unreviewed weights, missing reviewed forecast/target, or total other than 100 must not close.
- A zero-weight KR is complete without Next validation; every positive-weight KR requires both reviewed Next values.

## Closure

- Call `reviews_getCloseContext` again after any later write.
- A close-context approval is not authorization to close. Neither is an earlier “procediamo”, a stated preferred outcome, a request to draft the note, or approval of another write group.
- Show the exact final note, translated outcome label, and all user-visible closure effects first. Only an unambiguous affirmative answer to the dedicated question asked after that preview authorizes `reviews_close`.
- Include all and only returned OTO candidates once. Never invent a candidate or answer outside `stable`, `growing`, `declining`.
- Use either reviewer text notes or a valid Loom share URL as appropriate; never invent or normalize a video URL yourself.
