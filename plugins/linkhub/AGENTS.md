# Distributed LinkHub plugin

These instructions apply to the plugin shipped to LinkHub users.

- Keep `.agents/skills` for developers of LinkHub and `plugins/linkhub/skills`
  for end-user workflows. Never copy repository release procedures into the
  distributed plugin.
- Treat each skill description as routing logic: state positive triggers and
  important near-miss exclusions concisely.
- Verify every referenced MCP tool against the current `.mcp.json`, tool
  reference, or connected server. Do not preserve obsolete tool names as prose.
- Read before writing. Mutations that create, update, submit, finish, or delete
  user data require the confirmations specified by the owning workflow.
- Never invent identifiers, indicator values, actuals, forecasts, evidence, or
  successful tool outcomes.
- Keep plugin evals aligned with skill behavior, including positive,
  contextual, and negative trigger cases. Exported and legacy copies must be
  generated through the existing scripts, not edited as independent sources.
