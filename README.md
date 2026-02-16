# Python SME Plan (Zero Experience -> Enterprise Python Builder)
Home: [README](./README.md)

Last updated: **February 16, 2026**

This repository is a complete beginner-to-advanced Python learning system designed for a real enterprise environment:
- SolarWinds Orion
- SolarWinds DPA
- Custom MSSQL reporting backend
- Browser-based dashboard delivery

The plan is hands-on first. You will learn by building, breaking, fixing, and explaining.

## Start here in 30 minutes (absolute beginner)
1. Open [03_SETUP_WINDOWS11.md](./03_SETUP_WINDOWS11.md).
2. Complete install + verification until `python --version` works.
3. Create and activate `.venv`.
4. Run your first script and first `pytest` test.
5. Return here and pick your learning mode.

If you only do one thing today: finish Setup and commit your first working project folder.

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
Core learning path:
1. [01_ROADMAP.md](./01_ROADMAP.md)
2. [03_SETUP_WINDOWS11.md](./03_SETUP_WINDOWS11.md)
3. [04_FOUNDATIONS.md](./04_FOUNDATIONS.md)
4. [09_QUALITY_TOOLING.md](./09_QUALITY_TOOLING.md)
5. [05_AUTOMATION_FILES_EXCEL.md](./05_AUTOMATION_FILES_EXCEL.md)
6. [06_SQL.md](./06_SQL.md)
7. [07_SOLARWINDS_ORION.md](./07_SOLARWINDS_ORION.md)
8. [08_DASHBOARDS.md](./08_DASHBOARDS.md)
9. [10_CAPSTONE_PROJECTS.md](./10_CAPSTONE_PROJECTS.md)
10. [11_CHECKLISTS.md](./11_CHECKLISTS.md)

Reference support file (use anytime):
- [02_GLOSSARY.md](./02_GLOSSARY.md)

## Deliverable milestones
- Gate A: setup complete + first script + first passing test.
- Gate B: Excel automation handles bad input and safe reruns.
- Gate C: SQL ETL is idempotent.
- Gate D: Orion + DPA data is ingested into MSSQL cache tables.
- Gate E: Browser dashboard for non-technical users is delivered.

## Project lab ladder (level 0 -> level 10)
- Hands-on projects live in [`./projects`](./projects).
- There are 11 levels: `level-0` through `level-10`.
- Each level includes 15 projects designed to be altered, broken, fixed, and extended.
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

## Next
Go to [01_ROADMAP.md](./01_ROADMAP.md).
