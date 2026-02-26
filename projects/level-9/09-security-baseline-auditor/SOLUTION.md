# Solution: Level 9 / Project 09 - Security Baseline Auditor

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
"""Security Baseline Auditor — audit configurations against security baselines."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable


# --- Domain types -------------------------------------------------------

class Compliance(Enum):
    PASS = "pass"
    FAIL = "fail"
    WARNING = "warning"
    NOT_APPLICABLE = "n/a"


class ControlCategory(Enum):
    ACCESS_CONTROL = "access_control"
    ENCRYPTION = "encryption"
    LOGGING = "logging"
    NETWORK = "network"
    PATCHING = "patching"
    AUTHENTICATION = "authentication"


# WHY check_fn as a callable per control? -- Each security control has
# unique validation logic (encryption checks differ from access control checks).
# Storing the check function alongside the control metadata (Strategy pattern)
# means adding a new CIS Benchmark control is just adding one dataclass
# instance — no if/elif chain modifications needed.
@dataclass
class SecurityControl:
    """A single security control to audit."""
    control_id: str
    name: str
    category: ControlCategory
    description: str
    check_fn: Callable[[dict[str, Any]], Finding]
    severity: str = "medium"  # low, medium, high, critical


@dataclass
class Finding:
    """Result of auditing a single control."""
    control_id: str
    name: str
    compliance: Compliance
    actual_value: str
    expected_value: str
    remediation: str = ""

    def to_dict(self) -> dict[str, str]:
        return {
            "control_id": self.control_id,
            "name": self.name,
            "compliance": self.compliance.value,
            "actual": self.actual_value,
            "expected": self.expected_value,
            "remediation": self.remediation,
        }


@dataclass
class AuditReport:
    """Complete security audit report."""
    baseline_name: str
    findings: list[Finding] = field(default_factory=list)

    @property
    def pass_count(self) -> int:
        return sum(1 for f in self.findings if f.compliance == Compliance.PASS)

    @property
    def fail_count(self) -> int:
        return sum(1 for f in self.findings if f.compliance == Compliance.FAIL)

    # WHY exclude N/A from compliance percentage? -- A control marked "not
    # applicable" (e.g., encryption check on a service with no data at rest)
    # should not inflate the compliance score. Only applicable controls
    # contribute to the percentage.
    @property
    def compliance_pct(self) -> float:
        applicable = [f for f in self.findings if f.compliance != Compliance.NOT_APPLICABLE]
        if not applicable:
            return 100.0
        passed = sum(1 for f in applicable if f.compliance == Compliance.PASS)
        return round(passed / len(applicable) * 100, 1)

    def to_dict(self) -> dict[str, Any]:
        return {
            "baseline": self.baseline_name,
            "total_controls": len(self.findings),
            "passed": self.pass_count,
            "failed": self.fail_count,
            "compliance_pct": self.compliance_pct,
            "findings": [f.to_dict() for f in self.findings],
        }


# --- Baseline auditor ---------------------------------------------------

class SecurityBaselineAuditor:
    """Audits system configuration against a security baseline."""

    def __init__(self, baseline_name: str) -> None:
        self._baseline_name = baseline_name
        self._controls: list[SecurityControl] = []

    def add_control(self, control: SecurityControl) -> None:
        self._controls.append(control)

    def audit(self, config: dict[str, Any]) -> AuditReport:
        """Run all controls against the provided configuration."""
        report = AuditReport(baseline_name=self._baseline_name)
        for control in self._controls:
            finding = control.check_fn(config)
            report.findings.append(finding)
        return report


# --- Built-in security checks ------------------------------------------

def check_password_min_length(config: dict[str, Any]) -> Finding:
    actual = config.get("password_min_length", 0)
    required = 12
    return Finding(
        control_id="AUTH-001", name="Password minimum length",
        compliance=Compliance.PASS if actual >= required else Compliance.FAIL,
        actual_value=str(actual), expected_value=f">= {required}",
        remediation="Set password_min_length to at least 12",
    )


def check_mfa_enabled(config: dict[str, Any]) -> Finding:
    actual = config.get("mfa_enabled", False)
    return Finding(
        control_id="AUTH-002", name="MFA enabled",
        compliance=Compliance.PASS if actual else Compliance.FAIL,
        actual_value=str(actual), expected_value="True",
        remediation="Enable multi-factor authentication",
    )


def check_encryption_at_rest(config: dict[str, Any]) -> Finding:
    actual = config.get("encryption_at_rest", False)
    return Finding(
        control_id="ENC-001", name="Encryption at rest",
        compliance=Compliance.PASS if actual else Compliance.FAIL,
        actual_value=str(actual), expected_value="True",
        remediation="Enable encryption at rest for all data stores",
    )


def check_tls_version(config: dict[str, Any]) -> Finding:
    actual = config.get("min_tls_version", "1.0")
    required = "1.2"
    passed = actual >= required
    return Finding(
        control_id="ENC-002", name="Minimum TLS version",
        compliance=Compliance.PASS if passed else Compliance.FAIL,
        actual_value=actual, expected_value=f">= {required}",
        remediation="Set minimum TLS version to 1.2 or higher",
    )


def check_audit_logging(config: dict[str, Any]) -> Finding:
    actual = config.get("audit_logging_enabled", False)
    return Finding(
        control_id="LOG-001", name="Audit logging enabled",
        compliance=Compliance.PASS if actual else Compliance.FAIL,
        actual_value=str(actual), expected_value="True",
        remediation="Enable audit logging for all security events",
    )


def check_session_timeout(config: dict[str, Any]) -> Finding:
    actual = config.get("session_timeout_minutes", 0)
    max_allowed = 30
    return Finding(
        control_id="AUTH-003", name="Session timeout",
        compliance=Compliance.PASS if 0 < actual <= max_allowed else Compliance.FAIL,
        actual_value=str(actual), expected_value=f"<= {max_allowed} minutes",
        remediation=f"Set session timeout to {max_allowed} minutes or less",
    )


# --- Default baseline ---------------------------------------------------

def create_default_baseline() -> SecurityBaselineAuditor:
    auditor = SecurityBaselineAuditor("Standard Security Baseline v1.0")
    controls = [
        SecurityControl("AUTH-001", "Password min length", ControlCategory.AUTHENTICATION,
                        "Minimum password length", check_password_min_length, "high"),
        SecurityControl("AUTH-002", "MFA enabled", ControlCategory.AUTHENTICATION,
                        "Multi-factor authentication", check_mfa_enabled, "critical"),
        SecurityControl("ENC-001", "Encryption at rest", ControlCategory.ENCRYPTION,
                        "Data encryption at rest", check_encryption_at_rest, "critical"),
        SecurityControl("ENC-002", "TLS version", ControlCategory.ENCRYPTION,
                        "Minimum TLS version", check_tls_version, "high"),
        SecurityControl("LOG-001", "Audit logging", ControlCategory.LOGGING,
                        "Security audit logging", check_audit_logging, "high"),
        SecurityControl("AUTH-003", "Session timeout", ControlCategory.AUTHENTICATION,
                        "Session timeout policy", check_session_timeout, "medium"),
    ]
    for c in controls:
        auditor.add_control(c)
    return auditor


# --- CLI ----------------------------------------------------------------

def run_demo() -> dict[str, Any]:
    auditor = create_default_baseline()
    config = {
        "password_min_length": 8,
        "mfa_enabled": True,
        "encryption_at_rest": True,
        "min_tls_version": "1.2",
        "audit_logging_enabled": False,
        "session_timeout_minutes": 60,
    }
    report = auditor.audit(config)
    return report.to_dict()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Security baseline auditor")
    parser.add_argument("--config", default=None, help="JSON config file")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    parse_args(argv)
    print(json.dumps(run_demo(), indent=2))


if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Strategy pattern (callable per control) | Adding a new CIS control means writing one function and one SecurityControl instance; no if/elif chain to modify | Switch statement on control_id -- violates open-closed principle; every new control modifies the auditor |
| Remediation string on each finding | Actionable: a failing control tells the operator exactly what to fix | Findings without remediation -- the operator must look up the fix separately |
| NOT_APPLICABLE excluded from compliance percentage | Controls that do not apply should not inflate or deflate the score | Count N/A as passing -- artificially boosts compliance percentage |
| Factory function for default baseline | Encapsulates baseline construction; different baselines (CIS, NIST, SOC2) can use the same auditor | Hardcoded controls in the auditor -- prevents swapping baselines |
| Config dict as input rather than file path | Keeps the auditor testable and decoupled from I/O; the caller loads config from any source | Direct file reading inside audit -- couples the auditor to the filesystem, making testing harder |

## Alternative approaches

### Approach B: YAML-driven security baselines

```python
import yaml

def load_baseline_from_yaml(path: str) -> SecurityBaselineAuditor:
    """Load security controls from a YAML file, enabling non-engineers
    to define baselines without modifying Python code."""
    config = yaml.safe_load(open(path))
    auditor = SecurityBaselineAuditor(config["name"])
    for ctrl in config["controls"]:
        # Map check type to function
        check_fn = CHECK_REGISTRY[ctrl["check_type"]]
        auditor.add_control(SecurityControl(
            control_id=ctrl["id"],
            name=ctrl["name"],
            category=ControlCategory(ctrl["category"]),
            description=ctrl.get("description", ""),
            check_fn=check_fn,
            severity=ctrl.get("severity", "medium"),
        ))
    return auditor

CHECK_REGISTRY = {
    "password_min_length": check_password_min_length,
    "mfa_enabled": check_mfa_enabled,
    # ... register all check functions
}
```

**Trade-off:** YAML-driven baselines allow compliance officers to define and modify security controls without writing Python. This separates policy definition (YAML) from enforcement logic (Python). The tradeoff is that complex validation logic (like TLS version comparison) still requires code in the registry. Use code-defined baselines for learning; YAML-driven baselines when multiple compliance frameworks need to be managed by non-developers.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Config key missing from dict | `config.get()` returns the default (0, False, "1.0"); control may pass or fail based on the default | Document that missing keys are treated as the most insecure default |
| TLS version comparison as string | `"1.2" >= "1.10"` is True in string comparison (lexicographic), which is correct for TLS but not for arbitrary version strings | Use `tuple(int(x) for x in v.split("."))` for version comparison, or rely on the fact that TLS versions are single-digit minor |
| Check function raises an exception | Entire audit aborts; other controls are not evaluated | Wrap each `check_fn(config)` in try/except and record a FAIL finding with the error message |
