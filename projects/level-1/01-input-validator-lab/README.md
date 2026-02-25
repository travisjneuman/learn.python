# Level 1 / Project 01 - Input Validator Lab
Home: [README](../../../README.md)

## Focus
- validate required fields and safe defaults

## Why this project exists
Validate common input formats -- emails, phone numbers, and zip codes -- using string methods and basic regex. You will learn how to dispatch different validators based on input type and return structured pass/fail results.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-1/01-input-validator-lab
python project.py --input data/sample_input.txt
pytest -q
```

## Expected terminal output
```text
=== Validation Results ===

  PASS  [email] user@example.com
  FAIL  [email] bad-email-no-at -- must contain exactly one @
  FAIL  [email] missing@domain -- domain must contain a dot

  1/3 passed validation
5 passed
```

## Expected artifacts
- `data/output.json`
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a new validation type: "url" that checks for `http://` or `https://` prefix and a dot in the domain.
2. Add a `--strict` flag that rejects emails without a TLD of at least 2 characters.
3. Re-run script and tests.

## Break it (required)
1. Add a line with an unknown type like `ssn: 123-45-6789` -- does `validate_input()` handle it or crash?
2. Add a line with no colon separator like `just some text` -- does parsing fail gracefully?
3. Add an email like `user@` -- does `validate_email()` accept it when it should not?

## Fix it (required)
1. Ensure `validate_input()` returns an "unknown type" result for unrecognised types instead of crashing.
2. Handle lines without the `type: value` format by skipping them with a warning.
3. Add a test for the unknown-type case.

## Explain it (teach-back)
1. Why does `validate_email()` use basic string checks (`"@" in value`) rather than a full regex?
2. What does `re.fullmatch()` do differently from `re.search()`?
3. Why return a dict with `{"valid": True/False, "reason": "..."}` instead of just True/False?
4. Where would input validation appear in real software (form handlers, API endpoints, data import)?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Functions Explained](../../../concepts/functions-explained.md)
- [How Imports Work](../../../concepts/how-imports-work.md)
- [The Terminal Deeper](../../../concepts/the-terminal-deeper.md)
- [Quiz: Errors and Debugging](../../../concepts/quizzes/errors-and-debugging-quiz.py)

---

| [← Prev](../README.md) | [Home](../../../README.md) | [Next →](../02-password-strength-checker/README.md) |
|:---|:---:|---:|
