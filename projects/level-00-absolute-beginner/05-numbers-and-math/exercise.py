# ============================================================
# Exercise 05: Numbers and Math
# ============================================================
#
# Python has two types of numbers:
#   - int (integer): whole numbers like 5, -3, 1000
#   - float (floating point): decimal numbers like 3.14, -0.5
#
# Python can do all basic math operations.
# ============================================================

# Addition
print("5 + 3 =", 5 + 3)

# Subtraction
print("10 - 4 =", 10 - 4)

# Multiplication (use * not x)
print("6 * 7 =", 6 * 7)

# Division (always gives a decimal result)
print("15 / 4 =", 15 / 4)

# Integer division (drops the decimal part)
print("15 // 4 =", 15 // 4)

# Remainder (called "modulo" — what is left over after division)
print("15 % 4 =", 15 % 4)

# Exponent (power)
print("2 ** 8 =", 2 ** 8)

# Order of operations works like math class: parentheses first
print("(2 + 3) * 4 =", (2 + 3) * 4)
print("2 + 3 * 4 =", 2 + 3 * 4)

# Store results in variables
price = 29.99
tax_rate = 0.08
tax_amount = price * tax_rate
total = price + tax_amount

print()
print("Price:", price)
print("Tax:", tax_amount)
print("Total:", total)

# Round a number to 2 decimal places
print("Total (rounded):", round(total, 2))

# ============================================================
# COMMON GOTCHA:
#
# Division with / always gives a float (decimal), even if the
# answer is a whole number:
#   10 / 2 gives 5.0 (not 5)
#
# Use // if you want a whole number result:
#   10 // 2 gives 5
# ============================================================
