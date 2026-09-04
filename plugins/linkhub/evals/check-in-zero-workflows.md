# LH Check-in Zero evaluation cases

## Positive cases

1. **Explicit risk context option** — Given a pending initiative with `teamId` and
   `riskId`, when the user chooses D the agent reads `keyResults_byTeam` with
   `limit: 200`, searches `risks_byKeyResult` with `limit: 200` until the exact
   risk ID is found, shows risk description, priority, and readable Key Result,
   then asks A/B/C again for the same initiative.
2. **Natural-language context request** — Given the agent is collecting a status,
   note, or date, a request such as “what risk does this mitigate?” triggers the
   same read-only lookup and resumes the interrupted initiative without changing
   its counter.
3. **No active linked risk** — Given a pending initiative whose `riskId` is null,
   the agent states that there is no active linked risk, makes no speculative
   lookup, and returns to A/B/C.
4. **Unverifiable or saturated inventory** — If the exact risk ID is absent, the
   agent says the current context cannot be verified. An exact 200-row KR or risk
   response without a match is explicitly treated as potentially saturated.

## Negative cases

1. A risk-context request never performs a check-in, finish, update, or other
   mutation and never consumes a pending initiative.
2. The agent never selects a risk by textual similarity or exposes internal risk,
   Key Result, or team IDs to the user.
3. The agent never presents an unmatched or incomplete risk inventory as the
   initiative's verified context.
