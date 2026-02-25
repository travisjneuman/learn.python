# Level 10 / Project 05 - Compliance Evidence Builder
Home: [README](../../../README.md)

## Focus
- Observer pattern for pluggable evidence collectors
- Control framework mapping with coverage assessment
- Content hashing for evidence integrity verification
- Audit-ready report generation with status rollup

## Why this project exists
Compliance audits (SOC2, ISO 27001, PCI-DSS) require demonstrable proof that controls are active. This project automates evidence collection into a structured package, so teams can produce audit artifacts on demand instead of scrambling before an audit. The observer model lets new checks be added without modifying the core.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-10/05-compliance-evidence-builder
python project.py
pytest -v
```

## Expected terminal output
```text
Collected 4 evidence items
{
  "framework": "SOC2-mini",
  "total_controls": 5,
  "total_evidence": 4,
  "status_summary": { ... }
}
```

## Expected artifacts
- Compliance report printed to stdout
- Passing tests (`pytest -v` shows ~12 passed)

## Alter it (required)
1. Add a `LogSampleCollector` that reads recent log entries and packages them as evidence for monitoring controls.
2. Add evidence deduplication — if two collectors produce evidence with the same `content_hash`, keep only one.
3. Re-run tests and add coverage for deduplication logic.

## Break it (required)
1. Register no collectors and call `collect_all` — observe that all controls show NOT_ASSESSED.
2. Create evidence that maps to a non-existent control ID — verify it is collected but does not affect assessment.
3. Pass empty content to `Evidence` and check the hash behavior.

## Fix it (required)
1. Add validation that `control_ids` is non-empty when creating Evidence.
2. Make `collect_all` idempotent — calling it twice should not double the evidence list.
3. Add tests for both fixes.

## Explain it (teach-back)
1. How does the Observer pattern decouple evidence collection from assessment logic?
2. Why does each Evidence item store a `content_hash`? How does this support audit integrity?
3. What is the difference between SATISFIED, PARTIAL, and NOT_ASSESSED control statuses?
4. How would you extend this to support multiple compliance frameworks simultaneously?

## Mastery check
You can move on when you can:
- write a new EvidenceCollector that satisfies the Protocol,
- explain how evidence maps to controls through `control_ids`,
- generate a compliance report and interpret the status summary,
- describe how this pattern applies to real SOC2 or ISO 27001 audits.

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Async Explained](../../../concepts/async-explained.md)
- [Classes and Objects](../../../concepts/classes-and-objects.md)
- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../04-multi-tenant-data-guard/README.md) | [Home](../../../README.md) | [Next →](../06-resilience-chaos-workbench/README.md) |
|:---|:---:|---:|
