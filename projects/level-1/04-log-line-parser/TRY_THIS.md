# Try This — Project 04

1. Add a "time gap" feature that shows the time between consecutive log entries. After parsing all entries, calculate the difference between each entry and the one before it, and print it next to the log line:
   ```text
   [INFO]    09:30:00  Server started              (---)
   [INFO]    09:30:05  Database connected           (+5s)
   [WARNING] 09:31:12  Slow query detected          (+67s)
   ```
   Hint: use `datetime.strptime()` to parse timestamps, then subtract to get a `timedelta`.

2. Add a `--search` flag that filters log entries by a keyword in the message. For example, `--search database` should show only entries whose message contains "database" (case-insensitive). Print the matching count at the end.

3. Add a severity-based color indicator using plain text markers. Print `[!!!]` next to ERROR entries, `[! ]` next to WARNING, and `[  ]` next to INFO. Then add a "health check" summary at the bottom:
   ```text
   Health: DEGRADED (1 error, 2 warnings in last 10 entries)
   ```
   If there are zero errors and warnings, print `Health: HEALTHY`.

---

| [← Prev](../03-unit-price-calculator/TRY_THIS.md) | [Home](../../../README.md) | [Next →](../05-csv-first-reader/TRY_THIS.md) |
|:---|:---:|---:|
