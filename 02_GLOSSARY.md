# 02 — Glossary (Zero-Experience Friendly)

This file explains common terms used throughout the plan.

## Python, scripts, programs
- **Python**: a programming language used to write instructions for computers.
- **Script**: usually a small program meant to automate a task.
- **Program**: any set of instructions that runs to do work (scripts are programs too).

## Packages, libraries, pip, PyPI
- **Library / package**: reusable code someone else wrote so you don’t have to reinvent it.
  - Example: `openpyxl` (read/write Excel) or `requests` (HTTP calls).
- **pip**: the tool that installs packages into your Python environment.
  - Example: `python -m pip install openpyxl`
- **PyPI (Python Package Index)**: the public “app store” for Python libraries/packages. citeturn2search0
  - When you run `pip install <something>`, pip usually downloads it from PyPI by default.
- **Internal PyPI**: many companies run a private mirror/index so installs are controlled and audited.

## Virtual environments (venv)
- A **virtual environment** is an isolated Python “bubble” per project so projects don’t break each other. citeturn0search5turn0search9
- `venv` is the built-in tool that creates that bubble.
  - Create: `python -m venv .venv`
  - Activate (PowerShell): `.\.venv\Scripts\Activate.ps1`

## Dependencies and pinning
- **Dependency**: a package your project needs.
- **Pinning**: locking versions so “it works today” still works next month.
  - Common approach: `requirements.txt` with exact versions.
  - Modern approach: `pyproject.toml` plus a lock file (tool-dependent).

## Source control (Git)
- **Git**: tracks changes in files over time so you can revert, compare, collaborate.
- **Repository (repo)**: a folder tracked by Git.
- **Commit**: a saved snapshot of changes.

## Linting, formatting
- **Formatter**: rewrites code to consistent style (example: **Black**).
- **Linter**: finds suspicious code patterns and potential bugs (example: **Ruff**). citeturn0search2

## Tests (pytest)
- **Test**: code that checks your code behaves correctly.
- **pytest**: popular Python testing framework. citeturn2search2

## Logging
- **Log**: a record of what a program did (for troubleshooting, auditing).
- Good automation scripts always log: start/end, counts, warnings, errors.

## APIs and JSON
- **API**: a structured way to request data or perform actions in another system.
- **REST API**: common web API style using HTTP.
- **JSON**: common data format APIs return (like a structured text object).

## SQL and databases
- **Database**: stores data reliably for querying/reporting.
- **SQL**: query language for databases.
- **SQL Server**: Microsoft’s database platform (common in enterprises).
- **ETL**: Extract → Transform → Load (pipeline pattern).

## SolarWinds Orion terms (high level)
- **Orion**: SolarWinds platform (NPM/SAM/etc.) which exposes data via APIs/SDK.
- **SWIS**: Orion “information service” API concept used to query/manage data.
- **SWQL**: query language used with Orion data (like SQL, but Orion-specific).

## Web GUIs / Dashboards
- **Dashboard**: a web page/app that shows data and allows filtering/drill-down.
- **Streamlit**: fastest path to dashboards using only Python. citeturn1search0turn1search14
- **Dash**: dashboard framework for interactive web apps in Python. citeturn1search1
- **FastAPI**: backend API framework (when you need a real service layer). citeturn1search2

## CI/CD (Continuous Integration / Continuous Delivery or Deployment)
- **CI**: every code change is automatically built + tested.
- **CD**: automatically prepares releases and/or deploys them.
- Purpose: fewer “works on my machine” problems; repeatable releases. citeturn1search3turn1search10
- Even if you never run CI/CD at work initially, understanding it helps you structure projects correctly.

Next: **[03_SETUP_WINDOWS11.md](./03_SETUP_WINDOWS11.md)**
