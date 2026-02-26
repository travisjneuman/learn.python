# Pedagogy and Learning Science Research Report

**Audit Component:** Task #3 — Pedagogy Research
**Date:** 2026-02-25
**Scope:** Current research (2024-2026) on programming education best practices, mapped to learn.python curriculum

---

## Executive Summary

The learn.python curriculum is pedagogically strong in several areas: its progressive scaffolding (Level 00 through Level 10), the Alter/Break/Fix/Explain pattern, the graduated AI usage policy, and the emphasis on debugging through error exposure. However, research points to several areas where the curriculum could be strengthened: formal spaced repetition integration, more explicit cognitive load management at transitions, productive failure design, accessibility considerations, and more structured peer/AI pair programming guidance.

---

## 1. Cognitive Load Theory (CLT) in Programming Education

### What the Research Says

Recent meta-analyses and studies (2024-2025) confirm that cognitive load remains the primary bottleneck for novice programmers. Key findings:

- **Example-problem-based learning** reduces extraneous cognitive load compared to pure problem-based learning for beginners. Students who see worked examples before attempting problems perform significantly better on transfer tasks ([JISE 2024](https://jise.org/Volume35/n3/JISE2024v35n3pp303-312.pdf)).
- **Visual programming languages** produce lower cognitive load than text-based languages for complete beginners, though the advantage disappears by intermediate levels ([ICER 2024](https://dl.acm.org/doi/10.1145/3632620.3671124)).
- **AI-adaptive learning systems** can manage cognitive load dynamically by adjusting difficulty in real time, but this requires metacognitive skill from learners -- less capable learners may be overwhelmed ([PMC 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11852728/)).
- **Self-regulation** is essential for managing cognitive load during programming tasks. Learners who monitor their own understanding and take breaks perform better ([Tandfonline 2025](https://www.tandfonline.com/doi/full/10.1080/10494820.2025.2523401)).

### How learn.python Currently Handles This

**Strengths:**
- Level 00 introduces concepts one at a time (print, then input, then variables, then math) -- this is textbook CLT.
- The Feature Unlock Chart (FEATURE_UNLOCK.md) is excellent progressive disclosure: no imports until Level 0, no third-party packages until Level 3.
- Each project README has a single "Focus" line, keeping the learner's attention on one concept.
- The "no AI at Level 00" rule eliminates a major source of extraneous cognitive load for beginners.

**Gaps:**
- No worked examples precede the projects. The TRY_THIS.md files at Level 00 show code snippets, but Levels 0+ jump straight to "build this project." Research says learners benefit from studying a completed, annotated solution before attempting a similar problem.
- Transition points between levels (e.g., Level 00 to Level 0, which introduces pytest/ruff/project structure simultaneously) are cognitive load spikes. No explicit "bridge" exercises ease these transitions.
- No guidance on self-regulation strategies (when to take breaks, how to recognize overload, how to chunk study sessions).

### Recommendations

1. **Add worked examples** to the first 2-3 projects of each level. Show a completed, annotated solution for a similar (not identical) problem before the learner attempts their project.
2. **Create bridge exercises** at each level transition. For example, between Level 00 and Level 0: a single exercise that introduces pytest on a trivial function the learner already wrote at Level 00.
3. **Add a "Learning How to Learn" guide** with self-regulation tips: Pomodoro technique, recognizing frustration as a signal to step back, how to break problems into parts.

---

## 2. Spaced Repetition for Code Learning

### What the Research Says

Spaced repetition improves long-term retention across all domains, but programming has a specific nuance: **declarative knowledge** (syntax, API names, language rules) benefits enormously from spaced repetition, while **procedural knowledge** (debugging, design, architecture) benefits more from distributed practice across projects ([Spaced Repetition and Retrieval Practice, 2025](https://journals.zeuspress.org/index.php/IJASSR/article/view/425)).

- Double-spaced repetitions are superior to single-spaced for both learning and transfer.
- Spaced repetition works best as a supplement to project work, not a replacement.
- AI-enhanced spaced repetition systems (like LECTOR) show promise for adaptive scheduling ([arXiv 2025](https://www.arxiv.org/pdf/2508.03275)).
- The FSRS algorithm (used in Anki) has been validated as highly effective for scheduling reviews.

### How learn.python Currently Handles This

**Strengths:**
- The curriculum already has flashcard decks (mentioned in commit history for levels 6-10).
- The Alter/Break/Fix/Explain cycle inherently creates retrieval practice -- learners must recall how the code works to alter and break it.
- The Hybrid learning mode recommends "review flashcards daily."

**Gaps:**
- No formal spaced repetition schedule is built into the curriculum. Flashcards exist but there is no guidance on when to review what.
- Concepts from earlier levels are not explicitly revisited in later projects. A learner at Level 5 may have forgotten Level 1 pathlib patterns.
- No retrieval practice exercises (quick, low-stakes recall questions) are embedded in the project flow.

### Recommendations

1. **Add "Recall Checks" to project READMEs.** Before each project, include 2-3 quick questions that test recall of prerequisites. Example: "Before starting this project, can you write a function that reads a CSV file and returns a list of dictionaries? Try it from memory."
2. **Create a spaced repetition schedule** in a REVIEW_SCHEDULE.md file. Map concepts to review intervals (e.g., "Review Level 1 CSV concepts at the start of Level 3, Level 5, and Level 8").
3. **Add cross-level callback projects.** At Level 5, include a mini-exercise that requires Level 1 skills in a new context, forcing retrieval of earlier material.

---

## 3. Project-Based vs. Exercise-Based Learning

### What the Research Says

Recent meta-analyses (2024-2025) strongly favor project-based learning (PBL) for programming:

- PBL significantly amplifies computational thinking across innovation, collaboration, critical analysis, and problem resolution ([Springer, meta-analysis of 31 studies](https://link.springer.com/article/10.1007/s10639-023-12392-2)).
- PBL combined with self-regulated learning produces the strongest outcomes for problem-solving and metacognitive skills ([Wiley 2025](http://resolver.scholarsportal.info/resolve/doi/10.1111/jcal.70011)).
- However, PBL without scaffolding overwhelms novices. The optimal approach is **scaffolded PBL** -- structured projects with clear steps that gradually become more open-ended.
- Exercise-based learning (drills) is more effective for syntactic fluency and basic pattern recognition. Projects are more effective for design thinking and transfer.

### How learn.python Currently Handles This

**Strengths:**
- The curriculum uses projects as its primary vehicle from Level 0 onward -- this is well-aligned with research.
- Projects increase in complexity gradually (Level 0 projects are small and focused; Level 10 projects are enterprise-scale).
- Level 00 uses exercises (TRY_THIS.md), which is appropriate for absolute beginners who need syntactic fluency first.
- The Alter/Break/Fix/Explain pattern adds scaffolding to what could otherwise be overwhelming open-ended projects.

**Gaps:**
- No "open-ended" capstone projects beyond Level 15 (mini-toolkit). Research suggests that at higher levels (7+), learners benefit from choosing their own project scope and requirements.
- No explicit design-before-code phase. Research shows that requiring learners to plan (pseudocode, diagram, or outline) before coding improves outcomes.
- The expansion modules are project-based but disconnected from the main progression. Learners may not know when they are ready.

### Recommendations

1. **Add a design phase** to projects at Level 3+. Before coding, ask learners to write pseudocode or draw a diagram in their notes.md.
2. **Introduce open-ended projects** at Level 7+. Provide a problem domain but let learners define their own requirements, data sources, and architecture.
3. **Map expansion modules to levels** more explicitly. Add a "Prerequisites" section to each module README listing the specific levels/concepts required.

---

## 4. AI Tutoring in CS Education

### What the Research Says

AI tutoring is the fastest-moving area of CS education research. Key findings from 2024-2025:

- When **pedagogically constrained**, conversational AI improves learner autonomy, engagement, and reflective thinking. Unconstrained AI access leads to dependency ([arXiv 2024](https://arxiv.org/html/2512.11882v1)).
- CS students are heavy AI users -- 36.8% of Claude conversations come from CS students who are only 5.4% of degree holders. Most use AI to debug and get technical explanations ([Anthropic Education Report](https://www.anthropic.com/news/anthropic-education-report-how-university-students-use-claude)).
- AI hallucinations and error propagation are real risks. Human oversight and pedagogically sound design are critical ([arXiv 2025](https://arxiv.org/html/2507.11543)).
- **AI-assisted pair programming** produces outcomes comparable to human-human pair programming for motivation and anxiety reduction, and even outperforms both individual and human-human groups on programming tasks ([SpringerOpen 2025](https://stemeducationjournal.springeropen.com/articles/10.1186/s40594-025-00537-3)).

### How learn.python Currently Handles This

**Strengths:**
- The AI_USAGE_GUIDE.md is excellent and research-aligned. The graduated permission model (no AI at Level 00, error explanation only at 0-2, debugging hints at 3-4, code review at 5-6, pair programming at 7-8, full collaboration at 9-10) matches the pedagogical constraint research almost perfectly.
- The "Golden Rule" of understand-before-you-copy is critical and well-stated.
- The CLAUDE.md tutoring rules (Socratic method, predict-before-running, guide debugging) are aligned with best practices.
- The "describe before you paste" principle maps to research on self-explanation effects.

**Gaps:**
- No guidance on how to evaluate whether AI-generated code is correct. At Level 7+, learners are told to "review critically," but no framework is provided for what to check.
- No explicit "AI pair programming protocol" -- how should the learner structure a pair programming session with AI? Research shows that structured dialogue patterns produce better outcomes than ad-hoc interaction.
- No warning about AI hallucination risks specific to Python (e.g., AI suggesting deprecated APIs, inventing nonexistent module functions).

### Recommendations

1. **Add an "AI Code Review Checklist"** for Levels 5+. Teach learners to check: Does it run? Does it pass tests? Do I understand every line? Are there edge cases? Is the approach idiomatic Python?
2. **Add a structured AI pair programming protocol** for Levels 7-8. Example: "1. Describe the problem. 2. Propose your approach. 3. Ask AI to evaluate your approach. 4. Implement it yourself. 5. Ask AI to review."
3. **Add a section on AI limitations** in AI_USAGE_GUIDE.md covering hallucinations, deprecated API suggestions, and the importance of running/testing AI output.

---

## 5. Scaffolding and Progressive Disclosure

### What the Research Says

A 2026 meta-analysis of 30 studies on scaffolding in programming found a **high positive effect** on computational thinking. Key nuances:

- **Fade-out scaffolding** (gradually removing support) is more effective than constant scaffolding. The optimal pattern is: full support -> partial support -> independent work ([Wiley 2025](https://onlinelibrary.wiley.com/doi/abs/10.1111/jcal.70012)).
- **Three-stage fade-out** (modeled -> guided -> independent) produces the best results for programming self-efficacy and achievement.
- Scaffolding combined with self-regulated learning produces the strongest outcomes ([SAGE 2026](https://journals.sagepub.com/doi/abs/10.1177/07356331251386618)).
- LLMs as scaffolding resources show promise when integrated into structured learning frameworks ([Springer 2025](https://link.springer.com/chapter/10.1007/978-981-95-4499-8_9)).

### How learn.python Currently Handles This

**Strengths:**
- The overall curriculum structure is strong progressive disclosure: Level 00 has no imports, no tests, no project structure. Level 0 adds pytest and ruff. Level 3 adds third-party packages. Level 6 adds databases.
- The Feature Unlock Chart is a clear progressive disclosure map.
- The Alter/Break/Fix pattern provides scaffolding within each project (the learner works with existing code before writing from scratch).

**Gaps:**
- Scaffolding does not explicitly fade out. Level 0 projects and Level 10 projects have the same README structure (Focus, Run, Alter, Break, Fix, Explain). At higher levels, the Alter/Break/Fix prompts should become less specific.
- No "completion problems" (partially written code that the learner finishes). Research shows these are optimal for the transition from worked examples to independent work.
- The mastery check criteria are the same at every level ("run baseline without docs, explain one function, break and recover, keep tests passing"). These should become more demanding as levels increase.

### Recommendations

1. **Fade the scaffolding.** At Levels 0-2: detailed Alter/Break/Fix instructions (current approach). At Levels 3-5: vaguer prompts ("Add a feature that uses a concept from a previous level"). At Levels 7+: "Extend this project in a meaningful way. Document your design choices."
2. **Add completion problems** at Levels 1-3. Provide partially written functions where the learner fills in the logic. These bridge the gap between worked examples and blank-page projects.
3. **Scale mastery checks** by level. At Level 7+, mastery should include: "Can you explain the architectural trade-offs?" and "Can you refactor this for a different use case?"

---

## 6. Debugging as Pedagogy

### What the Research Says

Debugging is increasingly recognized as a core pedagogical tool, not just a skill to acquire:

- **Productive failure through debugging** -- when students encounter and resolve errors, they develop deeper understanding than students who see only correct code ([ACM SIGCSE 2019](https://dl.acm.org/doi/10.1145/3287324.3287333), still foundational).
- The **PRIMMDebug** framework (Predict, Run, Investigate, Modify, Make + Debug) provides a structured approach to teaching debugging in secondary education ([arXiv 2025](https://arxiv.org/html/2508.18875v1)).
- Effective debugging instruction requires **explicit teaching** of systematic strategies, not just exposure to errors ([PMC 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11802966/)).
- Instructor modeling of debugging (showing their own process, including dead ends) is more effective than presenting polished debugging steps.

### How learn.python Currently Handles This

**Strengths:**
- The "Break it" section in every project README is excellent. This deliberately exposes learners to errors and forces them to understand failure modes.
- The "Fix it" section that follows requires systematic debugging.
- The CLAUDE.md tutoring rules emphasize debugging pedagogy: "Ask them to read the error message out loud," "Ask what they think the error means."
- The AI_USAGE_GUIDE.md restricts AI debugging help at early levels, forcing learners to develop their own debugging skills.
- TRY_THIS.md files include deliberate error exposure (e.g., "Try dividing by zero. Read the error message carefully.").

**Gaps:**
- No explicit debugging methodology is taught. Learners are told to read error messages, but not taught a systematic process (reproduce, isolate, hypothesize, test, fix, verify).
- No "bug hunt" exercises where learners are given deliberately broken code to fix. The Break/Fix cycle uses code they wrote, which is different from debugging unfamiliar code.
- No guidance on using Python's built-in debugging tools (print-debugging is mentioned; pdb, breakpoints, and debugger integration are not).

### Recommendations

1. **Add a concepts/debugging-methodology.md** guide teaching a formal debugging process: Reproduce -> Isolate -> Hypothesize -> Test -> Fix -> Verify -> Prevent.
2. **Add "Bug Hunt" exercises** at Levels 2-4. Provide deliberately broken code with 3-5 bugs. The learner must find and fix all of them without being told what is wrong.
3. **Introduce Python debugging tools progressively.** Level 0-2: print() debugging. Level 3: introduce `breakpoint()` and pdb basics. Level 5+: IDE debugger integration.

---

## 7. Pair Programming for Learners

### What the Research Says

Research continues to show positive outcomes for pair programming in education:

- Pair programming enhances learning, confidence, problem-solving skills, and collaborative interaction ([ACM meta-analysis](https://dl.acm.org/doi/10.1145/2996201)).
- **Collaborative dialogue patterns** matter more than just pairing up. Four distinct patterns have different effects on self-efficacy and performance ([BJET 2024](https://bera-journals.onlinelibrary.wiley.com/doi/full/10.1111/bjet.13412)).
- **AI-assisted pair programming** significantly increases intrinsic motivation and reduces programming anxiety, with outcomes comparable to human pair programming ([SpringerOpen 2025](https://stemeducationjournal.springeropen.com/articles/10.1186/s40594-025-00537-3)).
- Novice programmers benefit most from pair programming due to reduced isolation and shared cognitive load.

### How learn.python Currently Handles This

**Strengths:**
- The AI_USAGE_GUIDE.md at Levels 7-8 frames AI interaction as pair programming ("you drive, AI assists"), which aligns with the research on AI-assisted pair programming.

**Gaps:**
- No guidance on human pair programming. The curriculum appears designed for solo learners only.
- No structured pair programming protocols (driver/navigator roles, time-boxed swaps, communication guidelines).
- The AI pair programming framing at Levels 7-8 could be more structured with specific interaction patterns.

### Recommendations

1. **Add optional pair programming guidance** for learners who have a study partner. Include driver/navigator role descriptions and swap intervals.
2. **Structure the AI pair programming protocol** at Levels 7-8 with specific conversation templates and role definitions.
3. **Add "Explain to a Partner" exercises** as an alternative to the Explain It section for learners working with someone else.

---

## 8. Gamification in Programming Education

### What the Research Says

Meta-analyses (2024-2025) show gamification has a positive but nuanced impact:

- Largest effect on **motivation**, followed by **academic achievement**, with least effect on cognitive load ([ScienceDirect meta-analysis](https://www.sciencedirect.com/science/article/pii/S2666920X22000510)).
- Gamification in programming education significantly outperforms non-gamified approaches for learning gains ([Wiley 2024](https://onlinelibrary.wiley.com/doi/10.1111/jcal.13000)).
- Overall effect size is large (g = 0.822) across educational contexts ([BJET 2024](https://bera-journals.onlinelibrary.wiley.com/doi/full/10.1111/bjet.13471)).
- However: effectiveness is highly context-dependent. Poorly designed gamification (arbitrary points, meaningless badges) can be counterproductive. The most effective elements are: progress visualization, meaningful milestones, and optional challenges.

### How learn.python Currently Handles This

**Strengths:**
- Progress tracking (PROGRESS.md, tools/progress.py) provides progress visualization.
- The level system itself is a form of gamification -- clear progression through numbered stages.
- Mastery checks serve as milestone gates.
- The "Alter it" challenges add optional extension beyond the baseline.

**Gaps:**
- No achievement/badge system for completing milestones (e.g., "Completed all Level 0 projects," "First expansion module finished").
- No streak tracking for consistent practice.
- No optional challenge problems that go beyond the curriculum (for motivated learners who want extra practice).
- The progress tracker appears to be binary (done/not done) rather than showing partial progress or mastery depth.

### Recommendations

1. **Add a lightweight achievement system** in PROGRESS.md or the progress tracker. Milestones like "First Bug Fixed," "10 Projects Completed," "First Expansion Module" provide motivational anchors.
2. **Add optional "Challenge Mode"** problems to projects at Level 3+. These are harder variations that are not required but provide extra depth for motivated learners.
3. **Enhance the progress tracker** to show mastery depth (baseline complete, alter complete, break/fix complete, explain complete) rather than binary completion.

---

## 9. Assessment Methods

### What the Research Says

Alternative assessment methods are gaining ground in programming education (2024-2025):

- **Portfolio-based assessment** provides a multifaceted representation of student skills and supports self-reflection, self-assessment, and goal-setting ([NCME 2025](https://ncme.org/wp-content/uploads/2025/10/Module-11-Classroom-Assessment-III-Portfolio-Asses-2.pdf)).
- **Competency-based assessment** evaluates mastery of specific skills through projects, portfolios, and practical tasks rather than timed exams ([AISL 2024](https://www.aislmall.com/news/assessment-trends-in-2024-shaping-educations-future)).
- **Authentic assessment** (case studies, simulations, real-world tasks) produces better transfer than traditional testing.
- For self-paced learners, the most effective assessment combines: self-assessment, peer review, and portfolio demonstration.

### How learn.python Currently Handles This

**Strengths:**
- The notes.md file in each project encourages self-reflection (a form of portfolio assessment).
- The Explain It (teach-back) section tests conceptual understanding, not just code output.
- Mastery checks are competency-based ("you can move on when you can...").
- Tests (pytest) provide immediate, objective feedback on correctness.

**Gaps:**
- No portfolio-building guidance. Learners complete projects but are not guided to curate their best work into a portfolio.
- No self-assessment rubrics. The mastery checks are binary ("can you or can't you"). A rubric would help learners gauge their depth of understanding.
- No peer review guidance for learners in cohorts or study groups.
- The curriculum documents (16-25) mention mastery scoring and assessment, but these are in the advanced curriculum path and may not reach most learners.

### Recommendations

1. **Add a portfolio guide** (PORTFOLIO.md) explaining how to select and present best projects for job applications or further study.
2. **Add self-assessment rubrics** to mastery checks. Example: "Rate yourself 1-5 on: Can explain the approach, Can modify for a new use case, Can debug without hints, Can explain trade-offs."
3. **Surface the mastery scoring system** from the advanced curriculum path into the main project flow so all learners benefit.

---

## 10. Accessibility in Coding Education

### What the Research Says

Accessibility in coding education remains an underserved area (2024-2025):

- Block-based coding platforms (Scratch, MakeCode) are currently **not accessible** to learners with visual or dexterity impairments. Google's Blockly team is working on keyboard navigation (2025) and screen reader compatibility (2026) ([micro:bit 2024](https://microbit.org/news/2024-12-05/google-blockly-accessibility-fund/)).
- AI tools show promise for improving accessibility, including real-time captioning, text-to-speech, and adaptive interfaces ([EDUCAUSE 2024](https://er.educause.edu/articles/2024/9/the-impact-of-ai-in-advancing-accessibility-for-learners-with-disabilities)).
- New ADA Title II regulations (April 2024) require public educational institutions to meet WCAG 2.1 AA standards.
- Screen reader users rely heavily on JAWS (41%) and NVDA (38%) in 2024 ([WebAIM Survey 2024](https://webaim.org/projects/screenreadersurvey10/)).

### How learn.python Currently Handles This

**Strengths:**
- The curriculum is text-based (Markdown files and Python scripts), which is inherently more accessible than video or visual platforms.
- Terminal/CLI focus is screen-reader-friendly compared to GUI-based coding environments.
- The curriculum works with any text editor, allowing learners to use their preferred assistive technology.

**Gaps:**
- No explicit accessibility statement or guidance for learners with disabilities.
- No alternative formats for visual content (if any diagrams exist, they may lack alt text).
- No guidance on accessible development environments (screen reader-friendly editors, high-contrast themes, keyboard navigation).
- No consideration of cognitive accessibility (dyslexia-friendly formatting, ADHD-friendly session structures).
- The progress tracker (CLI-based) may not be accessible to all users.

### Recommendations

1. **Add an ACCESSIBILITY.md** file with guidance for learners using assistive technology: recommended editors, screen reader tips, and how to navigate the curriculum.
2. **Ensure all Markdown files** follow accessibility best practices: descriptive link text (not "click here"), proper heading hierarchy, alt text for any images.
3. **Add cognitive accessibility guidance:** recommended session lengths, break reminders, and tips for learners with ADHD or dyslexia.
4. **Consider adding audio/video alternatives** for key concept explanations (or at least guidance on how to use AI text-to-speech tools with the curriculum).

---

## 11. Productive Failure

### What the Research Says

Productive failure (PF) is an emerging and important area in CS education:

- PF involves students attempting problems **before** receiving instruction. The initial struggle activates prior knowledge and creates "knowledge gaps" that make subsequent instruction more effective ([Kapur, ETH Zurich](https://lse.ethz.ch/research/productive-failure.html)).
- A 2024 study applied PF to teaching Python lists and found promising results for conceptual knowledge, though effects on procedural knowledge were mixed ([arXiv 2024](https://arxiv.org/html/2411.11227v1)).
- PF combined with pair programming and self-reflection shows strong results for self-directed learning ([MDPI 2025](https://www.mdpi.com/2227-7102/15/11/1427)).
- Debugging has been reframed as a form of productive failure in CS education -- encountering errors is not an obstacle but a learning mechanism.

### How learn.python Currently Handles This

**Strengths:**
- The "Break it" exercises are a form of productive failure -- learners deliberately create errors and must reason about why they occur.
- The "Play-First" learning mode (open a project, tinker, figure it out) is essentially a productive failure approach.
- The "When the learner is stuck" protocol in CLAUDE.md allows struggle before providing help (2-3 hints before showing the fix).

**Gaps:**
- Productive failure is not explicitly named or framed. Learners may interpret struggle as "I'm failing" rather than "I'm learning."
- No "try before you learn" exercises where learners attempt a problem using only their current knowledge before reading the concept guide.
- The structured learning mode goes concept -> quiz -> project, which is the opposite of productive failure (instruction first, practice second).

### Recommendations

1. **Reframe struggle as productive.** Add a note in GETTING_STARTED.md: "Getting stuck is not failing -- it is learning. Research shows you learn more deeply when you struggle first and then get the explanation."
2. **Add "Try First" prompts** to concept guides. Before explaining a concept, pose a problem: "Before reading further, try to write a function that... Don't worry about getting it right."
3. **Consider a "Productive Failure" learning mode** as a fourth option: attempt the project first with no guidance, then read the concept guide, then redo the project.

---

## Summary: What We Do Well

| Area | Strength |
|------|----------|
| Progressive disclosure | Feature Unlock Chart is excellent; single-concept focus per project |
| Debugging pedagogy | Break/Fix cycle is research-aligned; error exposure from Level 00 |
| AI integration | Graduated AI permission model is nearly optimal; Socratic tutoring rules |
| Project-based learning | Projects as primary vehicle from Level 0; scaffolded with Alter/Break/Fix |
| Self-explanation | Explain It (teach-back) section promotes deep processing |
| Appropriate difficulty | Level 00 removes all complexity; levels ramp gradually |

## Summary: What Should Change

| Area | Gap | Priority |
|------|-----|----------|
| Worked examples | No annotated solutions before projects | High |
| Level transitions | Cognitive load spikes at level boundaries | High |
| Spaced repetition | No formal review schedule or recall checks | High |
| Debugging methodology | No explicit systematic debugging process taught | Medium |
| Scaffolding fade | Same structure at Level 0 and Level 10 | Medium |
| Bug hunt exercises | No practice debugging unfamiliar code | Medium |
| Accessibility | No accessibility statement or guidance | Medium |
| Portfolio guidance | No help curating work for job applications | Medium |
| Productive failure framing | Struggle not explicitly normalized as learning | Medium |
| Open-ended projects | No learner-defined projects at higher levels | Low |
| Pair programming | No human pair programming guidance | Low |
| Gamification | No achievement system or streak tracking | Low |
| Self-assessment rubrics | Mastery checks are binary, not graduated | Low |

---

## Key Research Sources

- [Cognitive Load Theory: Emerging Trends (MDPI 2025)](https://www.mdpi.com/2227-7102/15/4/458)
- [Differentiated CLT Measurement in Programming (Springer 2024)](https://link.springer.com/article/10.1007/s12528-024-09411-7)
- [Spaced Repetition and Retrieval Practice (IJASSR 2025)](https://journals.zeuspress.org/index.php/IJASSR/article/view/425)
- [PBL Meta-Analysis for Computational Thinking (Springer 2023)](https://link.springer.com/article/10.1007/s10639-023-12392-2)
- [PBL + Self-Regulated Learning in Programming (Wiley 2025)](http://resolver.scholarsportal.info/resolve/doi/10.1111/jcal.70011)
- [Pedagogically Controlled AI Tutor (arXiv 2024)](https://arxiv.org/html/2512.11882v1)
- [Anthropic Education Report: How Students Use Claude](https://www.anthropic.com/news/anthropic-education-report-how-university-students-use-claude)
- [AI-Assisted Pair Programming (SpringerOpen 2025)](https://stemeducationjournal.springeropen.com/articles/10.1186/s40594-025-00537-3)
- [Scaffolding Meta-Analysis (SAGE 2026)](https://journals.sagepub.com/doi/abs/10.1177/07356331251386618)
- [Three-Stage Fade-Out Scaffolding (Wiley 2025)](https://onlinelibrary.wiley.com/doi/abs/10.1111/jcal.70012)
- [PRIMMDebug Framework (arXiv 2025)](https://arxiv.org/html/2508.18875v1)
- [Debugging as Productive Failure (ACM 2019)](https://dl.acm.org/doi/10.1145/3287324.3287333)
- [Gamification Meta-Analysis in Programming (ScienceDirect 2022)](https://www.sciencedirect.com/science/article/pii/S2666920X22000510)
- [Gamification in Programming Higher Ed (Wiley 2024)](https://onlinelibrary.wiley.com/doi/10.1111/jcal.13000)
- [Productive Failure for Python (arXiv 2024)](https://arxiv.org/html/2411.11227v1)
- [PF + Pair Programming in Coding Education (MDPI 2025)](https://www.mdpi.com/2227-7102/15/11/1427)
- [Accessibility and AI (EDUCAUSE 2024)](https://er.educause.edu/articles/2024/9/the-impact-of-ai-in-advancing-accessibility-for-learners-with-disabilities)
- [WebAIM Screen Reader Survey 2024](https://webaim.org/projects/screenreadersurvey10/)
- [Portfolio-Based Assessment (NCME 2025)](https://ncme.org/wp-content/uploads/2025/10/Module-11-Classroom-Assessment-III-Portfolio-Asses-2.pdf)
