# Level 7 / Project 05 - Polling Cadence Manager
Home: [README](../../../README.md)

## Focus
- collect interval planning and drift checks

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-7/05-polling-cadence-manager
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
1. Add a `jitter` parameter that adds random variation (e.g. +/- 10%) to the interval to prevent thundering herd.
2. Track and report the average interval across all polls in the simulation.
3. Re-run script and tests — verify jitter and average interval appear in output.

## Break it (required)
1. Set `backoff_factor` to 0 or negative and observe what happens to the interval.
2. Set `min_interval` greater than `max_interval` and run the simulation.
3. Capture the infinite loop or nonsensical interval values.

## Fix it (required)
1. Validate that `backoff_factor > 1.0` and `speedup_factor` is between 0 and 1.
2. Raise `ValueError` if `min_interval >= max_interval`.
3. Add tests for invalid config values and boundary conditions.

## Explain it (teach-back)
1. Why does exponential backoff reduce load on an unchanged data source?
2. What happened when backoff_factor was zero?
3. How did the validation prevent the runaway interval?
4. Where is adaptive polling used in real monitoring systems?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

## Mastery Check
- [ ] Can you explain the architectural trade-offs in your solution?
- [ ] Could you refactor this for a completely different use case?
- [ ] Can you identify at least two alternative approaches and explain why you chose yours?
- [ ] Could you debug this without print statements, using only breakpoint()?

---

## Related Concepts

- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [How Imports Work](../../../concepts/how-imports-work.md)
- [Types and Conversions](../../../concepts/types-and-conversions.md)
- [Quiz: Errors and Debugging](../../../concepts/quizzes/errors-and-debugging-quiz.py)

---

| [← Prev](../04-source-field-mapper/README.md) | [Home](../../../README.md) | [Next →](../06-token-rotation-simulator/README.md) |
|:---|:---:|---:|
