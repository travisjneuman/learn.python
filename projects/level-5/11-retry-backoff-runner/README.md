# Level 5 / Project 11 - Retry Backoff Runner
Home: [README](../../../README.md)

## Focus
- exponential backoff strategy practice

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-5/11-retry-backoff-runner
python project.py --max-retries 5 --base-delay 0.1 --output data/retry_report.json
pytest -q
```

## Expected terminal output
```text
Success after 3 retries (total delay: 0.7s)
5 passed
```

## Expected artifacts
- `data/retry_report.json`
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add jitter to the backoff delay (random variation) to prevent thundering-herd behavior.
2. Add a `--max-retries` flag that overrides the default retry count from the command line.
3. Log each retry attempt with the delay duration and the error that triggered it.
4. Re-run script and tests.

## Break it (required)
1. Set `--max-retries 0` so no retries are allowed and the flaky function always fails.
2. Set `--base-delay` to a negative number.
3. Capture the first failing test or visible bad output.

## Fix it (required)
1. Validate that max_retries >= 1 and base_delay > 0.
2. Return a clear error report when all retries are exhausted.
3. Add tests for zero retries and negative delay.
4. Re-run until output and tests are deterministic.

## Explain it (teach-back)
1. How does exponential backoff calculate the delay for each retry attempt?
2. Why does `create_flaky_function` use a counter to simulate intermittent failures?
3. What is jitter and why does it prevent thundering-herd problems?
4. Where do you see retry with backoff in production (AWS SDK, HTTP clients, message queues)?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Classes and Objects](../../../concepts/classes-and-objects.md)
- [Decorators Explained](../../../concepts/decorators-explained.md)
- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Types and Conversions](../../../concepts/types-and-conversions.md)
- [Quiz: Classes and Objects](../../../concepts/quizzes/classes-and-objects-quiz.py)

---

| [← Prev](../10-api-polling-simulator/README.md) | [Home](../../../README.md) | [Next →](../12-fail-safe-exporter/README.md) |
|:---|:---:|---:|
