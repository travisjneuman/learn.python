# Feature Unlock Chart

What Python features are introduced at each level. Use this to see what is expected of you and what tools you have available.

## By Level

### Level 00 -- Absolute Beginner (no imports, no tests)

| Feature | First Project |
|---------|---------------|
| `print()` | 01 First Steps |
| `input()` | 03 User Input |
| Variables, `=` | 04 Variables |
| Integers, `+`, `-`, `*`, `/`, `//`, `%` | 05 Numbers and Math |
| Strings, f-strings | 06 Strings and Text |
| `if` / `elif` / `else` | 08 Making Decisions |
| Lists, indexing, `.append()` | 09 Lists |
| `for` loops, `range()` | 10 For Loops |
| `while` loops | 11 While Loops |
| Dictionaries, key-value pairs | 12 Dictionaries |
| `def`, `return` | 13 Functions |
| `open()`, `.read()`, `.strip()` | 14 Reading Files |

### Level 0 -- Beginner (pytest and ruff start here)

| Feature | First Project |
|---------|---------------|
| Functions with parameters and return values | 02 Calculator Basics |
| `if`/`elif`/`else` branching | 04 Yes No Questionnaire |
| `for` / `while` with logic | 05 Number Classifier |
| File reading and writing (`open`, `with`) | 07 First File Reader |
| String methods (`.split()`, `.strip()`, `.lower()`) | 08 String Cleaner Starter |
| Lists and iteration patterns | 09 Daily Checklist Writer |
| Dictionaries for lookup/counting | 10 Duplicate Line Finder |
| `pytest` (test discovery, assertions) | All projects |
| `ruff` (linting) | All projects |

### Level 1 -- String Methods, CSV, JSON, pathlib

| Feature | First Project |
|---------|---------------|
| Input validation patterns | 01 Input Validator Lab |
| String method chaining | 02 Password Strength Checker |
| `csv` module | 05 CSV First Reader |
| `json` module | 09 JSON Settings Loader |
| `pathlib.Path` | 08 Path Exists Checker |
| `argparse` | 11 Command Dispatcher |
| `datetime` | 07 Date Difference Helper |
| Multi-file projects | 15 Level1 Mini Toolkit |

### Level 2 -- Nested Data, Comprehensions, Error Handling

| Feature | First Project |
|---------|---------------|
| Nested dicts and lists | 01 Dictionary Lookup Service |
| Data flattening | 02 Nested Data Flattener |
| `try` / `except` / `finally` | 04 Error Safe Divider |
| Dict and list comprehensions | 05 Comprehension Drills |
| Sets and set operations | 06 Set Intersection Report |
| Multiple exception types | 11 Retry Loop Practice |
| `collections.Counter` | 12 Multi File Stats Aggregator |
| Project structure (src/, tests/) | 15 Level2 Mini Capstone |

### Level 3 -- Packages, Logging, Refactoring

| Feature | First Project |
|---------|---------------|
| `pip install`, third-party packages | 01 First Package Install |
| `logging` module | 02 Logger Config Lab |
| `pytest` parametrize, fixtures | 03 Parameterized Test Writer |
| Code refactoring patterns | 04 Function Extraction Exercise |
| `__name__ == "__main__"` pattern | 05 Module Runner Pattern |
| Configuration files (INI, YAML) | 09 Config Merge Tool |
| Package boundaries | 10 Dependency Boundary Lab |

### Level 4 -- Data Validation, File Operations

| Feature | First Project |
|---------|---------------|
| Schema validation | 01 Schema Validator Intro |
| Data cleaning pipelines | 02 Field Normalizer |
| File backup and rotation | 04 Backup Rotation Manager |
| Regex basics (`re` module) | 05 Regex Practice Set |
| CSV transformation | 07 Csv Transform Pipeline |
| Checksums and hashing | 09 Checksum File Verifier |
| Batch file processing | 12 Bulk File Renamer |

### Level 5 -- Scheduling, Monitoring, ETL

| Feature | First Project |
|---------|---------------|
| `schedule` library | 01 Cron Style Scheduler |
| Environment variables | 02 Environment Config Loader |
| ETL (Extract, Transform, Load) | 03 Etl Pipeline Starter |
| Template rendering (`Jinja2`) | 05 Template Report Builder |
| Multi-layer configuration | 07 Config Layer Stack |
| Polling patterns | 10 API Polling Simulator |
| Metric collection | 11 Metric Aggregation Engine |

### Level 6 -- SQL, Databases, Transactions

