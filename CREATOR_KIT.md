# Creator Kit — Make Content About learn.python

Home: [README](./README.md)

This guide is for YouTubers, bloggers, streamers, and educators who want to create companion content for the learn.python curriculum. Use any part of this curriculum in your content. It is MIT-licensed.

---

## Curriculum Overview (For Your Audience)

learn.python is a free, open-source Python curriculum with 246 hands-on projects spanning 13 levels and 12 expansion modules. It takes a learner from "what is a terminal?" to deploying production applications. Everything is plain Markdown and Python files in a single GitHub repository.

**Key selling points for your audience:**

- Free and open-source (MIT license)
- No videos required — entirely text-based and self-paced
- 246 real projects, not toy examples
- Every document links to the next — learners never get lost
- Includes tests, quizzes, flashcards, and coding challenges
- Works on Windows, macOS, and Linux

---

## Suggested Video/Article Topics by Level

### Absolute Beginner Content (Highest Audience)

| Topic | Curriculum Link | Format Suggestion |
|-------|----------------|-------------------|
| "I Tried Learning Python From Zero" | Level 00 exercises | Vlog / screen recording |
| "Python in 10 Minutes — First Script" | [01-first-steps](./projects/level-00-absolute-beginner/01-first-steps/) | Tutorial |
| "What Happens When You Run Python?" | [00_COMPUTER_LITERACY_PRIMER.md](./00_COMPUTER_LITERACY_PRIMER.md) | Explainer |
| "Variables Explained (No CS Degree Needed)" | [What Is a Variable](./concepts/what-is-a-variable.md) | Explainer |
| "Your First Passing Test in Python" | [01-terminal-hello-lab](./projects/level-0/01-terminal-hello-lab/) | Tutorial |

### Beginner Content

| Topic | Curriculum Link | Format Suggestion |
|-------|----------------|-------------------|
| "Build a Calculator in Python" | [02-calculator-basics](./projects/level-0/02-calculator-basics/) | Code-along |
| "Reading Files in Python (Beginner)" | [07-first-file-reader](./projects/level-0/07-first-file-reader/) | Tutorial |
| "CSV Files in Python — First Reader" | [05-csv-first-reader](./projects/level-1/05-csv-first-reader/) | Tutorial |
| "Password Strength Checker in Python" | [02-password-strength-checker](./projects/level-1/02-password-strength-checker/) | Build video |
| "Python Loops Explained With Projects" | [How Loops Work](./concepts/how-loops-work.md) | Explainer |

### Intermediate Content

| Topic | Curriculum Link | Format Suggestion |
|-------|----------------|-------------------|
| "Data Cleaning Pipeline in Python" | [03-data-cleaning-pipeline](./projects/level-2/03-data-cleaning-pipeline/) | Tutorial |
| "CSV to JSON Converter" | [12-csv-to-json-converter](./projects/level-2/12-csv-to-json-converter/) | Build video |
| "Retry Patterns in Python" | [11-retry-loop-practice](./projects/level-2/11-retry-loop-practice/) | Explainer |
| "Web Scraping With BeautifulSoup" | [Module 01: Web Scraping](./projects/modules/01-web-scraping/) | Tutorial series |
| "Build a CLI Tool With Typer" | [Module 02: CLI Tools](./projects/modules/02-cli-tools/) | Build video |

### Advanced Content

| Topic | Curriculum Link | Format Suggestion |
|-------|----------------|-------------------|
| "FastAPI From Scratch" | [Module 04: FastAPI](./projects/modules/04-fastapi-web/) | Tutorial series |
| "Async Python Explained" | [Module 05: Async Python](./projects/modules/05-async-python/) | Deep dive |
| "Django Full-Stack App" | [Module 10: Django](./projects/modules/10-django-fullstack/) | Multi-part series |
| "Docker for Python Developers" | [Module 09: Docker](./projects/modules/09-docker-deployment/) | Tutorial |
| "Deploy Python to Production" | [Module 12: Cloud Deploy](./projects/modules/12-cloud-deploy/) | Walkthrough |

