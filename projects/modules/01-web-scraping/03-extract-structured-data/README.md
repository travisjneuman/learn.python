# Module 01 / Project 03 — Extract Structured Data

[README](../../../../README.md) · [Module Index](../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus

- Scraping multiple fields per item
- Building a list of dictionaries from scraped data
- Mapping CSS classes to meaningful values (star ratings)
- Printing formatted tabular output

## Why this project exists

Scraping one field at a time is useful for learning, but real scraping tasks require extracting multiple fields per item and organizing them into structured data. This project teaches you to build a list of dictionaries — the standard Python data structure for tabular data — from a scraped page. You will extract title, price, rating, and availability for every book on the page.

## Run

```bash
cd projects/modules/01-web-scraping/03-extract-structured-data
python project.py
```

## Expected output

```text
Fetching http://books.toscrape.com/ ...
Parsing page and extracting book data...

 #  Title                                    Price    Rating  Available
--- ---------------------------------------- -------- ------- ---------
  1 A Light in the Attic                     £51.77   3 star  In stock
  2 Tipping the Velvet                       £53.74   1 star  In stock
  3 Soumission                               £50.10   1 star  In stock
...
 20 (last title)                             £XX.XX   X star  In stock

Extracted 20 books with 4 fields each.
Done.
```

## Alter it

1. Add a fifth field: the book's detail page URL (the `href` attribute). Include it in each dictionary and print it as an extra column.
2. Filter the output to only show books rated 4 or 5 stars. Print how many books were filtered out.
3. Sort the books by price (lowest first) before printing. You will need to convert the price string to a float — strip the pound sign first.

## Break it

1. Change the rating mapping so it is missing one entry (e.g., remove "Three"). What happens when a book with that rating is processed?
2. Try to convert a price string to a float without removing the pound sign. What error do you get?
3. Change `find_all("article")` to `find_all("div")`. Does it still work? Why or why not?

## Fix it

1. Add a fallback for unknown ratings: if the rating class is not in your mapping, set it to 0 instead of crashing.
2. Use `price_text.replace("£", "")` or `price_text[1:]` to strip the currency symbol before converting to float.
3. Add a check: if `find_all()` returns an empty list, print a warning that the page structure may have changed.

## Explain it

1. Why is a list of dictionaries a good data structure for scraped data?
2. How did you map CSS class names (like "Three") to numeric values?
3. What would happen if the website changed its HTML structure? How would you detect that?
4. Why is it important to strip non-numeric characters before converting strings to numbers?

## Mastery check

You can move on when you can:

- Scrape multiple fields from each item on a page and store them as dicts.
- Map CSS classes or HTML attributes to meaningful values.
- Handle missing or unexpected values without crashing.
- Print structured data in a readable table format.

---

## Related Concepts

- [Api Basics](../../../../concepts/api-basics.md)
- [Classes and Objects](../../../../concepts/classes-and-objects.md)
- [Collections Explained](../../../../concepts/collections-explained.md)
- [Files and Paths](../../../../concepts/files-and-paths.md)
- [Quiz: Api Basics](../../../../concepts/quizzes/api-basics-quiz.py)

## Next

[Project 04 — Multi-Page Scraper](../04-multi-page-scraper/)
