# Solution: Level 8 / Project 05 - Export Governance Check

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [Walkthrough](./WALKTHROUGH.md) first -- it guides
> your thinking without giving away the answer.
>
> [Back to project README](./README.md)

---

## Complete solution

```python
"""Export Governance Check -- validate exports against governance rules."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable


# --- Domain types -------------------------------------------------------

# WHY four severity levels? -- Not all violations are equal. A missing
# changelog entry (INFO) should not block an export the way PII exposure
# (BLOCKING) does. Graduated severity lets governance be strict where it
# matters without creating friction on every export.
class Severity(Enum):
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
    export_id: str
    requester: str
    format: ExportFormat
    columns: list[str]
    row_count: int
    data_sample: list[dict[str, Any]] = field(default_factory=list)
    classification: str = "internal"


# WHY frozen=True for Violation? -- Violations are evidence in an audit
# trail. They must not be modified after creation to maintain integrity.
@dataclass(frozen=True)
class Violation:
    rule_name: str
    severity: Severity
    message: str
    field_name: str = ""

    def to_dict(self) -> dict[str, str]:
        return {
            "rule": self.rule_name, "severity": self.severity.value,
            "message": self.message, "field": self.field_name,
        }


@dataclass
class GovernanceResult:
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
            "export_id": self.export_id, "approved": self.approved,
            "rules_checked": self.rules_checked,
            "violation_count": len(self.violations),
            "blocking_count": self.blocking_count,
            "violations": [v.to_dict() for v in self.violations],
        }


# --- PII detection patterns ---------------------------------------------

# WHY pre-compiled regex? -- re.compile() parses the pattern once. Calling
# re.search() with a string pattern recompiles on every call. For scanning
# thousands of rows, pre-compilation gives significant speedup.
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

# WHY standalone functions instead of a Rule class hierarchy? -- Functions
# are simpler, composable, and follow the Strategy pattern. Each function
# has one responsibility. Adding a new rule means writing a new function
# and adding it to default_rules() -- no class inheritance required.

def check_pii_columns(request: ExportRequest) -> list[Violation]:
    """Flag columns whose names suggest PII content."""
    violations: list[Violation] = []
    for col in request.columns:
        if col.lower() in PII_COLUMN_NAMES:
            violations.append(Violation(
                rule_name="pii_column_name", severity=Severity.BLOCKING,
                message=f"Column '{col}' appears to contain PII", field_name=col,
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
                        rule_name="pii_content_detected", severity=Severity.CRITICAL,
                        message=f"Possible {pii_type} detected in column '{col_name}'",
                        field_name=col_name,
                    ))
    return violations


def check_row_limit(request: ExportRequest, max_rows: int = 100_000) -> list[Violation]:
    if request.row_count > max_rows:
        return [Violation(
            rule_name="row_limit_exceeded", severity=Severity.BLOCKING,
            message=f"Export has {request.row_count} rows, max is {max_rows}",
        )]
    return []


def check_format_allowed(
    request: ExportRequest, allowed: set[ExportFormat] | None = None,
) -> list[Violation]:
    if allowed is None:
        allowed = {ExportFormat.CSV, ExportFormat.JSON}
    if request.format not in allowed:
        return [Violation(
            rule_name="format_not_allowed", severity=Severity.BLOCKING,
            message=f"Format '{request.format.value}' is not permitted",
        )]
    return []


def check_classification_level(request: ExportRequest) -> list[Violation]:
    if request.classification == "restricted":
        return [Violation(
            rule_name="restricted_data", severity=Severity.BLOCKING,
            message="Restricted-classification data cannot be exported",
        )]
    if request.classification == "confidential":
        return [Violation(
            rule_name="confidential_warning", severity=Severity.WARNING,
            message="Confidential data export requires manager approval",
        )]
    return []


# --- Rule engine --------------------------------------------------------

GovernanceRule = Callable[[ExportRequest], list[Violation]]


def default_rules() -> list[GovernanceRule]:
    return [check_pii_columns, check_pii_content, check_row_limit,
            check_format_allowed, check_classification_level]


def evaluate_export(
    request: ExportRequest, rules: list[GovernanceRule] | None = None,
) -> GovernanceResult:
    if rules is None:
        rules = default_rules()
    all_violations: list[Violation] = []
    for rule in rules:
        all_violations.extend(rule(request))
    # WHY any() with BLOCKING check? -- A single blocking violation vetoes
    # the entire export. Non-blocking violations are logged for review but
    # don't prevent the export from proceeding.
    has_blockers = any(v.severity == Severity.BLOCKING for v in all_violations)
    return GovernanceResult(
        export_id=request.export_id, approved=not has_blockers,
        violations=all_violations, rules_checked=len(rules),
    )


# --- CLI ----------------------------------------------------------------

def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Export governance checker")
    parser.add_argument("--input", default="data/sample_input.json")
    args = parser.parse_args(argv)
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
        request = ExportRequest(
            export_id="demo-001", requester="analyst@company.com",
            format=ExportFormat.CSV,
            columns=["name", "email", "ssn", "department"], row_count=5000,
            data_sample=[{"name": "Alice", "email": "alice@example.com",
                          "ssn": "123-45-6789", "department": "eng"}],
            classification="confidential",
        )
    result = evaluate_export(request)
    print(json.dumps(result.to_dict(), indent=2))


if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Functions as rules (Strategy pattern) | Adding a new rule is just a new function; no class hierarchy needed | Abstract base class with `check()` method -- more formal but heavier for this use case |
| Pre-compiled regex patterns | One-time compilation cost; significant speedup when scanning many rows | Raw string patterns with `re.search()` -- recompiles the pattern on every call |
| Column-name heuristic + content scan | Defense in depth: catches PII even if column names are obfuscated | Content scan only -- misses cases where PII column has no data in the sample |
| Blocking severity as hard veto | Matches how real compliance systems work: some violations are non-negotiable | Weighted scoring -- more nuanced but risky for true compliance requirements |
| Frozen Violation dataclass | Audit trail integrity: violations must not be modified after detection | Mutable violations -- simpler but allows accidental tampering |

## Alternative approaches

### Approach B: Class-based rule engine with registration

```python
from abc import ABC, abstractmethod

class GovernanceRule(ABC):
    name: str
    @abstractmethod
    def check(self, request: ExportRequest) -> list[Violation]: ...

class PIIColumnRule(GovernanceRule):
    name = "pii_column_check"
    def check(self, request: ExportRequest) -> list[Violation]:
        # same logic as check_pii_columns()
        ...

class RuleEngine:
    _registry: list[GovernanceRule] = []

    @classmethod
    def register(cls, rule: GovernanceRule):
        cls._registry.append(rule)
```

**Trade-off:** Class-based rules with a registry are more formal and work well when rules need shared state or configuration. But for stateless validation functions, the function-based Strategy pattern is simpler and achieves the same extensibility with less boilerplate.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| PII field flagged twice (column name + content scan) | The same column gets two violations from different rules | Deduplicate violations by field_name before returning, or accept both for audit completeness |
| Phone regex matches non-phone numbers | `\b\d{3}[-.]?\d{3}[-.]?\d{4}\b` can match account numbers or order IDs | Add context-aware validation (check column name alongside content pattern) |
| Empty `data_sample` with PII columns | Content scan finds nothing, but column names still flag correctly | Column-name check provides a safety net even when sample data is missing |
