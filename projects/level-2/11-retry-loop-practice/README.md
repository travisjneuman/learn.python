# Level 2 / Project 11 - Retry Loop Practice
Home: [README](../../../README.md)

## Focus
- retry attempts with clear logging

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-2/11-retry-loop-practice
python project.py --operations 10 --failure-rate 0.6 --attempts 5
python project.py --operations 5 --failure-rate 0.9 --attempts 3
pytest -q
```

## Expected terminal output
```text
Simulating 10 operations (failure_rate=0.6, max_attempts=5)
  Operation 1: OK (attempts: 2)
  Operation 2: FAILED (attempts: 5)
  ...
=== Summary ===
9 passed
```

## Expected artifacts
- Retry simulation results on stdout
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `--jitter` flag that adds random variation to delay times.
2. Add a `--fail-fast` mode that stops all operations after the first failure.
3. Log each retry attempt with a timestamp.

## Break it (required)
1. Set `--failure-rate 1.0` — every operation should exhaust all attempts.
2. Set `--attempts 0` — what happens with zero allowed attempts?
3. Set `--delay -1` — negative delay makes no sense.

## Fix it (required)
1. Validate that max_attempts is at least 1.
2. Validate that delay is non-negative.
3. Add tests for edge-case configurations.

## Explain it (teach-back)
1. What is exponential backoff and why is it used?
2. Why catch specific exceptions instead of bare `except`?
3. What is a closure and how does `make_countdown_function` use one?
4. Where is retry logic essential in real systems (networks, APIs, databases)?

## Mastery check
You can move on when you can:
- implement retry with exponential backoff from memory,
- explain why backoff prevents "thundering herd" problems,
- describe the difference between flaky and deterministic test helpers,
- add jitter to a retry delay calculation.

---

## Related Concepts

- [Classes and Objects](../../../concepts/classes-and-objects.md)
- [Collections Explained](../../../concepts/collections-explained.md)
- [Decorators Explained](../../../concepts/decorators-explained.md)
- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Quiz: Classes and Objects](../../../concepts/quizzes/classes-and-objects-quiz.py)

---

| [← Prev](../10-mock-api-response-parser/README.md) | [Home](../../../README.md) | [Next →](../12-csv-to-json-converter/README.md) |
|:---|:---:|---:|
