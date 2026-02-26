# Test Driven Normalizer — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) before reading the solution.

---

## Complete Solution

```python
"""Level 3 project: Test Driven Normalizer."""

from __future__ import annotations

import argparse
import json
import logging
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


# WHY: the result dataclass captures both the cleaned value AND
# metadata (original, rule applied, whether it changed). This lets
# the caller generate reports without re-computing anything.
@dataclass
class NormalisationResult:
    """Result of normalising a single field."""
    original: str
    normalised: str
    rule_applied: str
    changed: bool


def normalise_whitespace(text: str) -> NormalisationResult:
    """Collapse multiple spaces/tabs into single spaces and strip edges.

    WHY: real-world data often has inconsistent whitespace from
    copy-paste, OCR, or manual entry. This is the most universally
    needed normaliser.
    """
    # WHY: \s+ matches any whitespace character (space, tab, newline)
    # one or more times, and replaces it with a single space.
    cleaned = re.sub(r"\s+", " ", text).strip()
    return NormalisationResult(
        original=text,
        normalised=cleaned,
        rule_applied="collapse_whitespace",
        changed=cleaned != text,
    )


def normalise_email(email: str) -> NormalisationResult:
    """Normalise an email address: lowercase, strip whitespace.

    WHY: email addresses are case-insensitive per RFC 5321,
    so lowercasing prevents duplicate accounts for the same person.
    """
    cleaned = email.strip().lower()
    return NormalisationResult(
        original=email,
        normalised=cleaned,
        rule_applied="lowercase_email",
        changed=cleaned != email,
    )


def normalise_phone(phone: str) -> NormalisationResult:
    """Extract digits from a phone string, format as (XXX) XXX-XXXX.

    WHY: phone numbers arrive in dozens of formats (555-867-5309,
    +1 555 867 5309, 5558675309). Stripping to digits first, then
    reformatting, handles all of them uniformly.
    """
    # WHY: \D matches any non-digit character. Removing all of them
    # reduces the problem to "do I have 10 or 11 digits?"
    digits = re.sub(r"\D", "", phone)

    # WHY: strip leading country code "1" if 11 digits.
    if len(digits) == 11 and digits[0] == "1":
        digits = digits[1:]

    if len(digits) == 10:
        formatted = f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    else:
        # WHY: return as-is rather than crashing — some numbers
        # are international or otherwise non-US. The caller can
        # check `changed == False` to detect these.
        formatted = phone.strip()

    return NormalisationResult(
        original=phone,
        normalised=formatted,
        rule_applied="us_phone_format",
        changed=formatted != phone,
    )


def normalise_name(name: str) -> NormalisationResult:
    """Title-case a person's name."""
    cleaned = name.strip()
    # WHY: .title() capitalises the first letter of each word.
    # Simple but imperfect — "mcdonald" becomes "Mcdonald" not "McDonald".
    # A production system would need a special-case lookup table.
    titled = cleaned.title()
    return NormalisationResult(
        original=name,
        normalised=titled,
        rule_applied="title_case_name",
        changed=titled != name,
    )


def normalise_date(date_str: str) -> NormalisationResult:
    """Normalise common date formats to YYYY-MM-DD (ISO 8601).

    WHY: ISO 8601 is the international standard, sorts correctly
    as a string, and is unambiguous (unlike MM/DD vs DD/MM).
    """
    date_str = date_str.strip()

    # WHY: each regex handles one known format. We try them in order
    # and stop at the first match. This is the "chain of responsibility"
    # pattern applied to parsing.

    # MM/DD/YYYY
    match = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{4})$", date_str)
    if match:
        mm, dd, yyyy = match.groups()
        # WHY: zfill(2) pads single digits — "1" becomes "01".
        normalised = f"{yyyy}-{mm.zfill(2)}-{dd.zfill(2)}"
        return NormalisationResult(date_str, normalised, "mm_dd_yyyy", True)

    # DD-MM-YYYY
    match = re.match(r"^(\d{1,2})-(\d{1,2})-(\d{4})$", date_str)
    if match:
        dd, mm, yyyy = match.groups()
        normalised = f"{yyyy}-{mm.zfill(2)}-{dd.zfill(2)}"
        return NormalisationResult(date_str, normalised, "dd_mm_yyyy", True)

    # YYYY.MM.DD
    match = re.match(r"^(\d{4})\.(\d{1,2})\.(\d{1,2})$", date_str)
    if match:
        yyyy, mm, dd = match.groups()
        normalised = f"{yyyy}-{mm.zfill(2)}-{dd.zfill(2)}"
        return NormalisationResult(date_str, normalised, "yyyy_mm_dd", True)

    # Already YYYY-MM-DD or unrecognised — return unchanged.
    return NormalisationResult(date_str, date_str, "no_change", False)


# WHY: the NORMALISERS registry maps field type names to functions.
# This is the same registry pattern used in the CLI workbench.
# Adding a new normaliser is one line here + one function above.
NORMALISERS = {
    "whitespace": normalise_whitespace,
    "email": normalise_email,
    "phone": normalise_phone,
    "name": normalise_name,
    "date": normalise_date,
}


def normalise_record(record: dict, field_types: dict[str, str]) -> dict:
    """Normalise all fields in a record according to field_types mapping.

    WHY: the field_types mapping decouples the schema from the code.
    The same functions work on any record shape — you just pass a
    different mapping.
    """
    result: dict = {}
    for field_name, value in record.items():
        normaliser_key = field_types.get(field_name)
        if normaliser_key and normaliser_key in NORMALISERS:
            nr = NORMALISERS[normaliser_key](str(value))
            result[field_name] = nr.normalised
            if nr.changed:
                logger.debug("Normalised %s: %r -> %r",
                             field_name, nr.original, nr.normalised)
        else:
            # WHY: pass through fields that are not in the mapping
            # unchanged. This preserves extra data.
            result[field_name] = value
    return result


def normalise_batch(
    records: list[dict],
    field_types: dict[str, str],
) -> list[dict]:
    """Normalise a batch of records, returning cleaned copies."""
    results = [normalise_record(r, field_types) for r in records]
    logger.info("Normalised %d records", len(results))
    return results


def build_parser() -> argparse.ArgumentParser:
    """Build CLI parser."""
    parser = argparse.ArgumentParser(description="Test-driven data normaliser")
    parser.add_argument("file", help="JSON file with records to normalise")
    parser.add_argument("--fields", required=True,
                        help="Comma-separated field:type pairs (e.g., email:email,name:name)")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--log-level", default="INFO")
    return parser


def main() -> None:
    """Entry point."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    parser = build_parser()
    args = parser.parse_args()

    # WHY: parse field types from CLI string into a dict.
    # "email:email,name:name" -> {"email": "email", "name": "name"}
    field_types: dict[str, str] = {}
    for pair in args.fields.split(","):
        parts = pair.strip().split(":")
        if len(parts) == 2:
            field_types[parts[0]] = parts[1]

    data = json.loads(Path(args.file).read_text(encoding="utf-8"))
    # WHY: handle both single-record and array JSON input.
    records = data if isinstance(data, list) else [data]

    normalised = normalise_batch(records, field_types)

    if args.json:
        print(json.dumps(normalised, indent=2))
    else:
        for i, rec in enumerate(normalised, 1):
            print(f"Record {i}:")
            for k, v in rec.items():
                print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| `NormalisationResult` with `changed` flag | Lets callers generate "what changed" reports without comparing before/after themselves. The metadata travels with the data. |
| NORMALISERS registry dict | Decouples the CLI and record-processing logic from the individual normalisers. New rules require zero changes to existing code. |
| Regex for date parsing instead of `datetime.strptime` | `strptime` is stricter and more correct for date validation, but regex shows the pattern more explicitly for learning purposes. Also handles partial dates without raising exceptions. |
| Pass-through for unmapped fields | Records often have fields beyond what we want to normalise. Dropping them silently would lose data. |
| Individual functions per normaliser | Each function is independently testable. TDD naturally produces this shape — you write one test, then one function. |

## Alternative Approaches

### Using `datetime.strptime` for date normalisation

```python
from datetime import datetime

