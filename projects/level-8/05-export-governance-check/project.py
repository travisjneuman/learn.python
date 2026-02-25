"""Export Governance Check — validate exports against governance rules.

Design rationale:
    Enterprise systems must enforce data governance before exporting data:
    PII detection, size limits, format validation, and access control.
    This project builds a rule engine that validates export requests
    against configurable policies — a pattern used in compliance-heavy
    industries (finance, healthcare, government).

Concepts practised:
    - Strategy pattern for pluggable validation rules
    - dataclasses for policy and violation modeling
    - regex-based PII detection
    - composable rule evaluation
    - structured audit logging
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable


# --- Domain types -------------------------------------------------------

class Severity(Enum):
    """Violation severity levels."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    BLOCKING = "blocking"


class ExportFormat(Enum):
    CSV = "csv"
    JSON = "json"
    EXCEL = "excel"
    PDF = "pdf"


@dataclass
class ExportRequest:
    """A request to export data from the system."""
    export_id: str
    requester: str
    format: ExportFormat
    columns: list[str]
    row_count: int
    data_sample: list[dict[str, Any]] = field(default_factory=list)
    classification: str = "internal"  # public, internal, confidential, restricted


@dataclass(frozen=True)
class Violation:
    """A single governance rule violation."""
    rule_name: str
    severity: Severity
    message: str
    field_name: str = ""

    def to_dict(self) -> dict[str, str]:
        return {
            "rule": self.rule_name,
            "severity": self.severity.value,
            "message": self.message,
            "field": self.field_name,
        }


@dataclass
class GovernanceResult:
    """Aggregated result of governance checks on an export request."""
    export_id: str
    approved: bool
    violations: list[Violation] = field(default_factory=list)
    rules_checked: int = 0

    @property
    def blocking_count(self) -> int:
        return sum(1 for v in self.violations if v.severity == Severity.BLOCKING)

    @property
    def critical_count(self) -> int:
        return sum(1 for v in self.violations if v.severity == Severity.CRITICAL)

    def to_dict(self) -> dict[str, Any]:
        return {
            "export_id": self.export_id,
            "approved": self.approved,
            "rules_checked": self.rules_checked,
            "violation_count": len(self.violations),
            "blocking_count": self.blocking_count,
            "violations": [v.to_dict() for v in self.violations],
        }


# --- PII detection patterns ---------------------------------------------

PII_PATTERNS: dict[str, re.Pattern[str]] = {
    "email": re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"),
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "phone": re.compile(r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b"),
    "credit_card": re.compile(r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b"),
}

PII_COLUMN_NAMES = {
    "ssn", "social_security", "credit_card", "cc_number",
    "password", "secret", "token", "api_key",
}


# --- Governance rules (Strategy pattern) --------------------------------

def check_pii_columns(request: ExportRequest) -> list[Violation]:
    """Flag columns whose names suggest PII content."""
    violations: list[Violation] = []
    for col in request.columns:
        if col.lower() in PII_COLUMN_NAMES:
            violations.append(Violation(
                rule_name="pii_column_name",
                severity=Severity.BLOCKING,
                message=f"Column '{col}' appears to contain PII",
                field_name=col,
            ))
    return violations


def check_pii_content(request: ExportRequest) -> list[Violation]:
    """Scan sample data for PII patterns."""
    violations: list[Violation] = []
    for row in request.data_sample:
        for col_name, value in row.items():
            text = str(value)
            for pii_type, pattern in PII_PATTERNS.items():
                if pattern.search(text):
                    violations.append(Violation(
                        rule_name="pii_content_detected",
                        severity=Severity.CRITICAL,
                        message=f"Possible {pii_type} detected in column '{col_name}'",
                        field_name=col_name,
                    ))
    return violations


def check_row_limit(request: ExportRequest, max_rows: int = 100_000) -> list[Violation]:
    """Enforce maximum export size."""
    if request.row_count > max_rows:
        return [Violation(
            rule_name="row_limit_exceeded",
            severity=Severity.BLOCKING,
            message=f"Export has {request.row_count} rows, max is {max_rows}",
        )]
    return []


def check_format_allowed(
    request: ExportRequest,
    allowed: set[ExportFormat] | None = None,
) -> list[Violation]:
    """Verify the export format is permitted."""
    if allowed is None:
        allowed = {ExportFormat.CSV, ExportFormat.JSON}
    if request.format not in allowed:
        return [Violation(
            rule_name="format_not_allowed",
            severity=Severity.BLOCKING,
            message=f"Format '{request.format.value}' is not permitted",
        )]
    return []


def check_classification_level(request: ExportRequest) -> list[Violation]:
    """Restricted data cannot be exported."""
    if request.classification == "restricted":
        return [Violation(
            rule_name="restricted_data",
            severity=Severity.BLOCKING,
            message="Restricted-classification data cannot be exported",
        )]
    if request.classification == "confidential":
        return [Violation(
            rule_name="confidential_warning",
            severity=Severity.WARNING,
            message="Confidential data export requires manager approval",
        )]
    return []


# --- Rule engine --------------------------------------------------------

# Type alias for a governance rule function
GovernanceRule = Callable[[ExportRequest], list[Violation]]


def default_rules() -> list[GovernanceRule]:
    """Return the standard set of governance rules."""
    return [
        check_pii_columns,
        check_pii_content,
        check_row_limit,
        check_format_allowed,
        check_classification_level,
    ]


def evaluate_export(
    request: ExportRequest,
    rules: list[GovernanceRule] | None = None,
) -> GovernanceResult:
    """Run all governance rules against an export request."""
    if rules is None:
        rules = default_rules()

    all_violations: list[Violation] = []
    for rule in rules:
        all_violations.extend(rule(request))

    has_blockers = any(v.severity == Severity.BLOCKING for v in all_violations)

    return GovernanceResult(
        export_id=request.export_id,
        approved=not has_blockers,
        violations=all_violations,
        rules_checked=len(rules),
    )


# --- CLI ----------------------------------------------------------------

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export governance checker")
    parser.add_argument("--input", default="data/sample_input.json",
                        help="Export request JSON file")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    from pathlib import Path
    input_path = Path(args.input)

    if input_path.exists():
        raw = json.loads(input_path.read_text(encoding="utf-8"))
        request = ExportRequest(
            export_id=raw.get("export_id", "test-001"),
            requester=raw.get("requester", "unknown"),
            format=ExportFormat(raw.get("format", "csv")),
            columns=raw.get("columns", []),
            row_count=raw.get("row_count", 0),
            data_sample=raw.get("data_sample", []),
            classification=raw.get("classification", "internal"),
        )
    else:
        # Demo request with PII
        request = ExportRequest(
            export_id="demo-001",
            requester="analyst@company.com",
            format=ExportFormat.CSV,
            columns=["name", "email", "ssn", "department"],
            row_count=5000,
            data_sample=[
                {"name": "Alice", "email": "alice@example.com",
                 "ssn": "123-45-6789", "department": "eng"},
            ],
            classification="confidential",
        )

    result = evaluate_export(request)
    print(json.dumps(result.to_dict(), indent=2))


if __name__ == "__main__":
    main()
