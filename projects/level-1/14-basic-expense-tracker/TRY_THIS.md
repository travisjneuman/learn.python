# Try This — Project 14

1. Add a `--month` filter that shows expenses for a specific month only. For example, `--month 2024-01` should show only January 2024 expenses and their category totals. Compare the filtered total to the overall total and show a percentage:
   ```text
   January 2024: $145.00 (23% of all-time total)
   ```
   Hint: compare the start of each expense's date string with the `--month` value using `date.startswith()`.

2. Add a "budget vs actual" feature. Create a simple budget dict at the top of the file (e.g., `BUDGET = {"food": 200, "transport": 100, "entertainment": 50}`). After computing category totals, compare each category to its budget and flag overspending:
   ```text
   Category       Budget    Actual    Status
   food           $200.00   $185.50   Under budget ($14.50 remaining)
   transport      $100.00   $135.00   OVER BUDGET by $35.00!
   entertainment  $50.00    $42.00    Under budget ($8.00 remaining)
   ```

3. Add a daily spending trend. Group expenses by date, compute the daily total, and print a simple text chart showing spending over time:
   ```text
   2024-01-01  $25.00  #####
   2024-01-02  $12.50  ###
   2024-01-03  $45.00  #########
   2024-01-04  $0.00
   2024-01-05  $8.50   ##
   ```
   Hint: use a dictionary to group expenses by date, then find the max daily total to scale the `#` bars.

---

| [← Prev](../13-batch-rename-simulator/TRY_THIS.md) | [Home](../../../README.md) | [Next →](../15-level1-mini-automation/TRY_THIS.md) |
|:---|:---:|---:|
