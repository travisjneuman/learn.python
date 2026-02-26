# Architecture Decision Log — Step-by-Step Walkthrough

[<- Back to Project README](./README.md) · [Solution](./SOLUTION.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. This project introduces patterns used by professional engineering teams at companies like Spotify, AWS, and Google to document the _why_ behind architectural choices. Spend at least 30 minutes attempting it independently before reading on.

## Thinking Process

This project models a real-world Architecture Decision Record (ADR) system. An ADR is a short document capturing a significant decision: what was the context, what alternatives were considered, what was decided, and what are the consequences. The key insight is that documentation is an engineering practice, not a chore -- without ADRs, teams repeat past mistakes because they forget why decisions were made.

The code has three layers to think about. First, the **data model**: an `ADR` dataclass with a lifecycle defined by an enum (`PROPOSED -> ACCEPTED -> DEPRECATED/SUPERSEDED/REJECTED`). Second, the **ADRLog manager class** that handles CRUD, search, and filtering. Third, the **Observer pattern** for status change notifications -- callbacks that fire automatically when any ADR changes status, enabling audit trails and external integrations without the log needing to know about them.

Before coding, map the lifecycle in your head: every ADR starts as `PROPOSED`. It can be `ACCEPTED` or `REJECTED`. An accepted ADR can later be `DEPRECATED` (we stopped using it) or `SUPERSEDED` (a newer ADR replaced it). The `superseded_by` field links old decisions to their replacements, creating an audit chain.

## Step 1: Define the Status Enum and ADR Dataclass

**What to do:** Create an `ADRStatus` enum with five states and an `ADR` dataclass that captures the full decision record.

**Why:** The enum prevents invalid status strings (you cannot accidentally set status to `"aproved"`). The dataclass gives you a structured document with typed fields, automatic `__init__`, and a clear contract for what every ADR must contain.

```python
class ADRStatus(Enum):
    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    DEPRECATED = "deprecated"
    SUPERSEDED = "superseded"
    REJECTED = "rejected"


@dataclass
class ADR:
    adr_id: int
    title: str
    status: ADRStatus
    context: str
    decision: str
    consequences: str
    created_date: str = ""
    superseded_by: int | None = None
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.adr_id,
            "title": self.title,
            "status": self.status.value,
            # ... remaining fields
        }
```

Two details to notice:

- **`field(default_factory=list)`** is required for mutable defaults in dataclasses. If you wrote `tags: list[str] = []`, every ADR would share the same list object, causing bugs where tagging one ADR changes another.
- **`superseded_by: int | None = None`** creates a linked chain between ADRs. When ADR-2 supersedes ADR-1, you set `adr1.superseded_by = 2`, creating an audit trail.

**Predict:** Why use `.value` in `to_dict()` for the status field? What would `json.dumps()` do if you passed the raw enum?

## Step 2: Build the ADRLog Manager with CRUD Operations

**What to do:** Create an `ADRLog` class with `create()`, `get()`, and `all()` methods. Internally, store ADRs in a `dict[int, ADR]` and auto-increment the ID.

**Why:** The dictionary provides O(1) lookup by ID. Auto-incrementing IDs ensure uniqueness without requiring the caller to manage identifiers -- the same pattern databases use for primary keys.

```python
class ADRLog:
    def __init__(self) -> None:
        self._adrs: dict[int, ADR] = {}
        self._next_id = 1
        self._observers: list[StatusChangeCallback] = []
        self._change_history: list[dict[str, Any]] = []

    def create(
        self,
        title: str,
        context: str,
        decision: str,
        consequences: str,
        tags: list[str] | None = None,
    ) -> ADR:
        adr = ADR(
            adr_id=self._next_id,
            title=title,
            status=ADRStatus.PROPOSED,
            context=context,
            decision=decision,
            consequences=consequences,
            created_date=datetime.now().isoformat()[:10],
            tags=tags or [],
        )
        self._adrs[adr.adr_id] = adr
        self._next_id += 1
        return adr
```

Notice that `create()` always sets the initial status to `PROPOSED`. This enforces the lifecycle: you cannot create an ADR that is already accepted. Every decision starts as a proposal.

**Predict:** What would happen if two threads called `create()` at the same time? Is `self._next_id += 1` safe in a concurrent context?

## Step 3: Implement Status Transitions with Observer Notifications

**What to do:** Write `update_status()` that changes an ADR's status and notifies all registered observer callbacks. Write `on_status_change()` to register observers.

**Why:** The Observer pattern decouples the ADR log from whatever needs to react to changes. The log does not need to know about Slack notifications, audit databases, or CI pipelines -- it just calls the registered callbacks. New integrations are added by registering a new observer, not by modifying the log.

```python
StatusChangeCallback = Callable[[ADR, ADRStatus, ADRStatus], None]

def on_status_change(self, callback: StatusChangeCallback) -> None:
    self._observers.append(callback)

def update_status(self, adr_id: int, new_status: ADRStatus) -> ADR:
    adr = self._adrs.get(adr_id)
    if adr is None:
        raise KeyError(f"ADR {adr_id} not found")
    old_status = adr.status
    adr.status = new_status

    change = {
        "adr_id": adr_id,
        "from": old_status.value,
        "to": new_status.value,
        "title": adr.title,
    }
    self._change_history.append(change)

    for observer in self._observers:
        observer(adr, old_status, new_status)

    return adr
```

The callback signature `(adr, old_status, new_status)` gives observers everything they need: which ADR changed, what its previous status was, and what it changed to. This is richer than a simple event flag.

**Predict:** If an observer callback raises an exception, what happens to the remaining observers in the list? Does the status change still stick?

## Step 4: Add Supersede Logic and Search

**What to do:** Write `supersede()` to link old and new ADRs, and `search()` for full-text search across all text fields.

**Why:** Superseding creates an explicit audit chain: "We used to do X (ADR-1), now we do Y (ADR-3) because Z." Without this chain, someone reading ADR-1 would not know it was replaced. Full-text search makes the log useful at scale -- when you have 50 ADRs, you need to find the one about "GraphQL" without scanning them all manually.

```python
def supersede(self, old_id: int, new_id: int) -> None:
    old_adr = self._adrs.get(old_id)
    new_adr = self._adrs.get(new_id)
    if not old_adr:
        raise KeyError(f"ADR {old_id} not found")
    if not new_adr:
        raise KeyError(f"ADR {new_id} not found")
    old_adr.superseded_by = new_id
    self.update_status(old_id, ADRStatus.SUPERSEDED)

def search(self, query: str) -> list[ADR]:
    q = query.lower()
    return [
        adr for adr in self._adrs.values()
        if q in adr.title.lower()
        or q in adr.context.lower()
        or q in adr.decision.lower()
        or q in adr.consequences.lower()
    ]
```

Notice that `supersede()` calls `update_status()` internally, which means observers are automatically notified of the superseding event. This is the power of composition -- the supersede operation reuses the existing notification pipeline.

**Predict:** The search is case-insensitive because both the query and the fields are lowercased. What is the performance cost of this approach for a log with 10,000 ADRs? What data structure would improve search performance?

## Step 5: Build the Summary and Demo

**What to do:** Write `summary()` to aggregate ADR counts by status, and `run_demo()` to demonstrate the full lifecycle: create three ADRs, accept them, supersede one with another.

**Why:** The summary provides a dashboard view of the decision log -- how many decisions are proposed, accepted, deprecated. The demo proves the system works end-to-end and serves as living documentation for how to use the API.

```python
def summary(self) -> dict[str, Any]:
    by_status: dict[str, int] = {}
    for adr in self._adrs.values():
        by_status[adr.status.value] = by_status.get(adr.status.value, 0) + 1
    return {
        "total": self.count,
        "by_status": by_status,
        "recent": [a.to_dict() for a in self.all()[-5:]],
    }
```

The demo creates three ADRs about database and API choices, then demonstrates a realistic scenario: the team initially chose REST (ADR-2), but later decided to migrate to GraphQL (ADR-3), so ADR-2 is superseded by ADR-3.

**Predict:** After the demo runs, what status does ADR-2 have? What value does `adr2.superseded_by` hold?

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| Using a raw list instead of a dict for storage | Lists are simpler but require O(n) lookup by ID | Use `dict[int, ADR]` for O(1) access |
| Forgetting `field(default_factory=list)` for tags | Using `tags: list = []` shares one list across all instances | Always use `field(default_factory=...)` for mutable defaults |
| Observer exception kills the status update | Not wrapping observer calls in try/except | Wrap each callback in try/except so one bad observer cannot break the system |
| Allowing invalid status transitions | No validation on `update_status()` | Add a transition map (e.g., deprecated ADRs cannot be superseded) |
| `json.dumps()` fails on enum values | Passing `ADRStatus.ACCEPTED` instead of `ADRStatus.ACCEPTED.value` | Always use `.value` when serializing enums to JSON |

## Testing Your Solution

```bash
pytest -q
```

Expected output:
```text
7 passed
```

Test from the command line:

```bash
python project.py --demo
```

You should see JSON output showing three ADRs, with status counts, search results for "graphql", observer notifications, and the change history.

## What You Learned

- **Architecture Decision Records (ADRs)** capture the context, decision, and consequences of significant choices. They create institutional memory that prevents teams from repeating past mistakes or reversing decisions without understanding the original constraints.
- **The Observer pattern** decouples event producers from consumers. The ADR log notifies callbacks without knowing what they do -- enabling audit trails, Slack alerts, and CI integrations through simple function registration.
- **Enum-based lifecycles** prevent invalid states at the type level. Using `ADRStatus` instead of raw strings means the Python type checker and your IDE catch typos before runtime.
