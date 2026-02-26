# Level 3 / Project 11 - Project Config Bootstrap
Home: [README](../../../README.md)

**Estimated time:** 50 minutes

## Focus
- bootstrap config with environment overrides

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-3/11-project-config-bootstrap
python project.py show
python project.py show --config-file config.json
python project.py validate --config-file config.json
python project.py generate default_config.json
pytest -q
```

## Expected terminal output
```text
{"app_name": "myapp", "debug": false, "port": 8000, ...}
Sources:
  app_name: myapp (from default)
  port: 5000 (from file)
12 passed
```

## Expected artifacts
- Config output on stdout
- Passing tests
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add support for TOML config files alongside JSON.
2. Add a `--mask-secrets` flag that hides secret_key and database_url in output.
3. Add a `diff` subcommand that shows which values differ from defaults.

## Break it (required) — Core
1. Set `APP_PORT=notanumber` as an environment variable — what happens?
2. Pass a config file with an unknown key — is it ignored or does it crash?
3. Set `port` to -1 in the config — does `validate` catch it?

## Fix it (required) — Core
1. Add type coercion error handling with clear messages.
2. Warn about unknown config keys instead of ignoring them silently.
3. Ensure `validate_config` catches all edge cases (negative values, etc.).

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. Why do configs need precedence (defaults < file < env < CLI)?
2. How does `os.environ` work and what are environment variables?
3. What is type coercion and why is it needed for env/CLI string values?
4. How does `monkeypatch.setenv` work in pytest?

## Mastery check
You can move on when you can:
- load configuration from multiple sources with precedence,
- coerce string values to typed Python values,
- validate configuration for common issues,
- test environment variable handling with `monkeypatch`.

---

## Related Concepts

- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [Types and Conversions](../../../concepts/types-and-conversions.md)
- [Quiz: Errors and Debugging](../../../concepts/quizzes/errors-and-debugging-quiz.py)

---

| [← Prev](../10-dependency-boundary-lab/README.md) | [Home](../../../README.md) | [Next →](../12-parser-with-fixtures/README.md) |
|:---|:---:|---:|
