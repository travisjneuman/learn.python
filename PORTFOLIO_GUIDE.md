# Portfolio Guide — Presenting Your Projects to Employers

Home: [README](./README.md)

You are building real software in this curriculum. This guide shows you how to turn your learn.python projects into a portfolio that gets interviews.

---

## Which Projects Make the Best Portfolio Pieces

Not every project belongs in a portfolio. Employers want to see judgment, not volume. Pick 3–5 of your best projects and present them well.

### High-Impact Projects by Level

| Level | Best Portfolio Projects | Why |
|-------|------------------------|-----|
| 2 | CSV-to-JSON converter, data cleaning pipeline | Shows you handle messy real-world data |
| 3 | Test-driven normalizer, any TDD project | Proves you write tests (most juniors do not) |
| 4 | Transformation pipeline, schema validator | Demonstrates data engineering thinking |
| 5 | Retry-backoff runner, monitoring project | Shows operational awareness |
| 6 | ETL pipeline, incremental load simulator | Database + pipeline skills employers need |
| 7 | API adapter with caching, observability kit | Integration + production-grade patterns |
| 8+ | Any capstone, fault injection harness | Architecture and systems thinking |
| Modules | FastAPI app, Django CRUD, Docker deployment | Framework experience employers search for |

### What Not to Include

- Level 00 exercises (too basic)
- Level 0 projects 01–05 (hello world, calculator — everyone has these)
- Projects where you only followed the instructions without adding anything

---

## How to Present a Project

### The README Template

Every portfolio project needs a README that a hiring manager can read in 60 seconds. Use this structure:

```markdown
# Project Name

One sentence: what it does and why it exists.

## What I Built

2–3 sentences describing the project. Focus on the problem it solves,
not the technologies it uses.

## How to Run It

\```bash
git clone <your-repo-url>
cd project-name
pip install -r requirements.txt
python project.py
\```

## What I Learned

- Bullet point 1: a specific concept you understood by building this
- Bullet point 2: a mistake you made and how you fixed it
- Bullet point 3: what you would do differently next time

## Technical Details

- **Language:** Python 3.11
- **Testing:** pytest (X tests passing)
- **Libraries:** list only the important ones
```

### The "What I Learned" Section Is the Most Important Part

Hiring managers see hundreds of calculator apps. They rarely see candidates who can articulate what they learned. This section separates you from other applicants.

Good examples:
- "I learned that retry logic needs exponential backoff — my first version hammered the API and got rate-limited."
- "I discovered that CSV files from Excel often have invisible BOM characters. I added detection for this after debugging a parsing failure for 2 hours."
- "I refactored this three times. The first version used nested dicts, the second used dataclasses, and the final version used Pydantic models. Each refactor taught me why the previous approach was limited."

Bad examples:
- "I learned Python." (too vague)
- "I learned how to use for loops." (too basic for a portfolio)
- "This was easy." (never say this)

---

## Writing About What You Learned

### The STAR Format for Technical Projects

When describing a project in an interview or cover letter:

- **Situation:** What problem were you solving?
- **Task:** What did you need to build?
- **Action:** What decisions did you make and why?
- **Result:** What did you deliver? What would you improve?

Example: "I needed to build a data pipeline that could handle CSV files with inconsistent formatting (Situation). The pipeline had to clean, validate, and transform the data into a normalized JSON format (Task). I chose to use Pydantic for schema validation because it gives clear error messages when data does not match the expected shape (Action). The pipeline now processes 10,000 rows in under 2 seconds and rejects malformed rows with descriptive error logs (Result)."

### Common Questions Interviewers Ask About Portfolio Projects

Prepare answers for these:

1. "Walk me through this project."
2. "What was the hardest part?"
3. "Why did you choose this approach over alternatives?"
4. "What would you change if you had more time?"
5. "How did you test it?"
6. "How would this scale to 10x the data?"

---

## GitHub Profile Tips for New Developers

### Your Profile README

Create a repository named after your GitHub username (e.g., `yourusername/yourusername`) with a README.md. Keep it short:

```markdown
# Hi, I'm [Name]

I'm learning Python through hands-on projects.
Currently at Level [X] of [learn.python](link-to-your-fork).

## Featured Projects

- [Project Name](link) — one line description
- [Project Name](link) — one line description
- [Project Name](link) — one line description
```

### Repository Hygiene

| Do | Do Not |
|----|--------|
| Pin your 3–5 best repositories | Pin everything |
| Write READMEs for pinned repos | Leave repos with no README |
| Use descriptive commit messages | Use "fix", "update", "stuff" |
| Show a contribution graph (commit regularly) | Commit 100 files once a month |
| Add topics/tags to repositories | Leave repos uncategorized |

### Commit Messages That Show Growth

Your git history tells a story. Make it a good one.

```
# Bad
fix bug
update code
asdf

# Good
fix: handle empty CSV rows instead of crashing
feat: add retry logic with exponential backoff
refactor: extract validation into separate module for testability
```

### The Green Graph

Employers look at your GitHub contribution graph. You do not need to commit every day, but consistent activity over weeks and months signals dedication. Working through this curriculum at a steady pace will naturally produce a healthy graph.

---

## Building Your Portfolio Website

You do not need a portfolio website to get a junior role, but it helps. If you build one:

1. Keep it simple — a single page with your name, a short bio, and links to 3–5 projects
2. Host it for free on GitHub Pages, Netlify, or Vercel
3. Include links to your GitHub profile and LinkedIn
4. Do not include projects you cannot explain in an interview

---

## Career Stage Portfolio Expectations

| Role | What Employers Expect to See |
|------|------------------------------|
| **Intern** | Evidence you can write code that runs. Tests are a bonus. |
| **Junior** | 3–5 projects with tests. Clear READMEs. Shows you can learn. |
| **Mid-level** | Projects showing architecture decisions. System design awareness. |
| **Senior** | Open-source contributions, complex systems, mentoring evidence. |

See [CAREER_READINESS.md](./CAREER_READINESS.md) for a detailed mapping of curriculum levels to job roles.

---

## Final Checklist

Before sharing your portfolio:

- [ ] 3–5 projects pinned on GitHub with READMEs
- [ ] Each README follows the template above
- [ ] Each project has passing tests (`python -m pytest tests/`)
- [ ] Your commit history shows real iteration (not a single bulk commit)
- [ ] You can explain every project in 2 minutes or less
- [ ] Your GitHub profile has a bio and profile README

---

| [← Teaching Guide](./TEACHING_GUIDE.md) | [Home](./README.md) | [Career Readiness →](./CAREER_READINESS.md) |
|:---|:---:|---:|
