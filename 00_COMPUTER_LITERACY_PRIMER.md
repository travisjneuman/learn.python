# 00 - Computer Literacy Primer
Home: [README](./README.md)

Read this before anything else if you have never programmed before. If you already know what a terminal is and have used a text editor, skip to [01_ROADMAP.md](./01_ROADMAP.md).

## What is programming?

Programming is writing instructions for a computer to follow. That is it.

A computer does not think. It does not guess. It reads your instructions one at a time, from top to bottom, and does exactly what you said. If you give it good instructions, it produces useful results. If you give it bad instructions, it tells you what went wrong (this is called an "error message" and they are helpful, not scary).

Python is one language you can use to write those instructions. It was designed to be readable and beginner-friendly. It is also used professionally by engineers at every major company.

## What is a file?

A file is a container for data stored on your computer. Every document, photo, song, and program is a file.

Files have names and extensions. The extension is the part after the dot:
- `report.docx` — a Word document
- `photo.jpg` — an image
- `hello.py` — a Python script

The `.py` extension tells your computer "this is a Python file." When you write Python code, you will create `.py` files.

## What is a folder (directory)?

A folder is a container for files. Folders can contain other folders. This creates a tree structure:

```
my_computer/
    Documents/
        report.docx
        budget.xlsx
    Projects/
        learn_python/
            hello.py
            exercise.py
```

The "path" is the address of a file or folder. It tells the computer exactly where to find something:
- Windows: `C:\Users\Travis\Projects\learn_python\hello.py`
- Mac/Linux: `/Users/Travis/Projects/learn_python/hello.py`

## What is a text editor?

A text editor is a program for writing plain text files. It is different from Microsoft Word:
- Word saves formatted text (bold, fonts, margins) — computers cannot run this as code
- A text editor saves plain text — just characters, no formatting

**VS Code** (Visual Studio Code) is the text editor recommended in this course. It is free, made by Microsoft, and specifically designed for writing code. It highlights your code in different colors to make it easier to read, catches mistakes as you type, and has a built-in terminal.

Other text editors you may hear about: Sublime Text, Notepad++, Vim. They all work. VS Code is the easiest to start with.

## What is a terminal?

The terminal (also called "command line" or "command prompt") is a text-based way to talk to your computer. Instead of clicking icons and menus, you type commands.

It looks like this:
```
C:\Users\Travis> _
```

The blinking cursor means the terminal is waiting for you to type a command.

### How to open the terminal

**Windows:**
- Press the Windows key, type "PowerShell", click "Windows PowerShell"
- Or: press the Windows key, type "cmd", click "Command Prompt"
- Or: in VS Code, press Ctrl+` (backtick, the key above Tab)

**Mac:**
- Press Cmd+Space, type "Terminal", press Enter
- Or: in VS Code, press Ctrl+` (backtick)

**Linux:**
- Press Ctrl+Alt+T (on most distributions)
- Or: in VS Code, press Ctrl+`

### Basic terminal commands

You only need a few commands to start:

| Command | What it does | Example |
|---------|-------------|---------|
| `cd` | Change directory (go to a folder) | `cd Projects` |
| `ls` (Mac/Linux) or `dir` (Windows) | List files in current folder | `ls` |
| `python` | Start Python interactive mode | `python` |
| `python file.py` | Run a Python file | `python hello.py` |
| `exit()` | Leave Python interactive mode | `exit()` |

When you type `cd Projects`, you are telling the computer "move into the Projects folder." When you type `python hello.py`, you are saying "run the file hello.py using Python."

## What does "running code" mean?

When you "run" a Python file, this happens:

1. You type `python hello.py` in the terminal
2. The Python program reads your file from top to bottom
3. It executes each instruction one at a time
4. If an instruction produces output (like `print("Hello")`), you see it in the terminal
5. When it reaches the end of the file, it stops

That is it. Your file does not change. The computer just read it and followed the instructions.

## What is an error message?

When Python cannot understand or execute your instructions, it shows an error message. Error messages are not punishment — they are Python telling you exactly what went wrong and where.

Example:
```
File "hello.py", line 3
    print("Hello)
                ^
SyntaxError: unterminated string literal
```

This tells you:
- The problem is in `hello.py`, line 3
- The `^` points to where Python got confused
- `SyntaxError: unterminated string literal` means you forgot to close a quote

Read error messages carefully. They almost always tell you what to fix.

## What you need to remember

1. A program is a file full of instructions
2. Python reads those instructions top to bottom
3. The terminal is where you tell the computer to run your program
4. Errors are helpful clues, not failures
5. You do not need to memorize anything — understanding the pattern is enough

## Next
Go to [01_ROADMAP.md](./01_ROADMAP.md).
