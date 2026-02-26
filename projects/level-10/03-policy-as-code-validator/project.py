"""Policy-as-Code Validator — Define and evaluate policies as Python code (OPA-style).

Architecture: Uses the Chain of Responsibility pattern where each policy rule is a
link in a chain. Rules are composable: AND-chains require all to pass, OR-chains
require at least one. A PolicyEngine collects rules, evaluates them against a
resource, and produces an auditable verdict with per-rule evidence.

Design rationale: Infrastructure-as-code demands that compliance checks live
alongside the code they govern. By expressing policies as composable Python
objects rather than configuration files, teams get IDE support, type checking,
and the ability to unit-test their compliance rules the same way they test code.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Protocol


# ---------------------------------------------------------------------------
# Domain types
# ---------------------------------------------------------------------------

class Severity(Enum):
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()


class Verdict(Enum):
    PASS = "pass"
    FAIL = "fail"
    SKIP = "skip"


# WHY frozen=True for RuleResult? -- Rule results are evidence for audits.
# They must be immutable once produced — if a result could be mutated after
# evaluation, the audit trail would be untrustworthy. This is the same
# principle that makes OPA (Open Policy Agent) decisions immutable.
@dataclass(frozen=True)
class RuleResult:
    """Outcome of evaluating a single policy rule against a resource."""
    rule_id: str
    verdict: Verdict
    severity: Severity
    message: str
    resource_key: str = ""


@dataclass
class EvaluationReport:
    """Aggregate evaluation of all rules against a resource."""
    resource_id: str
    results: list[RuleResult] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(r.verdict != Verdict.FAIL for r in self.results)

    @property
    def failures(self) -> list[RuleResult]:
        return [r for r in self.results if r.verdict == Verdict.FAIL]

    @property
    def warnings(self) -> list[RuleResult]:
        return [r for r in self.results if r.severity == Severity.WARNING and r.verdict == Verdict.FAIL]

    def summary(self) -> dict[str, Any]:
        return {
            "resource_id": self.resource_id,
            "total_rules": len(self.results),
            "passed": sum(1 for r in self.results if r.verdict == Verdict.PASS),
            "failed": sum(1 for r in self.results if r.verdict == Verdict.FAIL),
            "skipped": sum(1 for r in self.results if r.verdict == Verdict.SKIP),
            "overall": "PASS" if self.passed else "FAIL",
        }


# ---------------------------------------------------------------------------
# Policy rule protocol and implementations
# ---------------------------------------------------------------------------

class PolicyRule(Protocol):
    """Chain-of-responsibility link: evaluate a resource dict."""
    rule_id: str
    severity: Severity

    def evaluate(self, resource: dict[str, Any]) -> RuleResult: ...


@dataclass
class RequiredFieldRule:
    """Checks that a specific field exists and is non-empty in the resource."""
    rule_id: str
    field_name: str
    severity: Severity = Severity.ERROR

    def evaluate(self, resource: dict[str, Any]) -> RuleResult:
        value = resource.get(self.field_name)
        if value is None or value == "":
            return RuleResult(
                self.rule_id, Verdict.FAIL, self.severity,
                f"Required field '{self.field_name}' is missing or empty",
                self.field_name,
            )
        return RuleResult(
            self.rule_id, Verdict.PASS, self.severity,
            f"Field '{self.field_name}' present",
            self.field_name,
        )


@dataclass
class ValueInSetRule:
    """Checks that a field value is within an allowed set."""
    rule_id: str
    field_name: str
    allowed: set[str]
    severity: Severity = Severity.ERROR

    def evaluate(self, resource: dict[str, Any]) -> RuleResult:
        value = resource.get(self.field_name, "")
        if str(value) not in self.allowed:
            return RuleResult(
                self.rule_id, Verdict.FAIL, self.severity,
                f"'{self.field_name}' value '{value}' not in {sorted(self.allowed)}",
                self.field_name,
            )
        return RuleResult(
            self.rule_id, Verdict.PASS, self.severity,
            f"'{self.field_name}' value '{value}' is allowed",
            self.field_name,
        )


@dataclass
class NumericRangeRule:
    """Checks that a numeric field falls within [min_val, max_val]."""
    rule_id: str
    field_name: str
    min_val: float | None = None
    max_val: float | None = None
    severity: Severity = Severity.WARNING

    def evaluate(self, resource: dict[str, Any]) -> RuleResult:
        raw = resource.get(self.field_name)
        if raw is None:
            return RuleResult(
                self.rule_id, Verdict.SKIP, self.severity,
                f"Field '{self.field_name}' not present, skipping range check",
                self.field_name,
            )
        try:
            value = float(raw)
        except (TypeError, ValueError):
            return RuleResult(
                self.rule_id, Verdict.FAIL, self.severity,
                f"Field '{self.field_name}' is not numeric: {raw!r}",
                self.field_name,
            )
        if self.min_val is not None and value < self.min_val:
            return RuleResult(
                self.rule_id, Verdict.FAIL, self.severity,
                f"'{self.field_name}' value {value} below minimum {self.min_val}",
                self.field_name,
            )
        if self.max_val is not None and value > self.max_val:
            return RuleResult(
                self.rule_id, Verdict.FAIL, self.severity,
                f"'{self.field_name}' value {value} above maximum {self.max_val}",
                self.field_name,
            )
        return RuleResult(
            self.rule_id, Verdict.PASS, self.severity,
            f"'{self.field_name}' value {value} within range",
            self.field_name,
        )


@dataclass
class CustomPredicateRule:
    """Evaluates an arbitrary predicate function against the resource."""
    rule_id: str
    predicate: Callable[[dict[str, Any]], bool]
    failure_message: str
    severity: Severity = Severity.ERROR

    def evaluate(self, resource: dict[str, Any]) -> RuleResult:
        if self.predicate(resource):
            return RuleResult(self.rule_id, Verdict.PASS, self.severity, "Custom check passed")
        return RuleResult(self.rule_id, Verdict.FAIL, self.severity, self.failure_message)


# ---------------------------------------------------------------------------
# Policy engine — collects and evaluates rules
# ---------------------------------------------------------------------------

class PolicyEngine:
    """Collects policy rules and evaluates them against resources."""

    def __init__(self) -> None:
        self._rules: list[PolicyRule] = []

    def add_rule(self, rule: PolicyRule) -> None:
        self._rules.append(rule)

    @property
    def rule_count(self) -> int:
        return len(self._rules)

    def evaluate(self, resource_id: str, resource: dict[str, Any]) -> EvaluationReport:
        report = EvaluationReport(resource_id=resource_id)
        for rule in self._rules:
            result = rule.evaluate(resource)
            report.results.append(result)
        return report

    def evaluate_batch(
        self, resources: dict[str, dict[str, Any]]
    ) -> dict[str, EvaluationReport]:
        return {rid: self.evaluate(rid, res) for rid, res in resources.items()}


# ---------------------------------------------------------------------------
# Convenience: load policies from a JSON config
# ---------------------------------------------------------------------------

def load_policies_from_config(config: dict[str, Any]) -> PolicyEngine:
    """Build a PolicyEngine from a declarative JSON config."""
    engine = PolicyEngine()
    for rule_def in config.get("rules", []):
        rule_type = rule_def["type"]
        severity = Severity[rule_def.get("severity", "ERROR").upper()]
        if rule_type == "required_field":
            engine.add_rule(RequiredFieldRule(rule_def["id"], rule_def["field"], severity))
        elif rule_type == "value_in_set":
            engine.add_rule(ValueInSetRule(rule_def["id"], rule_def["field"], set(rule_def["allowed"]), severity))
        elif rule_type == "numeric_range":
            engine.add_rule(NumericRangeRule(
                rule_def["id"], rule_def["field"],
                rule_def.get("min"), rule_def.get("max"), severity,
            ))
        else:
            raise ValueError(f"Unknown rule type: {rule_type}")
    return engine


# ---------------------------------------------------------------------------
# CLI entrypoint
# ---------------------------------------------------------------------------

def main() -> None:
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(description="Policy-as-Code Validator")
    parser.add_argument("--config", type=Path, default=Path("data/config.json"))
    parser.add_argument("--resource", type=Path, default=Path("data/sample_input.txt"))
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    resource = json.loads(args.resource.read_text(encoding="utf-8"))

    engine = load_policies_from_config(config)
    report = engine.evaluate("cli-resource", resource)

    print(json.dumps(report.summary(), indent=2))
    for r in report.results:
        tag = r.verdict.value.upper().ljust(4)
        print(f"  [{tag}] {r.rule_id}: {r.message}")


if __name__ == "__main__":
    main()
