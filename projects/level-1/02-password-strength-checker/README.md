# Level 1 / Project 02 - Password Strength Checker
Home: [README](../../../README.md)

> **Try in Browser:** [Run this exercise online](../../browser/level-1.html?ex=2) — no installation needed!

## Before You Start

Recall these prerequisites before diving in:
- Can you use `any()` with a generator expression? (`any(c.isupper() for c in text)`)
- Can you read lines from a file into a list?

**Estimated time:** 20 minutes

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| [Concept](../../../concepts/how-imports-work.md) | **This project** | — | [Quiz](../../../concepts/quizzes/how-imports-work-quiz.py) | [Flashcards](../../../practice/flashcards/README.md) | — | [Browser](../../../browser/level-1.html) |

<!-- modality-hub-end -->

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

## Worked Example

Here is a similar (but different) problem, solved step by step.

**Problem:** Write a function that scores a username's strength based on rules: length, no spaces, no special characters at the start.

**Step 1: Define the rules and assign points.**

```python
def score_username(username):
    score = 0
    reasons = []

    if len(username) >= 3:
        score += 1
    else:
        reasons.append("too short (need 3+ characters)")

    if " " not in username:
        score += 1
    else:
        reasons.append("contains spaces")

    if username[0].isalpha():
        score += 1
    else:
        reasons.append("must start with a letter")

    return {"score": score, "max": 3, "issues": reasons}
```

**Step 2: Test it.** `score_username("alice")` gives 3/3. `score_username("a")` gives 2/3 (too short). `score_username("1bob")` gives 2/3 (starts with number).

**Step 3: Handle edge cases.** What if username is empty? `username[0]` would crash with `IndexError`. Add a guard.

```python
if not username:
    return {"score": 0, "max": 3, "issues": ["username is empty"]}
```

**The thought process:** Check one rule at a time, accumulate a score, collect reasons for failures. This is the same pattern the password strength checker uses with its multi-criteria scoring.

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a "sequential characters" penalty (e.g. "abc", "123" lose a point).
2. Add a `--min-score` flag that only shows passwords scoring at or above the threshold.
3. Re-run script and tests.

## Break it (required) — Core
1. Test an empty password (blank line) -- does `score_password()` crash or return 0?
2. Test a password that is the string `"password"` -- does the common-password check catch it?
3. Test a 1000-character password -- does any check break with very long input?

## Fix it (required) — Core
1. Handle empty passwords by returning a score of 0 with label "empty".
2. Ensure the common-password list comparison is case-insensitive.
3. Add a test for the empty-password edge case.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

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

## Stuck? Ask AI

If you are stuck after trying for 20 minutes, use one of these prompts:

- "I am working on Password Strength Checker. I got this error: [paste error]. Can you explain what this error means without giving me the fix?"
- "I am trying to check if a string contains at least one uppercase letter. I have tried a for loop but it feels clunky. Can you give me a hint about a more Pythonic way?"
- "Can you explain how `any()` works with generator expressions, using an example about checking a list of numbers?"

---

| [← Prev](../01-input-validator-lab/README.md) | [Home](../../../README.md) | [Next →](../03-unit-price-calculator/README.md) |
|:---|:---:|---:|
