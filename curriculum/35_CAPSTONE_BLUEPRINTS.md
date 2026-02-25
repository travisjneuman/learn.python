# 35 - Capstone Blueprints (Step-by-Step Endgame)
Home: [README](../README.md)

Path placeholder: `<repo-root>` means the folder containing this repository's `README.md`.

These are execution blueprints for final mastery-level deliverables.

## Capstone 1 - Automation platform
Goal:
- Build resilient file/Excel automation with validation, rejects, logs, and tests.

Execution steps:
1. Define input/output contract.
2. Build parsing and validation layer.
3. Build transformation layer.
4. Build output + rejects workflow.
5. Add tests and logging.
6. Add rerun safety checks.
7. Document runbook.

Command scaffold:
```bash
cd <repo-root>/projects/level-5/15-level5-mini-capstone
python project.py --input data/sample_input.txt --output data/output_summary.json
pytest -q
```

Expected output:
```text
... output_summary.json written ...
2 passed
```

## Capstone 2 - Data and SQL pipeline
Goal:
- Build idempotent staging-to-reporting pipeline with lineage and drift handling.

Execution steps:
1. Design staging/reporting schema.
2. Implement ingestion + idempotency key logic.
3. Implement promote/merge logic.
4. Add quality checks and summaries.
5. Simulate schema drift and recover.
6. Document lineage and risk controls.

Command scaffold:
```bash
cd <repo-root>/projects/level-6/15-level6-mini-capstone
python project.py --input data/sample_input.txt --output data/output_summary.json
pytest -q
```

Expected output:
```text
... output_summary.json written ...
2 passed
```

## Capstone 3 - Full-stack operational system
Goal:
- Build browser-consumable operational system with backend, data layer, and resilience.

Execution steps:
1. Define user stories and API contract.
2. Build backend endpoints and data access layer.
3. Build browser dashboard layer.
4. Add caching/fallback behavior.
5. Add tests + quality checks.
6. Add failure simulation and recovery steps.

Command scaffold:
```bash
cd <repo-root>/projects/level-10/15-level10-grand-capstone
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

## Final pass criteria
Pass when all are true:
1. All three capstones are reproducible from docs only.
2. Behavior is deterministic across reruns.
3. Failure modes are documented and validated.
4. Tests and quality checks are clean.
5. Architecture decisions and tradeoffs are clearly documented.

Fail when any are true:
1. Hidden setup assumptions remain.
2. Outputs differ without intentional changes.
3. Failure handling is not validated.
4. Tradeoff reasoning is unclear.

## Primary Sources
- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [SQLAlchemy tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html)
- [Streamlit get started](https://docs.streamlit.io/get-started)
- [Dash tutorial](https://dash.plotly.com/tutorial)
- [OrionSDK](https://github.com/solarwinds/OrionSDK)
- [DPA API docs](https://documentation.solarwinds.com/en/success_center/dpa/content/dpa-use-the-api.htm)

## Optional Resources
- [Real Python](https://realpython.com/tutorials/python/)

---

| [← Prev](34_FAILURE_RECOVERY_ATLAS.md) | [Home](../README.md) | [Next →](36_ELITE_ENGINEERING_TRACK.md) |
|:---|:---:|---:|
