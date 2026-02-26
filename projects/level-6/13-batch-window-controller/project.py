"""Level 6 / Project 13 — Batch Window Controller.

Manages processing windows (time ranges) for batch jobs.  Detects
overlapping windows, ensures no data is processed twice, and tracks
window completion status.

Key concepts:
- Time-range representation with start/end timestamps
- Overlap detection algorithm
- Window state machine: pending → running → completed / failed
- Gap detection: finding unprocessed time ranges
"""

from __future__ import annotations

import argparse
import json
import logging
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

# WHY batch windows? -- Without explicit time windows, batch jobs risk
# reprocessing the same data or missing gaps between runs. Each window
# claims a time range, and the status state machine (pending -> running
# -> completed/failed) ensures no two jobs process the same window.
WINDOWS_DDL = """\
CREATE TABLE IF NOT EXISTS batch_windows (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    start_ts   TEXT NOT NULL,
    end_ts     TEXT NOT NULL,
    status     TEXT NOT NULL DEFAULT 'pending'
                 CHECK(status IN ('pending','running','completed','failed')),
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
"""


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute(WINDOWS_DDL)
    conn.commit()


# ---------------------------------------------------------------------------
# Window management
# ---------------------------------------------------------------------------


@dataclass
class Window:
    start_ts: str
    end_ts: str
    status: str = "pending"
    id: int | None = None


def create_window(conn: sqlite3.Connection, start_ts: str, end_ts: str) -> int:
    """Create a new batch window. Returns its ID."""
    if end_ts <= start_ts:
        raise ValueError(f"end_ts must be after start_ts: {start_ts} >= {end_ts}")

    cur = conn.execute(
        "INSERT INTO batch_windows (start_ts, end_ts) VALUES (?, ?)",
        (start_ts, end_ts),
    )
    conn.commit()
    return cur.lastrowid


def update_status(conn: sqlite3.Connection, window_id: int, status: str) -> None:
    """Transition a window to a new status."""
    valid = {"pending", "running", "completed", "failed"}
    if status not in valid:
        raise ValueError(f"Invalid status: {status}")
    conn.execute(
        "UPDATE batch_windows SET status = ? WHERE id = ?", (status, window_id)
    )
    conn.commit()


def get_all_windows(conn: sqlite3.Connection) -> list[Window]:
    """Return all windows ordered by start timestamp."""
    rows = conn.execute(
        "SELECT id, start_ts, end_ts, status FROM batch_windows ORDER BY start_ts"
    ).fetchall()
    return [Window(id=r[0], start_ts=r[1], end_ts=r[2], status=r[3]) for r in rows]


# ---------------------------------------------------------------------------
# Overlap detection
# ---------------------------------------------------------------------------


def detect_overlaps(windows: list[Window]) -> list[tuple[Window, Window]]:
    """Find pairs of windows whose time ranges overlap.

    Two windows overlap when one starts before the other ends.
    We sort by start_ts and check consecutive pairs.
    """
    sorted_wins = sorted(windows, key=lambda w: w.start_ts)
    overlaps: list[tuple[Window, Window]] = []

    for i in range(len(sorted_wins) - 1):
        a = sorted_wins[i]
        b = sorted_wins[i + 1]
        # Overlap: b starts before a ends
        if b.start_ts < a.end_ts:
            overlaps.append((a, b))

    return overlaps


# ---------------------------------------------------------------------------
# Gap detection
# ---------------------------------------------------------------------------


def detect_gaps(windows: list[Window], range_start: str, range_end: str) -> list[dict]:
    """Find unprocessed time gaps within a given range.

    Returns a list of {"start": ..., "end": ...} for each gap.
    """
    sorted_wins = sorted(windows, key=lambda w: w.start_ts)
    gaps: list[dict] = []
    cursor = range_start

    for w in sorted_wins:
        if w.start_ts > cursor:
            gaps.append({"start": cursor, "end": w.start_ts})
        if w.end_ts > cursor:
            cursor = w.end_ts

    if cursor < range_end:
        gaps.append({"start": cursor, "end": range_end})

    return gaps


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


def run(input_path: Path, output_path: Path, db_path: str = ":memory:") -> dict:
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")

    config = json.loads(input_path.read_text(encoding="utf-8"))

    conn = sqlite3.connect(db_path)
    try:
        init_db(conn)

        for w in config.get("windows", []):
            wid = create_window(conn, w["start"], w["end"])
            if "status" in w:
                update_status(conn, wid, w["status"])

        all_wins = get_all_windows(conn)
        overlaps = detect_overlaps(all_wins)

        range_start = config.get("range_start", "")
        range_end = config.get("range_end", "")
        gaps = detect_gaps(all_wins, range_start, range_end) if range_start else []

    finally:
        conn.close()

    summary = {
        "windows_created": len(all_wins),
        "overlaps_found": len(overlaps),
        "overlaps": [
            {"a": f"{a.start_ts}–{a.end_ts}", "b": f"{b.start_ts}–{b.end_ts}"}
            for a, b in overlaps
        ],
        "gaps": gaps,
        "windows": [
            {"id": w.id, "start": w.start_ts, "end": w.end_ts, "status": w.status}
            for w in all_wins
        ],
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    logging.info("windows=%d overlaps=%d gaps=%d", len(all_wins), len(overlaps), len(gaps))
    return summary


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Batch Window Controller — overlap & gap detection"
    )
    parser.add_argument("--input", default="data/sample_input.json")
    parser.add_argument("--output", default="data/output_summary.json")
    parser.add_argument("--db", default=":memory:")
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    args = parse_args()
    summary = run(Path(args.input), Path(args.output), args.db)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
