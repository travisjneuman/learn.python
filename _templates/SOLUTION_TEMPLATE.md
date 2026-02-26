# Solution: [PROJECT_TITLE]

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [Walkthrough](./WALKTHROUGH.md) first — it guides
> your thinking without giving away the answer.

---

## Complete solution

```python
"""[Module docstring].

WHY this module exists: [Context from README]
"""

# WHY we import X: [Reason for this import]
import x


def function_name(param: type) -> return_type:
    """[Docstring].

    WHY this function: [Design reason — why a separate function?]
    WHY this signature: [Parameter choices — why these inputs?]
    """
    # WHY this check: [Guard clause reason]
    if not param:
        raise ValueError("param cannot be empty")

    # WHY this approach: [Algorithm or pattern choice]
    result = param.process()

    return result
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| [Decision 1] | [Reason] | [What else could work] |
| [Decision 2] | [Reason] | [What else could work] |
| [Decision 3] | [Reason] | [What else could work] |

## Alternative approaches

### Approach B: [Name]

```python
# Different valid approach with trade-offs explained
```

**Trade-off:** [When you would prefer this approach vs the primary one]

### Approach C: [Name] (advanced)

```python
# More sophisticated approach — come back to this after learning [concept]
```

**Trade-off:** [This approach is better when X, but worse when Y]

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| [Bad input 1] | [Error/behavior] | [How to handle] |
| [Edge case 1] | [Behavior] | [How to handle] |
| [Edge case 2] | [Behavior] | [How to handle] |

## Key takeaways

1. [Most important lesson from this project]
2. [Second lesson]
3. [Connection to future concepts — "You will use this pattern again in Level X"]
