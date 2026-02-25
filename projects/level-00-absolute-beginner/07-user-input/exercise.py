# ============================================================
# Exercise 07: User Input
# ============================================================
#
# The input() function pauses your program and waits for the
# user to type something. Whatever they type becomes a string.
#
# This is how you make interactive programs.
# ============================================================

# Ask for the user's name. The text inside input() is the prompt
# that the user sees.
name = input("What is your name? ")

# Now use what they typed.
print(f"Nice to meet you, {name}!")

# Ask for their favorite color.
color = input("What is your favorite color? ")
print(f"{color} is a great color.")

# IMPORTANT: input() always gives you a string, even if the
# user types a number. If you want to do math with it, you
# must convert it.

age_text = input("How old are you? ")

# Convert the string to a number using int()
age = int(age_text)

# Now you can do math with it.
print(f"You will be {age + 1} next year.")

# You can do the conversion on one line:
# age = int(input("How old are you? "))

# ============================================================
# COMMON ERROR:
#
# If the user types something that is not a number (like "abc")
# and you try int("abc"), Python will crash with a ValueError.
# For now, just type valid numbers. Later you will learn how
# to handle bad input gracefully.
# ============================================================
