# Workshop Kit

A ready-to-use guide for running learn.python workshops at Python meetups, user groups, coding dojos, and classrooms.

---

## 2-Hour Workshop Format

This format covers the first taste of Python: environment setup, absolute-beginner exercises, and a first real project. Participants leave with Python installed, working code they wrote, and a clear path to continue on their own.

### Schedule

| Time | Block | Activity |
|------|-------|----------|
| 0:00 -- 0:15 | Setup Check | Verify Python installed, editor ready, repo cloned |
| 0:15 -- 0:45 | Guided Exercises | Level 00 exercises 1--5, everyone together |
| 0:45 -- 1:00 | Break + Q&A | Answer questions, help stragglers finish setup |
| 1:00 -- 1:30 | Independent Work | Level 0 projects 01--03, facilitator floats |
| 1:30 -- 1:50 | Share and Discuss | Volunteers show solutions, compare approaches |
| 1:50 -- 2:00 | Next Steps | How to continue with the curriculum at home |

---

## Block 1: Setup Check (15 min)

### Facilitator Notes

Have participants run these commands before the workshop if possible (send instructions 48 hours ahead). Use this block to catch anyone who could not set up in advance.

**Pre-workshop email template:**

> Subject: Python Workshop Prep -- 3 Things to Do Before Saturday
>
> 1. Install Python 3.11+ from python.org (or your package manager)
> 2. Install VS Code from code.visualstudio.com
> 3. Clone the repo: `git clone https://github.com/travisjneuman/learn.python.git`
>
> If any step fails, do not worry -- we will help you at the start of the workshop.

**Verification commands (project on screen):**

```bash
python --version    # Should show 3.11 or higher
git --version       # Any version is fine
code --version      # Optional but recommended
```

**Common issues:**

| Problem | Fix |
|---------|-----|
| `python` not found on Windows | Try `python3` or `py`. If neither works, reinstall from python.org and check "Add to PATH". |
| `python` shows 2.7 on macOS | Use `python3` explicitly. Install via `brew install python` if needed. |
| Git not installed | Download from git-scm.com. On macOS, `xcode-select --install` also works. |
| VS Code not installed | Any text editor works. Notepad++, Sublime Text, or even IDLE are fine for the workshop. |
| Cannot clone repo | Download the ZIP from GitHub instead. |

---

## Block 2: Guided Exercises (30 min)

### Facilitator Notes

Open `projects/level-00-absolute-beginner/` and work through exercises 1--5 together. **Type the code live** -- do not copy-paste. Make mistakes on purpose and show how to read error messages.

**Pace:** Spend about 5 minutes per exercise. If the group is fast, do exercise 6. If the group is slow, skip exercise 5 and come back to it.

**Key teaching moments:**

| Exercise | Concept | What to Emphasize |
|----------|---------|-------------------|
| 01 | print() | Python runs top to bottom. Every line does one thing. |
| 02 | Variables | A variable is a name for a value. You can change the value later. |
| 03 | input() | Programs can ask the user for information. The result is always a string. |
| 04 | Math | Python does math with `+`, `-`, `*`, `/`. Division always returns a float. |
| 05 | if/else | Programs can make decisions. Indentation matters in Python. |

**Interaction pattern:**

1. Show the exercise on screen.
2. Ask: "What do you think this will do?" (30 seconds of think time)
3. Ask someone to predict the output.
4. Run the code. Compare to prediction.
5. Modify the code together. Ask: "What happens if we change X?"

---

## Block 3: Break + Q&A (15 min)

### Facilitator Notes

Use this time to:

- Help anyone who fell behind catch up.
- Answer questions that came up during the guided section.
- Make sure everyone's setup is working for the independent work block.
- Walk around and check screens -- some people will not ask for help.

**Good break questions to ask the group:**

- "What surprised you so far?"
- "What was confusing? No question is too basic."
- "Has anyone programmed before? In what language?"

---

## Block 4: Independent Work (30 min)

### Facilitator Notes

Participants work on Level 0 projects 01--03 at their own pace. The facilitator and any helpers should circulate the room.

**Project overview:**

| Project | What They Build | Key Skill |
|---------|----------------|-----------|
| 01-terminal-hello-lab | Terminal greeting program | Running Python scripts, print, input |
| 02-calculator-basics | Basic calculator | Arithmetic, int(), type conversion |
| 03-temperature-converter | Fahrenheit/Celsius converter | Variables, formulas, formatted output |

**Facilitator behavior:**

- Walk slowly around the room. Look at screens, not faces.
- When someone is stuck, ask "What does the error message say?" before giving the answer.
- If someone finishes early, suggest they try the TRY_THIS.md extensions or help a neighbor.
- Do not solve problems for people. Guide them to the answer.

**Common stuck points:**

| Symptom | Likely Cause | Guide Toward |
|---------|-------------|--------------|
| `SyntaxError` | Missing colon, quote, or parenthesis | "Read the error. What line does it point to?" |
| `NameError` | Typo in variable name | "Compare the name on this line to where you defined it." |
| `TypeError` | Forgot `int()` or `float()` on input | "What type does `input()` return? Check with `type()`." |
| Nothing happens | Script has no print or output | "How does your program show results to the user?" |

### Group Activity: Pair Programming on Project 02

If the group is comfortable, pair people up for project 02 (calculator). One person types ("driver"), the other person tells them what to type ("navigator"). Switch roles halfway through. This builds collaboration skills and forces people to articulate their thinking.

**Pairing rules to announce:**

