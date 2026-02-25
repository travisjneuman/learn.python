# Level 1 / Project 09 - JSON Settings Loader
Home: [README](../../../README.md)

## Focus
- load config and fallback behavior

## Why this project exists
Load application settings from a JSON file, merge them with sensible defaults, and validate required keys. You will learn `json.loads()`, dictionary merging with `{**defaults, **overrides}`, and config validation patterns.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-1/09-json-settings-loader
python project.py --input data/sample_input.txt
pytest -q
```

## Expected terminal output
```text
=== Settings Loader ===

  app_name: LearnPython (from file)
  debug:    True (from file)
  port:     8080 (default)
  host:     localhost (default)

  Loaded 4 settings (2 from file, 2 defaults)
5 passed
```

## Expected artifacts
- `data/output.json`
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `--validate` flag that checks whether all required keys exist without running the main logic.
2. Add environment variable overrides (e.g. `APP_PORT=9090` overrides `"port": 8080` from the file).
3. Re-run script and tests.

## Break it (required)
1. Use a settings file with invalid JSON (missing a closing brace) -- does `load_json()` raise `ValueError`?
2. Use a settings file missing a required key like `"host"` -- does `validate_settings()` catch it?
3. Use a file that exists but is completely empty -- does the loader crash or fall back to defaults?

## Fix it (required)
1. Ensure `load_json()` wraps `json.loads()` in a try/except and raises `ValueError` with context.
2. Handle empty files by treating them as empty dicts (fall back to all defaults).
3. Add a test for the empty-file case.

## Explain it (teach-back)
1. Why does `merge_settings()` create a new dict with `{**defaults, **overrides}` instead of modifying in place?
2. What does `json.loads()` do and how does it differ from `json.load()` (with no 's')?
3. Why keep a `DEFAULTS` dict at module level instead of hardcoding defaults inside functions?
4. Where would settings loaders appear in real software (web servers, CLI tools, microservices)?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Collections Explained](../../../concepts/collections-explained.md)
- [Functions Explained](../../../concepts/functions-explained.md)
- [How Imports Work](../../../concepts/how-imports-work.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../08-path-exists-checker/README.md) | [Home](../../../README.md) | [Next →](../10-ticket-priority-router/README.md) |
|:---|:---:|---:|
