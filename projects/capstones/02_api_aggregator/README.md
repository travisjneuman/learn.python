# Capstone 02 — API Aggregator

## Brief

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

Build a tool that pulls data from 2-3 public APIs, normalizes the results into a common format, and presents a unified dashboard or report.

## Requirements

### Core (must have)

- **Fetch from multiple APIs:** Use at least 2 of these free, no-auth-required APIs (or similar):
  - Weather: Open-Meteo (`open-meteo.com/en/docs`)
  - News: various free news APIs
  - Quotes: quotable.io or similar
  - Facts: uselessfacts.jsph.pl or similar
  - GitHub: `api.github.com` (public endpoints)
- **Normalize data:** Each API returns different JSON shapes. Transform them into a common schema so they can be displayed together.
- **Unified output:** Present all data in a single dashboard (terminal output, formatted text, or simple HTML file).
- **Error handling:** If one API is down, the dashboard should still show data from the others (graceful degradation).
- **Caching:** Cache API responses so repeated runs within N minutes do not re-fetch (save to a local file).

### Stretch (pick at least one)

- **Rate limiting:** Respect API rate limits. Implement a simple rate limiter that waits between requests if needed.
- **Async fetching:** Use `asyncio` and `aiohttp` to fetch from all APIs concurrently.
- **Configuration file:** Let the user configure which APIs to use, refresh intervals, and display preferences via a YAML or JSON config file.
- **Historical comparison:** Store fetched data over time and show trends (e.g., "temperature this week").

## Constraints

- Python 3.11+. Use `requests` or `urllib` for HTTP (or `aiohttp` for async stretch goal).
- Must handle network errors without crashing.
- Must include tests. Mock the API calls in tests so they run without internet.

## Deliverables

- Working application code
- Tests (`python -m pytest tests/`)
- Filled-out `notes.md` with your design decisions
- A `requirements.txt` listing any external packages

## Architecture decisions are yours

There is no starter code. You decide how to structure fetchers, normalizers, the cache layer, and the display layer. Fill out `notes.md` before you start coding.
