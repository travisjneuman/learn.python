# Level 5 / Project 02 - Alert Threshold Monitor
Home: [README](../../../README.md)

**Estimated time:** 60 minutes

## Focus
- threshold logic and breach summaries

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-5/02-alert-threshold-monitor
python project.py --metrics data/metrics.json --thresholds data/thresholds.json --output data/alert_report.json
pytest -q
```

## Expected terminal output
```text
Alert evaluation: 3 breaches found
5 passed
```

## Expected artifacts
- `data/alert_report.json`
- Passing tests
- Updated `notes.md`

## Worked Example

Here is a similar (but different) problem, solved step by step.

**Problem:** Write a function that checks disk usage against thresholds and returns alerts.

**Step 1: Define thresholds as config.**

```python
THRESHOLDS = {
    "disk_usage_percent": {"warn": 80, "critical": 95},
    "memory_usage_percent": {"warn": 70, "critical": 90},
}
```

**Step 2: Write the evaluator.**

```python
def evaluate_metrics(current_values, thresholds):
    alerts = []
    for metric, value in current_values.items():
        if metric not in thresholds:
            continue
        t = thresholds[metric]
        if value >= t["critical"]:
            alerts.append({"metric": metric, "value": value, "severity": "CRITICAL"})
        elif value >= t["warn"]:
            alerts.append({"metric": metric, "value": value, "severity": "WARNING"})
    return alerts
```

**Step 3: Test it.** `evaluate_metrics({"disk_usage_percent": 96}, THRESHOLDS)` returns one CRITICAL alert. `{"disk_usage_percent": 50}` returns no alerts.

**The thought process:** Check the most severe condition first (critical before warn). Skip metrics without thresholds. Return structured alerts. This is the same pattern the threshold monitor uses.

## Design First
Before writing code, sketch your approach in `notes.md`:
- What functions or classes do you need?
- What data structures will you use?
- What's the flow from input to output?
- What could go wrong?

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. What feature would reduce alert noise in a real monitoring system? Implement it.
2. Can you add a finer-grained severity level?
3. Improve the logging to capture more context per breach.

## Break it (required) — Core
1. What happens when the configuration itself is invalid or contradictory?
2. What if expected data is missing from the metrics input?
3. Find the first failure and capture it.

## Fix it (required) — Core
1. Add validation for the configuration issue you found.
2. Handle missing data gracefully rather than crashing.
3. Write tests for the broken cases and re-run until deterministic.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. Why is cooldown important in production alerting systems?
2. What happens if thresholds are misconfigured in a real monitoring stack?
3. How does `check_threshold` decide between warn, crit, and ok?
4. How would this pattern apply to monitoring dashboards or PagerDuty-style alerting?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Classes and Objects](../../../concepts/classes-and-objects.md)
- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [Quiz: Classes and Objects](../../../concepts/quizzes/classes-and-objects-quiz.py)

---

## Stuck? Ask AI

If you are stuck after trying for 20 minutes, use one of these prompts:

- "I am working on Alert Threshold Monitor. I got this error: [paste error]. Can you explain what this error means without giving me the fix?"
- "I am trying to implement threshold logic with warn and critical levels. Can you explain how to structure threshold comparisons so the most severe match wins?"
- "Can you explain what a 'cooldown' period means in alerting systems and why it is important?"

---

| [← Prev](../01-schedule-ready-script/README.md) | [Home](../../../README.md) | [Next →](../03-multi-file-etl-runner/README.md) |
|:---|:---:|---:|
