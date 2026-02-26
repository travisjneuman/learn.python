# Level 3 / Project 04 - Test Driven Normalizer
Home: [README](../../../README.md)

> **Try in Browser:** [Practice similar concepts online](../../browser/level-2.html?ex=4) — browser exercises cover Level 2 topics

## Before You Start

Recall these prerequisites before diving in:
- Can you write a pytest test function that uses `assert`?
- Can you explain what TDD (test-driven development) means? (Write the test first, then the code)

## Focus
- write tests before transform logic

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-3/04-test-driven-normalizer
pytest -q
python project.py contacts.json --fields "email:email,name:name,phone:phone" --json
```

## Expected terminal output
```text
14 passed
[{"name": "Jane Doe", "email": "jane.doe@example.com", ...}]
```

## Expected artifacts
- Normalised records on stdout
- All tests passing (written before implementation — TDD)
- Updated `notes.md`

## Alter it (required)
1. Add a `normalise_zip_code` function that pads US ZIP codes to 5 digits.
2. Add a `--report` flag that shows which fields were changed.
3. Add support for nested field types: `"address.zip:zip_code"`.

## Break it (required)
1. Pass a phone number with letters ("555-HELP") — what happens?
2. Pass a date in an unsupported format ("Jan 15, 2024") — does it error or pass through?
3. Pass an empty JSON array — does the batch normaliser handle it?

## Fix it (required)
1. Add graceful handling for unparseable phone numbers.
2. Add a fallback for unrecognised date formats (return as-is with a warning).
3. Validate that field_types reference real normaliser keys.

## Explain it (teach-back)
1. What is TDD and how does writing tests first change your design?
2. How does the `NORMALISERS` registry pattern work?
3. Why return a `NormalisationResult` dataclass instead of just the cleaned string?
4. What is `@pytest.mark.parametrize` and when should you use it?

## Mastery check
You can move on when you can:
- write tests before implementation (TDD workflow),
- build a registry of normalisation functions,
- use `@dataclass` for function return values,
- use `pytest.mark.parametrize` for table-driven tests.

---

## Related Concepts

- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [How Loops Work](../../../concepts/how-loops-work.md)
- [Quiz: Errors and Debugging](../../../concepts/quizzes/errors-and-debugging-quiz.py)

---

## Stuck? Ask AI

If you are stuck after trying for 20 minutes, use one of these prompts:

- "I am working on Test Driven Normalizer. I got this error: [paste error]. Can you explain what this error means without giving me the fix?"
- "I am trying to write tests before writing the code. Can you explain the Red-Green-Refactor cycle of TDD with a simple example?"
- "Can you explain how `pytest.mark.parametrize` works with a simple example that is not about data normalization?"

---

| [← Prev](../03-logging-baseline-tool/README.md) | [Home](../../../README.md) | [Next →](../05-refactor-monolith-drill/README.md) |
|:---|:---:|---:|
