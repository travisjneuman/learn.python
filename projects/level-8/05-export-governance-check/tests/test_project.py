"""Tests for Export Governance Check.

Covers: PII detection, row limits, format validation, classification, and rule engine.
"""

from __future__ import annotations

import pytest

from project import (
    ExportFormat,
    ExportRequest,
    GovernanceResult,
    Severity,
    check_classification_level,
    check_format_allowed,
    check_pii_columns,
    check_pii_content,
    check_row_limit,
    evaluate_export,
)


# --- Fixtures -----------------------------------------------------------

@pytest.fixture
def clean_request() -> ExportRequest:
    """A request with no governance issues."""
    return ExportRequest(
        export_id="test-001",
        requester="analyst",
        format=ExportFormat.CSV,
        columns=["name", "department", "start_date"],
        row_count=100,
        data_sample=[{"name": "Alice", "department": "eng", "start_date": "2024-01"}],
        classification="internal",
    )


@pytest.fixture
def pii_request() -> ExportRequest:
    """A request containing PII in columns and content."""
    return ExportRequest(
        export_id="test-002",
        requester="analyst",
        format=ExportFormat.CSV,
        columns=["name", "ssn", "email_addr"],
        row_count=50,
        data_sample=[
            {"name": "Bob", "ssn": "123-45-6789", "email_addr": "bob@example.com"},
        ],
        classification="internal",
    )


# --- PII column detection -----------------------------------------------

class TestPIIColumns:
    def test_flags_pii_column_names(self, pii_request: ExportRequest) -> None:
        violations = check_pii_columns(pii_request)
        flagged_cols = {v.field_name for v in violations}
        assert "ssn" in flagged_cols

    def test_clean_columns_pass(self, clean_request: ExportRequest) -> None:
        violations = check_pii_columns(clean_request)
        assert len(violations) == 0


# --- PII content detection ----------------------------------------------

class TestPIIContent:
    @pytest.mark.parametrize("value,should_detect", [
        ("123-45-6789", True),      # SSN
        ("bob@example.com", True),   # email
        ("555-123-4567", True),      # phone
        ("just plain text", False),  # clean
    ])
    def test_detects_pii_patterns(self, value: str, should_detect: bool) -> None:
        request = ExportRequest(
            export_id="t", requester="x", format=ExportFormat.CSV,
            columns=["data"], row_count=1,
            data_sample=[{"data": value}],
        )
        violations = check_pii_content(request)
        assert (len(violations) > 0) == should_detect


# --- Row limit ----------------------------------------------------------

class TestRowLimit:
    @pytest.mark.parametrize("rows,max_rows,should_block", [
        (100, 1000, False),
        (100_001, 100_000, True),
        (100_000, 100_000, False),  # exactly at limit
    ])
    def test_row_limit(self, rows: int, max_rows: int, should_block: bool) -> None:
        request = ExportRequest(
            export_id="t", requester="x", format=ExportFormat.CSV,
            columns=[], row_count=rows,
        )
        violations = check_row_limit(request, max_rows=max_rows)
        assert (len(violations) > 0) == should_block


# --- Format validation --------------------------------------------------

class TestFormatAllowed:
    def test_csv_allowed_by_default(self, clean_request: ExportRequest) -> None:
        assert len(check_format_allowed(clean_request)) == 0

    def test_excel_blocked_by_default(self) -> None:
        request = ExportRequest(
            export_id="t", requester="x", format=ExportFormat.EXCEL,
            columns=[], row_count=1,
        )
        violations = check_format_allowed(request)
        assert len(violations) == 1
        assert violations[0].severity == Severity.BLOCKING


# --- Classification -----------------------------------------------------

class TestClassification:
    @pytest.mark.parametrize("classification,expected_count", [
        ("public", 0),
        ("internal", 0),
        ("confidential", 1),  # warning
        ("restricted", 1),    # blocking
    ])
    def test_classification_levels(self, classification: str, expected_count: int) -> None:
        request = ExportRequest(
            export_id="t", requester="x", format=ExportFormat.CSV,
            columns=[], row_count=1, classification=classification,
        )
        violations = check_classification_level(request)
        assert len(violations) == expected_count


# --- Full evaluation ----------------------------------------------------

class TestEvaluateExport:
    def test_clean_export_approved(self, clean_request: ExportRequest) -> None:
        result = evaluate_export(clean_request)
        assert result.approved is True
        assert result.blocking_count == 0

    def test_pii_export_blocked(self, pii_request: ExportRequest) -> None:
        result = evaluate_export(pii_request)
        assert result.approved is False
        assert result.blocking_count > 0
