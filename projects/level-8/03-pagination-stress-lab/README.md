# Level 8 / Project 03 - Pagination Stress Lab
Home: [README](../../../README.md)

## Focus
- Offset-based and cursor-based pagination strategies
- Edge case handling: empty pages, beyond-range, partial last page
- Stress testing with multiple page sizes
- Invariant verification (no duplicates, no missing items)

## Why this project exists
Pagination bugs are among the most common issues in web APIs. Off-by-one errors, empty
last pages, and item drift during inserts all cause real production incidents. This lab
builds both offset and cursor paginators, then stress-tests them to verify correctness.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-8/03-pagination-stress-lab
python project.py --items 47 --page-sizes 1 5 10 25 100
pytest -q
```

## Expected terminal output
```text
{
  "data_size": 47,
  "page_sizes_tested": [1, 5, 10, 25, 100],
  "verification": [{"page_size": 1, "matches_total": true}, ...],
  ...
}
7 passed
```

## Alter it (required)
1. Add a `--sort-descending` flag that reverses the data before paginating.
2. Implement a `seek_to_item(item)` method that returns the page containing that item.
3. Add response time tracking to the stress test and flag slow pages.

## Break it (required)
1. Pass `page_size=0` — does the paginator crash or return infinity pages?
2. Insert items mid-iteration — does offset pagination skip or duplicate items?
3. Request page 1 of an empty dataset — is the response well-formed?

## Fix it (required)
1. Add validation that page_size >= 1 in `total_pages()`.
2. Handle empty datasets gracefully (total_pages should be 1, not 0).
3. Write a test that verifies no duplicates when iterating all pages.

## Explain it (teach-back)
1. What is the "page drift" problem and how does cursor pagination solve it?
2. Why does the stress test go one page beyond total_pages?
3. When would you choose cursor-based over offset-based pagination?
4. How do databases like PostgreSQL implement `LIMIT ... OFFSET`?

## Mastery check
You can move on when you can:
- explain why math.ceil is needed for total_pages,
- describe the tradeoff between offset and cursor pagination,
- write a stress test that catches off-by-one errors,
- explain why the last page often has fewer items than page_size.

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Async Explained](../../../concepts/async-explained.md)
- [Http Explained](../../../concepts/http-explained.md)
- [The Terminal Deeper](../../../concepts/the-terminal-deeper.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../02-query-cache-layer/README.md) | [Home](../../../README.md) | [Next →](../04-filter-state-manager/README.md) |
|:---|:---:|---:|
