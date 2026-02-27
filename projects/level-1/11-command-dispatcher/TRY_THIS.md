# Try This — Project 11

1. Add three new commands to the dispatcher: `snake` (converts text to snake_case), `length` (returns the character count), and `initials` (returns the first letter of each word). Register them in the `COMMANDS` dict:
   ```python
   def cmd_snake(text: str) -> str:
       return text.lower().replace(" ", "_")

   # "Hello World" => "H.W."
   def cmd_initials(text: str) -> str:
       words = text.split()
       return ".".join(w[0].upper() for w in words if w) + "."
   ```

2. Add command chaining so a user can write multiple commands separated by `|` on a single line. Each command's output becomes the next command's input:
   ```text
   upper | reverse  hello world
   ```
   This should first run `upper("hello world")` to get `"HELLO WORLD"`, then run `reverse("HELLO WORLD")` to get `"DLROW OLLEH"`. Hint: split the command part on `|`, then loop through each command, passing the result forward.

3. Add a `help` command that prints a description of every available command. Pull the description from each function's docstring using `handler.__doc__`:
   ```text
   Available commands:
     upper    — Convert text to uppercase.
     lower    — Convert text to lowercase.
     reverse  — Reverse the text.
     count    — Count words in the text.
     title    — Convert text to title case.
   ```

---

| [← Prev](../10-ticket-priority-router/TRY_THIS.md) | [Home](../../../README.md) | [Next →](../12-file-extension-counter/TRY_THIS.md) |
|:---|:---:|---:|
