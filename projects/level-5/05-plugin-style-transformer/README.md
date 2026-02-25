# Level 5 / Project 05 - Plugin Style Transformer
Home: [README](../../../README.md)

## Focus
- extensible transform dispatch

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-5/05-plugin-style-transformer
python project.py --input data/sample_input.json --output data/transformed.json --plugins uppercase,trim_whitespace,add_timestamp
pytest -q
```

## Expected terminal output
```text
Applied 3 plugins to 4 records
9 passed
```

## Expected artifacts
- `data/transformed.json`
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Write a new plugin class that reverses string values and register it in the registry.
2. Add a `--list-plugins` flag that prints all registered plugin names and exits.
3. Add execution order tracking so each record shows which plugins were applied.
4. Re-run script and tests.

## Break it (required)
1. Request a plugin name that does not exist in the registry (e.g. `--plugins nonexistent`).
2. Pass an input file where a record is missing the fields your plugins expect.
3. Capture the first failing test or visible bad output.

## Fix it (required)
1. Raise a clear error listing available plugins when a requested one is not found.
2. Make plugins skip fields that are missing rather than crashing.
3. Add tests for unknown plugin names and missing fields.
4. Re-run until output and tests are deterministic.

## Explain it (teach-back)
1. How does the plugin registry pattern decouple new transforms from the core pipeline?
2. What is the role of the `TransformPlugin` base class?
3. Why does `apply_plugins` iterate plugins in order?
4. Where do you see plugin architectures in real systems (webpack, pytest, Flask extensions)?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Classes and Objects](../../../concepts/classes-and-objects.md)
- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [How Imports Work](../../../concepts/how-imports-work.md)
- [How Loops Work](../../../concepts/how-loops-work.md)
- [Quiz: Classes and Objects](../../../concepts/quizzes/classes-and-objects-quiz.py)

---

| [← Prev](../04-config-layer-priority/README.md) | [Home](../../../README.md) | [Next →](../06-metrics-summary-engine/README.md) |
|:---|:---:|---:|
