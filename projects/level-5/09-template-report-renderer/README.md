# Level 5 / Project 09 - Template Report Renderer
Home: [README](../../../README.md)

## Focus
- report generation by template blocks

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-5/09-template-report-renderer
python project.py --template data/report_template.txt --data data/report_data.json --output data/rendered_report.txt
pytest -q
```

## Expected terminal output
```text
Report rendered: 25 lines written
7 passed
```

## Expected artifacts
- `data/rendered_report.txt`
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add `{{IF NOT condition}}...{{END IF}}` blocks for negated conditionals.
2. Add a `{{DATE}}` placeholder that inserts the current date.
3. Support nested variable access like `{{config.max_retries}}`.
4. Re-run script and tests.

## Break it (required)
1. Use a template with `{{variable}}` that is not in the data JSON.
2. Create an `{{EACH items}}` block where `items` is not a list.
3. Capture the first failing test or visible bad output.

## Fix it (required)
1. Replace missing variables with `[MISSING: variable]` instead of crashing.
2. Skip `EACH` blocks when the data is not iterable, with a warning.
3. Add tests for missing variables and non-iterable EACH data.
4. Re-run until output and tests are deterministic.

## Explain it (teach-back)
1. How does `render_variables` find and replace `{{name}}` placeholders?
2. Why are `EACH` blocks processed before `IF` blocks?
3. What regex pattern matches the `{{EACH items}}...{{END EACH}}` block?
4. Where do you see template engines in production (Jinja2, Handlebars, Mustache)?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Classes and Objects](../../../concepts/classes-and-objects.md)
- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Quiz: Classes and Objects](../../../concepts/quizzes/classes-and-objects-quiz.py)

---

| [← Prev](../08-cross-file-joiner/README.md) | [Home](../../../README.md) | [Next →](../10-api-polling-simulator/README.md) |
|:---|:---:|---:|
