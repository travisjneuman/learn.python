"""Level 3 project: Structured Error Handler.

Demonstrates custom exception hierarchies, error context propagation,
and safe error collection patterns.

Skills practiced: custom exceptions, dataclasses, typing basics,
logging, error handling patterns, JSON serialisation.
"""

from __future__ import annotations

import argparse
import json
import logging
import traceback
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


# ── Custom exception hierarchy ─────────────────────────────────

class AppError(Exception):
    """Base error for all application-specific exceptions."""

    def __init__(self, message: str, code: str = "UNKNOWN", context: Optional[dict] = None) -> None:
        super().__init__(message)
        self.code = code
        self.context = context or {}


class ValidationError(AppError):
    """Raised when input data fails validation."""

    def __init__(self, message: str, field: str = "", context: Optional[dict] = None) -> None:
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


# ── Error result dataclasses ──────────────────────────────────

@dataclass
class ErrorRecord:
    """A structured error record for reporting."""
    code: str
    message: str
    field: str = ""
    context: dict = field(default_factory=dict)
    traceback_lines: list[str] = field(default_factory=list)


@dataclass
class OperationResult:
    """Result of an operation that might fail.

    Wraps either a success value or a list of errors.
    This is the 'Result' pattern — avoids scattering try/except.
    """
    success: bool
    value: Optional[dict] = None
    errors: list[ErrorRecord] = field(default_factory=list)


def capture_error(exc: Exception) -> ErrorRecord:
    """Convert any exception into a structured ErrorRecord."""
    if isinstance(exc, AppError):
        return ErrorRecord(
            code=exc.code,
            message=str(exc),
            field=getattr(exc, "field", ""),
            context=exc.context,
            traceback_lines=traceback.format_exception(type(exc), exc, exc.__traceback__),
        )
    return ErrorRecord(
        code="UNEXPECTED",
        message=str(exc),
        traceback_lines=traceback.format_exception(type(exc), exc, exc.__traceback__),
    )


# ── Validation functions ──────────────────────────────────────

def validate_field(name: str, value: str, rules: dict) -> list[ErrorRecord]:
    """Validate a single field against rules.

    Supported rules: required, min_length, max_length, pattern.
    """
    import re
    errors: list[ErrorRecord] = []

    if rules.get("required") and not value.strip():
        errors.append(ErrorRecord(
            code="REQUIRED",
            message=f"Field '{name}' is required",
            field=name,
        ))
        return errors  # No point checking further.

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

    schema maps field names to rule dicts.
    Returns OperationResult with all errors collected.
    """
    all_errors: list[ErrorRecord] = []

    for field_name, rules in schema.items():
        value = str(record.get(field_name, ""))
        field_errors = validate_field(field_name, value, rules)
        all_errors.extend(field_errors)

    if all_errors:
        return OperationResult(success=False, errors=all_errors)
    return OperationResult(success=True, value=record)


def safe_process(records: list[dict], schema: dict[str, dict]) -> list[OperationResult]:
    """Process a batch of records, collecting errors instead of crashing.

    This demonstrates the 'error accumulation' pattern.
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
    """Build CLI parser."""
    parser = argparse.ArgumentParser(description="Structured error handler")
    parser.add_argument("file", help="JSON file with records")
    parser.add_argument("--schema", required=True, help="JSON file with validation schema")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--log-level", default="INFO")
    return parser


def main() -> None:
    """Entry point."""
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
