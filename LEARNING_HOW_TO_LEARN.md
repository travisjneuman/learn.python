# Learning How to Learn

This guide is about the process of learning itself. Programming is hard, and knowing how to learn effectively will save you hundreds of hours over the course of this curriculum.

---

## The Pomodoro Technique

Work in focused blocks of 25 minutes, then take a 5-minute break. After four blocks, take a longer break of 15-30 minutes.

**Why it works:** Your brain can only maintain deep focus for short periods. Forcing breaks prevents the kind of tired, unfocused coding where you stare at the same error for an hour without making progress.

**How to do it:**

1. Set a timer for 25 minutes.
2. Work on one thing only. No email, no phone, no browsing.
3. When the timer rings, stop. Even mid-sentence.
4. Take a 5-minute break. Stand up, stretch, look away from the screen.
5. Repeat. After four rounds, take a 15-30 minute break.

**Tip:** During the break, do not look at code or read about code. Your brain needs actual rest, not a different kind of screen time.

---

## Frustration vs Confusion

These feel similar but require different responses. Learning to tell them apart is a skill.

**Confusion** means you do not understand something. The fix is more information: re-read the concept doc, look at examples, or ask for an explanation.

Signs of confusion:
- "I do not know what this word means"
- "I do not understand what the code is supposed to do"
- "I have no idea where to start"

**Frustration** means you understand the concept but cannot get it to work. The fix is usually stepping away, then coming back with fresh eyes.

Signs of frustration:
- "I know what it should do but it keeps breaking"
- "I have tried everything and nothing works"
- "This should be simple but it is not"

**What to do when confused:** Slow down. Go back to the concept guide. Read the examples. Try the simplest possible version of the idea in isolation.

**What to do when frustrated:** Take a break. Seriously. Walk away for 10 minutes. When you come back, re-read your code from the top as if someone else wrote it. The bug will often jump out.

---

## Breaking Problems into Parts

Large problems are overwhelming. Small problems are solvable. The skill is learning to break large problems into small ones.

**The process:**

1. Read the entire problem statement.
2. List every separate thing the program needs to do.
3. Pick the simplest item on the list.
4. Solve just that item. Test it. Make sure it works.
5. Pick the next simplest item. Repeat.

**Example:** "Build a calculator that reads expressions from a file and writes results to JSON."

Break it down:
- Read a file (just print the lines first)
- Parse one line into operation, number1, number2
- Do the math for one operation
- Handle all four operations
- Collect results into a list
- Write the list to a JSON file

Each of those steps is small enough to do in one sitting. The whole project is not.

---

## Productive Failure

Getting stuck is not failing. It is learning.

Every professional programmer gets stuck daily. The difference between a beginner and an expert is not that experts never get stuck. The difference is that experts have gotten stuck thousands of times and built a toolkit for getting unstuck.

When you struggle with a concept and eventually figure it out, you remember it far better than if someone had just told you the answer. Research on learning consistently shows that effort during learning (even failed effort) produces stronger and longer-lasting understanding.

**Reframe your self-talk:**
- Instead of "I cannot do this" -- try "I cannot do this yet"
- Instead of "I am stuck" -- try "I am about to learn something"
- Instead of "I keep making mistakes" -- try "I am finding out what does not work"

**What productive failure looks like:**
- You try an approach and it does not work. You learn why.
- You misunderstand a concept. The error message teaches you what it actually means.
- You write code that breaks. You debug it and understand the code better than before.

**What unproductive failure looks like:**
- You stare at the screen for 45 minutes without trying anything.
- You copy code from the internet without reading it.
- You skip the project and move on, hoping the next one will make sense.

If you find yourself in unproductive failure, take a break or go back to a simpler exercise. There is no shame in reviewing earlier material.

---

## The Forgetting Curve and Spaced Repetition

You will forget most of what you learn within a few days if you do not revisit it. This is not a personal failing. This is how human memory works.

**The forgetting curve:** After learning something new, your memory of it drops sharply within 24 hours, then continues to fade over days and weeks.

**Spaced repetition** fights this by reviewing material at increasing intervals:
- Review new concepts the next day
- Review again after 3 days
- Review again after 1 week
- Review again after 2 weeks

Each review takes less time and strengthens the memory more.

**Practical tips for this curriculum:**
- Use the flashcard decks in `practice/flashcards/` -- they are designed for spaced repetition.
- Before starting a new project, spend 5 minutes recalling the previous project. What did you build? What functions did you write? What was tricky?
- When you finish a level, go back and redo the first project from that level without looking at your code. See how much you remember.

---

## How to Take Notes While Coding

Every project in this curriculum has a `notes.md` file. Use it. Writing about what you learned cements it in memory.

**What to write:**
- Concepts that were new to you, in your own words
- Mistakes you made and how you fixed them
- Things that surprised you
- Questions you still have

**What not to write:**
- Do not copy-paste code into your notes (you already have the code)
- Do not write a textbook explanation (write what you personally found useful)
- Do not worry about grammar or polish (these notes are for you)

**A template that works:**

```
## What I built
[One sentence]

## What I learned
[2-3 bullet points in your own words]

## What tripped me up
[The mistake and how I fixed it]

## What I would do differently
[Looking back, what would I change?]
```

Writing takes time. It is worth it. Students who write about what they learn score significantly better on later tests, even without re-reading their notes. The act of writing is the learning.

---

## When to Ask for Help

**The 20-minute rule:** If you have been stuck on the same problem for 20 minutes without making any progress, it is time to ask for help. Not 5 minutes (that is too soon -- you have not tried enough). Not 2 hours (that is too long -- you are wasting time).

**Before asking for help:**
1. Read the error message. What does it say?
2. Find the line number. What is happening on that line?
3. Add `print()` statements to see what your variables contain.
4. Re-read the relevant concept guide.
5. Search for the error message online.

**When asking for help:**
- Say what you are trying to do
- Say what you expected to happen
- Say what actually happened
- Show the error message (if any)
- Show what you have already tried

**Bad help request:** "My code does not work."

**Good help request:** "I am trying to read a CSV file and count the rows. I expected `len(rows)` to return 10, but it returns 11. I think the header row is being counted. I tried skipping the first line with `rows[1:]` but then my column names are wrong."

The second version will get you a useful answer in one exchange instead of five.

---

## Summary

| Technique | When to Use |
|-----------|-------------|
| Pomodoro (25 min on, 5 off) | Every study session |
| Frustration vs confusion check | When you feel stuck |
| Break problems into parts | At the start of every project |
| Productive failure framing | When you want to give up |
| Spaced repetition | Daily, using flashcards |
| Note-taking | After every project |
| 20-minute help rule | When stuck on one problem |

---

| [Home](README.md) |
|:---:|
