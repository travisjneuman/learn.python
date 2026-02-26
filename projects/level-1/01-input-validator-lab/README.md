# Level 1 / Project 01 - Input Validator Lab
Home: [README](../../../README.md)

> **Try in Browser:** [Run this exercise online](../../browser/level-1.html?ex=1) — no installation needed!

## Before You Start

Recall these prerequisites before diving in:
- Can you open a file and read its contents into a list of lines?
- Can you use `if`/`elif`/`else` to check multiple conditions?
- Can you check if a character is in a string? (`"@" in "user@example.com"`)

**Estimated time:** 20 minutes

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

## Worked Example

Here is a similar (but different) problem, solved step by step.

**Problem:** Write a function that validates a date string in `YYYY-MM-DD` format.

**Step 1: Think about what makes a date string valid.** It has three parts separated by dashes. The year is 4 digits, the month is 1-12, the day is 1-31.

```python
def validate_date(text):
    parts = text.strip().split("-")
    if len(parts) != 3:
        return {"valid": False, "reason": "must have three parts separated by -"}
    year, month, day = parts
    if not (year.isdigit() and month.isdigit() and day.isdigit()):
        return {"valid": False, "reason": "year, month, day must be numbers"}
    if not (1 <= int(month) <= 12):
        return {"valid": False, "reason": f"month {month} is out of range 1-12"}
    if not (1 <= int(day) <= 31):
        return {"valid": False, "reason": f"day {day} is out of range 1-31"}
    return {"valid": True, "reason": ""}
```

**Step 2: Test it.** `validate_date("2024-01-15")` returns valid. `validate_date("2024-13-01")` returns invalid (month 13). `validate_date("not-a-date")` returns invalid (not numbers).

**The thought process:** Validate one thing at a time: format first, then types, then ranges. Return structured results (dict with valid + reason) so the caller can display useful messages. This is the same pattern the input validator project uses.

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a new validation type: "url" that checks for `http://` or `https://` prefix and a dot in the domain.
2. Add a `--strict` flag that rejects emails without a TLD of at least 2 characters.
3. Re-run script and tests.

## Break it (required) — Core
1. Add a line with an unknown type like `ssn: 123-45-6789` -- does `validate_input()` handle it or crash?
2. Add a line with no colon separator like `just some text` -- does parsing fail gracefully?
3. Add an email like `user@` -- does `validate_email()` accept it when it should not?

## Fix it (required) — Core
1. Ensure `validate_input()` returns an "unknown type" result for unrecognised types instead of crashing.
2. Handle lines without the `type: value` format by skipping them with a warning.
3. Add a test for the unknown-type case.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

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

## Stuck? Ask AI

If you are stuck after trying for 20 minutes, use one of these prompts:

- "I am working on Input Validator Lab. I got this error: [paste error]. Can you explain what this error means without giving me the fix?"
- "I am trying to check if a string contains exactly one `@` symbol. I have tried `count()` but my logic is not quite right. Can you give me a hint?"
- "Can you explain how to return structured results from a validation function, using a different example like checking phone numbers?"

---

| [← Prev](../README.md) | [Home](../../../README.md) | [Next →](../02-password-strength-checker/README.md) |
|:---|:---:|---:|
