# The Terminal — Going Deeper

This builds on [00_COMPUTER_LITERACY_PRIMER.md](../00_COMPUTER_LITERACY_PRIMER.md). Here we cover pipes, redirects, environment variables, and other terminal skills you need for real development.

## Visualize It

See how Python interacts with the operating system via `os` and `sys`:
[Open in Python Tutor](https://pythontutor.com/render.html#code=import%20os%0Aprint%28os.getcwd%28%29%29%0A%0Aimport%20sys%0Aprint%28sys.platform%29%0Aprint%28sys.version_info%5B%3A2%5D%29&cumulative=false&curInstr=0&mode=display&origin=opt-frontend.js&py=3&rawInputLstJSON=%5B%5D)

## Pipes — connecting commands

The `|` (pipe) sends the output of one command into another:

```bash
# Count how many Python files are in the current directory.
ls *.py | wc -l

# Search for "error" in a log file and show only unique lines.
cat app.log | grep "error" | sort | uniq

# Find the 5 largest files.
du -sh * | sort -rh | head -5
```

## Redirects — saving output to files

```bash
# > writes output to a file (overwrites).
python script.py > output.txt

# >> appends to a file.
echo "new line" >> output.txt

# 2> redirects error messages.
python script.py 2> errors.txt

# &> redirects both output and errors.
python script.py &> all_output.txt
```

## Environment variables

Environment variables are values that any program can read. They configure behavior without changing code.

```bash
# Set a variable (current session only).
export DATABASE_URL="sqlite:///my.db"
export API_KEY="abc123"

# Read a variable.
echo $DATABASE_URL

# Use in Python.
python -c "import os; print(os.environ.get('DATABASE_URL'))"
```

### .env files

For development, store variables in a `.env` file:

```
# .env
DATABASE_URL=sqlite:///my.db
API_KEY=abc123
DEBUG=true
```

Load with `python-dotenv`:

```python
from dotenv import load_dotenv
load_dotenv()    # Reads .env into environment variables
```

**Never commit `.env` to git.** Add it to `.gitignore`.

## Useful terminal commands

| Command | What it does | Example |
|---------|-------------|---------|
| `pwd` | Print current directory | `pwd` |
| `ls -la` | List all files with details | `ls -la` |
| `mkdir -p` | Create directory (and parents) | `mkdir -p src/utils` |
| `rm -r` | Delete directory and contents | `rm -r old_folder` |
| `cp -r` | Copy directory | `cp -r src/ backup/` |
| `mv` | Move or rename | `mv old.py new.py` |
| `which` | Find where a command lives | `which python` |
| `history` | Show command history | `history | grep pip` |
| `cat` | Show file contents | `cat requirements.txt` |
| `less` | Page through a file | `less long_file.txt` |
| `grep` | Search in files | `grep "def " *.py` |
| `wc -l` | Count lines | `wc -l data.csv` |

## Process management

```bash
# Run a command in the background.
python server.py &

# See running processes.
ps aux | grep python

# Kill a process by PID.
kill 12345

# Kill by name.
pkill -f "python server.py"
```

## Keyboard shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+C` | Stop the current command |
| `Ctrl+D` | Exit the shell / end input |
| `Ctrl+L` | Clear the screen |
| `Ctrl+R` | Search command history |
| `Tab` | Auto-complete file/command names |
| `↑` / `↓` | Navigate command history |

## Chaining commands

```bash
# && — run next command only if previous succeeded.
python -m pytest && echo "All tests passed!"

# || — run next command only if previous failed.
python -m pytest || echo "Tests failed!"

# ; — run next command regardless.
echo "Starting..." ; python script.py ; echo "Done."
```

## Practice

- [Level 00 / 01 First Steps](../projects/level-00-absolute-beginner/01-first-steps/)
- [Module 02 CLI Tools](../projects/modules/02-cli-tools/)
- [Module 09 Docker Deployment](../projects/modules/09-docker-deployment/)
- [Level 0 / 01 Terminal Hello Lab](../projects/level-0/01-terminal-hello-lab/README.md)
- [Level 0 / 02 Calculator Basics](../projects/level-0/02-calculator-basics/README.md)
- [Level 0 / 03 Temperature Converter](../projects/level-0/03-temperature-converter/README.md)
- [Level 0 / 04 Yes No Questionnaire](../projects/level-0/04-yes-no-questionnaire/README.md)
- [Level 0 / 05 Number Classifier](../projects/level-0/05-number-classifier/README.md)
- [Level 0 / 06 Word Counter Basic](../projects/level-0/06-word-counter-basic/README.md)
- [Level 0 / 07 First File Reader](../projects/level-0/07-first-file-reader/README.md)
- [Level 0 / 08 String Cleaner Starter](../projects/level-0/08-string-cleaner-starter/README.md)
- [Level 0 / 09 Daily Checklist Writer](../projects/level-0/09-daily-checklist-writer/README.md)
- [Level 0 / 10 Duplicate Line Finder](../projects/level-0/10-duplicate-line-finder/README.md)

**Quick check:** [Take the quiz](quizzes/the-terminal-deeper-quiz.py)

**Review:** [Flashcard decks](../practice/flashcards/README.md)
**Practice reps:** [Coding challenges](../practice/challenges/README.md)

---

| [← Prev](errors-and-debugging.md) | [Home](../README.md) | [Next →](../projects/level-0/README.md) |
|:---|:---:|---:|
