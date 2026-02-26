# Backup Rotation Tool — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) and [walkthrough](./WALKTHROUGH.md) before reading the solution.

---

## Complete Solution

```python
"""Level 4 / Project 06 — Backup Rotation Tool.

Implements backup retention policies: keep N daily, M weekly, P monthly
backups. Older backups beyond the retention window are identified for
deletion. Backups are identified by filename timestamps.
"""

from __future__ import annotations

import argparse
import json
import logging
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ---------- logging ----------

def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

# ---------- backup classification ----------

# WHY: Parse dates from filenames rather than filesystem timestamps (mtime)
# because mtime is unreliable across OS copies, restores, and backups.
# Embedding the date in the filename makes backup age deterministic.
TIMESTAMP_PATTERN = re.compile(r"(\d{4}-\d{2}-\d{2})")


def parse_backup_date(filename: str) -> datetime | None:
    """Extract a date from a backup filename. Returns None if no date found."""
    match = TIMESTAMP_PATTERN.search(filename)
    if not match:
        return None
    try:
        return datetime.strptime(match.group(1), "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def classify_backups(
    files: list[str],
    now: datetime,
    daily_keep: int = 7,
    weekly_keep: int = 4,
    monthly_keep: int = 6,
) -> dict:
    """Classify backups into keep/delete buckets based on retention policy.

    Policy:
    - Daily: keep the most recent `daily_keep` backups
    - Weekly: keep one backup per week for the last `weekly_keep` weeks
    - Monthly: keep one backup per month for the last `monthly_keep` months
    - Everything else: mark for deletion
    """
    dated: list[tuple[str, datetime]] = []
    unparseable: list[str] = []

    for f in files:
        dt = parse_backup_date(f)
        if dt:
            dated.append((f, dt))
        else:
            unparseable.append(f)

    # WHY: Sort newest first because retention policies keep the N most
    # recent entries. Processing newest-first lets us fill daily/weekly/monthly
    # buckets greedily, preferring newer backups when there is a tie.
    dated.sort(key=lambda x: x[1], reverse=True)

    keep: list[dict] = []
    delete: list[dict] = []
    # WHY: A set tracks which filenames are already kept, so we never
    # count the same backup in two retention categories.
    kept_set: set[str] = set()

    # Daily retention — keep the N most recent within the daily window
    daily_cutoff = now - timedelta(days=daily_keep)
    daily_count = 0
    for fname, dt in dated:
        if dt >= daily_cutoff and daily_count < daily_keep:
            keep.append({"file": fname, "reason": "daily", "date": dt.isoformat()})
            kept_set.add(fname)
            daily_count += 1

    # Weekly retention — one per ISO week within the weekly window
    weekly_cutoff = now - timedelta(weeks=weekly_keep)
    seen_weeks: set[str] = set()
    for fname, dt in dated:
        if fname in kept_set:
            continue
        # WHY: Use strftime %Y-W%W as a week key so each calendar week
        # gets exactly one representative backup.
        week_key = dt.strftime("%Y-W%W")
        if dt >= weekly_cutoff and week_key not in seen_weeks:
            keep.append({"file": fname, "reason": "weekly", "date": dt.isoformat()})
            kept_set.add(fname)
            seen_weeks.add(week_key)

    # Monthly retention — one per month within the monthly window
    # WHY: Multiply by 31 (not 30) to be generous with month boundaries.
    monthly_cutoff = now - timedelta(days=monthly_keep * 31)
    seen_months: set[str] = set()
    for fname, dt in dated:
        if fname in kept_set:
            continue
        month_key = dt.strftime("%Y-%m")
        if dt >= monthly_cutoff and month_key not in seen_months:
            keep.append({"file": fname, "reason": "monthly", "date": dt.isoformat()})
            kept_set.add(fname)
            seen_months.add(month_key)

    # Everything not kept is marked for deletion
    for fname, dt in dated:
        if fname not in kept_set:
            delete.append({"file": fname, "date": dt.isoformat()})

    return {
        "keep": keep,
        "delete": delete,
        "unparseable": unparseable,
        "summary": {
            "total": len(files),
            "keeping": len(keep),
            "deleting": len(delete),
            "unparseable": len(unparseable),
        },
    }

# ---------- runner ----------


def run(backup_dir: Path, output_path: Path, now: datetime | None = None,
        daily: int = 7, weekly: int = 4, monthly: int = 6) -> dict:
    """Scan a backup directory and produce a rotation report."""
    if not backup_dir.is_dir():
        raise NotADirectoryError(f"Not a directory: {backup_dir}")

    files = sorted(f.name for f in backup_dir.iterdir() if f.is_file())
    # WHY: Accept `now` as a parameter for testability. Tests can inject
    # a fixed datetime so results are deterministic.
    now = now or datetime.now(timezone.utc)
    report = classify_backups(files, now, daily, weekly, monthly)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    logging.info(
        "Rotation plan: keeping %d, deleting %d",
        report["summary"]["keeping"], report["summary"]["deleting"],
    )
    return report

# ---------- CLI ----------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Backup rotation planner")
    parser.add_argument("--backup-dir", default="data/backups")
    parser.add_argument("--output", default="data/rotation_report.json")
    parser.add_argument("--daily", type=int, default=7, help="Daily backups to keep")
    parser.add_argument("--weekly", type=int, default=4, help="Weekly backups to keep")
    parser.add_argument("--monthly", type=int, default=6, help="Monthly backups to keep")
    return parser.parse_args()


def main() -> None:
    configure_logging()
    args = parse_args()
    report = run(
        Path(args.backup_dir), Path(args.output),
        daily=args.daily, weekly=args.weekly, monthly=args.monthly,
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Parse dates from filenames, not filesystem mtime | Filesystem timestamps change when files are copied, restored, or synced. Filename-embedded dates are deterministic and portable. |
| `classify_backups` takes `now` as a parameter | Dependency injection for testability. Tests can pass a fixed datetime to get reproducible results regardless of when they run. |
| Use a `kept_set` to track already-kept files | Prevents double-counting. A backup kept for the "daily" reason should not also be counted as "weekly," which would waste a weekly slot. |
| Plan-only by default (no actual deletion) | Destructive operations should require explicit confirmation. The `--execute` flag (in the Alter extension) is an intentional friction point. |

## Alternative Approaches

### Using file modification time instead of filename parsing

```python
from datetime import datetime, timezone

