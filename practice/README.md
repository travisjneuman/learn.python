# Practice — Active Recall & Skill Building

This directory contains practice tools that complement the main project ladder. Use these between projects to reinforce concepts and build fluency.

## What's Here

### Flashcards (`flashcards/`)
Spaced repetition flashcard decks for each level. Review cards regularly to retain concepts long-term.

```bash
python practice/flashcards/review-runner.py
```

### Coding Challenges (`challenges/`)
Short, focused exercises (10-30 minutes each) that reinforce specific patterns. Not full projects — just targeted practice reps.

```bash
# Try a challenge
python practice/challenges/beginner/01-swap-variables.py

# Check your solution
python practice/challenges/solutions/beginner/01-swap-variables-solution.py
```

## When to Use These

| Tool | When | Time |
|------|------|------|
| **Flashcards** | Daily, before starting project work | 5-10 min |
| **Challenges** | Between projects, or when you want quick practice | 10-30 min |
| **Concept quizzes** | After reading a concept doc (see `concepts/quizzes/`) | 5-10 min |

## How They Fit the Curriculum

```
Read concept doc → Take quiz → Do projects → Review flashcards → Try challenges
     ↑                                              |
     └──────────── review when cards appear ────────┘
```

The flashcards use a **Leitner box system** — cards you get right move to higher boxes and appear less often. Cards you get wrong drop back to box 1 for immediate review.
