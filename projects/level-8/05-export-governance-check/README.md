# Level 8 / Project 05 - Export Governance Check
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus
- Strategy pattern for pluggable validation rules
- PII detection via regex and column-name heuristics
- Severity-based violation classification (info, warning, critical, blocking)
- Composable rule evaluation pipeline
- Structured audit logging for compliance

## Why this project exists
Enterprise systems must enforce data governance before exporting data: PII detection,
size limits, format validation, and access control. A single accidental CSV export
containing Social Security numbers can trigger regulatory fines. This project builds
a rule engine that validates export requests against configurable policies — the same
pattern used in compliance-heavy industries like finance, healthcare, and government.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-8/05-export-governance-check
python project.py --input data/sample_input.json
pytest -q
```

## Expected terminal output
```text
{
  "export_id": "demo-001",
  "approved": false,
  "rules_checked": 5,
  "violation_count": 4,
  "blocking_count": 2,
  "violations": [...]
}
7 passed
```

## Expected artifacts
- Console JSON output showing governance evaluation
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a new rule `check_column_count` that blocks exports with more than 50 columns.
2. Add an `--allow-format` flag that overrides the default allowed formats.
3. Add a `check_data_freshness` rule that warns if sample timestamps are older than 30 days.

## Break it (required)
1. Pass an export with 200,000 rows — does `check_row_limit` block it correctly?
2. Submit a request with `classification="restricted"` — is the export blocked?
3. Include a credit card pattern (`1234-5678-9012-3456`) in sample data — does content scanning find it?

## Fix it (required)
1. Add deduplication so the same PII field is not flagged twice (once by column name, once by content).
2. Add a `--dry-run` mode that reports violations without writing any output file.
3. Add a test for each PII pattern (email, SSN, phone, credit card).

## Explain it (teach-back)
1. What is the Strategy pattern and how do pluggable rule functions implement it here?
2. Why does the engine use a `Callable` type alias instead of class inheritance for rules?
3. What is PII and why must exports be scanned for it before leaving the system?
4. How would you add a new governance rule without modifying existing code?

## Mastery check
You can move on when you can:
- explain the Strategy pattern with a concrete code example,
- add a new governance rule and wire it into the default rule set,
- describe PII categories and why each requires different handling,
- explain how severity levels (info → blocking) drive approval decisions.

## Mastery Check
- [ ] Can you explain the architectural trade-offs in your solution?
- [ ] Could you refactor this for a completely different use case?
- [ ] Can you identify at least two alternative approaches and explain why you chose yours?
- [ ] Could you debug this without print statements, using only breakpoint()?

---

## Related Concepts

- [Decorators Explained](../../../concepts/decorators-explained.md)
- [Error Handling](../../../concepts/error-handling.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [Types Explained](../../../concepts/types-explained.md)
- [Quiz: Error Handling](../../../concepts/quizzes/error-handling-quiz.py)

---

| [← Prev](../04-filter-state-manager/README.md) | [Home](../../../README.md) | [Next →](../06-response-time-profiler/README.md) |
|:---|:---:|---:|
