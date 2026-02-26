"""Level 7 / Project 11 — Pipeline Feature Flags.

Runtime toggles that let operators enable or disable pipeline stages
without redeploying.  Flags are stored in a simple JSON config and
evaluated at each stage boundary.

Key concepts:
- Feature flag evaluation (boolean + percentage rollout)
- Flag dependency chains (flag A requires flag B)
- Safe defaults when flag config is missing
- Audit log of flag evaluations
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
# pipeline stages at runtime without redeploying code. The rollout_pct
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
        """Check if a flag is active.  Respects dependencies and rollout %."""
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

        # Percentage rollout (deterministic hash)
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
