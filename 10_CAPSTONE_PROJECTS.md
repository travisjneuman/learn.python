# 10 - Capstone Projects (Graded Specs for SME Readiness)
Home: [README](./README.md)

## Who this is for
- Learners ready to prove end-to-end capability.
- Engineers preparing portfolio-quality internal tools.

## What you will build
- Four graded capstones that map to real operational workflows.

## Prerequisites
- Completion of phases 0-6.
- Quality tooling baseline and working template.

## Step-by-step lab pack

### Capstone A - Excel Merger + Validator + Report
Business goal:
- Standardize and merge operational spreadsheets safely.

Inputs/outputs:
- Input folder of `.xlsx` files.
- Outputs: master CSV/XLSX, rejects CSV, run log.

Implementation milestones:
1. schema contract,
2. normalization,
3. validation,
4. output writing,
5. tests and logging.

Test scenarios:
- missing required columns,
- mixed header styles,
- malformed workbook.

Failure modes:
- hard crash on one bad file,
- silent row drops,
- overwritten outputs.

Pass/fail rubric:
- pass = deterministic outputs, rejects with reasons, logs, tests.

Stretch goals:
- config-driven schemas,
- richer Excel formatting.

### Capstone B - ETL to MSSQL
Business goal:
- Move validated report data into durable SQL pipelines.

Inputs/outputs:
- Inputs from Capstone A.
- Outputs: staging load, reporting load, daily summary export.

Implementation milestones:
1. table design,
2. db connectivity,
3. idempotent loading,
4. summary query export.

Test scenarios:
- duplicate source data reruns,
- timeout and retry handling,
- schema mismatch.

Failure modes:
- duplicates in reporting table,
- partial writes without rollback,
- hidden auth assumptions.

Pass/fail rubric:
- pass = idempotent ETL, stable logging, recoverable failures.

Stretch goals:
- SQLAlchemy migration path,
- performance tuning and indexing.

### Capstone C - Orion + DPA Daily Ops Pipeline
Business goal:
- Ingest monitoring health data into reporting cache.

Inputs/outputs:
- Orion and DPA API reads.
- Outputs: cache tables + daily ops reports (xlsx/html).

Implementation milestones:
1. read-only endpoint integration,
2. field mapping worksheet,
3. cache table writes,
4. freshness checks.

Test scenarios:
- API auth failures,
- endpoint timeout,
- payload field drift.

Failure modes:
- stale data with no warning,
- mixed source semantics,
- over-polling source systems.

Pass/fail rubric:
- pass = stable read ingestion, clear ownership mapping, stale-data signaling.

Stretch goals:
- Teams/email summary delivery,
- adaptive polling windows.

### Capstone D - Browser Ops Dashboard
Business goal:
- Deliver usable operational visibility to non-technical users.

Inputs/outputs:
- MSSQL summary/cache data.
- Output: browser UI with filters and exports.

Implementation milestones:
1. user story definition,
2. baseline UI,
3. SQL-backed filters,
4. exports and freshness indicators,
5. deployment notes.

Test scenarios:
- empty data windows,
- stale cache,
- high row counts.

Failure modes:
- slow loads,
- unclear filter behavior,
- no ownership/hand-off docs.

Pass/fail rubric:
- pass = user can answer core daily questions without SQL access.

Stretch goals:
- role-based views,
- API service layer.

## Expected output
- A practical portfolio proving SME-level operational Python capability.

## Break/fix drills
1. Force one capstone dependency failure and recover without data corruption.
2. Simulate stale data and communicate impact clearly.
3. Rerun all capstones with same input and prove determinism.

## Troubleshooting
- project sprawl:
  - isolate each capstone boundary and dependencies.
- weak test confidence:
  - add scenario-based tests for failure paths.
- handoff risk:
  - strengthen runbooks and ownership metadata.

## Mastery check
You are SME-ready when you can:
- demo all capstones end-to-end,
- explain architecture tradeoffs,
- support and recover production-like failures.

## Learning-style options (Play/Build/Dissect/Teach-back)
- Play: add one meaningful enhancement per capstone.
- Build: complete base rubric before enhancements.
- Dissect: produce architecture diagrams and data flow notes.
- Teach-back: run a capstone walkthrough for peer review.

## Primary Sources
- [Streamlit docs](https://docs.streamlit.io/get-started)
- [Dash docs](https://dash.plotly.com/tutorial)
- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [OrionSDK](https://github.com/solarwinds/OrionSDK)
- [DPA API docs](https://documentation.solarwinds.com/en/success_center/dpa/content/dpa-use-the-api.htm)

## Optional Resources
- [Real Python](https://realpython.com/tutorials/python/)

---

| [← Prev](projects/modules/README.md) | [Home](README.md) | [Next →](11_CHECKLISTS.md) |
|:---|:---:|---:|
