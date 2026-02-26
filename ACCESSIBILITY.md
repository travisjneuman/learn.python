# Accessibility Guide

Home: [README](./README.md)

This curriculum is designed to be usable by everyone, regardless of ability. This guide covers how to navigate and use learn.python with assistive technologies, and how to request accommodations.

---

## Screen Reader Navigation

The entire curriculum is plain Markdown. Screen readers handle Markdown well because it uses semantic headings, lists, and tables rather than custom widgets.

**Tips for screen reader users:**

- Use heading navigation (H key in most screen readers) to jump between sections. Every document uses a consistent heading hierarchy: H1 for the title, H2 for major sections, H3 for subsections.
- Tables use standard Markdown syntax. Most screen readers announce row and column headers automatically.
- Code blocks are fenced with triple backticks. Your screen reader will announce "code block" or similar. The content inside is plain text.
- Navigation links at the bottom of each document follow the pattern: Previous | Home | Next. Use your screen reader's link navigation to find them.
- File paths use forward slashes and are written as inline code. They read naturally in most screen readers.

**Recommended screen readers:**

| Platform | Screen Reader | Notes |
|----------|---------------|-------|
| Windows | NVDA (free) | Works well with VS Code and terminal |
| Windows | JAWS | Commercial, excellent VS Code support |
| macOS | VoiceOver (built-in) | Activate with Cmd+F5 |
| Linux | Orca (built-in on GNOME) | Works with terminal applications |

---

## Visual Accessibility

### High Contrast and Large Text

**In your code editor:**

- VS Code: Settings > Accessibility > High Contrast Theme. Also try "High Contrast Light" or "High Contrast Dark."
- VS Code: Settings > Editor: Font Size. Set to 16px or higher for comfortable reading.
- Thonny: Tools > Options > Theme > select a high-contrast theme.

**In your terminal:**

- Most terminals let you increase font size with Ctrl+Plus (Cmd+Plus on macOS).
- Windows Terminal: Settings > Profiles > Appearance > Font size.
- macOS Terminal: Preferences > Profiles > Text > Font > Change.

**In your browser (for reading docs on GitHub):**

- Zoom in with Ctrl+Plus (Cmd+Plus on macOS). GitHub's Markdown rendering scales cleanly.
- Browser extensions like "Dark Reader" can add high-contrast themes to GitHub.

### Color Considerations

This curriculum does not rely on color to convey information. All code output, test results, and instructions use text labels alongside any color coding. If you encounter a place where color is the only indicator, please open an issue so we can fix it.

---

## Cognitive Accessibility

Learning to code is cognitively demanding. These strategies help manage that load.

### Chunking

Every level is broken into 15 small projects. Each project focuses on one concept. You are never asked to learn multiple new ideas in a single project. Work through one project at a time. Take a break between projects if needed.

### Pacing

There are no deadlines. The curriculum is self-paced. The recommended approach is:

- Work for 25-50 minutes, then take a 5-10 minute break (Pomodoro technique).
- Stop when you feel frustrated. Come back later with fresh eyes.
- Repeat a project if you did not fully understand it. Repetition is learning, not failure.

### One Concept at a Time

The curriculum introduces concepts in strict order. Each document builds on the previous one. If something feels confusing, go back one document and review. The confusion usually means a prerequisite concept needs reinforcement.

### Predictable Structure

Every project follows the same structure so you always know what to expect:

- **Level 00:** `exercise.py` + `TRY_THIS.md` (two files, nothing else)
- **Level 0 onward:** `README.md` (instructions), `project.py` (starter code), `tests/` (validation), `notes.md` (your notes)

This consistency reduces the cognitive overhead of figuring out "where do I start?" for each new project.

### Error Messages

Error messages are normal and expected. The curriculum teaches you to read them starting in Level 00. If an error message feels overwhelming, focus on the last line first. It usually contains the most useful information.

---

## Alternative Formats

### Diagrams and Visual Content

Where the curriculum includes diagrams or visual representations, a text description accompanies them. If you find a visual without a text alternative, please open an issue.

### Audio and Video

The curriculum is entirely text-based. There are no required audio or video components. If community members create video companions (see [Creator Kit](./CREATOR_KIT.md)), we encourage them to include captions and transcripts.

### Offline Access

Clone the repository and read all documents locally. Everything works offline except external links to documentation sites.

```bash
git clone https://github.com/travisjneuman/learn.python.git
cd learn.python
# All curriculum files are now on your machine
```

---

## Accessible Code Editors

These editors work well with assistive technologies and are suitable for beginners.

### VS Code (Recommended)

VS Code has strong accessibility support built in:

- Full screen reader support (NVDA, JAWS, VoiceOver, Orca)
- High-contrast themes included by default
- Keyboard-only navigation for all features
- Adjustable font size, line height, and letter spacing
- Tab focus mode (Tab key moves focus instead of inserting a tab)
- Accessible terminal built in

**Enable accessibility mode:** Press Ctrl+Shift+P, type "Accessibility," and explore the options.

### Thonny

Thonny is designed for beginners and has a simpler interface:

- Fewer menus and panels to navigate
- Built-in Python interpreter (no terminal setup required)
- Step-through debugger with visual feedback
- Works with screen readers on Windows and macOS
- Download: [thonny.org](https://thonny.org)

### IDLE

Python's built-in editor works on all platforms and has basic accessibility:

- Simple interface with few distractions
- Comes pre-installed with Python
- Works with screen readers
- Limited compared to VS Code, but sufficient for Level 00 through Level 2

---

## Motor Accessibility

### Keyboard-Only Workflows

The entire curriculum can be completed without a mouse:

- **Editor:** VS Code supports full keyboard navigation. Press Ctrl+Shift+P for the command palette.
- **Terminal:** All commands are typed. No mouse interaction needed.
- **Git:** All operations are command-line based.

### Voice Coding

If you use voice input, Python's clean syntax works well with dictation:

- Short keywords: `def`, `for`, `if`, `return`
- Indentation-based structure (configure your editor to use spaces, typically 4)
- Tools like Talon or Windows Voice Typing can be used for coding

### Repetitive Strain

If extended typing is uncomfortable:

- Use the Pomodoro technique (25 minutes on, 5 minutes off)
- The Level 00 exercises are intentionally short (under 10 lines each)
- Consider an ergonomic keyboard layout or split keyboard

---

## Requesting Accommodations

If you need an accommodation not covered here, or if you find an accessibility barrier in the curriculum:

1. **Open an issue** on GitHub with the label `accessibility`
2. Describe what you need and which part of the curriculum is affected
3. We will respond and work toward a solution

You can also start a discussion in [GitHub Discussions](https://github.com/travisjneuman/learn.python/discussions) if you prefer a less formal channel.

---

## Reporting Accessibility Issues

Found something that does not work with your assistive technology? Please report it:

- **GitHub Issues:** Use the "Bug Report" template and add the `accessibility` label
- **What to include:** The document or project affected, the assistive technology you use, what you expected to happen, and what actually happened

Every accessibility report helps make this curriculum better for the next learner.

---

| [← README](./README.md) | [Home](./README.md) | [Getting Started →](./GETTING_STARTED.md) |
|:---|:---:|---:|
