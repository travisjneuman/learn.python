"""Level 3 project: Test Driven Normalizer.

Demonstrates TDD workflow: write tests first, then implement normalisation
functions that clean and standardise data fields.

Skills practiced: pytest-first workflow, dataclasses, typing basics,
logging, re module, string manipulation.
"""

from __future__ import annotations

import argparse
import json
import logging
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class NormalisationResult:
    """Result of normalising a single field."""
    original: str
    normalised: str
    rule_applied: str
    changed: bool


def normalise_whitespace(text: str) -> NormalisationResult:
    """Collapse multiple spaces/tabs into single spaces and strip edges.

    'hello   world ' -> 'hello world'
    """
    cleaned = re.sub(r"\s+", " ", text).strip()
    return NormalisationResult(
        original=text,
        normalised=cleaned,
        rule_applied="collapse_whitespace",
        changed=cleaned != text,
    )


def normalise_email(email: str) -> NormalisationResult:
    """Normalise an email address: lowercase, strip whitespace.

    ' User@Example.COM ' -> 'user@example.com'
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

    '1-555-867-5309' -> '(555) 867-5309'
    Only works for 10- or 11-digit US numbers.
    """
    digits = re.sub(r"\D", "", phone)

    # Strip leading country code '1' if 11 digits.
    if len(digits) == 11 and digits[0] == "1":
        digits = digits[1:]

    if len(digits) == 10:
        formatted = f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    else:
        formatted = phone.strip()  # Can't normalise — return as-is.

    return NormalisationResult(
        original=phone,
        normalised=formatted,
        rule_applied="us_phone_format",
        changed=formatted != phone,
    )


def normalise_name(name: str) -> NormalisationResult:
    """Title-case a person's name, handling edge cases.

    'JANE DOE' -> 'Jane Doe'
    'mcdonald' -> 'Mcdonald' (simple title case)
    """
    cleaned = name.strip()
    titled = cleaned.title()
    return NormalisationResult(
        original=name,
        normalised=titled,
        rule_applied="title_case_name",
        changed=titled != name,
    )


def normalise_date(date_str: str) -> NormalisationResult:
    """Normalise common date formats to YYYY-MM-DD.

    Supports: MM/DD/YYYY, DD-MM-YYYY, YYYY.MM.DD
    """
    date_str = date_str.strip()

    # MM/DD/YYYY
    match = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{4})$", date_str)
    if match:
        mm, dd, yyyy = match.groups()
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

    # Already YYYY-MM-DD or unrecognised.
    return NormalisationResult(date_str, date_str, "no_change", False)


# Registry of all normalisation rules by field type.
NORMALISERS = {
    "whitespace": normalise_whitespace,
    "email": normalise_email,
    "phone": normalise_phone,
    "name": normalise_name,
    "date": normalise_date,
}


def normalise_record(record: dict, field_types: dict[str, str]) -> dict:
    """Normalise all fields in a record according to field_types mapping.

    field_types maps field names to normaliser keys, e.g.:
    {"email": "email", "full_name": "name", "phone": "phone"}
    """
    result: dict = {}
    for field_name, value in record.items():
        normaliser_key = field_types.get(field_name)
        if normaliser_key and normaliser_key in NORMALISERS:
            nr = NORMALISERS[normaliser_key](str(value))
            result[field_name] = nr.normalised
            if nr.changed:
                logger.debug("Normalised %s: %r -> %r", field_name, nr.original, nr.normalised)
        else:
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

    # Parse field types from CLI: "email:email,name:name,phone:phone"
    field_types: dict[str, str] = {}
    for pair in args.fields.split(","):
        parts = pair.strip().split(":")
        if len(parts) == 2:
            field_types[parts[0]] = parts[1]

    data = json.loads(Path(args.file).read_text(encoding="utf-8"))
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
