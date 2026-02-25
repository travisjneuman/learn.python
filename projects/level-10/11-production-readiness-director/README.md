# Level 10 / Project 11 - Production Readiness Director
Home: [README](../../../README.md)

## Focus
- Checklist-driven readiness evaluation with categorical checks
- Go/No-Go/Conditional decision logic with configurable thresholds
- Immutable service manifest describing production preparedness
- Category-grouped results (observability, reliability, security, operations)

## Why this project exists
Launching a service without checking readiness leads to incidents. This project codifies the readiness review as executable checks, giving teams consistent evaluation and a clear audit trail of what was verified before production.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-10/11-production-readiness-director
python project.py
pytest -v
```

## Expected terminal output
```text
{
  "service": "payment-service",
  "decision": "conditional_go",
  "pass_rate": "88%",
  ...
}
```

## Alter it (required)
1. Add a `BackupCheck` and `SLACheck` that evaluate the corresponding manifest fields.
2. Add weighted categories — security failures should block launch regardless of pass rate.
3. Add an override mechanism where a VP can force a "go" decision with an audit trail.

## Break it (required)
1. Create a `ServiceManifest` with all fields `False` and observe the NO_GO decision.
2. Set thresholds to zero and watch every service get auto-approved regardless of readiness.
3. Register no checks and observe a 0% pass rate.

## Fix it (required)
1. Add a minimum check count requirement — `evaluate` should fail if fewer than 3 checks are registered.
2. Make security checks "hard blockers" that always produce NO_GO on failure.
3. Test both safeguards.

## Explain it (teach-back)
1. Why is the service manifest immutable (frozen dataclass)?
2. How does the three-tier decision system (go/conditional/no-go) help operations teams?
3. Why are checks categorized — what does grouping by observability/reliability/security enable?
4. How would you integrate this into a CI/CD pipeline?

## Mastery check
You can move on when you can:
- add a new ReadinessCheck and register it in the director,
- explain the threshold-based decision logic,
- create a manifest that produces a CONDITIONAL_GO decision,
- describe how Google and Netflix approach production readiness reviews.

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Async Explained](../../../concepts/async-explained.md)
- [Collections Explained](../../../concepts/collections-explained.md)
- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../10-executive-metrics-publisher/README.md) | [Home](../../../README.md) | [Next →](../12-onboarding-accelerator-system/README.md) |
|:---|:---:|---:|
