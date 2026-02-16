# Level 9 / Project 14 - Dashboard Data Feed
Home: [README](../../../README.md)

## Skill level
- Level 9 (Expert)

## Focus
- dashboard-friendly summary production

## Project goal
Build a working project skeleton that you can alter, break, fix, and explain.

## Starter commands
Use the exact commands below.

## Alter it
Add observability hooks and failure classification.

## Break it
Introduce partial failures and classify blast radius.

## Fix it
- Add validation and clear error messages.
- Update tests for the failure you created.
- Re-run and verify deterministic output.

## Explain it
Answer these prompts:
1. What input did this project expect?
2. What failed first and why?
3. What changed after your fix?
4. How would this scale in enterprise usage?

## Expected output
- Console summary JSON.
- Passing baseline tests.
- A short notes update with what you changed.

## Next
Go back to [Level 9 index](../README.md).

### Exact commands
```bash
python project.py --input data/sample_input.txt --output data/output_summary.json
pytest -q
```
