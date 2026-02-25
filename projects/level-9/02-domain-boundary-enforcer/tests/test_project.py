"""Tests for Domain Boundary Enforcer.

Covers: dependency graph, cycle detection, rule enforcement, layer checking.
"""

from __future__ import annotations

import pytest

from project import (
    BoundaryEnforcer,
    DependencyGraph,
    DependencyRule,
    DomainModule,
    RuleType,
    ViolationSeverity,
)


# --- DependencyGraph ----------------------------------------------------

class TestDependencyGraph:
    def test_add_and_query_edges(self) -> None:
        g = DependencyGraph()
        g.add_edge("a", "b")
        g.add_edge("a", "c")
        assert g.dependencies_of("a") == {"b", "c"}

    def test_dependents_of(self) -> None:
        g = DependencyGraph()
        g.add_edge("a", "b")
        g.add_edge("c", "b")
        assert g.dependents_of("b") == {"a", "c"}

    def test_no_cycle(self) -> None:
        g = DependencyGraph()
        g.add_edge("a", "b")
        g.add_edge("b", "c")
        assert g.has_cycle() is False

    def test_cycle_detected(self) -> None:
        g = DependencyGraph()
        g.add_edge("a", "b")
        g.add_edge("b", "c")
        g.add_edge("c", "a")
        assert g.has_cycle() is True

    def test_self_loop_is_cycle(self) -> None:
        g = DependencyGraph()
        g.add_edge("a", "a")
        assert g.has_cycle() is True


# --- Rule enforcement ---------------------------------------------------

class TestBoundaryEnforcer:
    def test_deny_rule_creates_violation(self) -> None:
        enforcer = BoundaryEnforcer()
        enforcer.add_rule(DependencyRule("a", "b", RuleType.DENY, reason="forbidden"))
        g = DependencyGraph()
        g.add_edge("a", "b")
        violations = enforcer.enforce(g)
        assert len(violations) >= 1
        assert any(v.source == "a" and v.target == "b" for v in violations)

    def test_allow_rule_permits(self) -> None:
        enforcer = BoundaryEnforcer()
        enforcer.add_rule(DependencyRule("a", "b", RuleType.ALLOW))
        g = DependencyGraph()
        g.add_edge("a", "b")
        violations = enforcer.enforce(g)
        boundary_violations = [v for v in violations if v.source == "a" and v.target == "b"]
        assert len(boundary_violations) == 0

    def test_wildcard_deny(self) -> None:
        enforcer = BoundaryEnforcer()
        enforcer.add_rule(DependencyRule("*", "secret", RuleType.DENY))
        g = DependencyGraph()
        g.add_edge("any_module", "secret")
        violations = enforcer.enforce(g)
        assert any(v.target == "secret" for v in violations)

    @pytest.mark.parametrize("default_allow,expect_violation", [
        (True, False),
        (False, True),
    ])
    def test_default_policy(self, default_allow: bool, expect_violation: bool) -> None:
        enforcer = BoundaryEnforcer(default_allow=default_allow)
        g = DependencyGraph()
        g.add_edge("x", "y")
        violations = enforcer.enforce(g)
        has_violation = any(v.source == "x" and v.target == "y" for v in violations)
        assert has_violation == expect_violation


# --- Layer violations ---------------------------------------------------

class TestLayerViolations:
    def test_upward_dependency_flagged(self) -> None:
        enforcer = BoundaryEnforcer()
        enforcer.register_module(DomainModule("infra", layer=0))
        enforcer.register_module(DomainModule("app", layer=2))
        g = DependencyGraph()
        g.add_edge("infra", "app")  # infra(0) -> app(2): upward violation
        violations = enforcer.enforce(g)
        assert any("Layer violation" in v.message for v in violations)

    def test_downward_dependency_allowed(self) -> None:
        enforcer = BoundaryEnforcer()
        enforcer.register_module(DomainModule("app", layer=2))
        enforcer.register_module(DomainModule("domain", layer=1))
        g = DependencyGraph()
        g.add_edge("app", "domain")  # downward: ok
        violations = enforcer.enforce(g)
        layer_violations = [v for v in violations if "Layer" in v.message]
        assert len(layer_violations) == 0
