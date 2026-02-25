"""Domain Boundary Enforcer — enforce module boundaries and dependency rules.

Design rationale:
    As systems grow, uncontrolled cross-module dependencies create
    "Big Ball of Mud" architectures. This project builds a dependency
    rule engine that defines allowed/forbidden imports between domains,
    detects violations, and generates dependency graphs — the same
    pattern used by tools like ArchUnit and deptry.

Concepts practised:
    - graph-based dependency modeling
    - rule engine with allow/deny policies
    - topological analysis for layering violations
    - dataclasses for boundaries and violations
    - chain of responsibility for rule evaluation
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# --- Domain types -------------------------------------------------------

class RuleType(Enum):
    ALLOW = "allow"
    DENY = "deny"


class ViolationSeverity(Enum):
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class DomainModule:
    """A module or package within the system."""
    name: str
    layer: int = 0  # 0=infrastructure, 1=domain, 2=application, 3=presentation
    tags: list[str] = field(default_factory=list)


@dataclass
class DependencyRule:
    """A rule that allows or denies imports between modules."""
    source: str  # module name or "*" for wildcard
    target: str
    rule_type: RuleType
    severity: ViolationSeverity = ViolationSeverity.ERROR
    reason: str = ""


@dataclass
class DependencyEdge:
    """An actual dependency found in the codebase."""
    source: str
    target: str
    import_path: str = ""


@dataclass
class Violation:
    """A detected boundary violation."""
    source: str
    target: str
    rule: DependencyRule
    severity: ViolationSeverity
    message: str

    def to_dict(self) -> dict[str, str]:
        return {
            "source": self.source,
            "target": self.target,
            "severity": self.severity.value,
            "message": self.message,
        }


# --- Dependency graph ---------------------------------------------------

class DependencyGraph:
    """Directed graph of module dependencies."""

    def __init__(self) -> None:
        self._edges: list[DependencyEdge] = []
        self._adjacency: dict[str, set[str]] = defaultdict(set)

    def add_edge(self, source: str, target: str, import_path: str = "") -> None:
        self._edges.append(DependencyEdge(source, target, import_path))
        self._adjacency[source].add(target)

    @property
    def edges(self) -> list[DependencyEdge]:
        return list(self._edges)

    @property
    def nodes(self) -> set[str]:
        nodes: set[str] = set()
        for edge in self._edges:
            nodes.add(edge.source)
            nodes.add(edge.target)
        return nodes

    def dependencies_of(self, module: str) -> set[str]:
        return set(self._adjacency.get(module, set()))

    def dependents_of(self, module: str) -> set[str]:
        """Find all modules that depend on the given module."""
        return {e.source for e in self._edges if e.target == module}

    def has_cycle(self) -> bool:
        """Detect cycles using DFS-based cycle detection."""
        visited: set[str] = set()
        in_stack: set[str] = set()

        def dfs(node: str) -> bool:
            visited.add(node)
            in_stack.add(node)
            for neighbor in self._adjacency.get(node, set()):
                if neighbor in in_stack:
                    return True
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
            in_stack.discard(node)
            return False

        for node in self.nodes:
            if node not in visited:
                if dfs(node):
                    return True
        return False

    def to_dict(self) -> dict[str, Any]:
        return {
            "nodes": sorted(self.nodes),
            "edges": [{"from": e.source, "to": e.target} for e in self._edges],
            "has_cycle": self.has_cycle(),
        }


# --- Boundary enforcer (Chain of Responsibility) -----------------------

class BoundaryEnforcer:
    """Evaluates dependencies against boundary rules.

    Rules are evaluated in order (chain of responsibility):
    - First matching DENY rule produces a violation.
    - If no DENY matches and an ALLOW rule matches, the dependency is permitted.
    - If no rules match, a configurable default applies.
    """

    def __init__(self, default_allow: bool = True) -> None:
        self._rules: list[DependencyRule] = []
        self._modules: dict[str, DomainModule] = {}
        self._default_allow = default_allow

    def register_module(self, module: DomainModule) -> None:
        self._modules[module.name] = module

    def add_rule(self, rule: DependencyRule) -> None:
        self._rules.append(rule)

    def enforce(self, graph: DependencyGraph) -> list[Violation]:
        """Check all edges against rules and return violations."""
        violations: list[Violation] = []

        for edge in graph.edges:
            violation = self._check_edge(edge)
            if violation:
                violations.append(violation)

        # Also check layer violations
        violations.extend(self._check_layer_violations(graph))

        return violations

    def _check_edge(self, edge: DependencyEdge) -> Violation | None:
        """Evaluate a single edge against the rule chain."""
        for rule in self._rules:
            if self._rule_matches(rule, edge):
                if rule.rule_type == RuleType.DENY:
                    return Violation(
                        source=edge.source,
                        target=edge.target,
                        rule=rule,
                        severity=rule.severity,
                        message=rule.reason or
                                f"{edge.source} -> {edge.target} violates boundary rule",
                    )
                # ALLOW rule matched — dependency is ok
                return None

        # No rules matched — use default
        if not self._default_allow:
            return Violation(
                source=edge.source,
                target=edge.target,
                rule=DependencyRule(edge.source, edge.target, RuleType.DENY),
                severity=ViolationSeverity.WARNING,
                message=f"No explicit rule for {edge.source} -> {edge.target}",
            )
        return None

    def _rule_matches(self, rule: DependencyRule, edge: DependencyEdge) -> bool:
        source_match = rule.source == "*" or rule.source == edge.source
        target_match = rule.target == "*" or rule.target == edge.target
        return source_match and target_match

    def _check_layer_violations(self, graph: DependencyGraph) -> list[Violation]:
        """Check that dependencies flow downward through layers."""
        violations: list[Violation] = []
        for edge in graph.edges:
            src_mod = self._modules.get(edge.source)
            tgt_mod = self._modules.get(edge.target)
            if src_mod and tgt_mod and src_mod.layer < tgt_mod.layer:
                violations.append(Violation(
                    source=edge.source,
                    target=edge.target,
                    rule=DependencyRule(edge.source, edge.target, RuleType.DENY),
                    severity=ViolationSeverity.WARNING,
                    message=f"Layer violation: {edge.source} (L{src_mod.layer}) "
                            f"depends on {edge.target} (L{tgt_mod.layer})",
                ))
        return violations


# --- Demo ---------------------------------------------------------------

def run_demo() -> dict[str, Any]:
    enforcer = BoundaryEnforcer(default_allow=True)

    # Define domain modules with layers
    modules = [
        DomainModule("presentation", layer=3, tags=["ui"]),
        DomainModule("application", layer=2, tags=["service"]),
        DomainModule("domain", layer=1, tags=["core"]),
        DomainModule("infrastructure", layer=0, tags=["infra"]),
    ]
    for m in modules:
        enforcer.register_module(m)

    # Rules: infrastructure should not import from presentation
    enforcer.add_rule(DependencyRule(
        source="infrastructure", target="presentation",
        rule_type=RuleType.DENY, severity=ViolationSeverity.CRITICAL,
        reason="Infrastructure must not depend on presentation layer",
    ))
    enforcer.add_rule(DependencyRule(
        source="domain", target="infrastructure",
        rule_type=RuleType.DENY, severity=ViolationSeverity.ERROR,
        reason="Domain layer must not depend on infrastructure (use ports/adapters)",
    ))

    # Build dependency graph
    graph = DependencyGraph()
    graph.add_edge("presentation", "application")
    graph.add_edge("application", "domain")
    graph.add_edge("application", "infrastructure")
    graph.add_edge("domain", "infrastructure")  # violation!
    graph.add_edge("infrastructure", "presentation")  # violation!

    violations = enforcer.enforce(graph)

    return {
        "graph": graph.to_dict(),
        "violations": [v.to_dict() for v in violations],
        "violation_count": len(violations),
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Domain boundary enforcer")
    parser.add_argument("--demo", action="store_true", default=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    parse_args(argv)
    print(json.dumps(run_demo(), indent=2))


if __name__ == "__main__":
    main()
