# 02 - Glossary (Plain English + Practical Context)
Home: [README](./README.md)

Use this file anytime you see unknown terms.

## Core programming terms

### Python
- Plain English: A language used to write instructions for a computer.
- Why it matters: It is the core tool used throughout this roadmap.
- Example: Script that merges Excel files into one report.
- Common beginner mistake: Memorizing syntax without understanding inputs and outputs.

### Script
- Plain English: A small program designed to automate one task.
- Why it matters: Most automation starts as scripts.
- Example: Daily job that exports critical monitoring alerts.
- Common beginner mistake: Putting too many unrelated tasks into one script.

### Function
- Plain English: A named block of reusable logic.
- Why it matters: Keeps code testable and maintainable.
- Example: `normalize_status(text)` maps status variants.
- Common beginner mistake: Writing one giant function for everything.

### Variable
- Plain English: A named value that can change.
- Why it matters: Inputs and settings are stored as variables.
- Example: `input_folder = "./input"`.
- Common beginner mistake: Reusing variable names for different meanings.

### List and dictionary
- Plain English: List = ordered collection, dictionary = key/value record.
- Why it matters: Most table-like data in Python is handled as list-of-dicts.
- Example: `[{"TicketID": 123, "Status": "Critical"}]`.
- Common beginner mistake: Mixing list indexes and dict keys.

## Environment and packaging terms

### venv
- Plain English: Isolated Python environment per project.
- Why it matters: Prevents package conflicts between projects.
- Example: `python -m venv .venv`.
- Common beginner mistake: Installing packages globally instead of in `.venv`.

### pip
- Plain English: Package installer for Python.
- Why it matters: Installs tools like `pytest`, `openpyxl`, and `pandas`.
- Example: `python -m pip install pytest`.
- Common beginner mistake: Running `pip` without activating the correct environment.

### pyproject.toml
- Plain English: Standard configuration file for Python projects.
- Why it matters: Central place for tooling settings and metadata.
- Example: Ruff, Black, and pytest settings in one file.
- Common beginner mistake: Scattering config across too many files.

## Quality terms

### Linting
- Plain English: Static checks that find suspicious code patterns.
- Why it matters: Catches bugs before runtime.
- Example: Ruff flags unused imports.
- Common beginner mistake: Treating linter warnings as optional noise.

### Formatting
- Plain English: Automatic style cleanup.
- Why it matters: Makes code consistent and easier to review.
- Example: Black reformats line breaks and spacing.
- Common beginner mistake: Manual formatting and style arguments.

### Unit test
- Plain English: Automated check for a small piece of logic.
- Why it matters: Protects business rules from regressions.
- Example: Test that validates required Excel columns.
- Common beginner mistake: Testing only happy path and ignoring bad input.

### Idempotency
- Plain English: Running the same job multiple times gives the same final result.
- Why it matters: Critical for ETL and scheduled jobs.
- Example: Duplicate source rows are not inserted twice.
- Common beginner mistake: Assuming scheduled jobs run only once.

## SQL and data terms

### ETL
- Plain English: Extract, transform, load.
- Why it matters: Core pattern for reporting pipelines.
- Example: Excel -> clean rows -> SQL database table.
- Common beginner mistake: Skipping schema validation before load.

### Staging table
- Plain English: Temporary/raw landing table.
- Why it matters: Separates ingestion from curated reporting data.
- Example: `staging_alerts` table.
- Common beginner mistake: Writing directly to final reporting tables.

### Reporting table
- Plain English: Clean table used by reports and dashboards.
- Why it matters: Stable source for end users.
- Example: `alerts_current`.
- Common beginner mistake: Mixing raw and curated records.

### SQL auth vs SSO
- Plain English: SQL auth uses DB username/password; SSO uses identity provider (OAuth, SAML).
- Why it matters: Your database access may use SQL auth, not SSO.
- Example: Service account credentials for ETL jobs.
- Common beginner mistake: Hardcoding credentials in scripts.

## Monitoring and API terms

### REST API
- Plain English: Standard way for programs to exchange data over HTTP.
- Why it matters: Main way to query monitoring platforms and external services.
- Example: Query node or alert metadata from a monitoring API.
- Common beginner mistake: Treating API responses like raw SQL access.

### API token
- Plain English: Credential used to call REST API endpoints.
- Why it matters: Enables scripted data pulls from monitoring platforms.
- Example: Fetch instance health metrics daily.
- Common beginner mistake: Storing token in source code.

### Caching layer
- Plain English: Intermediate database layer to reduce repeated API calls.
- Why it matters: Improves dashboard speed and source-system stability.
- Example: Load API snapshots into database cache tables.
- Common beginner mistake: Querying live APIs directly for every dashboard request.

### Service account
- Plain English: Non-personal account for automation jobs.
- Why it matters: Reliable job ownership and audit trail.
- Example: Scheduled ETL user for SQL writes.
- Common beginner mistake: Running production jobs from personal credentials.

## Primary Sources
- [Python glossary and tutorial](https://docs.python.org/3/tutorial/)
- [PyPA guide](https://packaging.python.org/en/latest/tutorials/installing-packages/)
- [requests library](https://docs.python-requests.org/en/latest/)
- [SQLAlchemy tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html)

## Optional Resources
- [Python Tutor](https://pythontutor.com/)
- [Exercism Python](https://exercism.org/tracks/python)

## Next

[Next: 03_SETUP_ALL_PLATFORMS.md →](./03_SETUP_ALL_PLATFORMS.md)
