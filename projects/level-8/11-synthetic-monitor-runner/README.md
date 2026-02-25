# Level 8 / Project 11 - Synthetic Monitor Runner
Home: [README](../../../README.md)

## Focus
- Callable-based check definitions with factory pattern
- Scheduled execution of health checks with configurable intervals
- Check types: HTTP status, threshold comparison, pattern matching
- History tracking with trend analysis across check runs
- Structured reporting with overall health aggregation

## Why this project exists
Synthetic monitoring proactively detects outages by running scripted checks against your
system at regular intervals — before real users hit problems. Unlike real-user monitoring
that waits for complaints, synthetic checks continuously verify that login works, API
responses are fast, and databases are reachable. This project builds a monitor runner that
executes health checks, evaluates pass/fail criteria, tracks history for trend analysis,
and generates status reports — the same pattern used by Pingdom, UptimeRobot, and custom
health-check frameworks.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-8/11-synthetic-monitor-runner
python project.py --demo
pytest -q
```

## Expected terminal output
```text
{
  "overall_healthy": true,
  "checks_passed": 4,
  "checks_failed": 1,
  "results": [...]
}
7 passed
```

## Expected artifacts
- Console JSON output with check results and health summary
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `schedule_interval_seconds` field to `CheckDefinition` and implement periodic execution.
2. Add a `--tags` filter flag that runs only checks matching specified tags.
3. Add a `history` feature that stores the last N results per check for trend analysis.

## Break it (required)
1. Register a check with an unknown `check_type` — does the factory handle it gracefully?
2. Set a threshold check's expected value to `None` — what happens in comparison?
3. Mark a check as `critical=True` and make it fail — verify the report's `overall_healthy` flag.

## Fix it (required)
1. Add a default handler in the check factory for unknown check types.
2. Validate that threshold values are numeric in `CheckDefinition.__post_init__`.
3. Add a test that verifies critical check failure affects overall health status.

## Explain it (teach-back)
1. What are synthetic monitors and how do they differ from real-user monitoring?
2. How does the factory pattern let you add new check types without modifying existing code?
3. Why do checks have tags and how would you use them in a real monitoring system?
4. What is the difference between a health check and a smoke test?

## Mastery check
You can move on when you can:
- explain synthetic monitoring vs real-user monitoring and when to use each,
- add a new check type (e.g. DNS resolution) using the factory pattern,
- describe how check history enables trend detection and alerting,
- configure a monitoring suite for a real web service with appropriate thresholds.

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Async Explained](../../../concepts/async-explained.md)
- [Http Explained](../../../concepts/http-explained.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../10-dependency-timeout-matrix/README.md) | [Home](../../../README.md) | [Next →](../12-release-readiness-evaluator/README.md) |
|:---|:---:|---:|
