"""Tests for Security Baseline Auditor.

Covers: individual checks, baseline auditing, compliance scoring, and reporting.
"""

from __future__ import annotations

import pytest

from project import (
    AuditReport,
    Compliance,
    Finding,
    check_encryption_at_rest,
    check_mfa_enabled,
    check_password_min_length,
    check_session_timeout,
    check_tls_version,
    create_default_baseline,
)


# --- Individual checks --------------------------------------------------

class TestPasswordCheck:
    @pytest.mark.parametrize("length,expected", [
        (12, Compliance.PASS),
        (16, Compliance.PASS),
        (8, Compliance.FAIL),
        (0, Compliance.FAIL),
    ])
    def test_password_min_length(self, length: int, expected: Compliance) -> None:
        result = check_password_min_length({"password_min_length": length})
        assert result.compliance == expected


class TestMFACheck:
    def test_mfa_enabled(self) -> None:
        assert check_mfa_enabled({"mfa_enabled": True}).compliance == Compliance.PASS

    def test_mfa_disabled(self) -> None:
        assert check_mfa_enabled({"mfa_enabled": False}).compliance == Compliance.FAIL

    def test_mfa_missing(self) -> None:
        assert check_mfa_enabled({}).compliance == Compliance.FAIL


class TestTLSCheck:
    @pytest.mark.parametrize("version,expected", [
        ("1.2", Compliance.PASS),
        ("1.3", Compliance.PASS),
        ("1.1", Compliance.FAIL),
        ("1.0", Compliance.FAIL),
    ])
    def test_tls_versions(self, version: str, expected: Compliance) -> None:
        result = check_tls_version({"min_tls_version": version})
        assert result.compliance == expected


class TestSessionTimeout:
    @pytest.mark.parametrize("minutes,expected", [
        (15, Compliance.PASS),
        (30, Compliance.PASS),
        (60, Compliance.FAIL),
        (0, Compliance.FAIL),
    ])
    def test_timeout_values(self, minutes: int, expected: Compliance) -> None:
        result = check_session_timeout({"session_timeout_minutes": minutes})
        assert result.compliance == expected


# --- Full baseline audit ------------------------------------------------

class TestBaselineAudit:
    def test_fully_compliant_config(self) -> None:
        auditor = create_default_baseline()
        config = {
            "password_min_length": 16,
            "mfa_enabled": True,
            "encryption_at_rest": True,
            "min_tls_version": "1.3",
            "audit_logging_enabled": True,
            "session_timeout_minutes": 15,
        }
        report = auditor.audit(config)
        assert report.compliance_pct == 100.0
        assert report.fail_count == 0

    def test_partially_compliant_config(self) -> None:
        auditor = create_default_baseline()
        config = {
            "password_min_length": 8,
            "mfa_enabled": True,
            "encryption_at_rest": False,
            "min_tls_version": "1.2",
            "audit_logging_enabled": True,
            "session_timeout_minutes": 30,
        }
        report = auditor.audit(config)
        assert 0 < report.compliance_pct < 100

    def test_report_serialization(self) -> None:
        auditor = create_default_baseline()
        report = auditor.audit({"mfa_enabled": True})
        d = report.to_dict()
        assert "compliance_pct" in d
        assert "findings" in d
        assert len(d["findings"]) == 6
