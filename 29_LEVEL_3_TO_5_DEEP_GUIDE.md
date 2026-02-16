# 29 - Levels 3 to 5 Deep Guide (Competent to Strong Builder)
Home: [README](./README.md)

Path placeholder: `<repo-root>` means the folder containing this repository's `README.md`.

This guide upgrades you from script author to disciplined engineer.

## Objective
Build reusable, testable, maintainable Python tools with consistent quality checks.

## Required docs
- [09_QUALITY_TOOLING.md](./09_QUALITY_TOOLING.md)
- [05_AUTOMATION_FILES_EXCEL.md](./05_AUTOMATION_FILES_EXCEL.md)
- [projects/level-3/README.md](./projects/level-3/README.md)
- [projects/level-4/README.md](./projects/level-4/README.md)
- [projects/level-5/README.md](./projects/level-5/README.md)

## Standard quality run pattern (copy/paste)
```bash
cd <repo-root>/projects/level-3/01-package-layout-starter
python project.py --input data/sample_input.txt --output data/output_summary.json
ruff check .
black --check .
pytest -q
```

Expected output:
```text
All checks passed!
would reformat 0 files
2 passed
```

## Per-project sequence
1. Run baseline script.
2. Run tests.
3. Run `ruff` and `black --check`.
4. Improve one quality dimension:
   - module structure,
   - logging clarity,
   - validation strictness,
   - test depth.
5. Add one failure-path test.
6. Re-run full checks until clean.

## Common failure patterns and direct fixes
1. Failure: tests pass once and fail on rerun.
   - Fix: remove hidden state and reset generated files in tests.
2. Failure: code works on your machine only.
   - Fix: document setup assumptions in README and pin dependencies.
3. Failure: logs exist but are not actionable.
   - Fix: log run id, input path, counts, and final status.

## Weekly minimum deliverable
Per week, complete at least:
1. Three finished projects.
2. Three new or improved tests.
3. Three break/fix notes with root cause.

## Exit gate (must pass before level 6)
1. You can refactor a large function into smaller units.
2. You can explain why each critical test exists.
3. You can handle malformed input without crashing.
4. You can produce readable run summaries in logs.

## Primary Sources
- [Ruff docs](https://docs.astral.sh/ruff/)
- [Black docs](https://black.readthedocs.io/en/stable/)
- [Writing pyproject.toml](https://packaging.python.org/guides/writing-pyproject-toml/)
- [pytest getting started](https://docs.pytest.org/en/stable/getting-started.html)

## Optional Resources
- [Pro Git Book](https://git-scm.com/book/en/v2.html)
- [Real Python](https://realpython.com/tutorials/python/)

## Next
Go to [30_LEVEL_6_TO_8_DEEP_GUIDE.md](./30_LEVEL_6_TO_8_DEEP_GUIDE.md).
