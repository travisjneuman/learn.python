# Level 2 / Project 10 - Mock API Response Parser
Home: [README](../../../README.md)

## Focus
- parse response-like payloads

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-2/10-mock-api-response-parser
python project.py data/sample_input.txt
python project.py data/sample_input.txt --validate status data message
python project.py data/sample_input.txt --group role
pytest -q
```

## Expected terminal output
```text
Status: {'status': 200, 'category': 'success'}
{"count": 5, "fields": ["active", "id", "name", "role"], ...}
11 passed
```

## Expected artifacts
- Parsed response summary on stdout
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `--filter` flag: `--filter active=true` to show only matching items.
2. Add support for paginated responses (read `pagination.total_pages`).
3. Add a `--status-only` flag that just checks and prints the status category.

## Break it (required)
1. Feed a file with a JSON array at the root instead of an object.
2. Feed a response where `data` is a string instead of a list.
3. Pass a response with no `status` field at all.

## Fix it (required)
1. Handle non-object JSON roots (wrap arrays in a response dict).
2. Guard against non-list data values in `extract_items`.
3. Return a clear message when status code is missing.

## Explain it (teach-back)
1. What makes a JSON response "valid" beyond just being parseable JSON?
2. How do HTTP status code ranges (2xx, 4xx, 5xx) map to outcomes?
3. Why is `dict.get(key, default)` safer than `dict[key]` for API data?
4. What is the pagination pattern and why do APIs use it?

## Mastery check
You can move on when you can:
- parse a nested JSON response and extract specific fields,
- validate response structure against a schema,
- categorise HTTP status codes from memory,
- handle missing or malformed API data gracefully.

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Collections Explained](../../../concepts/collections-explained.md)
- [Functions Explained](../../../concepts/functions-explained.md)
- [How Loops Work](../../../concepts/how-loops-work.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../09-config-driven-calculator/README.md) | [Home](../../../README.md) | [Next →](../11-retry-loop-practice/README.md) |
|:---|:---:|---:|
