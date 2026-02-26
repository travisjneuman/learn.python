# Walkthrough: Input Validator Lab

> This guide walks through the **thinking process** for building this project.
> It does NOT give you the complete solution. For that, see [SOLUTION.md](./SOLUTION.md).

## Before reading this

**Try the project yourself first.** Spend at least 20 minutes.
If you have not tried yet, close this file and open the [project README](./README.md).

---

## Understanding the problem

You need to build a system that validates different types of input: email addresses, phone numbers, and zip codes. The input comes from a file where each line has the format `type: value` (e.g., `email: user@example.com`). Your program reads each line, figures out what type of validation to apply, runs the right validator, and reports whether the input passed or failed with a clear reason.

The sample input file looks like this:

```
email: user@example.com
email: bad-email-no-at
phone: 555-123-4567
zip: 90210
```

## Planning before code

```mermaid
flowchart TD
    A[Read lines from file] --> B[For each line]
    B --> C[Parse 'type: value']
    C --> D{Which type?}
    D -->|email| E[validate_email]
    D -->|phone| F[validate_phone]
    D -->|zip| G[validate_zip_code]
    D -->|unknown| H[Return error]
    E --> I[Collect result: PASS or FAIL + reasons]
    F --> I
    G --> I
    H --> I
    I --> J[Print summary + save JSON]
```

Four layers to build:

1. **Individual validators** -- one function per input type, each returning a structured result
2. **A dispatcher** -- parse the line, route to the correct validator
3. **File processing** -- read lines, skip blanks, collect results
4. **Output** -- print a table and save JSON

## Step 1: Email validation

Start with the most complex validator. An email needs:
- Exactly one `@` symbol
- Text before the `@`
- A dot in the domain part (after `@`)
- No spaces

```python
def validate_email(email: str) -> dict:
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
```

The pattern here is **accumulate errors**: start with an empty list, add each problem you find, then check if the list is empty at the end. This is better than returning after the first error because it tells the user everything that is wrong at once.

### Predict before you scroll

What does `validate_email("user@example.com")` return? What about `validate_email("@example.com")`? Trace through the conditions.

## Step 2: Phone validation

Phone validation is simpler: extract only the digits, then check that there are exactly 10.

```python
def validate_phone(phone: str) -> dict:
    phone = phone.strip()
    digits = ""
    for char in phone:
        if char.isdigit():
            digits += char

    errors = []
    if len(digits) != 10:
        errors.append(f"expected 10 digits, got {len(digits)}")

    return {"value": phone, "type": "phone", "valid": len(errors) == 0, "errors": errors}
```

By stripping out everything except digits, this function accepts multiple formats: `555-123-4567`, `(555) 123-4567`, and `5551234567` all produce the same 10 digits.

### Predict before you scroll

What happens if the user enters `12345`? How many digits does the function extract, and what error does it report?

## Step 3: Zip code validation with regex

Zip codes have a strict format: exactly 5 digits, optionally followed by a dash and 4 more digits. This is a good case for a regular expression:

```python
import re

def validate_zip_code(zipcode: str) -> dict:
    zipcode = zipcode.strip()
    errors = []

    pattern = r"^\d{5}(-\d{4})?$"
    if not re.match(pattern, zipcode):
        errors.append("must be 5 digits or 5+4 format (12345-6789)")

    return {"value": zipcode, "type": "zip", "valid": len(errors) == 0, "errors": errors}
```

Breaking down the regex `r"^\d{5}(-\d{4})?$"`:
- `^` -- start of string
- `\d{5}` -- exactly 5 digits
- `(-\d{4})?` -- optionally: a dash followed by 4 digits
- `$` -- end of string

## Step 4: The dispatcher

The dispatcher parses the `type: value` format and routes to the right validator:

```python
def validate_input(line: str) -> dict:
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
```

Notice the `validators` dictionary maps type names to functions. This is the **dispatch table** pattern -- it is cleaner than a long `if/elif` chain and easier to extend. To add a new type, you just add one entry to the dictionary.

Also notice `maxsplit=1` in the `.split()` call. This ensures we only split on the first colon, so a value like `time: 12:30:00` would not break.

## Common mistakes

| Mistake | Why it happens | How to fix |
|---------|---------------|------------|
| Email validator accepts `user@domain` (no dot) | Forgot to check for a dot in the domain part | Add `"." not in domain` check |
| Phone validator rejects `(555) 123-4567` | Checking format instead of just extracting digits | Strip all non-digits first, then count |
| `line.split(":")` breaks on values containing `:` | Default split splits on every colon | Use `split(":", maxsplit=1)` |
| Returning just `True/False` instead of a dict | Simpler but less useful | Return `{"valid": bool, "errors": [...]}` so the caller knows WHY it failed |

## Testing your solution

Run the tests from the project directory:

```bash
pytest -q
```

The seven tests check:
- Valid email passes
- Email without `@` fails
- Valid phone number (with dashes) passes
- Short phone number fails
- Both zip formats (`90210` and `90210-1234`) pass
- Short zip fails
- The dispatcher routes `email: test@test.com` to the email validator

## What to explore next

1. Add a new validation type: "url" that checks for `http://` or `https://` prefix and a dot in the domain
2. Add a `--strict` flag that rejects emails where the TLD (the part after the last dot) is fewer than 2 characters
