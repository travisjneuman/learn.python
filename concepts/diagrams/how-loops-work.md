# Diagrams: How Loops Work

[Back to concept](../how-loops-work.md)

---

## For Loop Flowchart

A `for` loop walks through each item in a sequence, one at a time.

```mermaid
flowchart TD
    START(["Start"]) --> INIT["Get the sequence<br/>(list, range, string, etc.)"]
    INIT --> CHECK{"Any items<br/>left?"}
    CHECK -->|Yes| ASSIGN["Assign next item<br/>to loop variable"]
    ASSIGN --> BODY["Run the loop body"]
    BODY --> CHECK
    CHECK -->|No| END(["Done — continue<br/>after the loop"])
```

## While Loop Flowchart

A `while` loop keeps running as long as its condition is `True`.

```mermaid
flowchart TD
    START(["Start"]) --> CHECK{"Is condition<br/>True?"}
    CHECK -->|Yes| BODY["Run the loop body"]
    BODY --> UPDATE["Update something<br/>(or you loop forever!)"]
    UPDATE --> CHECK
    CHECK -->|No| END(["Done — continue<br/>after the loop"])

    style UPDATE fill:#ffd43b,stroke:#f59f00,color:#000
```

## Break and Continue Flow

`break` exits the loop entirely. `continue` skips to the next iteration.

```mermaid
flowchart TD
    START(["Loop starts"]) --> CHECK{"More items?"}
    CHECK -->|Yes| BODY["Run loop body"]
    BODY --> HIT_CONTINUE{"Hit<br/>continue?"}
    HIT_CONTINUE -->|Yes| CHECK
    HIT_CONTINUE -->|No| HIT_BREAK{"Hit<br/>break?"}
    HIT_BREAK -->|Yes| EXIT(["Exit loop<br/>immediately"])
    HIT_BREAK -->|No| CHECK
    CHECK -->|No| END(["Loop finished<br/>normally"])

    style EXIT fill:#ff6b6b,stroke:#c0392b,color:#fff
    style HIT_CONTINUE fill:#51cf66,stroke:#27ae60,color:#fff
```

## Decision Tree: For vs While

```mermaid
flowchart TD
    Q1{"Do you know<br/>how many times<br/>to repeat?"}
    Q1 -->|"Yes — I have a list,<br/>range, or fixed count"| FOR["Use a FOR loop<br/>for item in sequence:"]
    Q1 -->|"No — I repeat until<br/>something happens"| WHILE["Use a WHILE loop<br/>while condition:"]
    FOR --> EX1["Example:<br/>for name in names:<br/>    print(name)"]
    WHILE --> EX2["Example:<br/>while guess != answer:<br/>    guess = input()"]

    style FOR fill:#4a9eff,stroke:#2670c2,color:#fff
    style WHILE fill:#ff6b6b,stroke:#c0392b,color:#fff
```
