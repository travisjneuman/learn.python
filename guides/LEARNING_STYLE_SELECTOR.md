# How Do You Learn Best?

This curriculum supports every learning style. Answer 5 quick questions to discover your recommended path through the material.

Every concept and project offers multiple ways to learn the same topic — read about it, build it, watch it being built, test your knowledge, visualize it, or try it in the browser. You do not need to use all of them. Find the combination that works for you.

---

## Question 1

**When learning something completely new, I prefer to...**

- **A)** Read about it first, then try it
- **B)** Jump in and figure it out by doing
- **C)** Watch someone else do it first, then try myself
- **D)** See a diagram or visual overview before anything else

## Question 2

**When I get stuck on a problem, I usually...**

- **A)** Go back and re-read the explanation
- **B)** Try different approaches until something works
- **C)** Look for a video or walkthrough showing the solution
- **D)** Draw out the problem on paper or whiteboard

## Question 3

**I feel most confident I understand something when I can...**

- **A)** Explain it in my own words
- **B)** Build something that uses it
- **C)** Recognize it when I see it in someone else's code
- **D)** See how it connects to other concepts I know

## Question 4

**When reviewing material I have already learned, I prefer to...**

- **A)** Re-read my notes or the documentation
- **B)** Redo a practice exercise or challenge
- **C)** Watch a refresher video
- **D)** Review flashcards or take a quiz

## Question 5

**The ideal learning session for me looks like...**

- **A)** Reading a concept guide, then doing the project
- **B)** Starting the project immediately, looking things up as needed
- **C)** Watching how it is done, then trying it myself
- **D)** Seeing the big picture first, then filling in the details

---

## Results

### Mostly A: Reader-First Learner

You learn best by understanding concepts before applying them.

**Your recommended path at each step:**

1. Read the **concept guide** for the topic
2. Take the **quiz** to check understanding
3. Do the **project** with the concept fresh in mind
4. Use **flashcards** for long-term retention

**Tip:** When you encounter a new project, read the "Why this project exists" and "Focus" sections carefully before starting. They give you the conceptual frame.

### Mostly B: Builder-First Learner (Play Mode)

You learn best by doing. Explanations click after you have struggled with the problem.

**Your recommended path at each step:**

1. Start the **project** immediately
2. If stuck after 20 minutes, read the **Walkthrough** (thinking process, not the answer)
3. After completing the project, read the **concept guide** to fill gaps
4. Take the **quiz** to confirm what you picked up

**Tip:** Use `--learning-mode play` when generating your study plan. Set a timer for each project so you stay in the productive struggle zone.

### Mostly C: Watcher-First Learner

You learn best by observing someone else do it first, then replicating and adapting.

**Your recommended path at each step:**

1. Watch the **curated video** for the topic
2. Read the **Walkthrough** to see the thinking process in text
3. Do the **project** yourself
4. Compare your solution to the **annotated solution** (SOLUTION.md)

**Tip:** Videos are linked for every concept. If the first video does not click, each page lists 2-3 alternative explanations from different teachers.

### Mostly D: Visualizer-First Learner

You learn best by seeing the big picture before diving into details.

**Your recommended path at each step:**

1. Open the **Mermaid diagrams** for the topic — see how things connect
2. Read the **concept guide** with the diagram as your mental map
3. Do the **project**, referring back to the diagram when stuck
4. Review with **flashcards** and **quizzes**

**Tip:** Many concept diagrams include decision trees. Use them when you are unsure which tool or pattern to reach for.

---

## Integrating with the study plan generator

Once you know your style, generate a personalized plan:

```bash
python tools/generate_personalized_study_plan.py \
    --hours-per-week 10 \
    --learning-mode hybrid \
    --confidence medium \
    --experience beginner \
    --goal full_stack \
    --learning-style reader
```

Available `--learning-style` values: `reader`, `builder`, `watcher`, `visualizer`

The generator will weight its recommendations toward your preferred modalities while still including all essential hands-on practice.

---

## You can mix styles

Most people use a blend. The categories above are starting points, not boxes. You might be a builder for simple topics and a reader for complex ones. You might watch videos for new concepts and use flashcards for review.

**The "Learn Your Way" table** at the top of every project and concept page gives you one-click access to every available modality. Use whatever works in the moment.

---

| [Home](../README.md) |
|:---:|
