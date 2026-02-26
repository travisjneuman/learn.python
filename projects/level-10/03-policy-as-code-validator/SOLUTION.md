# Solution: Level 10 / Project 03 - Policy As Code Validator

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> Check the [README](./README.md) for requirements and the
>.

---

## Complete solution

```python
"""Policy-as-Code Validator -- Define and evaluate policies as Python code (OPA-style)."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Protocol


class Severity(Enum):
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()


class Verdict(Enum):
    PASS = "pass"
    FAIL = "fail"
    SKIP = "skip"


# WHY frozen=True? -- Rule results are audit evidence. Once a rule produces a
# verdict, it must never change. Immutability ensures the audit trail is
# trustworthy -- the same principle used by OPA (Open Policy Agent).
@dataclass(frozen=True)
class RuleResult:
    rule_id: str
    verdict: Verdict
    severity: Severity
    message: str
    resource_key: str = ""


@dataclass
class EvaluationReport:
    resource_id: str
    results: list[RuleResult] = field(default_factory=list)

    # WHY "all non-FAIL" instead of "all PASS"? -- SKIP verdicts are neutral
    # (field absent, rule not applicable). A resource that passes 4 rules and
    # skips 1 should still be considered passing.
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


# WHY Protocol for PolicyRule? -- New rule types can be added by any team without
# modifying the engine. As long as a class has rule_id, severity, and evaluate(),
# it plugs into the Chain of Responsibility.
class PolicyRule(Protocol):
    rule_id: str
    severity: Severity
    def evaluate(self, resource: dict[str, Any]) -> RuleResult: ...


@dataclass
class RequiredFieldRule:
    """Checks that a specific field exists and is non-empty."""
    rule_id: str
    field_name: str
    severity: Severity = Severity.ERROR

    def evaluate(self, resource: dict[str, Any]) -> RuleResult:
        value = resource.get(self.field_name)
        if value is None or value == "":
            return RuleResult(self.rule_id, Verdict.FAIL, self.severity,
                              f"Required field '{self.field_name}' is missing or empty",
                              self.field_name)
        return RuleResult(self.rule_id, Verdict.PASS, self.severity,
                          f"Field '{self.field_name}' present", self.field_name)


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
            return RuleResult(self.rule_id, Verdict.FAIL, self.severity,
                              f"'{self.field_name}' value '{value}' not in {sorted(self.allowed)}",
                              self.field_name)
        return RuleResult(self.rule_id, Verdict.PASS, self.severity,
                          f"'{self.field_name}' value '{value}' is allowed", self.field_name)


@dataclass
class NumericRangeRule:
    """Checks that a numeric field falls within [min_val, max_val]."""
    rule_id: str
    field_name: str
    min_val: float | None = None
    max_val: float | None = None
    severity: Severity = Severity.WARNING

    # WHY SKIP when field is absent? -- A missing field is different from an
    # invalid value. SKIP says "this rule doesn't apply"; FAIL says "this rule
    # was violated." This distinction is critical for audit clarity.
    def evaluate(self, resource: dict[str, Any]) -> RuleResult:
        raw = resource.get(self.field_name)
        if raw is None:
            return RuleResult(self.rule_id, Verdict.SKIP, self.severity,
                              f"Field '{self.field_name}' not present, skipping range check",
                              self.field_name)
        try:
            value = float(raw)
        except (TypeError, ValueError):
            return RuleResult(self.rule_id, Verdict.FAIL, self.severity,
                              f"Field '{self.field_name}' is not numeric: {raw!r}",
                              self.field_name)
        if self.min_val is not None and value < self.min_val:
            return RuleResult(self.rule_id, Verdict.FAIL, self.severity,
                              f"'{self.field_name}' value {value} below minimum {self.min_val}",
                              self.field_name)
        if self.max_val is not None and value > self.max_val:
            return RuleResult(self.rule_id, Verdict.FAIL, self.severity,
                              f"'{self.field_name}' value {value} above maximum {self.max_val}",
                              self.field_name)
        return RuleResult(self.rule_id, Verdict.PASS, self.severity,
                          f"'{self.field_name}' value {value} within range", self.field_name)


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


class PolicyEngine:
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
            report.results.append(rule.evaluate(resource))
        return report

    # WHY evaluate_batch returns a dict? -- Keyed by resource_id so callers can
    # look up results by ID rather than iterating a list.
    def evaluate_batch(self, resources: dict[str, dict[str, Any]]) -> dict[str, EvaluationReport]:
        return {rid: self.evaluate(rid, res) for rid, res in resources.items()}


# WHY load from JSON config? -- Separating rule definitions from code lets
# non-engineers (security teams, compliance officers) define policies
# declaratively without writing Python.
def load_policies_from_config(config: dict[str, Any]) -> PolicyEngine:
    engine = PolicyEngine()
    for rule_def in config.get("rules", []):
        rule_type = rule_def["type"]
        severity = Severity[rule_def.get("severity", "ERROR").upper()]
        if rule_type == "required_field":
            engine.add_rule(RequiredFieldRule(rule_def["id"], rule_def["field"], severity))
        elif rule_type == "value_in_set":
            engine.add_rule(ValueInSetRule(rule_def["id"], rule_def["field"],
                                           set(rule_def["allowed"]), severity))
        elif rule_type == "numeric_range":
            engine.add_rule(NumericRangeRule(rule_def["id"], rule_def["field"],
                                             rule_def.get("min"), rule_def.get("max"), severity))
        else:
            raise ValueError(f"Unknown rule type: {rule_type}")
    return engine


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
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Three-valued Verdict (PASS/FAIL/SKIP) | Distinguishes "rule violated" from "rule not applicable" -- critical for audit clarity | Binary pass/fail -- loses the "not applicable" signal |
| Severity separate from Verdict | A WARNING-severity FAIL means "fix this soon" vs ERROR-severity FAIL meaning "fix now" -- enables prioritized remediation | Severity baked into verdict -- less granular triage |
| JSON-configurable rules | Non-engineers (compliance officers) can define policies without writing Python | Python-only rules -- requires a developer for every policy change |
| Protocol-based PolicyRule | New rule types plug in without modifying the engine or inheriting from a base class | ABC inheritance -- forces coupling to the engine module |

## Alternative approaches

### Approach B: Decorator-based rule registration

```python
_RULES: dict[str, type] = {}

def policy_rule(rule_type: str):
    def decorator(cls):
        _RULES[rule_type] = cls
        return cls
    return decorator

@policy_rule("required_field")
class RequiredFieldRule:
    ...

# In load_policies_from_config:
cls = _RULES.get(rule_type)
if cls is None:
    raise ValueError(f"Unknown rule type: {rule_type}")
engine.add_rule(cls(**rule_def))
```

**Trade-off:** Decorator registration is more extensible -- adding a new rule type requires only the `@policy_rule` decorator, not an elif in `load_policies_from_config`. However, it introduces global mutable state and makes the rule-to-type mapping implicit rather than explicit.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Unknown rule type in JSON config | `ValueError` with message "Unknown rule type: X" | Validate config schema before loading, or use a registry pattern |
| Non-numeric value passed to NumericRangeRule | Returns FAIL verdict (catches `TypeError`/`ValueError` in float conversion) | Already handled -- the try/except block produces a clear failure message |
| Malformed JSON config file | `json.JSONDecodeError` with an unhelpful traceback | Wrap in try/except with a user-friendly message pointing to the config file |
