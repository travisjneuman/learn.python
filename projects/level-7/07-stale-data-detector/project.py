"""Level 7 / Project 07 — Stale Data Detector.

Checks data freshness by comparing last-updated timestamps against
configurable TTL thresholds.  Reports stale sources so operators
can trigger refreshes before downstream consumers read outdated data.

Key concepts:
- Freshness = now - last_updated  vs  max_age_seconds
- Per-source TTL overrides
- Severity levels: fresh / warning / stale / critical
"""

from __future__ import annotations

import argparse
import json
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path


# -- Data model ----------------------------------------------------------

# WHY per-source thresholds? -- Different data sources have different
# acceptable staleness. Order data might be fine at 5 min old, but
# inventory data (which changes rapidly) should trigger alerts sooner.
# Three severity tiers let operators escalate response proportionally.
@dataclass
class FreshnessRule:
    """Per-source freshness thresholds (seconds)."""
    source: str
    warning: float = 300.0     # 5 min
    stale: float = 600.0       # 10 min
    critical: float = 1800.0   # 30 min


@dataclass
class SourceStatus:
    """Result of checking one source."""
    source: str
    last_updated: float
    age_seconds: float
    severity: str              # fresh | warning | stale | critical


# -- Core logic ----------------------------------------------------------

def default_rules() -> dict[str, FreshnessRule]:
    """Built-in defaults for common sources."""
    return {
        "api_orders": FreshnessRule("api_orders", 120, 300, 900),
        "api_inventory": FreshnessRule("api_inventory", 60, 180, 600),
    }


def merge_rules(
    defaults: dict[str, FreshnessRule],
    overrides: list[dict],
) -> dict[str, FreshnessRule]:
    """Merge user-supplied overrides into default rules."""
    merged = dict(defaults)
    for entry in overrides:
        src = entry["source"]
        merged[src] = FreshnessRule(
            source=src,
            warning=entry.get("warning", 300),
            stale=entry.get("stale", 600),
            critical=entry.get("critical", 1800),
        )
    return merged


def classify_age(age: float, rule: FreshnessRule) -> str:
    """Return severity label for a given age in seconds."""
    if age >= rule.critical:
        return "critical"
    if age >= rule.stale:
        return "stale"
    if age >= rule.warning:
        return "warning"
    return "fresh"


def check_sources(
    sources: list[dict],
    rules: dict[str, FreshnessRule],
    now: float | None = None,
) -> list[SourceStatus]:
    """Evaluate freshness for every source record."""
    now = now or time.time()
    fallback = FreshnessRule(source="__default__")
    results: list[SourceStatus] = []
    for src in sources:
        name = src["source"]
        last = src["last_updated"]
        age = now - last
        rule = rules.get(name, fallback)
        sev = classify_age(age, rule)
        results.append(SourceStatus(name, last, round(age, 2), sev))
        logging.info("source=%s age=%.1fs severity=%s", name, age, sev)
    return results


def summarise(statuses: list[SourceStatus]) -> dict:
    """Aggregate freshness check results."""
    counts: dict[str, int] = {"fresh": 0, "warning": 0, "stale": 0, "critical": 0}
    for s in statuses:
        counts[s.severity] += 1
    stale_names = [s.source for s in statuses if s.severity in ("stale", "critical")]
    return {
        "total_sources": len(statuses),
        "counts": counts,
        "stale_sources": stale_names,
        "all_fresh": len(stale_names) == 0,
    }


# -- Entry points --------------------------------------------------------

def run(input_path: Path, output_path: Path) -> dict:
    """Read config, check freshness, write summary."""
    config = json.loads(input_path.read_text(encoding="utf-8")) if input_path.exists() else {}

    rule_overrides = config.get("rules", [])
    sources = config.get("sources", [])
    now = config.get("now", time.time())

    rules = merge_rules(default_rules(), rule_overrides)
    statuses = check_sources(sources, rules, now=now)
    summary = summarise(statuses)
    summary["details"] = [
        {"source": s.source, "age": s.age_seconds, "severity": s.severity}
        for s in statuses
    ]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stale Data Detector")
    parser.add_argument("--input", default="data/sample_input.json")
    parser.add_argument("--output", default="data/output_summary.json")
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    args = parse_args()
    summary = run(Path(args.input), Path(args.output))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
