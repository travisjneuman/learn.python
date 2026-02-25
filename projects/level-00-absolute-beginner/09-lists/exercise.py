# ============================================================
# Exercise 09: Lists
# ============================================================
#
# A list is an ordered collection of items.
# Think of it like a numbered shelf where you can store things.
# Lists use square brackets [] and items are separated by commas.
# ============================================================

# Create a list
colors = ["red", "blue", "green", "yellow"]
print("Colors:", colors)

# Access items by position (called "index").
# IMPORTANT: Counting starts at 0, not 1.
print("First color:", colors[0])    # red
print("Second color:", colors[1])   # blue
print("Last color:", colors[-1])    # yellow (-1 means last)

# How many items are in the list?
print("Number of colors:", len(colors))

# Add an item to the end
colors.append("purple")
print("After adding purple:", colors)

# Remove an item by value
colors.remove("blue")
print("After removing blue:", colors)

# Check if something is in the list
if "red" in colors:
    print("Red is in the list!")

if "orange" not in colors:
    print("Orange is NOT in the list.")

# Lists can hold numbers too
scores = [95, 87, 92, 78, 100]
print("Scores:", scores)
print("Highest:", max(scores))
print("Lowest:", min(scores))
print("Total:", sum(scores))
print("Average:", sum(scores) / len(scores))

# Lists can hold a mix of types (but usually you keep them uniform)
mixed = ["Alice", 30, True, 3.14]
print("Mixed list:", mixed)

# Sort a list
numbers = [5, 2, 8, 1, 9, 3]
numbers.sort()
print("Sorted:", numbers)

# ============================================================
# KEY CONCEPT:
#
# Lists are "mutable" — you can change them after creating them.
# This is different from strings, which cannot be changed in place.
# ============================================================
