# Diagrams: Collections Explained

[Back to concept](../collections-explained.md)

---

## Side-by-Side Comparison

Each collection type has different properties. Pick the one that fits your needs.

```mermaid
flowchart TD
    subgraph LIST ["list  [1, 2, 3]"]
        L1["Mutable: YES"]
        L2["Ordered: YES"]
        L3["Indexed: YES - items[0]"]
        L4["Duplicates: YES"]
    end

    subgraph TUPLE ["tuple  (1, 2, 3)"]
        T1["Mutable: NO"]
        T2["Ordered: YES"]
        T3["Indexed: YES - items[0]"]
        T4["Duplicates: YES"]
    end

    subgraph DICT ["dict  {'a': 1, 'b': 2}"]
        D1["Mutable: YES"]
        D2["Ordered: YES (3.7+)"]
        D3["Indexed: BY KEY - items['a']"]
        D4["Duplicate keys: NO"]
    end

    subgraph SET ["set  {1, 2, 3}"]
        S1["Mutable: YES"]
        S2["Ordered: NO"]
        S3["Indexed: NO"]
        S4["Duplicates: NO"]
    end

    style LIST fill:#4a9eff,stroke:#2670c2,color:#fff
    style TUPLE fill:#20c997,stroke:#0ca678,color:#fff
    style DICT fill:#ff922b,stroke:#e8590c,color:#fff
    style SET fill:#cc5de8,stroke:#9c36b5,color:#fff
```

## Decision Tree: Which Collection Should I Use?

```mermaid
flowchart TD
    START{"What do you<br/>need to store?"}
    START -->|"Key-value pairs<br/>(name -> value)"| DICT_Q{"Will you<br/>change it?"}
    DICT_Q -->|Yes| DICT["Use a DICT<br/>{&quot;name&quot;: &quot;Alice&quot;}"]
    DICT_Q -->|No| DICT

    START -->|"A group of<br/>unique items"| SET["Use a SET<br/>{&quot;a&quot;, &quot;b&quot;, &quot;c&quot;}"]

    START -->|"An ordered<br/>sequence of items"| SEQ_Q{"Will you need<br/>to change it later?"}
    SEQ_Q -->|"Yes — add, remove,<br/>or change items"| LIST["Use a LIST<br/>[1, 2, 3]"]
    SEQ_Q -->|"No — it should<br/>never change"| TUPLE["Use a TUPLE<br/>(1, 2, 3)"]

    style LIST fill:#4a9eff,stroke:#2670c2,color:#fff
    style TUPLE fill:#20c997,stroke:#0ca678,color:#fff
    style DICT fill:#ff922b,stroke:#e8590c,color:#fff
    style SET fill:#cc5de8,stroke:#9c36b5,color:#fff
```

## How You Access Data in Each Collection

```mermaid
flowchart LR
    subgraph "List / Tuple: By Position"
        LA["items[0]"] --> LV["first item"]
        LB["items[2]"] --> LW["third item"]
        LC["items[-1]"] --> LX["last item"]
    end

    subgraph "Dict: By Key Name"
        DA["person[&quot;name&quot;]"] --> DV["&quot;Alice&quot;"]
        DB["person[&quot;age&quot;]"] --> DW["25"]
    end

    subgraph "Set: No Direct Access"
        SA["Loop through it"] --> SV["for item in my_set:"]
        SB["Check membership"] --> SW["&quot;a&quot; in my_set"]
    end
```
