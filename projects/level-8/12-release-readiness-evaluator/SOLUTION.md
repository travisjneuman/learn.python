# Solution: Level 8 / Project 12 - Release Readiness Evaluator

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
"""Release Readiness Evaluator -- score release readiness based on configurable criteria."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable

class ReadinessLevel(Enum):
    GO = "go"
    CONDITIONAL = "conditional"
    NO_GO = "no_go"

class CriterionCategory(Enum):
    TESTING = "testing"
    SECURITY = "security"
    DOCUMENTATION = "documentation"
    PERFORMANCE = "performance"
    COMPLIANCE = "compliance"
    INFRASTRUCTURE = "infrastructure"

# WHY weighted scoring + required flag? -- Not all gates are equal: 80%
# test coverage is acceptable, but a critical vulnerability is always a
# blocker. Weights produce a nuanced score, while required=True gives
# hard veto power -- matching how CI/CD gates work (GitHub required
# checks + optional quality scores).
@dataclass
class Criterion:
    name: str
    category: CriterionCategory
    weight: float
    evaluate_fn: Callable[[], CriterionResult]
    required: bool = False

@dataclass
class CriterionResult:
    name: str
    passed: bool
    score: float  # 0.0 - 1.0
    message: str = ""
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "passed": self.passed,
                "score": round(self.score, 2), "message": self.message}

@dataclass
class ReadinessReport:
    release_name: str
    overall_score: float
    readiness: ReadinessLevel
    criteria_results: list[CriterionResult]
    required_failures: list[str]
    go_threshold: float
    conditional_threshold: float

    @property
    def passed_count(self) -> int:
        return sum(1 for r in self.criteria_results if r.passed)

    @property
    def failed_count(self) -> int:
        return sum(1 for r in self.criteria_results if not r.passed)

    def to_dict(self) -> dict[str, Any]:
        return {
            "release_name": self.release_name,
            "overall_score": round(self.overall_score, 2),
            "readiness": self.readiness.value,
            "passed": self.passed_count, "failed": self.failed_count,
            "required_failures": self.required_failures,
            "criteria": [r.to_dict() for r in self.criteria_results],
        }

@dataclass
class EvaluatorConfig:
    go_threshold: float = 0.8
    conditional_threshold: float = 0.6

class ReleaseReadinessEvaluator:
    def __init__(self, config: EvaluatorConfig | None = None) -> None:
        self._config = config or EvaluatorConfig()
        self._criteria: list[Criterion] = []

    def add_criterion(self, criterion: Criterion) -> None:
        self._criteria.append(criterion)

    def evaluate(self, release_name: str) -> ReadinessReport:
        results: list[CriterionResult] = []
        required_failures: list[str] = []
        total_weight = sum(c.weight for c in self._criteria)

        if total_weight == 0:
            return ReadinessReport(
                release_name=release_name, overall_score=0.0,
                readiness=ReadinessLevel.NO_GO, criteria_results=[],
                required_failures=[], go_threshold=self._config.go_threshold,
                conditional_threshold=self._config.conditional_threshold)

        # WHY weighted average? -- Different criteria matter differently.
        # Security (weight=0.25) affects the score more than changelog (0.10).
        weighted_score = 0.0
        for criterion in self._criteria:
            result = criterion.evaluate_fn()
            results.append(result)
            weighted_score += result.score * (criterion.weight / total_weight)
            if criterion.required and not result.passed:
                required_failures.append(criterion.name)

        # WHY required failures override score? -- Even a 95% score is NO_GO
        # if a required criterion (critical security) fails. Hard vetoes
        # prevent gaming the system with high optional scores.
        if required_failures:
            readiness = ReadinessLevel.NO_GO
        elif weighted_score >= self._config.go_threshold:
            readiness = ReadinessLevel.GO
        elif weighted_score >= self._config.conditional_threshold:
            readiness = ReadinessLevel.CONDITIONAL
        else:
            readiness = ReadinessLevel.NO_GO

        return ReadinessReport(
            release_name=release_name, overall_score=weighted_score,
            readiness=readiness, criteria_results=results,
            required_failures=required_failures,
            go_threshold=self._config.go_threshold,
            conditional_threshold=self._config.conditional_threshold)

# --- Criterion factories ------------------------------------------------

def coverage_criterion(coverage_pct: float, required_pct: float = 80.0) -> Criterion:
    def evaluate() -> CriterionResult:
        score = min(coverage_pct / required_pct, 1.0)
        return CriterionResult(name="test_coverage", passed=coverage_pct >= required_pct,
                               score=score, message=f"Coverage {coverage_pct}% (required {required_pct}%)")
    return Criterion(name="test_coverage", category=CriterionCategory.TESTING,
                     weight=0.25, evaluate_fn=evaluate, required=True)

def lint_clean_criterion(issues_count: int) -> Criterion:
    def evaluate() -> CriterionResult:
        return CriterionResult(name="lint_clean", passed=issues_count == 0,
                               score=1.0 if issues_count == 0 else max(0, 1 - issues_count / 20),
                               message=f"{issues_count} lint issues")
    return Criterion(name="lint_clean", category=CriterionCategory.TESTING,
                     weight=0.15, evaluate_fn=evaluate)

def security_scan_criterion(vulnerabilities: int, critical: int = 0) -> Criterion:
    def evaluate() -> CriterionResult:
        return CriterionResult(name="security_scan", passed=critical == 0,
                               score=1.0 if vulnerabilities == 0 else max(0, 1 - vulnerabilities / 10),
                               message=f"{vulnerabilities} vulns ({critical} critical)")
    return Criterion(name="security_scan", category=CriterionCategory.SECURITY,
                     weight=0.25, evaluate_fn=evaluate, required=True)

def changelog_criterion(has_entry: bool) -> Criterion:
    def evaluate() -> CriterionResult:
        return CriterionResult(name="changelog_updated", passed=has_entry,
                               score=1.0 if has_entry else 0.0,
                               message="Changelog updated" if has_entry else "No changelog entry")
    return Criterion(name="changelog_updated", category=CriterionCategory.DOCUMENTATION,
                     weight=0.10, evaluate_fn=evaluate)

def performance_criterion(p99_ms: float, threshold_ms: float = 500.0) -> Criterion:
    def evaluate() -> CriterionResult:
        score = min(threshold_ms / max(p99_ms, 0.1), 1.0)
        return CriterionResult(name="performance_p99", passed=p99_ms <= threshold_ms,
                               score=score, message=f"p99={p99_ms}ms (threshold={threshold_ms}ms)")
    return Criterion(name="performance_p99", category=CriterionCategory.PERFORMANCE,
                     weight=0.25, evaluate_fn=evaluate)

def run_demo() -> dict[str, Any]:
    evaluator = ReleaseReadinessEvaluator()
    evaluator.add_criterion(coverage_criterion(85.0))
    evaluator.add_criterion(lint_clean_criterion(2))
    evaluator.add_criterion(security_scan_criterion(1, critical=0))
    evaluator.add_criterion(changelog_criterion(True))
    evaluator.add_criterion(performance_criterion(320.0))
    return evaluator.evaluate("v2.1.0-rc1").to_dict()

def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Release readiness evaluator")
    parser.add_argument("--release", default="v2.1.0-rc1")
    parser.parse_args(argv)
    print(json.dumps(run_demo(), indent=2))

if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Weighted scoring with normalized weights | Different criteria matter differently; weights express relative importance | Equal weights -- treats all criteria as equally important, which they aren't |
| `required=True` as hard veto | A critical security failure must block release regardless of overall score | Severity multipliers -- more nuanced but risks a high score hiding a critical failure |
| Factory functions for criteria | Encapsulate evaluation logic with configuration; easy to add new criteria | Class inheritance -- more formal OOP but excessive for simple pass/fail evaluations |
| Three-level readiness (GO/CONDITIONAL/NO_GO) | Allows "ship with conditions" -- common in real release processes | Binary go/no-go -- loses the nuance of conditional releases |

## Alternative approaches

### Approach B: Policy-as-code with YAML configuration

```python
import yaml

def load_criteria_from_yaml(path: str) -> list[Criterion]:
    """Load release criteria from a YAML config file.
    Allows non-engineers to modify release gates."""
    config = yaml.safe_load(open(path))
    criteria = []
    for c in config["criteria"]:
        criteria.append(Criterion(
            name=c["name"], category=CriterionCategory(c["category"]),
            weight=c["weight"], required=c.get("required", False),
            evaluate_fn=build_evaluator(c["type"], c["config"]),
        ))
    return criteria
```

**Trade-off:** YAML-driven criteria allow release managers to modify gates without code changes. This is how mature CI/CD systems work (GitHub Actions, GitLab CI). The tradeoff is that YAML cannot express arbitrary evaluation logic -- complex criteria still need code.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| All criteria have weight=0 | Division by zero in weighted average calculation | Guard with `if total_weight == 0: return NO_GO` |
| Required criterion with high score | Even score=0.95 is overridden to NO_GO if a required criterion fails | This is intentional; document that required criteria are hard vetoes |
| Adding criteria after evaluate() | New criteria are not included in the previous report | Evaluator is stateless -- each call to `evaluate()` uses the current criteria list |
