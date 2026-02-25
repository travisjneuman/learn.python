# Python Mastery Plan (Zero Experience -> World-Class Full-Stack Developer)
Home: [README](./README.md)

Last updated: **February 24, 2026**

This repository is a complete beginner-to-expert Python learning system. It covers two tracks:

**Operations & Integration Track** — monitoring APIs, SQL databases, Excel automation, dashboards (the original core).

**Full-Stack Expansion Modules** — Web scraping, CLI tools, REST APIs, FastAPI, async Python, databases/ORM, data analysis, advanced testing, Docker, Django, package publishing, and cloud deployment.

The plan is hands-on first. You will learn by building, breaking, fixing, and explaining.

## Never programmed before?
Start here: [START_HERE.md](./START_HERE.md)

Or if you need to understand what a terminal and file are first: [00_COMPUTER_LITERACY_PRIMER.md](./00_COMPUTER_LITERACY_PRIMER.md)

## Cross-platform baseline (Windows, macOS, Linux, Android, iOS)
This learning plan supports all major desktop platforms plus mobile companion paths.

Minimum baseline:
- Python 3.11+ installed and available in terminal.
- VS Code (or equivalent editor) installed.
- Ability to create a virtual environment (`venv`) and run `python` from terminal.

Quick command differences:
- Create venv (all): `python3 -m venv .venv` (or `python -m venv .venv` on Windows)
- Activate venv:
  - Windows PowerShell: `.\.venv\Scripts\Activate.ps1`
  - macOS/Linux bash/zsh: `source .venv/bin/activate`
- Install package (all): `python -m pip install <package>`

Primary setup guide in this repo is cross-platform:
- [03_SETUP_ALL_PLATFORMS.md](./03_SETUP_ALL_PLATFORMS.md)

