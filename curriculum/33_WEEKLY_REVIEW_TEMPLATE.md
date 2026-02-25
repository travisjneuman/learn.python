# 33 - Weekly Review Template (No Fake Progress)
Home: [README](../README.md)

Path placeholder: `<repo-root>` means the folder containing this repository's `README.md`.

Use this every week to prevent drifting and self-delusion.

## Weekly evidence pull (copy/paste)
```bash
cd <repo-root>
git log --since="7 days ago" --oneline
```

Expected output:
```text
<one or more commits showing study activity>
```

Optional weekly quality snapshot:
```bash
# run from one active project folder
pytest -q
ruff check .
black --check .
```

Expected output:
```text
... passed ...
All checks passed!
would reformat 0 files
```

## Weekly scorecard
- Projects completed:
- Break/fix drills completed:
- Tests added or improved:
- Major blockers:
- Root causes discovered:
- Confidence level (1-10):

## Hard questions
1. What did I avoid this week because it was hard?
2. Which bug took longest and why?
3. Which concept still feels fragile?
4. What exact fix will I prioritize next week?

## Next-week plan
- Top 3 priorities:
- One stretch goal:
- One non-negotiable mastery check:

## Weekly scoring rubric (0-2 each)
- Build output quality:
- Test quality:
- Failure diagnosis quality:
- Documentation clarity:
- Consistency (sessions completed):

Interpretation:
- 0-4: stabilization week needed.
- 5-7: continue current pace.
- 8-10: increase complexity next week.

## Primary Sources
- [pytest getting started](https://docs.pytest.org/en/stable/getting-started.html)
- [Python tutorial](https://docs.python.org/3/tutorial/)

## Optional Resources
- [Pro Git Book](https://git-scm.com/book/en/v2.html)

## Next
Go to [34_FAILURE_RECOVERY_ATLAS.md](./34_FAILURE_RECOVERY_ATLAS.md).
