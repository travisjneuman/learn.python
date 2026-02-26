"""
Quiz: Git Basics
Review: concepts/git-basics.md
"""

from _quiz_helpers import normalize_answer


def run_quiz():
    print("=" * 60)
    print("  QUIZ: Git Basics")
    print("  Review: concepts/git-basics.md")
    print("=" * 60)
    print()

    score = 0
    total = 12

    # Question 1
    print("Question 1/12: What are the three areas in git's basic workflow?")
    print()
    print("  a) Draft, Review, Published")
    print("  b) Working Directory, Staging Area, Repository")
    print("  c) Local, Cloud, Backup")
    print("  d) Source, Build, Deploy")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! You edit in the Working Directory, stage with 'git add',")
        print("and save to the Repository with 'git commit'.")
    else:
        print("Incorrect. The answer is b).")
        print("Working Directory -> git add -> Staging Area -> git commit -> Repository.")
    print()

    # Question 2
    print("Question 2/12: What does 'git status' show?")
    print()
    print("  a) The commit history")
    print("  b) Which files have been modified, staged, or are untracked")
    print("  c) The remote repository URL")
    print("  d) The current Python version")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! git status shows the current state of your working")
        print("directory and staging area.")
    else:
        print("Incorrect. The answer is b).")
        print("git status shows modified, staged, and untracked files.")
    print()

    # Question 3
    print("Question 3/12: What does 'git add .' do?")
    print()
    print("  a) Creates a new commit")
    print("  b) Stages all changes in the current directory for commit")
    print("  c) Pushes all files to GitHub")
    print("  d) Adds a new remote")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! 'git add .' stages all modified and new files in")
        print("the current directory.")
    else:
        print("Incorrect. The answer is b).")
        print("'git add' moves changes to the staging area. The '.' means")
        print("all files in the current directory.")
    print()

    # Question 4
    print("Question 4/12: What is a branch in git?")
    print()
    print("  a) A copy of the repository on GitHub")
    print("  b) A parallel timeline where you can experiment without")
    print("     affecting the main code")
    print("  c) A backup of your files")
    print("  d) A folder inside the repository")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Branches let you work on features independently")
        print("and merge them back when ready.")
    else:
        print("Incorrect. The answer is b).")
        print("Branches are parallel timelines for independent work.")
    print()

    # Question 5
    print("Question 5/12: What command creates AND switches to a new branch?")
    print()
    print("  a) git branch new-feature")
    print("  b) git switch -c new-feature")
    print("  c) git checkout new-feature")
    print("  d) git create new-feature")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! 'git switch -c' creates a new branch and switches")
        print("to it in one step.")
    else:
        print("Incorrect. The answer is b) git switch -c new-feature.")
        print("'git branch' only creates. 'git switch -c' creates and switches.")
    print()

    # Question 6
    print("Question 6/12: What does 'git log --oneline' show?")
    print()
    print("  a) Only the last commit")
    print("  b) Each commit on a single line with short hash and message")
    print("  c) The full diff of every commit")
    print("  d) Only merge commits")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! --oneline gives a compact view with short hash")
        print("and commit message on each line.")
    else:
        print("Incorrect. The answer is b).")
        print("--oneline gives a compact one-line-per-commit history view.")
    print()

    # Question 7
    print("Question 7/12: What does 'git restore --staged filename.py' do?")
    print()
    print("  a) Deletes the file")
    print("  b) Unstages the file (removes from staging but keeps changes)")
    print("  c) Discards all changes to the file")
    print("  d) Renames the file")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! --staged removes the file from the staging area")
        print("but your changes remain in the working directory.")
    else:
        print("Incorrect. The answer is b).")
        print("Without --staged, git restore discards changes. With --staged,")
        print("it only unstages.")
    print()

    # Question 8
    print("Question 8/12: What should you put in .gitignore?")
    print()
    print("  a) Your Python source files")
    print("  b) Files git should NOT track: __pycache__, .venv, .env, etc.")
    print("  c) Your README")
    print("  d) Test files")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! .gitignore lists patterns for files git should ignore:")
        print("build artifacts, virtual environments, secrets, and OS files.")
    else:
        print("Incorrect. The answer is b).")
        print("Never commit __pycache__, .venv, .env, or IDE config files.")
    print()

    # Question 9
    print("Question 9/12: What makes a commit message 'good'?")
    print()
    print("  a) It is as short as possible, like 'fix'")
    print("  b) It describes WHAT changed and WHY, like")
    print("     'Fix off-by-one error in pagination'")
    print("  c) It includes the date and time")
    print("  d) It lists every file that changed")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Good commit messages describe the change clearly.")
        print("Your future self will thank you.")
    else:
        print("Incorrect. The answer is b).")
        print("Descriptive messages like 'Fix off-by-one error in pagination'")
        print("are much more useful than 'fix' or 'stuff'.")
    print()

    # Question 10
    print("Question 10/12: What happens if you accidentally commit a secret")
    print("(API key) to git?")
    print()
    print("  a) Just delete the file and commit again — it is gone")
    print("  b) The secret lives in git history forever — you must rotate")
    print("     (change) the exposed credentials")
    print("  c) Git automatically encrypts secrets")
    print("  d) Nothing — git ignores sensitive data")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Git history is permanent. Deleting the file does not")
        print("remove it from old commits. Always rotate exposed credentials.")
    else:
        print("Incorrect. The answer is b).")
        print("Secrets in git history can always be found. Prevention (.gitignore)")
        print("is key, and exposed credentials must be changed immediately.")
    print()

    # Question 11
    print("Question 11/12: What does 'git pull' do?")
    print()
    print("  a) Pushes your code to the remote")
    print("  b) Downloads changes from the remote and merges them")
    print("  c) Creates a pull request")
    print("  d) Pulls a specific file from another branch")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! git pull fetches changes from the remote repository")
        print("and merges them into your current branch.")
    else:
        print("Incorrect. The answer is b).")
        print("git pull = git fetch + git merge. It syncs your local branch")
        print("with the remote.")
    print()

    # Question 12
    print("Question 12/12: In a merge conflict, what do the <<<<<<< and")
    print(">>>>>>> markers show?")
    print()
    print("  a) Syntax errors in the code")
    print("  b) The conflicting versions from each branch — you must choose")
    print("     which to keep")
    print("  c) Comments added by git")
    print("  d) Files that should be deleted")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! The markers show both versions. You edit the file to")
        print("keep the right code, remove the markers, then stage and commit.")
    else:
        print("Incorrect. The answer is b).")
        print("Resolve conflicts by choosing which changes to keep, removing")
        print("the markers, and committing the result.")
    print()

    # Final score
    print("=" * 60)
    pct = round(score / total * 100)
    print(f"  Final Score: {score}/{total} ({pct}%)")
    print()
    if pct == 100:
        print("  Perfect! You understand git fundamentals.")
    elif pct >= 70:
        print("  Good work! Review the questions you missed.")
    else:
        print("  Keep practicing! Re-read concepts/git-basics.md")
        print("  and try again.")
    print("=" * 60)


if __name__ == "__main__":
    run_quiz()
