# AI Usage Guide

How and when to use AI tools (ChatGPT, Claude, Copilot, etc.) at each level of the curriculum. The goal is to build real skill, not just get answers.

## The Golden Rule

**Understand before you copy.** If you cannot explain what a piece of code does line by line, you do not understand it yet. Using AI to skip understanding is borrowing from your future self.

## Guidelines by Level

### Level 00 -- No AI

Type everything yourself. Every character. This builds the muscle memory and mental model that everything else depends on.

- Do not use AI to write code
- Do not use AI to explain error messages
- Do not use AI to check your work
- **Why:** You need to feel the keyboard, make typos, fix them yourself. This is how your brain builds the connection between intent and code.

### Levels 0-2 -- AI for Error Messages Only

You may ask AI to explain an error message *after* you have tried to understand it yourself.

- Read the error message yourself first (see [Reading Error Messages](concepts/reading-error-messages.md))
- Try to fix it based on the line number and error type
- If stuck after 2-3 attempts, paste the error into an AI and ask "what does this error mean?"
- **Do not** paste your code and ask "fix this"
- **Do not** ask AI to write code for you
- **Why:** Error messages are a language. You need to learn to read them, but it is okay to get translation help while learning.

### Levels 3-4 -- AI for Debugging Hints

You have the fundamentals. Now AI can help you debug, but you still write all the code.

- Write your code first, always
- When stuck on a bug, describe the problem to the AI in words before sharing code
- Ask "what could cause this behavior?" rather than "fix my code"
- Use AI to explain library documentation you find confusing
- **Do not** ask AI to generate functions or modules
- **Why:** Describing a problem clearly is a skill. If you can explain what is wrong, you are halfway to fixing it.

### Levels 5-6 -- AI for Code Review

You write it, AI reviews it. This is how you level up from working code to good code.

- Write your solution completely before asking AI for feedback
- Ask: "What could I improve in this code?" or "Are there edge cases I missed?"
- Use AI to learn about design patterns relevant to your project
- AI can explain new concepts (SQL, scheduling, templates) that the curriculum introduces
- **Do not** ask AI to write the initial implementation
- **Why:** Code review is how professionals grow. Getting feedback on *your* code teaches you patterns that stick.

### Levels 7-8 -- AI Pair Programming

You drive, AI assists. Think of it like pair programming where you are the driver.

- You decide the architecture and approach
- AI can help implement specific functions after you describe what they should do
- AI can suggest test cases you might have missed
- Discuss trade-offs with AI: "Should I use caching here? What are the pros and cons?"
- **Always** understand what the AI-generated code does before using it
- **Why:** At this level you are learning to evaluate and direct, not just write. Working with AI is a professional skill.

### Levels 9-10 -- Full AI Collaboration

You focus on architecture, design, and decisions. AI handles routine implementation.

- Use AI for boilerplate, scaffolding, and repetitive patterns
- Focus your energy on system design, trade-offs, and architecture decisions
- Use AI to explore approaches: "Give me three ways to implement event sourcing in Python"
- Review all AI-generated code critically -- AI makes mistakes too
- **Why:** Senior engineers spend most of their time on design and review, not typing code. This mirrors real-world practice.

## General Principles

**Build muscle memory first.** Levels 00-2 exist to wire your brain for Python. Skipping this with AI is like using a calculator before learning multiplication -- you will be permanently dependent.

**Test AI suggestions.** AI confidently generates wrong code. Always run it, test it, and verify it works. If you cannot tell whether AI code is correct, you are not ready to use it.

**Describe before you paste.** Before sharing code with AI, try to describe your problem in words. This forces you to think about what you know and what you do not. Often, the act of describing it reveals the answer.

**AI is a tool, not a teacher.** AI can explain and generate, but it cannot assess your understanding. Only you know whether you truly get it or are just copying patterns.

**Never submit AI-generated work as your own understanding.** If a project asks you to explain your approach in `notes.md`, write it in your own words. The notes are for you, not for a grade.

## AI Limitations: What AI Gets Wrong

AI tools are powerful, but they have real limitations that you need to understand before relying on them.

**Hallucinations.** AI sometimes generates code that looks correct but is completely wrong. It might invent function names that do not exist, reference libraries that were never real, or describe behavior that a function does not actually have. This is called "hallucination" and it happens more often than you might expect.

**Deprecated APIs.** AI training data has a cutoff date. It may suggest using functions, libraries, or syntax that were valid two years ago but have since been removed or replaced. Always check that imports actually work and that the API you are calling still exists.

**Subtle bugs.** AI-generated code often works for the "happy path" but fails on edge cases. Off-by-one errors, missing null checks, incorrect exception handling -- these are common in AI output. The code runs, passes a basic test, and breaks in production.

**Confident wrongness.** AI does not say "I am not sure." It presents incorrect information with the same confidence as correct information. You cannot tell from the tone whether the answer is right. You must verify.

**What to do about it:**
- Always run AI-generated code before trusting it
- Write tests for AI code, especially edge cases
- If AI suggests an import or function you have not seen before, verify it exists
- When AI explains a concept, cross-check with official documentation
- Treat AI output as a first draft that needs review, not a finished product

## Structured Pair Programming Protocol (Levels 7-8)

At Levels 7-8, you can use AI as a pair programming partner. Follow this five-step protocol to keep yourself in the driver's seat:

### 1. Describe

Tell the AI what you are building and why, without showing any code yet.

> "I need a function that reads a CSV file, groups rows by the 'category' column, and returns a dict where keys are categories and values are lists of rows."

### 2. Propose

Ask the AI to outline an approach (not write code). Evaluate the approach.

> "What approach would you suggest for this? What data structures would you use?"

### 3. Evaluate

Discuss trade-offs. Ask about alternatives. Make the design decision yourself.

> "You suggested using defaultdict. What would be different if I used setdefault instead? Which is more readable?"

### 4. Implement

Write the code yourself based on the approach you chose. If you get stuck on a specific part, ask for help with that part only.

> "I am implementing the grouping logic. How do I iterate over csv.DictReader rows while keeping the header?"

### 5. Review

Share your finished code and ask for a review.

> "Here is my implementation. What would you improve? Are there edge cases I missed?"

**The key discipline:** You make every decision. AI provides information and feedback. If you find yourself copying large blocks of AI code, you have switched from pair programming to dictation. Stop and go back to step 1.

## Quick Reference

| Level | AI Allowed For | AI Not Allowed For |
|-------|---------------|-------------------|
| 00 | Nothing | Everything |
| 0-2 | Explaining error messages | Writing code, fixing bugs |
| 3-4 | Debugging hints, explaining docs | Writing code, generating functions |
| 5-6 | Code review, explaining concepts | Initial implementation |
| 7-8 | Pair programming (you drive) | Unsupervised code generation |
| 9-10 | Full collaboration | Skipping architecture thinking |

---

| [Home](README.md) |
|:---:|
