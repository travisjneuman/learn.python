# Module 01 / Project 05 — Save to CSV

[README](../../../../README.md) · [Module Index](../README.md)

## Focus

- `csv.DictWriter` for writing dictionaries to CSV
- Deduplicating scraped data by a key field
- Combining scraping and file output in one script
- Verifying output files

## Why this project exists

Scraping data is only half the job. You need to save it somewhere useful. CSV is the simplest structured file format and works with Excel, Google Sheets, pandas, and virtually every data tool. This project teaches you to write scraped data to a CSV file, handle duplicates, and verify the output. It combines everything from the previous four projects into one complete scraping pipeline.

## Run

```bash
cd projects/modules/01-web-scraping/05-save-to-csv
python project.py
```

## Expected output

```text
Scraping books from 2 pages of books.toscrape.com...
  Page 1: fetched 20 books. Sleeping 1 second...
  Page 2: fetched 20 books.

Collected 40 books total.
After deduplication: 40 unique books.

Writing to data/books.csv...
Wrote 40 rows to data/books.csv

Preview (first 3 rows):
  A Light in the Attic, £51.77, 3 star, In stock
  Tipping the Velvet, £53.74, 1 star, In stock
  Soumission, £50.10, 1 star, In stock

Done.
```

## Alter it

1. Add a `url` column to the CSV that includes each book's detail page link.
2. Change the script to scrape 3 pages instead of 2. Open the resulting CSV in a spreadsheet program or text editor and verify it has more rows.
3. Add a command-line argument (using `sys.argv`) that lets the user specify how many pages to scrape: `python project.py 5`.

## Break it

1. Change the output path to a directory that does not exist (e.g., `output/books.csv`). What error do you get?
2. Intentionally add duplicate entries by appending the same page's books twice. Does the deduplication catch them?
3. Open the CSV in a text editor and add a row manually with a comma in the title. Re-read it with Python's `csv.reader`. Does it parse correctly?

## Fix it

1. Before writing, create the output directory if it does not exist using `os.makedirs("data", exist_ok=True)`.
2. If duplicates are found, print how many were removed so the user knows.
3. Handle the case where scraping returns zero books: skip writing the CSV and print a warning instead of writing an empty file.

## Explain it

1. What is `csv.DictWriter` and why is it better than writing comma-separated strings manually?
2. How did you deduplicate the books? What key did you use and why?
3. What happens if a book title contains a comma? How does the CSV module handle that?
4. Why did we put the output in a `data/` subdirectory instead of the project root?

## Mastery check

You can move on when you can:

- Write a list of dicts to a CSV file from memory.
- Deduplicate a list of dicts by any key.
- Open and verify a CSV file you created.
- Explain why `csv.DictWriter` handles edge cases (commas, quotes) that manual string joining does not.

---

## Related Concepts

- [Api Basics](../../../../concepts/api-basics.md)
- [Collections Explained](../../../../concepts/collections-explained.md)
- [Files and Paths](../../../../concepts/files-and-paths.md)
- [How Loops Work](../../../../concepts/how-loops-work.md)
- [Quiz: Api Basics](../../../../concepts/quizzes/api-basics-quiz.py)

## Next

You have completed Module 01. Go back to the [Module Index](../README.md) or continue to the next module from the [Modules Overview](../../README.md).
