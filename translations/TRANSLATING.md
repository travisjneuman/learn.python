# Translating the learn.python Curriculum

Thank you for helping make Python education accessible to more people. This guide explains how to contribute a translation.

## Before You Start

1. Check the [translations README](./README.md) to see which languages are in progress.
2. Open an issue titled "Translation: [Language Name]" to claim a language or join an existing effort.
3. Read this entire guide before translating anything.

## What to Translate First

Start with the documents learners encounter earliest. This order maximizes impact:

| Priority | File | Why |
|----------|------|-----|
| 1 | `README.md` | First impression, decides if someone continues |
| 2 | `START_HERE.md` | Immediate onboarding |
| 3 | `00_COMPUTER_LITERACY_PRIMER.md` | Absolute beginners need native language most |
| 4 | `GETTING_STARTED.md` | Setup and pacing guidance |
| 5 | `FAQ.md` | Common questions |
| 6 | Level 00 exercises (`projects/level-00-absolute-beginner/`) | First hands-on experience |
| 7 | Concept guides (`concepts/`) | Reference material |

## Style Guide

### Keep Code in English

All Python code, variable names, function names, and file names stay in English. Translate only:

- Explanatory text and prose
- Comments inside code blocks
- Print statement strings (when they are instructional, not functional)
- Error message explanations

**Example:**

```python
# GOOD: Translate the comment, keep the code
# Esta funcion calcula el promedio de una lista de numeros
def calculate_average(numbers):
    return sum(numbers) / len(numbers)

# BAD: Do not translate code
def calcular_promedio(numeros):
    return sum(numeros) / len(numeros)
```

### Translate Technical Terms Carefully

- Use the accepted translation for technical terms in your language community.
- When a term has no widely accepted translation, keep the English term and add an explanation in parentheses the first time it appears.
- Be consistent: once you choose a translation for a term, use it everywhere.

### Preserve Structure

- Keep all headings, links, and formatting identical to the source.
- Keep file names in English (do not translate file names).
- Update internal links to point to the translated versions where they exist, and to the English originals where they do not.

### Tone

- Match the original tone: clear, encouraging, direct.
- Use informal address if your language distinguishes formality (tu/vous, tu/usted).
- Avoid overly academic or formal phrasing.

## How to Submit a Translation

### Setup

1. Fork the repository.
2. Create a branch: `translation/[language-code]` (e.g., `translation/es`).
3. Work inside `translations/[language-code]/`.

### File Organization

Mirror the source directory structure:

```
translations/es/
  README.md                    -- translated README
  START_HERE.md                -- translated START_HERE
  00_COMPUTER_LITERACY_PRIMER.md
  concepts/
    what-is-a-variable.md
    how-loops-work.md
  projects/
    level-00-absolute-beginner/
      README.md
```

### Pull Request Process

1. Submit one PR per document or small group of related documents.
2. Title format: `translation(es): README.md` or `translation(pt-BR): Level 00 exercises`.
3. In the PR description, note any terms where you made a translation choice that others should follow.
4. Request review from another native speaker if possible.

## Quality Checklist

Before submitting, verify:

- [ ] All code blocks are unchanged (English variable names, function names)
- [ ] All internal links work (point to translated or English originals)
- [ ] Markdown formatting renders correctly
- [ ] Technical terms are consistent throughout the document
- [ ] Tone matches the original (clear, encouraging, direct)
- [ ] No machine translation artifacts (awkward phrasing, literal translations)
- [ ] Document has been read aloud for natural flow
- [ ] Navigation links (Prev/Next) updated where applicable

## Getting Help

- Open an issue with the `translation` label for questions.
- Tag the language maintainer (listed in the translations README) for review.
- Join the Discussions board to coordinate with other translators.
