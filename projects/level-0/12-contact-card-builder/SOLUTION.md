# Solution: Level 0 / Project 12 - Contact Card Builder

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
"""Level 0 project: Contact Card Builder.

Read contact data from a file, build structured contact cards
(dictionaries), and save them to a JSON file.

Concepts: dictionaries, key-value pairs, string splitting, file I/O.
"""


import argparse
import json
from pathlib import Path


def parse_contact_line(line: str) -> dict:
    """Parse a comma-separated line into a contact dictionary.

    Expected format: name, phone, email
    Example: 'Ada Lovelace, 555-0101, ada@example.com'

    WHY split on comma? -- CSV (comma-separated values) is the simplest
    structured text format.  Each field is separated by a comma.
    """
    parts = line.split(",")

    # WHY check for 3 parts: The expected format has exactly 3 fields.
    # If fewer are provided, we cannot build a valid contact. Returning
    # an error dict (instead of crashing) lets the caller count errors
    # and continue processing the remaining lines.
    if len(parts) < 3:
        return {"raw": line.strip(), "error": "Expected: name, phone, email"}

    # WHY .strip() each part: CSV fields often have spaces after the comma.
    # "Ada Lovelace, 555-0101, ada@example.com" splits into
    # ["Ada Lovelace", " 555-0101", " ada@example.com"].
    # Stripping removes those leading spaces.
    name = parts[0].strip()
    phone = parts[1].strip()
    email = parts[2].strip()

    # WHY validate name: An empty name is probably a data error.
    if not name:
        return {"raw": line.strip(), "error": "Name is empty"}

    # WHY check for @: A minimal email validation.  Real email validation
    # is incredibly complex, but checking for @ catches the most obvious
    # mistakes (forgetting to include it).
    if "@" not in email:
        return {"raw": line.strip(), "error": f"Invalid email: {email}"}

    return {
        "name": name,
        "phone": phone,
        "email": email,
    }


def format_card(contact: dict) -> str:
    """Format a contact dict as a printable card.

    WHY a separate format function? -- It keeps display logic out of
    data logic.  We can change how cards look without touching parsing.
    """
    # WHY check for "error" key: parse_contact_line() returns error dicts
    # for bad input.  format_card() must handle both valid contacts and
    # error records gracefully.
    if "error" in contact:
        return f"  [ERROR] {contact['raw']} -- {contact['error']}"

    # WHY box-drawing with fixed widths: The border and field alignment
    # create a visual "card" that is easy to scan.  The :<10 and :<24
    # format specs left-align text within fixed-width columns.
    border = "+" + "-" * 36 + "+"
    lines = [
        border,
        f"| {'Name:':<10} {contact['name']:<24} |",
        f"| {'Phone:':<10} {contact['phone']:<24} |",
        f"| {'Email:':<10} {contact['email']:<24} |",
        border,
    ]
    return "\n".join(lines)


def load_contacts(path: Path) -> list[dict]:
    """Load and parse contacts from a file."""
    if not path.exists():
        raise FileNotFoundError(f"Contacts file not found: {path}")

    lines = path.read_text(encoding="utf-8").splitlines()
    contacts = []

    for line in lines:
        stripped = line.strip()
        # WHY skip empty lines: Blank lines between contacts are common
        # in text files.  Skipping them avoids false "Expected: name,
        # phone, email" errors.
        if not stripped:
            continue
        contacts.append(parse_contact_line(stripped))

    return contacts


def contacts_summary(contacts: list[dict]) -> dict:
    """Build a summary of the parsed contacts.

    WHY separate valid and errors? -- Knowing the error count tells the
    user whether their data file needs cleaning.  The valid contacts
    list is what gets saved to JSON.
    """
    valid = [c for c in contacts if "error" not in c]
    errors = [c for c in contacts if "error" in c]

    return {
        "total": len(contacts),
        "valid": len(valid),
        "errors": len(errors),
        "contacts": valid,
    }


def parse_args() -> argparse.Namespace:
    """Define command-line options."""
    parser = argparse.ArgumentParser(description="Contact Card Builder")
    parser.add_argument("--input", default="data/sample_input.txt")
    parser.add_argument("--output", default="data/contacts.json")
    return parser.parse_args()


