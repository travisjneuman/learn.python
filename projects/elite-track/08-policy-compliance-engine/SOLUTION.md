# Solution: Elite Track / Policy and Compliance Engine

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> Check the [README](./README.md) for requirements and the
> [Walkthrough](./WALKTHROUGH.md) for guided hints.

---

## Complete solution

```python
"""Policy and Compliance Engine.

This project is part of the elite extension track.
It intentionally emphasizes explicit, testable engineering decisions.
"""

# WHY policy-as-code? -- Writing compliance rules as executable code (not
# documents) means they can be version-controlled, tested, and enforced
# automatically in CI/CD pipelines. This is the same approach as OPA
# (Open Policy Agent) and AWS Config Rules.

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    """Parse CLI inputs for deterministic project execution."""
    parser = argparse.ArgumentParser(description="Policy and Compliance Engine")
    parser.add_argument("--input", required=True, help="Path to input text data")
    parser.add_argument("--output", required=True, help="Path to output JSON summary")
    parser.add_argument("--run-id", default="manual-run", help="Optional run identifier")
    return parser.parse_args()


def load_lines(input_path: Path) -> list[str]:
    """Load normalized input lines and reject empty datasets safely."""
    if not input_path.exists():
        raise FileNotFoundError(f"input file not found: {input_path}")
    lines = [line.strip() for line in input_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        raise ValueError("input file contains no usable lines")
    return lines


def classify_line(line: str) -> dict[str, Any]:
    """Transform one CSV-like line into structured fields with validation."""
    parts = [piece.strip() for piece in line.split(",")]
    if len(parts) != 3:
        raise ValueError(f"invalid line format (expected 3 comma fields): {line}")

    name, score_raw, severity = parts
    score = int(score_raw)
    return {
        "name": name,
        "score": score,
        "severity": severity,
        # WHY is_high_risk for compliance? -- In a policy context, "warn"
        # and "critical" map to compliance violations that require remediation.
        # Low scores indicate controls that are not meeting minimum standards.
        # Flagging these generates audit evidence for remediation tracking.
        "is_high_risk": severity in {"warn", "critical"} or score < 5,
    }


def build_summary(records: list[dict[str, Any]], project_title: str, run_id: str) -> dict[str, Any]:
    """Build deterministic summary payload for testing and teach-back review."""
    high_risk_count = sum(1 for record in records if record["is_high_risk"])
    avg_score = round(sum(record["score"] for record in records) / len(records), 2)

    return {
        "project_title": project_title,
        "run_id": run_id,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "record_count": len(records),
        "high_risk_count": high_risk_count,
        "average_score": avg_score,
        "records": records,
    }


def write_summary(output_path: Path, payload: dict[str, Any]) -> None:
    """Write JSON output with parent directory creation for first-time runs."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> int:
    """Execute end-to-end project run."""
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    lines = load_lines(input_path)
    records = [classify_line(line) for line in lines]

    payload = build_summary(records, "Policy and Compliance Engine", args.run_id)
    write_summary(output_path, payload)

    print(f"output_summary.json written to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Policy-as-code (executable rules) | Version-controlled, testable, enforceable in CI/CD; same approach as OPA and AWS Config Rules | Document-based policies -- not enforceable automatically, drift from actual practice |
| Deterministic policy evaluation | Compliance audits must be reproducible; auditors need to see the same results every time | Real-time policy evaluation against live infrastructure -- realistic but non-reproducible |
| High-risk flagging for violations | Maps directly to compliance findings that require remediation; auditors expect a clear list of violations | Pass/fail only -- misses the severity gradient between minor warnings and critical violations |
| JSON output as audit evidence | Structured evidence is required by compliance frameworks (SOC2, ISO 27001); JSON is machine-parseable | PDF reports -- human-readable but not automatable |

## Alternative approaches

### Approach B: Rule engine with declarative policy definitions

```python
from dataclasses import dataclass
from typing import Callable, Any

@dataclass(frozen=True)
class PolicyRule:
    rule_id: str
    description: str
    check_fn: Callable[[dict[str, Any]], bool]
    severity: str = "warn"

def evaluate_policies(resource: dict[str, Any], rules: list[PolicyRule]) -> list[dict]:
    """Evaluate a resource against all policy rules."""
    violations = []
    for rule in rules:
        if not rule.check_fn(resource):
            violations.append({
                "rule_id": rule.rule_id,
                "description": rule.description,
                "severity": rule.severity,
            })
    return violations

# Example usage:
rules = [
    PolicyRule("SEC-001", "Encryption at rest must be enabled",
               lambda r: r.get("encryption_enabled", False), "critical"),
    PolicyRule("SEC-002", "Public access must be disabled",
               lambda r: not r.get("public_access", True), "critical"),
    PolicyRule("OPS-001", "Backup must be configured",
               lambda r: r.get("backup_enabled", False), "warn"),
]
```

**Trade-off:** A declarative rule engine lets non-developers define policies as data (JSON/YAML) rather than code. This is how Open Policy Agent (OPA) works. However, callable-based rules are more flexible and can express complex logic. The trade-off is between accessibility (anyone can write rules) and expressiveness (complex conditions).

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Policy rules that conflict with each other | One rule requires encryption, another prohibits it for a specific service -- evaluation produces contradictory findings | Add conflict detection that flags mutually exclusive rules before evaluation |
| Compliance framework changes mid-audit | Rules that were passing now fail; existing evidence becomes invalid | Version policy rule sets and tie each audit to a specific rule version |
| False positives from overly strict rules | Teams ignore compliance alerts (alert fatigue), missing real violations | Tune severity levels carefully; use "warn" for aspirational rules and "critical" only for regulatory requirements |
