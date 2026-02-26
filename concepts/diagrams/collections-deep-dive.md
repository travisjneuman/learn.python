# Diagrams: Collections Deep Dive

[Back to concept](../collections-deep-dive.md)

---

## Collection Type Decision Tree

Use this flowchart to pick the right collection type for your use case.

```mermaid
flowchart TD
    START["What do you need?"] --> Q1{"Need key-value<br/>pairs?"}

    Q1 -->|"Yes"| Q2{"Default values<br/>for missing keys?"}
    Q1 -->|"No"| Q5{"Need to count<br/>items?"}

    Q2 -->|"Yes"| DDICT["defaultdict<br/>Auto-creates missing keys<br/>with a factory function"]
    Q2 -->|"No"| Q3{"Multiple dicts<br/>to search through?"}

    Q3 -->|"Yes"| CHAIN["ChainMap<br/>Layer dicts for lookup<br/>First match wins"]
    Q3 -->|"No"| DICT["Plain dict<br/>Standard key-value store"]

    Q5 -->|"Yes"| COUNTER["Counter<br/>Count occurrences<br/>most_common(), arithmetic"]
    Q5 -->|"No"| Q6{"Need fast add/remove<br/>from both ends?"}

    Q6 -->|"Yes"| DEQUE["deque<br/>O(1) append/pop<br/>from left and right"]
    Q6 -->|"No"| Q7{"Lightweight<br/>immutable record?"}

    Q7 -->|"Yes"| NTUPLE["namedtuple<br/>Like a tuple with<br/>named fields"]
    Q7 -->|"No"| Q8{"Ordered +<br/>equality matters?"}

    Q8 -->|"Yes"| ODICT["OrderedDict<br/>Order-sensitive<br/>equality comparison"]
    Q8 -->|"No"| LIST["Plain list or tuple<br/>Standard sequences"]

    style DDICT fill:#51cf66,stroke:#27ae60,color:#fff
    style CHAIN fill:#4a9eff,stroke:#2670c2,color:#fff
    style COUNTER fill:#cc5de8,stroke:#9c36b5,color:#fff
    style DEQUE fill:#ff922b,stroke:#e8590c,color:#fff
    style NTUPLE fill:#ffd43b,stroke:#f59f00,color:#000
    style ODICT fill:#ff6b6b,stroke:#c92a2a,color:#fff
    style DICT fill:#4a9eff,stroke:#2670c2,color:#fff
    style LIST fill:#ffd43b,stroke:#f59f00,color:#000
```

## Performance Comparison

Big-O time complexity for common operations across collection types.

```mermaid
flowchart TD
    subgraph LIST_OPS ["list"]
        L1["Append: O(1)"]
        L2["Insert at front: O(n)"]
        L3["Pop from end: O(1)"]
        L4["Pop from front: O(n)"]
        L5["Search by value: O(n)"]
        L6["Index access: O(1)"]
    end

    subgraph DEQUE_OPS ["deque"]
        D1["Append right: O(1)"]
        D2["Append left: O(1)"]
        D3["Pop right: O(1)"]
        D4["Pop left: O(1)"]
        D5["Search by value: O(n)"]
        D6["Index access: O(n)"]
    end

    subgraph DICT_OPS ["dict / defaultdict / Counter"]
        DD1["Get by key: O(1)"]
        DD2["Set by key: O(1)"]
        DD3["Delete by key: O(1)"]
        DD4["Check membership: O(1)"]
        DD5["Iterate all: O(n)"]
    end

    subgraph TAKEAWAY ["Key Takeaway"]
        T1["list: best for indexed access"]
        T2["deque: best for queue/stack patterns"]
        T3["dict types: best for key lookup"]
    end

    style LIST_OPS fill:#4a9eff,stroke:#2670c2,color:#fff
    style DEQUE_OPS fill:#ff922b,stroke:#e8590c,color:#fff
    style DICT_OPS fill:#51cf66,stroke:#27ae60,color:#fff
    style TAKEAWAY fill:#cc5de8,stroke:#9c36b5,color:#fff
```

## When to Use Each Collection

A comparison showing the strengths of each collection type through real-world examples.

```mermaid
flowchart LR
    subgraph COUNTER_USE ["Counter"]
        C1["Word frequency in text"]
        C2["Most common log levels"]
        C3["Vote tallying"]
    end

    subgraph DDICT_USE ["defaultdict"]
        DD1["Group items by category"]
        DD2["Build adjacency lists"]
        DD3["Accumulate values by key"]
    end

    subgraph DEQUE_USE ["deque"]
        DQ1["Recent history buffer"]
        DQ2["BFS traversal queue"]
        DQ3["Sliding window"]
    end

    subgraph CHAIN_USE ["ChainMap"]
        CH1["Config: defaults + user + CLI"]
        CH2["Scoped variable lookup"]
        CH3["Template context layers"]
    end

    subgraph NTUPLE_USE ["namedtuple"]
        NT1["Database row records"]
        NT2["API response objects"]
        NT3["Coordinate pairs"]
    end

    style COUNTER_USE fill:#cc5de8,stroke:#9c36b5,color:#fff
    style DDICT_USE fill:#51cf66,stroke:#27ae60,color:#fff
    style DEQUE_USE fill:#ff922b,stroke:#e8590c,color:#fff
    style CHAIN_USE fill:#4a9eff,stroke:#2670c2,color:#fff
    style NTUPLE_USE fill:#ffd43b,stroke:#f59f00,color:#000
```
