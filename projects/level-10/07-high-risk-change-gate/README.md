# Level 10 / Project 07 - High Risk Change Gate
Home: [README](../../../README.md)

## Focus
- Weighted risk scoring pipeline with pluggable factors
- Gate policy enforcement (auto-approve, review, block)
- Immutable change request modeling
- Rollback detection as a risk reducer

## Why this project exists
Production incidents often stem from changes deployed without proportionate review. This system quantifies risk with multiple weighted factors and enforces proportionate gates: small doc fixes auto-approve, while schema migrations to three services get blocked until multiple reviewers sign off.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-10/07-high-risk-change-gate
python project.py
pytest -v
```

## Expected terminal output
```text
{"change_id": "CHG-001", "risk_level": "LOW", "decision": "approved", ...}
{"change_id": "CHG-002", "risk_level": "HIGH", "decision": "needs_review", ...}
```

## Alter it (required)
1. Add a `TimeOfDayFactor` that scores higher for deployments during peak traffic hours.
2. Add an override mechanism: certain users (e.g., "oncall-lead") can bypass the gate with an audit trail.
3. Re-run tests and verify the new factor integrates into the scoring pipeline.

## Break it (required)
1. Create a change that hits every risk factor — observe how scores accumulate to CRITICAL.
2. Register no factors and observe a zero-score auto-approval for a clearly risky change.
3. Set `is_rollback=True` with many other risk factors and see if it still reduces risk.

## Fix it (required)
1. Add a minimum-score floor per factor type so rollback alone cannot bring risk to zero for a critical change.
2. Require at least one factor registered before `evaluate` can be called.
3. Add tests for both safeguards.

## Explain it (teach-back)
1. Why is risk quantified as a numeric score rather than a categorical label?
2. How does the `RollbackFactor` negative score interact with the floor at zero?
3. What is the relationship between risk level and the number of required approvers?
4. How would you integrate this gate into a CI/CD pipeline?

## Mastery check
You can move on when you can:
- add a custom risk factor and see it reflected in the gate decision,
- explain the risk level thresholds and why they map to specific policies,
- trace how a rollback reduces total risk score,
- describe why immutable `ChangeRequest` prevents accidental mutation.

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Async Explained](../../../concepts/async-explained.md)
- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Functions Explained](../../../concepts/functions-explained.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../06-resilience-chaos-workbench/README.md) | [Home](../../../README.md) | [Next →](../08-zero-downtime-migration-lab/README.md) |
|:---|:---:|---:|
