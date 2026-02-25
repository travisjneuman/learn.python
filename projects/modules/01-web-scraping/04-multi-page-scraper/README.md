# Module 01 / Project 04 — Multi-Page Scraper

[README](../../../../README.md) · [Module Index](../README.md)

## Focus

- Constructing URLs for paginated content
- Looping over multiple pages
- Rate limiting with `time.sleep()`
- Aggregating results across pages

## Why this project exists

Most websites split content across many pages. A scraper that only reads the first page misses most of the data. This project teaches you to follow pagination links, respect rate limits so you do not hammer the server, and combine results from multiple pages into one collection. These are the patterns that separate a toy script from a useful scraper.

## Run

```bash
cd projects/modules/01-web-scraping/04-multi-page-scraper
python project.py
```

## Expected output

```text
Scraping books from 3 pages of books.toscrape.com...

Page 1: http://books.toscrape.com/catalogue/page-1.html
  Found 20 books. Sleeping 1 second...
Page 2: http://books.toscrape.com/catalogue/page-2.html
  Found 20 books. Sleeping 1 second...
Page 3: http://books.toscrape.com/catalogue/page-3.html
  Found 20 books.

Total books collected: 60

Sample (first 5):
  1. A Light in the Attic — £51.77
  2. Tipping the Velvet — £53.74
  3. Soumission — £50.10
  4. Sharp Objects — £47.82
  5. Sapiens: A Brief History of Humankind — £54.23

Done.
```

## Alter it

1. Change the number of pages to scrape from 3 to 5. Verify you get 100 books.
2. Increase the sleep time to 2 seconds. Time the full run with `time python project.py` (on Linux/macOS) or measure manually on Windows. How much slower is it?
3. Add a progress indicator that prints `[2/5]` style counts before each page URL.

## Break it

1. Change a page URL to `page-999.html` (a page that does not exist). What status code do you get? Does your script crash or silently collect zero books?
2. Remove the `time.sleep()` call. The script still works against this practice site, but discuss: why is rate limiting important when scraping real websites?
3. Set the number of pages to 0. Does your script handle that edge case?

## Fix it

1. Before parsing each page, check the status code. If it is not 200, print a warning and skip that page instead of crashing.
2. After the loop, check if you collected zero books total. If so, print a message suggesting the URLs may be wrong.
3. Handle the case where the user sets pages to 0: print "Nothing to scrape" and exit cleanly.

## Explain it

1. How did you construct the URL for each page? Why is string formatting useful here?
2. What is rate limiting and why does it matter in web scraping?
3. What would happen if you scraped 1000 pages with no delay? (Think about the server, not your script.)
4. How do you combine lists from multiple pages into one list in Python?

## Mastery check

You can move on when you can:

- Build paginated URLs with f-strings or `.format()`.
- Scrape multiple pages in a loop with rate limiting.
- Handle pages that fail to load without crashing the entire run.
- Explain why rate limiting is an ethical requirement, not just a technical one.

## Next

[Project 05 — Save to CSV](../05-save-to-csv/)
