"""Level 1 project: Input Validator Lab.

Validate common input formats: email addresses, phone numbers,
and zip codes using string methods (no regex at this level).

Concepts: string methods (find, count, isdigit), validation patterns, re basics.
"""


import argparse
import json
import re
from pathlib import Path


def validate_email(email: str) -> dict:
    """Check whether a string looks like a valid email address.

    Rules:
    - Must contain exactly one @
    - Must have text before and after the @
    - The part after @ must contain at least one dot
    - No spaces allowed

    WHY string methods first? -- Before learning regex, you can do
    a lot of validation with find(), count(), and split().
    """
    email = email.strip()
    errors = []

    if " " in email:
        errors.append("contains spaces")
    if email.count("@") != 1:
        errors.append("must contain exactly one @")
    elif "@" in email:
        local, domain = email.split("@")
        if not local:
            errors.append("nothing before @")
        if not domain or "." not in domain:
            errors.append("domain must contain a dot")

    return {"value": email, "type": "email", "valid": len(errors) == 0, "errors": errors}


def validate_phone(phone: str) -> dict:
    """Check whether a string looks like a US phone number.

    Accepts: 555-123-4567, 5551234567, (555) 123-4567
    Must have exactly 10 digits after stripping formatting.
    """
    phone = phone.strip()
    # Extract only digits.
    digits = ""
    for char in phone:
        if char.isdigit():
            digits += char

    errors = []
    if len(digits) != 10:
        errors.append(f"expected 10 digits, got {len(digits)}")

    return {"value": phone, "type": "phone", "valid": len(errors) == 0, "errors": errors}


def validate_zip_code(zipcode: str) -> dict:
    """Check whether a string looks like a US zip code.

    Accepts: 12345 or 12345-6789
    """
    zipcode = zipcode.strip()
    errors = []

    # Use a simple regex pattern for zip codes.
    pattern = r"^\d{5}(-\d{4})?$"
    if not re.match(pattern, zipcode):
        errors.append("must be 5 digits or 5+4 format (12345-6789)")

    return {"value": zipcode, "type": "zip", "valid": len(errors) == 0, "errors": errors}


def validate_input(line: str) -> dict:
    """Parse a line like 'email: user@example.com' and validate it.

    WHY a dispatcher? -- The line tells us which validator to use.
    This pattern scales: add a new type, add a new validator.
    """
    if ":" not in line:
        return {"raw": line.strip(), "error": "Expected format: type: value"}

    input_type, value = line.split(":", maxsplit=1)
    input_type = input_type.strip().lower()
    value = value.strip()

    validators = {
        "email": validate_email,
        "phone": validate_phone,
        "zip": validate_zip_code,
    }

    if input_type not in validators:
        return {"raw": line.strip(), "error": f"Unknown type: {input_type}"}

    return validators[input_type](value)


def process_file(path: Path) -> list[dict]:
    """Read input lines and validate each one."""
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    lines = path.read_text(encoding="utf-8").splitlines()
    results = []
    for line in lines:
        if not line.strip():
            continue
        results.append(validate_input(line))
    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Input Validator Lab")
    parser.add_argument("--input", default="data/sample_input.txt")
    parser.add_argument("--output", default="data/output.json")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    results = process_file(Path(args.input))

    print("=== Validation Results ===\n")
    for r in results:
        if "error" in r:
            print(f"  PARSE ERROR: {r['error']}")
        elif r["valid"]:
            print(f"  PASS  [{r['type']}] {r['value']}")
        else:
            print(f"  FAIL  [{r['type']}] {r['value']} -- {', '.join(r['errors'])}")

    valid_count = sum(1 for r in results if r.get("valid", False))
    print(f"\n  {valid_count}/{len(results)} passed validation")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(results, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
