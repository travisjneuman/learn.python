# Level 10 / Project 15 - Level 10 Grand Capstone
Home: [README](../../../README.md)

## Focus
- Facade pattern composing 5 independent subsystems into a unified platform
- Multi-tenant management with policy governance
- End-to-end assessment: policy + readiness + architecture + change gates
- Health scoring with subsystem-level breakdown

## Why this project exists
Real enterprise platforms are compositions of specialized systems. This capstone integrates patterns from all 14 prior projects — tenant isolation, policy engine, change gates, readiness checks, and architecture fitness — into a coherent whole using dependency injection and protocol-based interfaces.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-10/15-level10-grand-capstone
python project.py
pytest -v
```

## Expected terminal output
```text
{
  "overall": "AT_RISK",
  "health_score": 88.9,
  "total_checks": 9,
  "passed": 8,
  "warnings": 1,
  "subsystems": { "policy": [...], "readiness": [...], "architecture": [...], "change_gate": [...] }
}
```

## Alter it (required)
1. Add a `ComplianceSubsystem` that runs evidence collection checks (from project 05).
2. Add a `ChaosReadiness` check that verifies chaos experiments have been run (from project 06).
3. Add a dashboard-style output that shows each subsystem with a traffic-light status.

## Break it (required)
1. Run an assessment with empty context — observe multiple policy failures cascading to UNHEALTHY.
2. Submit a high-risk change with an unready service — observe both change gate and readiness failures.
3. Create an architecture with 50 services and high coupling — verify fitness checks flag it.

## Fix it (required)
1. Add subsystem-level health scores so you can identify which subsystem is dragging down the overall score.
2. Add a `minimum_checks_per_subsystem` threshold — the platform should warn if any subsystem has zero checks.
3. Test both fixes.

## Explain it (teach-back)
1. How does the Facade pattern keep subsystems decoupled while enabling end-to-end assessment?
2. Why does the platform use a universal `CheckResult` type across all subsystems?
3. How does the health score differ from a simple pass/fail count?
4. If you were building this for a real company, which subsystem would you implement first and why?

## Mastery check
You can move on when you can:
- trace a full assessment through all five subsystems,
- add a new subsystem and integrate it into the platform facade,
- explain how Protocol-based interfaces enable loose coupling,
- describe how this architecture maps to real enterprise platforms (AWS Well-Architected, Google SRE).

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Async Explained](../../../concepts/async-explained.md)
- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Functions Explained](../../../concepts/functions-explained.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../14-sme-mentorship-toolkit/README.md) | [Home](../../../README.md) | [Next →](../README.md) |
|:---|:---:|---:|
