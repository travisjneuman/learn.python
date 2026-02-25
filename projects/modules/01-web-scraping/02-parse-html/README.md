# Module 01 / Project 02 — Parse HTML

[README](../../../../README.md) · [Module Index](../README.md)

## Focus

- Creating a BeautifulSoup object from HTML
- `find()` and `find_all()` to locate elements
- CSS selectors with `select()`
- Extracting text and attributes from elements

## Why this project exists

Raw HTML is a mess of tags, attributes, and nesting. BeautifulSoup turns that mess into a tree structure you can search. This project teaches you to find specific elements on a page — the single most important skill in web scraping. You will extract book titles and prices from a real webpage.

## Run

```bash
cd projects/modules/01-web-scraping/02-parse-html
python project.py
```

## Expected output

```text
Fetching http://books.toscrape.com/ ...
Parsing HTML with BeautifulSoup...

Found 20 books on the page:

  1. A Light in the Attic                         £51.77
  2. Tipping the Velvet                            £53.74
  3. Soumission                                    £50.10
  ...
 20. (last book title)                             £XX.XX

Done. Extracted 20 books.
```

The exact titles and prices depend on the current page content, but you should see 20 books listed.

## Alter it

1. Instead of printing the price, print the star rating. Each book has a `<p>` tag with a class like `star-rating Three`. Extract and print the rating word (One, Two, Three, etc.).
2. Use `soup.select()` with a CSS selector instead of `find_all()`. For example, `soup.select("article.product_pod h3 a")` selects all title links. Try rewriting the extraction using only CSS selectors.
3. Extract and print the URL of each book's detail page (the `href` attribute on the title link).

## Break it

1. Change the parser from `"lxml"` to `"html.parser"` (Python's built-in). Does the output change? What if the HTML were malformed — which parser would handle it better?
2. Search for a tag that does not exist: `soup.find("div", class_="nonexistent")`. What does it return? What happens if you try to call `.text` on that result?
3. Remove the `import` for BeautifulSoup and run the script. Read the error.

## Fix it

1. Before calling `.text` on a found element, add a check: `if element is not None`. Print "Not found" if the element is missing.
2. If the page fetch fails (status code is not 200), skip the parsing step entirely and print an error message.
3. Restore any imports you removed.

## Explain it

1. What does `BeautifulSoup(html, "lxml")` do? What is the second argument for?
2. What is the difference between `find()` and `find_all()`?
3. How do you get the text content of a tag? How do you get an attribute like `href`?
4. What is a CSS selector and why might you prefer `select()` over `find_all()`?

## Mastery check

You can move on when you can:

- Parse any HTML string with BeautifulSoup without looking up the syntax.
- Find elements by tag name, class, and CSS selector.
- Extract both text content and attributes from elements.
- Handle the case where an element is not found on the page.

## Next

[Project 03 — Extract Structured Data](../03-extract-structured-data/)
