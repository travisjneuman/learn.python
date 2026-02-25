# ============================================================
# Exercise 06: Strings and Text
# ============================================================
#
# A "string" is any text inside quotes.
# Strings are one of the most common things you will work with.
# ============================================================

# Creating strings
greeting = "Hello"
name = "Alice"

# Combining strings (concatenation) — glues them together
message = greeting + ", " + name + "!"
print(message)

# f-strings — the modern, clean way to put variables inside text.
# Put an f before the opening quote, then use {variable_name} inside.
print(f"Hello, {name}! Welcome to Python.")

# You can put any expression inside the curly braces.
age = 30
print(f"{name} is {age} years old.")
print(f"In 10 years, {name} will be {age + 10}.")

# String length — how many characters (including spaces)
sentence = "Python is fun"
print(f"The sentence '{sentence}' has {len(sentence)} characters.")

# Uppercase and lowercase
print("hello".upper())     # HELLO
print("HELLO".lower())     # hello
print("hello".title())     # Hello

# Checking what a string contains
email = "user@example.com"
print(f"Does the email contain @? {'@' in email}")

# Replacing text
old_text = "I like Java"
new_text = old_text.replace("Java", "Python")
print(new_text)

# Splitting a string into a list of words
words = "one two three four".split()
print(words)

# ============================================================
# KEY CONCEPT:
#
# Strings are "immutable" — you cannot change them in place.
# When you call .upper() or .replace(), Python creates a NEW
# string. The original is unchanged unless you reassign it.
# ============================================================
