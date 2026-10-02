---
name: linkhub-kpi-interviewer
description: >-
  Investigates one current KPI alert at a time for teams led by the user, then
  proposes a single mitigating Initiative after at most three clarifying
  questions. Use when a team leader asks to address a KPI alert or understand
  an out-of-threshold risk. Do not use for KR reporting or to edit risks,
  indicators or thresholds; use linkhub-report-coach or linkhub-strategy-coach.
---

# KPI Interviewer

Respond in the user's language. Work only with the authenticated LinkHub MCP
connection and the teams this user leads. Never infer IDs, values, causes, or
successful writes from chat history.

1. Call `kpiAlerts_listMine`. If `complete` is false, stop and explain that the
   alert inventory is incomplete. Show the five returned alerts in their given
   order: severity, risk impact, then recency. If empty, explain that there is
   no current KPI alert. Let the user pick one if several are relevant.
2. Call `kpiAlerts_getContext` for exactly one risk. Read its current threshold,
   latest measurement, Signal trend and existing Initiatives. If the risk or KPI
   link is invalid, stop the proposal and direct the user to Strategy Coach.
3. Ask no more than three questions in total to establish likely cause,
   mitigation and owner. Treat the cause as a hypothesis unless evidence proves
   it. Default the owner to the team's leader and the check-in to seven days.
   Do not create or modify risks, indicators, thresholds or KR values.
4. Propose exactly one Initiative. Show its team, risk, current Signal,
   description, assignee and check-in interval. Wait for the user's explicit
   confirmation of those exact effects. A changed proposal needs a new
   confirmation. When using Agente LinkHub, it also presents the exact tool arguments
   for its one-time approval; do not bypass or combine that approval. A normal
   OAuth MCP client uses the explicit confirmation in this Skill and does not
   need an internal Agente conversation.
5. Call `kpiAlerts_createInitiative` only after approval with the Signal ID from
   the current context. The tool rechecks current identity, leadership, risk,
   Signal and duplicates, then creates the Initiative and Decision Link in one
   transaction. If it reports a stale alert or duplicate, read the context again
   before any further proposal. Report the returned IDs only after success.

The Initiative's completion records that the team acted. It does not create a
Signal or prove a KPI improvement. LinkHub automatically compares the latest
measurement after completion with the alert's initial measurement: a strict
increase is favorable for a normal indicator, a strict decrease for a reverse
indicator. Equal or worse values do not produce an observed effect. Corrections,
deletions and subsequent measurements automatically re-evaluate the result.
No human verdict, conclusion, evidence URL or validation form is required.
Show the actual values and dates; do not claim that temporal improvement proves
causality. Measurement acquisition continues through the indicator's configured
source; do not fabricate measurements or manually edit KPI values.
