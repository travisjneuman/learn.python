# ============================================================
# Exercise 12: Dictionaries
# ============================================================
#
# A dictionary stores data as key-value pairs.
# Think of it like a real dictionary: you look up a word (key)
# and get its definition (value).
#
# Lists use positions (index 0, 1, 2...).
# Dictionaries use labels (keys) to find values.
#
# Dictionaries use curly braces {} and colons between key:value.
# ============================================================

# Create a dictionary
person = {
    "name": "Travis",
    "age": 30,
    "city": "Denver",
    "job": "Engineer"
}

# Access a value by its key
print("Name:", person["name"])
print("Age:", person["age"])

# Print the whole dictionary
print("Full person:", person)

# Add a new key-value pair
person["hobby"] = "coding"
print("After adding hobby:", person)

# Change an existing value
person["age"] = 31
print("After birthday:", person)

# Remove a key-value pair
del person["job"]
print("After removing job:", person)

# Check if a key exists
if "name" in person:
    print("Name is in the dictionary.")

if "salary" not in person:
    print("Salary is NOT in the dictionary.")

# Loop through a dictionary
print()
print("All info about this person:")
for key, value in person.items():
    print(f"  {key}: {value}")

# A more practical example — a phone book
phone_book = {
    "Alice": "555-0101",
    "Bob": "555-0102",
    "Charlie": "555-0103"
}

name = "Bob"
print(f"\n{name}'s number is {phone_book[name]}")

# ============================================================
# KEY CONCEPT:
#
# Use a LIST when you have an ordered collection of similar items.
#   Example: a list of scores, a list of names
#
# Use a DICTIONARY when you have labeled data.
#   Example: a person's details, a configuration, a lookup table
# ============================================================
