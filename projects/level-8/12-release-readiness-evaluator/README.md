# Level 8 / Project 12 - Release Readiness Evaluator
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus
- Weighted scoring with configurable criteria and weights
- Strategy pattern for pluggable evaluation functions
- Three-tier readiness: GO, CONDITIONAL, NO_GO
- Required criteria that force NO_GO regardless of score
- Structured reporting with per-criterion pass/fail detail

## Why this project exists
Shipping software requires checking many gates: test coverage, linting, security scans,
documentation, and changelog entries. A manual checklist is error-prone and slows down
releases. This project builds a configurable readiness evaluator that scores a release
candidate against weighted criteria and produces a go/no-go decision — the same pattern
used in CI/CD release gates at companies like Google, GitHub, and Spotify.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-8/12-release-readiness-evaluator
python project.py --demo
pytest -q
```

## Expected terminal output
```text
{
  "version": "v2.1.0",
  "readiness": "GO",
  "score": 87.5,
  "criteria": [...]
}
7 passed
```

## Expected artifacts
- Console JSON output with readiness evaluation
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `documentation_criterion` factory that checks if README/CHANGELOG are updated.
2. Change the `EvaluatorConfig` thresholds to be configurable via CLI flags.
3. Add a `--verbose` flag that prints each criterion's score and pass/fail status.

## Break it (required)
1. Add a criterion with `weight=0` — does the weighted score calculation handle it?
2. Set `go_threshold` lower than `conditional_threshold` — what readiness level results?
3. Pass no criteria at all — does `evaluate()` return a valid report?

## Fix it (required)
1. Validate that `go_threshold >= conditional_threshold` in `EvaluatorConfig`.
2. Add a guard for `total_weight == 0` to avoid division by zero.
3. Add a test for overlapping threshold values.

## Explain it (teach-back)
1. How does weighted scoring differ from simple pass/fail gating?
2. Why are some criteria marked `required=True` — what does that override?
3. What is the difference between GO, CONDITIONAL, and NO_GO readiness levels?
4. How do real CI/CD pipelines implement release gates similar to this evaluator?

## Mastery check
You can move on when you can:
- explain weighted scoring and how criterion weights affect the overall score,
- add a new criterion factory end-to-end (definition + evaluation + test),
- describe the three readiness levels and when CONDITIONAL is appropriate,
- design a release gate for a real project with appropriate criteria and weights.

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Async Explained](../../../concepts/async-explained.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [Http Explained](../../../concepts/http-explained.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../11-synthetic-monitor-runner/README.md) | [Home](../../../README.md) | [Next →](../13-sla-breach-detector/README.md) |
|:---|:---:|---:|