1. The driver only types what the navigator says.
2. The navigator cannot touch the keyboard.
3. Switch roles after 7 minutes.
4. Both people should understand every line before moving on.

### Group Activity: Code Review of Project 01

After most people finish project 01, ask 2--3 volunteers to show their solution on the projector. Compare different approaches. Point out that there is no single "right" answer. Highlight good practices (descriptive variable names, clear output).

---

## Block 5: Share and Discuss (20 min)

### Facilitator Notes

Ask for 2--3 volunteers to share their screen and walk through their solution to any of the three projects. Guide the discussion:

- "Why did you choose that variable name?"
- "What would happen if the user typed a word instead of a number?"
- "How would you add a new feature to this?"

**If no one volunteers:** Share your own solution and intentionally leave a bug in it. Ask the group to find it.

---

## Block 6: Next Steps (10 min)

### Facilitator Notes

Project these on screen:

**To continue on your own:**

1. You already have the repo cloned. Open `START_HERE.md` and follow the links.
2. Finish Level 00 exercises (you did 5, there are 15 total).
3. Continue through Level 0 projects (you did 3, there are 15 total).
4. Read the concept guides in `concepts/` when you need to understand something deeper.
5. Use the flashcards and quizzes to reinforce what you learn.

**How to get help:**

- Open an issue on the GitHub repo.
- Join the Discussions board on GitHub.
- Come to the next meetup.

**Handout (print or share digitally):**

```
Learn Python -- What to Do Next
================================
1. Open START_HERE.md in the repo you cloned today
2. Finish Level 00 (exercises 6-15)
3. Move to Level 0 (projects 04-15)
4. Read concept guides when stuck
5. Run flashcards daily: python practice/flashcards/review-runner.py
6. Ask for help: github.com/travisjneuman/learn.python/discussions
```

---

## For Online Workshops

### Screen Sharing Tips

- Use a large font size (18pt minimum) in your editor.
- Use a high-contrast theme (dark background, light text).
- Zoom your terminal to at least 150%.
- Keep your screen uncluttered: editor on the left, terminal on the right.

### Breakout Room Structure

For platforms that support breakout rooms (Zoom, Teams):

| Room | Activity | Duration |
|------|----------|----------|
| Main room | Guided exercises (Block 2) | 30 min |
| Breakout rooms (3--4 people each) | Independent work (Block 4) | 30 min |
| Main room | Share and discuss (Block 5) | 20 min |

**Assign one helper per 2 breakout rooms.** Helpers rotate between their assigned rooms every 5 minutes.

### Online-Specific Issues

| Problem | Solution |
|---------|----------|
| Participant cannot share screen | Ask them to paste code in chat. Help them verbally. |
| Audio echo | Everyone mutes except the speaker. |
| Participant falls behind | Invite them to a 1-on-1 breakout room with a helper. |
| Low engagement | Use polls: "Who got exercise 3 working? React with a thumbs up." |

---

## Adapting for Different Durations

### 1-Hour Lightning Version

- Skip Block 3 (break) and Block 5 (share).
- Do only exercises 1--3 in the guided block.
- Do only project 01 in the independent block.
- Spend 5 minutes on next steps.

### Half-Day (4 Hours)

- Add all 15 Level 00 exercises.
- Add Level 0 projects 04--07.
- Add a concept guide reading session (pick 2 from beginner concepts).
- Add a quiz session.

### Full-Day (8 Hours)

- Complete all of Level 00 and Level 0.
- Include concept guides and quizzes.
- Add expansion module 01 (Web Scraping) project 01 if the group is advanced.
- End with a mini-capstone: participants choose one project to extend and present.

---

## Printable Exercise Summary Cards

These summaries can be printed (one per table) as quick reference during the workshop.

### Card 1: Python Basics

```
PYTHON BASICS
=============
Print:       print("Hello")
Variable:    name = "Alice"
Input:       answer = input("Question? ")
Math:        result = 10 + 5
Convert:     number = int("42")
If/else:     if x > 0:
                 print("positive")
             else:
                 print("not positive")
```

### Card 2: Common Errors

```
COMMON ERRORS
=============
SyntaxError     Missing : or ) or "
NameError       Typo in variable name
TypeError       Wrong type (e.g., "5" + 3)
IndentationError  Spaces don't match

HOW TO READ ERRORS:
1. Look at the LAST line -- it says what went wrong
2. Look at the line number -- it says where
3. Read the ^^ arrows -- they point to the problem
```

### Card 3: Terminal Commands

```
TERMINAL COMMANDS
=================
python file.py     Run a Python script
python --version   Check Python version
cd folder          Change directory
ls (or dir)        List files
clear (or cls)     Clear the screen
```

---

## Facilitator Preparation Checklist

One week before:

- [ ] Send pre-workshop setup email to participants.
- [ ] Test the repo clone and exercises on a fresh machine.
- [ ] Prepare your editor with large font and high-contrast theme.
- [ ] Print exercise summary cards (1 set per table of 4).
- [ ] Recruit 1 helper per 10 participants.

Day of:

- [ ] Arrive 30 minutes early to test projector/screen sharing.
- [ ] Have the repo open in your editor and terminal ready.
- [ ] Write the WiFi password on the board.
- [ ] Have a USB drive with the repo ZIP for participants who cannot clone.

---

<table width="100%">
<tr>
<td align="left"><a href="./TEACHING_GUIDE.md">Prev</a></td>
<td align="center"><a href="./README.md">Home</a></td>
<td align="right"><a href="./START_HERE.md">Next</a></td>
</tr>
</table>
