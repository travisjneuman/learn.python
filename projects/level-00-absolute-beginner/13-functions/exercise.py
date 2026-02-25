# ============================================================
# Exercise 13: Functions
# ============================================================
#
# A function is a reusable block of code with a name.
# Instead of writing the same code over and over, you put it
# in a function and call it whenever you need it.
#
# You define a function with "def", give it a name, and put
# the code inside (indented).
# ============================================================

# Define a simple function
def say_hello():
    print("Hello! This message comes from a function.")

# Call (use) the function
say_hello()
say_hello()  # You can call it as many times as you want

# Functions with parameters — values you pass in
def greet(name):
    print(f"Hello, {name}! Nice to meet you.")

greet("Travis")
greet("Alice")
greet("Bob")

# Functions that return a value
def add(a, b):
    result = a + b
    return result  # "return" sends the value back to whoever called it

total = add(5, 3)
print(f"5 + 3 = {total}")

# You can use the returned value directly
print(f"10 + 20 = {add(10, 20)}")

# Functions with default values
def make_greeting(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(make_greeting("Travis"))              # Uses default: "Hello"
print(make_greeting("Travis", "Hey"))       # Uses provided: "Hey"
print(make_greeting("Travis", "Welcome"))   # Uses provided: "Welcome"

# A more practical function
def calculate_tip(meal_price, tip_percent=18):
    tip = meal_price * (tip_percent / 100)
    total = meal_price + tip
    return round(total, 2)

print()
print(f"$50 meal, 18% tip: ${calculate_tip(50)}")
print(f"$50 meal, 20% tip: ${calculate_tip(50, 20)}")
print(f"$75 meal, 15% tip: ${calculate_tip(75, 15)}")

# ============================================================
# WHY FUNCTIONS MATTER:
#
# 1. Reusability — write code once, use it many times
# 2. Organization — break big problems into small pieces
# 3. Readability — a well-named function explains what it does
# 4. Testing — you can test each function independently
#
# If you find yourself copying and pasting code, that is a
# sign you should put it in a function.
# ============================================================
