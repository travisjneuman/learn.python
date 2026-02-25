# Level 0 / Project 02 - Calculator Basics
Home: [README](../../../README.md)

## Focus
- numeric input, arithmetic, and safe casting

## Why this project exists
Build a four-operation calculator that reads expressions from a file. You will practise arithmetic operators, float/int conversion, and dispatching operations with a dictionary.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-0/02-calculator-basics
python project.py --input data/sample_input.txt
pytest -q
```

## Expected terminal output
```text
  10 + 5  =>  15.0
  20 - 8  =>  12.0
  6 * 7  =>  42.0

4 results written to data/output.json
5 passed
```

## Expected artifacts
- `data/output.json`
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add support for modulo (`%`) and exponentiation (`**`) operations.
2. Add a `--precision` flag that controls how many decimal places appear in results.
3. Re-run script and tests.

## Break it (required)
1. Add a line `divide 10 0` to the input file -- does it raise `ValueError` or crash with `ZeroDivisionError`?
2. Add a line with only one number like `add 5` -- what happens when there is no second operand?
3. Add a line with text instead of numbers like `add hello world` -- does `float()` fail gracefully?

## Fix it (required)
1. Ensure `divide()` raises `ValueError` with a clear message for zero divisors.
2. Add validation in `calculate()` that checks for exactly two numeric operands.
3. Add a test for the malformed-expression case.

## Explain it (teach-back)
1. Why does the `operations` dict map strings to functions, instead of using if/elif chains?
2. What does `float()` do and when does it raise `ValueError`?
3. Why is division by zero handled in `divide()` rather than in `calculate()`?
4. Where would expression parsers be used in real software (spreadsheets, query engines)?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Files and Paths](../../../concepts/files-and-paths.md)
- [Functions Explained](../../../concepts/functions-explained.md)
- [How Loops Work](../../../concepts/how-loops-work.md)
- [The Terminal Deeper](../../../concepts/the-terminal-deeper.md)
- [Quiz: Files and Paths](../../../concepts/quizzes/files-and-paths-quiz.py)

---

| [← Prev](../01-terminal-hello-lab/README.md) | [Home](../../../README.md) | [Next →](../03-temperature-converter/README.md) |
|:---|:---:|---:|
