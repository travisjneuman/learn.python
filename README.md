# Python SME Plan (Zero Experience -> Enterprise Python Builder)
Home: [README](./README.md)

Last updated: **February 16, 2026**

This repository is a complete beginner-to-advanced Python learning system designed for a real enterprise environment:
- SolarWinds Orion
- SolarWinds DPA
- Custom MSSQL reporting backend
- Browser-based dashboard delivery

The plan is hands-on first. You will learn by building, breaking, fixing, and explaining.

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
5. Run your first script and first `pytest` test.
6. Return here and pick your learning mode.

If you only do one thing today: finish Setup and commit your first working project folder.

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
Full root-doc sequence (deterministic, no guesswork):
1. [01_ROADMAP.md](./01_ROADMAP.md)
2. [02_GLOSSARY.md](./02_GLOSSARY.md)
3. [03_SETUP_ALL_PLATFORMS.md](./03_SETUP_ALL_PLATFORMS.md)
4. [04_FOUNDATIONS.md](./04_FOUNDATIONS.md)
5. [09_QUALITY_TOOLING.md](./09_QUALITY_TOOLING.md)
6. [05_AUTOMATION_FILES_EXCEL.md](./05_AUTOMATION_FILES_EXCEL.md)
7. [06_SQL.md](./06_SQL.md)
8. [07_SOLARWINDS_ORION.md](./07_SOLARWINDS_ORION.md)
9. [08_DASHBOARDS.md](./08_DASHBOARDS.md)
10. [10_CAPSTONE_PROJECTS.md](./10_CAPSTONE_PROJECTS.md)
11. [11_CHECKLISTS.md](./11_CHECKLISTS.md)
12. [12_SCREENSHOT_CHECKPOINTS.md](./12_SCREENSHOT_CHECKPOINTS.md)
13. [13_ENTERPRISE_SAMPLE_SCHEMAS.md](./13_ENTERPRISE_SAMPLE_SCHEMAS.md)
14. [14_NAVIGATION_AND_STUDY_WORKFLOW.md](./14_NAVIGATION_AND_STUDY_WORKFLOW.md)
15. [15_NEXT_LEVEL_EXPANSION_PLAN.md](./15_NEXT_LEVEL_EXPANSION_PLAN.md)
16. [16_LEARNER_PROFILE_AND_PLACEMENT.md](./16_LEARNER_PROFILE_AND_PLACEMENT.md)
17. [17_ASSESSMENT_AND_RUBRICS.md](./17_ASSESSMENT_AND_RUBRICS.md)
18. [18_REMEDIATION_PLAYBOOK.md](./18_REMEDIATION_PLAYBOOK.md)
19. [19_MENTOR_GUIDE.md](./19_MENTOR_GUIDE.md)
20. [20_CURRICULUM_CHANGELOG.md](./20_CURRICULUM_CHANGELOG.md)
21. [21_FULL_STACK_MASTERY_PATH.md](./21_FULL_STACK_MASTERY_PATH.md)
22. [22_SPECIALIZATION_TRACKS.md](./22_SPECIALIZATION_TRACKS.md)
23. [23_RESOURCE_AND_CURRICULUM_MAP.md](./23_RESOURCE_AND_CURRICULUM_MAP.md)
24. [24_MASTERY_SCORING_AND_GATES.md](./24_MASTERY_SCORING_AND_GATES.md)
25. [25_INFINITY_MASTERY_LOOP.md](./25_INFINITY_MASTERY_LOOP.md)
26. [26_ZERO_TO_MASTER_PLAYBOOK.md](./26_ZERO_TO_MASTER_PLAYBOOK.md)
27. [27_DAY_0_TO_DAY_30_BOOTSTRAP.md](./27_DAY_0_TO_DAY_30_BOOTSTRAP.md)
28. [28_LEVEL_0_TO_2_DEEP_GUIDE.md](./28_LEVEL_0_TO_2_DEEP_GUIDE.md)
29. [29_LEVEL_3_TO_5_DEEP_GUIDE.md](./29_LEVEL_3_TO_5_DEEP_GUIDE.md)
30. [30_LEVEL_6_TO_8_DEEP_GUIDE.md](./30_LEVEL_6_TO_8_DEEP_GUIDE.md)
31. [31_LEVEL_9_TO_10_AND_BEYOND.md](./31_LEVEL_9_TO_10_AND_BEYOND.md)
32. [32_DAILY_SESSION_SCRIPT.md](./32_DAILY_SESSION_SCRIPT.md)
33. [33_WEEKLY_REVIEW_TEMPLATE.md](./33_WEEKLY_REVIEW_TEMPLATE.md)
34. [34_FAILURE_RECOVERY_ATLAS.md](./34_FAILURE_RECOVERY_ATLAS.md)
35. [35_CAPSTONE_BLUEPRINTS.md](./35_CAPSTONE_BLUEPRINTS.md)
36. [36_ELITE_ENGINEERING_TRACK.md](./36_ELITE_ENGINEERING_TRACK.md)
37. [37_QUARTERLY_EXAMS_AND_DEFENSES.md](./37_QUARTERLY_EXAMS_AND_DEFENSES.md)
38. [38_SYSTEM_DESIGN_AND_RFCS.md](./38_SYSTEM_DESIGN_AND_RFCS.md)
39. [39_PRODUCTION_PLATFORM_LAB.md](./39_PRODUCTION_PLATFORM_LAB.md)
40. [40_SECURITY_COMPLIANCE_HARDENING.md](./40_SECURITY_COMPLIANCE_HARDENING.md)
41. [41_PERFORMANCE_ENGINEERING_LAB.md](./41_PERFORMANCE_ENGINEERING_LAB.md)
42. [42_OPEN_SOURCE_CONTRIBUTION_LANE.md](./42_OPEN_SOURCE_CONTRIBUTION_LANE.md)
43. [43_PUBLIC_PROOF_OF_WORK_PORTFOLIO.md](./43_PUBLIC_PROOF_OF_WORK_PORTFOLIO.md)
44. [44_SME_INTERVIEW_AND_DEBATE_BANK.md](./44_SME_INTERVIEW_AND_DEBATE_BANK.md)
45. [45_MASTERY_TELEMETRY_AND_REMEDIATION.md](./45_MASTERY_TELEMETRY_AND_REMEDIATION.md)
46. [46_ACCESSIBILITY_AND_LEARNING_PROFILE_PLAYBOOK.md](./46_ACCESSIBILITY_AND_LEARNING_PROFILE_PLAYBOOK.md)
47. [47_DIAGNOSTIC_AND_PERSONALIZED_STUDY_ENGINE.md](./47_DIAGNOSTIC_AND_PERSONALIZED_STUDY_ENGINE.md)
48. [48_MISCONCEPTION_AND_FAILURE_ATLAS_EXPANDED.md](./48_MISCONCEPTION_AND_FAILURE_ATLAS_EXPANDED.md)
49. [49_COMPETENCY_COVERAGE_AND_GAP_CLOSURE_MATRIX.md](./49_COMPETENCY_COVERAGE_AND_GAP_CLOSURE_MATRIX.md)
50. [50_CERTIFICATION_GRADE_COMPLETION_PROTOCOL.md](./50_CERTIFICATION_GRADE_COMPLETION_PROTOCOL.md)

