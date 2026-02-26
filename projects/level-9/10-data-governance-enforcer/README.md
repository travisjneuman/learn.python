# Level 9 / Project 10 - Data Governance Enforcer
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus
- Data classification taxonomy: public, internal, confidential, restricted
- Retention policy enforcement with min/max retention periods
- Access control matrix mapping roles to classification levels
- Policy engine with composable rule evaluation
- PII handling requirements tied to classification and purpose

## Why this project exists
Data governance ensures that data is classified, retained appropriately, and accessed only
by authorized roles. Without governance, sensitive customer data leaks through analyst
exports, logs retain PII indefinitely, and intern accounts access production databases.
This project builds a policy engine for data governance — classifying data assets, enforcing
retention windows, and validating access requests against role-based policies. These are
the same patterns used in GDPR/CCPA compliance systems at every regulated organization.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-9/10-data-governance-enforcer
python project.py --demo
pytest -q
```

## Expected terminal output
```text
{
  "assets": 4,
  "retention_violations": [...],
  "access_decisions": [...],
  "compliance_summary": {...}
}
7 passed
```

## Expected artifacts
- Console JSON output with governance enforcement results
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add an `encryption_required` check — CONFIDENTIAL and RESTRICTED assets should require encryption.
2. Add an audit log that records all access evaluations (granted and denied).
3. Add a `--report` flag that outputs the full compliance summary as formatted JSON.

## Break it (required)
1. Register an asset with a classification not covered by any retention policy — what happens?
2. Request access with a role that has no access policy defined — what error occurs?
3. Set `min_retention_days > max_retention_days` in a `RetentionPolicy` — does validation catch it?

## Fix it (required)
1. Add validation that `min_retention_days <= max_retention_days` in `RetentionPolicy.__post_init__`.
2. Return a clear warning when an asset's classification has no retention policy.
3. Add a test for the missing retention policy case.

## Explain it (teach-back)
1. What is data classification (PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED) and why does it matter?
2. How does the access control matrix map roles to allowed classification levels?
3. Why does PII access require a stated purpose — what regulation drives this?
4. How do real organizations implement data governance for GDPR/CCPA compliance?

## Mastery check
You can move on when you can:
- explain data classification levels and give examples of each,
- add a new access policy role with specific permissions,
- describe how retention policies prevent both premature deletion and data hoarding,
- explain the relationship between PII handling and privacy regulations.

---

## Related Concepts

- [Async Explained](../../../concepts/async-explained.md)
- [Classes and Objects](../../../concepts/classes-and-objects.md)
- [Decorators Explained](../../../concepts/decorators-explained.md)
- [How Loops Work](../../../concepts/how-loops-work.md)
- [Quiz: Async Explained](../../../concepts/quizzes/async-explained-quiz.py)

---

| [← Prev](../09-security-baseline-auditor/README.md) | [Home](../../../README.md) | [Next →](../11-recovery-time-estimator/README.md) |
|:---|:---:|---:|
