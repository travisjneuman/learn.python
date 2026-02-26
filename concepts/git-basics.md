# Git Basics

Git is a version control system — it tracks every change you make to your code, lets you undo mistakes, and makes it possible for multiple people to work on the same project without overwriting each other's work. Every professional developer uses git daily.

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize |
|:---: | :---: | :---: | :---: | :---: | :---:|
| **You are here** | [Projects](#practice) | — | [Quiz](quizzes/git-basics-quiz.py) | [Flashcards](../practice/flashcards/README.md) | — |

<!-- modality-hub-end -->

## Why This Matters

Without version control, you end up with folders named `project_final`, `project_final_v2`, `project_ACTUALLY_final`. Git replaces all of that with a clean history of changes. It also makes it safe to experiment — you can always go back to a working version.

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

## Working with remotes (GitHub)

A **remote** is a copy of your repo on a server. GitHub is the most popular host.

```bash
# Add a remote (usually done once):
git remote add origin https://github.com/username/repo-name.git

# Push your code to GitHub:
git push origin main

# After the first push, you can just use:
git push

# Download changes from GitHub:
git pull

# See your remotes:
git remote -v
```

## The GitHub workflow

1. **Fork** the repo on GitHub (creates your own copy)
2. **Clone** your fork locally: `git clone <your-fork-url>`
3. **Create a branch**: `git switch -c my-feature`
4. **Make changes**, commit them
5. **Push** the branch: `git push origin my-feature`
6. **Open a Pull Request** on GitHub to propose your changes

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

## Resolving merge conflicts

When two branches change the same line, git cannot merge automatically. It marks the conflict:

```python
<<<<<<< HEAD
def greet(name):
    return f"Hello, {name}!"
=======
def greet(name):
    return f"Hi there, {name}!"
>>>>>>> feature-branch
```

To resolve:
1. Open the file and choose which version to keep (or combine them)
2. Remove the `<<<<<<<`, `=======`, and `>>>>>>>` markers
3. Stage and commit the fix:

```bash
git add filename.py
git commit -m "Resolve merge conflict in greet function"
```

## Essential commands cheat sheet

| Command | What it does |
|---------|-------------|
| `git init` | Start tracking a folder |
| `git clone <url>` | Download a repo |
| `git status` | See what has changed |
| `git add <file>` | Stage changes for commit |
| `git commit -m "msg"` | Save a checkpoint |
| `git log --oneline` | View commit history |
| `git diff` | See unstaged changes |
| `git branch` | List branches |
| `git switch -c <name>` | Create and switch to a branch |
| `git merge <branch>` | Merge a branch into current |
| `git push` | Upload commits to remote |
| `git pull` | Download commits from remote |
| `git restore <file>` | Discard working changes |
| `git stash` | Temporarily shelve changes |

## Common Mistakes

**Committing too much at once:**
Each commit should be one logical change. "Add login form" is good. "Add login form, fix CSS, update README, refactor utils" is too much — make separate commits.

**Writing bad commit messages:**
```bash
# BAD:
git commit -m "fix"
git commit -m "stuff"
git commit -m "asdfg"

# GOOD:
git commit -m "Fix off-by-one error in pagination"
git commit -m "Add password validation to signup form"
```

**Committing secrets:**
```bash
# NEVER do this:
git add .env              # Contains API keys and passwords!
git add credentials.json  # Contains service account keys!
```

Add these to `.gitignore` BEFORE your first commit. If you accidentally commit secrets, they are in the history forever (even if you delete the file later). You must rotate (change) the exposed credentials.

**Forgetting to pull before pushing:**
```bash
git push    # Rejected! Remote has changes you do not have.
git pull    # Download remote changes first
git push    # Now it works
```

## Practice

- Every project in this curriculum uses git — practice with each one
- [Level 0 projects](../projects/level-0/) — start committing your work
- [Module 09 Docker Deployment](../projects/modules/09-docker-deployment/) — git + CI/CD

**Review:** [Flashcard decks](../practice/flashcards/README.md)
**Practice reps:** [Coding challenges](../practice/challenges/README.md)

## Further Reading

- [Git documentation](https://git-scm.com/doc)
- [GitHub's Git Handbook](https://docs.github.com/en/get-started/using-git/about-git)
- [Pro Git book (free)](https://git-scm.com/book/en/v2)

---

| [← Prev](reading-documentation.md) | [Home](../README.md) | [Next →](security-basics.md) |
|:---|:---:|---:|
