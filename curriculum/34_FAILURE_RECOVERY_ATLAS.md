# 34 - Failure Recovery Atlas (When You Get Stuck)
Home: [README](../README.md)

Path placeholder: `<repo-root>` means the folder containing this repository's `README.md`.

Use this when progress stalls. Follow the matching recovery script exactly.

## Failure type A - Environment/setup
Symptoms:
- `python` or `pytest` command not found.
- venv activation fails.

Recovery commands:
```bash
cd <repo-root>
python --version
python -m venv .venv
```

Windows activation:
```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux activation:
```bash
source .venv/bin/activate
```

Expected output:
```text
Python 3.11.x (or newer)
```

## Failure type B - Logic confusion
Symptoms:
- Script runs, output is wrong.

Recovery commands:
```bash
# in current project folder
python project.py --input data/sample_input.txt --output data/output_summary.json
pytest -q
```

Then add temporary debug prints and rerun. Remove debug prints after fix.

Expected output:
```text
failing test points to one behavior mismatch
```

## Failure type C - Tooling overwhelm
Symptoms:
- Too many tool errors, unclear starting point.

Recovery sequence:
```bash
pytest -q
ruff check .
black --check .
```

Fix in this order:
1. Failing tests.
2. Lint violations.
3. Formatting violations.

## Failure type D - Confidence crash
Symptoms:
- Avoiding sessions.
- Starting but not finishing.

Recovery script:
1. Drop to one easier project (`level-0` or `level-1`).
2. Complete one full run + one test pass.
3. Write one short win note.
4. Return to current level with smaller scope.

## Failure type E - SQL or integration drift
Symptoms:
- Query/payload shape changed.
- Field mapping no longer matches.

Recovery sequence:
1. Compare current payload/schema to last known-good sample.
2. Update transform/mapping code.
3. Add regression tests for changed shape.
4. Run small-batch validation before full rerun.

## Failure type F - Dashboard mismatch
Symptoms:
- Dashboard values do not match SQL validation.

Recovery sequence:
1. Validate source cache tables first.
2. Validate dashboard query window/filter logic.
3. Add one reconciliation query to runbook.
4. Re-run and verify parity.

## Primary Sources
- [Using Python on Windows](https://docs.python.org/3/using/windows.html)
- [pytest getting started](https://docs.pytest.org/en/stable/getting-started.html)
- [OrionSDK](https://github.com/solarwinds/OrionSDK)
- [DPA API docs](https://documentation.solarwinds.com/en/success_center/dpa/content/dpa-use-the-api.htm)

## Optional Resources
- [Python Tutor](https://pythontutor.com/)

---

| [← Prev](33_WEEKLY_REVIEW_TEMPLATE.md) | [Home](../README.md) | [Next →](35_CAPSTONE_BLUEPRINTS.md) |
|:---|:---:|---:|
