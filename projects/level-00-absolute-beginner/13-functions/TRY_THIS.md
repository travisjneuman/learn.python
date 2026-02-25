# Try This — Exercise 13

1. Write a function that takes a temperature in Fahrenheit and returns Celsius:
   ```python
   def to_celsius(fahrenheit):
       return (fahrenheit - 32) * 5 / 9

   print(to_celsius(212))  # 100.0
   print(to_celsius(32))   # 0.0
   print(to_celsius(72))   # 22.2...
   ```

2. Write a function that takes a list of numbers and returns the average:
   ```python
   def average(numbers):
       return sum(numbers) / len(numbers)

   print(average([90, 85, 92, 78]))
   ```

3. Write a function called `is_even` that takes a number and returns `True` if it is even, `False` if odd:
   ```python
   def is_even(number):
       return number % 2 == 0

   print(is_even(4))   # True
   print(is_even(7))   # False
   ```

---

| [← Prev](../12-dictionaries/TRY_THIS.md) | [Home](../../../README.md) | [Next →](../14-reading-files/TRY_THIS.md) |
|:---|:---:|---:|
