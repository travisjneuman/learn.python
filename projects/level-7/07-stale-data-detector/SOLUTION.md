# Solution: Level 7 / Project 07 - Stale Data Detector

> **STOP — Try it yourself first!**
>
> You learn by building, not by reading answers. Spend at least 30 minutes
> attempting this project before looking here.
>
> - Re-read the [README](./README.md) for requirements
> 
---

## Complete solution

```python
"""Level 7 / Project 07 — Stale Data Detector.

Checks data freshness by comparing last-updated timestamps against
configurable TTL thresholds.  Reports stale sources so operators
can trigger refreshes before downstream consumers read outdated data.
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
# acceptable staleness.  Order data might be fine at 5 min old, but
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
    """Merge user-supplied overrides into default rules.

    WHY merge instead of replace? -- Defaults provide sensible baselines
    for known sources.  Overrides let operators tune thresholds without
    needing to redeclare every rule.  New sources get their own rules
    without affecting existing ones.
    """
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
    """Return severity label for a given age in seconds.

    WHY check from highest severity down? -- If age exceeds the critical
    threshold, it also exceeds warning and stale.  Checking critical first
    ensures we return the most severe applicable label.
    """
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
    # WHY a fallback rule? -- Sources not listed in the rules dict still
    # need to be checked.  The fallback provides generous defaults so
    # unknown sources are not silently classified as "fresh."
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
        # WHY all_fresh flag? -- Single boolean makes it trivial for
        # downstream automation to decide "do I need to trigger a refresh?"
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
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Per-source `FreshnessRule` with three thresholds | Different sources have different acceptable staleness; graduated severity enables proportional response | Single global threshold -- too coarse; inventory and orders have very different freshness needs |
| Defaults merged with overrides | Sensible baselines without requiring explicit config for every source | Override-only (no defaults) -- forces operators to declare every rule, even for common sources |
| `classify_age` checks from critical down | Ensures the most severe applicable label is returned first | Check from fresh up -- would need `elif` chains and is more error-prone |
| `now` injectable in `check_sources` | Makes tests deterministic; no dependency on real clock | Always use `time.time()` -- simpler but tests become flaky |

## Alternative approaches

### Approach B: Continuous freshness score (0.0-1.0)

```python
def freshness_score(age: float, max_age: float) -> float:
    """1.0 = perfectly fresh, 0.0 = critically stale."""
    return max(0.0, 1.0 - (age / max_age))
```

**Trade-off:** A continuous score gives more nuance than discrete buckets (fresh/warning/stale/critical). Useful for dashboards and weighted decisions. But discrete categories are easier for operators to act on -- "stale" is clearer than "0.37 freshness."

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| `last_updated` is in the future (ahead of `now`) | Negative age; `classify_age` returns "fresh" even though the timestamp is suspicious | Clamp negative ages to zero and log a warning |
| Source record is missing the `"source"` key | `KeyError` crashes the check loop | Validate required keys before processing, or use `.get()` with a fallback |
| All sources share the same rule but have different data volumes | Low-volume sources may appear fresh simply because they rarely change | Track both age AND expected update frequency to distinguish "unchanged" from "broken" |
