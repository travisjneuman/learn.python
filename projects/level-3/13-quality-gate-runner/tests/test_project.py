"""Tests for Quality Gate Runner."""

from pathlib import Path

import pytest

from project import (
    GateResult,
    PipelineResult,
    check_file_exists,
    check_file_size,
    check_no_print_statements,
    check_no_syntax_errors,
    format_pipeline_text,
    run_default_gates,
    run_pipeline,
)


@pytest.fixture
def valid_py(tmp_path: Path) -> Path:
    """Create a valid Python file."""
    f = tmp_path / "good.py"
    f.write_text("def hello():\n    return 42\n", encoding="utf-8")
    return f


@pytest.fixture
def bad_syntax_py(tmp_path: Path) -> Path:
    """Create a Python file with syntax errors."""
    f = tmp_path / "bad.py"
    f.write_text("def broken(\n", encoding="utf-8")
    return f


@pytest.fixture
def print_py(tmp_path: Path) -> Path:
    """Create a Python file with print statements."""
    f = tmp_path / "chatty.py"
    f.write_text("x = 1\nprint(x)\nprint('hello')\n", encoding="utf-8")
    return f


def test_check_file_exists(valid_py: Path) -> None:
    """Existing file should pass."""
    result = check_file_exists(valid_py)
    assert result.passed is True


def test_check_file_exists_missing(tmp_path: Path) -> None:
    """Missing file should fail."""
    result = check_file_exists(tmp_path / "nope.py")
    assert result.passed is False


def test_check_no_syntax_errors_valid(valid_py: Path) -> None:
    """Valid Python should pass syntax check."""
    result = check_no_syntax_errors(valid_py)
    assert result.passed is True


def test_check_no_syntax_errors_bad(bad_syntax_py: Path) -> None:
    """Broken Python should fail syntax check."""
    result = check_no_syntax_errors(bad_syntax_py)
    assert result.passed is False
    assert "Syntax error" in result.message


def test_check_no_print_clean(valid_py: Path) -> None:
    """File without prints should pass."""
    result = check_no_print_statements(valid_py)
    assert result.passed is True


def test_check_no_print_violations(print_py: Path) -> None:
    """File with prints should fail with details."""
    result = check_no_print_statements(print_py)
    assert result.passed is False
    assert len(result.details) == 2


def test_check_file_size(valid_py: Path) -> None:
    """Small file should pass size check."""
    result = check_file_size(valid_py, max_lines=100)
    assert result.passed is True


def test_check_file_size_over_limit(tmp_path: Path) -> None:
    """Large file should fail size check."""
    f = tmp_path / "big.py"
    f.write_text("\n".join(f"x_{i} = {i}" for i in range(500)), encoding="utf-8")
    result = check_file_size(f, max_lines=100)
    assert result.passed is False


def test_run_pipeline() -> None:
    """Pipeline should aggregate gate results."""
    gates = [
        GateResult("a", True, 1.0),
        GateResult("b", False, 2.0, message="failed"),
        GateResult("c", True, 1.0),
    ]
    result = run_pipeline(gates)
    assert result.status == "FAIL"
    assert result.passed == 2
    assert result.failed == 1


def test_run_pipeline_all_pass() -> None:
    """All passing gates should produce PASS status."""
    gates = [GateResult("a", True, 1.0), GateResult("b", True, 1.0)]
    result = run_pipeline(gates)
    assert result.status == "PASS"


def test_run_default_gates(valid_py: Path) -> None:
    """Default gates on valid file should all pass."""
    result = run_default_gates(valid_py)
    assert result.status == "PASS"
    assert result.total_gates == 4


def test_format_pipeline_text() -> None:
    """Text output should contain status and gate names."""
    result = PipelineResult(
        total_gates=1, passed=1, failed=0,
        duration_ms=5.0, status="PASS",
        gates=[GateResult("test_gate", True, 5.0, "OK")],
    )
    text = format_pipeline_text(result)
    assert "PASS" in text
    assert "test_gate" in text
