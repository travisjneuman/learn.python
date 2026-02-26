# Diagrams: Reading Error Messages

[Back to concept](../reading-error-messages.md)

---

## Traceback Anatomy

Python error messages read from **bottom to top**. The last line tells you WHAT happened. The lines above tell you WHERE.

```mermaid
flowchart TD
    subgraph "Read the traceback bottom-to-top"
        LINE1["Traceback (most recent call last):"]
        LINE2["  File &quot;main.py&quot;, line 10, in main"]
        LINE3["    result = calculate(x, y)"]
        LINE4["  File &quot;math_utils.py&quot;, line 5, in calculate"]
        LINE5["    return x / y"]
        LINE6["ZeroDivisionError: division by zero"]
    end

    LINE6 --> WHAT["WHAT happened?<br/>ZeroDivisionError<br/>You divided by zero"]
    LINE5 --> WHERE_EXACT["WHERE exactly?<br/>Line: return x / y<br/>y must be 0"]
    LINE4 --> WHERE_FILE["WHICH file?<br/>math_utils.py, line 5<br/>in function calculate"]
    LINE2 --> WHO_CALLED["WHO called it?<br/>main.py, line 10<br/>in function main"]

    style LINE6 fill:#ff6b6b,stroke:#c0392b,color:#fff
    style LINE5 fill:#ffd43b,stroke:#f59f00,color:#000
    style LINE4 fill:#4a9eff,stroke:#2670c2,color:#fff
    style LINE2 fill:#51cf66,stroke:#27ae60,color:#fff
    style WHAT fill:#ff6b6b,stroke:#c0392b,color:#fff
```

## Common Error Types: Quick Diagnosis

When you see an error, match the type to its most likely cause.

```mermaid
flowchart TD
    ERR{"What error<br/>type did<br/>you get?"}

    ERR --> NAME["NameError"]
    NAME --> NAME_FIX["Did you spell the<br/>variable name right?<br/>Is it defined above<br/>this line?"]

    ERR --> TYPE["TypeError"]
    TYPE --> TYPE_FIX["Are you mixing types?<br/>&quot;5&quot; + 3 does not work.<br/>Did you call a<br/>non-function?"]

    ERR --> VALUE["ValueError"]
    VALUE --> VALUE_FIX["Right type but<br/>wrong content.<br/>int(&quot;hello&quot;) fails<br/>because &quot;hello&quot; is<br/>not a number."]

    ERR --> INDEX["IndexError"]
    INDEX --> INDEX_FIX["List too short.<br/>You asked for<br/>item 5 but only<br/>have 3 items."]

    ERR --> KEY["KeyError"]
    KEY --> KEY_FIX["Dict key missing.<br/>Check spelling.<br/>Use .get() to<br/>avoid crashes."]

    ERR --> SYNTAX["SyntaxError"]
    SYNTAX --> SYNTAX_FIX["Python cannot parse<br/>your code at all.<br/>Missing : or )<br/>or bad indentation."]

    ERR --> ATTR["AttributeError"]
    ATTR --> ATTR_FIX["That object does not<br/>have that method.<br/>Check the type with<br/>type(your_variable)."]

    style NAME fill:#4a9eff,stroke:#2670c2,color:#fff
    style TYPE fill:#ff922b,stroke:#e8590c,color:#fff
    style VALUE fill:#cc5de8,stroke:#9c36b5,color:#fff
    style INDEX fill:#51cf66,stroke:#27ae60,color:#fff
    style KEY fill:#ffd43b,stroke:#f59f00,color:#000
    style SYNTAX fill:#ff6b6b,stroke:#c0392b,color:#fff
    style ATTR fill:#20c997,stroke:#0ca678,color:#fff
```

## Error Message Reading Checklist

Follow these steps every time you get an error.

```mermaid
flowchart TD
    STEP1["Step 1:<br/>Look at the LAST LINE<br/>What is the error type<br/>and message?"]
    STEP1 --> STEP2["Step 2:<br/>Find the LINE NUMBER<br/>Which line of YOUR code<br/>caused it?"]
    STEP2 --> STEP3["Step 3:<br/>Look at THAT LINE<br/>What does it do?<br/>What values are involved?"]
    STEP3 --> STEP4{"Step 4:<br/>Can you fix it?"}
    STEP4 -->|Yes| FIX["Fix it and run again"]
    STEP4 -->|No| HELP["Add print() above<br/>that line to see<br/>what the values<br/>actually are"]
    HELP --> STEP3

    style STEP1 fill:#ff6b6b,stroke:#c0392b,color:#fff
    style STEP2 fill:#ffd43b,stroke:#f59f00,color:#000
    style STEP3 fill:#4a9eff,stroke:#2670c2,color:#fff
    style FIX fill:#51cf66,stroke:#27ae60,color:#fff
```
