# Level 9 / Project 08 - Change Impact Analyzer
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus
- BFS graph traversal for impact propagation through service dependencies
- Risk scoring with weighted factors (change type, service tier, dependency depth)
- Service dependency graph modeling with tier classification
- Blast radius estimation for proposed changes
- Stakeholder identification from affected service ownership

## Why this project exists
Before deploying a change, engineers must understand its blast radius: which services,
teams, and SLOs are affected. A database schema migration might seem local, but it
propagates through 12 downstream services owned by 4 different teams. This project
builds an impact analyzer that traverses dependency graphs, scores change risk based
on service tiers and change types, and identifies all affected stakeholders — the same
analysis that platform teams perform before every production deployment.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-9/08-change-impact-analyzer
python project.py --demo
pytest -q
```

## Expected terminal output
```text
{
  "change": {"service": "user-db", "type": "schema_migration"},
  "blast_radius": 5,
  "risk_score": 8.5,
  "affected_services": [...],
  "affected_teams": [...]
}
7 passed
```

## Expected artifacts
- Console JSON output with impact analysis
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `visualize_blast_radius()` method that outputs affected services as a tree diagram.
2. Add a `ChangeType.INFRASTRUCTURE` variant with its own risk scoring multiplier.
3. Add a `--team` filter that shows only impact on services owned by a specific team.

## Break it (required)
1. Create a circular dependency (A -> B -> A) — does `transitive_dependents` handle cycles?
2. Analyze a change to a service not in the graph — what error or result occurs?
3. Set service tier to 0 (invalid) — does the risk scoring handle it?

## Fix it (required)
1. Add cycle detection in `transitive_dependents` using a visited set.
2. Return a clear error when the changed service is not found in the graph.
3. Validate service tier values are in the range 1-3.

## Explain it (teach-back)
1. What is blast radius analysis and why is it important before making changes?
2. How does BFS traversal find transitive dependents in a service graph?
3. Why do schema changes carry higher risk than code changes?
4. How do real organizations use impact analysis to decide deployment strategies?

## Mastery check
You can move on when you can:
- explain BFS graph traversal and how it maps to dependency discovery,
- add a new service to the graph and predict its impact on risk scores,
- describe how service tiers affect risk scoring (tier-1 = critical = higher risk),
- design an impact analysis for a real microservices architecture.

---

## Related Concepts

- [Async Explained](../../../concepts/async-explained.md)
- [Classes and Objects](../../../concepts/classes-and-objects.md)
- [Decorators Explained](../../../concepts/decorators-explained.md)
- [Virtual Environments](../../../concepts/virtual-environments.md)
- [Quiz: Async Explained](../../../concepts/quizzes/async-explained-quiz.py)

---

| [← Prev](../07-canary-rollout-simulator/README.md) | [Home](../../../README.md) | [Next →](../09-security-baseline-auditor/README.md) |
|:---|:---:|---:|
