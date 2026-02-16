# Level 4 / Project 15 - Mini Pipeline Capstone
Home: [README](../../../README.md)

## Skill level
- Level 4 (Junior Plus)

## Focus
- end-to-end ingestion and publishing

## Project goal
Build a working project skeleton that you can alter, break, fix, and explain.

## Starter commands
Use the exact commands below.

## Alter it
Add file path validation and structured error messages.

## Break it
Point to missing files and invalid paths.

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
Go back to [Level 4 index](../README.md).

### Exact commands
```bash
python project.py --input data/sample_input.txt --output data/output_summary.json
pytest -q
```
