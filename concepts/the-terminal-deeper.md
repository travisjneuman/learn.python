# The Terminal — Going Deeper

This builds on [00_COMPUTER_LITERACY_PRIMER.md](../00_COMPUTER_LITERACY_PRIMER.md). Here we cover pipes, redirects, environment variables, and other terminal skills you need for real development.

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

## Related exercises

- [Level 00, Exercise 01 — First Steps](../projects/level-00-absolute-beginner/01-first-steps/) (basic terminal)
- [Module 02 — CLI Tools](../projects/modules/02-cli-tools/) (building terminal programs)
- [Module 09 — Docker](../projects/modules/09-docker-deployment/) (Docker CLI commands)
