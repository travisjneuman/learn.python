# Level 2 / Project 13 - Validation Rule Engine
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| [Concept](../../../concepts/collections-explained.md) | **This project** | — | [Quiz](../../../concepts/quizzes/collections-explained-quiz.py) | [Flashcards](../../../practice/flashcards/README.md) | [Diagram](../../../concepts/diagrams/collections-explained.md) | [Browser](../../../browser/level-2.html) |

<!-- modality-hub-end -->

**Estimated time:** 45 minutes

## Focus
- rule evaluation and reason codes

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-2/13-validation-rule-engine
python project.py data/sample_input.txt
python project.py data/sample_input.txt --verbose
pytest -q
```

## Expected terminal output
```text
Validated 8 records: 4 valid, 4 invalid (50.0% pass rate)
Most common failures: R003: 1, R001: 1, ...
12 passed
```

## Expected artifacts
- Validation report on stdout
- Passing tests
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a new rule type `"one_of"` that checks if a value is in an allowed list.
2. Add a `--rules` flag to load rules from a separate JSON file.
3. Add a `--strict` mode that stops validation after the first failure per record.

## Break it (required) — Core
1. Pass a record with a field that is an unexpected type (e.g. age as a list).
2. Use an invalid regex pattern in a rule — does it crash?
3. Feed an empty records array — does the pass_rate calculation divide by zero?

## Fix it (required) — Core
1. Guard the regex check against `re.error` exceptions.
2. Handle division by zero in pass_rate for empty batches.
3. Add type checking before range validation.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. Why are rules defined as data instead of hard-coded if/else chains?
2. How does the dispatch pattern (`if rule_type == ...`) work?
3. What is the advantage of returning result dicts instead of printing directly?
4. Where would a validation rule engine be used in production systems?

## Mastery check
You can move on when you can:
- add a new rule type without modifying existing rule checks,
- explain data-driven design vs code-driven design,
- write regex patterns for common validations (email, phone, URL),
- describe how this pattern scales to complex validation scenarios.

---

## Related Concepts

- [Collections Explained](../../../concepts/collections-explained.md)
- [Functions Explained](../../../concepts/functions-explained.md)
- [How Loops Work](../../../concepts/how-loops-work.md)
- [Quiz: Collections Explained](../../../concepts/quizzes/collections-explained-quiz.py)

---

| [← Prev](../12-csv-to-json-converter/README.md) | [Home](../../../README.md) | [Next →](../14-anomaly-flagger/README.md) |
|:---|:---:|---:|