### Meta / Series Ideas

| Topic | Description |
|-------|-------------|
| "30-Day Python Challenge" | Follow the [30-Day Challenge](./30_DAY_PYTHON_CHALLENGE.md) and film daily progress |
| "Python Curriculum Review" | Review the overall structure, compare to other learning paths |
| "Level-Up Series" | One video per level, showing the projects and what you learn |
| "Expansion Module Spotlight" | Deep dive into one module per video |
| "Beginner Mistakes in Python" | Use common mistakes from the curriculum (see Teaching Guide) |

---

## Project Descriptions for Thumbnails/Titles

Short, punchy descriptions suitable for video thumbnails and blog post titles:

| Project | Thumbnail-Ready Title |
|---------|----------------------|
| 02-calculator-basics | "Build a Python Calculator" |
| 02-password-strength-checker | "Is Your Password Strong Enough?" |
| 05-csv-first-reader | "Read Any CSV File in Python" |
| 03-data-cleaning-pipeline | "Clean Messy Data in Python" |
| 12-csv-to-json-converter | "Convert CSV to JSON in Python" |
| 08-mini-inventory-engine | "Build an Inventory System" |
| Module 01 | "Scrape Any Website With Python" |
| Module 04 | "Build an API in 30 Minutes" |
| Module 10 | "Full-Stack Python With Django" |

---

## How to Credit learn.python

We appreciate credit but do not require it (MIT license). If you want to credit the project:

**In video descriptions or blog posts:**

```
Curriculum: learn.python by Travis Neuman
https://github.com/travisjneuman/learn.python
License: MIT (free to use, share, and modify)
```

**In spoken content:**

> "This project is from learn.python, a free open-source Python curriculum on GitHub. Link in the description."

**If you modify projects for your content,** that is completely fine. The MIT license allows modification and redistribution with attribution.

---

## Embedding and Linking Guidelines

**Linking to projects:** Link directly to the project directory on GitHub. The README in each project directory serves as the landing page.

```
https://github.com/travisjneuman/learn.python/tree/main/projects/level-0/02-calculator-basics
```

**Linking to concept guides:** Link to the Markdown file on GitHub. It renders nicely in the browser.

```
https://github.com/travisjneuman/learn.python/tree/main/concepts/how-loops-work.md
```

**Embedding code:** You are free to show code from the repository in your content. The MIT license covers this.

**Forking for content:** If you want to create a modified version for your audience (for example, adding your own exercises), fork the repository and customize it. Link back to the original.

---

## Share Your Content

If you create content about learn.python, we want to know about it. Open a pull request to add your content to a community content list:

1. Fork the repository
2. Add your content link and description to `COMMUNITY_CONTENT.md` (create it if it does not exist)
3. Open a pull request with the title: "Add community content: [Your Content Title]"

We will review and merge pull requests that link to genuine educational content related to the curriculum.

---

## Content Creation Tips

**What works well:**

- Screen recordings of solving projects in real time (including mistakes and debugging)
- Side-by-side comparisons: "How I solved it vs. the test expectations"
- "What I learned" reflections after completing a level
- Explanations of WHY the curriculum teaches things in a particular order

**What to avoid:**

- Posting full solutions without explanation (this undermines the learning process)
- Claiming the curriculum as your own creation
- Modifying tests to make incorrect solutions pass

**Accessibility:** If you create video content, please consider adding captions and transcripts. See our [Accessibility Guide](./ACCESSIBILITY.md) for more context on why this matters.

---

## Questions

Open an issue on GitHub with the label `community` or start a discussion in [GitHub Discussions](https://github.com/travisjneuman/learn.python/discussions).

---

| [← README](./README.md) | [Home](./README.md) | [Contributing →](./CONTRIBUTING.md) |
|:---|:---:|---:|
