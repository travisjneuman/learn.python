# Structured Error Handler — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) before reading the solution.

---

## Complete Solution

```python
"""Level 3 project: Structured Error Handler."""

from __future__ import annotations

import argparse
import json
import logging
import traceback
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


# -- Custom exception hierarchy -------------------------------------------
# WHY: a hierarchy lets callers catch broad categories (AppError) or
# specific ones (ValidationError). Without it, you catch bare Exception
# and lose all context about WHAT went wrong.

class AppError(Exception):
    """Base error for all application-specific exceptions."""

    def __init__(self, message: str, code: str = "UNKNOWN",
                 context: Optional[dict] = None) -> None:
        super().__init__(message)
        # WHY: machine-readable codes like "VALIDATION_ERROR" are
        # easier to filter and aggregate than free-text messages.
        self.code = code
        # WHY: context dict carries structured data (field name,
        # expected pattern, etc.) that a human-readable message alone
        # cannot convey programmatically.
        self.context = context or {}


class ValidationError(AppError):
    """Raised when input data fails validation."""

    def __init__(self, message: str, field: str = "",
                 context: Optional[dict] = None) -> None:
        super().__init__(message, code="VALIDATION_ERROR", context=context)
        self.field = field


class NotFoundError(AppError):
    """Raised when a requested resource does not exist."""

    def __init__(self, resource: str, identifier: str) -> None:
        super().__init__(
            f"{resource} not found: {identifier}",
            code="NOT_FOUND",
            context={"resource": resource, "identifier": identifier},
        )


class ConfigError(AppError):
    """Raised when configuration is invalid or missing."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="CONFIG_ERROR")


# -- Error result dataclasses ---------------------------------------------

@dataclass
class ErrorRecord:
    """A structured error record for reporting.

    WHY: exceptions are for flow control. ErrorRecords are for
    reporting. You convert exceptions to ErrorRecords so they can
    be serialised to JSON, aggregated, and displayed.
    """
    code: str
    message: str
    field: str = ""
    context: dict = field(default_factory=dict)
    traceback_lines: list[str] = field(default_factory=list)


@dataclass
class OperationResult:
    """Result of an operation that might fail.

    WHY: the "Result pattern" wraps either success or failure in
    one return type. The caller checks .success instead of catching
    exceptions, which makes batch processing cleaner — no nested
    try/except blocks.
    """
    success: bool
    value: Optional[dict] = None
    errors: list[ErrorRecord] = field(default_factory=list)


def capture_error(exc: Exception) -> ErrorRecord:
    """Convert any exception into a structured ErrorRecord.

    WHY: this bridges the exception world (raise/catch) and the
    data world (dicts/JSON). After capture, the error is just data
    that can be serialised, stored, or aggregated.
    """
    if isinstance(exc, AppError):
        return ErrorRecord(
            code=exc.code,
            message=str(exc),
            field=getattr(exc, "field", ""),
            context=exc.context,
            # WHY: format_exception produces the full traceback as a
            # list of strings, useful for debugging but not for users.
            traceback_lines=traceback.format_exception(
                type(exc), exc, exc.__traceback__),
        )
    # WHY: unknown exceptions get code "UNEXPECTED" so they stand out
    # in reports. They indicate a bug, not a validation failure.
    return ErrorRecord(
        code="UNEXPECTED",
        message=str(exc),
        traceback_lines=traceback.format_exception(
            type(exc), exc, exc.__traceback__),
    )


# -- Validation functions -------------------------------------------------

def validate_field(name: str, value: str, rules: dict) -> list[ErrorRecord]:
    """Validate a single field against rules.

    WHY: each rule is checked independently and all errors are
    collected — not just the first one. This gives the user a
    complete picture of what needs fixing.
    """
    import re
    errors: list[ErrorRecord] = []

    # WHY: if a required field is empty, further checks are pointless.
    # Return early to avoid confusing "too short" errors on empty strings.
    if rules.get("required") and not value.strip():
        errors.append(ErrorRecord(
            code="REQUIRED",
            message=f"Field '{name}' is required",
            field=name,
        ))
        return errors

    if "min_length" in rules and len(value) < rules["min_length"]:
        errors.append(ErrorRecord(
            code="TOO_SHORT",
            message=f"Field '{name}' must be at least {rules['min_length']} characters",
            field=name,
            context={"actual_length": len(value)},
        ))

    if "max_length" in rules and len(value) > rules["max_length"]:
        errors.append(ErrorRecord(
            code="TOO_LONG",
            message=f"Field '{name}' must be at most {rules['max_length']} characters",
            field=name,
            context={"actual_length": len(value)},
        ))

    if "pattern" in rules and not re.match(rules["pattern"], value):
        errors.append(ErrorRecord(
            code="INVALID_FORMAT",
            message=f"Field '{name}' does not match expected pattern",
            field=name,
            context={"pattern": rules["pattern"]},
        ))

    return errors


def validate_record(record: dict, schema: dict[str, dict]) -> OperationResult:
    """Validate a full record against a schema.

    WHY: iterating ALL schema fields (not just fields present in
    the record) catches missing required fields too.
    """
    all_errors: list[ErrorRecord] = []

    for field_name, rules in schema.items():
        # WHY: convert to string and default to "" so validate_field
        # always receives a string. Missing fields become empty strings.
        value = str(record.get(field_name, ""))
        field_errors = validate_field(field_name, value, rules)
        all_errors.extend(field_errors)

    if all_errors:
        return OperationResult(success=False, errors=all_errors)
    return OperationResult(success=True, value=record)


def safe_process(records: list[dict], schema: dict[str, dict]) -> list[OperationResult]:
    """Process a batch of records, collecting errors instead of crashing.

    WHY: the outer try/except is a safety net that catches truly
    unexpected errors (bugs in validate_record itself). Without it,
    one bad record could crash the entire batch.
    """
    results: list[OperationResult] = []

    for i, record in enumerate(records):
        try:
            result = validate_record(record, schema)
            logger.info("Record %d: %s", i, "OK" if result.success else "FAILED")
            results.append(result)
        except Exception as exc:
            logger.error("Unexpected error on record %d: %s", i, exc)
            results.append(OperationResult(
                success=False,
                errors=[capture_error(exc)],
            ))

    return results


def summarise_results(results: list[OperationResult]) -> dict:
    """Summarise batch processing results."""
    passed = sum(1 for r in results if r.success)
    failed = sum(1 for r in results if not r.success)
    all_errors = [asdict(e) for r in results for e in r.errors]

    # WHY: counting by error code reveals patterns.
    # "90% of failures are REQUIRED" tells you the data source
    # is not providing mandatory fields.
    error_codes: dict[str, int] = {}
    for err in all_errors:
        code = err["code"]
        error_codes[code] = error_codes.get(code, 0) + 1

    return {
        "total": len(results),
        "passed": passed,
        "failed": failed,
        "error_counts": error_codes,
        "errors": all_errors,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Structured error handler")
    parser.add_argument("file", help="JSON file with records")
    parser.add_argument("--schema", required=True,
                        help="JSON file with validation schema")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--log-level", default="INFO")
    return parser


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    parser = build_parser()
    args = parser.parse_args()

    records = json.loads(Path(args.file).read_text(encoding="utf-8"))
    schema = json.loads(Path(args.schema).read_text(encoding="utf-8"))

    results = safe_process(records, schema)
    summary = summarise_results(results)

    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"Processed {summary['total']} records: "
              f"{summary['passed']} passed, {summary['failed']} failed")
        if summary["error_counts"]:
            print("Error breakdown:")
            for code, count in summary["error_counts"].items():
                print(f"  {code}: {count}")


if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Custom exception hierarchy (AppError base) | Callers can catch `AppError` for all app errors or `ValidationError` for just validation. Built-in exceptions like `ValueError` do not carry error codes or structured context. |
| `OperationResult` (Result pattern) | Avoids scattering try/except throughout calling code. The caller checks `.success` and iterates `.errors` — no exception handling needed at the call site. |
| `capture_error` bridge function | Converts exceptions (control flow) into ErrorRecords (data). Once captured, errors are just dicts that can be serialised, aggregated, or displayed. |
| Collect ALL errors, not just the first | Users strongly prefer seeing "5 fields are wrong" over fixing one field, resubmitting, and discovering the next one. |
| Machine-readable error codes | Codes like "REQUIRED" and "INVALID_FORMAT" are filterable and countable. Human-readable messages are for display only. |

## Alternative Approaches

### Using `pydantic` for validation

```python
from pydantic import BaseModel, EmailStr, validator

class ContactRecord(BaseModel):
    name: str
    email: EmailStr
    phone: str

    @validator("phone")
    def must_be_digits(cls, v):
        if not v.replace("-", "").isdigit():
            raise ValueError("Phone must contain only digits and dashes")
        return v
```

**Trade-off:** Pydantic does all of this automatically (type coercion, validation, error collection). But it is a third-party dependency and hides the mechanics. Understanding the manual approach first makes pydantic feel like magic you can debug instead of magic you depend on.

## Common Pitfalls

1. **Catching bare `Exception` too broadly** — The `safe_process` function catches `Exception` as a safety net, but individual validators should raise specific errors. If everything is caught as "UNEXPECTED", you lose the ability to distinguish bugs from validation failures.

2. **Not validating the schema itself** — If the schema JSON has a typo (e.g., "requird" instead of "required"), the rule is silently ignored and validation passes. Add a schema validation step before processing.

3. **Forgetting that `record.get(field_name, "")` hides missing fields** — A missing field and an empty field both produce `""`. If you need to distinguish "not provided" from "provided but empty", use a sentinel value or check `field_name in record` separately.
