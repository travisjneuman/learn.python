# Solution: Level 9 / Project 10 - Data Governance Enforcer

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
"""Data Governance Enforcer — enforce data classification, retention, and access policies."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# --- Domain types -------------------------------------------------------

class DataClassification(Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


class AccessLevel(Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"


# WHY classification on each asset? -- GDPR/CCPA require different handling
# based on data sensitivity. PUBLIC data can be exported freely; RESTRICTED
# data requires encryption and audit logging. Tagging each asset with its
# classification lets the policy engine apply rules automatically instead
# of relying on developers to remember per-field compliance requirements.
@dataclass
class DataAsset:
    """A data asset subject to governance."""
    name: str
    classification: DataClassification
    owner: str
    retention_days: int = 365
    contains_pii: bool = False
    tags: list[str] = field(default_factory=list)


@dataclass
class AccessRequest:
    """A request to access a data asset."""
    requester: str
    role: str
    asset_name: str
    access_level: AccessLevel
    purpose: str = ""


@dataclass
class PolicyViolation:
    """A governance policy violation."""
    policy_name: str
    asset_name: str
    severity: str
    message: str
    remediation: str = ""

    def to_dict(self) -> dict[str, str]:
        return {
            "policy": self.policy_name,
            "asset": self.asset_name,
            "severity": self.severity,
            "message": self.message,
            "remediation": self.remediation,
        }


@dataclass
class RetentionPolicy:
    """Retention requirements per classification."""
    classification: DataClassification
    min_retention_days: int
    max_retention_days: int
    requires_encryption: bool = False
    requires_audit_log: bool = False


@dataclass
class AccessPolicy:
    """Access control policy mapping roles to allowed levels."""
    role: str
    max_classification: DataClassification
    allowed_access: set[AccessLevel] = field(default_factory=set)


# --- Governance engine --------------------------------------------------

# WHY a numeric rank for classifications? -- Comparing classifications
# requires an ordering (RESTRICTED > CONFIDENTIAL > INTERNAL > PUBLIC).
# A numeric mapping makes this comparison mechanical: if the asset rank
# exceeds the policy rank, access is denied. Without numeric ordering,
# you'd need a chain of if/elif comparisons.
CLASSIFICATION_RANK = {
    DataClassification.PUBLIC: 0,
    DataClassification.INTERNAL: 1,
    DataClassification.CONFIDENTIAL: 2,
    DataClassification.RESTRICTED: 3,
}


class DataGovernanceEnforcer:
    """Enforces data governance policies across assets and access requests."""

    def __init__(self) -> None:
        self._assets: dict[str, DataAsset] = {}
        self._retention_policies: dict[DataClassification, RetentionPolicy] = {}
        self._access_policies: dict[str, AccessPolicy] = {}

    def register_asset(self, asset: DataAsset) -> None:
        self._assets[asset.name] = asset

    def add_retention_policy(self, policy: RetentionPolicy) -> None:
        self._retention_policies[policy.classification] = policy

    def add_access_policy(self, policy: AccessPolicy) -> None:
        self._access_policies[policy.role] = policy

    def audit_assets(self) -> list[PolicyViolation]:
        """Check all assets against retention and classification policies."""
        violations: list[PolicyViolation] = []
        for asset in self._assets.values():
            violations.extend(self._check_retention(asset))
            violations.extend(self._check_classification(asset))
        return violations

    def evaluate_access(self, request: AccessRequest) -> tuple[bool, list[PolicyViolation]]:
        """Evaluate whether an access request should be granted."""
        violations: list[PolicyViolation] = []
        asset = self._assets.get(request.asset_name)
        if not asset:
            return False, [PolicyViolation(
                "asset_not_found", request.asset_name, "error",
                f"Asset '{request.asset_name}' not registered",
            )]

        policy = self._access_policies.get(request.role)
        if not policy:
            return False, [PolicyViolation(
                "role_not_found", request.asset_name, "error",
                f"No access policy for role '{request.role}'",
            )]

        # Check classification level
        asset_rank = CLASSIFICATION_RANK[asset.classification]
        max_rank = CLASSIFICATION_RANK[policy.max_classification]
        if asset_rank > max_rank:
            violations.append(PolicyViolation(
                "classification_exceeded", asset.name, "critical",
                f"Role '{request.role}' cannot access "
                f"{asset.classification.value} data (max: {policy.max_classification.value})",
                remediation="Request elevated access through security team",
            ))

        # Check access level
        if request.access_level not in policy.allowed_access:
            violations.append(PolicyViolation(
                "access_level_denied", asset.name, "warning",
                f"Role '{request.role}' does not have "
                f"{request.access_level.value} permission",
            ))

        # WHY require purpose for PII access? -- GDPR Article 5 requires
        # purpose limitation: personal data must be collected for a specified,
        # explicit purpose. Recording the purpose in the access request creates
        # an audit trail that demonstrates compliance.
        if asset.contains_pii and not request.purpose:
            violations.append(PolicyViolation(
                "pii_purpose_required", asset.name, "warning",
                "Access to PII requires a stated purpose",
            ))

        return len(violations) == 0, violations

    def _check_retention(self, asset: DataAsset) -> list[PolicyViolation]:
        policy = self._retention_policies.get(asset.classification)
        if not policy:
            return []
        violations: list[PolicyViolation] = []
        if asset.retention_days < policy.min_retention_days:
            violations.append(PolicyViolation(
                "retention_too_short", asset.name, "warning",
                f"Retention {asset.retention_days}d below minimum "
                f"{policy.min_retention_days}d for {asset.classification.value}",
            ))
        if asset.retention_days > policy.max_retention_days:
            violations.append(PolicyViolation(
                "retention_too_long", asset.name, "warning",
                f"Retention {asset.retention_days}d exceeds maximum "
                f"{policy.max_retention_days}d",
                remediation="Reduce retention period or request exception",
            ))
        return violations

    def _check_classification(self, asset: DataAsset) -> list[PolicyViolation]:
        if asset.contains_pii and asset.classification == DataClassification.PUBLIC:
            return [PolicyViolation(
                "pii_public_data", asset.name, "critical",
                "PII data cannot be classified as public",
                remediation="Reclassify to at least INTERNAL",
            )]
        return []

    def compliance_summary(self) -> dict[str, Any]:
        violations = self.audit_assets()
        return {
            "total_assets": len(self._assets),
            "violations": len(violations),
            "by_severity": {
                s: sum(1 for v in violations if v.severity == s)
                for s in ["critical", "warning", "error"]
            },
            "details": [v.to_dict() for v in violations],
        }


# --- Demo ---------------------------------------------------------------

def run_demo() -> dict[str, Any]:
    enforcer = DataGovernanceEnforcer()

    enforcer.add_retention_policy(RetentionPolicy(DataClassification.PUBLIC, 30, 365))
    enforcer.add_retention_policy(RetentionPolicy(DataClassification.CONFIDENTIAL, 90, 730))
    enforcer.add_retention_policy(RetentionPolicy(DataClassification.RESTRICTED, 365, 2555))

    enforcer.add_access_policy(AccessPolicy(
        "analyst", DataClassification.INTERNAL, {AccessLevel.READ},
    ))
    enforcer.add_access_policy(AccessPolicy(
        "engineer", DataClassification.CONFIDENTIAL, {AccessLevel.READ, AccessLevel.WRITE},
    ))
    enforcer.add_access_policy(AccessPolicy(
        "admin", DataClassification.RESTRICTED, {AccessLevel.READ, AccessLevel.WRITE, AccessLevel.DELETE, AccessLevel.ADMIN},
    ))

    enforcer.register_asset(DataAsset("user_profiles", DataClassification.CONFIDENTIAL, "identity-team", 365, True))
    enforcer.register_asset(DataAsset("public_docs", DataClassification.PUBLIC, "docs-team", 180))
    enforcer.register_asset(DataAsset("payment_data", DataClassification.RESTRICTED, "payments-team", 730, True))
    enforcer.register_asset(DataAsset("pii_leak", DataClassification.PUBLIC, "unknown", 30, True))  # violation!

    summary = enforcer.compliance_summary()

    allowed, _ = enforcer.evaluate_access(AccessRequest("alice", "analyst", "public_docs", AccessLevel.READ))
    denied, violations = enforcer.evaluate_access(AccessRequest("bob", "analyst", "payment_data", AccessLevel.READ))

    return {
        "compliance": summary,
        "access_tests": [
            {"requester": "alice", "asset": "public_docs", "allowed": allowed},
            {"requester": "bob", "asset": "payment_data", "allowed": denied,
             "violations": [v.to_dict() for v in violations]},
        ],
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Data governance enforcer")
    parser.add_argument("--demo", action="store_true", default=True)
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
| Numeric classification ranking | Enables mechanical comparison (`asset_rank > max_rank`) for access control decisions | String-based comparison -- requires mapping logic or chain of if/elif for each pair |
| Separate retention and access policies | Retention is about data lifecycle (how long to keep); access is about authorization (who can see). Different concerns, different policy shapes | Single unified policy -- conflates two independent regulatory requirements |
| Purpose requirement for PII access | GDPR Article 5 mandates purpose limitation; recording purpose creates an audit trail | No purpose tracking -- fails regulatory compliance for personal data access |
| Critical severity for PII classified as public | This is the most dangerous misconfiguration: personal data exposed to everyone | Warning severity -- too lenient for a violation that could result in regulatory fines |
| `evaluate_access` returns both boolean and violations list | The boolean answers "allow or deny" immediately; the violations list explains why and what to fix | Boolean only -- the caller has to re-evaluate to understand the denial reason |

## Alternative approaches

### Approach B: Attribute-based access control (ABAC)

```python
class ABACEnforcer:
    """ABAC evaluates access based on multiple attributes (role, department,
    time of day, location) rather than just role-to-classification mapping.
    More flexible but more complex to reason about."""
    def __init__(self):
        self._policies: list[dict] = []

    def add_policy(self, conditions: dict, effect: str):
        """conditions: {attribute: value} pairs that must all match."""
        self._policies.append({"conditions": conditions, "effect": effect})

    def evaluate(self, request_attributes: dict) -> str:
        for policy in self._policies:
            if all(
                request_attributes.get(k) == v
                for k, v in policy["conditions"].items()
            ):
                return policy["effect"]  # "allow" or "deny"
        return "deny"  # deny by default
```

**Trade-off:** ABAC is more flexible than role-based access control (RBAC). Instead of mapping roles to classifications, you define policies over arbitrary attributes (department, time, location, data type). This enables fine-grained rules like "analysts can read CONFIDENTIAL data during business hours from the office network." The tradeoff is policy explosion: more attributes mean more rules to manage and audit. Use RBAC for simple systems; ABAC when you need fine-grained, context-aware access control.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Asset registered without a matching retention policy | `_check_retention` returns empty list; retention is not enforced | Log a warning when an asset's classification has no retention policy |
| Role not registered in access policies | `evaluate_access` returns False with "role_not_found" violation | Ensure all roles are registered during setup; consider a default policy for unknown roles |
| PII data classified as INTERNAL (not PUBLIC) | Passes the `_check_classification` check but may still need special handling | Add additional PII checks for INTERNAL classification (e.g., require encryption, audit logging) |
