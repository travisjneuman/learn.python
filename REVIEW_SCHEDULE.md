# Spaced Repetition Review Schedule

Home: [README](./README.md)

This schedule tells you when to stop and review what you have learned. Spaced repetition is the most effective way to move knowledge from short-term to long-term memory. Follow this schedule as you progress through the curriculum.

---

## How to Use This Schedule

1. When you finish a review checkpoint level, stop building new projects
2. Spend 1-2 sessions on the review activities listed below
3. If you score below 80% on quizzes or miss more than 5 flashcards, review the linked concept docs before continuing
4. Mark the review as complete in your `PROGRESS.md` and move on

---

## Review Point 1: After Level 0

**When:** After completing all 15 Level 0 projects

**What to review:** Variables, loops, functions, file I/O, string methods

### Activities

| Activity | Tool | Time |
|----------|------|------|
| Flashcard review | `python practice/flashcards/review-runner.py --level 00` then `--level 0` | 15 min |
| Variable quiz | `python concepts/quizzes/what-is-a-variable-quiz.py` | 5 min |
| Loops quiz | `python concepts/quizzes/how-loops-work-quiz.py` | 5 min |
| Functions quiz | `python concepts/quizzes/functions-explained-quiz.py` | 5 min |
| Files quiz | `python concepts/quizzes/files-and-paths-quiz.py` | 5 min |
| Coding challenge | [01-swap-variables](./practice/challenges/beginner/01-swap-variables.py) | 10 min |
| Coding challenge | [02-fizzbuzz](./practice/challenges/beginner/02-fizzbuzz.py) | 10 min |
| Coding challenge | [03-reverse-string](./practice/challenges/beginner/03-reverse-string.py) | 10 min |

**Pass criteria:** Score 80%+ on all quizzes. Complete all three coding challenges.

**If struggling:** Re-read [What Is a Variable](./concepts/what-is-a-variable.md), [How Loops Work](./concepts/how-loops-work.md), and [Functions Explained](./concepts/functions-explained.md). Then redo Level 0 projects 05, 07, and 13.

---

## Review Point 2: After Level 2

**When:** After completing all 15 Level 2 projects

**What to review:** Everything from Review Point 1, plus collections, types, errors, classes, file paths

### Activities

| Activity | Tool | Time |
|----------|------|------|
| Flashcard review | `python practice/flashcards/review-runner.py --level 1` then `--level 2` | 20 min |
| Collections quiz | `python concepts/quizzes/collections-explained-quiz.py` | 5 min |
| Types quiz | `python concepts/quizzes/types-and-conversions-quiz.py` | 5 min |
| Errors quiz | `python concepts/quizzes/errors-and-debugging-quiz.py` | 5 min |
| Coding challenge | [04-count-vowels](./practice/challenges/beginner/04-count-vowels.py) | 10 min |
| Coding challenge | [08-remove-duplicates](./practice/challenges/beginner/08-remove-duplicates.py) | 10 min |
| Coding challenge | [09-word-frequency](./practice/challenges/beginner/09-word-frequency.py) | 10 min |
| Coding challenge | [10-caesar-cipher](./practice/challenges/beginner/10-caesar-cipher.py) | 15 min |
| Re-solve (no notes) | Redo Level 1 project 05 (CSV reader) from scratch | 20 min |

**Pass criteria:** Score 80%+ on all new quizzes. Complete all four coding challenges. Finish the CSV reader re-solve with passing tests.

**If struggling:** Re-read [Collections Explained](./concepts/collections-explained.md) and [Errors and Debugging](./concepts/errors-and-debugging.md). Redo Level 2 projects 01, 03, and 12.

---

## Review Point 3: After Level 5

**When:** After completing all 15 Level 5 projects

**What to review:** Comprehensive review of all fundamentals plus imports, classes, decorators, virtual environments

### Activities

| Activity | Tool | Time |
|----------|------|------|
| Full flashcard review | `python practice/flashcards/review-runner.py` (all levels 0-5) | 30 min |
| Imports quiz | `python concepts/quizzes/how-imports-work-quiz.py` | 5 min |
| Classes quiz | `python concepts/quizzes/classes-and-objects-quiz.py` | 5 min |
| Decorators quiz | `python concepts/quizzes/decorators-explained-quiz.py` | 5 min |
| Virtual envs quiz | `python concepts/quizzes/virtual-environments-quiz.py` | 5 min |
| Terminal quiz | `python concepts/quizzes/the-terminal-deeper-quiz.py` | 5 min |
| Coding challenge | [05-palindrome-check](./practice/challenges/beginner/05-palindrome-check.py) | 10 min |
| Coding challenge | [11-flatten-list](./practice/challenges/beginner/11-flatten-list.py) | 10 min |
| Coding challenge | [13-binary-search](./practice/challenges/beginner/13-binary-search.py) | 15 min |
| Coding challenge | [15-anagram-check](./practice/challenges/beginner/15-anagram-check.py) | 10 min |
| Intermediate challenge | [01-decorator-timer](./practice/challenges/intermediate/01-decorator-timer.py) | 15 min |
| Re-solve (no notes) | Redo Level 3 project 04 (TDD normalizer) from scratch | 25 min |

