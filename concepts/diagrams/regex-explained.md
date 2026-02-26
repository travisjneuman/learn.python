# Diagrams: Regex Explained

[Back to concept](../regex-explained.md)

---

## Regex Engine Matching Flow

How the regex engine processes a pattern against a string, step by step.

```mermaid
flowchart TD
    INPUT["Input: text = 'hello 42 world'<br/>Pattern: r'\\d+'"] --> START["Engine starts at position 0"]

    START --> POS0{"Position 0: 'h'<br/>Matches \\d?"}
    POS0 -->|"No"| POS1{"Position 1: 'e'<br/>Matches \\d?"}
    POS1 -->|"No"| POS2{"...skip to position 6"}
    POS2 -->|"No matches at 2-5"| POS6{"Position 6: '4'<br/>Matches \\d?"}
    POS6 -->|"Yes!"| EXTEND{"Position 7: '2'<br/>Matches \\d+ (more)?"}
    EXTEND -->|"Yes!"| EXTEND2{"Position 8: ' '<br/>Matches \\d+ (more)?"}
    EXTEND2 -->|"No — stop"| MATCH["Match found!<br/>'42' at positions 6-7"]

    MATCH --> MODE{"Which function?"}
    MODE -->|"search()"| RETURN_FIRST["Return first match: '42'"]
    MODE -->|"findall()"| CONTINUE["Continue scanning<br/>from position 8..."]
    MODE -->|"match()"| NO_MATCH["No match<br/>(string doesn't start with \\d)"]

    style INPUT fill:#cc5de8,stroke:#9c36b5,color:#fff
    style MATCH fill:#51cf66,stroke:#27ae60,color:#fff
    style RETURN_FIRST fill:#51cf66,stroke:#27ae60,color:#fff
    style NO_MATCH fill:#ff6b6b,stroke:#c92a2a,color:#fff
```

## Character Class Hierarchy

How regex character classes relate to each other, from specific to general.

```mermaid
flowchart TD
    DOT[". (dot)<br/>Any character except newline"] --> WORD["\\w — Word characters<br/>Letters + Digits + Underscore"]

    WORD --> ALPHA["[a-zA-Z]<br/>Letters only"]
    WORD --> DIGIT["\\d — Digits<br/>[0-9]"]
    WORD --> UNDER["[_]<br/>Underscore"]

    DOT --> SPACE["\\s — Whitespace<br/>Space, tab, newline"]
    DOT --> PUNCT["[^\\w\\s]<br/>Punctuation and symbols"]

    subgraph NEGATIONS ["Negated Classes"]
        ND["\\D — NOT a digit<br/>Same as [^0-9]"]
        NW["\\W — NOT a word char<br/>Same as [^a-zA-Z0-9_]"]
        NS["\\S — NOT whitespace<br/>Same as [^ \\t\\n\\r]"]
    end

    subgraph CUSTOM ["Custom Classes"]
        CC1["[aeiou] — Vowels only"]
        CC2["[A-Fa-f0-9] — Hex digits"]
        CC3["[^aeiou] — NOT vowels"]
    end

    style DOT fill:#cc5de8,stroke:#9c36b5,color:#fff
    style WORD fill:#4a9eff,stroke:#2670c2,color:#fff
    style DIGIT fill:#51cf66,stroke:#27ae60,color:#fff
    style SPACE fill:#ff922b,stroke:#e8590c,color:#fff
    style NEGATIONS fill:#ff6b6b,stroke:#c92a2a,color:#fff
    style CUSTOM fill:#ffd43b,stroke:#f59f00,color:#000
```

## Common Pattern Decision Tree

Not sure which regex pattern to use? Follow this flowchart.

```mermaid
flowchart TD
    START["What are you matching?"] --> Q1{"Digits?"}

    Q1 -->|"Yes"| Q1A{"How many?"}
    Q1A -->|"Any amount"| D_PLUS["\\d+"]
    Q1A -->|"Exact count"| D_EXACT["\\d{3} (exactly 3)"]
    Q1A -->|"Range"| D_RANGE["\\d{2,4} (2 to 4)"]

    Q1 -->|"No"| Q2{"Words/letters?"}
    Q2 -->|"Yes"| Q2A{"Include digits<br/>and underscore?"}
    Q2A -->|"Yes"| W_PLUS["\\w+"]
    Q2A -->|"Letters only"| ALPHA_PLUS["[a-zA-Z]+"]

    Q2 -->|"No"| Q3{"Specific format?"}
    Q3 -->|"Email"| EMAIL["[\\w.+-]+@[\\w-]+\\.[\\w.]+"]
    Q3 -->|"Date"| DATE["\\d{4}-\\d{2}-\\d{2}"]
    Q3 -->|"Phone"| PHONE["\\d{3}[-.]\\d{3}[-.]\\d{4}"]
    Q3 -->|"IP address"| IP["\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}"]

    Q3 -->|"No"| Q4{"Boundaries?"}
    Q4 -->|"Start of string"| CARET["^pattern"]
    Q4 -->|"End of string"| DOLLAR["pattern$"]
    Q4 -->|"Whole word"| BOUNDARY["\\bword\\b"]
    Q4 -->|"Entire string"| FULL["^pattern$"]

    style D_PLUS fill:#51cf66,stroke:#27ae60,color:#fff
    style D_EXACT fill:#51cf66,stroke:#27ae60,color:#fff
    style D_RANGE fill:#51cf66,stroke:#27ae60,color:#fff
    style W_PLUS fill:#4a9eff,stroke:#2670c2,color:#fff
    style ALPHA_PLUS fill:#4a9eff,stroke:#2670c2,color:#fff
    style EMAIL fill:#cc5de8,stroke:#9c36b5,color:#fff
    style DATE fill:#cc5de8,stroke:#9c36b5,color:#fff
    style PHONE fill:#cc5de8,stroke:#9c36b5,color:#fff
    style IP fill:#cc5de8,stroke:#9c36b5,color:#fff
```

## Greedy vs Lazy Matching

By default, quantifiers are greedy (match as much as possible). Adding `?` makes them lazy (match as little as possible).

```mermaid
flowchart TD
    INPUT["Text: '&lt;b&gt;bold&lt;/b&gt; and &lt;b&gt;more&lt;/b&gt;'<br/>Pattern: &lt;b&gt;.*&lt;/b&gt;"]

    INPUT --> GREEDY["Greedy: .*<br/>Match as MUCH as possible"]
    INPUT --> LAZY["Lazy: .*?<br/>Match as LITTLE as possible"]

    GREEDY --> G_RESULT["'&lt;b&gt;bold&lt;/b&gt; and &lt;b&gt;more&lt;/b&gt;'<br/>Grabs everything between first &lt;b&gt;<br/>and LAST &lt;/b&gt;"]

    LAZY --> L_RESULT["'&lt;b&gt;bold&lt;/b&gt;'<br/>Stops at the FIRST &lt;/b&gt;<br/>it finds"]

    subgraph RULE ["The Rule"]
        R1["* + ? {} → Greedy by default"]
        R2["*? +? ?? {}? → Add ? for lazy"]
    end

    style GREEDY fill:#ff6b6b,stroke:#c92a2a,color:#fff
    style LAZY fill:#51cf66,stroke:#27ae60,color:#fff
    style G_RESULT fill:#ff6b6b,stroke:#c92a2a,color:#fff
    style L_RESULT fill:#51cf66,stroke:#27ae60,color:#fff
    style RULE fill:#4a9eff,stroke:#2670c2,color:#fff
```