FORMATS = ["%m/%d/%Y", "%d-%m-%Y", "%Y.%m.%d", "%Y-%m-%d"]

def normalise_date_strict(date_str: str) -> NormalisationResult:
    for fmt in FORMATS:
        try:
            dt = datetime.strptime(date_str.strip(), fmt)
            normalised = dt.strftime("%Y-%m-%d")
            return NormalisationResult(date_str, normalised, fmt, normalised != date_str)
        except ValueError:
            continue
    return NormalisationResult(date_str, date_str, "no_change", False)
```

**Trade-off:** This validates that dates are actually real (rejects "13/32/2024"), which regex alone cannot do. But it is less transparent — format strings like `%m/%d/%Y` are harder for beginners to read than explicit regex groups.

## Common Pitfalls

1. **Ambiguous date formats** — Is "01/02/2024" January 2nd or February 1st? The MM/DD/YYYY vs DD/MM/YYYY ambiguity is unsolvable without context. The code assumes MM/DD/YYYY for slash-separated dates. Document your assumption clearly.

2. **Normalising data that should not be normalised** — Title-casing "mcdonald" gives "Mcdonald" not "McDonald". Simple rules break on edge cases. For production, consider a lookup-based approach for known exceptions.

3. **Not testing with the `changed` flag** — Many TDD beginners test only the `normalised` output and forget to assert that `changed` is `True` or `False`. The `changed` flag is part of the contract.
