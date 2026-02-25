# Frequently Asked Questions

Common questions from learners, with straight answers.

---

## Getting Started

### Do I need prior programming experience?

No. Level 00 starts from absolute zero -- it explains what a terminal is, what a file is, and what it means to run a program. If you have never written a line of code, that is exactly where this curriculum begins.

### What IDE or editor should I use?

[VS Code](https://code.visualstudio.com/) is recommended because it is free, cross-platform, and has excellent Python support. But any text editor works -- Sublime Text, PyCharm, Notepad++, even the terminal-based editors (nano, vim) if you prefer. The curriculum does not depend on any specific editor.

### What version of Python do I need?

Python 3.11 or newer. The setup guide ([03_SETUP_ALL_PLATFORMS.md](./03_SETUP_ALL_PLATFORMS.md)) covers installation for Windows, Mac, and Linux.

### Where do I start?

Open [START_HERE.md](./START_HERE.md). It will have you running Python in under 10 minutes. For a more detailed orientation, read [GETTING_STARTED.md](./GETTING_STARTED.md).

---

## Pacing and Progress

### How long will this take?

The full curriculum is approximately 400-500 hours of work. At 10 hours per week, that is roughly one year. At 5 hours per week, roughly two years. See [GETTING_STARTED.md](./GETTING_STARTED.md) for a detailed breakdown by level.

### Can I skip levels?

Not recommended. Each level builds on skills from the previous one. If you think you already know the material, run the diagnostic tool to find your appropriate starting level:

```bash
python tools/diagnose.py
```

This will test your knowledge and suggest where to begin.

### Do I need to do every single project in a level?

You should attempt all 15 projects in each level. The first few in each level reinforce core patterns, and the last one is a capstone that ties everything together. Skipping projects leaves gaps that show up later.

### How do I track my progress?

Run the progress tracker:

```bash
python tools/progress.py
```

You can also manually update [PROGRESS.md](./PROGRESS.md) as you complete projects.

---

## Expansion Modules

### Do I need to do all expansion modules?

No. Expansion modules are optional specializations. Pick the ones that match your interests or career goals. Modules 01-03 (Web Scraping, CLI Tools, REST APIs) are broadly useful. Modules like 10 (Django) or 12 (Cloud Deploy) are for specific career paths.

### What order should I do the modules in?

The [README](./README.md) has a suggested order based on prerequisites. In short: Modules 01-03 and 07 after Level 2. Modules 04-06, 08, 11 after Level 3. Modules 09-10, 12 after Level 5.

---

## Troubleshooting

### What if my tests fail?

1. **Read the error message.** The last line tells you what went wrong. The lines above it show you where.
2. **Check the expected output.** Each project README shows what the output should look like.
3. **Re-read the concept doc.** The project links to related concepts -- review those sections.
4. **Add print statements.** Print the value of variables to see what your code is actually doing vs. what you expect.
5. **Compare with the "Run" command.** Make sure you are in the right directory and using the correct command.

### I get "ModuleNotFoundError" -- what do I do?

This means Python cannot find a library you are trying to import. Common causes:

- You have not installed the required packages. Check if the project has a `requirements.txt` and run `pip install -r requirements.txt`.
- You are not in a virtual environment. See the [Virtual Environments](./concepts/virtual-environments.md) concept guide.
- You have multiple Python installations and pip installed the package to the wrong one. Try `python -m pip install <package>` instead of just `pip install`.

### I get "FileNotFoundError" -- what do I do?

Python cannot find the file you are trying to open. Common causes:

- You are not in the project directory. Run `cd` to the project folder before running the script.
- The filename is misspelled. Check for typos, including capitalization.
- The file path uses the wrong separator. On Windows, use forward slashes (`/`) or raw strings (`r"path\to\file"`).

### My code runs but produces wrong output

1. Print your variables at key points to see their actual values.
2. Walk through your code line by line with a small example.
3. Check if you are reading the right input file.
4. Make sure you are not confusing `=` (assignment) with `==` (comparison).

---

## Curriculum and Licensing

### Can I use this curriculum in a classroom?

Yes. This curriculum is MIT licensed. You can use it for teaching, workshops, bootcamps, or any educational purpose. Attribution is appreciated but not required.

### I found a bug or broken link. How do I report it?

[Open an issue](https://github.com/travisjneuman/learn.python/issues) on GitHub. Include which file has the problem and what you expected vs. what you found.

### Can I contribute?

Yes. See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines. Bug fixes, improved explanations, and new test cases are especially welcome.

---

| [← Prev](START_HERE.md) | [Home](README.md) | [Next →](00_COMPUTER_LITERACY_PRIMER.md) |
|:---|:---:|---:|
