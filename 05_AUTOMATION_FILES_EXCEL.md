# 05 — Automation: Files + Excel Reporting (Step-by-step)

## Goal
You will build scripts that:
- scan folders
- read multiple Excel files
- validate columns
- merge data
- generate outputs (Excel + CSV + log)

This is where you start producing work that others can use immediately.

---

## Concepts you must understand first
- Paths and files (`pathlib`)
- Loops (processing many files)
- Dictionaries (rows as key/value records)
- Functions (parse → validate → transform → output)
- Logging (runs unattended)
- Virtual environments + pip

If you’re shaky, revisit **[04_FOUNDATIONS.md](./04_FOUNDATIONS.md)**.

---

## Library choices
### Excel I/O
- **openpyxl**: reliable Excel reading/writing for .xlsx
### Transformations
- **pandas**: powerful for cleaning/merging tables

Recommendation:
- Start with openpyxl to understand “cells/sheets”.
- Use pandas once you understand the data model.

---

## Capstone A: Excel Merger + Validator + Report (enterprise version)

### Inputs
- Folder: `input/`
- 3–20 Excel files
- Expected columns (example):
  - `Customer`
  - `Site`
  - `Status`
  - `Opened`
  - `TicketID`

### Outputs
- `output/Master_Report.xlsx`
- `output/Master_Report.csv`
- `logs/run_YYYYMMDD_HHMM.log`
- `output/rejects.csv` (rows that fail validation)

### Step-by-step build plan
#### Step 1 — Project scaffolding
Create project folder with the template structure from **[09_QUALITY_TOOLING.md](./09_QUALITY_TOOLING.md)**.

#### Step 2 — Define your schema
Create a Python list of required columns:
- required = ["Customer", "Site", "Status", "Opened", "TicketID"]

#### Step 3 — Header normalization
Real spreadsheets have:
- `ticket id`, `Ticket_ID`, `TicketId`

Write a function:
- `normalize_header(text: str) -> str`
that:
- trims whitespace
- makes consistent casing
- removes punctuation like `_`

#### Step 4 — Read workbooks
Write `read_rows_from_excel(path) -> list[dict]`
- load workbook
- find header row
- map each row to dict by header

#### Step 5 — Validate rows
Write `validate_row(row) -> (is_ok, reason)`
- missing required fields?
- invalid status?
- invalid date?

Bad rows go to rejects.

#### Step 6 — Merge all data
Combine into a single list of dicts.
Add metadata:
- `SourceFile`
- `IngestedAt`

#### Step 7 — Write outputs
- Write CSV for easy consumption
- Write Excel:
  - main sheet: AllRows
  - second sheet: CriticalRows
  - highlight critical

#### Step 8 — Tests
Write tests for:
- normalize_header
- status normalization
- validate_row

#### Step 9 — CLI wrapper
Add commands like:
- `excelmerge run --input input --output output`

---

## What “good” looks like
- It processes 20 files even if 1 is malformed.
- It never overwrites outputs without versioning.
- It logs counts per file and totals.
- It produces rejects with reasons.

Next: **[06_SQL.md](./06_SQL.md)**
