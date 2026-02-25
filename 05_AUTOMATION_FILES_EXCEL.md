# 05 - Automation: Files and Excel Reporting (Capstone A Build Guide)
Home: [README](./README.md)

## Who this is for
- Learners ready to produce business-value automation from spreadsheets.
- Teams that need repeatable reporting with validation and auditability.

## What you will build
A full Excel ingestion pipeline that:
- scans `input/` for `.xlsx` files,
- normalizes headers,
- validates rows,
- writes `Master_Report.xlsx`, `Master_Report.csv`, and `rejects.csv`,
- writes a run log with summary counts.

## Prerequisites
- Foundations phase complete.
- Quality tooling baseline from [09_QUALITY_TOOLING.md](./09_QUALITY_TOOLING.md).
- Installed packages: `openpyxl`, optional `pandas`.

## Step-by-step lab pack

### Step 1 - Project scaffolding
Create structure:
```text
excel_merger/
  input/
  output/
  logs/
  src/
    excel_merger/
      __init__.py
      main.py
      schema.py
      normalize.py
      validate.py
      io_excel.py
      io_csv.py
  tests/
```

### Step 2 - Define schema contract
Required columns:
- `Customer`
- `Site`
- `Status`
- `Opened`
- `TicketID`

Define allowed status values and date rules.

### Step 3 - Header normalization rules
Implement `normalize_header(text)` rules:
- trim whitespace,
- lowercase,
- remove `_`, `-`, and extra spaces,
- map known aliases (for example `ticket id`, `ticket_id`, `ticketid`).

### Step 4 - Workbook ingestion (`openpyxl` path)
- Detect header row.
- Build row dictionaries by normalized headers.
- Capture source filename and row number.

### Step 5 - Row validation
Implement `validate_row(row)` checks:
- missing required fields,
- invalid status,
- invalid date format,
- duplicate TicketID in same file.

Write failures to `rejects.csv` with reason codes.

### Step 6 - Merge and transform
- Combine valid rows from all files.
- Add metadata fields:
  - `source_file`
  - `ingested_at_utc`

### Step 7 - Write outputs
- `output/Master_Report.csv`
- `output/Master_Report.xlsx`
  - worksheet `AllRows`
  - worksheet `CriticalRows`
  - highlight critical rows.

### Step 8 - Logging standards
- one log file per run: `logs/run_YYYYMMDD_HHMMSS.log`
- include:
  - files discovered,
  - rows accepted/rejected,
  - final output paths,
  - fatal errors with traceback.

### Step 9 - Optional `pandas` path
After `openpyxl` baseline works:
- load dataframes,
- apply vectorized transforms,
- compare results to baseline outputs.

### Step 10 - CLI wrapper
Implement command:
```bash
python -m excel_merger.main --input ./input --output ./output --log-dir ./logs
```

## Expected output
- A rerunnable tool that handles malformed files safely.
- Clear output artifacts and rejects report.
- Deterministic behavior when rerun on same input.

## Break/fix drills
1. Remove `TicketID` column in one file and confirm it lands in rejects.
2. Introduce mixed header styles and confirm normalization works.
3. Add a corrupted workbook and confirm pipeline continues with logging.

## Troubleshooting
- Missing package errors:
  - activate `.venv` and reinstall dependencies.
- Date parsing errors:
  - normalize date formats before validation.
- Excel formatting issues:
  - verify workbook writes happen after data transforms, not before.

## Mastery check
You are ready for SQL integration when you can:
- process 20 files with mixed quality,
- produce clean master outputs,
- explain every reject reason,
- rerun without duplicate or conflicting outputs.

## Learning-style options (Play/Build/Dissect/Teach-back)
- Play: modify header aliases and test edge cases.
- Build: follow steps exactly and track completion.
- Dissect: inspect one malformed file and explain why it failed.
- Teach-back: present schema and validation rules to a teammate.

## Acceptance checklist and rubric
Pass criteria:
- functional: all required outputs generated.
- reliability: malformed data does not crash full run.
- traceability: each rejected row has a reason.
- maintainability: tests exist for normalization and validation.

Scoring rubric (0-2 each):
- correctness,
- resilience,
- logging quality,
- test coverage,
- usability of CLI.

## Primary Sources
- [openpyxl tutorial](https://openpyxl.readthedocs.io/en/stable/tutorial.html)
- [pandas 10 minutes](https://pandas.pydata.org/docs/user_guide/10min.html)
- [pandas.read_excel](https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html)

## Optional Resources
- [Automate the Boring Stuff](https://automatetheboringstuff.com/3e/)
- [Real Python Excel articles](https://realpython.com/tutorials/python/)

---

| [← Prev](concepts/virtual-environments.md) | [Home](README.md) | [Next →](projects/level-3/README.md) |
|:---|:---:|---:|
