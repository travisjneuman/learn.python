# CI/CD Pipeline — Diagrams

[<- Back to Diagram Index](../../guides/DIAGRAM_INDEX.md)

## Overview

These diagrams show how continuous integration and continuous deployment pipelines automate code quality checks, testing, and deployment using GitHub Actions as the primary example.

## Full CI/CD Pipeline Flow

A CI/CD pipeline runs automatically on every push or pull request. Each stage acts as a gate: if one fails, later stages do not run, preventing broken code from reaching production.

```mermaid
flowchart LR
    PUSH["git push / PR opened"] --> LINT["Lint & Format<br/>ruff check .<br/>black --check ."]
    LINT -->|"Pass"| TYPE["Type Check<br/>mypy src/"]
    TYPE -->|"Pass"| TEST["Run Tests<br/>pytest --cov"]
    TEST -->|"Pass"| BUILD["Build<br/>docker build -t app ."]
    BUILD -->|"Pass"| DEPLOY_STAGING["Deploy to Staging<br/>Automatic"]
    DEPLOY_STAGING --> SMOKE["Smoke Tests<br/>Hit /health endpoint"]
    SMOKE -->|"Pass"| GATE{"Manual Approval?"}
    GATE -->|"Approved"| DEPLOY_PROD["Deploy to Production"]
    GATE -->|"Skip"| DONE["Pipeline Complete"]
    DEPLOY_PROD --> DONE

    LINT -->|"Fail"| STOP1["Pipeline Stops<br/>Fix lint errors"]
    TYPE -->|"Fail"| STOP2["Pipeline Stops<br/>Fix type errors"]
    TEST -->|"Fail"| STOP3["Pipeline Stops<br/>Fix failing tests"]
    BUILD -->|"Fail"| STOP4["Pipeline Stops<br/>Fix build errors"]

    style PUSH fill:#cc5de8,stroke:#9c36b5,color:#fff
    style LINT fill:#ffd43b,stroke:#f59f00,color:#000
    style TYPE fill:#ffd43b,stroke:#f59f00,color:#000
    style TEST fill:#4a9eff,stroke:#2670c2,color:#fff
    style BUILD fill:#ff922b,stroke:#e8590c,color:#fff
    style DEPLOY_STAGING fill:#51cf66,stroke:#27ae60,color:#fff
    style DEPLOY_PROD fill:#51cf66,stroke:#27ae60,color:#fff
    style STOP1 fill:#ff6b6b,stroke:#c92a2a,color:#fff
    style STOP2 fill:#ff6b6b,stroke:#c92a2a,color:#fff
    style STOP3 fill:#ff6b6b,stroke:#c92a2a,color:#fff
    style STOP4 fill:#ff6b6b,stroke:#c92a2a,color:#fff
```

**Key points:**
- Fast checks (lint, format) run first so you get quick feedback on simple mistakes
- Each stage is a gate: failures stop the pipeline early, saving compute time
- Staging deployment happens automatically; production may require manual approval
- Smoke tests verify the deployed app actually starts and responds

## GitHub Actions Workflow Structure

A GitHub Actions workflow is a YAML file in `.github/workflows/`. It defines triggers, jobs, and steps. Jobs run in parallel by default; use `needs` to create dependencies.

```mermaid
flowchart TD
    subgraph TRIGGER ["Triggers (on:)"]
        PUSH_T["push:<br/>branches: [main]"]
        PR_T["pull_request:<br/>branches: [main]"]
    end

    subgraph JOB_LINT ["Job: lint"]
        LINT_1["runs-on: ubuntu-latest"]
        LINT_2["Step: checkout code"]
        LINT_3["Step: setup-python"]
        LINT_4["Step: pip install ruff"]
        LINT_5["Step: ruff check ."]
        LINT_1 --> LINT_2 --> LINT_3 --> LINT_4 --> LINT_5
    end

    subgraph JOB_TEST ["Job: test"]
        TEST_1["runs-on: ubuntu-latest"]
        TEST_M["strategy: matrix<br/>python: [3.11, 3.12, 3.13]"]
        TEST_2["Step: checkout code"]
        TEST_3["Step: setup-python (matrix)"]
        TEST_4["Step: pip install -r requirements.txt"]
        TEST_5["Step: pytest --cov"]
        TEST_1 --> TEST_M --> TEST_2 --> TEST_3 --> TEST_4 --> TEST_5
    end

    subgraph JOB_DEPLOY ["Job: deploy"]
        DEP_1["runs-on: ubuntu-latest"]
        DEP_2["Step: checkout code"]
        DEP_3["Step: deploy to Railway/Render"]
        DEP_1 --> DEP_2 --> DEP_3
    end

    PUSH_T --> JOB_LINT
    PR_T --> JOB_LINT
    PUSH_T --> JOB_TEST
    PR_T --> JOB_TEST
    JOB_LINT -->|"needs: lint"| JOB_DEPLOY
    JOB_TEST -->|"needs: test"| JOB_DEPLOY

    style TRIGGER fill:#cc5de8,stroke:#9c36b5,color:#fff
    style JOB_LINT fill:#ffd43b,stroke:#f59f00,color:#000
    style JOB_TEST fill:#4a9eff,stroke:#2670c2,color:#fff
    style JOB_DEPLOY fill:#51cf66,stroke:#27ae60,color:#fff
```

**Key points:**
- Jobs run in parallel by default: `lint` and `test` start at the same time
- `needs:` creates dependencies: `deploy` waits for both `lint` and `test` to pass
- Matrix strategy runs the same steps across multiple Python versions simultaneously
- Each job gets a fresh virtual machine: no state leaks between jobs

## Sequence: Pull Request Lifecycle

The full lifecycle from opening a PR to merging, showing how CI checks integrate with code review.

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant GH as GitHub
    participant CI as GitHub Actions
    participant Rev as Reviewer

    Dev->>GH: Open Pull Request
    GH->>CI: Trigger workflow (on: pull_request)

    par Parallel Jobs
        CI->>CI: Job: lint (ruff, black)
        CI->>CI: Job: test (pytest, 3 Python versions)
    end

    alt All checks pass
        CI-->>GH: Status: All checks passed
        GH-->>Dev: Green checkmarks
        Dev->>Rev: Request review
        Rev->>GH: Review changes
        Rev-->>Dev: Approve / Request changes

        alt Approved
            Dev->>GH: Merge PR
            GH->>CI: Trigger deploy workflow (on: push to main)
            CI->>CI: Build and deploy to production
            CI-->>GH: Deployment successful
        end
    else Some checks fail
        CI-->>GH: Status: Checks failed
        GH-->>Dev: Red X marks
        Dev->>Dev: Fix issues locally
        Dev->>GH: Push fix commits
        GH->>CI: Re-trigger workflow
    end
```

**Key points:**
- CI runs automatically when a PR is opened and on every subsequent push to the PR branch
- Merge is blocked until all required checks pass (configurable in branch protection rules)
- Deploying on merge to `main` means every merged PR goes to production automatically
- Failed checks give immediate feedback: fix and push again to re-trigger

---

| [Back to Diagram Index](../../guides/DIAGRAM_INDEX.md) |
|:---:|
