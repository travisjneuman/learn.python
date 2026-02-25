# Level 7 / Project 02 - Monitoring API Adapter
Home: [README](../../../README.md)

## Focus
- api call abstraction and result normalization

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-7/02-monitoring-api-adapter
python project.py --input data/sample_input.txt --output data/output_summary.json
pytest -q
```

## Expected terminal output
```text
... output_summary.json written ...
2 passed
```

## Expected artifacts
- `data/output_summary.json`
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `network_latency` metric adapter that returns latency in milliseconds.
2. Add a `severity` field to alerts (info / warning / critical) based on how far above threshold the value is.
3. Re-run script and tests — verify new metric and severity appear in output.

## Break it (required)
1. Set a threshold to a negative number and observe what alerts are generated.
2. Return a non-numeric value from a mock API (e.g. `"N/A"`) and watch the comparison fail.
3. Capture the TypeError or unexpected alert behavior.

## Fix it (required)
1. Validate that thresholds are positive before comparing.
2. Wrap metric values in a `float()` cast with a try/except to handle non-numeric responses.
3. Add a test for non-numeric metric values and negative thresholds.

## Explain it (teach-back)
1. Why does each metric type need its own adapter function?
2. What happened when the mock API returned a string instead of a number?
3. How did input validation prevent the false alert?
4. How would you extend this to a real Prometheus or Datadog integration?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [How Imports Work](../../../concepts/how-imports-work.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../01-api-query-adapter/README.md) | [Home](../../../README.md) | [Next →](../03-unified-cache-writer/README.md) |
|:---|:---:|---:|
