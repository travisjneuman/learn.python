# Level 0 / Project 03 - Temperature Converter
Home: [README](../../../README.md)

## Focus
- functions and unit conversion practice

## Why this project exists
Convert temperatures between Celsius, Fahrenheit, and Kelvin by routing all conversions through Celsius as a hub. You will learn the hub-and-spoke pattern, which reduces code duplication when supporting multiple unit types.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-0/03-temperature-converter
python project.py --input data/sample_input.txt
pytest -q
```

## Expected terminal output
```text
  100.00 C  =>  212.00 F
  212.00 F  =>  100.00 C
  0.00 C  =>  273.15 K

3 conversions written to data/output.json
5 passed
```

## Expected artifacts
- `data/output.json`
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add Rankine as a fourth temperature scale (Rankine = Fahrenheit + 459.67).
2. Add a `--round` flag that controls the number of decimal places in output.
3. Re-run script and tests.

## Break it (required)
1. Add a line `K C -300` to the input -- this is below absolute zero. Does `convert_temperature()` catch it?
2. Add a line with an unknown unit like `X C 100` -- what happens?
3. Add a line with non-numeric temperature like `C F hot` -- does `float()` fail gracefully?

## Fix it (required)
1. Ensure `celsius_to_kelvin()` and `kelvin_to_celsius()` reject temperatures below absolute zero.
2. Add validation for unknown unit codes in `convert_temperature()`.
3. Add a test that verifies the below-absolute-zero ValueError.

## Explain it (teach-back)
1. Why does the converter route all conversions through Celsius instead of having 6 direct functions?
2. What is the "hub and spoke" pattern and how does it reduce code duplication?
3. Why does `round()` matter for temperature display?
4. Where would unit conversion code appear in real applications (weather APIs, scientific instruments)?

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

| [← Prev](../02-calculator-basics/README.md) | [Home](../../../README.md) | [Next →](../04-yes-no-questionnaire/README.md) |
|:---|:---:|---:|
