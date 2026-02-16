# 01 - Roadmap: Zero Experience -> Python SME (Enterprise Automation and Dashboards)
Home: [README](./README.md)

## Who this is for
- You have zero coding, scripting, or programming experience.
- You need practical outcomes in an enterprise operations environment.
- You learn best by doing real work, not passive studying.

## What you will build
- Reliable Python automations for files, Excel, SQL, and monitoring data.
- Repeatable ETL workflows using MSSQL as a reporting backbone.
- SolarWinds Orion and DPA data ingestion jobs.
- Browser-based dashboards for non-technical stakeholders.

## Prerequisites
- Windows 11 machine.
- Permission to install Python and VS Code.
- Access path for MSSQL credentials (non-SSO SQL auth is supported in this plan).
- Read-only API access to Orion and DPA to start.

## Program overview (8-10 hrs/week default)
- Phase 0 (Week 1): environment setup and first script.
- Phase 1 (Weeks 2-6): Python foundations.
- Phase 2 (Weeks 7-10): quality tooling and team-ready workflow.
- Phase 3 (Weeks 11-16): file and Excel automation.
- Phase 4 (Weeks 17-22): SQL-first ETL pipelines.
- Phase 5 (Weeks 23-28): Orion and DPA integration.
- Phase 6 (Weeks 29-38): dashboard delivery for browser users.
- Phase 7 (Weeks 39+): release process, governance, and handoff maturity.

## Step-by-step lab pack

### Phase 0 - Setup (Week 1)
Weekly outcome:
- Local Python environment works reliably.

Minimum deliverables:
- `python --version` works.
- `.venv` created and activated.
- First script runs.
- First test passes.

Done means done:
- You can repeat setup in a fresh folder without guessing.

Fail/recover guidance:
- If activation fails, use the troubleshooting section in [03_SETUP_WINDOWS11.md](./03_SETUP_WINDOWS11.md).

### Phase 1 - Foundations (Weeks 2-6)
Weekly outcomes:
- Week 2: variables, types, conditionals.
- Week 3: loops and collections.
- Week 4: functions and modular thinking.
- Week 5: file IO and paths.
- Week 6: debugging and code reading.

Minimum deliverables:
- 15 micro-scripts.
- One debugging diary file.

Done means done:
- You can explain each script out loud in plain language.

Fail/recover guidance:
- If stuck, reduce problem size and rebuild with toy data.

### Phase 2 - Quality and workflow (Weeks 7-10)
Weekly outcomes:
- toolchain setup, formatting, linting, tests, logging.

Minimum deliverables:
- reusable project template with `pyproject.toml`, tests, logging, and README.

Done means done:
- Any teammate can run your tool using documented steps.

Fail/recover guidance:
- If tooling feels heavy, keep features tiny and run checks per feature.

### Phase 3 - Files and Excel automation (Weeks 11-16)
Weekly outcomes:
- robust ingestion of multiple spreadsheets with validation.

Minimum deliverables:
- Capstone A baseline complete.

Done means done:
- malformed inputs are rejected safely with clear logs.

Fail/recover guidance:
- Start with a 2-file sample dataset and scale gradually.

### Phase 4 - SQL ETL (Weeks 17-22)
Weekly outcomes:
- clean table design and idempotent pipeline loads.

Minimum deliverables:
- staging and reporting tables + ETL job + daily summary query.

Done means done:
- rerunning ETL does not duplicate records.

Fail/recover guidance:
- freeze schema changes until test dataset passes end-to-end.

### Phase 5 - Orion and DPA integration (Weeks 23-28)
Weekly outcomes:
- read-only ingestion from Orion and DPA into cache tables.

Minimum deliverables:
- one daily ingestion job from each source.

Done means done:
- data contract documented, ingestion stable, errors logged.

Fail/recover guidance:
- enforce read-only endpoints first and short polling windows.

### Phase 6 - Dashboard delivery (Weeks 29-38)
Weekly outcomes:
- browser-consumable dashboard with filters and exports.

Minimum deliverables:
- working dashboard with data freshness indicator.

Done means done:
- non-technical user can answer core ops questions without SQL access.

Fail/recover guidance:
- fallback to SQL-only cache mode when source APIs are slow.

### Phase 7 - Shipping and governance (Weeks 39+)
Weekly outcomes:
- release process, support runbook, handoff standards.

Minimum deliverables:
- release checklist and operational runbook.

Done means done:
- another engineer can operate and troubleshoot your tools.

Fail/recover guidance:
- capture every incident and convert it into checklist updates.

## Milestone gates
- Gate A: setup + first script + first passing test.
- Gate B: Capstone A supports safe reruns and rejects.
- Gate C: SQL ETL is idempotent and logged.
- Gate D: Orion/DPA ingestion proof into MSSQL cache.
- Gate E: browser dashboard available to stakeholders.

## Project ladder mapping (practice by skill level)
- Use [`./projects`](./projects) continuously while progressing through phases.
- Suggested mapping:
  - Levels 0-2 during Phase 0-1
  - Levels 3-5 during Phase 2-3
  - Levels 6-7 during Phase 4
  - Levels 8-9 during Phase 5-6
  - Level 10 during Phase 7 and capstone hardening
- Project index:
  - [projects/README.md](./projects/README.md)

## Screenshot and checkpoint workflow
- Capture proof screenshots and reflections while learning:
  - [12_SCREENSHOT_CHECKPOINTS.md](./12_SCREENSHOT_CHECKPOINTS.md)
- Use this after each session to improve retention and speed up troubleshooting.

## If you fall behind (catch-up plan)
1. Keep only one active project at a time.
2. Finish minimum deliverables before adding features.
3. Switch to 45-minute sessions with explicit goals.
4. Use Hybrid mode until momentum returns.

## Learning-style options (Play/Build/Dissect/Teach-back)
- Play: tweak example scripts and observe behavior changes.
- Build: implement full milestone checklists exactly.
- Dissect: read unfamiliar scripts and annotate line-by-line intent.
- Teach-back: explain one concept weekly to another person or a written journal.

## Expected output
- A complete progression from beginner to enterprise-capable Python practitioner.
- A portfolio of capstones tied to your real data systems.

## Break/fix drills
- Break path assumptions by renaming input folders.
- Break schema assumptions by removing required columns.
- Break API assumptions by forcing timeout values.

## Troubleshooting
- If learning stalls: reduce scope, keep daily continuity, and ship smaller increments.
- If project complexity spikes: return to the previous gate and stabilize.

## Mastery check
You are ready to advance when you can:
- describe your current phase deliverable in one sentence,
- run it end-to-end,
- explain where it fails and how to recover.

## Primary Sources
- [Python Tutorial](https://docs.python.org/3/tutorial/)
- [Automate the Boring Stuff](https://automatetheboringstuff.com/3e/)
- [pytest getting started](https://docs.pytest.org/en/stable/getting-started.html)

## Optional Resources
- [Exercism Python](https://exercism.org/tracks/python)
- [Real Python](https://realpython.com/tutorials/python/)

## Next
Go to [03_SETUP_WINDOWS11.md](./03_SETUP_WINDOWS11.md).
