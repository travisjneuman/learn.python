# Solution: Level 7 / Project 12 - Incident Mode Switch

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
"""Level 7 / Project 12 — Incident Mode Switch.

Implements graceful degradation for data pipelines.  When an incident
is declared, the system switches non-critical stages to passthrough
or skip mode while keeping essential stages running.
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


# WHY explicit transition rules? -- Not all mode changes are safe.  Jumping
# directly from MAINTENANCE to EMERGENCY could skip necessary recovery steps.
# Declaring valid transitions as data (not if/elif) makes the state machine
# auditable and prevents accidental illegal transitions.
TRANSITIONS: dict[Mode, set[Mode]] = {
    Mode.NORMAL: {Mode.DEGRADED, Mode.MAINTENANCE, Mode.EMERGENCY},
    Mode.DEGRADED: {Mode.NORMAL, Mode.EMERGENCY},
    Mode.MAINTENANCE: {Mode.NORMAL},
    Mode.EMERGENCY: {Mode.DEGRADED, Mode.NORMAL},
}

# WHY map modes to criticality sets? -- During an incident, you want to
# shed load by disabling non-essential stages.  This lookup table makes the
# decision mechanical: check if stage.criticality is in ACTIVE_IN[current_mode].
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
        """Check if transition is allowed from current mode."""
        return target in TRANSITIONS.get(self.mode, set())

    def switch_mode(self, target: Mode, reason: str = "") -> bool:
        """Attempt a mode transition.  Returns False if not allowed.

        WHY return bool instead of raising? -- In an incident, the operator
        may try several transitions quickly.  Returning False lets them
        try alternatives without catching exceptions in a high-stress moment.
        """
        if not self.can_transition(target):
            logging.warning("invalid transition %s -> %s", self.mode.value, target.value)
            return False
        event = IncidentEvent(
            timestamp=time.time(),
            from_mode=self.mode.value,
            to_mode=target.value,
            reason=reason,
        )
        self.timeline.append(event)
        logging.info("mode %s -> %s: %s", self.mode.value, target.value, reason)
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
        # WHY Mode(t["mode"]) here? -- Converts the raw string from config
        # into a Mode enum.  If the string is invalid, Python raises
        # ValueError immediately rather than letting a bad mode propagate.
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
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Transition rules as a data dict | Auditable and declarative; adding a new mode means updating the dict, not writing new if/elif branches | Method-per-transition -- e.g. `normal_to_degraded()` -- becomes combinatorially explosive with more modes |
| Enum for Mode and Criticality | Prevents typos (`Mode("norml")` raises ValueError immediately); IDE autocomplete helps operators | Plain strings -- flexible but typos cause silent bugs ("norml" != "normal") |
| `ACTIVE_IN` maps mode to allowed criticalities | Single lookup determines which stages run; no conditional logic in `active_stages()` | if/elif chain inside `active_stages` -- harder to audit and extend |
| `switch_mode` returns bool | Non-throwing API is safer during high-stress incident response | Raise on invalid transition -- forces try/except at every call site |

## Alternative approaches

### Approach B: State machine with enter/exit hooks

```python
class StateMachine:
    def __init__(self):
        self._hooks: dict[str, dict[str, Callable]] = {}

    def on_enter(self, mode: str, fn: Callable):
        self._hooks.setdefault(mode, {})["enter"] = fn

    def on_exit(self, mode: str, fn: Callable):
        self._hooks.setdefault(mode, {})["exit"] = fn

    def transition(self, target: Mode):
        self._hooks[self.mode.value].get("exit", lambda: None)()
        self.mode = target
        self._hooks[target.value].get("enter", lambda: None)()
```

**Trade-off:** Enter/exit hooks let you run cleanup on mode exit and initialization on mode enter (e.g. flush buffers when leaving normal, enable rate limiting when entering degraded). More powerful but adds complexity that is unnecessary when stages are simply toggled on/off.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Unknown mode string in config (e.g. `"panic"`) | `Mode("panic")` raises `ValueError` crashing the loop | Wrap `Mode(t["mode"])` in try/except and log a warning listing valid modes |
| Invalid transition attempted (e.g. maintenance to degraded) | `switch_mode` returns False; system stays in previous mode | Log the rejection clearly so the operator knows to try a different path |
| All stages marked as "optional" | In degraded/emergency mode, zero stages run; pipeline does nothing | Require at least one critical stage; validate stage list at startup |
