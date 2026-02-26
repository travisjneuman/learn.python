# Level 9 / Project 13 - Platform Cost Estimator
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus
- Strategy pattern for cloud pricing models (on-demand, reserved, spot)
- Tiered pricing calculation with volume discounts
- Resource usage modeling: compute, storage, network, database
- What-if scenario analysis for cost optimization
- Cost optimization recommendations based on usage patterns

## Why this project exists
Cloud infrastructure costs can spiral without visibility — a team discovers their monthly
AWS bill doubled because someone left GPU instances running over a holiday weekend. This
project models resource consumption across compute, storage, network, and database tiers,
projects monthly costs using different pricing models, and runs what-if scenarios to find
optimization opportunities. It teaches the same FinOps (financial operations) approach
used by cloud cost management platforms like CloudHealth and Kubecost.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-9/13-platform-cost-estimator
python project.py --demo
pytest -q
```

## Expected terminal output
```text
{
  "total_monthly": 12450.00,
  "by_resource": {...},
  "what_if_savings": {...},
  "recommendations": [...]
}
7 passed
```

## Expected artifacts
- Console JSON output with cost estimates and optimization recommendations
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `SAVINGS_PLAN` pricing tier with even lower rates than reserved.
2. Add a `by_tag` breakdown that groups costs by resource tags (e.g. team, environment).
3. Add a `--budget` flag that compares estimated costs against a monthly budget limit.

## Break it (required)
1. Create a `ResourceUsage` with `quantity=-100` — does the cost calculation handle negatives?
2. Use a `PricingTier.SPOT` for a resource type with no spot pricing rule — what fallback occurs?
3. Set volume tier thresholds in non-ascending order — does `PricingRule.calculate` break?

## Fix it (required)
1. Validate that `quantity >= 0` in resource usage.
2. Sort volume tiers by threshold in `PricingRule.calculate` to handle unsorted input.
3. Add a test for the fallback-to-on-demand pricing behavior.

## Explain it (teach-back)
1. How do cloud pricing tiers (on-demand, reserved, spot) differ in cost and commitment?
2. What are volume discount tiers and how does tiered pricing work in practice?
3. Why is what-if analysis important for infrastructure cost optimization?
4. How do real FinOps teams use cost estimators to manage cloud spend?

## Mastery check
You can move on when you can:
- explain on-demand vs reserved vs spot pricing with real-world examples,
- run a what-if scenario that shows savings from switching pricing tiers,
- describe how volume tiers apply different rates to different usage ranges,
- add a new resource type with custom pricing rules.

---

## Related Concepts

- [Async Explained](../../../concepts/async-explained.md)
- [Classes and Objects](../../../concepts/classes-and-objects.md)
- [Decorators Explained](../../../concepts/decorators-explained.md)
- [How Loops Work](../../../concepts/how-loops-work.md)
- [Quiz: Async Explained](../../../concepts/quizzes/async-explained-quiz.py)

---

| [← Prev](../12-incident-postmortem-generator/README.md) | [Home](../../../README.md) | [Next →](../14-cross-team-handoff-kit/README.md) |
|:---|:---:|---:|
