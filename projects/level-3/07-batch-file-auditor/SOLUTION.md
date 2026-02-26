# Batch File Auditor — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) before reading the solution.

---

## Complete Solution

```python
"""Level 3 project: Batch File Auditor."""

from __future__ import annotations

import argparse
import json
import logging
import os
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class FileInfo:
    """Metadata about a single file."""
    name: str
    path: str
    size_bytes: int
    extension: str
    is_empty: bool


@dataclass
class AuditIssue:
    """A single issue found during audit.

    WHY: structured issues with severity and check name let you
    filter ("show only warnings") and aggregate ("3 naming issues,
    1 empty file") programmatically.
    """
    file: str
    severity: str  # "error", "warning", "info"
    check: str
    message: str


@dataclass
class AuditReport:
    """Full audit report for a directory."""
    directory: str
    total_files: int
    total_size: int
    files: list[FileInfo] = field(default_factory=list)
    issues: list[AuditIssue] = field(default_factory=list)
    summary: dict = field(default_factory=dict)


def scan_directory(root: Path, pattern: str = "*") -> list[FileInfo]:
    """Scan a directory and collect FileInfo for each matching file.

    WHY: raises NotADirectoryError (a built-in) instead of returning
    empty results. Silent failure on bad input wastes debugging time.
    """
    if not root.is_dir():
        raise NotADirectoryError(f"Not a directory: {root}")

    files: list[FileInfo] = []
    for path in sorted(root.glob(pattern)):
        if not path.is_file():
            continue
        # WHY: path.stat() returns OS-level metadata (size, timestamps,
        # permissions) in a single system call — much faster than
        # reading the file content to check if it is empty.
        stat = path.stat()
        files.append(FileInfo(
            name=path.name,
            path=str(path),
            size_bytes=stat.st_size,
            extension=path.suffix.lower(),
            is_empty=stat.st_size == 0,
        ))

    logger.info("Scanned %d files in %s", len(files), root)
    return files


# WHY: each check function takes a list of FileInfo and returns
# a list of AuditIssues. This composable design means you can add
# or remove checks without touching any other code.

def check_empty_files(files: list[FileInfo]) -> list[AuditIssue]:
    """Flag files that are 0 bytes."""
    return [
        AuditIssue(
            file=f.name, severity="warning",
            check="empty_file",
            message=f"File is empty (0 bytes)",
        )
        for f in files if f.is_empty
    ]


def check_large_files(files: list[FileInfo],
                       max_bytes: int = 1_000_000) -> list[AuditIssue]:
    """Flag files larger than max_bytes (default 1 MB).

    WHY: the threshold is a parameter, not a constant. Different
    projects have different size limits. Making it configurable
    costs nothing and adds real flexibility.
    """
    return [
        AuditIssue(
            file=f.name, severity="warning",
            check="large_file",
            message=f"File is {f.size_bytes:,} bytes (limit: {max_bytes:,})",
        )
        for f in files if f.size_bytes > max_bytes
    ]


def check_naming_convention(
    files: list[FileInfo],
    allowed_chars: str = "abcdefghijklmnopqrstuvwxyz0123456789_-.",
) -> list[AuditIssue]:
    """Flag files with names containing unexpected characters.

    WHY: filenames with spaces, unicode, or special characters cause
    problems in shell scripts, URLs, and cross-platform sharing.
    """
    issues: list[AuditIssue] = []
    for f in files:
        # WHY: set difference finds characters in the filename that
        # are NOT in the allowed set. Efficient O(n) check.
        bad_chars = set(f.name.lower()) - set(allowed_chars)
        if bad_chars:
            issues.append(AuditIssue(
                file=f.name, severity="info",
                check="naming",
                message=f"Unexpected characters in filename: {bad_chars}",
            ))
    return issues


def check_no_extension(files: list[FileInfo]) -> list[AuditIssue]:
    """Flag files without an extension."""
    return [
        AuditIssue(
            file=f.name, severity="info",
            check="no_extension",
            message="File has no extension",
        )
        for f in files if not f.extension
    ]


def run_audit(
    root: Path,
    pattern: str = "*",
    max_file_size: int = 1_000_000,
) -> AuditReport:
    """Run a full audit on a directory.

    WHY: this orchestrator calls scan_directory once and passes
    the result to multiple check functions. Each check is independent
    and composable — you can add new checks without modifying existing ones.
    """
    files = scan_directory(root, pattern)

    issues: list[AuditIssue] = []
    issues.extend(check_empty_files(files))
    issues.extend(check_large_files(files, max_file_size))
    issues.extend(check_naming_convention(files))
    issues.extend(check_no_extension(files))

    # WHY: summary by severity tells you at a glance whether the
    # audit found anything serious or just informational notes.
    severity_counts: dict[str, int] = {}
    for issue in issues:
        severity_counts[issue.severity] = severity_counts.get(issue.severity, 0) + 1

    extension_counts: dict[str, int] = {}
    for f in files:
        ext = f.extension or "(none)"
        extension_counts[ext] = extension_counts.get(ext, 0) + 1

    return AuditReport(
        directory=str(root),
        total_files=len(files),
        total_size=sum(f.size_bytes for f in files),
        files=files,
        issues=issues,
        summary={
            "by_severity": severity_counts,
            "by_extension": extension_counts,
        },
    )


def format_report_text(report: AuditReport) -> str:
    """Format an audit report as human-readable text."""
    lines = [
        f"Audit: {report.directory}",
        f"Files: {report.total_files}, Total size: {report.total_size:,} bytes",
        "",
    ]

    if report.issues:
        lines.append(f"Issues ({len(report.issues)}):")
        for issue in report.issues:
            # WHY: fixed-width severity formatting aligns the output
            # for easy scanning.
            lines.append(f"  [{issue.severity.upper():7s}] {issue.file}: {issue.message}")
    else:
        lines.append("No issues found.")

    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Batch file auditor")

    sub = parser.add_subparsers(dest="command")

    audit = sub.add_parser("audit", help="Audit a directory")
    audit.add_argument("directory", help="Directory to audit")
    audit.add_argument("--pattern", default="*", help="Glob pattern")
    audit.add_argument("--max-size", type=int, default=1_000_000)
    audit.add_argument("--json", action="store_true")

    scan = sub.add_parser("scan", help="List files in a directory")
    scan.add_argument("directory", help="Directory to scan")
    scan.add_argument("--pattern", default="*")

    parser.add_argument("--log-level", default="INFO")
    return parser


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "audit":
        report = run_audit(Path(args.directory), args.pattern, args.max_size)
        if args.json:
            print(json.dumps(asdict(report), indent=2))
        else:
            print(format_report_text(report))

    elif args.command == "scan":
        files = scan_directory(Path(args.directory), args.pattern)
        for f in files:
            print(f"{f.size_bytes:>10,} {f.name}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Composable check functions (`check_empty_files`, `check_large_files`, etc.) | Each check is independently testable and can be enabled/disabled without modifying others. This is the "plugin" pattern. |
| `Path.stat()` for metadata instead of reading file content | `stat()` is a single OS call that returns size, timestamps, and permissions. Reading the entire file just to check emptiness would be wasteful for large files. |
| `Path.glob()` (non-recursive) by default | Recursive scanning can be slow on large directory trees. The user opts in to recursion explicitly. |
| Set difference for naming convention check | `set(filename) - set(allowed)` is concise and runs in O(n) time. The alternative — looping through each character with `if c not in allowed` — is equivalent but less Pythonic. |
| Severity levels ("error", "warning", "info") | Matches the logging convention developers already know. Makes it natural to filter by severity. |

## Alternative Approaches

### Using `os.walk` for recursive scanning

```python
import os

def scan_recursive(root: str) -> list[FileInfo]:
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        for fname in filenames:
            full = os.path.join(dirpath, fname)
            stat = os.stat(full)
            files.append(FileInfo(
                name=fname, path=full,
                size_bytes=stat.st_size,
                extension=os.path.splitext(fname)[1].lower(),
                is_empty=stat.st_size == 0,
            ))
    return files
```

**Trade-off:** `os.walk` is the classic approach and gives you directory names too (useful for detecting nested packages). `Path.rglob()` is more modern and integrates with pathlib's API, but both work well.

## Common Pitfalls

1. **Not handling permission errors** — Directories with restricted permissions raise `PermissionError` when you call `stat()` or `read_text()`. Wrap file operations in try/except and log a warning instead of crashing the entire audit.

2. **Glob pattern matching nothing** — `root.glob("*.xyz")` returns an empty iterator, not an error. The audit will report "0 files, no issues" which looks like success. Add a warning when the scan finds zero files.

3. **Binary files breaking text analysis** — If you later add checks that read file content (like encoding detection), binary files (.pyc, .jpg) will raise `UnicodeDecodeError`. Always catch encoding errors when reading files, or filter to known text extensions first.