**Pass criteria:** Score 80%+ on all quizzes. Complete all beginner challenges. Attempt the decorator timer (passing is a bonus at this stage).

**If struggling with fundamentals:** Go back to Review Point 2 and redo those activities first. Solid fundamentals are more important than speed.

**If struggling with intermediate concepts:** Re-read [Classes and Objects](./concepts/classes-and-objects.md) and [Decorators Explained](./concepts/decorators-explained.md). Redo Level 3 projects 01-05.

---

## Review Point 4: After Level 7

**When:** After completing all 15 Level 7 projects

**What to review:** Advanced patterns including HTTP, APIs, async, plus all previous material

### Activities

| Activity | Tool | Time |
|----------|------|------|
| Flashcard review | `python practice/flashcards/review-runner.py --level 6` then `--level 7` | 20 min |
| HTTP quiz | `python concepts/quizzes/http-explained-quiz.py` | 5 min |
| API quiz | `python concepts/quizzes/api-basics-quiz.py` | 5 min |
| Async quiz | `python concepts/quizzes/async-explained-quiz.py` | 5 min |
| Intermediate challenge | [05-retry-decorator](./practice/challenges/intermediate/05-retry-decorator.py) | 15 min |
| Intermediate challenge | [06-lru-cache](./practice/challenges/intermediate/06-lru-cache.py) | 15 min |
| Intermediate challenge | [09-parse-log-file](./practice/challenges/intermediate/09-parse-log-file.py) | 15 min |
| Intermediate challenge | [11-rate-limiter](./practice/challenges/intermediate/11-rate-limiter.py) | 15 min |
| Re-solve (no notes) | Redo Level 5 project 11 (retry-backoff-runner) from scratch | 30 min |

**Pass criteria:** Score 80%+ on HTTP, API, and async quizzes. Complete at least 3 of 4 intermediate challenges.

**If struggling:** Re-read [HTTP Explained](./concepts/http-explained.md) and [API Basics](./concepts/api-basics.md). The async quiz is hard; review [Async Explained](./concepts/async-explained.md) and revisit Level 5 projects on scheduling and resilience.

---

## Review Point 5: After Level 10 (Full Mastery Review)

**When:** After completing all 15 Level 10 projects

**What to review:** Everything. This is a comprehensive assessment of your Python knowledge.

### Activities

| Activity | Tool | Time |
|----------|------|------|
| Full flashcard review | `python practice/flashcards/review-runner.py` (all levels) | 45 min |
| All quizzes | Run every quiz in `concepts/quizzes/` | 60 min |
| Beginner challenges | Complete any you have not done from [beginner/](./practice/challenges/beginner/) | 30 min |
| Intermediate challenges | Complete any you have not done from [intermediate/](./practice/challenges/intermediate/) | 60 min |
| Advanced challenge | [01-generator-pipeline](./practice/challenges/advanced/01_generator_pipeline.py) | 20 min |
| Advanced challenge | [05-type-narrowing](./practice/challenges/advanced/05_type_narrowing.py) | 20 min |
| Capstone re-solve | Pick any capstone project (level X, project 15) and redo from scratch | 45 min |
| Self-assessment | Write a one-page summary of what you know and what you want to learn next | 20 min |

**Pass criteria:** Score 90%+ on all beginner and intermediate quizzes. Complete all beginner challenges and at least 10 intermediate challenges. Attempt both advanced challenges.

**What this proves:** You have solid, recallable Python knowledge across the entire curriculum. You are ready for the elite track, expansion modules, or real-world projects.

---

## Ongoing Review Habits

Even after completing review checkpoints, maintain these habits:

**Daily (5 minutes):** Run flashcards for your current level. The Leitner system automatically surfaces cards you need to review.

```bash
python practice/flashcards/review-runner.py
```

**Weekly (15 minutes):** Pick one coding challenge you have not done and solve it without looking at any reference material.

**After each expansion module:** Review the module-specific flashcard deck. For example, after completing the FastAPI module:

```bash
python practice/flashcards/review-runner.py --deck module-fastapi-cards
```

**Available module flashcard decks:**

| Deck | After Module |
|------|-------------|
| `module-web-scraping-cards` | Module 01: Web Scraping |
| `module-fastapi-cards` | Module 04: FastAPI |
| `module-databases-cards` | Module 06: Databases & ORM |
| `module-django-cards` | Module 10: Django |

---

## Why Spaced Repetition Works

Without review, you forget roughly 50% of new material within 24 hours and 80% within a week (Ebbinghaus forgetting curve). Spaced repetition interrupts this decay by reviewing material at increasing intervals. Each review strengthens the memory trace.

The flashcard system handles the spacing automatically. The review checkpoints in this schedule handle the deeper, project-level review that flashcards cannot cover.

---

| [← README](./README.md) | [Home](./README.md) | [Practice Tools →](./practice/flashcards/README.md) |
|:---|:---:|---:|
