# 39 - Production Platform Lab (API + Jobs + Caching + Observability)
Home: [README](../README.md)

Build a reusable platform skeleton that mirrors real production constraints.

## Platform stack goals
- Service API layer
- Async/background job processing
- Caching layer
- Structured logging and metrics
- Health checks and readiness checks

## Mandatory lab sequence
1. Build API skeleton (versioned endpoints).
2. Add background jobs and retry policy.
3. Add cache with explicit TTL rules.
4. Add structured logs with correlation IDs.
5. Add smoke tests and integration tests.
6. Add load/error drill and recovery playbook.

## Deliverables
- Project template usable for future systems.
- Runbook and incident quick-start guide.
- One dashboard view of system health KPIs.

## Primary Sources
- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI security](https://fastapi.tiangolo.com/tutorial/security/first-steps/)
- [Streamlit docs](https://docs.streamlit.io/get-started)
- [Dash deployment](https://dash.plotly.com/deployment)

## Optional Resources
- [Real Python](https://realpython.com/tutorials/python/)

## Next

[Next: 40_SECURITY_COMPLIANCE_HARDENING.md →](./40_SECURITY_COMPLIANCE_HARDENING.md)
