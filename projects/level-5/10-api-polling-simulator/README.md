# Level 5 / Project 10 - API Polling Simulator
Home: [README](../../../README.md)

> **Quick Recall:** This project uses rule-based scoring to decide when to retry or back off. Before starting, make sure you can: write a function that evaluates multiple conditions and returns a score or category based on thresholds (Level 1, Project 02 - Password Strength Checker).

## Focus
- poll cycles, retries, and delays

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-5/10-api-polling-simulator
python project.py --max-polls 10 --output data/poll_results.json
pytest -q
```

## Expected terminal output
```text
Polling complete: 10 attempts, 7 successful, 2 rate-limited
6 passed
```

## Expected artifacts
- `data/poll_results.json`
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `--timeout` flag that stops polling after N seconds regardless of max polls.
2. Track and report the average response time per successful poll.
3. Add a `--fail-rate` parameter to control the MockAPI's simulated failure percentage.
4. Re-run script and tests.

## Break it (required)
1. Set `--max-polls 0` and observe the behavior.
2. Configure the MockAPI to always return rate-limit errors and watch backoff grow indefinitely.
3. Capture the first failing test or visible bad output.

## Fix it (required)
1. Validate that max_polls is at least 1.
2. Cap the maximum backoff delay so it does not grow unbounded.
3. Add tests for zero-polls and capped backoff.
4. Re-run until output and tests are deterministic.

## Explain it (teach-back)
1. How does `poll_with_backoff` increase the delay after each rate-limit response?
2. What is the purpose of the `MockAPI` class in testing?
3. Why is exponential backoff better than fixed-interval polling?
4. Where do you see polling with backoff in production (AWS SDK, GitHub API, payment webhooks)?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Classes and Objects](../../../concepts/classes-and-objects.md)
- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Http Explained](../../../concepts/http-explained.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../09-template-report-renderer/README.md) | [Home](../../../README.md) | [Next →](../11-retry-backoff-runner/README.md) |
|:---|:---:|---:|
