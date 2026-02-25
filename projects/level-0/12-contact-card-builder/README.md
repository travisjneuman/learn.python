# Level 0 / Project 12 - Contact Card Builder
Home: [README](../../../README.md)

## Focus
- dictionary creation and formatting

## Why this project exists
Parse comma-separated contact records into structured dictionaries and display them as formatted cards with box borders. You will practise string splitting, dictionary construction, and text alignment.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-0/12-contact-card-builder
python project.py --input data/sample_input.txt
pytest -q
```

## Expected terminal output
```text
=== Contact Cards ===

  +---------------------------+
  | Ada Lovelace              |
  | Phone: 555-0101           |
  | Email: ada@example.com    |
  +---------------------------+

Parsed 3 valid contacts (0 errors)
Output written to data/contacts.json
5 passed
```

## Expected artifacts
- `data/output.json`
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a phone number field (4th comma-separated value) to the contact card format.
2. Add a `--format` flag to choose between "card" (box drawing) and "csv" (plain comma-separated) output.
3. Re-run script and tests.

## Break it (required)
1. Add a line with only a name and no email like `John Smith` -- does `parse_contact_line()` raise `ValueError`?
2. Add a line with an invalid email like `alice@` -- does the email validator catch it?
3. Add a line with extra commas like `Name, Role, email@test.com, , ,` -- what happens?

## Fix it (required)
1. Ensure `parse_contact_line()` raises `ValueError` with a clear message for lines with fewer than 3 fields.
2. Improve email validation to reject emails without a domain part.
3. Add a test for the malformed-line edge case.

## Explain it (teach-back)
1. Why does `parse_contact_line()` use `.split(",")` and then `.strip()` each part?
2. What does the `"@" in email and "." in email` check actually validate (and what does it miss)?
3. Why does `format_card()` use box-drawing characters for the border?
4. Where would contact card parsing appear in real software (CRM imports, vCard generation, address books)?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Classes and Objects](../../../concepts/classes-and-objects.md)
- [Collections Explained](../../../concepts/collections-explained.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [Functions Explained](../../../concepts/functions-explained.md)
- [Quiz: Classes and Objects](../../../concepts/quizzes/classes-and-objects-quiz.py)

---

| [← Prev](../11-simple-menu-loop/README.md) | [Home](../../../README.md) | [Next →](../13-alarm-message-generator/README.md) |
|:---|:---:|---:|
