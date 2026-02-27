# Try This — Project 10

1. Add a `--stats` flag that prints a summary of the routing results as percentages:
   ```text
   Priority Distribution:
     CRITICAL:  10%  (1 ticket)
     HIGH:      20%  (2 tickets)
     MEDIUM:    40%  (4 tickets)
     LOW:       30%  (3 tickets)
   ```
   Hint: divide each queue's count by the total number of tickets and multiply by 100.

2. Add a "keyword highlight" feature. When printing each ticket, bold or uppercase the keyword that triggered its classification. For example, if `"crash"` matched the critical category, show:
   ```text
   [CRITICAL] #1: The website CRASH-ed and customers cannot access...
   ```
   Hint: in `classify_ticket()`, return both the priority and the matched keyword so the display code knows what to highlight.

3. Add a second classification method: score-based routing. Instead of picking the first matching priority, give each keyword a point value (critical keywords = 4 points, high = 3, medium = 2, low = 1). A ticket that matches multiple keywords adds up all the points, and the final priority is based on the total score. Compare the results to the keyword-first method and print any tickets that would be classified differently.

---

| [← Prev](../09-json-settings-loader/TRY_THIS.md) | [Home](../../../README.md) | [Next →](../11-command-dispatcher/TRY_THIS.md) |
|:---|:---:|---:|
