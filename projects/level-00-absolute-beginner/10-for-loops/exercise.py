# ============================================================
# Exercise 10: For Loops
# ============================================================
#
# A for loop repeats code once for each item in a collection.
# "For each color in my list of colors, print that color."
#
# This is one of the most powerful ideas in programming.
# Instead of writing the same code 100 times, you write it
# once and let the loop repeat it.
# ============================================================

# Loop through a list of items
fruits = ["apple", "banana", "cherry", "date"]

print("My fruits:")
for fruit in fruits:
    # This indented code runs once for each fruit.
    # The variable "fruit" holds a different value each time.
    print(f"  - {fruit}")

# Loop through numbers using range()
# range(5) gives you: 0, 1, 2, 3, 4
print()
print("Counting from 0 to 4:")
for number in range(5):
    print(number)

# range(1, 6) gives you: 1, 2, 3, 4, 5
print()
print("Counting from 1 to 5:")
for number in range(1, 6):
    print(number)

# Use a loop to calculate something
scores = [85, 92, 78, 95, 88]
total = 0

for score in scores:
    total = total + score

average = total / len(scores)
print()
print(f"Scores: {scores}")
print(f"Total: {total}")
print(f"Average: {average}")

# Loop with an if statement inside
print()
print("Numbers from 1 to 10 that are even:")
for number in range(1, 11):
    if number % 2 == 0:
        print(f"  {number} is even")

# ============================================================
# KEY CONCEPT:
#
# The variable name after "for" (like "fruit" or "number") is
# your choice. Pick something descriptive:
#   for student in students:
#   for file in files:
#   for item in shopping_list:
# ============================================================
