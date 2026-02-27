# Try This — Project 02

1. Add a new scoring rule: check whether the password contains three or more consecutive identical characters (like `"aaa"` or `"111"`). If it does, subtract 1 point from the total score. Hint: loop through the password with `range(len(password) - 2)` and compare `password[i]`, `password[i+1]`, and `password[i+2]`.

2. Add a `--generate` flag that creates a random strong password instead of checking one. Use `random.choice()` to pick characters from uppercase, lowercase, digits, and symbols until the password scores at least 7/8:
   ```python
   import random
   import string
   chars = string.ascii_letters + string.digits + string.punctuation
   password = "".join(random.choice(chars) for _ in range(16))
   ```

3. Make the output show exactly which character classes are missing. Instead of just printing the score, print something like:
   ```text
   "abc123" => Score: 3/8 (weak)
     Missing: uppercase, special character
   ```
   Use the `variety` dict from `check_character_variety()` to find which classes are `False`.

---

| [← Prev](../01-input-validator-lab/TRY_THIS.md) | [Home](../../../README.md) | [Next →](../03-unit-price-calculator/TRY_THIS.md) |
|:---|:---:|---:|
