# Diagrams: The Terminal — Going Deeper

[Back to concept](../the-terminal-deeper.md)

---

## Shell Command Pipeline

The pipe `|` connects commands by routing one command's output into the next command's input. Each command runs as a separate process.

```mermaid
flowchart LR
    subgraph CMD1 ["cat access.log"]
        C1_OUT["stdout:<br/>every line of the file"]
    end

    subgraph CMD2 ["grep 'ERROR'"]
        C2_IN["stdin: all lines"]
        C2_WORK["Filter: keep only<br/>lines containing ERROR"]
        C2_OUT["stdout: error lines only"]
        C2_IN --> C2_WORK --> C2_OUT
    end

    subgraph CMD3 ["sort"]
        C3_IN["stdin: error lines"]
        C3_WORK["Sort alphabetically"]
        C3_OUT["stdout: sorted errors"]
        C3_IN --> C3_WORK --> C3_OUT
    end

    subgraph CMD4 ["uniq -c"]
        C4_IN["stdin: sorted errors"]
        C4_WORK["Count consecutive<br/>duplicate lines"]
        C4_OUT["stdout:<br/>3 ERROR timeout<br/>7 ERROR auth failed"]
        C4_IN --> C4_WORK --> C4_OUT
    end

    C1_OUT -->|"pipe"| C2_IN
    C2_OUT -->|"pipe"| C3_IN
    C3_OUT -->|"pipe"| C4_IN

    style CMD1 fill:#cc5de8,stroke:#9c36b5,color:#fff
    style CMD2 fill:#4a9eff,stroke:#2670c2,color:#fff
    style CMD3 fill:#ff922b,stroke:#e8590c,color:#fff
    style CMD4 fill:#51cf66,stroke:#27ae60,color:#fff
```

## Process I/O: stdin, stdout, stderr

Every process has three standard streams. Understanding these is essential for pipes, redirects, and debugging.

```mermaid
flowchart LR
    subgraph INPUT ["Input Sources"]
        KB["Keyboard<br/>(interactive)"]
        PIPE_IN["Pipe from<br/>previous command"]
        FILE_IN["Redirect from file<br/>< input.txt"]
    end

    subgraph PROCESS ["python script.py"]
        STDIN["stdin (fd 0)<br/>input() reads from here"]
        CODE["Your Python Code"]
        STDOUT["stdout (fd 1)<br/>print() writes here"]
        STDERR["stderr (fd 2)<br/>Errors and warnings"]
        STDIN --> CODE
        CODE --> STDOUT
        CODE --> STDERR
    end

    subgraph OUTPUT ["Output Destinations"]
        TERMINAL["Terminal screen<br/>(default)"]
        PIPE_OUT["Pipe to<br/>next command"]
        FILE_OUT["> output.txt<br/>>> append.txt"]
        ERR_FILE["2> errors.txt"]
    end

    KB --> STDIN
    PIPE_IN --> STDIN
    FILE_IN --> STDIN

    STDOUT --> TERMINAL
    STDOUT --> PIPE_OUT
    STDOUT --> FILE_OUT

    STDERR --> TERMINAL
    STDERR --> ERR_FILE

    style INPUT fill:#4a9eff,stroke:#2670c2,color:#fff
    style PROCESS fill:#cc5de8,stroke:#9c36b5,color:#fff
    style OUTPUT fill:#51cf66,stroke:#27ae60,color:#fff
```

## Redirect Operators Cheat Sheet

How each redirect operator routes output to files or other commands.

```mermaid
flowchart TD
    subgraph OPERATORS ["Redirect Operators"]
        direction LR
        O1["> file<br/>Overwrite stdout to file"]
        O2[">> file<br/>Append stdout to file"]
        O3["2> file<br/>Redirect stderr to file"]
        O4["2>&1<br/>Merge stderr into stdout"]
        O5["&> file<br/>Redirect both to file"]
        O6["< file<br/>Read stdin from file"]
    end

    subgraph EXAMPLES ["Common Patterns"]
        E1["python app.py > output.txt 2> errors.txt<br/>Separate stdout and stderr"]
        E2["python app.py &> all.txt<br/>Capture everything"]
        E3["python app.py > /dev/null 2>&1<br/>Silence all output"]
        E4["python app.py < input.txt > output.txt<br/>File in, file out"]
    end

    style OPERATORS fill:#4a9eff,stroke:#2670c2,color:#fff
    style EXAMPLES fill:#ff922b,stroke:#e8590c,color:#fff
```

## Command Chaining Logic

The operators `&&`, `||`, and `;` control whether the next command runs based on the previous command's success or failure.

```mermaid
flowchart TD
    CMD["Run Command A"] --> EXIT{"Exit code?"}

    EXIT -->|"0 (success)"| AND_THEN["&& Command B<br/>Runs only on SUCCESS"]
    EXIT -->|"non-zero (failure)"| OR_THEN["|| Command C<br/>Runs only on FAILURE"]
    EXIT -->|"any"| SEMI["&#59; Command D<br/>Runs REGARDLESS"]

    subgraph EXAMPLES_CHAIN ["Examples"]
        EX1["pytest && echo 'All passed!'<br/>Echo runs only if tests pass"]
        EX2["pytest || echo 'Tests failed!'<br/>Echo runs only if tests fail"]
        EX3["echo 'Start' ; pytest ; echo 'Done'<br/>All three always run"]
        EX4["mkdir build && cd build && cmake ..<br/>Each step depends on the previous"]
    end

    style AND_THEN fill:#51cf66,stroke:#27ae60,color:#fff
    style OR_THEN fill:#ff6b6b,stroke:#c92a2a,color:#fff
    style SEMI fill:#ffd43b,stroke:#f59f00,color:#000
    style EXAMPLES_CHAIN fill:#4a9eff,stroke:#2670c2,color:#fff
```
