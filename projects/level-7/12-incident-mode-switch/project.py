"""Level 7 / Project 12 — Incident Mode Switch.

Implements graceful degradation for data pipelines.  When an incident
is declared, the system switches non-critical stages to passthrough
or skip mode while keeping essential stages running.

Key concepts:
- Operating modes: normal / degraded / maintenance / emergency
- Stage criticality levels (critical / standard / optional)
- Mode transition rules and validation
- Incident timeline logging
"""

from __future__ import annotations

import argparse
import json
import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


# -- Data model ----------------------------------------------------------

class Mode(Enum):
    NORMAL = "normal"
    DEGRADED = "degraded"
    MAINTENANCE = "maintenance"
    EMERGENCY = "emergency"


class Criticality(Enum):
    CRITICAL = "critical"
    STANDARD = "standard"
    OPTIONAL = "optional"


# Allowed transitions: from_mode → set of to_modes
TRANSITIONS: dict[Mode, set[Mode]] = {
    Mode.NORMAL: {Mode.DEGRADED, Mode.MAINTENANCE, Mode.EMERGENCY},
    Mode.DEGRADED: {Mode.NORMAL, Mode.EMERGENCY},
    Mode.MAINTENANCE: {Mode.NORMAL},
    Mode.EMERGENCY: {Mode.DEGRADED, Mode.NORMAL},
}

# Which criticality levels run in each mode
ACTIVE_IN: dict[Mode, set[Criticality]] = {
    Mode.NORMAL: {Criticality.CRITICAL, Criticality.STANDARD, Criticality.OPTIONAL},
    Mode.DEGRADED: {Criticality.CRITICAL, Criticality.STANDARD},
    Mode.MAINTENANCE: {Criticality.CRITICAL},
    Mode.EMERGENCY: {Criticality.CRITICAL},
}


@dataclass
class Stage:
    name: str
    criticality: Criticality


@dataclass
class IncidentEvent:
    timestamp: float
    from_mode: str
    to_mode: str
    reason: str


# -- Core logic ----------------------------------------------------------

class IncidentController:
    """Manage operating mode and decide which stages run."""

    def __init__(self, stages: list[Stage] | None = None) -> None:
        self.mode: Mode = Mode.NORMAL
        self.stages: list[Stage] = stages or []
        self.timeline: list[IncidentEvent] = []

    def can_transition(self, target: Mode) -> bool:
        return target in TRANSITIONS.get(self.mode, set())

    def switch_mode(self, target: Mode, reason: str = "") -> bool:
        if not self.can_transition(target):
            logging.warning("invalid transition %s → %s", self.mode.value, target.value)
            return False
        event = IncidentEvent(
            timestamp=time.time(),
            from_mode=self.mode.value,
            to_mode=target.value,
            reason=reason,
        )
        self.timeline.append(event)
        logging.info("mode %s → %s: %s", self.mode.value, target.value, reason)
        self.mode = target
        return True

    def active_stages(self) -> list[str]:
        """Return names of stages that should run in current mode."""
        allowed = ACTIVE_IN[self.mode]
        return [s.name for s in self.stages if s.criticality in allowed]

    def skipped_stages(self) -> list[str]:
        allowed = ACTIVE_IN[self.mode]
        return [s.name for s in self.stages if s.criticality not in allowed]

    def summary(self) -> dict:
        return {
            "mode": self.mode.value,
            "active": self.active_stages(),
            "skipped": self.skipped_stages(),
            "transitions": len(self.timeline),
        }


def stages_from_config(raw: list[dict]) -> list[Stage]:
    return [
        Stage(name=d["name"], criticality=Criticality(d.get("criticality", "standard")))
        for d in raw
    ]


# -- Entry points --------------------------------------------------------

def run(input_path: Path, output_path: Path) -> dict:
    config = json.loads(input_path.read_text(encoding="utf-8")) if input_path.exists() else {}

    stages = stages_from_config(config.get("stages", []))
    transitions = config.get("transitions", [])

    ctrl = IncidentController(stages)
    results: list[dict] = []

    for t in transitions:
        target = Mode(t["mode"])
        ok = ctrl.switch_mode(target, t.get("reason", ""))
        results.append({
            "target": target.value,
            "accepted": ok,
            "active_after": ctrl.active_stages(),
        })

    summary = {
        "final_mode": ctrl.mode.value,
        "transition_results": results,
        "timeline_events": len(ctrl.timeline),
        **ctrl.summary(),
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Incident Mode Switch")
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
