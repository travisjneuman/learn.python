# Level 3 / Project 14 - Service Simulator
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | [Browser](../../../browser/level-3.html) |

<!-- modality-hub-end -->

**Estimated time:** 60 minutes

## Focus
- emulate service responses and failures

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-3/14-service-simulator
python project.py request --seed 42
python project.py load --count 100 --json
python project.py retry --max-retries 5 --seed 42
pytest -q
```

## Expected terminal output
```text
{"status_code": 200, "body": {"message": "OK"}, ...}
Load test: 100 requests
  200: 82
  429: 5
  500: 8
  504: 5
10 passed
```

## Expected artifacts
- Simulated responses on stdout
- Passing tests
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a `--failure-rate` flag to override the default error rate.
2. Add exponential backoff to the `retry_request` function (wait 2^attempt ms).
3. Add a `health` subcommand that checks if the service is "healthy" (3 consecutive 200s).

## Break it (required) — Core
1. Set `success_rate` to 0.0 — does `retry_request` exhaust all retries?
2. Run `load` with `--count 0` — what happens with zero requests?
3. Create a service with `--seed` and verify results are identical each run.

## Fix it (required) — Core
1. Add validation for rate parameters (must sum to <= 1.0).
2. Handle the zero-requests edge case in `run_load_test`.
3. Add a `--timeout` flag that limits total retry duration.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. What HTTP status codes mean 200, 429, 500, 504?
2. How does `random.Random(seed)` make tests deterministic?
3. What is retry logic and when should you retry vs. fail fast?
4. Why use a class (`SimulatedService`) instead of standalone functions?

## Mastery check
You can move on when you can:
- simulate service responses with configurable probabilities,
- implement retry logic with max attempts,
- use seed-based randomness for reproducible tests,
- understand HTTP status code categories.

---

## Related Concepts

- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [Http Explained](../../../concepts/http-explained.md)
- [Quiz: Errors and Debugging](../../../concepts/quizzes/errors-and-debugging-quiz.py)

---

| [← Prev](../13-quality-gate-runner/README.md) | [Home](../../../README.md) | [Next →](../15-level3-mini-capstone/README.md) |
|:---|:---:|---:|
