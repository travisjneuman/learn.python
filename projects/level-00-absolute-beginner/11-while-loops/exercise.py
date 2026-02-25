# ============================================================
# Exercise 11: While Loops
# ============================================================
#
# A while loop repeats code as long as a condition is True.
# "While this is true, keep doing this."
#
# For loops are for "do this for each item."
# While loops are for "keep doing this until something changes."
# ============================================================

# Count from 1 to 5 using a while loop
count = 1

while count <= 5:
    print(f"Count is: {count}")
    count = count + 1  # This is critical! Without it, the loop never ends.

print("Done counting!")

# A countdown
print()
countdown = 5

while countdown > 0:
    print(countdown)
    countdown = countdown - 1

print("Go!")

# Using a while loop for user input validation
# (This keeps asking until the user gives a valid answer)
print()
print("--- Guessing Game ---")

secret = 7
guess = 0  # Start with a wrong value so the loop runs at least once

while guess != secret:
    guess = int(input("Guess a number between 1 and 10: "))
    if guess < secret:
        print("Too low!")
    elif guess > secret:
        print("Too high!")

print("You got it!")

# Using "break" to exit a loop early
print()
print("--- Type 'quit' to stop ---")

while True:  # This loop would run forever without a break
    text = input("Say something: ")
    if text == "quit":
        break  # Immediately exits the loop
    print(f"You said: {text}")

print("Goodbye!")

# ============================================================
# WARNING:
#
# If you forget to change the condition (like forgetting
# count = count + 1), the loop runs forever. This is called
# an "infinite loop." If this happens, press Ctrl+C in your
# terminal to stop the program.
# ============================================================
