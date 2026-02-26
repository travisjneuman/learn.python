# Level 10 / Project 04 - Multi Tenant Data Guard
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| [Concept](../../../concepts/how-imports-work.md) | **This project** | — | [Quiz](../../../concepts/quizzes/how-imports-work-quiz.py) | [Flashcards](../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus
- Proxy pattern for transparent tenant isolation
- Role-based access control (RBAC) with permission matrix
- Immutable tenant context to prevent mutation during operations
- Audit logging for every data access

## Why this project exists
In SaaS systems, tenant data leakage is catastrophic. This project makes tenant context mandatory at the data-access layer — not optional middleware — so cross-tenant access is structurally impossible. The Proxy pattern wraps a raw store, injecting filtering on every operation.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-10/04-multi-tenant-data-guard
python project.py
pytest -v
```

## Expected terminal output
```text
Acme sees 2 records
Super admin sees 3 records
Blocked: Tenant 'acme' cannot access record owned by 'globex'
Audit log (4 entries):
  [acme] alice -> INSERT inv-001
  ...
```

## Expected artifacts
- Demo output showing isolation and blocking
- Passing tests (`pytest -v` shows ~13 passed)

## Alter it (required)
1. Add a `FIELD_LEVEL` permission that lets certain roles see only specific fields (e.g., viewers cannot see `amount`).
2. Add a `bulk_insert` method that accepts multiple records and applies tenant tagging to each.
3. Re-run tests to verify isolation holds for bulk operations.

## Break it (required)
1. Try to read a record from another tenant — observe the `TenantViolationError`.
2. Use a `VIEWER` role to attempt an insert — observe `PermissionDeniedError`.
3. Mutate a `TenantContext` after creation (it should fail because it is frozen).

## Fix it (required)
1. Add rate limiting to the audit log (cap at N entries to prevent memory growth in long-running processes).
2. Add a `get_or_none` method that returns `None` instead of raising when a record belongs to another tenant.
3. Write tests for both fixes.

## Explain it (teach-back)
1. Why is `TenantContext` frozen (immutable)? What attacks does this prevent?
2. How does the Proxy pattern differ from middleware-based tenant filtering?
3. Why does the system log all access attempts, including denied ones?
4. How would you adapt this for a database-backed store using SQL WHERE clauses?

## Mastery check
You can move on when you can:
- explain why tenant isolation must happen at the data layer not the API layer,
- trace a cross-tenant access attempt through the code to see where it is blocked,
- add a new role with custom permissions and verify access control,
- describe the difference between RBAC and ABAC (attribute-based access control).

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Async Explained](../../../concepts/async-explained.md)
- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Functions Explained](../../../concepts/functions-explained.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../03-policy-as-code-validator/README.md) | [Home](../../../README.md) | [Next →](../05-compliance-evidence-builder/README.md) |
|:---|:---:|---:|
