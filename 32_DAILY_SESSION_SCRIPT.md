# 32 - Daily Session Script (Exact Session Routine)
Home: [README](./README.md)

Path placeholder: `<repo-root>` means the folder containing this repository's `README.md`.

Use this script every study day. No exceptions.

## Session pre-flight (copy/paste)
```bash
cd <repo-root>
python --version
pytest --version
```

Expected output:
```text
Python 3.11.x (or newer)
pytest X.Y.Z
```

## 60-minute session (minimum)
1. 5 min: set one objective.
2. 20 min: implement one change.
3. 15 min: induce one failure.
4. 10 min: fix and verify.
5. 10 min: document root cause and next action.

## 120-minute session (recommended)
1. 10 min: objective and context.
2. 40 min: implementation.
3. 25 min: break/fix drill.
4. 25 min: tests and quality checks.
5. 20 min: notes and next-session planning.

## Per-session command template
```bash
# replace with your current project
cd <repo-root>/projects/level-3/01-package-layout-starter
python project.py --input data/sample_input.txt --output data/output_summary.json
pytest -q
ruff check .
black --check .
```

Expected output:
```text
... output_summary.json written ...
2 passed
All checks passed!
would reformat 0 files
```

## Session completion criteria
A session is complete only if all are true:
1. Code ran.
2. At least one failure was investigated.
3. At least one fix was verified.
4. Notes were updated.

## Primary Sources
- [pytest getting started](https://docs.pytest.org/en/stable/getting-started.html)
- [logging HOWTO](https://docs.python.org/3/howto/logging.html)
- [Ruff docs](https://docs.astral.sh/ruff/)

## Optional Resources
- [Python Tutor](https://pythontutor.com/)

## Next
Go to [33_WEEKLY_REVIEW_TEMPLATE.md](./33_WEEKLY_REVIEW_TEMPLATE.md).
