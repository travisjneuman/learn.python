"""Tests for Service Account Policy Check."""

from __future__ import annotations

import json

import pytest

from project import (
    PolicyRule,
    ServiceAccount,
    check_key_age,
    check_max_permissions,
    check_naming,
    check_unknown_permissions,
    compliance_summary,
    run,
    run_policy_check,
)


@pytest.fixture
def good_account() -> ServiceAccount:
    return ServiceAccount(
        name="svc-data-loader",
        permissions=["read", "write"],
        key_created_at=1_700_000_000,
    )


class TestIndividualChecks:
    def test_max_permissions_pass(self, good_account: ServiceAccount) -> None:
        assert check_max_permissions(good_account, 5) is None

    def test_max_permissions_fail(self, good_account: ServiceAccount) -> None:
        good_account.permissions = ["read", "write", "delete", "admin", "deploy", "logs:read"]
        v = check_max_permissions(good_account, 5)
        assert v is not None
        assert "6 permissions" in v.message

    def test_key_age_pass(self, good_account: ServiceAccount) -> None:
        now = good_account.key_created_at + 86400 * 30  # 30 days
        assert check_key_age(good_account, 90, now) is None

    def test_key_age_fail(self, good_account: ServiceAccount) -> None:
        now = good_account.key_created_at + 86400 * 100  # 100 days
        v = check_key_age(good_account, 90, now)
        assert v is not None

    @pytest.mark.parametrize("name,pattern,valid", [
        ("svc-loader", r"^svc-", True),
        ("my-app", r"^svc-", False),
        ("bot_reader", r"^(svc|bot)[-_]", True),
    ])
    def test_naming(self, name: str, pattern: str, valid: bool) -> None:
        acct = ServiceAccount(name, [], 0)
        result = check_naming(acct, pattern)
        assert (result is None) == valid

    def test_unknown_permissions(self) -> None:
        acct = ServiceAccount("x", ["read", "hack_stuff"], 0)
        vs = check_unknown_permissions(acct)
        assert len(vs) == 1
        assert "hack_stuff" in vs[0].message


class TestPolicyCheck:
    def test_compliant_account(self, good_account: ServiceAccount) -> None:
        rules = [PolicyRule("perm_limit", "max_permissions", {"max": 5})]
        vs = run_policy_check([good_account], rules)
        assert len(vs) == 0

    def test_multiple_violations(self) -> None:
        bad = ServiceAccount("bad_name", ["read", "write", "delete", "admin", "deploy", "hack"],
                             key_created_at=0)
        rules = [
            PolicyRule("perms", "max_permissions", {"max": 3}),
            PolicyRule("naming", "naming", {"pattern": r"^svc-"}),
            PolicyRule("age", "key_age", {"max_days": 90}),
        ]
        vs = run_policy_check([bad], rules, now=86400 * 365)
        assert len(vs) >= 3  # perms + naming + age + unknown perm


class TestComplianceSummary:
    def test_all_compliant(self) -> None:
        accts = [ServiceAccount("svc-a", ["read"], 0)]
        s = compliance_summary(accts, [])
        assert s["compliant"] == 1
        assert s["non_compliant"] == 0


@pytest.mark.integration
def test_run_end_to_end(tmp_path) -> None:
    config = {
        "now": 1_700_100_000,
        "accounts": [
            {"name": "svc-loader", "permissions": ["read", "write"],
             "key_created_at": 1_700_000_000},
            {"name": "bad-bot", "permissions": ["admin", "delete", "deploy", "read", "write", "logs:read"],
             "key_created_at": 1_690_000_000},
        ],
        "rules": [
            {"name": "perm_limit", "check": "max_permissions", "params": {"max": 4}},
            {"name": "naming", "check": "naming", "params": {"pattern": "^svc-"}},
            {"name": "key_age", "check": "key_age", "params": {"max_days": 90}},
        ],
    }
    inp = tmp_path / "config.json"
    inp.write_text(json.dumps(config), encoding="utf-8")
    out = tmp_path / "out.json"
    summary = run(inp, out)
    assert summary["non_compliant"] >= 1
    assert summary["total_violations"] >= 2
