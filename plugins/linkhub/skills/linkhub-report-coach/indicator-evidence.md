# Indicator evidence protocol

Treat intervals as half-open: `startDate` inclusive and `endDate` exclusive. Copy dates from `referenceContext.referencePeriod`; do not infer them from the conversation.

The default evidence sequence is `summary` followed by `compare_previous_period`. If either call fails, omit its numerical conclusion. Describe only the relevant measurement limitation in simple words; never expose operation names or diagnostic codes to the user.

An empty `rows` array means “no evidence for this exact metric and interval”, not zero. `truncated: true` means the response is incomplete and must be described as incomplete in simple words.

Only keys listed in the explanation's approved measures and dimensions may be sent. Never provide SQL, table names, columns, relations, or free-form expressions.

For a different metric, search the authorized catalog first and pass the exact returned `namespace` and `metricKey` to the catalog evidence tool.
