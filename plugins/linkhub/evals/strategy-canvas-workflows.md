# Strategy Canvas workflow evals

## Positive cases

1. **Single sufficient KR** — The facilitator starts with one KR, confirms that
   it proves the Objective, uses it as the lead KR, and does not solicit extras.
2. **Three distinct KRs** — The facilitator accepts up to three distinct outcome
   measures, requires one explicit lead KR, and links all three risks only to it.
3. **Optional KPI** — A risk without a measurable early-warning signal is
   exported with `kpi: null`; another risk can include a confirmed threshold.
4. **Initiative prioritization** — Each risk has one to three confirmed,
   action-oriented initiatives and no fourth initiative is added to the Canvas.
5. **Dual export** — One confirmed canonical payload produces a human-readable
   Markdown handoff and a one-page A4 landscape PDF with equivalent content.
6. **Creation handoff** — The final message explains that a later
   `linkhub-strategy-coach` session can create records for the existing team and
   that indicators still need valid LinkHub selections.

## Negative cases

1. The skill never calls a LinkHub MCP write tool or claims records were created.
2. It never invents a target, date, threshold, indicator, initiative, or ID.
3. It never accepts more than three KRs, fewer or more than three risks, or more
   than three initiatives per risk.
4. It never links a risk to a complementary non-lead KR.
5. It never turns an activity such as “publish posts” into a KR without an
   outcome measure.
6. It never silently truncates overflowing PDF content; it requests confirmed
   shorter wording and regenerates from the revised canonical payload.
7. It never exports before showing the complete Canvas and receiving a dedicated
   final confirmation.

## Pass criteria

- The conversation teaches Objective, KR, risk, KPI, and initiative distinctions
  before asking the corresponding workshop question.
- The JSON satisfies `linkhub-strategy-canvas/v1` and is the single source for
  both outputs.
- The PDF is one A4 landscape page and every visible business value also appears
  in the Markdown.
- The Markdown contains no platform IDs and makes the later creation boundary
  explicit.