Official platform references:
- Windows: [Using Python on Windows](https://docs.python.org/3/using/windows.html)
- macOS: [Using Python on macOS](https://docs.python.org/3/using/mac.html)
- Unix/Linux: [Using Python on Unix](https://docs.python.org/3/using/unix.html)

## Path placeholder rule
In many docs and project READMEs, `<repo-root>` means:
- the folder that contains this repo's `README.md`
- example: if this repo is cloned to `D:\learn.python`, then `<repo-root>` is `D:\learn.python`
- example: if this repo is cloned to `/home/you/learn.python`, then `<repo-root>` is `/home/you/learn.python`

## Start here in 30 minutes (absolute beginner)
1. Open [03_SETUP_ALL_PLATFORMS.md](./03_SETUP_ALL_PLATFORMS.md).
2. Choose your platform path (Windows, macOS, Linux, Android, or iOS).
3. Complete install + verification until `python --version` (or equivalent) works.
4. Create and activate `.venv` if your platform supports it.
5. Run your first exercise: `python projects/level-00-absolute-beginner/01-first-steps/exercise.py`
6. Return here and pick your learning mode.

If you only do one thing today: finish Setup and run your first exercise.

## Click-through navigation rule (very important)
If you want the exact intended order with zero guesswork:
1. Start with the `Next` link at the bottom of this file.
2. In every document, scroll to the bottom and click only `Next`.
3. Do not branch unless a doc tells you to.
4. When you reach the end of the chain, you will return to this README.

## Choose your learning mode
Use the mode that matches how you learn best. You can switch any week.

### Play-first mode (best if you learn by tinkering)
- Run the example first.
- Change one thing at a time.
- Intentionally break it.
- Explain what changed and why.

### Structured mode (best if you want a checklist)
- Follow each file in order.
- Complete every "Mastery check" before moving on.
- Keep notes in a single study log.

### Hybrid mode (recommended for most learners)
- Weekdays: structured labs.
- Weekend: free exploration and mini-project upgrades.

## Weekly commitment model (default 8-10 hrs/week)
- 4 sessions x 2 hours plus 1 review hour.
- Minimum viable pace: 6 hrs/week.
- Fast-track pace: 12+ hrs/week.

Do not optimize for speed. Optimize for repeatable output and understanding.

## How to use this repo (exact order)

### Foundation path (docs 00-15, in this directory)
0. [00_COMPUTER_LITERACY_PRIMER.md](./00_COMPUTER_LITERACY_PRIMER.md) — what is a terminal, file, program
1. [01_ROADMAP.md](./01_ROADMAP.md) — full program overview
2. [02_GLOSSARY.md](./02_GLOSSARY.md) — key terms defined
3. [03_SETUP_ALL_PLATFORMS.md](./03_SETUP_ALL_PLATFORMS.md) — install Python
4. [04_FOUNDATIONS.md](./04_FOUNDATIONS.md) — core Python concepts
5. [09_QUALITY_TOOLING.md](./09_QUALITY_TOOLING.md) — Ruff, Black, pytest, logging
6. [05_AUTOMATION_FILES_EXCEL.md](./05_AUTOMATION_FILES_EXCEL.md) — file and Excel automation
7. [06_SQL.md](./06_SQL.md) — SQL databases and SQLAlchemy
8. [07_MONITORING_API_INTEGRATION.md](./07_MONITORING_API_INTEGRATION.md) — monitoring data ingestion
9. [08_DASHBOARDS.md](./08_DASHBOARDS.md) — Streamlit/Dash delivery
10. [10_CAPSTONE_PROJECTS.md](./10_CAPSTONE_PROJECTS.md) — integration projects
11. [11_CHECKLISTS.md](./11_CHECKLISTS.md) — gate verification
12. [12_SCREENSHOT_CHECKPOINTS.md](./12_SCREENSHOT_CHECKPOINTS.md) — screenshot evidence
13. [13_SAMPLE_DATABASE_SCHEMAS.md](./13_SAMPLE_DATABASE_SCHEMAS.md) — sample database schemas
14. [14_NAVIGATION_AND_STUDY_WORKFLOW.md](./14_NAVIGATION_AND_STUDY_WORKFLOW.md) — study patterns
15. [15_NEXT_LEVEL_EXPANSION_PLAN.md](./15_NEXT_LEVEL_EXPANSION_PLAN.md) — what comes next

### Advanced path (docs 16-50, in `curriculum/`)
These are for after you complete the foundation path:

**Assessment & placement (16-20):**
- [curriculum/16_LEARNER_PROFILE_AND_PLACEMENT.md](./curriculum/16_LEARNER_PROFILE_AND_PLACEMENT.md)
- [curriculum/17_ASSESSMENT_AND_RUBRICS.md](./curriculum/17_ASSESSMENT_AND_RUBRICS.md)
- [curriculum/18_REMEDIATION_PLAYBOOK.md](./curriculum/18_REMEDIATION_PLAYBOOK.md)
- [curriculum/19_MENTOR_GUIDE.md](./curriculum/19_MENTOR_GUIDE.md)
- [curriculum/20_CURRICULUM_CHANGELOG.md](./curriculum/20_CURRICULUM_CHANGELOG.md)

**Full-stack mastery (21-25):**
- [curriculum/21_FULL_STACK_MASTERY_PATH.md](./curriculum/21_FULL_STACK_MASTERY_PATH.md)
- [curriculum/22_SPECIALIZATION_TRACKS.md](./curriculum/22_SPECIALIZATION_TRACKS.md)
- [curriculum/23_RESOURCE_AND_CURRICULUM_MAP.md](./curriculum/23_RESOURCE_AND_CURRICULUM_MAP.md)
- [curriculum/24_MASTERY_SCORING_AND_GATES.md](./curriculum/24_MASTERY_SCORING_AND_GATES.md)
- [curriculum/25_INFINITY_MASTERY_LOOP.md](./curriculum/25_INFINITY_MASTERY_LOOP.md)

**Zero-to-master execution (26-35):**
- [curriculum/26_ZERO_TO_MASTER_PLAYBOOK.md](./curriculum/26_ZERO_TO_MASTER_PLAYBOOK.md)
- [curriculum/27_DAY_0_TO_DAY_30_BOOTSTRAP.md](./curriculum/27_DAY_0_TO_DAY_30_BOOTSTRAP.md)
- [curriculum/28_LEVEL_0_TO_2_DEEP_GUIDE.md](./curriculum/28_LEVEL_0_TO_2_DEEP_GUIDE.md)
- [curriculum/29_LEVEL_3_TO_5_DEEP_GUIDE.md](./curriculum/29_LEVEL_3_TO_5_DEEP_GUIDE.md)
- [curriculum/30_LEVEL_6_TO_8_DEEP_GUIDE.md](./curriculum/30_LEVEL_6_TO_8_DEEP_GUIDE.md)
- [curriculum/31_LEVEL_9_TO_10_AND_BEYOND.md](./curriculum/31_LEVEL_9_TO_10_AND_BEYOND.md)
- [curriculum/32_DAILY_SESSION_SCRIPT.md](./curriculum/32_DAILY_SESSION_SCRIPT.md)
- [curriculum/33_WEEKLY_REVIEW_TEMPLATE.md](./curriculum/33_WEEKLY_REVIEW_TEMPLATE.md)
- [curriculum/34_FAILURE_RECOVERY_ATLAS.md](./curriculum/34_FAILURE_RECOVERY_ATLAS.md)
- [curriculum/35_CAPSTONE_BLUEPRINTS.md](./curriculum/35_CAPSTONE_BLUEPRINTS.md)

**Elite world-class extension (36-45):**
- [curriculum/36_ELITE_ENGINEERING_TRACK.md](./curriculum/36_ELITE_ENGINEERING_TRACK.md)
- [curriculum/37_QUARTERLY_EXAMS_AND_DEFENSES.md](./curriculum/37_QUARTERLY_EXAMS_AND_DEFENSES.md)
- [curriculum/38_SYSTEM_DESIGN_AND_RFCS.md](./curriculum/38_SYSTEM_DESIGN_AND_RFCS.md)
- [curriculum/39_PRODUCTION_PLATFORM_LAB.md](./curriculum/39_PRODUCTION_PLATFORM_LAB.md)
- [curriculum/40_SECURITY_COMPLIANCE_HARDENING.md](./curriculum/40_SECURITY_COMPLIANCE_HARDENING.md)
- [curriculum/41_PERFORMANCE_ENGINEERING_LAB.md](./curriculum/41_PERFORMANCE_ENGINEERING_LAB.md)
- [curriculum/42_OPEN_SOURCE_CONTRIBUTION_LANE.md](./curriculum/42_OPEN_SOURCE_CONTRIBUTION_LANE.md)
- [curriculum/43_PUBLIC_PROOF_OF_WORK_PORTFOLIO.md](./curriculum/43_PUBLIC_PROOF_OF_WORK_PORTFOLIO.md)
- [curriculum/44_SME_INTERVIEW_AND_DEBATE_BANK.md](./curriculum/44_SME_INTERVIEW_AND_DEBATE_BANK.md)
- [curriculum/45_MASTERY_TELEMETRY_AND_REMEDIATION.md](./curriculum/45_MASTERY_TELEMETRY_AND_REMEDIATION.md)

**Universal learner-adaptive (46-50):**
- [curriculum/46_ACCESSIBILITY_AND_LEARNING_PROFILE_PLAYBOOK.md](./curriculum/46_ACCESSIBILITY_AND_LEARNING_PROFILE_PLAYBOOK.md)
- [curriculum/47_DIAGNOSTIC_AND_PERSONALIZED_STUDY_ENGINE.md](./curriculum/47_DIAGNOSTIC_AND_PERSONALIZED_STUDY_ENGINE.md)
- [curriculum/48_MISCONCEPTION_AND_FAILURE_ATLAS_EXPANDED.md](./curriculum/48_MISCONCEPTION_AND_FAILURE_ATLAS_EXPANDED.md)
- [curriculum/49_COMPETENCY_COVERAGE_AND_GAP_CLOSURE_MATRIX.md](./curriculum/49_COMPETENCY_COVERAGE_AND_GAP_CLOSURE_MATRIX.md)
- [curriculum/50_CERTIFICATION_GRADE_COMPLETION_PROTOCOL.md](./curriculum/50_CERTIFICATION_GRADE_COMPLETION_PROTOCOL.md)

If you only have 8-10 hours/week, focus on docs 00 to 11 first, then run docs 26 to 35 as your deep step-by-step execution layer.
After that, run docs 36 to 45 as the elite-world-class extension layer.
Then run docs 46 to 50 to guarantee adaptive coverage for any learner profile.

Exact click path if you follow `Next` in each file:
`README -> 00 -> 01 -> 02 -> 03 -> 04 -> 09 -> 05 -> 06 -> 07 -> 08 -> 10 -> 11 -> 12 -> 13 -> 14 -> 15 -> 16 -> 17 -> 18 -> 19 -> 20 -> 21 -> 22 -> 23 -> 24 -> 25 -> 26 -> 27 -> 28 -> 29 -> 30 -> 31 -> 32 -> 33 -> 34 -> 35 -> 36 -> 37 -> 38 -> 39 -> 40 -> 41 -> 42 -> 43 -> 44 -> 45 -> 46 -> 47 -> 48 -> 49 -> 50 -> README`

## Deliverable milestones
- Gate A: setup complete + first script + first passing test.
- Gate B: Excel automation handles bad input and safe reruns.
- Gate C: SQL ETL is idempotent.
- Gate D: External API data is ingested into local database cache tables.
- Gate E: Browser dashboard for non-technical users is delivered.

## Project lab ladder (level-00 -> level 10 + elite extension)
- Hands-on projects live in [`./projects`](./projects).
- **Start with level-00-absolute-beginner** if you have never coded before: [`./projects/level-00-absolute-beginner/README.md`](./projects/level-00-absolute-beginner/README.md)
- Then progress through `level-0` through `level-10`.
- Each level includes 15 projects designed to be altered, broken, fixed, and extended.
- Elite extension projects live in [`./projects/elite-track`](./projects/elite-track) for top-tier architecture and systems depth.
- Project index: [`./projects/README.md`](./projects/README.md)

## Expansion modules (full-stack Python)
12 technology modules with 56 hands-on projects covering the full Python ecosystem. Each module is self-contained with real libraries, not simulations.

**After Level 2:** Web Scraping, CLI Tools, REST APIs, Data Analysis
**After Level 3:** FastAPI, Async Python, Databases/ORM, Advanced Testing, Package Publishing
**After Level 5:** Docker & Deployment, Django Full-Stack, Cloud Deployment

Full module index: [`./projects/modules/README.md`](./projects/modules/README.md)

## Concept reference docs
Plain-language explanations of Python concepts at [`./concepts/README.md`](./concepts/README.md):
- Core: variables, loops, functions, collections, files, errors, types
- Intermediate: imports, classes, decorators, virtual environments, terminal
- Advanced: HTTP, APIs, async/await

## Second-pass support packs
- Screenshot checkpoints and study prompts:
  - [12_SCREENSHOT_CHECKPOINTS.md](./12_SCREENSHOT_CHECKPOINTS.md)
- Sample database schemas:
  - [13_SAMPLE_DATABASE_SCHEMAS.md](./13_SAMPLE_DATABASE_SCHEMAS.md)
- Navigation and editorial workflow guide:
  - [14_NAVIGATION_AND_STUDY_WORKFLOW.md](./14_NAVIGATION_AND_STUDY_WORKFLOW.md)

## Sources Library

### Official and vendor documentation (primary)
- Python docs: [Tutorial](https://docs.python.org/3/tutorial/), [Using Python on Windows](https://docs.python.org/3/using/windows.html), [venv](https://docs.python.org/3/library/venv.html), [pathlib](https://docs.python.org/3/library/pathlib.html), [argparse](https://docs.python.org/3/library/argparse.html), [logging HOWTO](https://docs.python.org/3/howto/logging.html)
- Packaging and pip: [PyPA installing packages](https://packaging.python.org/en/latest/tutorials/installing-packages/), [Writing pyproject.toml](https://packaging.python.org/guides/writing-pyproject-toml/), [Project metadata spec](https://packaging.python.org/specifications/declaring-project-metadata/), [pip docs](https://pip.pypa.io/en/stable/)
- VS Code: [Python in VS Code](https://code.visualstudio.com/docs/python/python-tutorial), [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python), [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance), [Black extension](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter), [Ruff extension](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)
- Quality tooling: [Ruff docs](https://docs.astral.sh/ruff/), [Black docs](https://black.readthedocs.io/en/stable/), [pytest getting started](https://docs.pytest.org/en/stable/getting-started.html)
- Data and Excel: [openpyxl tutorial](https://openpyxl.readthedocs.io/en/stable/tutorial.html), [10 minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html), [pandas.read_excel](https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html)
- SQL and Python: [SQLAlchemy tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html), [SQLite docs](https://www.sqlite.org/docs.html), [PostgreSQL docs](https://www.postgresql.org/docs/), [pyodbc](https://github.com/mkleehammer/pyodbc)
- Monitoring APIs: [OpenWeatherMap API](https://openweathermap.org/api), [GitHub REST API](https://docs.github.com/en/rest), [requests library](https://docs.python-requests.org/en/latest/)
- Dashboard stack: [Streamlit get started](https://docs.streamlit.io/get-started), [Dash tutorial](https://dash.plotly.com/tutorial), [Dash deployment](https://dash.plotly.com/deployment), [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/), [FastAPI security basics](https://fastapi.tiangolo.com/tutorial/security/first-steps/)

### Free practice and reinforcement
- [Automate the Boring Stuff (3rd ed)](https://automatetheboringstuff.com/3e/)
- [Exercism Python Track](https://exercism.org/tracks/python)
- [Python Tutor](https://pythontutor.com/)
- [GitHub Git basics](https://docs.github.com/en/get-started/getting-started-with-git)
- [Set up Git](https://docs.github.com/en/get-started/git-basics/set-up-git)
- [Git docs](https://git-scm.com/docs)
- [Pro Git Book](https://git-scm.com/book/en/v2.html)

### Optional paid resources
- [Real Python](https://realpython.com/tutorials/python/)
- Paid courses and books are optional. They should accelerate learning, not block progress.

## Success criteria for this repo
- You can build and explain each capstone.
- Your scripts are safe to rerun.
- Your SQL loads are idempotent.
- Your dashboards are useful to non-technical users.
- You can discuss tradeoffs with experienced engineers.

## Repo validation commands
Run these from repo root to verify curriculum integrity:
- `./tools/check_markdown_links.sh`
- `./tools/check_root_doc_contract.sh`
- `./tools/check_level_index_contract.sh`
- `./tools/check_project_readme_contract.sh`
- `./tools/check_project_python_comment_contract.sh`
- `./tools/check_portable_paths.sh`
- `./tools/check_elite_track_contract.sh`
- `./projects/run_smoke_checks.sh`
- `./projects/run_smoke_checks.sh --full`
- `./projects/run_elite_smoke_checks.sh`
- `./projects/run_elite_smoke_checks.sh --full`
- `python ./tools/generate_personalized_study_plan.py --help`
- `./tools/run_all_curriculum_checks.sh`
- `./tools/run_all_curriculum_checks.sh --full`

---

| [← Prev](curriculum/50_CERTIFICATION_GRADE_COMPLETION_PROTOCOL.md) | [Home](README.md) | [Next →](START_HERE.md) |
|:---|:---:|---:|
