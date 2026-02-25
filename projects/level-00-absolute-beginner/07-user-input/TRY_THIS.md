# Try This — Exercise 07

1. Build a simple greeting program that asks for first name and last name separately, then prints the full name:
   ```python
   first = input("First name? ")
   last = input("Last name? ")
   print(f"Hello, {first} {last}!")
   ```

2. Build a tip calculator: ask for the meal price and tip percentage, calculate the tip and total:
   ```python
   price = float(input("Meal price: $"))
   tip_pct = float(input("Tip percentage (like 20): "))
   tip = price * (tip_pct / 100)
   print(f"Tip: ${round(tip, 2)}")
   print(f"Total: ${round(price + tip, 2)}")
   ```
   Note: `float()` converts to a decimal number (instead of `int()` which is whole numbers only).

3. What happens if you type a word when the program expects a number? Try it and read the error.
