# Expansion Modules

Home: [README](../../README.md)

These modules teach Python technologies beyond the enterprise operations ladder. Each module is self-contained with 3–5 projects that progress from basics to intermediate use. They use real libraries, not simulations.

## How to use these modules

1. Complete the prerequisite level listed for each module.
2. Create a virtual environment and install the module's dependencies: `pip install -r requirements.txt`
3. Work through projects in order (01 → 02 → 03 …).
4. Each project follows the same pattern: **run → alter → break → fix → explain**.

## Module index

| # | Module | Projects | Prerequisite | What you learn |
|---|--------|----------|-------------|----------------|
| 01 | [Web Scraping](./01-web-scraping/) | 5 | Level 2 | requests, BeautifulSoup, CSS selectors, pagination, CSV export |
| 02 | [CLI Tools](./02-cli-tools/) | 5 | Level 2 | click, typer, subcommands, interactive prompts, progress bars |
| 03 | [REST APIs — Consuming](./03-rest-apis/) | 5 | Level 2 | requests, JSON parsing, authentication, retries, API client design |
| 04 | [FastAPI Web Apps](./04-fastapi-web/) | 5 | Level 3 + Module 03 | FastAPI, Pydantic, uvicorn, CRUD endpoints, JWT auth |
| 05 | [Async Python](./05-async-python/) | 5 | Level 3 | async/await, asyncio, aiohttp, queues, concurrent tasks |
| 06 | [Databases & ORM](./06-databases-orm/) | 5 | Level 3 | sqlite3, SQLAlchemy, Alembic migrations, query optimization |
| 07 | [Data Analysis](./07-data-analysis/) | 5 | Level 2 | pandas, matplotlib, data cleaning, grouping, visualization |
| 08 | [Advanced Testing](./08-testing-advanced/) | 5 | Level 3 | parametrize, mocking, fixtures, hypothesis, integration tests |
| 09 | [Docker & Deployment](./09-docker-deployment/) | 5 | Level 5 | Dockerfile, multi-stage builds, docker-compose, GitHub Actions |
| 10 | [Django Full-Stack](./10-django-fullstack/) | 5 | Module 04 + Module 06 | Django models, views, templates, DRF, full CRUD app |
| 11 | [Package Publishing](./11-package-publishing/) | 3 | Level 3 | pyproject.toml, src layout, build, TestPyPI |
| 12 | [Cloud Deployment](./12-cloud-deploy/) | 3 | Module 04 + Module 09 | Railway/Render, Postgres, production checklist |

## Suggested order by learning phase

**After Level 2** (you know functions, files, basic testing):
- Module 01 — Web Scraping
- Module 02 — CLI Tools
- Module 03 — REST APIs
- Module 07 — Data Analysis

**After Level 3** (you know packages, error handling, project structure):
- Module 04 — FastAPI Web Apps
- Module 05 — Async Python
- Module 06 — Databases & ORM
- Module 08 — Advanced Testing
- Module 11 — Package Publishing

**After Level 5** (you know architecture, reliability, CI patterns):
- Module 09 — Docker & Deployment
- Module 10 — Django Full-Stack
- Module 12 — Cloud Deployment

## Virtual environments

Each module has its own `requirements.txt`. Create a virtual environment per module:

```bash
cd projects/modules/01-web-scraping
python -m venv .venv
source .venv/bin/activate    # macOS/Linux
.venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

See [concepts/virtual-environments.md](../../concepts/virtual-environments.md) for a full explanation.

---

| [← Prev](../elite-track/README.md) | [Home](../../README.md) | [Next →](../../10_CAPSTONE_PROJECTS.md) |
|:---|:---:|---:|
