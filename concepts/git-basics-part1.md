# Git Basics — Part 1: Local Git

[← Back to Overview](./git-basics.md) · [Part 2: Remote Git →](./git-basics-part2.md)

---

Git is a version control system — it tracks every change you make to your code, lets you undo mistakes, and makes it possible for multiple people to work on the same project. This part covers everything you need to work with git locally: init, add, commit, branch, and merge.

## Core concepts

Think of git like a checkpoint system in a video game:

- **Repository (repo)** — your project folder, tracked by git
- **Commit** — a saved checkpoint of your code at a specific moment
- **Branch** — a parallel timeline where you can experiment without affecting the main code
- **Remote** — a copy of your repo on a server (like GitHub)

## Setting up git

```bash
# Check if git is installed:
git --version

# Configure your name and email (do this once):
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

## Starting a repository

```bash
# Option 1: Create a new repo in an existing folder
cd my_project
git init

# Option 2: Clone (download) an existing repo from GitHub
git clone https://github.com/username/repo-name.git
```

## The basic workflow

Git has three areas:

```
Working Directory  →  Staging Area  →  Repository
  (your files)       (ready to save)   (saved history)
     edit              git add          git commit
```

1. **Edit** your files normally
2. **Stage** the changes you want to save: `git add`
3. **Commit** the staged changes with a message: `git commit`

```bash
# 1. Check what has changed:
git status

# 2. Stage specific files:
git add main.py utils.py

# Or stage everything:
git add .

# 3. Commit with a descriptive message:
git commit -m "Add user login function"
```

## Viewing history

```bash
# See commit history:
git log

# Compact one-line history:
git log --oneline

# See what changed in each commit:
git log -p

# See what changed in your working files:
git diff

# See what is staged (ready to commit):
git diff --staged
```

## Undoing things

```bash
# Unstage a file (keep the changes, just remove from staging):
git restore --staged filename.py

# Discard changes to a file (go back to last commit):
git restore filename.py

# Undo the last commit but keep the changes:
git reset --soft HEAD~1

# Change the last commit message:
git commit --amend -m "Better message"
```

## Branches

Branches let you work on features without affecting the main code:

```bash
# See all branches (* marks the current one):
git branch

# Create a new branch:
git branch feature-login

# Switch to it:
git switch feature-login

# Create AND switch in one step:
git switch -c feature-login

# When done, merge back into main:
git switch main
git merge feature-login

# Delete the branch after merging:
git branch -d feature-login
```

## `.gitignore` — files git should not track

Create a file called `.gitignore` in your repo root:

```gitignore
# Python
__pycache__/
*.pyc
.venv/

# IDE files
.vscode/
.idea/

# Environment variables (secrets!)
.env

# OS files
.DS_Store
Thumbs.db

# Build outputs
dist/
build/
*.egg-info/
```

Git will ignore any files matching these patterns. Never commit secrets, virtual environments, or build artifacts.

## Essential commands cheat sheet

| Command | What it does |
|---------|-------------|
| `git init` | Start tracking a folder |
| `git status` | See what has changed |
| `git add <file>` | Stage changes for commit |
| `git commit -m "msg"` | Save a checkpoint |
| `git log --oneline` | View commit history |
| `git diff` | See unstaged changes |
| `git branch` | List branches |
| `git switch -c <name>` | Create and switch to a branch |
| `git merge <branch>` | Merge a branch into current |
| `git restore <file>` | Discard working changes |
| `git stash` | Temporarily shelve changes |

---

| [← Overview](./git-basics.md) | [Part 2: Remote Git →](./git-basics-part2.md) |
|:---|---:|
