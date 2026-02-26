# 40 - Security and Compliance Hardening (Default-Safe Engineering)
Home: [README](../README.md)

Security cannot be bolted on. It must be built in from first commit.

## Hardening objectives
- Protect credentials, tokens, and sensitive data.
- Enforce least privilege access patterns.
- Reduce dependency and supply-chain risk.
- Maintain auditable evidence of control execution.

## Hardening lab pack
1. Secrets handling baseline (env vars + secret manager model).
2. Input validation and output sanitization checks.
3. Dependency inventory and upgrade policy.
4. AuthN/AuthZ policy checks for services.
5. Audit log schema and retention policy.
6. Security incident drill with documented response.

## Evidence requirements
- Threat model for each major system.
- Security checklist in every release package.
- Audit-ready artifacts for quarterly review.

## Primary Sources
- [FastAPI security](https://fastapi.tiangolo.com/tutorial/security/first-steps/)
- [pip docs](https://pip.pypa.io/en/stable/)
- [PyPA guidance](https://packaging.python.org/en/latest/tutorials/installing-packages/)
- [Python logging HOWTO](https://docs.python.org/3/howto/logging.html)

## Optional Resources
- [Real Python](https://realpython.com/tutorials/python/)

## Next

[Next: 41_PERFORMANCE_ENGINEERING_LAB.md →](./41_PERFORMANCE_ENGINEERING_LAB.md)
