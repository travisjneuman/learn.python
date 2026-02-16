# 01 — Roadmap: Zero → Python SME (Automation + Dashboards + Excel/SQL/SolarWinds)

Generated: **Monday, February 16, 2026, 2:11 PM (America/Detroit)**

## What “Python SME” means (concrete outcomes)
By the end, you can:
- Build **reliable automation tools** that run unattended (scheduled tasks) and are safe to rerun.
- Build **repeatable reporting pipelines**: Excel → transform → SQL → dashboard/report.
- Integrate with **SolarWinds Orion** via API (read metrics, alerts; write/ack where permitted).
- Ship **internal web GUIs / dashboards** for non-technical teammates.
- Use modern team standards: **virtual environments, dependency pinning, formatting, linting, tests, logging, packaging**.
- Teach others: docs, examples, code reviews, patterns, “pitfall” guidance.

## The optimal learning order (why this order)
1. **Foundations**: logic + reading code + debugging (otherwise everything else is random memorization).
2. **Professional workflow**: venv/pip, git, lint/format, tests, logging (so you don’t build fragile scripts).
3. **Data + IO**: files + Excel (fastest path to real business value).
4. **SQL**: data persistence + reporting pipeline.
5. **SolarWinds**: apply APIs + query language + auth + data modeling.
6. **Dashboards**: UI + data access patterns + caching + security basics.
7. **CI/CD + packaging**: how you ship repeatably (even if corporate is locked down, you will understand it).

## Time model (flexible)
- Baseline: **6–8 hours/week**
- Typical: **9–12 months** to “team-trusted SME” if you consistently ship small tools.
- Faster path: 10–12 hours/week + weekly capstone increments.

You progress by **deliverables**, not by time spent.

---

# Phase 0 — Setup (Week 1)
**Goal:** Your environment is predictable and professional.

Do: **[03_SETUP_WINDOWS11.md](./03_SETUP_WINDOWS11.md)** (exact steps)

Deliverables:
- A folder called `python_sme/` with:
  - `templates/` (project template)
  - `notes/` (your learning notes)
  - `projects/` (each project gets its own folder)
- You can:
  - create a venv
  - install packages with pip
  - run a script
  - run tests

---

# Phase 1 — Foundations (Weeks 2–6)
**Goal:** You can read and write basic programs without copying blindly.

Study backbone:
- **Automate the Boring Stuff (3rd ed)** (Ch. 1–11) citeturn0search12turn0search19
- Python tutorial for reinforcement (esp. functions, modules) citeturn0search1

What you must master:
- Types: int/float/str/bool/None
- Data structures: list/dict/set/tuple
- Control: if/elif/else, for/while, break/continue
- Functions: parameters, return values, “small composable functions”
- Debugging: reading tracebacks, printing, using VS Code debugger
- Files: read/write text safely (encoding), paths, directories

Deliverables:
- 12–20 “micro scripts” (each 30–120 lines) that do one thing well
- A personal “pitfalls” note (truthiness, mutability, off-by-one)

Guide: **[04_FOUNDATIONS.md](./04_FOUNDATIONS.md)**

---

# Phase 2 — Professional workflow (Weeks 7–10)
**Goal:** Your code is usable by others (consistent, tested, logged).

Core:
- `venv` + `pip` + dependency pinning citeturn0search5turn0search9
- `pyproject.toml` as the single config hub citeturn2search1
- Lint/format: Ruff + Black citeturn0search2
- Tests: pytest citeturn2search2
- Logging: Python logging module

Deliverables:
- A reusable **tool template**:
  - `src/` layout
  - CLI entrypoint
  - config loading
  - structured logging
  - tests
  - lint/format scripts

Guide: **[09_QUALITY_TOOLING.md](./09_QUALITY_TOOLING.md)** + **[02_GLOSSARY.md](./02_GLOSSARY.md)**

---

