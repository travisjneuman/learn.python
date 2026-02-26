# Level 9 / Project 02 - Domain Boundary Enforcer
Home: [README](../../../README.md)

## Focus
- Graph-based dependency modeling for module boundaries
- Allow/deny rule engine for cross-module imports
- DFS-based cycle detection in directed dependency graphs
- Layered architecture validation (lower layers cannot depend on upper)
- Chain of Responsibility pattern for rule evaluation

## Why this project exists
As codebases grow, uncontrolled cross-module dependencies create "Big Ball of Mud"
architectures where everything depends on everything. A small change in one module
breaks 15 others. This project builds a dependency rule engine that defines
allowed/forbidden imports between domains, detects cycles, and validates layering
rules — the same pattern used by tools like ArchUnit, deptry, and import-linter
to enforce architectural boundaries in real Python and Java projects.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-9/02-domain-boundary-enforcer
python project.py --demo
pytest -q
```

## Expected terminal output
```text
{
  "modules": 6,
  "violations": [...],
  "cycles": [],
  "layer_violations": [...]
}
7 passed
```

## Expected artifacts
- Console JSON output with boundary enforcement results
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `visualize_graph()` method that outputs the dependency graph in DOT format.
2. Add wildcard support for boundary rules (e.g. `infra.*` blocks all infra sub-modules).
3. Add a `--strict` flag that treats layer violations as errors (exit code 1).

## Break it (required)
1. Add a circular dependency (A -> B -> C -> A) — does `detect_cycles` catch it?
2. Add a dependency from a lower layer to a higher layer — does the layer rule catch it?
3. Remove a module that others depend on — what happens during `enforce()`?

## Fix it (required)
1. Improve the cycle detection error message to show the full cycle path.
2. Add validation that modules in rules must exist in the dependency graph.
3. Add a test for multi-step transitive dependency violations.

## Explain it (teach-back)
1. What are domain boundaries and why do large codebases need enforced module rules?
2. How does DFS-based cycle detection work in a directed graph?
3. What is the layered architecture pattern and why should lower layers never depend on upper ones?
4. How do tools like `deptry` or `import-linter` enforce boundaries in real Python projects?

## Mastery check
You can move on when you can:
- explain dependency graphs, cycles, and topological ordering,
- add a new boundary rule and verify it with existing tests,
- describe how layered architecture prevents spaghetti dependencies,
- detect and break a circular dependency given a graph description.

## Mastery Check
- [ ] Can you explain the architectural trade-offs in your solution?
- [ ] Could you refactor this for a completely different use case?
- [ ] Can you identify at least two alternative approaches and explain why you chose yours?
- [ ] Could you debug this without print statements, using only breakpoint()?

---

## Related Concepts

- [Async Explained](../../../concepts/async-explained.md)
- [Classes and Objects](../../../concepts/classes-and-objects.md)
- [Decorators Explained](../../../concepts/decorators-explained.md)
- [How Imports Work](../../../concepts/how-imports-work.md)
- [Quiz: Async Explained](../../../concepts/quizzes/async-explained-quiz.py)

---

| [← Prev](../01-architecture-decision-log/README.md) | [Home](../../../README.md) | [Next →](../03-event-driven-pipeline-lab/README.md) |
|:---|:---:|---:|
