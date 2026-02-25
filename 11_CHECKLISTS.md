# 11 - Checklists and Runbooks (Operate Like an SME)
Home: [README](./README.md)

## Project startup checklist
- [ ] Create project from standard template.
- [ ] Create and activate `.venv`.
- [ ] Install dependencies.
- [ ] Configure `pyproject.toml`.
- [ ] Add initial tests.
- [ ] Add logging setup.
- [ ] Add README run instructions.
- [ ] Commit baseline.

## Pre-run checklist
- [ ] Confirm input path and format.
- [ ] Confirm output path does not overwrite critical data.
- [ ] Confirm credentials are loaded from secure source.
- [ ] Confirm DB/API connectivity tests pass.
- [ ] Confirm dry-run or small-sample run completed.

## Post-run validation checklist
- [ ] Logs contain start/end timestamps.
- [ ] Row/file counts match expectations.
- [ ] Reject file generated and reviewed.
- [ ] Output artifacts versioned and discoverable.
- [ ] Data freshness timestamps updated.

## Incident triage checklist
- [ ] Capture exact error message and stack trace.
- [ ] Classify impact (none, degraded, outage).
- [ ] Pause unsafe writes if integrity is at risk.
- [ ] Identify blast radius (files/tables/users).
- [ ] Roll forward or rollback with documented action.
- [ ] Add permanent prevention check after incident.

## Release and handoff checklist
- [ ] `ruff check .` passes.
- [ ] `black .` applied.
- [ ] `pytest` passes.
- [ ] End-to-end sample run documented.
- [ ] Versioned artifact prepared.
- [ ] Runbook updated.
- [ ] Support owner and escalation path assigned.

## Dashboard UX checklist (non-technical users)
- [ ] Filters are obvious and labeled in plain language.
- [ ] Refresh timestamp is visible.
- [ ] Empty-state messages are actionable.
- [ ] Export path is obvious.
- [ ] Performance is acceptable on common queries.

## SME conversation prep checklist
Use before architecture reviews with experienced engineers:
- [ ] Can explain your data flow in under 2 minutes.
- [ ] Can justify staging vs reporting schema design.
- [ ] Can explain idempotency strategy.
- [ ] Can explain API data cache strategy.
- [ ] Can explain security posture for credentials and access.
- [ ] Can explain dashboard fallback behavior during outages.

## Screenshot and checkpoint checklist
- [ ] Capture one setup screenshot per major milestone.
- [ ] Capture one failure screenshot and one fix screenshot per week.
- [ ] Write 3 checkpoint reflections after each study session:
  - what I changed,
  - what broke,
  - what I fixed.
- [ ] Keep screenshots and notes organized by phase and date.
- [ ] Use [12_SCREENSHOT_CHECKPOINTS.md](./12_SCREENSHOT_CHECKPOINTS.md) as the standard template.

## Primary Sources
- [pytest getting started](https://docs.pytest.org/en/stable/getting-started.html)
- [Ruff docs](https://docs.astral.sh/ruff/)
- [Black docs](https://black.readthedocs.io/en/stable/)
- [GitHub Git basics](https://docs.github.com/en/get-started/getting-started-with-git)

## Optional Resources
- [Pro Git Book](https://git-scm.com/book/en/v2.html)
- [Real Python](https://realpython.com/tutorials/python/)

---

| [← Prev](10_CAPSTONE_PROJECTS.md) | [Home](README.md) | [Next →](12_SCREENSHOT_CHECKPOINTS.md) |
|:---|:---:|---:|
