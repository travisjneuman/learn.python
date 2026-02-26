# Module 02 / Project 03 -- Interactive Prompts

Home: [README](../../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus

- `click.prompt()` to ask the user for input
- `click.confirm()` to ask yes/no questions
- `click.echo()` with `click.style()` for colored terminal output
- Building an interactive experience inside a CLI

## Why this project exists

Not every CLI is a one-shot command. Sometimes you need to ask the user questions, confirm dangerous actions, or highlight results with color. Click provides prompt, confirm, and styling utilities that handle edge cases (encoding, piped input, Windows terminals) so you do not have to. This project builds an interactive quiz to put all three to work.

## Run

```bash
cd projects/modules/02-cli-tools/03-interactive-prompts

# Run the quiz (interactive)
python project.py

# Run with a specific number of questions
python project.py --questions 3

# Skip the welcome confirmation
python project.py --no-confirm
```

## Expected output

```text
$ python project.py --questions 2
Welcome to the Python Quiz!
Ready to start? [Y/n]: y

Question 1 of 2
What keyword defines a function in Python? def
Correct!

Question 2 of 2
What built-in function returns the length of a list? len
Correct!

Final score: 2/2
Great job!
```

(Colors will appear in your terminal -- green for correct, red for incorrect.)

## Alter it

1. Add three new questions to the quiz bank.
2. Add a `--shuffle` flag that randomizes the question order.
3. After the quiz, prompt the user for their name and write the score to a `scores.txt` file.

## Break it

1. Replace `click.prompt()` with Python's built-in `input()`. Run the script and pipe input from a file (`echo "def" | python project.py`). Compare the behavior.
2. Remove the `click.style()` calls and use plain `click.echo()`. Note what you lose.
3. Change `click.confirm()` to `click.prompt()` with no default. What happens when the user presses Enter without typing anything?

## Fix it

1. Restore `click.prompt()` and verify piped input works again.
2. Restore the `click.style()` calls and confirm colors appear.
3. Restore `click.confirm()` and verify that pressing Enter defaults to "yes".

## Explain it

1. What does `click.prompt()` handle that `input()` does not?
2. How does `click.style()` apply color -- what terminal standard does it use?
3. Why does `click.confirm(abort=True)` exist and when would you use it?
4. What happens to colors when you redirect output to a file (`python project.py > output.txt`)?

## Mastery check

You can move on when you can:
- use `click.prompt()` with type conversion (e.g., `type=int`),
- style output with foreground color, bold, and underline,
- build an interactive flow that asks questions and acts on answers,
- explain why `click.echo()` is preferred over `print()` in Click apps.

---

## Related Concepts

- [Functions Explained](../../../../concepts/functions-explained.md)
- [How Imports Work](../../../../concepts/how-imports-work.md)
- [How Loops Work](../../../../concepts/how-loops-work.md)
- [The Terminal Deeper](../../../../concepts/the-terminal-deeper.md)
- [Quiz: Functions Explained](../../../../concepts/quizzes/functions-explained-quiz.py)

## Next

Continue to [04 - File Processor CLI](../04-file-processor-cli/).
