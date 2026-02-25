# Level 3 / Project 08 - Template Driven Reporter
Home: [README](../../../README.md)

## Focus
- report rendering from templates

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-3/08-template-driven-reporter
python project.py render report_template.txt report_data.json
python project.py discover report_template.txt
python project.py batch invoice_template.txt customers.json
pytest -q
```

## Expected terminal output
```text
===== Monthly Report =====
Company: Acme Corp
Period: January 2024
...
12 passed
```

## Expected artifacts
- Rendered report on stdout
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `--validate` flag that checks all variables are provided before rendering.
2. Add support for simple conditionals: `${if_debug}...${endif}`.
3. Add an `--output` flag to write rendered output to a file.

## Break it (required)
1. Use a template with a missing variable in strict mode — what happens?
2. Pass a data file with nested objects but no `build_report_context` flattening — what renders?
3. Use `$$` literal dollar signs in a template — does Template handle them?

## Fix it (required)
1. Add a `--missing` flag that lists all variables not provided by the data.
2. Improve `build_report_context` to handle deeper nesting (2+ levels).
3. Add error handling for invalid JSON in the data file.

## Explain it (teach-back)
1. How does `string.Template` differ from f-strings?
2. What is the difference between `substitute` and `safe_substitute`?
3. Why separate data from presentation (templates)?
4. How does `discover_variables` find placeholders in a template?

## Mastery check
You can move on when you can:
- use `string.Template` for safe text rendering,
- separate data from presentation in reports,
- discover and validate template variables,
- render templates for batch data (multiple records).

---

## Related Concepts

- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [How Imports Work](../../../concepts/how-imports-work.md)
- [Quiz: Errors and Debugging](../../../concepts/quizzes/errors-and-debugging-quiz.py)

---

| [← Prev](../07-batch-file-auditor/README.md) | [Home](../../../README.md) | [Next →](../09-reusable-utils-library/README.md) |
|:---|:---:|---:|
