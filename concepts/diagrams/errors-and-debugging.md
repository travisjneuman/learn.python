# Diagrams: Errors and Debugging

[Back to concept](../errors-and-debugging.md)

---

## Exception Hierarchy

Python errors form a family tree. Catching a parent catches all its children too.

```mermaid
flowchart TD
    BASE["BaseException<br/>(do not catch this)"]
    BASE --> KBI["KeyboardInterrupt<br/>Ctrl+C pressed"]
    BASE --> SYS["SystemExit<br/>Program told to quit"]
    BASE --> EXC["Exception<br/>(catch this one)"]

    EXC --> VAL["ValueError<br/>Right type,<br/>wrong value"]
    EXC --> TYPE["TypeError<br/>Wrong type<br/>entirely"]
    EXC --> NAME["NameError<br/>Name not<br/>found"]
    EXC --> IDX["IndexError<br/>List index<br/>out of range"]
    EXC --> KEY["KeyError<br/>Dict key<br/>not found"]
    EXC --> ATTR["AttributeError<br/>Object has no<br/>such attribute"]
    EXC --> FILE["FileNotFoundError<br/>File does<br/>not exist"]
    EXC --> ZERO["ZeroDivisionError<br/>Divided<br/>by zero"]
    EXC --> IMPORT["ImportError<br/>Module not<br/>found"]
    EXC --> SYNTAX["SyntaxError<br/>Code is not<br/>valid Python"]

    style BASE fill:#888,stroke:#666,color:#fff
    style EXC fill:#4a9eff,stroke:#2670c2,color:#fff
    style SYNTAX fill:#ff6b6b,stroke:#c0392b,color:#fff
```

## Try / Except / Else / Finally Flow

```mermaid
flowchart TD
    START(["Start"]) --> TRY["TRY block<br/>Run the risky code"]
    TRY --> ERR{"Did an<br/>error happen?"}

    ERR -->|"Yes"| EXCEPT["EXCEPT block<br/>Handle the error"]
    ERR -->|"No"| ELSE["ELSE block<br/>Runs only if<br/>NO error happened"]

    EXCEPT --> FINALLY["FINALLY block<br/>ALWAYS runs<br/>(cleanup goes here)"]
    ELSE --> FINALLY

    FINALLY --> END(["Continue program"])

    style TRY fill:#4a9eff,stroke:#2670c2,color:#fff
    style EXCEPT fill:#ff6b6b,stroke:#c0392b,color:#fff
    style ELSE fill:#51cf66,stroke:#27ae60,color:#fff
    style FINALLY fill:#ffd43b,stroke:#f59f00,color:#000
```

## Debugging Decision Tree: What Kind of Error?

```mermaid
flowchart TD
    START{"Your program<br/>has a problem"}

    START -->|"Red error<br/>message appears"| RUNTIME["RUNTIME ERROR<br/>Program crashed"]
    START -->|"No error, but<br/>wrong output"| LOGIC["LOGIC ERROR<br/>Code runs but<br/>does the wrong thing"]
    START -->|"Error before<br/>code even runs"| SYNTAX["SYNTAX ERROR<br/>Python cannot<br/>read your code"]

    SYNTAX --> S1["Check for:<br/>missing colons :<br/>unmatched ( ) [ ]<br/>bad indentation"]

    RUNTIME --> R1["Read the error<br/>message carefully"]
    R1 --> R2["Find the line<br/>number it points to"]
    R2 --> R3["Check: what type<br/>of error is it?"]

    LOGIC --> L1["Add print() statements<br/>to see what values<br/>your variables have"]
    L1 --> L2["Compare expected<br/>vs actual output"]
    L2 --> L3["Find where they<br/>first differ"]

    style RUNTIME fill:#ff6b6b,stroke:#c0392b,color:#fff
    style LOGIC fill:#ffd43b,stroke:#f59f00,color:#000
    style SYNTAX fill:#cc5de8,stroke:#9c36b5,color:#fff
```
