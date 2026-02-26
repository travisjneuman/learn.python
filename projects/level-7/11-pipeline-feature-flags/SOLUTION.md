# Solution: Level 7 / Project 11 - Pipeline Feature Flags

> **STOP — Try it yourself first!**
>
> You learn by building, not by reading answers. Spend at least 30 minutes
> attempting this project before looking here.
>
> - Re-read the [README](./README.md) for requirements
> - Try the [WALKTHROUGH](./WALKTHROUGH.md) for guided hints without spoilers

---

## Complete solution

```python
"""Level 7 / Project 11 — Pipeline Feature Flags.

Runtime toggles that let operators enable or disable pipeline stages
without redeploying.  Flags are stored in a simple JSON config and
evaluated at each stage boundary.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path


# -- Data model ----------------------------------------------------------

# WHY feature flags in a data pipeline? -- Flags let operators toggle
# pipeline stages at runtime without redeploying code.  The rollout_pct
# field enables gradual rollouts (e.g. 10% of traffic uses the new stage)
# and the requires list enforces dependency chains (flag A needs flag B).
@dataclass
class Flag:
    """One feature flag."""
    name: str
    enabled: bool = True
    rollout_pct: float = 100.0   # 0-100
    requires: list[str] = field(default_factory=list)


# -- Core logic ----------------------------------------------------------

class FlagManager:
    """Evaluate and manage feature flags."""

    def __init__(self, flags: list[Flag] | None = None) -> None:
        self._flags: dict[str, Flag] = {}
        self._audit: list[dict] = []
        for f in (flags or []):
            self._flags[f.name] = f

    def register(self, flag: Flag) -> None:
        self._flags[flag.name] = flag

    def is_enabled(self, name: str, context_key: str = "") -> bool:
        """Check if a flag is active.  Respects dependencies and rollout %.

        WHY three-stage evaluation (enabled -> dependencies -> rollout)?
        Each check is progressively more expensive.  Short-circuiting on
        the cheapest check first (boolean enabled) avoids unnecessary
        dependency traversal and hash computation.
        """
        flag = self._flags.get(name)
        if flag is None:
            self._record(name, False, "unknown flag")
            return False

        if not flag.enabled:
            self._record(name, False, "disabled")
            return False

        # Check dependencies first
        for dep in flag.requires:
            if not self.is_enabled(dep, context_key):
                self._record(name, False, f"dependency {dep} not met")
                return False

        # WHY deterministic hash for rollout? -- Using MD5 of flag name +
        # context key ensures the same user always gets the same result
        # (no random flipping between requests).  The hash maps to a 0-99
        # bucket that is compared against rollout_pct.
        if flag.rollout_pct < 100.0:
            h = int(hashlib.md5(f"{name}:{context_key}".encode()).hexdigest(), 16)
            bucket = h % 100
            if bucket >= flag.rollout_pct:
                self._record(name, False, f"rollout {flag.rollout_pct}%")
                return False

        self._record(name, True, "ok")
        return True

    def evaluate_all(self, context_key: str = "") -> dict[str, bool]:
        """Evaluate every registered flag."""
        return {name: self.is_enabled(name, context_key) for name in self._flags}

    def _record(self, name: str, result: bool, reason: str) -> None:
        self._audit.append({"flag": name, "result": result, "reason": reason})
        logging.info("flag=%s result=%s reason=%s", name, result, reason)

    @property
    def audit_log(self) -> list[dict]:
        return list(self._audit)

    def stats(self) -> dict:
        total = len(self._flags)
        enabled = sum(1 for f in self._flags.values() if f.enabled)
        return {"total": total, "enabled": enabled, "disabled": total - enabled}


def flags_from_config(raw: list[dict]) -> list[Flag]:
    return [
        Flag(
            name=d["name"],
            enabled=d.get("enabled", True),
            rollout_pct=d.get("rollout_pct", 100.0),
            requires=d.get("requires", []),
        )
        for d in raw
    ]


# -- Entry points --------------------------------------------------------

def run(input_path: Path, output_path: Path) -> dict:
    config = json.loads(input_path.read_text(encoding="utf-8")) if input_path.exists() else {}

    flags = flags_from_config(config.get("flags", []))
    context_key = config.get("context_key", "default")

    mgr = FlagManager(flags)
    evaluations = mgr.evaluate_all(context_key)

    summary = {
        "evaluations": evaluations,
        "stats": mgr.stats(),
        "audit_entries": len(mgr.audit_log),
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Pipeline Feature Flags")
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
| Deterministic hash for rollout percentage | Same context_key always gets the same flag result; no random flipping between evaluations | `random.random() < pct/100` -- simpler but non-deterministic; same user could get different results on each call |
| Recursive dependency resolution | Naturally follows dependency chains (A requires B, B requires C) | Topological sort upfront -- more efficient for many flags but adds complexity |
| Three-stage evaluation (enabled -> deps -> rollout) | Short-circuits on cheapest check first; avoids hash computation when flag is simply disabled | Single evaluation function -- harder to debug which stage rejected the flag |
| Audit log records every evaluation | Essential for debugging "why was this flag off for user X?"; compliance requirement in regulated environments | No audit -- simpler but impossible to troubleshoot flag behavior in production |

## Alternative approaches

### Approach B: Percentage rollout with sticky assignments

```python
class StickyFlagManager(FlagManager):
    def __init__(self, flags, storage_path: Path):
        super().__init__(flags)
        self._assignments: dict[str, dict[str, bool]] = {}
        self._storage = storage_path

    def is_enabled(self, name: str, context_key: str = "") -> bool:
        cache_key = f"{name}:{context_key}"
        if cache_key in self._assignments:
            return self._assignments[cache_key]
        result = super().is_enabled(name, context_key)
        self._assignments[cache_key] = result
        return result
```

**Trade-off:** Sticky assignments persist flag decisions across restarts, ensuring users never flip between variants. But they require storage and complicate flag updates (changing rollout_pct does not affect already-assigned users).

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Circular dependency (flag A requires B, B requires A) | `is_enabled` recurses infinitely until `RecursionError` | Track visited flags in a set during dependency resolution; break cycles |
| `rollout_pct` set above 100 or below 0 | Above 100: always on (harmless). Below 0: always off (surprising) | Clamp to 0-100 range in the Flag constructor or `flags_from_config` |
| Flag name typo in `requires` list | Dependency check calls `is_enabled("typo")`, which returns False for unknown flags | Validate that all dependency names exist in the flag registry during initialization |
