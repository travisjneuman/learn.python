# Level 3 / Project 12 - Parser With Fixtures
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | [Browser](../../../browser/level-3.html) |

<!-- modality-hub-end -->

**Estimated time:** 55 minutes

## Focus
- test fixtures and parser stability

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-3/12-parser-with-fixtures
python project.py data/sample_input.txt
python project.py data/sample_input.txt --format ini --json
pytest -q
```

## Expected terminal output
```text
Format: ini, Lines: 15
[database]
  host = localhost
  port = 5432
...
18 passed
```

## Expected artifacts
- Parsed output on stdout
- Passing tests with fixture-generated files
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a YAML-like parser (indentation-based key: value pairs).
2. Add `--validate` flag that checks all sections have at least one entry.
3. Add line number tracking to each parsed record for error reporting.

## Break it (required) — Core
1. Parse an INI file with duplicate section names — what happens?
2. Parse a CSV with quoted fields containing commas — does simple split work?
3. Auto-detect format on ambiguous input (e.g., `a=b,c=d`) — which parser wins?

## Fix it (required) — Core
1. Handle duplicate sections by merging entries (or warning).
2. Document that the CSV parser doesn't handle quoted fields (limitation).
3. Add a `--format` override so users can bypass auto-detection.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. What is a pytest fixture and how does it differ from setup/teardown?
2. Why do the fixtures use `tmp_path` instead of real files?
3. How does `detect_format` use heuristics to guess the file type?
4. What is the registry pattern (`PARSERS` dict) and why use it?

## Mastery check
You can move on when you can:
- write pytest fixtures that create temporary test data,
- build parsers for multiple text formats,
- use a registry pattern to dispatch to the right parser,
- auto-detect file formats from content.

---

## Related Concepts

- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [Quiz: Errors and Debugging](../../../concepts/quizzes/errors-and-debugging-quiz.py)

---

| [← Prev](../11-project-config-bootstrap/README.md) | [Home](../../../README.md) | [Next →](../13-quality-gate-runner/README.md) |
|:---|:---:|---:|
