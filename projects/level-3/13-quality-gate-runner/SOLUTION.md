# Quality Gate Runner — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) before reading the solution.

---

## Complete Solution

```python
"""Level 3 project: Quality Gate Runner."""

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
    """Result of running the full pipeline.

    WHY: aggregating individual gate results into a pipeline-level
    pass/fail mirrors how real CI/CD works — the build is green
    only if ALL gates pass.
    """
    total_gates: int
    passed: int
    failed: int
    duration_ms: float
    status: str  # "PASS", "FAIL"
    gates: list[GateResult] = field(default_factory=list)


# -- Gate check functions -------------------------------------------------
# WHY: each gate is a standalone function that returns a GateResult.
# This makes gates composable — you can add, remove, or reorder
# them without changing any other code.

def check_file_exists(path: Path) -> GateResult:
    """Gate: verify a required file exists."""
    # WHY: perf_counter() is the right clock for measuring elapsed
    # time. time.time() can jump backwards (NTP sync, daylight saving).
    # perf_counter() is monotonic and high-resolution.
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
    """Gate: check a Python file for syntax errors using compile().

    WHY: compile() parses the source into bytecode without executing
    it. This catches syntax errors (missing colons, bad indentation)
    without running any side effects. It is the same thing Python
    does when you import a module.
    """
    start = time.perf_counter()

    if not path.exists():
        elapsed = (time.perf_counter() - start) * 1000
        return GateResult(
            name=f"syntax:{path.name}", passed=False,
            duration_ms=round(elapsed, 2),
            message=f"File not found: {path}",
        )

    try:
        source = path.read_text(encoding="utf-8")
        # WHY: "exec" mode compiles the source as a module (statements).
        # "eval" mode would only accept a single expression.
        compile(source, str(path), "exec")
        elapsed = (time.perf_counter() - start) * 1000
        return GateResult(
            name=f"syntax:{path.name}", passed=True,
            duration_ms=round(elapsed, 2),
            message="No syntax errors",
        )
    except SyntaxError as exc:
        elapsed = (time.perf_counter() - start) * 1000
        return GateResult(
            name=f"syntax:{path.name}", passed=False,
            duration_ms=round(elapsed, 2),
            message=f"Syntax error at line {exc.lineno}: {exc.msg}",
        )


def check_no_print_statements(path: Path) -> GateResult:
    """Gate: check that a Python file has no bare print() calls.

    WHY: in production code, logging should replace print().
    This simplified lint check flags files that use print()
    for output, which is a common beginner habit to outgrow.
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
        # WHY: check startswith("print(") to find calls, but skip
        # comments. This is a heuristic — it would also flag
        # `printer(x)` if it started with "print(". A real linter
        # uses AST analysis.
        if stripped.startswith("print(") and not stripped.startswith("#"):
            violations.append(f"Line {line_num}: {stripped[:60]}")

    elapsed = (time.perf_counter() - start) * 1000
    return GateResult(
        name=f"no_print:{path.name}",
        passed=len(violations) == 0,
        duration_ms=round(elapsed, 2),
        message=(f"{len(violations)} print statement(s) found"
                 if violations else "Clean"),
        details=violations,
    )


def check_file_size(path: Path, max_lines: int = 300) -> GateResult:
    """Gate: check that a file does not exceed max lines.

    WHY: long files are hard to navigate and usually indicate
    that the code should be split into multiple modules.
    """
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
    """Aggregate gate results into a pipeline result.

    WHY: the pipeline does not run gates — it only aggregates.
    This separation means you can run gates in any order, skip
    some, or add new ones without changing the aggregation logic.
    """
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
    parser = argparse.ArgumentParser(description="Quality gate runner")
    parser.add_argument("file", help="Python file to check")
    parser.add_argument("--max-lines", type=int, default=300)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--log-level", default="INFO")
    return parser


def main() -> None:
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
```

## Design Decisions

| Decision | Why |
|----------|-----|
| `time.perf_counter()` instead of `time.time()` | `perf_counter()` is monotonic (never goes backwards) and high-resolution. `time.time()` can jump during NTP corrections, giving negative durations. |
| `compile()` for syntax checking | Parses source into bytecode WITHOUT executing it. Safe to run on untrusted code because no side effects occur. Real linters (ruff, pylint) use similar AST-based approaches. |
| Each gate handles missing files independently | A missing file should not prevent other gates from running. Each gate returns a clear "File not found" message instead of raising an exception that stops the pipeline. |
| `run_pipeline` only aggregates, never runs | Separation of execution and aggregation. You can run gates in parallel, cache results, or skip gates without changing the aggregation logic. |
| `details` list on GateResult | For gates that find multiple violations (like print statements), the details list provides line-by-line information without cluttering the summary message. |

## Alternative Approaches

### Using `ast` module for the print-statement check

```python
import ast

def check_no_print_ast(path: Path) -> GateResult:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    violations = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name) and func.id == "print":
                violations.append(f"Line {node.lineno}")
    # ... return GateResult
```

**Trade-off:** The AST approach correctly identifies `print()` calls even when indented or in unusual positions, and would NOT falsely flag `printer()`. But it requires understanding `ast.walk` and AST node types, which is more advanced. The text-based approach is simpler and sufficient for this learning level.

## Common Pitfalls

1. **`compile()` does not catch runtime errors** — `compile("x = 1/0", ...)` succeeds because division-by-zero is a runtime error, not a syntax error. This gate only catches syntax issues like missing colons, bad indentation, or unmatched parentheses.

2. **The print check is a heuristic, not a guarantee** — `stripped.startswith("print(")` misses `print (x)` (space before paren) and falsely flags `print_report()`. For real linting, use ruff or pylint which parse the AST.

3. **Reading the file multiple times** — Each gate reads the file independently. For large files, this is wasteful. An optimisation would read once and pass the content to all gates, but the current approach prioritises simplicity and gate independence.
