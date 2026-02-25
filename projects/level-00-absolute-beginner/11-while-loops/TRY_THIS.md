# Try This — Exercise 11

1. Write a while loop that doubles a number until it exceeds 1000:
   ```python
   number = 1
   while number <= 1000:
       print(number)
       number = number * 2
   ```

2. Build a password checker that keeps asking until the correct password is entered:
   ```python
   correct = "python"
   attempt = ""
   while attempt != correct:
       attempt = input("Enter password: ")
   print("Welcome!")
   ```

3. Intentionally create an infinite loop (a loop that never stops). Then press Ctrl+C to stop it. Getting comfortable with Ctrl+C is important — you will need it when debugging.
   ```python
   while True:
       print("This will never stop on its own!")
   ```

---

| [← Prev](../10-for-loops/TRY_THIS.md) | [Home](../../../README.md) | [Next →](../12-dictionaries/TRY_THIS.md) |
|:---|:---:|---:|
