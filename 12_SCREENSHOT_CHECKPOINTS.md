# 12 - Screenshot Checkpoints and Reflection Prompts
Home: [README](./README.md)

Use this file to support visual learners and to build a clean troubleshooting history.

## How to use this file
- At each checkpoint, capture a screenshot and store it in your notes/work log folder.
- Use naming format:
  - `phase-<n>_checkpoint-<n>_YYYYMMDD_HHMM.png`
- Add a short reflection after each screenshot.

## Phase checkpoint map

### Phase 0 - Setup
Capture screenshots of:
1. Python version output.
2. Active `.venv` prompt.
3. First passing `pytest` output.

Reflection prompts:
- What command worked immediately?
- What command failed first?
- How did you fix it?

### Phase 1 - Foundations
Capture screenshots of:
1. A working loop output.
2. A traceback you diagnosed.
3. Passing tests for a small function module.

Reflection prompts:
- What bug pattern repeated this week?
- Which debugging method helped most?
- What would you teach a beginner from this lab?

### Phase 2 - Quality and workflow
Capture screenshots of:
1. Ruff clean output.
2. Black format run.
3. pytest test summary.

Reflection prompts:
- Which quality check catches your most common mistakes?
- Which check feels confusing and why?
- What did you standardize in your template?

### Phase 3 - Excel automation
Capture screenshots of:
1. Input folder with sample files.
2. `Master_Report` output.
3. `rejects.csv` with reason codes.

Reflection prompts:
- What invalid data patterns appeared?
- Which validation rule prevented bad output?
- What is still fragile in your pipeline?

### Phase 4 - SQL ETL
Capture screenshots of:
1. Staging table row sample.
2. Reporting table row sample.
3. Summary query result.

Reflection prompts:
- Where can duplicate data still sneak in?
- How did you verify idempotency?
- What index or query improvement did you add?

### Phase 5 - Orion and DPA integration
Capture screenshots of:
1. Orion ingestion result snapshot.
2. DPA ingestion result snapshot.
3. Cache table freshness timestamps.

Reflection prompts:
- Which source failed first and why?
- How did you prove read-only safety?
- Which fields required transformation mapping?

### Phase 6 - Dashboard delivery
Capture screenshots of:
1. Dashboard home view.
2. Filtered view with date + severity.
3. Export action/result.

Reflection prompts:
- Which dashboard view helps non-technical users most?
- What confuses users today?
- What is your fallback when data is stale?

### Phase 7 - Shipping and governance
Capture screenshots of:
1. Release checklist completion.
2. Runbook ownership section.
3. Final capstone demo screen.

Reflection prompts:
- What support risks remain?
- What handoff gaps still exist?
- Which part of your process now feels "SME-level"?

## Weekly checkpoint template (copy/paste)
```markdown
## Weekly Checkpoint - YYYY-MM-DD
- Goal:
- What I changed:
- What broke:
- Root cause:
- Fix applied:
- Evidence screenshots:
  - [ ] link 1
  - [ ] link 2
  - [ ] link 3
- What I will improve next session:
```

## Primary Sources
- [Python tutorial](https://docs.python.org/3/tutorial/)
- [pytest getting started](https://docs.pytest.org/en/stable/getting-started.html)
- [VS Code Python tutorial](https://code.visualstudio.com/docs/python/python-tutorial)

## Optional Resources
- [Python Tutor](https://pythontutor.com/)
- [Exercism Python](https://exercism.org/tracks/python)

## Next
Go to [13_ENTERPRISE_SAMPLE_SCHEMAS.md](./13_ENTERPRISE_SAMPLE_SCHEMAS.md).
