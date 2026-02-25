# Flashcards — Spaced Repetition Review

Flashcard decks for each curriculum level. Cards test recall of key concepts, syntax patterns, and common pitfalls.

## Quick Start

```bash
# Review all due cards
python practice/flashcards/review-runner.py

# Review a specific level
python practice/flashcards/review-runner.py --level 0

# See your stats
python practice/flashcards/review-runner.py --stats
```

## How It Works

The runner uses the **Leitner box system**:

| Box | Review Interval | Meaning |
|-----|----------------|---------|
| 1 | Every session | New or recently wrong |
| 2 | Every 2 days | Getting it |
| 3 | Every 4 days | Know it |
| 4 | Every 8 days | Solid |
| 5 | Every 16 days | Mastered |

- **Correct answer** → card moves up one box
- **Wrong answer** → card drops back to box 1
- Cards are shown front-first; you think of the answer, then press Enter to reveal

## Card Decks

### Core Levels

| File | Level | Cards | Topics |
|------|-------|-------|--------|
| `level-00-cards.json` | Absolute Beginner | 25 | Variables, print, input, basic types |
| `level-0-cards.json` | Terminal & I/O | 25 | File I/O, string methods, loops, conditionals |
| `level-1-cards.json` | Functions | 25 | def, return, scope, parameters, docstrings |
| `level-2-cards.json` | Collections | 25 | Lists, dicts, sets, comprehensions, sorting |
| `level-3-cards.json` | File Automation | 25 | pathlib, os, shutil, glob, CSV |
| `level-4-cards.json` | JSON & Data | 25 | json module, nested data, schemas, validation |
| `level-5-cards.json` | Exceptions | 25 | try/except, custom exceptions, logging, context managers |
| `level-6-cards.json` | SQL & ETL | 25 | SQL, staging areas, ETL patterns, idempotent operations, data integrity |
| `level-7-cards.json` | API Integration | 25 | API adapters, caching, polling, observability, rate limiting, contracts |
| `level-8-cards.json` | Dashboards & Resilience | 25 | Concurrency, thread safety, fault injection, graceful degradation, SLAs |
| `level-9-cards.json` | Architecture & Governance | 25 | Architecture patterns, SLOs, capacity planning, security, design principles |
| `level-10-cards.json` | Enterprise Excellence | 25 | Enterprise patterns, compliance, production readiness, operational excellence |

### Expansion Modules

| File | Module | Cards | Topics |
|------|--------|-------|--------|
| `module-web-scraping-cards.json` | Web Scraping | 15 | requests, BeautifulSoup, CSS selectors, pagination, robots.txt, CSV |
| `module-fastapi-cards.json` | FastAPI Web Apps | 17 | FastAPI, Pydantic, path/query params, dependency injection, JWT, uvicorn |
| `module-databases-cards.json` | Databases & ORM | 17 | sqlite3, SQLAlchemy Core/ORM, sessions, Alembic migrations, query optimization |
| `module-django-cards.json` | Django Full-Stack | 18 | Django models, views, templates, URL routing, DRF serializers, admin |

## Card Format

Each card has:
- **front**: The question or prompt
- **back**: The answer
- **concept_ref**: Link to the relevant concept doc
- **difficulty**: 1 (easy), 2 (medium), 3 (hard)
- **tags**: Topic labels for filtering

## Progress File

Your review progress is saved to `practice/flashcards/.review-state.json` (git-ignored). This tracks which box each card is in and when it's due for review.

## Tips

- Review daily, even for just 5 minutes
- Don't peek at the back — test yourself honestly
- If a card is too easy, you'll naturally see it less often
- If you keep getting one wrong, go back to the concept doc

---

| [← Prev](../../concepts/functions-explained.md) | [Home](../../README.md) | [Next →](../challenges/README.md) |
|:---|:---:|---:|
