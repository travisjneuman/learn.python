"""Level 0 project: Contact Card Builder.

Read contact data from a file, build structured contact cards
(dictionaries), and save them to a JSON file.

Concepts: dictionaries, key-value pairs, string splitting, file I/O.
"""

from __future__ import annotations

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

    if len(parts) < 3:
        return {"raw": line.strip(), "error": "Expected: name, phone, email"}

    name = parts[0].strip()
    phone = parts[1].strip()
    email = parts[2].strip()

    # Basic validation.
    if not name:
        return {"raw": line.strip(), "error": "Name is empty"}
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
    if "error" in contact:
        return f"  [ERROR] {contact['raw']} -- {contact['error']}"

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
        if not stripped:
            continue
        contacts.append(parse_contact_line(stripped))

    return contacts


def contacts_summary(contacts: list[dict]) -> dict:
    """Build a summary of the parsed contacts."""
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
