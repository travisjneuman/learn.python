"""Tests for Data Governance Enforcer.

Covers: retention policies, access control, PII handling, and compliance summary.
"""

from __future__ import annotations

import pytest

from project import (
    AccessLevel,
    AccessPolicy,
    AccessRequest,
    DataAsset,
    DataClassification,
    DataGovernanceEnforcer,
    RetentionPolicy,
)


# --- Fixtures -----------------------------------------------------------

@pytest.fixture
def enforcer() -> DataGovernanceEnforcer:
    e = DataGovernanceEnforcer()
    e.add_retention_policy(RetentionPolicy(DataClassification.PUBLIC, 30, 365))
    e.add_retention_policy(RetentionPolicy(DataClassification.CONFIDENTIAL, 90, 730))
    e.add_access_policy(AccessPolicy("viewer", DataClassification.INTERNAL, {AccessLevel.READ}))
    e.add_access_policy(AccessPolicy("admin", DataClassification.RESTRICTED,
                                      {AccessLevel.READ, AccessLevel.WRITE, AccessLevel.DELETE, AccessLevel.ADMIN}))
    return e


# --- Retention checks ---------------------------------------------------

class TestRetention:
    def test_retention_too_short(self, enforcer: DataGovernanceEnforcer) -> None:
        enforcer.register_asset(DataAsset("short", DataClassification.CONFIDENTIAL, "t", 30))
        violations = enforcer.audit_assets()
        assert any(v.policy_name == "retention_too_short" for v in violations)

    def test_retention_too_long(self, enforcer: DataGovernanceEnforcer) -> None:
        enforcer.register_asset(DataAsset("long", DataClassification.PUBLIC, "t", 500))
        violations = enforcer.audit_assets()
        assert any(v.policy_name == "retention_too_long" for v in violations)

    def test_valid_retention(self, enforcer: DataGovernanceEnforcer) -> None:
        enforcer.register_asset(DataAsset("ok", DataClassification.PUBLIC, "t", 180))
        violations = enforcer.audit_assets()
        retention_viols = [v for v in violations if v.asset_name == "ok"]
        assert len(retention_viols) == 0


# --- Classification checks ---------------------------------------------

class TestClassification:
    def test_pii_public_violation(self, enforcer: DataGovernanceEnforcer) -> None:
        enforcer.register_asset(DataAsset("leak", DataClassification.PUBLIC, "t", 30, True))
        violations = enforcer.audit_assets()
        assert any(v.policy_name == "pii_public_data" for v in violations)


# --- Access control -----------------------------------------------------

class TestAccessControl:
    def test_allowed_access(self, enforcer: DataGovernanceEnforcer) -> None:
        enforcer.register_asset(DataAsset("doc", DataClassification.INTERNAL, "t"))
        allowed, violations = enforcer.evaluate_access(
            AccessRequest("alice", "viewer", "doc", AccessLevel.READ)
        )
        assert allowed is True
        assert len(violations) == 0

    def test_classification_exceeded(self, enforcer: DataGovernanceEnforcer) -> None:
        enforcer.register_asset(DataAsset("secret", DataClassification.RESTRICTED, "t"))
        allowed, violations = enforcer.evaluate_access(
            AccessRequest("bob", "viewer", "secret", AccessLevel.READ)
        )
        assert allowed is False
        assert any(v.policy_name == "classification_exceeded" for v in violations)

    def test_pii_requires_purpose(self, enforcer: DataGovernanceEnforcer) -> None:
        enforcer.register_asset(DataAsset("users", DataClassification.INTERNAL, "t", 365, True))
        allowed, violations = enforcer.evaluate_access(
            AccessRequest("carol", "viewer", "users", AccessLevel.READ, purpose="")
        )
        assert any(v.policy_name == "pii_purpose_required" for v in violations)

    @pytest.mark.parametrize("role,expected_allowed", [
        ("admin", True),
        ("viewer", False),
    ])
    def test_delete_access(self, enforcer: DataGovernanceEnforcer,
                           role: str, expected_allowed: bool) -> None:
        enforcer.register_asset(DataAsset("data", DataClassification.INTERNAL, "t"))
        allowed, _ = enforcer.evaluate_access(
            AccessRequest("x", role, "data", AccessLevel.DELETE)
        )
        assert allowed == expected_allowed

    def test_unknown_asset(self, enforcer: DataGovernanceEnforcer) -> None:
        allowed, violations = enforcer.evaluate_access(
            AccessRequest("x", "admin", "nonexistent", AccessLevel.READ)
        )
        assert allowed is False
