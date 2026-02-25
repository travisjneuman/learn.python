# Try This — Exercise 10

1. Print a multiplication table for a number:
   ```python
   number = 7
   for i in range(1, 11):
       print(f"{number} x {i} = {number * i}")
   ```

2. Loop through a list of names and greet each one:
   ```python
   names = ["Alice", "Bob", "Charlie"]
   for name in names:
       print(f"Hello, {name}!")
   ```

3. Use a for loop with `range()` to count backwards from 10 to 1:
   ```python
   for i in range(10, 0, -1):
       print(i)
   print("Liftoff!")
   ```
   The third number in `range()` is the step. `-1` means count down.

---

| [← Prev](../09-lists/TRY_THIS.md) | [Home](../../../README.md) | [Next →](../11-while-loops/TRY_THIS.md) |
|:---|:---:|---:|
