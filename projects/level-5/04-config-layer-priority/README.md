# Level 5 / Project 04 - Config Layer Priority
Home: [README](../../../README.md)

## Focus
- defaults, env, and cli precedence

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-5/04-config-layer-priority
python project.py --config data/config.json --output data/resolved_config.json
# Try with env override:
APP_LOG_LEVEL=DEBUG python project.py --config data/config.json --output data/resolved_config.json
pytest -q
```

## Expected terminal output
```text
Resolved config: 5 keys from 3 layers
6 passed
```

## Expected artifacts
- `data/resolved_config.json`
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `--set` flag that allows setting individual keys from the CLI (e.g. `--set log_level=TRACE`).
2. Add a `--dump-sources` mode that prints which layer each final value came from.
3. Support nested config keys using dot notation (e.g. `database.host`).
4. Re-run script and tests.

## Break it (required)
1. Set an environment variable with a non-numeric value for a key that expects an integer (e.g. `APP_MAX_CONNECTIONS=abc`).
2. Reference a config file that does not exist.
3. Capture the first failing test or visible bad output.

## Fix it (required)
1. Add type coercion with error handling that logs a warning and falls back to the default.
2. Handle missing config file gracefully (use defaults only).
3. Add tests for bad env var types and missing files.
4. Re-run until output and tests are deterministic.

## Explain it (teach-back)
1. Why is env > file > defaults the standard precedence order?
2. What happens when `coerce_types` encounters a value it cannot convert?
3. How does `os.environ.get` with a prefix prevent collisions with other apps?
4. Where do you see layered configuration in production systems (12-factor apps, Kubernetes)?

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
- [Functions Explained](../../../concepts/functions-explained.md)
- [The Terminal Deeper](../../../concepts/the-terminal-deeper.md)
- [Quiz: Classes and Objects](../../../concepts/quizzes/classes-and-objects-quiz.py)

---

| [← Prev](../03-multi-file-etl-runner/README.md) | [Home](../../../README.md) | [Next →](../05-plugin-style-transformer/README.md) |
|:---|:---:|---:|
