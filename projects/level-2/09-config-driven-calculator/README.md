# Level 2 / Project 09 - Config Driven Calculator
Home: [README](../../../README.md)

## Focus
- read behavior from json config

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-2/09-config-driven-calculator
python project.py --config data/sample_input.txt --list
python project.py --config data/sample_input.txt --op add --a 10 --b 5
python project.py --config data/sample_input.txt --op divide --a 10 --b 0
pytest -q
```

## Expected terminal output
```text
{"success": true, "operation": "add", "a": 10.0, "b": 5.0, "result": 15.0}
10 passed
```

## Expected artifacts
- Calculation results on stdout
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `sqrt` operation that only uses the `--a` operand.
2. Add a `--chain` mode: `--chain "add:5,multiply:2"` starting from `--a`.
3. Use `settings.precision` from the config to control decimal places.

## Break it (required)
1. Pass a config file with missing "operations" key.
2. Compute `2 ** 1000` — does the result overflow?
3. Pass non-numeric values for `--a` or `--b`.

## Fix it (required)
1. Add `config.setdefault` for missing keys.
2. Check for overflow/infinity in calculate results.
3. Wrap float() conversion in try/except in batch mode.

## Explain it (teach-back)
1. Why is config-driven design useful vs hard-coding operations?
2. How does `dict.setdefault` differ from `dict.get`?
3. What is the Strategy pattern and how does this project resemble it?
4. When would you use JSON config files in real applications?

## Mastery check
You can move on when you can:
- load and validate JSON config from memory,
- add a new operation by editing only the config file,
- explain the difference between hard-coded and config-driven behaviour,
- implement operation chaining from scratch.

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Collections Explained](../../../concepts/collections-explained.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [Functions Explained](../../../concepts/functions-explained.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../08-mini-inventory-engine/README.md) | [Home](../../../README.md) | [Next →](../10-mock-api-response-parser/README.md) |
|:---|:---:|---:|
