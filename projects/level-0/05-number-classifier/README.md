# Level 0 / Project 05 - Number Classifier
Home: [README](../../../README.md)

## Before You Start

Recall these prerequisites before diving in:
- Can you write an if/elif/else chain that checks multiple conditions?
- Do you know what `%` (modulo) does? What does `10 % 3` return?

## Focus
- if-elif-else decision trees

## Why this project exists
Classify numbers as positive/negative/zero, even/odd, and prime/composite. You will build decision trees with if/elif/else and learn the modulo operator for divisibility checks.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-0/05-number-classifier
python project.py
pytest -q
```

The program asks for numbers one at a time. Type `quit` to see a summary.

## Expected terminal output
```text
=== Number Classifier ===
Enter numbers one at a time. Type 'quit' to see a summary.

Enter a number (or 'quit'): 7
  7 is positive, odd, prime

Enter a number (or 'quit'): -3
  -3 is negative, odd, composite

Enter a number (or 'quit'): 0
  0 is zero, even, composite

Enter a number (or 'quit'): quit

=== Summary ===
  Numbers classified: 3
  Primes found: 1
  Even numbers: 1
  Odd numbers: 2
5 passed
```

## Expected artifacts
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a "perfect number" check (a number equal to the sum of its proper divisors, e.g. 6 = 1+2+3).
2. After all numbers are entered, ask "Show only primes? (y/n): " and filter the summary.
3. Re-run script and tests.

## Break it (required)
1. Enter `0` -- is it classified as prime or composite? (It should be neither.)
2. Enter `1` -- the `is_prime()` function should return `False`, but does it?
3. Enter a negative number like `-7` -- does `is_prime()` handle negatives correctly?

## Fix it (required)
1. Ensure `is_prime()` returns `False` for values less than 2.
2. Add the "neither prime nor composite" label for 0 and 1.
3. Add a test that verifies `is_prime(1)` returns `False`.

## Explain it (teach-back)
1. Why does `is_prime()` only check divisors up to the square root of `n`?
2. What is the difference between `n % 2 == 0` (even check) and `n > 1 and all(...)` (prime check)?
3. Why does `classify_number()` return a dict instead of printing directly?
4. Where would number classification appear in real software (data validation, cryptography)?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Classes and Objects](../../../concepts/classes-and-objects.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [How Loops Work](../../../concepts/how-loops-work.md)
- [The Terminal Deeper](../../../concepts/the-terminal-deeper.md)
- [Quiz: Classes and Objects](../../../concepts/quizzes/classes-and-objects-quiz.py)

---

## Stuck? Ask AI

If you are stuck after trying for 20 minutes, use one of these prompts:

- "I am working on Number Classifier. I got this error: [paste error]. Can you explain what this error means without giving me the fix?"
- "I am trying to check if a number is prime. I know I need to check divisors, but I am not sure where to stop. Can you give me a hint about the mathematical shortcut?"
- "Can you explain the modulo operator `%` with three examples that do not involve prime numbers?"

---

| [← Prev](../04-yes-no-questionnaire/README.md) | [Home](../../../README.md) | [Next →](../06-word-counter-basic/README.md) |
|:---|:---:|---:|
