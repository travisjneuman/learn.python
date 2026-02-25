# Module 01 — Web Scraping

[README](../../../README.md)

## Overview

This module teaches you how to fetch web pages, parse HTML, extract structured data, handle pagination, and save results to CSV files. You will use real libraries (requests, BeautifulSoup) against a real website designed for scraping practice.

Every project targets [books.toscrape.com](http://books.toscrape.com), a safe sandbox site that exists specifically for people learning web scraping. You will not get in trouble for scraping it.

## Prerequisites

Complete **Level 2** before starting this module. You should be comfortable with:

- Functions and return values
- Reading and writing files
- Dictionaries and lists
- Basic testing with pytest
- Running scripts from the command line

## Learning objectives

By the end of this module you will be able to:

1. Fetch a web page with `requests` and inspect the response.
2. Parse HTML with BeautifulSoup and extract elements using tags, classes, and CSS selectors.
3. Build structured data (list of dicts) from scraped content.
4. Follow pagination links to scrape multiple pages with rate limiting.
5. Write scraped data to a CSV file using `csv.DictWriter`.

## Projects

| # | Project | What you learn |
|---|---------|----------------|
| 01 | [Fetch a Webpage](./01-fetch-a-webpage/) | `requests.get()`, status codes, response body |
| 02 | [Parse HTML](./02-parse-html/) | BeautifulSoup, `find()`, `find_all()`, CSS selectors |
| 03 | [Extract Structured Data](./03-extract-structured-data/) | Scraping tables, building list of dicts, star ratings |
| 04 | [Multi-Page Scraper](./04-multi-page-scraper/) | Pagination, `time.sleep()`, collecting across pages |
| 05 | [Save to CSV](./05-save-to-csv/) | `csv.DictWriter`, deduplication, file output |

Work through them in order. Each project builds on the previous one.

## Setup

Create a virtual environment and install dependencies before starting:

```bash
cd projects/modules/01-web-scraping
python -m venv .venv
source .venv/bin/activate    # macOS/Linux
.venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

See [concepts/virtual-environments.md](../../../concepts/virtual-environments.md) for a full explanation of virtual environments.

## Dependencies

This module requires three packages (listed in `requirements.txt`):

- **requests** — makes HTTP requests simple. You call `requests.get(url)` and get a response object back.
- **beautifulsoup4** — parses HTML into a tree you can search. The import name is `bs4`.
- **lxml** — a fast HTML/XML parser that BeautifulSoup uses under the hood.

## A note on web scraping ethics

Web scraping is a powerful tool, but it comes with responsibilities:

- Always check a site's `robots.txt` before scraping (e.g., `http://example.com/robots.txt`).
- Respect rate limits. Add delays between requests so you do not overload servers.
- Do not scrape personal data or content behind login walls without permission.
- The site we use in this module (books.toscrape.com) is explicitly designed for scraping practice.
