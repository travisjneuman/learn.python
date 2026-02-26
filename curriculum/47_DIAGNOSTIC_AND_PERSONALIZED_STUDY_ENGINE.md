# 47 - Diagnostic and Personalized Study Engine (Adaptive, Not Generic)
Home: [README](../README.md)

Path placeholder: `<repo-root>` means the folder containing this repository's `README.md`.

Use this diagnostic to generate a personalized plan with explicit doc/project order and pacing.

## Inputs captured
- Hours per week.
- Confidence level.
- Preferred learning mode.
- Starting skill estimate.
- End goal (automation, full-stack, elite).
- Current stuck area.

## Tooling in this repo
Generate a custom plan from terminal:

```bash
cd <repo-root>
python tools/generate_personalized_study_plan.py \
  --hours-per-week 8 \
  --learning-mode hybrid \
  --confidence medium \
  --experience zero \
  --goal elite \
  --stuck-area setup \
  --output personalized_plan.md
```

## Output contract
The generated plan must include:
1. Recommended weekly cadence.
2. Doc sequence priorities.
3. Project-level starting point.
4. Catch-up protocol if behind.
5. Escalation path when blocked for 2+ sessions.

## Re-run cadence
- Re-run diagnostic every 4 weeks.
- Re-run immediately after two failed weekly goals.

## Primary Sources
- [Python Tutorial](https://docs.python.org/3/tutorial/)
- [pytest docs](https://docs.pytest.org/en/stable/)
- [Ruff docs](https://docs.astral.sh/ruff/)

## Optional Resources
- [Exercism Python Track](https://exercism.org/tracks/python)
- [Real Python](https://realpython.com/tutorials/python/)

## Next

[Next: 48_MISCONCEPTION_AND_FAILURE_ATLAS_EXPANDED.md →](./48_MISCONCEPTION_AND_FAILURE_ATLAS_EXPANDED.md)
