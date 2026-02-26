# Solution: Level 1 / Project 01 - Input Validator Lab

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [Walkthrough](./WALKTHROUGH.md) first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
"""Level 1 project: Input Validator Lab.

Validate common input formats: email addresses, phone numbers,
and zip codes using string methods (no regex at this level).

Concepts: string methods (find, count, isdigit), validation patterns, re basics.
"""


import argparse
import json
import re
from pathlib import Path


# WHY validate_email: Emails are the most common user-submitted data on
# the web.  Validating them with basic string methods teaches you that
# you can do a lot of useful checking before ever learning regex.
def validate_email(email: str) -> dict:
    """Check whether a string looks like a valid email address."""
    # WHY strip: Users often paste text with trailing spaces or newlines.
    # Stripping whitespace prevents those invisible characters from
    # causing a false "contains spaces" error.
    email = email.strip()
    errors = []

    # WHY check spaces first: Spaces are never valid in email addresses.
    # Checking this independently of the @ logic keeps each rule simple.
    if " " in email:
        errors.append("contains spaces")

    # WHY count("@") != 1: An email must have exactly one @ symbol.
    # count() returns how many times a character appears in the string,
    # which is more precise than just checking "@ in email".
    if email.count("@") != 1:
        errors.append("must contain exactly one @")
    elif "@" in email:
        # WHY split on @: Once we know there is exactly one @, splitting
        # gives us the local part (before @) and the domain part (after @).
        local, domain = email.split("@")
        if not local:
            errors.append("nothing before @")
        # WHY check for dot in domain: A domain like "example" without
        # a TLD (.com, .org) is not valid for email delivery.
        if not domain or "." not in domain:
            errors.append("domain must contain a dot")

    # WHY return a dict: Returning structured data (not just True/False)
    # lets the caller display helpful error messages to the user.
    return {"value": email, "type": "email", "valid": len(errors) == 0, "errors": errors}


# WHY validate_phone: Phone numbers come in many formats (dashes,
# parentheses, spaces).  Extracting only digits is a practical technique
# that handles all common US phone formats in one pass.
def validate_phone(phone: str) -> dict:
    """Check whether a string looks like a US phone number."""
    phone = phone.strip()
    # WHY build digits manually: At this level, a for-loop with isdigit()
    # is more understandable than a regex like r"\d".  It shows exactly
    # what is happening: keep only the digit characters.
    digits = ""
    for char in phone:
        if char.isdigit():
            digits += char

    errors = []
    # WHY 10 digits: US phone numbers are always 10 digits (area code +
    # 7-digit number).  This is the simplest valid-length check.
    if len(digits) != 10:
        errors.append(f"expected 10 digits, got {len(digits)}")

    return {"value": phone, "type": "phone", "valid": len(errors) == 0, "errors": errors}


# WHY validate_zip_code: Zip codes are a fixed-format string, making
# them a perfect first use of regex.  The pattern is simple enough to
# learn without being overwhelming.
def validate_zip_code(zipcode: str) -> dict:
    """Check whether a string looks like a US zip code."""
    zipcode = zipcode.strip()
    errors = []

    # WHY regex here: Zip codes follow a strict pattern (5 digits, or
    # 5+4 digits with a dash).  A regex captures this in one line,
    # whereas string methods would require multiple checks.
    # ^ anchors to the start, $ anchors to the end, \d{5} matches
    # exactly 5 digits, (-\d{4})? optionally matches a dash + 4 digits.
    pattern = r"^\d{5}(-\d{4})?$"
    if not re.match(pattern, zipcode):
        errors.append("must be 5 digits or 5+4 format (12345-6789)")

    return {"value": zipcode, "type": "zip", "valid": len(errors) == 0, "errors": errors}


# WHY validate_input: This is the dispatcher — it reads a line like
# "email: user@example.com", figures out which validator to call, and
# routes the value to the right function.  This pattern scales: adding
# a new type means adding one entry to the validators dict.
def validate_input(line: str) -> dict:
    """Parse a line like 'email: user@example.com' and validate it."""
    # WHY check for colon: The colon separates the type label from the
    # value.  Without it, we cannot determine which validator to use.
    if ":" not in line:
        return {"raw": line.strip(), "error": "Expected format: type: value"}

    # WHY maxsplit=1: The value itself might contain colons (e.g., a
    # URL).  maxsplit=1 ensures we only split on the first colon.
    input_type, value = line.split(":", maxsplit=1)
    input_type = input_type.strip().lower()
    value = value.strip()

    # WHY a dict of validators: This is the "dispatch table" pattern.
    # Instead of a chain of if/elif, we map type names to functions.
    # Adding a new validator is one line, not a new branch.
    validators = {
        "email": validate_email,
        "phone": validate_phone,
        "zip": validate_zip_code,
    }

    if input_type not in validators:
        return {"raw": line.strip(), "error": f"Unknown type: {input_type}"}

    return validators[input_type](value)


