# Diagrams: Virtual Environments

[Back to concept](../virtual-environments.md)

---

## Virtual Environment Creation Flow

Creating and using a virtual environment follows a predictable lifecycle.

```mermaid
flowchart TD
    START["Start a new project"] --> CREATE["python -m venv .venv"]
    CREATE --> CREATED["Directory .venv/ created<br/>with its own Python copy"]
    CREATED --> ACTIVATE["Activate it"]
    ACTIVATE --> WIN["Windows:<br/>.venv\Scripts\activate"]
    ACTIVATE --> MAC["macOS/Linux:<br/>source .venv/bin/activate"]
    WIN --> ACTIVE["(.venv) appears in prompt<br/>python and pip point to .venv/"]
    MAC --> ACTIVE
    ACTIVE --> INSTALL["pip install requests flask ..."]
    INSTALL --> FREEZE["pip freeze > requirements.txt"]
    FREEZE --> WORK["Write your code"]
    WORK --> DONE["Done for now?"]
    DONE --> DEACTIVATE["deactivate"]
    DEACTIVATE --> BACK["Back to system Python"]

    style CREATE fill:#4a9eff,stroke:#2670c2,color:#fff
    style ACTIVE fill:#51cf66,stroke:#27ae60,color:#fff
    style DEACTIVATE fill:#ffd43b,stroke:#f59f00,color:#000
```

## Package Isolation: Why Virtual Environments Matter

Without venvs, all projects share the same packages. Version conflicts break things.

```mermaid
flowchart TD
    subgraph PROBLEM ["Without venvs: CONFLICT"]
        SYS["System Python"]
        PROJ_A["Project A<br/>needs requests 2.28"]
        PROJ_B["Project B<br/>needs requests 2.31"]
        SYS --> PROJ_A
        SYS --> PROJ_B
        CONFLICT["Only ONE version<br/>can be installed!"]
        PROJ_A --> CONFLICT
        PROJ_B --> CONFLICT
    end

    subgraph SOLUTION ["With venvs: ISOLATED"]
        VENV_A[".venv for Project A<br/>requests==2.28"]
        VENV_B[".venv for Project B<br/>requests==2.31"]
        OK_A["Project A works"]
        OK_B["Project B works"]
        VENV_A --> OK_A
        VENV_B --> OK_B
    end

    style PROBLEM fill:#ff6b6b,stroke:#c0392b,color:#fff
    style SOLUTION fill:#51cf66,stroke:#27ae60,color:#fff
    style CONFLICT fill:#ff6b6b,stroke:#c0392b,color:#fff
```

## Activate / Deactivate Lifecycle

Activating changes which `python` and `pip` your terminal uses. Deactivating restores the system default.

```mermaid
flowchart LR
    subgraph BEFORE ["Before activate"]
        B1["python → /usr/bin/python3"]
        B2["pip → /usr/bin/pip3"]
        B3["Packages: system-wide"]
    end

    subgraph DURING ["After activate"]
        D1["python → .venv/bin/python"]
        D2["pip → .venv/bin/pip"]
        D3["Packages: .venv/lib/ only"]
    end

    subgraph AFTER ["After deactivate"]
        A1["python → /usr/bin/python3"]
        A2["pip → /usr/bin/pip3"]
        A3["Back to system packages"]
    end

    BEFORE -->|"source .venv/bin/activate"| DURING
    DURING -->|"deactivate"| AFTER

    style BEFORE fill:#ffd43b,stroke:#f59f00,color:#000
    style DURING fill:#51cf66,stroke:#27ae60,color:#fff
    style AFTER fill:#ffd43b,stroke:#f59f00,color:#000
```
