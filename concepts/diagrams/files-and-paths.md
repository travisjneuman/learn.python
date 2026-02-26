# Diagrams: Files and Paths

[Back to concept](../files-and-paths.md)

---

## File I/O Flowchart

The safe way to work with files uses a `with` statement, which closes the file automatically.

```mermaid
flowchart TD
    subgraph "WITHOUT with (risky)"
        A1["f = open(&quot;data.txt&quot;)"] --> A2["data = f.read()"]
        A2 --> A3{"Error<br/>happens?"}
        A3 -->|No| A4["f.close()"]
        A3 -->|Yes| A5["FILE LEFT OPEN!<br/>Resource leak"]
        style A5 fill:#ff6b6b,stroke:#c0392b,color:#fff
    end

    subgraph "WITH with (safe)"
        B1["with open(&quot;data.txt&quot;) as f:"] --> B2["data = f.read()"]
        B2 --> B3{"Error<br/>happens?"}
        B3 -->|No| B4["File closed<br/>automatically"]
        B3 -->|Yes| B5["File STILL closed<br/>automatically"]
        style B4 fill:#51cf66,stroke:#27ae60,color:#fff
        style B5 fill:#51cf66,stroke:#27ae60,color:#fff
    end
```

## Path Types: Absolute vs Relative

```mermaid
flowchart TD
    subgraph "Absolute Path (full address)"
        ABS["/home/user/projects/data.txt"]
        ABS_W["C:\Users\user\projects\data.txt"]
        ABS_NOTE["Always starts from the root<br/>Works from anywhere"]
    end

    subgraph "Relative Path (directions from here)"
        REL1["data.txt<br/>(same folder)"]
        REL2["../data.txt<br/>(one folder up)"]
        REL3["sub/data.txt<br/>(inside subfolder)"]
        REL_NOTE["Depends on where<br/>you are right now"]
    end

    CWD["Your current<br/>working directory:<br/>/home/user/projects/"]
    CWD -->|"+ data.txt"| RESULT1["/home/user/projects/data.txt"]
    CWD -->|"+ ../data.txt"| RESULT2["/home/user/data.txt"]
    CWD -->|"+ sub/data.txt"| RESULT3["/home/user/projects/sub/data.txt"]

    style ABS_NOTE fill:#4a9eff,stroke:#2670c2,color:#fff
    style REL_NOTE fill:#ffd43b,stroke:#f59f00,color:#000
```

## File Mode Decision Tree

The `mode` argument in `open()` controls what you can do with the file.

```mermaid
flowchart TD
    START{"What do you<br/>want to do?"}

    START -->|"Read existing<br/>content"| R["mode=&quot;r&quot;<br/>(default)<br/>Read only"]
    START -->|"Write new content<br/>(erase old)"| W["mode=&quot;w&quot;<br/>Write — erases<br/>existing content!"]
    START -->|"Add to the end<br/>(keep old)"| A_MODE["mode=&quot;a&quot;<br/>Append — adds<br/>to the end"]
    START -->|"Create new file<br/>(fail if exists)"| X["mode=&quot;x&quot;<br/>Exclusive create"]

    R --> TEXT_Q{"Text or<br/>binary data?"}
    W --> TEXT_Q
    A_MODE --> TEXT_Q
    X --> TEXT_Q

    TEXT_Q -->|"Text<br/>(words, CSV, JSON)"| TEXT["No extra flag<br/>open(&quot;f.txt&quot;, &quot;r&quot;)"]
    TEXT_Q -->|"Binary<br/>(images, PDFs)"| BIN["Add b<br/>open(&quot;f.png&quot;, &quot;rb&quot;)"]

    style W fill:#ff6b6b,stroke:#c0392b,color:#fff
    style A_MODE fill:#51cf66,stroke:#27ae60,color:#fff
    style R fill:#4a9eff,stroke:#2670c2,color:#fff
    style X fill:#ffd43b,stroke:#f59f00,color:#000
```