# Phase 3 — Files + Excel reporting (Weeks 11–16)
**Goal:** Immediate business value: repeatable reporting from spreadsheets.

Tools:
- `pathlib`, `csv`, `json`
- `openpyxl` (Excel) and optionally `pandas` (transformations)

Capstone Project A: **Excel Merger + Validator + Report**
- Input: folder of Excel files
- Output: `Master_Report.xlsx` + `Master_Report.csv`
- Features:
  - schema validation (required columns)
  - normalization (header mismatches)
  - highlight “Critical” rows
  - separate “Critical” tab
  - logs + error summary
  - safe reruns (versioned output)

Guide: **[05_AUTOMATION_FILES_EXCEL.md](./05_AUTOMATION_FILES_EXCEL.md)**

---

# Phase 4 — SQL integration (Weeks 17–22)
**Goal:** Build “data pipelines” rather than “one-off reports”.

Tools:
- SQL basics: SELECT/JOIN/GROUP BY
- Python DB access (pyodbc and/or SQLAlchemy)
- Migrations concept (optional early, important later)

Capstone Project B: **Ingest + Transform + Load**
- Read Excel/CSV → validate → write to SQL staging → promote to reporting table
- Idempotency key (reruns don’t duplicate)
- Reject file output (bad rows)

Guide: **[06_SQL.md](./06_SQL.md)**

---

# Phase 5 — SolarWinds Orion integration (Weeks 23–28)
**Goal:** Automate monitoring/reporting workflows using Orion data.

You will learn:
- Orion platform API basics (SWIS, SWQL concepts)
- Read nodes/interfaces/alerts/events
- Produce “daily health” reports
- (If allowed) acknowledge/annotate alerts

References:
- Orion SDK repo citeturn0search23
- orionsdk-python client citeturn0search3

Capstone Project C: **SolarWinds Daily Ops Report**
- Pull top alerts, down interfaces, capacity metrics
- Output: Excel + HTML dashboard page
- Optional: push summary to email/Teams webhook

Guide: **[07_SOLARWINDS_ORION.md](./07_SOLARWINDS_ORION.md)**

---

# Phase 6 — Web GUIs / Dashboards (Weeks 29–38)
**Goal:** Put your reports behind a usable internal UI.

Recommended order for beginners:
1. **Streamlit** (fastest to working dashboards) citeturn1search0turn1search14
2. **Dash** (more “app-like” dashboards; strong data grids) citeturn1search1
3. **FastAPI** (when you need a real backend API) citeturn1search2

Capstone Project D: **Ops Dashboard**
- Tabs: Excel reports, SQL summaries, SolarWinds health
- Filters: customer/site, date range, severity
- Caching to avoid hammering SolarWinds/SQL
- Auth strategy appropriate for your environment (documented)

Guide: **[08_DASHBOARDS.md](./08_DASHBOARDS.md)**

---

# Phase 7 — Shipping: CI/CD + Packaging + Governance (Weeks 39+)
**Goal:** Make your work easy to run, update, audit, and hand off.

You will learn (plain-English definitions in glossary):
- CI/CD (automate test/build/release) citeturn1search3turn1search10
- PyPI and “internal package indexes” citeturn2search0turn2search7
- Packaging and distribution options citeturn2search3

Deliverables:
- A “release checklist”
- A “deployment modes” guide: zip deploy vs wheel vs internal index
- A “security baseline”: secrets, least privilege, dependency hygiene

Guide: **[11_CHECKLISTS.md](./11_CHECKLISTS.md)** + **[02_GLOSSARY.md](./02_GLOSSARY.md)**

---

# How you will be evaluated (by your team)
You become the SME when you can consistently:
- take ambiguous automation/reporting requests
- clarify requirements
- deliver tools with:
  - good defaults
  - safe behavior
  - logs + tests
  - docs
  - predictable deploy/run steps

Next: **[03_SETUP_WINDOWS11.md](./03_SETUP_WINDOWS11.md)**
