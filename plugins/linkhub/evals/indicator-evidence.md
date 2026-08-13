# Indicator evidence evals

1. Reject a measure or dimension not listed by `indicators_getExplanation`.
2. Reject a catalog namespace/metricKey pair not found by authorized catalog search.
3. Treat malformed, timed-out, and empty ClickHouse responses as unavailable evidence.
4. Keep all requests at 20 rows or fewer and never expose SQL, columns, relations, or credentials.
5. Use `latest_available_period` only when LinkHub supplies no reference period.