| Feature | First Project |
|---------|---------------|
| `sqlite3` | 01 Sqlite Hello World |
| SQL: SELECT, INSERT, UPDATE, DELETE | 02 Crud Operations Lab |
| Joins and relationships | 03 Join Query Builder |
| Transactions and rollback | 05 Transaction Rollback Lab |
| Database migrations | 06 Schema Migration Runner |
| Idempotent operations | 07 Idempotent Upsert Drill |
| Connection pooling | 09 Connection Pool Monitor |

### Level 7 -- APIs, Caching, Observability

| Feature | First Project |
|---------|---------------|
| `requests` library (advanced) | 01 Api Response Validator |
| Rate limiting | 02 Rate Limit Handler |
| Caching strategies | 03 Cache Invalidation Lab |
| Token-based auth | 05 Token Refresh Handler |
| Webhook patterns | 06 Webhook Receiver Stub |
| Structured logging | 07 Structured Log Formatter |
| Observability metrics | 08 Ingestion Observability Kit |

### Level 8 -- Dashboards, Concurrency, Profiling

| Feature | First Project |
|---------|---------------|
| Dashboard data assembly | 01 Dashboard Data Assembler |
| Query caching | 02 Query Cache Layer |
| Pagination | 03 Pagination Stress Lab |
| `concurrent.futures` | 07 Concurrent Refresh Scheduler |
| Fault injection testing | 08 Fault Injection Harness |
| `cProfile`, profiling | 09 Profile Guided Optimization |
| Snapshot testing | 11 Snapshot Regression Guard |

### Level 9 -- Architecture, Events, SLOs

| Feature | First Project |
|---------|---------------|
| Event-driven architecture | 01 Event Bus Prototype |
| Domain-driven design concepts | 02 Domain Model Boundary Lab |
| SLO (Service Level Objectives) | 03 Slo Budget Tracker |
| Feature flags | 04 Feature Flag Gate |
| Capacity planning | 05 Capacity Forecast Model |
| Dependency graphs | 06 Dependency Graph Walker |
| Change management | 08 Change Impact Analyzer |

### Level 10 -- Enterprise Patterns

| Feature | First Project |
|---------|---------------|
| Enterprise architecture | 01 Enterprise Python Blueprint |
| Orchestration patterns | 02 Autonomous Run Orchestrator |
| Policy-as-code | 03 Policy As Code Validator |
| Multi-tenancy | 04 Multi Tenant Data Guard |
| Compliance automation | 05 Compliance Evidence Builder |
| Chaos engineering | 06 Resilience Chaos Workbench |
| Zero-downtime migrations | 08 Zero Downtime Migration Lab |

## Key Standard Library Modules by Level

| Level | Modules |
|-------|---------|
| 00 | (none -- built-ins only) |
| 0 | `os`, `sys` |
| 1 | `csv`, `json`, `pathlib`, `argparse`, `datetime` |
| 2 | `collections`, `itertools` |
| 3 | `logging`, `configparser`, `unittest` |
| 4 | `re`, `hashlib`, `shutil`, `glob` |
| 5 | `sched`, `string`, `textwrap` |
| 6 | `sqlite3` |
| 7 | `http.server`, `urllib` |
| 8 | `concurrent.futures`, `cProfile`, `timeit` |
| 9 | `abc`, `dataclasses`, `functools` |
| 10 | `typing`, `contextlib`, `importlib` |

## Key Third-Party Packages by Level

| Level | Packages |
|-------|----------|
| 0-2 | `pytest`, `ruff`, `black` |
| 3 | `pyyaml`, `toml` |
| 4 | `pydantic` |
| 5 | `schedule`, `jinja2`, `python-dotenv` |
| 6 | `sqlalchemy`, `alembic` |
| 7 | `requests`, `httpx`, `structlog` |
| 8 | `matplotlib`, `rich` |
| 9 | `click`, `typer` |
| 10 | (all of the above combined) |

## Expansion Modules

| Module | Key Packages |
|--------|-------------|
| 01 Web Scraping | `requests`, `beautifulsoup4` |
| 02 CLI Tools | `click`, `typer`, `rich` |
| 03 REST APIs | `requests`, `httpx` |
| 04 FastAPI Web | `fastapi`, `uvicorn`, `pydantic` |
| 05 Async Python | `asyncio`, `aiohttp` |
| 06 Databases & ORM | `sqlalchemy`, `alembic` |
| 07 Data Analysis | `pandas`, `matplotlib` |
| 08 Advanced Testing | `pytest`, `hypothesis`, `responses` |
| 09 Docker Deployment | `docker`, `docker-compose` |
| 10 Django Fullstack | `django`, `djangorestframework` |
| 11 Package Publishing | `build`, `twine`, `setuptools` |
| 12 Cloud Deploy | `gunicorn`, `psycopg2` |

---

| [Home](README.md) |
|:---:|
