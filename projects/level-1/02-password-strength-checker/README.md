# Level 1 / Project 02 - Password Strength Checker
Home: [README](../../../README.md)

## Focus
- rule-based scoring and condition checks

## Why this project exists
Score passwords on length, character variety, and common-password checks. You will learn rule-based scoring, the `any()` built-in with generator expressions, and how to build a multi-criteria evaluation system.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-1/02-password-strength-checker
python project.py --input data/sample_input.txt
pytest -q
```

## Expected terminal output
```text
=== Password Strength Report ===

  "password"              => Score: 1/5 (weak)
  "abc123"                => Score: 2/5 (weak)
  "MyStr0ng!Pass#2024"    => Score: 5/5 (strong)

3 passwords checked. Output written to data/output.json
5 passed
```

## Expected artifacts
- `data/output.json`
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a "sequential characters" penalty (e.g. "abc", "123" lose a point).
2. Add a `--min-score` flag that only shows passwords scoring at or above the threshold.
3. Re-run script and tests.

## Break it (required)
1. Test an empty password (blank line) -- does `score_password()` crash or return 0?
2. Test a password that is the string `"password"` -- does the common-password check catch it?
3. Test a 1000-character password -- does any check break with very long input?

## Fix it (required)
1. Handle empty passwords by returning a score of 0 with label "empty".
2. Ensure the common-password list comparison is case-insensitive.
3. Add a test for the empty-password edge case.

## Explain it (teach-back)
1. Why does `check_character_variety()` check for uppercase, lowercase, digits, and special characters separately?
2. What does `any(c.isupper() for c in password)` do and why use `any()` instead of a loop?
3. Why is "password" in a common-passwords list instead of checking for specific patterns?
4. Where would password strength checking appear in real software (registration forms, password managers)?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Functions Explained](../../../concepts/functions-explained.md)
- [How Imports Work](../../../concepts/how-imports-work.md)
- [The Terminal Deeper](../../../concepts/the-terminal-deeper.md)
- [Types and Conversions](../../../concepts/types-and-conversions.md)
- [Quiz: Functions Explained](../../../concepts/quizzes/functions-explained-quiz.py)

---

| [← Prev](../01-input-validator-lab/README.md) | [Home](../../../README.md) | [Next →](../03-unit-price-calculator/README.md) |
|:---|:---:|---:|