# WHY process_file: Separating file I/O from validation logic makes
# each function testable on its own.  validate_email() can be tested
# with strings; process_file() handles the filesystem.
def process_file(path: Path) -> list[dict]:
    """Read input lines and validate each one."""
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    lines = path.read_text(encoding="utf-8").splitlines()
    results = []
    for line in lines:
        # WHY skip blanks: Empty lines in input files are common.
        # Skipping them avoids parse errors on non-data.
        if not line.strip():
            continue
        results.append(validate_input(line))
    return results


# WHY parse_args: argparse gives us --input and --output flags for free,
# with help text and error handling.  Hardcoded paths would make the
# script inflexible.
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Input Validator Lab")
    parser.add_argument("--input", default="data/sample_input.txt")
    parser.add_argument("--output", default="data/output.json")
    return parser.parse_args()


# WHY main: Wrapping the top-level logic in a main() function keeps
# the module importable without side effects.  Other code can import
# validate_email() without triggering file reads.
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
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Separate validator functions per type | Each validator has its own rules and error messages; isolating them makes testing and modification easy | One big function with nested if/elif for all types — harder to test and extend |
| Dispatch table (dict mapping type to function) | Adding a new type is one line instead of a new elif branch; the dict is also iterable for help text | if/elif chain — works but does not scale well and is harder to extend |
| Return dict with `valid` + `errors` list | Gives the caller both the pass/fail decision and the specific reasons, enabling rich error messages | Return just True/False — caller loses context about what failed |
| Use `re.match` for zip codes but string methods for email/phone | Zip codes have a strict fixed pattern ideal for regex; emails and phones benefit from step-by-step checks that are easier to understand at this level | Use regex for everything — works but is harder to debug at Level 1 |

## Alternative approaches

### Approach B: All-regex validation

```python
import re

def validate_email_regex(email: str) -> dict:
    """Use a single regex pattern for email validation."""
    email = email.strip()
    # WHY this pattern: \S+ matches non-whitespace before @, then
    # requires at least one dot in the domain portion.
    pattern = r"^\S+@\S+\.\S+$"
    valid = bool(re.match(pattern, email))
    errors = [] if valid else ["does not match email pattern"]
    return {"value": email, "type": "email", "valid": valid, "errors": errors}
```

**Trade-off:** A regex approach is more concise but gives less specific error messages. The string-methods approach tells users exactly what is wrong ("nothing before @", "domain must contain a dot"), while the regex approach can only say "does not match pattern". For a learning project, the string-methods approach teaches more about how validation logic works step by step.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Input line has no colon separator | `validate_input()` returns an error dict instead of crashing, because we check for ":" before splitting | The check is already in place; always test with malformed input |
| Email like `user@` (no domain) | `validate_email()` catches it — after splitting on @, the domain part is empty, triggering "domain must contain a dot" | The elif branch handles this; add test cases for edge-case emails |
| Unknown type like `ssn: 123-45-6789` | `validate_input()` returns `{"error": "Unknown type: ssn"}` because `ssn` is not in the validators dict | Already handled; the dict lookup pattern naturally rejects unknown keys |
| File does not exist | `process_file()` raises `FileNotFoundError` with a clear message before attempting to read | The existence check is explicit; argparse defaults to a sample file |

## Key takeaways

1. **Validate one thing at a time.** Each validator checks a single format, and each check within a validator tests one rule. This makes bugs easy to isolate and fixes easy to verify.
2. **Return structured results, not just True/False.** Returning a dict with `valid`, `type`, `value`, and `errors` gives callers everything they need to display helpful feedback — a pattern used in every form validation library.
3. **The dispatch table pattern (dict mapping names to functions) will appear repeatedly** in future projects: command dispatchers, API routers, plugin systems. Learning it here at Level 1 prepares you for the pattern everywhere else.
