# Level 10 / Project 14 - SME Mentorship Toolkit
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| [Concept](../../../concepts/how-imports-work.md) | **This project** | — | [Quiz](../../../concepts/quizzes/how-imports-work-quiz.py) | [Flashcards](../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus
- Weighted matching algorithm based on skill overlap and experience gaps
- Greedy mentor assignment respecting capacity constraints
- Milestone tracking with completion rate metrics
- Skill-level modeling with proficiency-based matching

## Why this project exists
Ad-hoc mentorship often fails because pairings are suboptimal or progress is invisible. This project formalizes skill matching and milestone tracking so organizations can measure mentorship ROI and ensure knowledge transfer happens systematically.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-10/14-sme-mentorship-toolkit
python project.py
pytest -v
```

## Expected terminal output
```text
Matches:
  E1 -> M1 (score: 85.0, skills: ['python', 'sql'])
  E2 -> M2 (score: 72.0, skills: ['javascript', 'react'])
  ...
```

## Alter it (required)
1. Add a `timezone` field to Person and penalize matches where mentor/mentee are >6 hours apart.
2. Add a `feedback_score` to milestones so mentees can rate each milestone completion.
3. Add a `MentorReport` that shows how many mentees each mentor has and their completion rates.

## Break it (required)
1. Create a mentee with goals that no mentor can fulfill — observe a low compatibility score.
2. Set `max_mentees=0` for all mentors and verify no matches are produced.
3. Try to complete a non-existent milestone ID.

## Fix it (required)
1. Add a minimum compatibility threshold — do not assign a mentor if the score is below 30.
2. Add a warning when a mentee cannot be matched due to capacity constraints.
3. Test both fixes.

## Explain it (teach-back)
1. How does the compatibility score weight skill overlap vs experience gap vs availability?
2. Why does the greedy matching algorithm assign mentees in order rather than using global optimization?
3. How does tracking milestone completion rate help measure mentorship effectiveness?
4. How would you extend this to handle re-matching when a mentor leaves?

## Mastery check
You can move on when you can:
- compute a compatibility score by hand for a mentor-mentee pair,
- explain why capacity constraints prevent one mentor from being overloaded,
- add a milestone and track it through to completion,
- describe the difference between greedy matching and optimal (Hungarian) assignment.

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Async Explained](../../../concepts/async-explained.md)
- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Functions Explained](../../../concepts/functions-explained.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../13-legacy-modernization-planner/README.md) | [Home](../../../README.md) | [Next →](../15-level10-grand-capstone/README.md) |
|:---|:---:|---:|