def main() -> None:
    """Program entry point."""
    args = parse_args()

    contacts = load_contacts(Path(args.input))

    print("=== Contact Cards ===\n")
    for contact in contacts:
        print(format_card(contact))
        print()

    summary = contacts_summary(contacts)
    print(f"Parsed {summary['valid']} valid contacts ({summary['errors']} errors)")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Output written to {output_path}")


if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| `parse_contact_line()` returns error dicts instead of raising exceptions | The program continues processing remaining lines. A batch of 100 contacts with 3 errors still produces 97 valid cards | Raise `ValueError` — stops processing at the first error, losing all subsequent contacts |
| `format_card()` uses fixed-width alignment | `:<10` and `:<24` create uniform columns so all cards look the same regardless of content length | Variable-width cards — each card looks different, making them harder to scan visually |
| `load_contacts()` skips blank lines | Real CSV files often have blank lines between sections or at the end. Skipping them avoids false errors | Parse blank lines — creates error entries for empty lines, cluttering the report |
| CSV parsing with `split(",")` | Simplest possible approach for Level 0. No imports needed | Use the `csv` module — more robust (handles quoted fields, escaped commas) but introduces new concepts |

## Alternative approaches

### Approach B: Using the `csv` module for robust parsing

```python
import csv
import io

def load_contacts_csv(text: str) -> list[dict]:
    """Parse contacts using Python's csv module.

    The csv module handles edge cases like:
    - Fields containing commas: "Smith, Jr.", 555-0101, j@x.com
    - Quoted fields: '"Ada Lovelace"', 555-0101, ada@x.com
    """
    reader = csv.reader(io.StringIO(text))
    contacts = []
    for row in reader:
        if len(row) < 3:
            contacts.append({"raw": ",".join(row), "error": "Too few fields"})
            continue
        name, phone, email = row[0].strip(), row[1].strip(), row[2].strip()
        if "@" not in email:
            contacts.append({"raw": ",".join(row), "error": f"Invalid email: {email}"})
            continue
        contacts.append({"name": name, "phone": phone, "email": email})
    return contacts
```

**Trade-off:** The `csv` module handles quoted fields (e.g., names containing commas like "Smith, Jr.") and other CSV edge cases automatically. For production code, always use the `csv` module. At Level 0, manual `split(",")` teaches string manipulation fundamentals. Once you encounter real-world CSV files with edge cases, switching to the `csv` module is an easy upgrade.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Line has only a name, no phone or email | `parts` has fewer than 3 elements. Returns error dict: `"Expected: name, phone, email"` | Already handled by the `len(parts) < 3` check |
| Email is missing @ (e.g. `"alice-at-test.com"`) | Returns error dict: `"Invalid email: alice-at-test.com"` | Already handled by the `"@" not in email` check |
| Line has extra commas (e.g. `"Name, Role, email@x.com, , ,"`) | `split(",")` produces 6 parts. We take the first 3: name, phone (which is actually "Role"), email. The data is wrong but no crash | For robust parsing, use a proper CSV library or validate field content |
| Name contains a comma (e.g. `"Smith, Jr."`) | `split(",")` breaks "Smith" and "Jr." into separate fields. The phone field gets "Jr." and parsing is wrong | Use the `csv` module which handles quoted fields, or choose a different delimiter (like `|`) |
| File is entirely empty | `load_contacts()` returns `[]`. Summary shows 0 total, 0 valid, 0 errors | Already handled — the for loop simply does not execute |

## Key takeaways

1. **Structured data parsing follows a consistent pattern: split, validate, build.** Split the raw line into parts, check that the parts are valid, then assemble them into a clean data structure. This pattern appears in CSV parsing, log analysis, API response handling, and form processing.
2. **Error dicts let you continue processing despite bad data.** Instead of crashing on the first invalid record, returning `{"error": "..."}` lets the program process all records and report errors at the end. In real data pipelines, this is called "error collection" or "accumulating errors."
3. **Separating parsing from formatting keeps code flexible.** `parse_contact_line()` handles data extraction; `format_card()` handles visual presentation. You can add a new output format (JSON, HTML, CSV) without changing the parser. This separation of concerns is a core software engineering principle.
4. **String alignment with format specs creates professional output.** `f"{'Name:':<10}"` left-aligns "Name:" in a 10-character field. This is how tables, reports, and formatted output are built in Python. You will use alignment specs in dashboards, reports, and data displays.
