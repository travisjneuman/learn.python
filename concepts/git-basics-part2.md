# Git Basics — Part 2: Remote Git and GitHub

[← Part 1: Local Git](./git-basics-part1.md) · [Back to Overview](./git-basics.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize |
|:---: | :---: | :---: | :---: | :---: | :---:|
| **You are here** | [Projects](#practice) | — | — | [Flashcards](../practice/flashcards/README.md) | — |

<!-- modality-hub-end -->

---

This part covers working with remote repositories on GitHub: pushing, pulling, cloning, the pull request workflow, and resolving merge conflicts.

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

## Remote commands cheat sheet

| Command | What it does |
|---------|-------------|
| `git clone <url>` | Download a repo |
| `git remote add origin <url>` | Link to a remote |
| `git push` | Upload commits to remote |
| `git pull` | Download commits from remote |
| `git remote -v` | Show remote URLs |
| `git push origin <branch>` | Push a specific branch |

---

| [← Part 1: Local Git](./git-basics-part1.md) | [Overview](./git-basics.md) |
|:---|---:|