If you only have 8-10 hours/week, focus on docs 01 to 11 first, then run docs 26 to 35 as your deep step-by-step execution layer.
After that, run docs 36 to 45 as the elite-world-class extension layer.
Then run docs 46 to 50 to guarantee adaptive coverage for any learner profile.

Exact click path if you follow `Next` in each file:
`README -> 01 -> 02 -> 03 -> 04 -> 09 -> 05 -> 06 -> 07 -> 08 -> 10 -> 11 -> 12 -> 13 -> 14 -> 15 -> 16 -> 17 -> 18 -> 19 -> 20 -> 21 -> 22 -> 23 -> 24 -> 25 -> 26 -> 27 -> 28 -> 29 -> 30 -> 31 -> 32 -> 33 -> 34 -> 35 -> 36 -> 37 -> 38 -> 39 -> 40 -> 41 -> 42 -> 43 -> 44 -> 45 -> 46 -> 47 -> 48 -> 49 -> 50 -> README`

## Deliverable milestones
- Gate A: setup complete + first script + first passing test.
- Gate B: Excel automation handles bad input and safe reruns.
- Gate C: SQL ETL is idempotent.
- Gate D: Orion + DPA data is ingested into MSSQL cache tables.
- Gate E: Browser dashboard for non-technical users is delivered.

## Project lab ladder (level 0 -> level 10 + elite extension)
- Hands-on projects live in [`./projects`](./projects).
- There are 11 levels: `level-0` through `level-10`.
- Each level includes 15 projects designed to be altered, broken, fixed, and extended.
- Elite extension projects live in [`./projects/elite-track`](./projects/elite-track) for top-tier architecture and systems depth.
- Start here:
  - [`./projects/README.md`](./projects/README.md)
  - [`./projects/level-0/README.md`](./projects/level-0/README.md)

