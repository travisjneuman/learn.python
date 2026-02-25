"""Level 3 project: Quality Gate Runner.

Simulates a CI/CD quality gate pipeline: runs a sequence of checks
(lint, test, build) and reports pass/fail with structured output.

Skills practiced: dataclasses, typing basics, logging, subprocess
simulation, pipeline patterns, JSON reporting.
"""

from __future__ import annotations

import argparse
import json
import logging
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class GateResult:
    """Result of running a single quality gate."""
    name: str
    passed: bool
    duration_ms: float
    message: str = ""
    details: list[str] = field(default_factory=list)


@dataclass
class PipelineResult:
    """Result of running the full pipeline."""
    total_gates: int
    passed: int
    failed: int
    duration_ms: float
    status: str  # "PASS", "FAIL"
    gates: list[GateResult] = field(default_factory=list)


# ── Gate check functions ──────────────────────────────────────
# Each returns a GateResult. In a real project these would call
# external tools; here we simulate with file checks.

def check_file_exists(path: Path) -> GateResult:
    """Gate: verify a required file exists."""
    start = time.perf_counter()
    exists = path.exists()
    elapsed = (time.perf_counter() - start) * 1000

    return GateResult(
        name=f"file_exists:{path.name}",
        passed=exists,
        duration_ms=round(elapsed, 2),
        message="File found" if exists else f"Missing: {path}",
    )


def check_no_syntax_errors(path: Path) -> GateResult:
    """Gate: check a Python file for syntax errors using compile()."""
    start = time.perf_counter()

    if not path.exists():
        elapsed = (time.perf_counter() - start) * 1000
        return GateResult(
            name=f"syntax:{path.name}",
            passed=False,
            duration_ms=round(elapsed, 2),
            message=f"File not found: {path}",
        )

    try:
        source = path.read_text(encoding="utf-8")
        compile(source, str(path), "exec")
        elapsed = (time.perf_counter() - start) * 1000
        return GateResult(
            name=f"syntax:{path.name}",
            passed=True,
            duration_ms=round(elapsed, 2),
            message="No syntax errors",
        )
    except SyntaxError as exc:
        elapsed = (time.perf_counter() - start) * 1000
        return GateResult(
            name=f"syntax:{path.name}",
            passed=False,
            duration_ms=round(elapsed, 2),
            message=f"Syntax error at line {exc.lineno}: {exc.msg}",
        )


def check_no_print_statements(path: Path) -> GateResult:
    """Gate: check that a Python file has no bare print() calls.

    This is a simplified lint check.
    """
    start = time.perf_counter()

    if not path.exists():
        elapsed = (time.perf_counter() - start) * 1000
        return GateResult(name=f"no_print:{path.name}", passed=False,
                          duration_ms=round(elapsed, 2), message="File not found")

    source = path.read_text(encoding="utf-8")
    violations: list[str] = []

    for line_num, line in enumerate(source.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("print(") and not stripped.startswith("#"):
            violations.append(f"Line {line_num}: {stripped[:60]}")

    elapsed = (time.perf_counter() - start) * 1000
    return GateResult(
        name=f"no_print:{path.name}",
        passed=len(violations) == 0,
        duration_ms=round(elapsed, 2),
        message=f"{len(violations)} print statement(s) found" if violations else "Clean",
        details=violations,
    )


def check_file_size(path: Path, max_lines: int = 300) -> GateResult:
    """Gate: check that a file doesn't exceed max lines."""
    start = time.perf_counter()

    if not path.exists():
        elapsed = (time.perf_counter() - start) * 1000
        return GateResult(name=f"size:{path.name}", passed=False,
                          duration_ms=round(elapsed, 2), message="File not found")

    lines = path.read_text(encoding="utf-8").splitlines()
    elapsed = (time.perf_counter() - start) * 1000
    passed = len(lines) <= max_lines

    return GateResult(
        name=f"size:{path.name}",
        passed=passed,
        duration_ms=round(elapsed, 2),
        message=f"{len(lines)} lines (limit: {max_lines})",
    )


def run_pipeline(gates: list[GateResult]) -> PipelineResult:
    """Aggregate gate results into a pipeline result."""
    passed = sum(1 for g in gates if g.passed)
    failed = sum(1 for g in gates if not g.passed)
    total_ms = sum(g.duration_ms for g in gates)

    return PipelineResult(
        total_gates=len(gates),
        passed=passed,
        failed=failed,
        duration_ms=round(total_ms, 2),
        status="PASS" if failed == 0 else "FAIL",
        gates=gates,
    )


def run_default_gates(target: Path) -> PipelineResult:
    """Run all default gates on a Python file."""
    gates: list[GateResult] = [
        check_file_exists(target),
        check_no_syntax_errors(target),
        check_no_print_statements(target),
        check_file_size(target),
    ]
    return run_pipeline(gates)


def format_pipeline_text(result: PipelineResult) -> str:
    """Format pipeline result as human-readable text."""
    lines = [f"Pipeline: {result.status} ({result.duration_ms:.1f}ms)", ""]

    for gate in result.gates:
        icon = "PASS" if gate.passed else "FAIL"
        lines.append(f"  [{icon}] {gate.name}: {gate.message}")
        for detail in gate.details:
            lines.append(f"         {detail}")

    lines.append(f"\n{result.passed}/{result.total_gates} gates passed")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    """Build CLI parser."""
    parser = argparse.ArgumentParser(description="Quality gate runner")
    parser.add_argument("file", help="Python file to check")
    parser.add_argument("--max-lines", type=int, default=300)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--log-level", default="INFO")
    return parser


def main() -> None:
    """Entry point."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    parser = build_parser()
    args = parser.parse_args()

    target = Path(args.file)
    result = run_default_gates(target)

    if args.json:
        print(json.dumps(asdict(result), indent=2))
    else:
        print(format_pipeline_text(result))


if __name__ == "__main__":
    main()
