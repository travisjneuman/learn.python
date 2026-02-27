"""Learn to open, read, and parse data from text files line by line."""
# ============================================================
# Exercise 14: Reading Files
# ============================================================
#
# Programs need to read data from files — spreadsheets, logs,
# configuration, reports. Reading a file is one of the most
# common things you will do.
#
# Python's open() function opens a file.
# .read() gets all the text at once.
# .readlines() gets each line as a separate item in a list.
#
# RUN THIS: python exercise.py
# (Make sure you are in the 14-reading-files folder)
# ============================================================

# Read the entire file as one big string
contents = open("data/sample.txt").read()
print("--- Raw file contents ---")
print(contents)

# Read the file line by line
print("--- Line by line ---")
lines = open("data/sample.txt").readlines()

for line in lines:
    # .strip() removes the newline character at the end of each line
    clean_line = line.strip()
    if clean_line:  # Skip empty lines
        print(clean_line)

# Parse the data — each line has "name,score"
print()
print("--- Parsed data ---")

names = []
scores = []

for line in open("data/sample.txt"):
    line = line.strip()
    if not line:
        continue  # Skip empty lines

    # .split(",") breaks the line at every comma
    parts = line.split(",")
    name = parts[0]
    score = int(parts[1])

    names.append(name)
    scores.append(score)

    print(f"  {name}: {score}")

# Calculate stats from the file data
print()
print(f"Students: {len(names)}")
print(f"Highest score: {max(scores)}")
print(f"Lowest score: {min(scores)}")
print(f"Average: {sum(scores) / len(scores)}")

# ============================================================
# THE BETTER WAY (you will learn this in Level 0):
#
# Using "with open()" is safer because it automatically closes
# the file when you are done:
#
#   with open("data/sample.txt") as f:
#       for line in f:
#           print(line.strip())
#
# For now, the simpler open() style works fine for learning.
# ============================================================