## Second-pass support packs
- Screenshot checkpoints and study prompts:
  - [12_SCREENSHOT_CHECKPOINTS.md](./12_SCREENSHOT_CHECKPOINTS.md)
- Enterprise sample schemas (MSSQL + Orion + DPA):
  - [13_ENTERPRISE_SAMPLE_SCHEMAS.md](./13_ENTERPRISE_SAMPLE_SCHEMAS.md)
- Navigation and editorial workflow guide:
  - [14_NAVIGATION_AND_STUDY_WORKFLOW.md](./14_NAVIGATION_AND_STUDY_WORKFLOW.md)

## Sources Library

### Official and vendor documentation (primary)
- Python docs: [Tutorial](https://docs.python.org/3/tutorial/), [Using Python on Windows](https://docs.python.org/3/using/windows.html), [venv](https://docs.python.org/3/library/venv.html), [pathlib](https://docs.python.org/3/library/pathlib.html), [argparse](https://docs.python.org/3/library/argparse.html), [logging HOWTO](https://docs.python.org/3/howto/logging.html)
- Packaging and pip: [PyPA installing packages](https://packaging.python.org/en/latest/tutorials/installing-packages/), [Writing pyproject.toml](https://packaging.python.org/guides/writing-pyproject-toml/), [Project metadata spec](https://packaging.python.org/specifications/declaring-project-metadata/), [pip docs](https://pip.pypa.io/en/stable/)
- VS Code: [Python in VS Code](https://code.visualstudio.com/docs/python/python-tutorial), [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python), [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance), [Black extension](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter), [Ruff extension](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)
- Quality tooling: [Ruff docs](https://docs.astral.sh/ruff/), [Black docs](https://black.readthedocs.io/en/stable/), [pytest getting started](https://docs.pytest.org/en/stable/getting-started.html)
- Data and Excel: [openpyxl tutorial](https://openpyxl.readthedocs.io/en/stable/tutorial.html), [10 minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html), [pandas.read_excel](https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html)
- SQL Server and Python: [Drivers overview](https://learn.microsoft.com/en-gb/sql/connect/python/python-driver-for-sql-server), [MSSQL Python quickstart](https://learn.microsoft.com/en-us/sql/connect/python/mssql-python/python-sql-driver-mssql-python-quickstart?view=sql-server-ver17), [ODBC connection strings](https://learn.microsoft.com/en-us/sql/connect/odbc/dsn-connection-string-attribute?view=sql-server-ver17), [SQLAlchemy tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html), [pyodbc](https://github.com/mkleehammer/pyodbc)
- Oracle option: [python-oracledb connection handling](https://python-oracledb.readthedocs.io/en/latest/user_guide/connection_handling.html)
- SolarWinds: [OrionSDK](https://github.com/solarwinds/OrionSDK), [orionsdk-python](https://github.com/solarwinds/orionsdk-python), [DPA docs](https://documentation.solarwinds.com/en/success_center/dpa/content/dpa_documentation.htm), [DPA Admin Guide](https://documentation.solarwinds.com/en/success_center/dpa/content/dpa_administrator_guide.htm), [DPA Getting Started](https://documentation.solarwinds.com/en/success_center/dpa/content/dpa_getting_started_guide.htm), [DPA API](https://documentation.solarwinds.com/en/success_center/dpa/content/dpa-use-the-api.htm)
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

## Full-stack expert + infinite mastery track
If your goal is top-end Python mastery (not just competency), follow this advanced chain after finishing the baseline roadmap:
- [21_FULL_STACK_MASTERY_PATH.md](./21_FULL_STACK_MASTERY_PATH.md)
- [22_SPECIALIZATION_TRACKS.md](./22_SPECIALIZATION_TRACKS.md)
- [23_RESOURCE_AND_CURRICULUM_MAP.md](./23_RESOURCE_AND_CURRICULUM_MAP.md)
- [24_MASTERY_SCORING_AND_GATES.md](./24_MASTERY_SCORING_AND_GATES.md)
- [25_INFINITY_MASTERY_LOOP.md](./25_INFINITY_MASTERY_LOOP.md)

## Next-level expansion plan
- [15_NEXT_LEVEL_EXPANSION_PLAN.md](./15_NEXT_LEVEL_EXPANSION_PLAN.md)
- [16_LEARNER_PROFILE_AND_PLACEMENT.md](./16_LEARNER_PROFILE_AND_PLACEMENT.md)
- [17_ASSESSMENT_AND_RUBRICS.md](./17_ASSESSMENT_AND_RUBRICS.md)
- [18_REMEDIATION_PLAYBOOK.md](./18_REMEDIATION_PLAYBOOK.md)
- [19_MENTOR_GUIDE.md](./19_MENTOR_GUIDE.md)
- [20_CURRICULUM_CHANGELOG.md](./20_CURRICULUM_CHANGELOG.md)

## Zero-to-Master execution layer (literal step-by-step)
If you need every process broken down, run this chain after baseline setup:
- [26_ZERO_TO_MASTER_PLAYBOOK.md](./26_ZERO_TO_MASTER_PLAYBOOK.md)
- [27_DAY_0_TO_DAY_30_BOOTSTRAP.md](./27_DAY_0_TO_DAY_30_BOOTSTRAP.md)
- [28_LEVEL_0_TO_2_DEEP_GUIDE.md](./28_LEVEL_0_TO_2_DEEP_GUIDE.md)
- [29_LEVEL_3_TO_5_DEEP_GUIDE.md](./29_LEVEL_3_TO_5_DEEP_GUIDE.md)
- [30_LEVEL_6_TO_8_DEEP_GUIDE.md](./30_LEVEL_6_TO_8_DEEP_GUIDE.md)
- [31_LEVEL_9_TO_10_AND_BEYOND.md](./31_LEVEL_9_TO_10_AND_BEYOND.md)
- [32_DAILY_SESSION_SCRIPT.md](./32_DAILY_SESSION_SCRIPT.md)
- [33_WEEKLY_REVIEW_TEMPLATE.md](./33_WEEKLY_REVIEW_TEMPLATE.md)
- [34_FAILURE_RECOVERY_ATLAS.md](./34_FAILURE_RECOVERY_ATLAS.md)
- [35_CAPSTONE_BLUEPRINTS.md](./35_CAPSTONE_BLUEPRINTS.md)

## Elite world-class extension layer
Run this after the baseline and zero-to-master layers:
- [36_ELITE_ENGINEERING_TRACK.md](./36_ELITE_ENGINEERING_TRACK.md)
- [37_QUARTERLY_EXAMS_AND_DEFENSES.md](./37_QUARTERLY_EXAMS_AND_DEFENSES.md)
- [38_SYSTEM_DESIGN_AND_RFCS.md](./38_SYSTEM_DESIGN_AND_RFCS.md)
- [39_PRODUCTION_PLATFORM_LAB.md](./39_PRODUCTION_PLATFORM_LAB.md)
- [40_SECURITY_COMPLIANCE_HARDENING.md](./40_SECURITY_COMPLIANCE_HARDENING.md)
- [41_PERFORMANCE_ENGINEERING_LAB.md](./41_PERFORMANCE_ENGINEERING_LAB.md)
- [42_OPEN_SOURCE_CONTRIBUTION_LANE.md](./42_OPEN_SOURCE_CONTRIBUTION_LANE.md)
- [43_PUBLIC_PROOF_OF_WORK_PORTFOLIO.md](./43_PUBLIC_PROOF_OF_WORK_PORTFOLIO.md)
- [44_SME_INTERVIEW_AND_DEBATE_BANK.md](./44_SME_INTERVIEW_AND_DEBATE_BANK.md)
- [45_MASTERY_TELEMETRY_AND_REMEDIATION.md](./45_MASTERY_TELEMETRY_AND_REMEDIATION.md)

## Universal learner-adaptive completion layer
Run this to ensure the plan adapts to any learning profile:
- [46_ACCESSIBILITY_AND_LEARNING_PROFILE_PLAYBOOK.md](./46_ACCESSIBILITY_AND_LEARNING_PROFILE_PLAYBOOK.md)
- [47_DIAGNOSTIC_AND_PERSONALIZED_STUDY_ENGINE.md](./47_DIAGNOSTIC_AND_PERSONALIZED_STUDY_ENGINE.md)
- [48_MISCONCEPTION_AND_FAILURE_ATLAS_EXPANDED.md](./48_MISCONCEPTION_AND_FAILURE_ATLAS_EXPANDED.md)
- [49_COMPETENCY_COVERAGE_AND_GAP_CLOSURE_MATRIX.md](./49_COMPETENCY_COVERAGE_AND_GAP_CLOSURE_MATRIX.md)
- [50_CERTIFICATION_GRADE_COMPLETION_PROTOCOL.md](./50_CERTIFICATION_GRADE_COMPLETION_PROTOCOL.md)

## Next
Go to [01_ROADMAP.md](./01_ROADMAP.md).