def get_file_date(path: Path) -> datetime:
    stat = path.stat()
    return datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)
```

**Trade-off:** Using mtime requires no filename convention (any backup file works), but modification times are unreliable when files are copied between systems, restored from archives, or transferred via certain protocols. Filename-based dating is more robust for backup management.

### Using a single-pass approach instead of three loops

```python
def classify_single_pass(dated, now, daily, weekly, monthly):
    keep = []
    for fname, dt in dated:  # sorted newest-first
        age_days = (now - dt).days
        if age_days <= daily:
            keep.append((fname, "daily"))
        elif age_days <= weekly * 7:
            keep.append((fname, "weekly"))
        elif age_days <= monthly * 31:
            keep.append((fname, "monthly"))
    return keep
```

**Trade-off:** A single pass is slightly more efficient but does not enforce the "one per week" and "one per month" constraints. The three-loop approach explicitly limits each retention tier, which is the correct behavior for real backup rotation.

## Common Pitfalls

1. **Using `timedelta(months=N)` — it does not exist** — Python's `timedelta` supports days, weeks, hours, minutes, and seconds, but not months (because months have variable lengths). The solution approximates with `days=N*31`.
2. **Not handling unparseable filenames** — Not every file in a backup directory has a date in its name (think `README.txt` or `.DS_Store`). These must be reported separately rather than crashing the classifier.
3. **Setting all retention values to 0** — This would mark every backup for deletion, which is dangerous. Production tools should enforce a `--min-keep` safety net that refuses to delete below a threshold.
