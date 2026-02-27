# Try This — Project 01

1. Add a new validation type: `"username"`. A valid username should be 3-20 characters long, start with a letter, and contain only letters, digits, and underscores. Add a line like `username: cool_user99` to `data/sample_input.txt` and make sure your validator handles it.

2. Make the output friendlier by adding a suggestion for each failed validation. For example, if an email has no `@`, the error should say something like `"Try: name@example.com"`. Update `validate_email()` to include a `"suggestion"` key in its returned dict alongside the error.

3. Add a `--summary` flag that prints a table at the end showing how many of each type passed and failed:
   ```text
   Type     Passed  Failed
   ------   ------  ------
   email       1       2
   phone       2       0
   zip         0       1
   ```
   Hint: loop through your results and count by type using a dictionary.

---

| [← Prev](../README.md) | [Home](../../../README.md) | [Next →](../02-password-strength-checker/TRY_THIS.md) |
|:---|:---:|---:|
