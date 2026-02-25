# Level 9 / Project 09 - Security Baseline Auditor
Home: [README](../../../README.md)

## Focus
- Rule-based auditing against security baselines (CIS, NIST, SOC2)
- Strategy pattern for different security check types
- Compliance scoring with pass/fail/warning/not-applicable states
- Gap analysis identifying missing or weak configurations
- Structured audit reporting with remediation guidance

## Why this project exists
Security baselines like CIS Benchmarks and NIST frameworks define hundreds of required
configuration settings: TLS versions, password policies, logging requirements, encryption
standards. Manually checking them is slow, error-prone, and quickly outdated. This project
builds a configurable security auditor that checks system configurations against baselines,
scores compliance, and generates actionable gap analysis reports — the same automation that
compliance teams run before every SOC2 or ISO 27001 audit.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-9/09-security-baseline-auditor
python project.py --demo
pytest -q
```

## Expected terminal output
```text
{
  "baseline": "CIS-v1",
  "compliance_pct": 75.0,
  "controls_passed": 6,
  "controls_failed": 2,
  "findings": [...]
}
7 passed
```

## Expected artifacts
- Console JSON output with audit results and compliance score
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `check_ip_allowlist` control that validates IP ranges against an allowed list.
2. Add severity-weighted compliance scoring (critical failures reduce score more than medium ones).
3. Add a `--config` flag that loads the system configuration from a JSON file.

## Break it (required)
1. Pass an empty config dictionary — how many controls fail and what compliance_pct results?
2. Set `min_tls_version` to a non-numeric string (e.g. "abc") — does the comparison work?
3. Add a custom check function that raises an exception — does the auditor handle it?

## Fix it (required)
1. Add a fallback value for missing config keys so checks degrade gracefully.
2. Validate TLS version format before comparison.
3. Wrap check function calls in try/except to isolate individual control failures.

## Explain it (teach-back)
1. What is a security baseline and how do standards like CIS Benchmarks define them?
2. How does the Strategy pattern let you plug in new security checks without modifying the auditor?
3. Why does compliance percentage exclude NOT_APPLICABLE controls?
4. How do real organizations automate baseline auditing in their CI/CD pipelines?

## Mastery check
You can move on when you can:
- explain CIS Benchmarks, NIST, and SOC2 at a high level,
- add a new security control (check function + SecurityControl registration),
- describe how compliance scoring works with pass/fail/warning/n-a states,
- design a baseline audit for a real web application with appropriate controls.

---

## Related Concepts

- [Async Explained](../../../concepts/async-explained.md)
- [Classes and Objects](../../../concepts/classes-and-objects.md)
- [Decorators Explained](../../../concepts/decorators-explained.md)
- [Quiz: Async Explained](../../../concepts/quizzes/async-explained-quiz.py)

---

| [← Prev](../08-change-impact-analyzer/README.md) | [Home](../../../README.md) | [Next →](../10-data-governance-enforcer/README.md) |
|:---|:---:|---:|
