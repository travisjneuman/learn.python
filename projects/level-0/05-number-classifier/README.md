# Level 0 / Project 05 - Number Classifier
Home: [README](../../../README.md)

## Focus
- if-elif-else decision trees

## Why this project exists
Classify numbers as positive/negative/zero, even/odd, and prime/composite. You will build decision trees with if/elif/else and learn the modulo operator for divisibility checks.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-0/05-number-classifier
python project.py --input data/sample_input.txt
pytest -q
```

## Expected terminal output
```text
       7  =>  positive, odd, prime
      -3  =>  negative, odd, composite
       0  =>  zero, even, composite

  Summary: 1 primes out of 3 valid numbers
  Output written to data/output.json
5 passed
```

## Expected artifacts
- `data/output.json`
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a "perfect number" check (a number equal to the sum of its proper divisors, e.g. 6 = 1+2+3).
2. Add a `--filter` flag that shows only prime numbers, only even numbers, etc.
3. Re-run script and tests.

## Break it (required)
1. Add `0` to the input -- is it classified as prime or composite? (It should be neither.)
2. Add `1` -- the `is_prime()` function should return `False`, but does it?
3. Add a negative number like `-7` -- does `is_prime()` handle negatives correctly?

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

| [← Prev](../04-yes-no-questionnaire/README.md) | [Home](../../../README.md) | [Next →](../06-word-counter-basic/README.md) |
|:---|:---:|---:|
