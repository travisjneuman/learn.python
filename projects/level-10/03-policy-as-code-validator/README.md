# Level 10 / Project 03 - Policy As Code Validator
Home: [README](../../../README.md)

## Focus
- Chain of Responsibility pattern for composable policy rules
- Protocol-based rule interface for extensibility
- Declarative policy configuration loaded from JSON
- Batch evaluation with per-rule verdicts and severity levels

## Why this project exists
Infrastructure-as-code demands that compliance checks live alongside the code they govern. By expressing policies as composable Python objects rather than config files, teams get IDE support, type checking, and the ability to unit-test compliance rules. This project builds an OPA-style policy engine in pure Python.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-10/03-policy-as-code-validator
python project.py --config data/config.json --resource data/sample_input.txt
pytest -v
```

## Expected terminal output
```text
{
  "resource_id": "cli-resource",
  "total_rules": 5,
  "passed": 5,
  "failed": 0,
  ...
}
```

## Expected artifacts
- Evaluation report printed to stdout
- Passing tests (`pytest -v` shows ~16 passed)

## Alter it (required)
1. Add a `RegexMatchRule` that validates a field against a regex pattern — register it in `load_policies_from_config`.
2. Add AND/OR composite rules: `AllOfRule` (all sub-rules must pass) and `AnyOfRule` (at least one must pass).
3. Re-run tests and add coverage for the new rule types.

## Break it (required)
1. Pass an unknown rule type in the JSON config and observe the `ValueError`.
2. Evaluate a resource missing all required fields and verify every rule returns FAIL.
3. Pass a non-numeric value to `NumericRangeRule` and confirm the FAIL verdict.

## Fix it (required)
1. Add graceful handling for malformed JSON config (catch `json.JSONDecodeError` with a friendly message).
2. Make `NumericRangeRule` return SKIP instead of FAIL when the field is missing (distinguish "absent" from "invalid").
3. Add tests for the fixed behavior.

## Explain it (teach-back)
1. How does the `PolicyRule` Protocol enable adding new rule types without modifying the engine?
2. Why is severity separate from verdict — when would a FAIL with WARNING severity be useful?
3. How does `evaluate_batch` make it efficient to validate many resources against the same ruleset?
4. What are the tradeoffs between policy-as-code (Python) vs policy-as-data (JSON/YAML)?

## Mastery check
You can move on when you can:
- write a new rule class that satisfies the PolicyRule protocol,
- explain the difference between PASS/FAIL/SKIP verdicts,
- load policies from JSON and evaluate them programmatically,
- describe how this pattern scales to hundreds of rules across multiple frameworks.

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Async Explained](../../../concepts/async-explained.md)
- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Functions Explained](../../../concepts/functions-explained.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../02-autonomous-run-orchestrator/README.md) | [Home](../../../README.md) | [Next →](../04-multi-tenant-data-guard/README.md) |
|:---|:---:|---:|
