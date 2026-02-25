"""Level 4 / Project 05 — Path Safe File Mover.

Moves files between directories with collision handling and rollback
capability. If a destination file already exists, appends a counter
(report_1.csv, report_2.csv). Logs every operation for audit.
"""

from __future__ import annotations

import argparse
import json
import logging
import shutil
from datetime import datetime, timezone
from pathlib import Path

# ---------- logging ----------

def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

# ---------- safe-move logic ----------


def resolve_collision(dest: Path) -> Path:
    """If *dest* already exists, find a non-colliding name.

    Strategy: append _1, _2, ... before the file extension.
    Example: report.csv -> report_1.csv -> report_2.csv
    """
    if not dest.exists():
        return dest

    stem = dest.stem
    suffix = dest.suffix
    parent = dest.parent
    counter = 1

    while True:
        candidate = parent / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def plan_moves(source_dir: Path, dest_dir: Path) -> list[dict]:
    """Build a move plan: for each file in source_dir, compute the target path.

    The plan is a list of dicts with keys: source, destination, status.
    This separation lets us do dry-runs and rollbacks.
    """
    if not source_dir.is_dir():
        raise NotADirectoryError(f"Source is not a directory: {source_dir}")

    dest_dir.mkdir(parents=True, exist_ok=True)
    plan: list[dict] = []

    for file_path in sorted(source_dir.iterdir()):
        if not file_path.is_file():
            continue  # skip subdirectories

        target = resolve_collision(dest_dir / file_path.name)
        plan.append({
            "source": str(file_path),
            "destination": str(target),
            "status": "planned",
        })

    return plan


def execute_moves(plan: list[dict], dry_run: bool = False) -> list[dict]:
    """Execute a move plan. If dry_run is True, just mark as 'dry_run'.

    Returns the updated plan with statuses: 'moved', 'failed', or 'dry_run'.
    Keeps a rollback stack so we can undo on failure.
    """
    completed: list[dict] = []

    for entry in plan:
        src = Path(entry["source"])
        dst = Path(entry["destination"])

        if dry_run:
            entry["status"] = "dry_run"
            logging.info("[DRY RUN] %s -> %s", src, dst)
            continue

        try:
            shutil.move(str(src), str(dst))
            entry["status"] = "moved"
            entry["timestamp"] = datetime.now(timezone.utc).isoformat()
            completed.append(entry)
            logging.info("Moved: %s -> %s", src, dst)
        except OSError as exc:
            entry["status"] = "failed"
            entry["error"] = str(exc)
            logging.error("Failed to move %s: %s", src, exc)
            # Rollback all previously completed moves
            _rollback(completed)
            break

    return plan


def _rollback(completed: list[dict]) -> None:
    """Undo completed moves by moving files back to their source paths."""
    for entry in reversed(completed):
        try:
            shutil.move(entry["destination"], entry["source"])
            entry["status"] = "rolled_back"
            logging.warning("Rolled back: %s -> %s", entry["destination"], entry["source"])
        except OSError as exc:
            logging.error("Rollback failed for %s: %s", entry["destination"], exc)

# ---------- runner ----------


def run(source_dir: Path, dest_dir: Path, output_path: Path, dry_run: bool = False) -> dict:
    """Plan moves, execute (or dry-run), write log."""
    plan = plan_moves(source_dir, dest_dir)
    executed = execute_moves(plan, dry_run=dry_run)

    report = {
        "source_dir": str(source_dir),
        "dest_dir": str(dest_dir),
        "dry_run": dry_run,
        "total_files": len(executed),
        "moved": sum(1 for e in executed if e["status"] == "moved"),
        "failed": sum(1 for e in executed if e["status"] == "failed"),
        "operations": executed,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    logging.info("Move complete — %d moved, %d failed", report["moved"], report["failed"])
    return report

# ---------- CLI ----------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Safely move files with collision handling")
    parser.add_argument("--source", default="data/source", help="Source directory")
    parser.add_argument("--dest", default="data/dest", help="Destination directory")
    parser.add_argument("--output", default="data/move_log.json", help="Move log output")
    parser.add_argument("--dry-run", action="store_true", help="Plan but do not execute")
    return parser.parse_args()


def main() -> None:
    configure_logging()
    args = parse_args()
    report = run(Path(args.source), Path(args.dest), Path(args.output), dry_run=args.dry_run)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
